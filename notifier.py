import requests
import json
import logging
from datetime import datetime
from typing import Optional, Dict, List

logger = logging.getLogger(__name__)


class DingTalkNotifier:
    """钉钉通知推送类"""
    
    def __init__(self, webhook_url: str):
        """
        初始化钉钉通知器
        
        Args:
            webhook_url: 钉钉机器人Webhook地址
        """
        self.webhook_url = webhook_url
    
    def send_text(self, content: str, at_all: bool = False, at_mobiles: List[str] = None) -> bool:
        """
        发送文本消息
        
        Args:
            content: 消息内容
            at_all: 是否@所有人
            at_mobiles: @指定手机号列表
            
        Returns:
            是否发送成功
        """
        if not self.webhook_url:
            logger.error("钉钉Webhook地址未配置")
            return False
        
        data = {
            "msgtype": "text",
            "text": {
                "content": content
            },
            "at": {
                "atMobiles": at_mobiles or [],
                "isAtAll": at_all
            }
        }
        
        return self._send_request(data)
    
    def send_markdown(self, title: str, text: str, at_all: bool = False, at_mobiles: List[str] = None) -> bool:
        """
        发送Markdown消息
        
        Args:
            title: 消息标题
            text: Markdown格式的消息内容
            at_all: 是否@所有人
            at_mobiles: @指定手机号列表
            
        Returns:
            是否发送成功
        """
        if not self.webhook_url:
            logger.error("钉钉Webhook地址未配置")
            return False
        
        data = {
            "msgtype": "markdown",
            "markdown": {
                "title": title,
                "text": text
            },
            "at": {
                "atMobiles": at_mobiles or [],
                "isAtAll": at_all
            }
        }
        
        return self._send_request(data)
    
    def send_vulnerability_alert(self, task_name: str, url: str, change_info: Dict, 
                                  matched_keywords: List[str], priority: str = 'medium') -> bool:
        """
        发送漏洞预警消息
        
        Args:
            task_name: 任务名称
            url: 监控URL
            change_info: 变化信息
            matched_keywords: 匹配的关键词
            priority: 优先级
            
        Returns:
            是否发送成功
        """
        # 判断是否需要@所有人
        at_all = (priority == 'high' and matched_keywords)
        
        # 构建Markdown消息
        title = f"🚨 漏洞情报预警 - {task_name}"
        
        # 优先级emoji
        priority_emoji = {
            'high': '🔴',
            'medium': '🟡',
            'low': '🟢'
        }
        emoji = priority_emoji.get(priority, '🟡')
        
        text = f"""## {emoji} 漏洞情报预警

**来源**: {task_name}

**时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

**优先级**: {priority.upper()}

"""
        
        # 添加漏洞信息
        vuln_info = change_info.get('vulnerability_info', {})
        if vuln_info.get('cve_ids'):
            text += f"**CVE编号**: {', '.join(vuln_info['cve_ids'])}\n\n"
        if vuln_info.get('cnvd_ids'):
            text += f"**CNVD编号**: {', '.join(vuln_info['cnvd_ids'])}\n\n"
        if vuln_info.get('cnnvd_ids'):
            text += f"**CNNVD编号**: {', '.join(vuln_info['cnnvd_ids'])}\n\n"
        if vuln_info.get('cvss_scores'):
            text += f"**CVSS评分**: {', '.join(vuln_info['cvss_scores'])}\n\n"
        if vuln_info.get('severity_levels'):
            text += f"**风险等级**: {', '.join(set(vuln_info['severity_levels']))}\n\n"
        
        # 匹配的关键词
        if matched_keywords:
            text += f"**匹配关键词**: {', '.join(matched_keywords)}\n\n"
        
        # 变化摘要
        summary = change_info.get('summary', '')
        if summary:
            text += f"**变化摘要**:\n{summary}\n\n"
        
        # 链接
        text += f"**查看详情**: [{url}]({url})\n\n"
        
        # 高危提醒
        if at_all:
            text += "---\n\n@所有人 请相关团队立即响应！"
        
        return self.send_markdown(title, text, at_all=at_all)
    
    def send_simple_alert(self, task_name: str, url: str, summary: str) -> bool:
        """
        发送简单通知
        
        Args:
            task_name: 任务名称
            url: 监控URL
            summary: 变化摘要
            
        Returns:
            是否发送成功
        """
        title = f"📢 监控提醒 - {task_name}"
        
        text = f"""## 📢 内容变化提醒

**来源**: {task_name}

**时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

**变化摘要**:
{summary}

**查看详情**: [{url}]({url})
"""
        
        return self.send_markdown(title, text)
    
    def _send_request(self, data: Dict) -> bool:
        """
        发送HTTP请求到钉钉
        
        Args:
            data: 消息数据
            
        Returns:
            是否发送成功
        """
        try:
            headers = {'Content-Type': 'application/json'}
            response = requests.post(
                self.webhook_url,
                headers=headers,
                data=json.dumps(data),
                timeout=10
            )
            
            result = response.json()
            
            if result.get('errcode') == 0:
                logger.info("钉钉消息发送成功")
                return True
            else:
                logger.error(f"钉钉消息发送失败: {result.get('errmsg')}")
                return False
        
        except requests.RequestException as e:
            logger.error(f"发送钉钉消息时网络错误: {str(e)}")
            return False
        except Exception as e:
            logger.error(f"发送钉钉消息时发生错误: {str(e)}")
            return False


def create_notifier(webhook_url: str) -> Optional[DingTalkNotifier]:
    """
    创建钉钉通知器
    
    Args:
        webhook_url: Webhook地址
        
    Returns:
        DingTalkNotifier实例,如果URL无效返回None
    """
    if not webhook_url or not webhook_url.startswith('http'):
        logger.warning("无效的钉钉Webhook地址")
        return None
    
    return DingTalkNotifier(webhook_url)
