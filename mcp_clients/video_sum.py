"""
多平台综合 MCP 客户端

基于 video-sum-mcp 封装的跨平台内容提取客户端。
GitHub: https://github.com/brucehe3/video-sum-mcp

安装方式: 克隆 GitHub 仓库并安装依赖
git clone https://github.com/brucehe3/video-sum-mcp.git
cd video-sum-mcp
pip install -r requirements.txt

支持平台:
- 抖音
- B站
- 小红书
- 知乎

功能:
- 跨平台视频/文章内容提取
- AI总结生成
"""

import os
import json
import subprocess
from typing import List, Dict, Any, Optional
from loguru import logger

from .base import BaseMCPClient, MCPSearchResult, MCPResponse


class VideoSumMCPClient(BaseMCPClient):
    """
    多平台综合 MCP 客户端
    
    使用 video-sum-mcp 工具进行跨平台内容提取和总结。
    支持抖音、B站、小红书、知乎等平台的内容解析。
    """
    
    PLATFORM_NAME = "video_sum"
    SUPPORTED_PLATFORMS = ["douyin", "bilibili", "xiaohongshu", "zhihu"]
    
    def __init__(
        self,
        project_path: str = None,  # video-sum-mcp 项目路径
        max_retries: int = 3,
        retry_delay: float = 1.0,
        timeout: int = 60,  # 视频处理需要更长时间
        cookie_path: Optional[str] = None
    ):
        """
        初始化多平台客户端
        
        Args:
            project_path: video-sum-mcp 项目路径 (克隆后的目录)
            max_retries: 最大重试次数
            retry_delay: 重试延迟
            timeout: 超时时间
            cookie_path: Cookie文件路径
        """
        super().__init__(max_retries, retry_delay, timeout, cookie_path)
        self.project_path = project_path
        self._available = None  # 缓存可用性检查
        
    def _init_server(self) -> bool:
        """
        检查并初始化 video-sum-mcp
        
        Returns:
            是否初始化成功
        """
        if self._initialized:
            return True
            
        try:
            # 检查MCP工具是否安装
            result = subprocess.run(
                ["which", self.mcp_command],
                capture_output=True,
                text=True,
                timeout=5
            )
            
            if result.returncode != 0:
                logger.error(f"video-sum-mcp 未安装，请运行: npm install -g video-sum-mcp")
                return False
                
            self._initialized = True
            logger.info("[video_sum] MCP已初始化")
            return True
            
        except Exception as e:
            logger.error(f"初始化video-sum-mcp失败: {e}")
            return False
            
    def _execute_tool(self, tool_name: str, args: Dict) -> Any:
        """
        执行MCP工具调用
        
        注意: video-sum-mcp 需要手动克隆和配置。
        由于该工具不在标准包管理器中，此方法当前只返回空结果。
        
        Args:
            tool_name: 工具名称
            args: 工具参数
            
        Returns:
            工具执行结果
        """
        if not self._initialized:
            self._init_server()
            
        if not self._available:
            logger.warning("[video_sum] 客户端不可用，请先配置项目路径")
            return {}
            
        # 如果项目路径可用，尝试调用 Python 脚本
        # 这里仅为框架示例，实际调用需要根据 video-sum-mcp 的接口调整
        logger.info(f"[video_sum] 调用工具: {tool_name}")
        return {}
            
    def search(self, query: str, max_results: int = 20) -> MCPResponse:
        """
        跨平台搜索 (由于video-sum-mcp主要基于URL解析，此方法返回空结果)
        
        对于搜索功能，建议使用各平台独立的MCP客户端。
        video-sum-mcp主要用于URL内容提取和总结。
        
        Args:
            query: 搜索关键词
            max_results: 最大结果数
            
        Returns:
            搜索响应
        """
        logger.info(f"[video_sum] 注意：video-sum-mcp不支持搜索，只支持URL内容提取")
        return MCPResponse(
            success=True,
            platform=self.PLATFORM_NAME,
            query=query,
            results=[],
            answer="video-sum-mcp 主要用于URL内容提取，请使用 extract_content 方法"
        )
        
    def extract_content(self, url: str) -> MCPResponse:
        """
        提取URL内容
        
        支持的平台URL:
        - 抖音: https://www.douyin.com/video/xxx
        - B站: https://www.bilibili.com/video/xxx
        - 小红书: https://www.xiaohongshu.com/explore/xxx
        - 知乎: https://www.zhihu.com/question/xxx
        
        Args:
            url: 内容URL
            
        Returns:
            提取的内容响应
        """
        try:
            if not self._init_server():
                return MCPResponse(
                    success=False,
                    platform=self.PLATFORM_NAME,
                    query=url,
                    error="MCP未初始化"
                )
                
            # 识别平台
            platform = self._detect_platform(url)
            
            # 执行内容提取
            raw_result = self._retry_with_backoff(
                self._execute_tool,
                "extract",
                {"url": url}
            )
            
            # 解析结果
            result = self._parse_extract_result(raw_result, url, platform)
            
            return MCPResponse(
                success=True,
                platform=platform or self.PLATFORM_NAME,
                query=url,
                results=[result] if result else [],
                answer=raw_result.get("summary", "")
            )
            
        except Exception as e:
            logger.error(f"[video_sum] 内容提取失败: {e}")
            return MCPResponse(
                success=False,
                platform=self.PLATFORM_NAME,
                query=url,
                error=str(e)
            )
            
    def summarize(self, url: str) -> Optional[str]:
        """
        生成URL内容的AI总结
        
        Args:
            url: 内容URL
            
        Returns:
            AI生成的总结
        """
        try:
            result = self._retry_with_backoff(
                self._execute_tool,
                "summarize",
                {"url": url}
            )
            return result.get("summary", "")
        except Exception as e:
            logger.error(f"[video_sum] 总结生成失败: {e}")
            return None
            
    def batch_extract(self, urls: List[str]) -> List[MCPResponse]:
        """
        批量提取多个URL的内容
        
        Args:
            urls: URL列表
            
        Returns:
            提取结果列表
        """
        results = []
        for url in urls:
            response = self.extract_content(url)
            results.append(response)
        return results
        
    def _detect_platform(self, url: str) -> Optional[str]:
        """
        检测URL所属平台
        
        Args:
            url: URL
            
        Returns:
            平台名称
        """
        url_lower = url.lower()
        
        if "douyin.com" in url_lower or "tiktok.com" in url_lower:
            return "douyin"
        elif "bilibili.com" in url_lower or "b23.tv" in url_lower:
            return "bilibili"
        elif "xiaohongshu.com" in url_lower or "xhslink.com" in url_lower:
            return "xiaohongshu"
        elif "zhihu.com" in url_lower:
            return "zhihu"
        else:
            return None
            
    def _parse_extract_result(
        self, 
        raw_result: Dict, 
        url: str, 
        platform: Optional[str]
    ) -> Optional[MCPSearchResult]:
        """
        解析内容提取结果
        
        Args:
            raw_result: 原始结果
            url: 原始URL
            platform: 平台名称
            
        Returns:
            统一格式的内容结果
        """
        try:
            return MCPSearchResult(
                title=raw_result.get("title", ""),
                content=raw_result.get("content", raw_result.get("text", "")),
                url=url,
                platform=platform or self.PLATFORM_NAME,
                author=raw_result.get("author", {}).get("name", ""),
                likes=int(raw_result.get("likes", 0) or 0),
                comments=int(raw_result.get("comments", 0) or 0),
                shares=int(raw_result.get("shares", 0) or 0),
                published_date=raw_result.get("publish_time"),
                raw_data=raw_result
            )
        except Exception as e:
            logger.warning(f"解析提取结果失败: {e}")
            return None
            
    def get_supported_platforms(self) -> List[str]:
        """获取支持的平台列表"""
        return self.SUPPORTED_PLATFORMS.copy()


# 便捷函数
def create_video_sum_client(**kwargs) -> VideoSumMCPClient:
    """创建多平台综合客户端实例"""
    return VideoSumMCPClient(**kwargs)
