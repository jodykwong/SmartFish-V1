"""
数据库初始化模块
解决循环导入问题：app.py -> thinking -> models -> app.db
"""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def init_db(app):
    """初始化数据库"""
    db.init_app(app)
    return db
