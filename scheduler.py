from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from datetime import datetime
from models import db, MonitorTask, ContentChange, NotificationLog
from monitor_engine import ContentMonitor
from notifier import create_notifier
import logging

logger = logging.getLogger(__name__)


class MonitorScheduler:
    """监控任务调度器"""
    
    def __init__(self, app):
        """
        初始化调度器
        
        Args:
            app: Flask应用实例
        """
        self.app = app
        self.scheduler = BackgroundScheduler()
        self.monitor = ContentMonitor()
        self.running_tasks = set()
    
    def start(self):
        """启动调度器"""
        # 添加定期检查任务的作业
        self.scheduler.add_job(
            func=self.check_all_tasks,
            trigger=IntervalTrigger(seconds=60),  # 每分钟检查一次
            id='check_tasks',
            name='检查所有监控任务',
            replace_existing=True
        )
        
        self.scheduler.start()
        logger.info("监控调度器已启动")
    
    def stop(self):
        """停止调度器"""
        if self.scheduler.running:
            self.scheduler.shutdown()
            logger.info("监控调度器已停止")
    
    def check_all_tasks(self):
        """检查所有激活的监控任务"""
        with self.app.app_context():
            try:
                # 获取所有激活的任务
                tasks = MonitorTask.query.filter_by(is_active=True).all()
                
                current_time = datetime.utcnow()
                
                for task in tasks:
                    # 检查是否到达检查时间
                    if self._should_check(task, current_time):
                        # 避免重复执行
                        if task.id not in self.running_tasks:
                            self.running_tasks.add(task.id)
                            try:
                                self._check_task(task)
                            finally:
                                self.running_tasks.discard(task.id)
            
            except Exception as e:
                logger.error(f"检查任务时发生错误: {str(e)}")
    
    def _should_check(self, task: MonitorTask, current_time: datetime) -> bool:
        """
        判断任务是否应该执行检查
        
        Args:
            task: 监控任务
            current_time: 当前时间
            
        Returns:
            是否应该检查
        """
        if task.last_check_time is None:
            return True
        
        # 计算距离上次检查的时间(秒)
        elapsed = (current_time - task.last_check_time).total_seconds()
        
        return elapsed >= task.check_interval
    
    def _check_task(self, task: MonitorTask):
        """
        执行单个任务的检查
        
        Args:
            task: 监控任务
        """
        logger.info(f"开始检查任务: {task.name} (ID: {task.id})")
        
        try:
            # 1. 抓取内容
            content = self.monitor.fetch_content(task.url, task.selector)
            
            if content is None:
                logger.warning(f"任务 {task.name} 抓取内容失败")
                return
            
            # 2. 检测变化
            changed, new_hash = self.monitor.detect_change(task.last_content_hash, content)
            
            # 更新最后检查时间和哈希
            task.last_check_time = datetime.utcnow()
            task.last_content_hash = new_hash
            db.session.commit()
            
            if not changed:
                logger.info(f"任务 {task.name} 内容未变化")
                return
            
            logger.info(f"任务 {task.name} 检测到内容变化")
            
            # 3. 提取关键词
            keywords = task.keywords.split(',') if task.keywords else []
            matched_keywords = self.monitor.extract_keywords(content, keywords)
            
            # 4. 生成摘要
            summary = self.monitor.generate_summary(content)
            
            # 5. 提取漏洞信息
            vuln_info = self.monitor.extract_vulnerability_info(content)
            
            # 6. 保存变化记录
            change = ContentChange(
                task_id=task.id,
                content_hash=new_hash,
                change_summary=summary,
                change_detail=content[:5000],  # 保存前5000字符
                matched_keywords=','.join(matched_keywords) if matched_keywords else None
            )
            db.session.add(change)
            db.session.commit()
            
            # 7. 发送通知
            if task.dingtalk_webhook:
                self._send_notification(task, change, summary, matched_keywords, vuln_info)
            else:
                logger.warning(f"任务 {task.name} 未配置钉钉Webhook,跳过通知")
        
        except Exception as e:
            logger.error(f"检查任务 {task.name} 时发生错误: {str(e)}")
            db.session.rollback()
    
    def _send_notification(self, task: MonitorTask, change: ContentChange, 
                          summary: str, matched_keywords: list, vuln_info: dict):
        """
        发送通知
        
        Args:
            task: 监控任务
            change: 变化记录
            summary: 摘要
            matched_keywords: 匹配的关键词
            vuln_info: 漏洞信息
        """
        try:
            notifier = create_notifier(task.dingtalk_webhook)
            
            if notifier is None:
                logger.error(f"任务 {task.name} 钉钉通知器创建失败")
                return
            
            # 构建变化信息
            change_info = {
                'summary': summary,
                'vulnerability_info': vuln_info
            }
            
            # 根据是否匹配关键词选择不同的通知方式
            if matched_keywords:
                success = notifier.send_vulnerability_alert(
                    task_name=task.name,
                    url=task.url,
                    change_info=change_info,
                    matched_keywords=matched_keywords,
                    priority=task.priority
                )
            else:
                success = notifier.send_simple_alert(
                    task_name=task.name,
                    url=task.url,
                    summary=summary
                )
            
            # 记录通知日志
            log = NotificationLog(
                task_id=task.id,
                change_id=change.id,
                notification_type='dingtalk',
                status='success' if success else 'failed',
                error_message=None if success else '发送失败'
            )
            db.session.add(log)
            
            # 更新变化记录的通知状态
            change.is_notified = success
            
            db.session.commit()
            
            if success:
                logger.info(f"任务 {task.name} 通知发送成功")
            else:
                logger.error(f"任务 {task.name} 通知发送失败")
        
        except Exception as e:
            logger.error(f"发送通知时发生错误: {str(e)}")
            db.session.rollback()
    
    def trigger_task_check(self, task_id: int):
        """
        手动触发任务检查
        
        Args:
            task_id: 任务ID
        """
        with self.app.app_context():
            try:
                task = MonitorTask.query.get(task_id)
                if task and task.is_active:
                    self._check_task(task)
                    logger.info(f"手动触发任务检查完成: {task.name}")
                else:
                    logger.warning(f"任务 {task_id} 不存在或未激活")
            except Exception as e:
                logger.error(f"手动触发任务检查失败: {str(e)}")
