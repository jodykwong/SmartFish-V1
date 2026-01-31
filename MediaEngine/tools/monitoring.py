"""基础监控和日志"""

import logging
import time
from functools import wraps
from typing import Callable
from datetime import datetime

# 结构化日志配置
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

logger = logging.getLogger('smartfish.trilayer')

class Metrics:
    """简单指标收集器"""
    
    def __init__(self):
        self.counters = {
            'requests_total': 0,
            'requests_success': 0,
            'requests_failed': 0,
            'tier1_calls': 0,
            'tier2_calls': 0,
            'tier3_calls': 0
        }
        self.timings = []
    
    def increment(self, counter: str):
        """增加计数器"""
        if counter in self.counters:
            self.counters[counter] += 1
    
    def record_timing(self, duration: float):
        """记录响应时间"""
        self.timings.append(duration)
        if len(self.timings) > 1000:
            self.timings = self.timings[-1000:]
    
    def get_stats(self):
        """获取统计信息"""
        avg_time = sum(self.timings) / len(self.timings) if self.timings else 0
        return {
            **self.counters,
            'avg_response_time': round(avg_time, 3),
            'p95_response_time': self._percentile(95) if self.timings else 0
        }
    
    def _percentile(self, p: int) -> float:
        """计算百分位数"""
        sorted_times = sorted(self.timings)
        index = int(len(sorted_times) * p / 100)
        return round(sorted_times[index], 3) if index < len(sorted_times) else 0

# 全局指标实例
metrics = Metrics()

def monitor_request(tier: str = None):
    """请求监控装饰器"""
    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            start_time = time.time()
            metrics.increment('requests_total')
            
            if tier:
                metrics.increment(f'{tier}_calls')
            
            try:
                result = await func(*args, **kwargs)
                metrics.increment('requests_success')
                
                duration = time.time() - start_time
                metrics.record_timing(duration)
                
                logger.info(f"{func.__name__} completed in {duration:.3f}s")
                return result
                
            except Exception as e:
                metrics.increment('requests_failed')
                logger.error(f"{func.__name__} failed: {str(e)}", exc_info=True)
                raise
        
        return wrapper
    return decorator
