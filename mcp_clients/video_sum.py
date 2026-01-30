"""
兼容性转发模块: mcp_clients.video_sum -> MediaEngine.tools.mcp.clients.video_sum

⚠️ 已弃用: 请更新您的导入路径
"""
import warnings
warnings.warn(
    "mcp_clients.video_sum 已迁移至 MediaEngine.tools.mcp.clients.video_sum",
    DeprecationWarning,
    stacklevel=2
)
from MediaEngine.tools.mcp.clients.video_sum import *
