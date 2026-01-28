"""
抖音 MCP 客户端

基于 douyin-mcp-server 封装的抖音搜索客户端。
GitHub: https://github.com/yzfly/douyin-mcp-server

安装方式: 使用 uvx 运行 Python 包
uvx douyin-mcp-server

前置条件:
- 安装 uv: pip install uv
- 配置 DASHSCOPE_API_KEY (阿里云百炼 API)

功能:
- 无水印视频链接获取
- 视频文案提取
"""

import os
import json
import subprocess
from typing import List, Dict, Any, Optional
from loguru import logger

from .base import BaseMCPClient, MCPSearchResult, MCPResponse


class DouyinMCPClient(BaseMCPClient):
    """
    抖音 MCP 客户端
    
    使用 douyin-mcp-server 进行抖音内容获取。
    """
    
    PLATFORM_NAME = "douyin"
    
    def __init__(
        self,
        mcp_command: str = "uvx",
        mcp_args: list = None,  # ["douyin-mcp-server"]
        max_retries: int = 3,
        retry_delay: float = 1.0,
        timeout: int = 30,
        cookie_path: Optional[str] = None,
        dashscope_api_key: Optional[str] = None
    ):
        """
        初始化抖音客户端
        
        Args:
            mcp_command: MCP命令路径 (默认使用 uvx)
            mcp_args: MCP命令参数 (默认 ["douyin-mcp-server"])
            max_retries: 最大重试次数
            retry_delay: 重试延迟
            timeout: 超时时间
            cookie_path: Cookie文件路径
            dashscope_api_key: 阿里云百炼 API 密钥
        """
        super().__init__(max_retries, retry_delay, timeout, cookie_path)
        self.mcp_command = mcp_command
        self.mcp_args = mcp_args or ["douyin-mcp-server"]
        self.dashscope_api_key = dashscope_api_key or os.environ.get("DASHSCOPE_API_KEY", "")
        
    def _init_server(self) -> bool:
        """初始化抖音MCP"""
        if self._initialized:
            return True
            
        try:
            # 检查 uvx 是否可用
            result = subprocess.run(
                ["which", "uvx"],
                capture_output=True,
                text=True,
                timeout=5
            )
            
            if result.returncode != 0:
                logger.error(f"uvx 未安装，请先运行: pip install uv")
                return False
            
            logger.info("[抖音] 使用 uvx douyin-mcp-server")
            self._initialized = True
            return True
            
        except Exception as e:
            logger.error(f"初始化抖音MCP失败: {e}")
            return False
            
    def _execute_tool(self, tool_name: str, args: Dict) -> Any:
        """执行MCP工具调用"""
        if not self._initialized and not self._init_server():
            raise RuntimeError("抖音MCP未初始化")
            
        mcp_request = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "tools/call",
            "params": {
                "name": tool_name,
                "arguments": args
            }
        }
        
        # 设置环境变量
        env = os.environ.copy()
        if self.dashscope_api_key:
            env["DASHSCOPE_API_KEY"] = self.dashscope_api_key
        
        try:
            # 使用 uvx 运行
            cmd = [self.mcp_command] + self.mcp_args
            result = subprocess.run(
                cmd,
                input=json.dumps(mcp_request),
                capture_output=True,
                text=True,
                timeout=self.timeout,
                env=env
            )
            
            if result.returncode != 0:
                raise RuntimeError(f"MCP调用失败: {result.stderr}")
                
            response = json.loads(result.stdout)
            
            if "error" in response:
                raise RuntimeError(f"MCP错误: {response['error']}")
                
            return response.get("result", {})
            
        except subprocess.TimeoutExpired:
            raise TimeoutError(f"MCP调用超时 ({self.timeout}秒)")
        except json.JSONDecodeError as e:
            raise ValueError(f"MCP响应解析失败: {e}")
            
    def search(self, query: str, max_results: int = 20) -> MCPResponse:
        """
        搜索抖音视频 (注意：douyin-mcp主要基于URL解析)
        
        Args:
            query: 搜索关键词
            max_results: 最大结果数
            
        Returns:
            统一格式的搜索响应
        """
        try:
            if not self._init_server():
                return MCPResponse(
                    success=False,
                    platform=self.PLATFORM_NAME,
                    query=query,
                    error="MCP未初始化"
                )
            
            # 尝试搜索（如果MCP支持）
            raw_result = self._retry_with_backoff(
                self._execute_tool,
                "search",
                {"keyword": query, "count": max_results}
            )
            
            results = self._parse_search_results(raw_result)
            
            return MCPResponse(
                success=True,
                platform=self.PLATFORM_NAME,
                query=query,
                results=results,
                answer=self._generate_summary(results, query)
            )
            
        except Exception as e:
            logger.warning(f"[douyin] 搜索可能不支持: {e}")
            return MCPResponse(
                success=True,
                platform=self.PLATFORM_NAME,
                query=query,
                results=[],
                answer="抖音MCP主要支持URL解析，请使用 get_video_info 方法"
            )
            
    def _parse_search_results(self, raw_result: Any) -> List[MCPSearchResult]:
        """解析抖音搜索结果"""
        results = []
        
        videos = raw_result if isinstance(raw_result, list) else raw_result.get("aweme_list", [])
        
        for video in videos:
            try:
                author = video.get("author", {})
                stats = video.get("statistics", {})
                
                result = MCPSearchResult(
                    title=video.get("desc", "")[:50],
                    content=video.get("desc", ""),
                    url=video.get("share_url", f"https://www.douyin.com/video/{video.get('aweme_id', '')}"),
                    platform=self.PLATFORM_NAME,
                    author=author.get("nickname", ""),
                    likes=int(stats.get("digg_count", 0) or 0),
                    comments=int(stats.get("comment_count", 0) or 0),
                    shares=int(stats.get("share_count", 0) or 0),
                    published_date=video.get("create_time"),
                    raw_data=video
                )
                results.append(result)
            except Exception as e:
                logger.warning(f"解析抖音结果失败: {e}")
                continue
                
        return results
        
    def _generate_summary(self, results: List[MCPSearchResult], query: str) -> str:
        """生成搜索结果摘要"""
        if not results:
            return f"未找到关于「{query}」的抖音视频"
            
        total_likes = sum(r.likes for r in results)
        total_comments = sum(r.comments for r in results)
        
        return (
            f"在抖音找到 {len(results)} 个关于「{query}」的视频，"
            f"共 {total_likes} 个点赞，{total_comments} 条评论"
        )
        
    def get_video_info(self, url: str) -> Optional[MCPSearchResult]:
        """
        根据URL获取视频信息
        
        Args:
            url: 抖音视频URL（支持分享链接）
            
        Returns:
            视频信息
        """
        try:
            result = self._retry_with_backoff(
                self._execute_tool,
                "get_video_info",
                {"url": url}
            )
            
            return self._parse_video_info(result, url)
            
        except Exception as e:
            logger.error(f"[douyin] 获取视频信息失败: {e}")
            return None
            
    def _parse_video_info(self, data: Dict, url: str) -> Optional[MCPSearchResult]:
        """解析单个视频信息"""
        try:
            author = data.get("author", {})
            stats = data.get("statistics", data.get("stats", {}))
            
            return MCPSearchResult(
                title=data.get("desc", data.get("title", ""))[:50],
                content=data.get("desc", data.get("title", "")),
                url=data.get("share_url", url),
                platform=self.PLATFORM_NAME,
                author=author.get("nickname", author.get("name", "")),
                likes=int(stats.get("digg_count", stats.get("likes", 0)) or 0),
                comments=int(stats.get("comment_count", stats.get("comments", 0)) or 0),
                shares=int(stats.get("share_count", stats.get("shares", 0)) or 0),
                raw_data=data
            )
        except Exception as e:
            logger.warning(f"解析视频信息失败: {e}")
            return None
            
    def get_video_no_watermark(self, url: str) -> Optional[str]:
        """
        获取无水印视频链接
        
        Args:
            url: 抖音视频URL
            
        Returns:
            无水印视频URL
        """
        try:
            result = self._retry_with_backoff(
                self._execute_tool,
                "get_video_no_watermark",
                {"url": url}
            )
            return result.get("video_url", result.get("url", ""))
        except Exception as e:
            logger.error(f"[douyin] 获取无水印链接失败: {e}")
            return None
            
    def get_video_caption(self, url: str) -> Optional[str]:
        """
        获取视频文案
        
        Args:
            url: 抖音视频URL
            
        Returns:
            视频文案
        """
        try:
            result = self._retry_with_backoff(
                self._execute_tool,
                "get_video_caption",
                {"url": url}
            )
            return result.get("desc", result.get("caption", ""))
        except Exception as e:
            logger.error(f"[douyin] 获取视频文案失败: {e}")
            return None


# 便捷函数
def create_douyin_client(**kwargs) -> DouyinMCPClient:
    """创建抖音客户端实例"""
    return DouyinMCPClient(**kwargs)
