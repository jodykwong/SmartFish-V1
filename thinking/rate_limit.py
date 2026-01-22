"""
速率限制配置
防止 API 滥用和 DDoS 攻击
"""
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

def init_limiter(app):
    """初始化速率限制器"""
    limiter = Limiter(
        app=app,
        key_func=get_remote_address,
        default_limits=["200 per day", "50 per hour"],
        storage_uri="memory://",
    )
    return limiter

# 速率限制装饰器
# 使用示例:
# @limiter.limit("10 per minute")
# def api_endpoint():
#     pass
