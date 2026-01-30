"""
MCP客户端包 (已迁移)

⚠️ 已弃用警告: 此模块已迁移至 MediaEngine.tools.mcp
请更新您的导入语句:

    # 旧 (已弃用)
    from mcp_clients import DataSourceRouter
    from mcp_clients.xiaohongshu import XiaohongshuMCPClient
    
    # 新
    from MediaEngine.tools.mcp import DataSourceRouter
    from MediaEngine.tools.mcp.clients.xiaohongshu import XiaohongshuMCPClient

此兼容性转发将在未来版本中移除。
"""

import warnings

warnings.warn(
    "mcp_clients 模块已迁移至 MediaEngine.tools.mcp，"
    "请更新您的导入路径。此兼容性转发将在未来版本中移除。",
    DeprecationWarning,
    stacklevel=2
)

# 兼容性转发：从新位置导入所有内容
from MediaEngine.tools.mcp import (
    BaseMCPClient,
    MCPSearchResult,
    MCPResponse,
    DataSourceRouter,
    get_router,
    init_router,
    get_xiaohongshu_client,
    get_weibo_client,
    get_zhihu_client,
    get_bilibili_client,
    get_douyin_client,
    get_video_sum_client,
)

__all__ = [
    "BaseMCPClient",
    "MCPSearchResult",
    "MCPResponse",
    "DataSourceRouter",
    "get_router",
    "init_router",
    "get_xiaohongshu_client",
    "get_weibo_client",
    "get_zhihu_client",
    "get_bilibili_client",
    "get_douyin_client",
    "get_video_sum_client",
]
