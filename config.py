import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """应用配置类"""
    
    # Flask配置
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-please-change-in-production')
    FLASK_ENV = os.getenv('FLASK_ENV', 'development')
    
    # 数据库配置
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///monitor.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # 监控配置
    DEFAULT_CHECK_INTERVAL = int(os.getenv('DEFAULT_CHECK_INTERVAL', 300))  # 默认5分钟
    MAX_CONCURRENT_TASKS = int(os.getenv('MAX_CONCURRENT_TASKS', 100))
    REQUEST_TIMEOUT = int(os.getenv('REQUEST_TIMEOUT', 30))
    
    # 钉钉配置
    DEFAULT_DINGTALK_WEBHOOK = os.getenv('DEFAULT_DINGTALK_WEBHOOK', '')
    
    # 截图配置
    SCREENSHOT_DIR = 'screenshots'
    
    # 日志配置
    LOG_DIR = 'logs'
    LOG_LEVEL = 'INFO'
    
    # JWT配置
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'jwt-secret-key-please-change')
    JWT_ACCESS_TOKEN_EXPIRES = 86400  # 24小时
