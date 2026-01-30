"""
兼容性转发模块: mcp_clients.bilibili -> MediaEngine.tools.mcp.clients.bilibili

⚠️ 已弃用: 请更新您的导入路径
"""
import warnings
warnings.warn(
    "mcp_clients.bilibili 已迁移至 MediaEngine.tools.mcp.clients.bilibili",
    DeprecationWarning,
    stacklevel=2
)
from MediaEngine.tools.mcp.clients.bilibili import *
