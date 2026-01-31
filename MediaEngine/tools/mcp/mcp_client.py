"""MCP 客户端基础类"""

import asyncio
import json
from typing import Dict, List, Any, Optional
from abc import ABC, abstractmethod

class MCPClient(ABC):
    """MCP 客户端基础类"""
    
    def __init__(self, platform: str):
        self.platform = platform
        self.session = None
    
    async def __aenter__(self):
        """异步上下文管理器入口"""
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """异步上下文管理器出口"""
        if self.session:
            await self.session.close()
    
    @abstractmethod
    async def search(self, query: str, limit: int = 20) -> List[Dict[str, Any]]:
        """搜索内容"""
        pass
    
    @abstractmethod
    async def get_comments(self, post_id: str, limit: int = 50) -> List[Dict[str, Any]]:
        """获取评论"""
        pass
    
    def normalize_data(self, raw_data: Dict[str, Any]) -> Dict[str, Any]:
        """标准化数据格式"""
        return {
            'source': self.platform,
            'url': raw_data.get('url', ''),
            'raw_content': raw_data.get('content', ''),
            'author': raw_data.get('author', ''),
            'publish_time': raw_data.get('timestamp', 0),
            'meta': raw_data
        }
