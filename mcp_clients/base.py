"""
兼容性转发模块: mcp_clients.base -> MediaEngine.tools.mcp.base

⚠️ 已弃用: 请更新您的导入路径
"""
import warnings
warnings.warn(
    "mcp_clients.base 已迁移至 MediaEngine.tools.mcp.base",
    DeprecationWarning,
    stacklevel=2
)
from MediaEngine.tools.mcp.base import *
