"""
MCP客户端包 - MediaEngine集成

提供中国主流社交媒体平台的MCP客户端集成：
- 小红书 (xiaohongshu)
- 微博 (weibo)
- 知乎 (zhihu)
- B站 (bilibili)
- 抖音 (douyin)
- 多平台综合 (video_sum)

迁移自: mcp_clients/
"""

from .base import (
    BaseMCPClient,
    MCPSearchResult,
    MCPResponse,
    DataSourceRouter,
    get_router,
    init_router
)

# 三层架构简化客户端
from .mcp_client import MCPClient
from .weibo_mcp import WeiboMCP
from .douyin_mcp import DouyinMCP

__all__ = [
    # 基类
    "BaseMCPClient",
    "MCPSearchResult", 
    "MCPResponse",
    "DataSourceRouter",
    "get_router",
    "init_router",
    # 简化客户端
    "MCPClient",
    "WeiboMCP",
    "DouyinMCP",
]

# 延迟导入平台客户端（避免循环依赖）
def get_xiaohongshu_client():
    """获取小红书客户端"""
    from .clients.xiaohongshu import XiaohongshuMCPClient
    return XiaohongshuMCPClient

def get_weibo_client():
    """获取微博客户端"""
    from .clients.weibo import WeiboMCPClient
    return WeiboMCPClient

def get_zhihu_client():
    """获取知乎客户端"""
    from .clients.zhihu import ZhihuMCPClient
    return ZhihuMCPClient

def get_bilibili_client():
    """获取B站客户端"""
    from .clients.bilibili import BilibiliMCPClient
    return BilibiliMCPClient

def get_douyin_client():
    """获取抖音客户端"""
    from .clients.douyin import DouyinMCPClient
    return DouyinMCPClient

def get_video_sum_client():
    """获取多平台综合客户端"""
    from .clients.video_sum import VideoSumMCPClient
    return VideoSumMCPClient
