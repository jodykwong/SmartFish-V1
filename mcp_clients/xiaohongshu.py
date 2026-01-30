"""
兼容性转发模块: mcp_clients.xiaohongshu -> MediaEngine.tools.mcp.clients.xiaohongshu

⚠️ 已弃用: 请更新您的导入路径
"""
import warnings
warnings.warn(
    "mcp_clients.xiaohongshu 已迁移至 MediaEngine.tools.mcp.clients.xiaohongshu",
    DeprecationWarning,
    stacklevel=2
)
from MediaEngine.tools.mcp.clients.xiaohongshu import *
