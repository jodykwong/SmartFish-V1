"""
知乎 MCP 客户端

基于 zhihuMcpServer 封装的知乎搜索客户端。
GitHub: https://github.com/morrain/zhihuMcpServer

安装方式: 使用 npx 从 GitHub 运行
npx github:morrain/zhihuMcpServer

功能:
- 热门文章获取
- 内容搜索
- Markdown输出
"""

import os
import json
import subprocess
from typing import List, Dict, Any, Optional
from loguru import logger

from .base import BaseMCPClient, MCPSearchResult, MCPResponse


class ZhihuMCPClient(BaseMCPClient):
    """
    知乎 MCP 客户端
    
    使用 zhihuMcpServer 进行知乎内容搜索。
    """
    
    PLATFORM_NAME = "zhihu"
    
    def __init__(
        self,
        mcp_command: str = "npx",
        mcp_args: list = None,  # ["github:morrain/zhihuMcpServer"]
        max_retries: int = 3,
        retry_delay: float = 1.0,
        timeout: int = 30,
        cookie_path: Optional[str] = None
    ):
        """
        初始化知乎客户端
        
        Args:
            mcp_command: MCP命令路径 (默认使用 npx)
            mcp_args: MCP命令参数 (默认 ["github:morrain/zhihuMcpServer"])
            max_retries: 最大重试次数
            retry_delay: 重试延迟
            timeout: 超时时间
            cookie_path: Cookie文件路径
        """
        super().__init__(max_retries, retry_delay, timeout, cookie_path)
        self.mcp_command = mcp_command
        self.mcp_args = mcp_args or ["github:morrain/zhihuMcpServer"]
        
    def _init_server(self) -> bool:
        """初始化知乎MCP"""
        if self._initialized:
            return True
            
        try:
            # 检查 npx 是否可用
            result = subprocess.run(
                ["which", "npx"],
                capture_output=True,
                text=True,
                timeout=5
            )
            
            if result.returncode != 0:
                logger.error(f"npx 未安装，请先安装 Node.js")
                return False
            
            logger.info("[知乎] 使用 npx github:morrain/zhihuMcpServer")
            self._initialized = True
            return True
            
        except Exception as e:
            logger.error(f"初始化知乎MCP失败: {e}")
            return False
            
    def _execute_tool(self, tool_name: str, args: Dict) -> Any:
        """执行MCP工具调用"""
        if not self._initialized and not self._init_server():
            raise RuntimeError("知乎MCP未初始化")
            
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
            # 使用 npx 运行
            cmd = [self.mcp_command] + self.mcp_args
            result = subprocess.run(
                cmd,
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
        搜索知乎内容
        
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
                "search",
                {"query": query, "limit": max_results}
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
            logger.error(f"[zhihu] 搜索失败: {e}")
            return MCPResponse(
                success=False,
                platform=self.PLATFORM_NAME,
                query=query,
                error=str(e)
            )
            
    def _parse_search_results(self, raw_result: Any) -> List[MCPSearchResult]:
        """解析知乎搜索结果"""
        results = []
        
        items = raw_result if isinstance(raw_result, list) else raw_result.get("data", [])
        
        for item in items:
            try:
                # 知乎有多种内容类型：问题、回答、文章等
                item_type = item.get("type", "answer")
                
                if item_type == "question":
                    title = item.get("title", "")
                    content = item.get("excerpt", item.get("detail", ""))
                    url = f"https://www.zhihu.com/question/{item.get('id', '')}"
                elif item_type == "article":
                    title = item.get("title", "")
                    content = item.get("excerpt", item.get("content", ""))
                    url = f"https://zhuanlan.zhihu.com/p/{item.get('id', '')}"
                else:  # answer
                    question = item.get("question", {})
                    title = question.get("title", item.get("title", ""))
                    content = item.get("excerpt", item.get("content", ""))
                    url = f"https://www.zhihu.com/question/{question.get('id', '')}/answer/{item.get('id', '')}"
                
                author = item.get("author", {})
                
                result = MCPSearchResult(
                    title=title,
                    content=content[:500],  # 限制内容长度
                    url=url,
                    platform=self.PLATFORM_NAME,
                    author=author.get("name", author.get("user_name", "")),
                    likes=int(item.get("voteup_count", 0) or 0),
                    comments=int(item.get("comment_count", 0) or 0),
                    published_date=item.get("created_time"),
                    raw_data=item
                )
                results.append(result)
            except Exception as e:
                logger.warning(f"解析知乎结果失败: {e}")
                continue
                
        return results
        
    def _generate_summary(self, results: List[MCPSearchResult], query: str) -> str:
        """生成搜索结果摘要"""
        if not results:
            return f"未找到关于「{query}」的知乎内容"
            
        total_likes = sum(r.likes for r in results)
        total_comments = sum(r.comments for r in results)
        
        return (
            f"在知乎找到 {len(results)} 篇关于「{query}」的内容，"
            f"共 {total_likes} 个赞同，{total_comments} 条评论"
        )
        
    def get_hot_list(self, count: int = 50) -> List[Dict]:
        """
        获取知乎热榜
        
        Args:
            count: 获取数量
            
        Returns:
            热榜列表
        """
        try:
            result = self._retry_with_backoff(
                self._execute_tool,
                "get_hot_list",
                {"limit": count}
            )
            return result if isinstance(result, list) else result.get("data", [])
        except Exception as e:
            logger.error(f"[zhihu] 获取热榜失败: {e}")
            return []
            
    def get_question_answers(self, question_id: str, count: int = 20) -> List[Dict]:
        """
        获取问题的回答
        
        Args:
            question_id: 问题ID
            count: 获取数量
            
        Returns:
            回答列表
        """
        try:
            result = self._retry_with_backoff(
                self._execute_tool,
                "get_question_answers",
                {"question_id": question_id, "limit": count}
            )
            return result if isinstance(result, list) else result.get("data", [])
        except Exception as e:
            logger.error(f"[zhihu] 获取回答失败: {e}")
            return []
            
    def get_article_content(self, article_id: str, format: str = "markdown") -> Optional[str]:
        """
        获取专栏文章内容
        
        Args:
            article_id: 文章ID
            format: 输出格式 (markdown/html/text)
            
        Returns:
            文章内容
        """
        try:
            result = self._retry_with_backoff(
                self._execute_tool,
                "get_article",
                {"article_id": article_id, "format": format}
            )
            return result.get("content", result.get("text", ""))
        except Exception as e:
            logger.error(f"[zhihu] 获取文章内容失败: {e}")
            return None


# 便捷函数
def create_zhihu_client(**kwargs) -> ZhihuMCPClient:
    """创建知乎客户端实例"""
    return ZhihuMCPClient(**kwargs)
