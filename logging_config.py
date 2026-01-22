"""
结构化日志配置
JSON 格式，便于日志聚合和分析
"""
import logging
import json
import sys
from datetime import datetime

class JSONFormatter(logging.Formatter):
    """JSON 格式化器"""
    
    def format(self, record):
        log_data = {
            'timestamp': datetime.utcnow().isoformat(),
            'level': record.levelname,
            'logger': record.name,
            'message': record.getMessage(),
            'module': record.module,
            'function': record.funcName,
            'line': record.lineno
        }
        
        if record.exc_info:
            log_data['exception'] = self.formatException(record.exc_info)
        
        return json.dumps(log_data)

def setup_logging(app):
    """配置应用日志"""
    # JSON 日志处理器
    json_handler = logging.StreamHandler(sys.stdout)
    json_handler.setFormatter(JSONFormatter())
    json_handler.setLevel(logging.INFO)
    
    # 配置根日志
    app.logger.addHandler(json_handler)
    app.logger.setLevel(logging.INFO)
    
    return app.logger
