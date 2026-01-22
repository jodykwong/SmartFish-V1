"""
Prometheus 监控集成
导出应用指标
"""
from prometheus_flask_exporter import PrometheusMetrics

def init_metrics(app):
    """初始化 Prometheus 指标"""
    metrics = PrometheusMetrics(app)
    
    # 自定义指标
    metrics.info('app_info', 'Application info', version='1.0.1')
    
    return metrics
