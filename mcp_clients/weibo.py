"""
兼容性转发模块: mcp_clients.weibo -> MediaEngine.tools.mcp.clients.weibo

⚠️ 已弃用: 请更新您的导入路径
"""
import warnings
warnings.warn(
    "mcp_clients.weibo 已迁移至 MediaEngine.tools.mcp.clients.weibo",
    DeprecationWarning,
    stacklevel=2
)
from MediaEngine.tools.mcp.clients.weibo import *
