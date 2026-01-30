"""
B站 MCP 客户端

基于 bilibili-video-info-mcp 封装的B站搜索客户端。
GitHub: https://github.com/lesir831/bilibili-video-info-mcp

功能:
- 视频详情获取
- 弹幕获取
- 字幕提取
- 评论区
"""

import os
import json
import subprocess
from typing import List, Dict, Any, Optional
from loguru import logger

from ..base import BaseMCPClient, MCPSearchResult, MCPResponse


class BilibiliMCPClient(BaseMCPClient):
    """
    B站 MCP 客户端
    
    使用 bilibili-video-info-mcp 进行B站内容获取。
    """
    
    PLATFORM_NAME = "bilibili"
    
    def __init__(
        self,
        mcp_command: str = "bilibili-mcp",
        max_retries: int = 3,
        retry_delay: float = 1.0,
        timeout: int = 30,
        cookie_path: Optional[str] = None
    ):
        """
        初始化B站客户端
        
        Args:
            mcp_command: MCP命令路径
            max_retries: 最大重试次数
            retry_delay: 重试延迟
            timeout: 超时时间
            cookie_path: Cookie文件路径
        """
        super().__init__(max_retries, retry_delay, timeout, cookie_path)
        self.mcp_command = mcp_command
        
    def _init_server(self) -> bool:
        """初始化B站MCP"""
        if self._initialized:
            return True
            
        try:
            result = subprocess.run(
                ["which", self.mcp_command],
                capture_output=True,
                text=True,
                timeout=5
            )
            
            if result.returncode != 0:
                logger.error(f"bilibili-mcp 未安装")
                return False
                
            self._initialized = True
            return True
            
        except Exception as e:
            logger.error(f"初始化B站MCP失败: {e}")
            return False
            
    def _execute_tool(self, tool_name: str, args: Dict) -> Any:
        """执行MCP工具调用"""
        if not self._initialized and not self._init_server():
            raise RuntimeError("B站MCP未初始化")
            
        mcp_request = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "tools/call",
            "params": {
                "name": tool_name,
                "arguments": args
            }
        }
        
        try:
            result = subprocess.run(
                [self.mcp_command],
                input=json.dumps(mcp_request),
                capture_output=True,
                text=True,
                timeout=self.timeout
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
        搜索B站视频
        
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
            
            raw_result = self._retry_with_backoff(
                self._execute_tool,
                "search_video",
                {"keyword": query, "page_size": max_results}
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
            logger.error(f"[bilibili] 搜索失败: {e}")
            return MCPResponse(
                success=False,
                platform=self.PLATFORM_NAME,
                query=query,
                error=str(e)
            )
            
    def _parse_search_results(self, raw_result: Any) -> List[MCPSearchResult]:
        """解析B站搜索结果"""
        results = []
        
        videos = raw_result if isinstance(raw_result, list) else raw_result.get("result", [])
        
        for video in videos:
            try:
                bvid = video.get("bvid", "")
                result = MCPSearchResult(
                    title=video.get("title", "").replace("<em class=\"keyword\">", "").replace("</em>", ""),
                    content=video.get("description", video.get("desc", "")),
                    url=f"https://www.bilibili.com/video/{bvid}" if bvid else "",
                    platform=self.PLATFORM_NAME,
                    author=video.get("author", video.get("owner", {}).get("name", "")),
                    likes=int(video.get("like", 0) or 0),
                    comments=int(video.get("review", video.get("reply", 0)) or 0),
                    shares=int(video.get("share", 0) or 0),
                    published_date=video.get("pubdate"),
                    raw_data=video
                )
                results.append(result)
            except Exception as e:
                logger.warning(f"解析B站结果失败: {e}")
                continue
                
        return results
        
    def _generate_summary(self, results: List[MCPSearchResult], query: str) -> str:
        """生成搜索结果摘要"""
        if not results:
            return f"未找到关于「{query}」的B站视频"
            
        total_likes = sum(r.likes for r in results)
        total_comments = sum(r.comments for r in results)
        
        return (
            f"在B站找到 {len(results)} 个关于「{query}」的视频，"
            f"共 {total_likes} 个点赞，{total_comments} 条评论"
        )
        
    def get_video_info(self, bvid: str) -> Optional[Dict]:
        """
        获取视频详情
        
        Args:
            bvid: 视频BV号
            
        Returns:
            视频详情
        """
        try:
            return self._retry_with_backoff(
                self._execute_tool,
                "get_video_info",
                {"bvid": bvid}
            )
        except Exception as e:
            logger.error(f"[bilibili] 获取视频详情失败: {e}")
            return None
            
    def get_danmaku(self, bvid: str, page: int = 1) -> List[Dict]:
        """
        获取视频弹幕
        
        Args:
            bvid: 视频BV号
            page: 分P号
            
        Returns:
            弹幕列表
        """
        try:
            result = self._retry_with_backoff(
                self._execute_tool,
                "get_danmaku",
                {"bvid": bvid, "page": page}
            )
            return result if isinstance(result, list) else result.get("danmaku", [])
        except Exception as e:
            logger.error(f"[bilibili] 获取弹幕失败: {e}")
            return []
            
    def get_comments(self, bvid: str, count: int = 50) -> List[Dict]:
        """
        获取视频评论
        
        Args:
            bvid: 视频BV号
            count: 获取数量
            
        Returns:
            评论列表
        """
        try:
            result = self._retry_with_backoff(
                self._execute_tool,
                "get_comments",
                {"bvid": bvid, "count": count}
            )
            return result if isinstance(result, list) else result.get("replies", [])
        except Exception as e:
            logger.error(f"[bilibili] 获取评论失败: {e}")
            return []
            
    def get_subtitle(self, bvid: str, page: int = 1) -> Optional[str]:
        """
        获取视频字幕
        
        Args:
            bvid: 视频BV号
            page: 分P号
            
        Returns:
            字幕文本
        """
        try:
            result = self._retry_with_backoff(
                self._execute_tool,
                "get_subtitle",
                {"bvid": bvid, "page": page}
            )
            return result.get("subtitle", result.get("content", ""))
        except Exception as e:
            logger.error(f"[bilibili] 获取字幕失败: {e}")
            return None


# 便捷函数
def create_bilibili_client(**kwargs) -> BilibiliMCPClient:
    """创建B站客户端实例"""
    return BilibiliMCPClient(**kwargs)
