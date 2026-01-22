"""
健康检查端点
提供系统健康状态和就绪状态
"""
from flask import Blueprint, jsonify
from database import db
import time

health_bp = Blueprint('health', __name__)

@health_bp.route('/health', methods=['GET'])
def health_check():
    """基础健康检查 - 应用是否运行"""
    return jsonify({
        'status': 'healthy',
        'timestamp': time.time()
    }), 200

@health_bp.route('/ready', methods=['GET'])
def readiness_check():
    """就绪检查 - 应用是否准备好接收流量"""
    checks = {
        'database': check_database(),
        'application': True
    }
    
    all_ready = all(checks.values())
    status_code = 200 if all_ready else 503
    
    return jsonify({
        'status': 'ready' if all_ready else 'not_ready',
        'checks': checks,
        'timestamp': time.time()
    }), status_code

def check_database():
    """检查数据库连接"""
    try:
        # 简单查询测试连接
        db.session.execute(db.text('SELECT 1'))
        return True
    except Exception:
        return False
