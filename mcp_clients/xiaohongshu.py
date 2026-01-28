"""
小红书 MCP 客户端

基于 xiaohongshu-mcp 封装的小红书搜索客户端。
GitHub: https://github.com/xpzouying/xiaohongshu-mcp

功能:
- search_feeds: 关键词搜索笔记
- get_feed_detail: 获取笔记详情
- 评论访问
"""

import os
import json
import subprocess
from typing import List, Dict, Any, Optional
from loguru import logger

from .base import BaseMCPClient, MCPSearchResult, MCPResponse


class XiaohongshuMCPClient(BaseMCPClient):
    """
    小红书 MCP 客户端
    
    使用 xiaohongshu-mcp 工具进行小红书内容搜索。
    需要先通过 npm install -g xiaohongshu-mcp 安装。
    """
    
    PLATFORM_NAME = "xiaohongshu"
    
    def __init__(
        self,
        mcp_command: str = "xiaohongshu-mcp",
        max_retries: int = 3,
        retry_delay: float = 1.0,
        timeout: int = 30,
        cookie_path: Optional[str] = None
    ):
        """
        初始化小红书客户端
        
        Args:
            mcp_command: MCP命令路径
            max_retries: 最大重试次数
            retry_delay: 重试延迟
            timeout: 超时时间
            cookie_path: Cookie文件路径
        """
        super().__init__(max_retries, retry_delay, timeout, cookie_path)
        self.mcp_command = mcp_command
        self._mcp_available = None  # 缓存可用性检查结果
        
    def _init_server(self) -> bool:
        """
        检查并初始化 xiaohongshu-mcp
        
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
                logger.error(f"xiaohongshu-mcp 未安装，请运行: npm install -g xiaohongshu-mcp")
                return False
                
            # 加载Cookie
            cookies = self.load_cookies()
            if cookies:
                logger.info("[xiaohongshu] 已加载保存的Cookie")
            else:
                logger.warning("[xiaohongshu] 无有效Cookie，可能需要扫码登录")
                
            self._initialized = True
            return True
            
        except Exception as e:
            logger.error(f"初始化小红书MCP失败: {e}")
            return False
            
    def _execute_tool(self, tool_name: str, args: Dict) -> Any:
        """
        执行MCP工具调用
        
        通过子进程调用 xiaohongshu-mcp 并解析JSON响应
        
        Args:
            tool_name: 工具名称 (search_feeds, get_feed_detail等)
            args: 工具参数
            
        Returns:
            工具执行结果
        """
        if not self._initialized and not self._init_server():
            raise RuntimeError("小红书MCP未初始化")
            
        # 构建MCP请求
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
            # 通过stdin/stdout与MCP服务通信
            result = subprocess.run(
                [self.mcp_command],
                input=json.dumps(mcp_request),
                capture_output=True,
                text=True,
                timeout=self.timeout,
                env={
                    **os.environ,
                    "XHS_COOKIE_PATH": self.cookie_path
                }
            )
            
            if result.returncode != 0:
                logger.error(f"MCP执行失败: {result.stderr}")
                raise RuntimeError(f"MCP调用失败: {result.stderr}")
                
            # 解析JSON响应
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
        搜索小红书笔记
        
        Args:
            query: 搜索关键词
            max_results: 最大结果数
            
        Returns:
            统一格式的搜索响应
        """
        try:
            # 确保初始化
            if not self._init_server():
                return MCPResponse(
                    success=False,
                    platform=self.PLATFORM_NAME,
                    query=query,
                    error="MCP未初始化"
                )
            
            # 使用重试机制执行搜索
            raw_result = self._retry_with_backoff(
                self._execute_tool,
                "search_feeds",
                {"keyword": query, "limit": max_results}
            )
            
            # 解析结果
            results = self._parse_search_results(raw_result)
            
            return MCPResponse(
                success=True,
                platform=self.PLATFORM_NAME,
                query=query,
                results=results,
                answer=self._generate_summary(results, query)
            )
            
        except Exception as e:
            logger.error(f"[xiaohongshu] 搜索失败: {e}")
            return MCPResponse(
                success=False,
                platform=self.PLATFORM_NAME,
                query=query,
                error=str(e)
            )
            
    def _parse_search_results(self, raw_result: Any) -> List[MCPSearchResult]:
        """
        解析小红书搜索结果
        
        Args:
            raw_result: MCP原始响应
            
        Returns:
            统一格式的搜索结果列表
        """
        results = []
        
        # 处理不同的响应格式
        feeds = raw_result if isinstance(raw_result, list) else raw_result.get("feeds", [])
        
        for feed in feeds:
            try:
                result = MCPSearchResult(
                    title=feed.get("title", feed.get("note_card", {}).get("title", "")),
                    content=feed.get("desc", feed.get("note_card", {}).get("desc", "")),
                    url=self._build_url(feed.get("note_id", feed.get("id", ""))),
                    platform=self.PLATFORM_NAME,
                    author=feed.get("user", {}).get("nickname", 
                                   feed.get("note_card", {}).get("user", {}).get("nickname", "")),
                    likes=int(feed.get("liked_count", feed.get("note_card", {}).get("liked_count", 0)) or 0),
                    comments=int(feed.get("comment_count", 0) or 0),
                    shares=int(feed.get("share_count", 0) or 0),
                    published_date=feed.get("time", feed.get("note_card", {}).get("time")),
                    raw_data=feed
                )
                results.append(result)
            except Exception as e:
                logger.warning(f"解析小红书结果失败: {e}")
                continue
                
        return results
        
    def _build_url(self, note_id: str) -> str:
        """构建小红书笔记URL"""
        if not note_id:
            return ""
        return f"https://www.xiaohongshu.com/explore/{note_id}"
        
    def _generate_summary(self, results: List[MCPSearchResult], query: str) -> str:
        """生成搜索结果摘要"""
        if not results:
            return f"未找到关于「{query}」的小红书笔记"
            
        total_likes = sum(r.likes for r in results)
        total_comments = sum(r.comments for r in results)
        
        return (
            f"在小红书找到 {len(results)} 篇关于「{query}」的笔记，"
            f"共 {total_likes} 个赞，{total_comments} 条评论"
        )
        
    def get_feed_detail(self, note_id: str) -> Optional[Dict]:
        """
        获取笔记详情
        
        Args:
            note_id: 笔记ID
            
        Returns:
            笔记详情字典
        """
        try:
            return self._retry_with_backoff(
                self._execute_tool,
                "get_feed_detail",
                {"note_id": note_id}
            )
        except Exception as e:
            logger.error(f"[xiaohongshu] 获取详情失败: {e}")
            return None
            
    def get_comments(self, note_id: str, max_count: int = 50) -> List[Dict]:
        """
        获取笔记评论
        
        Args:
            note_id: 笔记ID
            max_count: 最大评论数
            
        Returns:
            评论列表
        """
        try:
            result = self._retry_with_backoff(
                self._execute_tool,
                "get_comments",
                {"note_id": note_id, "count": max_count}
            )
            return result if isinstance(result, list) else result.get("comments", [])
        except Exception as e:
            logger.error(f"[xiaohongshu] 获取评论失败: {e}")
            return []
            
    def login_with_qrcode(self) -> bool:
        """
        通过扫码登录
        
        Returns:
            是否登录成功
        """
        logger.info("[xiaohongshu] 请使用小红书App扫描二维码登录...")
        
        try:
            result = subprocess.run(
                [self.mcp_command, "--login"],
                capture_output=True,
                text=True,
                timeout=120  # 登录需要更长超时
            )
            
            if result.returncode == 0:
                # 登录成功后保存Cookie
                # 注意：实际Cookie由xiaohongshu-mcp管理
                self.save_cookies({"logged_in": True})
                logger.info("[xiaohongshu] 登录成功")
                return True
            else:
                logger.error(f"[xiaohongshu] 登录失败: {result.stderr}")
                return False
                
        except Exception as e:
            logger.error(f"[xiaohongshu] 登录异常: {e}")
            return False


# 便捷函数
def create_xiaohongshu_client(**kwargs) -> XiaohongshuMCPClient:
    """创建小红书客户端实例"""
    return XiaohongshuMCPClient(**kwargs)
