"""
兼容性转发模块: mcp_clients.douyin -> MediaEngine.tools.mcp.clients.douyin

⚠️ 已弃用: 请更新您的导入路径
"""
import warnings
warnings.warn(
    "mcp_clients.douyin 已迁移至 MediaEngine.tools.mcp.clients.douyin",
    DeprecationWarning,
    stacklevel=2
)
from MediaEngine.tools.mcp.clients.douyin import *
