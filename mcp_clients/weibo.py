"""
微博 MCP 客户端

基于 mcp-server-weibo 封装的微博搜索客户端。
GitHub: https://github.com/qinyuanpei/mcp-server-weibo

功能:
- 用户动态搜索
- 热搜榜单
- 内容搜索
- 话题分析
"""

import os
import json
import subprocess
from typing import List, Dict, Any, Optional
from loguru import logger

from .base import BaseMCPClient, MCPSearchResult, MCPResponse


class WeiboMCPClient(BaseMCPClient):
    """
    微博 MCP 客户端
    
    使用 mcp-server-weibo 工具进行微博内容搜索。
    """
    
    PLATFORM_NAME = "weibo"
    
    def __init__(
        self,
        mcp_command: str = "mcp-server-weibo",
        max_retries: int = 3,
        retry_delay: float = 1.0,
        timeout: int = 30,
        cookie_path: Optional[str] = None
    ):
        """
        初始化微博客户端
        
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
        """初始化微博MCP"""
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
                logger.error(f"mcp-server-weibo 未安装")
                return False
                
            cookies = self.load_cookies()
            if cookies:
                logger.info("[weibo] 已加载保存的Cookie")
                
            self._initialized = True
            return True
            
        except Exception as e:
            logger.error(f"初始化微博MCP失败: {e}")
            return False
            
    def _execute_tool(self, tool_name: str, args: Dict) -> Any:
        """执行MCP工具调用"""
        if not self._initialized and not self._init_server():
            raise RuntimeError("微博MCP未初始化")
            
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
                timeout=self.timeout,
                env={
                    **os.environ,
                    "WEIBO_COOKIE_PATH": self.cookie_path
                }
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
        搜索微博内容
        
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
                "search_weibo",
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
            logger.error(f"[weibo] 搜索失败: {e}")
            return MCPResponse(
                success=False,
                platform=self.PLATFORM_NAME,
                query=query,
                error=str(e)
            )
            
    def _parse_search_results(self, raw_result: Any) -> List[MCPSearchResult]:
        """解析微博搜索结果"""
        results = []
        
        statuses = raw_result if isinstance(raw_result, list) else raw_result.get("statuses", [])
        
        for status in statuses:
            try:
                user = status.get("user", {})
                result = MCPSearchResult(
                    title=status.get("text", "")[:50],  # 微博没有标题，取内容前50字
                    content=status.get("text", ""),
                    url=f"https://weibo.com/{user.get('id')}/{status.get('mblogid', status.get('id', ''))}",
                    platform=self.PLATFORM_NAME,
                    author=user.get("screen_name", user.get("name", "")),
                    likes=int(status.get("attitudes_count", 0) or 0),
                    comments=int(status.get("comments_count", 0) or 0),
                    shares=int(status.get("reposts_count", 0) or 0),
                    published_date=status.get("created_at"),
                    raw_data=status
                )
                results.append(result)
            except Exception as e:
                logger.warning(f"解析微博结果失败: {e}")
                continue
                
        return results
        
    def _generate_summary(self, results: List[MCPSearchResult], query: str) -> str:
        """生成搜索结果摘要"""
        if not results:
            return f"未找到关于「{query}」的微博"
            
        total_likes = sum(r.likes for r in results)
        total_comments = sum(r.comments for r in results)
        total_shares = sum(r.shares for r in results)
        
        return (
            f"在微博找到 {len(results)} 条关于「{query}」的内容，"
            f"共 {total_likes} 个赞，{total_comments} 条评论，{total_shares} 次转发"
        )
        
    def get_hot_search(self, count: int = 50) -> List[Dict]:
        """
        获取微博热搜榜
        
        Args:
            count: 获取数量
            
        Returns:
            热搜列表
        """
        try:
            result = self._retry_with_backoff(
                self._execute_tool,
                "get_hot_search",
                {"count": count}
            )
            return result if isinstance(result, list) else result.get("data", [])
        except Exception as e:
            logger.error(f"[weibo] 获取热搜失败: {e}")
            return []
            
    def get_user_timeline(self, user_id: str, count: int = 20) -> List[Dict]:
        """
        获取用户动态
        
        Args:
            user_id: 用户ID
            count: 获取数量
            
        Returns:
            用户微博列表
        """
        try:
            result = self._retry_with_backoff(
                self._execute_tool,
                "get_user_timeline",
                {"user_id": user_id, "count": count}
            )
            return result if isinstance(result, list) else result.get("statuses", [])
        except Exception as e:
            logger.error(f"[weibo] 获取用户动态失败: {e}")
            return []
            
    def get_topic_info(self, topic: str) -> Optional[Dict]:
        """
        获取话题信息
        
        Args:
            topic: 话题名称
            
        Returns:
            话题详情
        """
        try:
            return self._retry_with_backoff(
                self._execute_tool,
                "get_topic_info",
                {"topic": topic}
            )
        except Exception as e:
            logger.error(f"[weibo] 获取话题信息失败: {e}")
            return None


# 便捷函数
def create_weibo_client(**kwargs) -> WeiboMCPClient:
    """创建微博客户端实例"""
    return WeiboMCPClient(**kwargs)
