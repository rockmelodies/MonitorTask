"""
MonitorTask - 漏洞情报监控平台启动脚本
"""
from app import app
from scheduler import MonitorScheduler
import logging
import signal
import sys

logger = logging.getLogger(__name__)

# 创建调度器实例
scheduler = MonitorScheduler(app)


def signal_handler(sig, frame):
    """处理退出信号"""
    logger.info("接收到退出信号,正在关闭...")
    scheduler.stop()
    sys.exit(0)


# 注册信号处理
signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)


if __name__ == '__main__':
    try:
        # 启动调度器
        scheduler.start()
        logger.info("="*50)
        logger.info("MonitorTask 漏洞情报监控平台已启动")
        logger.info("Web界面: http://localhost:5000")
        logger.info("按 Ctrl+C 停止服务")
        logger.info("="*50)
        
        # 启动Flask应用
        app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False)
    
    except Exception as e:
        logger.error(f"启动失败: {str(e)}")
        scheduler.stop()
        sys.exit(1)
