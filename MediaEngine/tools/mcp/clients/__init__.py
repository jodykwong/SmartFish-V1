"""
MCP客户端 - 平台实现

包含各平台的MCP客户端实现：
- XiaohongshuMCPClient: 小红书
- WeiboMCPClient: 微博
- ZhihuMCPClient: 知乎
- BilibiliMCPClient: B站
- DouyinMCPClient: 抖音
- VideoSumMCPClient: 多平台综合
- HotNewsMCPClient: 多平台热榜 (9平台)
"""

from .xiaohongshu import XiaohongshuMCPClient, create_xiaohongshu_client
from .weibo import WeiboMCPClient, create_weibo_client
from .zhihu import ZhihuMCPClient, create_zhihu_client
from .bilibili import BilibiliMCPClient, create_bilibili_client
from .douyin import DouyinMCPClient, create_douyin_client
from .video_sum import VideoSumMCPClient, create_video_sum_client
from .hotnews import HotNewsMCPClient, HotNewsPlatform

__all__ = [
    # 客户端类
    "XiaohongshuMCPClient",
    "WeiboMCPClient",
    "ZhihuMCPClient",
    "BilibiliMCPClient",
    "DouyinMCPClient",
    "VideoSumMCPClient",
    "HotNewsMCPClient",
    "HotNewsPlatform",
    # 工厂函数
    "create_xiaohongshu_client",
    "create_weibo_client",
    "create_zhihu_client",
    "create_bilibili_client",
    "create_douyin_client",
    "create_video_sum_client",
]
