"""
SmartFish 版本管理模块
提供版本信息获取和管理功能
"""

import os
from pathlib import Path

class VersionManager:
    def __init__(self):
        self.version_file = Path(__file__).parent / "VERSION"
        
    def get_version(self):
        """获取当前版本号"""
        try:
            return self.version_file.read_text().strip()
        except FileNotFoundError:
            return "1.0.0"
    
    def get_version_info(self):
        """获取详细版本信息"""
        return {
            "version": self.get_version(),
            "name": "SmartFish",
            "description": "智能舆情分析系统"
        }

# 全局版本管理器实例
version_manager = VersionManager()
