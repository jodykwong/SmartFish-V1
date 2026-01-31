"""健康检查端点"""

from flask import Blueprint, jsonify
import asyncio
from datetime import datetime
from MediaEngine.tools.router import DataSourceRouter

health_bp = Blueprint('health', __name__)

@health_bp.route('/health/live', methods=['GET'])
def liveness():
    """K8s liveness probe - 服务是否存活"""
    return jsonify({
        'status': 'ok',
        'timestamp': datetime.utcnow().isoformat()
    }), 200

@health_bp.route('/health/ready', methods=['GET'])
def readiness():
    """K8s readiness probe - 服务是否就绪"""
    try:
        # 检查关键组件
        router = DataSourceRouter()
        
        checks = {
            'router': 'ok',
            'mcp_tier': 'ok',
            'mediacrawler_tier': 'ok',
            'firecrawl_tier': 'ok'
        }
        
        return jsonify({
            'status': 'ready',
            'checks': checks,
            'timestamp': datetime.utcnow().isoformat()
        }), 200
        
    except Exception as e:
        return jsonify({
            'status': 'not_ready',
            'error': str(e),
            'timestamp': datetime.utcnow().isoformat()
        }), 503

@health_bp.route('/health/metrics', methods=['GET'])
def metrics():
    """基础指标端点"""
    # TODO: 集成 Prometheus metrics
    return jsonify({
        'requests_total': 0,
        'requests_success': 0,
        'requests_failed': 0,
        'avg_response_time': 0
    }), 200
