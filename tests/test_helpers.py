"""
Flask App Context 测试辅助工具
提供测试用的 Flask 应用和数据库
"""
import sys
sys.path.insert(0, '.')

from flask import Flask
from database import db

def create_test_app():
    """创建测试用 Flask 应用"""
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'test-secret-key'
    
    # 初始化数据库
    db.init_app(app)
    
    # 注册健康检查
    from health import health_bp
    app.register_blueprint(health_bp)
    
    with app.app_context():
        db.create_all()
    
    return app

def get_test_client(app):
    """获取测试客户端"""
    return app.test_client()

def get_authenticated_client(app, user_id=1):
    """获取已认证的测试客户端"""
    client = app.test_client()
    with client.session_transaction() as sess:
        sess['user_id'] = user_id
    return client
