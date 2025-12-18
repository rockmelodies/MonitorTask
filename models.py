from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from datetime import datetime

db = SQLAlchemy()
bcrypt = Bcrypt()


class MonitorTask(db.Model):
    """监控任务模型"""
    __tablename__ = 'monitor_tasks'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False, comment='任务名称')
    url = db.Column(db.String(500), nullable=False, comment='监控URL')
    check_interval = db.Column(db.Integer, default=300, comment='检查间隔(秒)')
    selector = db.Column(db.String(500), comment='CSS选择器')
    keywords = db.Column(db.Text, comment='关键词,逗号分隔')
    dingtalk_webhook = db.Column(db.String(500), comment='钉钉Webhook地址')
    priority = db.Column(db.String(20), default='medium', comment='优先级: low/medium/high')
    tags = db.Column(db.String(200), comment='标签,逗号分隔')
    is_active = db.Column(db.Boolean, default=True, comment='是否启用')
    last_check_time = db.Column(db.DateTime, comment='最后检查时间')
    last_content_hash = db.Column(db.String(64), comment='最后内容哈希')
    created_at = db.Column(db.DateTime, default=datetime.utcnow, comment='创建时间')
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, comment='更新时间')
    
    # 关系
    changes = db.relationship('ContentChange', backref='task', lazy='dynamic', cascade='all, delete-orphan')
    
    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'name': self.name,
            'url': self.url,
            'check_interval': self.check_interval,
            'selector': self.selector,
            'keywords': self.keywords.split(',') if self.keywords else [],
            'dingtalk_webhook': self.dingtalk_webhook,
            'priority': self.priority,
            'tags': self.tags.split(',') if self.tags else [],
            'is_active': self.is_active,
            'last_check_time': self.last_check_time.isoformat() if self.last_check_time else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


class ContentChange(db.Model):
    """内容变化记录模型"""
    __tablename__ = 'content_changes'
    
    id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.Integer, db.ForeignKey('monitor_tasks.id'), nullable=False, comment='任务ID')
    content_hash = db.Column(db.String(64), nullable=False, comment='内容哈希')
    change_summary = db.Column(db.Text, comment='变化摘要')
    change_detail = db.Column(db.Text, comment='变化详情')
    screenshot_path = db.Column(db.String(500), comment='截图路径')
    is_notified = db.Column(db.Boolean, default=False, comment='是否已通知')
    matched_keywords = db.Column(db.String(500), comment='匹配的关键词')
    detected_at = db.Column(db.DateTime, default=datetime.utcnow, comment='检测时间')
    
    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'task_id': self.task_id,
            'content_hash': self.content_hash,
            'change_summary': self.change_summary,
            'change_detail': self.change_detail,
            'screenshot_path': self.screenshot_path,
            'is_notified': self.is_notified,
            'matched_keywords': self.matched_keywords.split(',') if self.matched_keywords else [],
            'detected_at': self.detected_at.isoformat() if self.detected_at else None
        }


class NotificationLog(db.Model):
    """通知日志模型"""
    __tablename__ = 'notification_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.Integer, db.ForeignKey('monitor_tasks.id'), comment='任务ID')
    change_id = db.Column(db.Integer, db.ForeignKey('content_changes.id'), comment='变化记录ID')
    notification_type = db.Column(db.String(50), default='dingtalk', comment='通知类型')
    status = db.Column(db.String(20), comment='状态: success/failed')
    error_message = db.Column(db.Text, comment='错误信息')
    sent_at = db.Column(db.DateTime, default=datetime.utcnow, comment='发送时间')
    
    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'task_id': self.task_id,
            'change_id': self.change_id,
            'notification_type': self.notification_type,
            'status': self.status,
            'error_message': self.error_message,
            'sent_at': self.sent_at.isoformat() if self.sent_at else None
        }


class User(db.Model):
    """用户模型"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, comment='用户名')
    password_hash = db.Column(db.String(128), nullable=False, comment='密码哈希')
    email = db.Column(db.String(120), unique=True, comment='邮箱')
    role = db.Column(db.String(20), default='user', comment='角色: admin/user/viewer')
    is_active = db.Column(db.Boolean, default=True, comment='是否激活')
    created_at = db.Column(db.DateTime, default=datetime.utcnow, comment='创建时间')
    last_login = db.Column(db.DateTime, comment='最后登录时间')
    
    # 通知设置
    email_notify_enabled = db.Column(db.Boolean, default=False, comment='是否启用邮箱通知')
    wechat_notify_enabled = db.Column(db.Boolean, default=False, comment='是否启用微信通知')
    wechat_webhook = db.Column(db.String(500), comment='企业微信Webhook地址')
    
    def set_password(self, password):
        """设置密码"""
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
    
    def check_password(self, password):
        """验证密码"""
        return bcrypt.check_password_hash(self.password_hash, password)
    
    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'role': self.role,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'last_login': self.last_login.isoformat() if self.last_login else None,
            'email_notify_enabled': self.email_notify_enabled,
            'wechat_notify_enabled': self.wechat_notify_enabled,
            'wechat_webhook': self.wechat_webhook
        }
