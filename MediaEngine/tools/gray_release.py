"""灰度发布配置"""

import random
from typing import Optional

class GrayReleaseConfig:
    """灰度发布控制器"""
    
    def __init__(self, percentage: int = 0):
        """
        Args:
            percentage: 灰度流量百分比 (0-100)
        """
        self.percentage = max(0, min(100, percentage))
        self.enabled = percentage > 0
    
    def should_use_new_version(self, user_id: Optional[str] = None) -> bool:
        """判断是否使用新版本"""
        if not self.enabled:
            return False
        
        if user_id:
            # 基于用户 ID 的稳定哈希
            hash_value = hash(user_id) % 100
            return hash_value < self.percentage
        else:
            # 随机分配
            return random.randint(0, 99) < self.percentage
    
    def set_percentage(self, percentage: int):
        """动态调整灰度比例"""
        self.percentage = max(0, min(100, percentage))
        self.enabled = percentage > 0

# 全局灰度配置
gray_release = GrayReleaseConfig(percentage=0)  # 默认关闭
