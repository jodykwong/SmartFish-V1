"""
兼容性转发模块: mcp_clients.zhihu -> MediaEngine.tools.mcp.clients.zhihu

⚠️ 已弃用: 请更新您的导入路径
"""
import warnings
warnings.warn(
    "mcp_clients.zhihu 已迁移至 MediaEngine.tools.mcp.clients.zhihu",
    DeprecationWarning,
    stacklevel=2
)
from MediaEngine.tools.mcp.clients.zhihu import *
