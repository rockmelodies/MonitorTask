from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from models import db, bcrypt, MonitorTask, ContentChange, NotificationLog, User
from config import Config
from functools import wraps
import os
import logging
from datetime import datetime

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# 创建Flask应用
app = Flask(__name__, static_folder='static')
app.config.from_object(Config)

# 初始化扩展
CORS(app, 
     resources={r"/api/*": {"origins": "*"}},
     supports_credentials=True,
     allow_headers=["Content-Type", "Authorization"],
     methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"])
db.init_app(app)
bcrypt.init_app(app)
jwt = JWTManager(app)

# 创建必要的目录
os.makedirs(Config.SCREENSHOT_DIR, exist_ok=True)
os.makedirs(Config.LOG_DIR, exist_ok=True)


# 权限装饰器
def admin_required(fn):
    """需要管理员权限"""
    @wraps(fn)
    @jwt_required()
    def wrapper(*args, **kwargs):
        current_user_id = int(get_jwt_identity())
        user = User.query.get(current_user_id)
        if not user or user.role != 'admin':
            return jsonify({'success': False, 'message': '需要管理员权限'}), 403
        return fn(*args, **kwargs)
    return wrapper


def user_or_admin_required(fn):
    """需要用户或管理员权限"""
    @wraps(fn)
    @jwt_required()
    def wrapper(*args, **kwargs):
        current_user_id = int(get_jwt_identity())
        user = User.query.get(current_user_id)
        if not user or user.role not in ['admin', 'user']:
            return jsonify({'success': False, 'message': '权限不足'}), 403
        return fn(*args, **kwargs)
    return wrapper


# ==================== 健康检查 ====================

@app.route('/api/health', methods=['GET'])
def health_check():
    """健康检查"""
    return jsonify({
        'success': True,
        'message': 'Service is running'
    })


# ==================== 用户认证 API ====================

@app.route('/api/auth/register', methods=['POST'])
def register():
    """用户注册"""
    try:
        data = request.get_json()
        
        if not data.get('username') or not data.get('password'):
            return jsonify({'success': False, 'message': '用户名和密码为必填项'}), 400
        
        # 检查用户名是否已存在
        if User.query.filter_by(username=data['username']).first():
            return jsonify({'success': False, 'message': '用户名已存在'}), 400
        
        # 检查邮箱是否已存在
        if data.get('email') and User.query.filter_by(email=data['email']).first():
            return jsonify({'success': False, 'message': '邮箱已被使用'}), 400
        
        # 创建用户
        user = User(
            username=data['username'],
            email=data.get('email'),
            role='user'  # 默认普通用户
        )
        user.set_password(data['password'])
        
        db.session.add(user)
        db.session.commit()
        
        logger.info(f"用户注册成功: {user.username}")
        
        return jsonify({
            'success': True,
            'message': '注册成功',
            'data': user.to_dict()
        }), 201
    
    except Exception as e:
        db.session.rollback()
        logger.error(f"用户注册失败: {str(e)}")
        return jsonify({'success': False, 'message': str(e)}), 500


@app.route('/api/auth/login', methods=['POST'])
def login():
    """用户登录"""
    try:
        data = request.get_json()
        
        if not data.get('username') or not data.get('password'):
            return jsonify({'success': False, 'message': '用户名和密码为必填项'}), 400
        
        user = User.query.filter_by(username=data['username']).first()
        
        if not user or not user.check_password(data['password']):
            return jsonify({'success': False, 'message': '用户名或密码错误'}), 401
        
        if not user.is_active:
            return jsonify({'success': False, 'message': '账户已被禁用'}), 403
        
        # 更新最后登录时间
        user.last_login = datetime.utcnow()
        db.session.commit()
        
        # 生成 JWT token
        access_token = create_access_token(identity=str(user.id))
        
        logger.info(f"用户登录成功: {user.username}")
        
        return jsonify({
            'success': True,
            'message': '登录成功',
            'data': {
                'token': access_token,
                'user': user.to_dict()
            }
        })
    
    except Exception as e:
        logger.error(f"用户登录失败: {str(e)}")
        return jsonify({'success': False, 'message': str(e)}), 500


@app.route('/api/auth/me', methods=['GET'])
@jwt_required()
def get_current_user():
    """获取当前用户信息"""
    try:
        current_user_id = int(get_jwt_identity())
        user = User.query.get(current_user_id)
        
        if not user:
            return jsonify({'success': False, 'message': '用户不存在'}), 404
        
        return jsonify({
            'success': True,
            'data': user.to_dict()
        })
    
    except Exception as e:
        logger.error(f"获取用户信息失败: {str(e)}")
        return jsonify({'success': False, 'message': str(e)}), 500


# ==================== 用户管理 API ====================

@app.route('/api/users', methods=['GET'])
@admin_required
def get_users():
    """获取所有用户(仅管理员)"""
    try:
        users = User.query.order_by(User.created_at.desc()).all()
        return jsonify({
            'success': True,
            'data': [user.to_dict() for user in users]
        })
    except Exception as e:
        logger.error(f"获取用户列表失败: {str(e)}")
        return jsonify({'success': False, 'message': str(e)}), 500


@app.route('/api/users/<int:user_id>', methods=['PUT'])
@admin_required
def update_user(user_id):
    """更新用户(仅管理员)"""
    try:
        user = User.query.get_or_404(user_id)
        data = request.get_json()
        
        if 'email' in data:
            user.email = data['email']
        if 'role' in data:
            user.role = data['role']
        if 'is_active' in data:
            user.is_active = data['is_active']
        if 'password' in data and data['password']:
            user.set_password(data['password'])
        
        db.session.commit()
        
        logger.info(f"更新用户成功: {user.username}")
        
        return jsonify({
            'success': True,
            'data': user.to_dict(),
            'message': '用户更新成功'
        })
    
    except Exception as e:
        db.session.rollback()
        logger.error(f"更新用户失败: {str(e)}")
        return jsonify({'success': False, 'message': str(e)}), 500


@app.route('/api/users/<int:user_id>', methods=['DELETE'])
@admin_required
def delete_user(user_id):
    """删除用户(仅管理员)"""
    try:
        user = User.query.get_or_404(user_id)
        username = user.username
        
        db.session.delete(user)
        db.session.commit()
        
        logger.info(f"删除用户成功: {username}")
        
        return jsonify({
            'success': True,
            'message': '用户删除成功'
        })
    
    except Exception as e:
        db.session.rollback()
        logger.error(f"删除用户失败: {str(e)}")
        return jsonify({'success': False, 'message': str(e)}), 500


# ==================== 监控任务 API ====================


@app.route('/api/tasks', methods=['GET'])
@jwt_required()
def get_tasks():
    """获取所有监控任务"""
    try:
        tasks = MonitorTask.query.order_by(MonitorTask.created_at.desc()).all()
        return jsonify({
            'success': True,
            'data': [task.to_dict() for task in tasks]
        })
    except Exception as e:
        logger.error(f"获取任务列表失败: {str(e)}")
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@app.route('/api/tasks', methods=['POST'])
@user_or_admin_required
def create_task():
    """创建监控任务"""
    try:
        data = request.get_json()
        
        # 验证必填字段
        if not data.get('name') or not data.get('url'):
            return jsonify({
                'success': False,
                'message': '任务名称和URL为必填项'
            }), 400
        
        # 创建任务
        task = MonitorTask(
            name=data.get('name'),
            url=data.get('url'),
            check_interval=data.get('check_interval', Config.DEFAULT_CHECK_INTERVAL),
            selector=data.get('selector'),
            keywords=','.join(data.get('keywords', [])) if isinstance(data.get('keywords'), list) else data.get('keywords'),
            dingtalk_webhook=data.get('dingtalk_webhook'),
            priority=data.get('priority', 'medium'),
            tags=','.join(data.get('tags', [])) if isinstance(data.get('tags'), list) else data.get('tags'),
            is_active=data.get('is_active', True)
        )
        
        db.session.add(task)
        db.session.commit()
        
        logger.info(f"创建监控任务成功: {task.name} (ID: {task.id})")
        
        return jsonify({
            'success': True,
            'data': task.to_dict(),
            'message': '任务创建成功'
        }), 201
    
    except Exception as e:
        db.session.rollback()
        logger.error(f"创建任务失败: {str(e)}")
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@app.route('/api/tasks/<int:task_id>', methods=['GET'])
@jwt_required()
def get_task(task_id):
    """获取单个任务详情"""
    try:
        task = MonitorTask.query.get_or_404(task_id)
        return jsonify({
            'success': True,
            'data': task.to_dict()
        })
    except Exception as e:
        logger.error(f"获取任务失败: {str(e)}")
        return jsonify({
            'success': False,
            'message': str(e)
        }), 404


@app.route('/api/tasks/<int:task_id>', methods=['PUT'])
@user_or_admin_required
def update_task(task_id):
    """更新监控任务"""
    try:
        task = MonitorTask.query.get_or_404(task_id)
        data = request.get_json()
        
        # 更新字段
        if 'name' in data:
            task.name = data['name']
        if 'url' in data:
            task.url = data['url']
        if 'check_interval' in data:
            task.check_interval = data['check_interval']
        if 'selector' in data:
            task.selector = data['selector']
        if 'keywords' in data:
            task.keywords = ','.join(data['keywords']) if isinstance(data['keywords'], list) else data['keywords']
        if 'dingtalk_webhook' in data:
            task.dingtalk_webhook = data['dingtalk_webhook']
        if 'priority' in data:
            task.priority = data['priority']
        if 'tags' in data:
            task.tags = ','.join(data['tags']) if isinstance(data['tags'], list) else data['tags']
        if 'is_active' in data:
            task.is_active = data['is_active']
        
        db.session.commit()
        
        logger.info(f"更新监控任务成功: {task.name} (ID: {task.id})")
        
        return jsonify({
            'success': True,
            'data': task.to_dict(),
            'message': '任务更新成功'
        })
    
    except Exception as e:
        db.session.rollback()
        logger.error(f"更新任务失败: {str(e)}")
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@app.route('/api/tasks/<int:task_id>', methods=['DELETE'])
@user_or_admin_required
def delete_task(task_id):
    """删除监控任务"""
    try:
        task = MonitorTask.query.get_or_404(task_id)
        task_name = task.name
        
        db.session.delete(task)
        db.session.commit()
        
        logger.info(f"删除监控任务成功: {task_name} (ID: {task_id})")
        
        return jsonify({
            'success': True,
            'message': '任务删除成功'
        })
    
    except Exception as e:
        db.session.rollback()
        logger.error(f"删除任务失败: {str(e)}")
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@app.route('/api/tasks/<int:task_id>/changes', methods=['GET'])
def get_task_changes(task_id):
    """获取任务的变化记录"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        
        task = MonitorTask.query.get_or_404(task_id)
        
        pagination = ContentChange.query.filter_by(task_id=task_id)\
            .order_by(ContentChange.detected_at.desc())\
            .paginate(page=page, per_page=per_page, error_out=False)
        
        return jsonify({
            'success': True,
            'data': {
                'changes': [change.to_dict() for change in pagination.items],
                'total': pagination.total,
                'page': page,
                'per_page': per_page,
                'pages': pagination.pages
            }
        })
    
    except Exception as e:
        logger.error(f"获取变化记录失败: {str(e)}")
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@app.route('/api/changes', methods=['GET'])
def get_all_changes():
    """获取所有变化记录"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        
        pagination = ContentChange.query\
            .order_by(ContentChange.detected_at.desc())\
            .paginate(page=page, per_page=per_page, error_out=False)
        
        return jsonify({
            'success': True,
            'data': {
                'changes': [change.to_dict() for change in pagination.items],
                'total': pagination.total,
                'page': page,
                'per_page': per_page,
                'pages': pagination.pages
            }
        })
    
    except Exception as e:
        logger.error(f"获取变化记录失败: {str(e)}")
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@app.route('/api/stats', methods=['GET'])
@jwt_required()
def get_stats():
    """获取统计信息"""
    try:
        total_tasks = MonitorTask.query.count()
        active_tasks = MonitorTask.query.filter_by(is_active=True).count()
        total_changes = ContentChange.query.count()
        total_notifications = NotificationLog.query.count()
        
        # 最近24小时的变化数
        from datetime import datetime, timedelta
        yesterday = datetime.utcnow() - timedelta(days=1)
        recent_changes = ContentChange.query.filter(ContentChange.detected_at >= yesterday).count()
        
        return jsonify({
            'success': True,
            'data': {
                'total_tasks': total_tasks,
                'active_tasks': active_tasks,
                'total_changes': total_changes,
                'recent_changes': recent_changes,
                'total_notifications': total_notifications
            }
        })
    
    except Exception as e:
        logger.error(f"获取统计信息失败: {str(e)}")
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


# ==================== 静态文件服务 ====================
# 必须放在最后,避免拦截API路由

@app.route('/')
def index():
    """首页"""
    return send_from_directory(app.static_folder, 'index.html')


@app.route('/assets/<path:filename>')
def assets(filename):
    """静态资源"""
    return send_from_directory(os.path.join(app.static_folder, 'assets'), filename)


@app.route('/<path:filename>')
def static_files(filename):
    """其他静态文件"""
    # 排除API路由
    if filename.startswith('api/'):
        return jsonify({'error': 'Not found'}), 404
    
    file_path = os.path.join(app.static_folder, filename)
    if os.path.exists(file_path) and os.path.isfile(file_path):
        return send_from_directory(app.static_folder, filename)
    else:
        # SPA路由,返回index.html
        return send_from_directory(app.static_folder, 'index.html')


# 初始化数据库
with app.app_context():
    db.create_all()
    
    # 创建默认管理员账户
    admin = User.query.filter_by(username='admin').first()
    if not admin:
        admin = User(
            username='admin',
            email='admin@monitortask.com',
            role='admin'
        )
        admin.set_password('admin123')  # 默认密码
        db.session.add(admin)
        db.session.commit()
        logger.info("默认管理员账户已创建: admin/admin123")
    
    logger.info("数据库初始化完成")


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
