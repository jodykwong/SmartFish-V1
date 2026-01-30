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

from ..base import BaseMCPClient, MCPSearchResult, MCPResponse


class ZhihuMCPClient(BaseMCPClient):
    """
    知乎 MCP 客户端
    
    使用 zhihuMcpServer 进行知乎内容搜索。
    """
    
    PLATFORM_NAME = "zhihu"
    
    def __init__(
        self,
        mcp_command: str = "node",
        mcp_args: list = None,  # Default: local build path
        max_retries: int = 3,
        retry_delay: float = 1.0,
        timeout: int = 30,
        cookie_path: Optional[str] = None
    ):
        """
        初始化知乎客户端
        
        Args:
            mcp_command: MCP命令路径 (默认使用 node)
            mcp_args: MCP命令参数 (默认使用本地构建)
            max_retries: 最大重试次数
            retry_delay: 重试延迟
            timeout: 超时时间
            cookie_path: Cookie文件路径
        """
        super().__init__(max_retries, retry_delay, timeout, cookie_path)
        self.mcp_command = mcp_command
        # 使用本地构建的 zhihu-mcp-server
        local_build = os.path.expanduser("~/.smartfish/mcp/servers/zhihu-mcp/build/index.js")
        self.mcp_args = mcp_args or [local_build]
        
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
            import re
            
            # 使用 Popen 进行双向通信
            cmd = [self.mcp_command] + self.mcp_args
            process = subprocess.Popen(
                cmd,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                cwd=os.path.expanduser("~/.smartfish/mcp/servers/zhihu-mcp")
            )
            
            # 发送请求并等待响应
            stdout, stderr = process.communicate(
                input=json.dumps(mcp_request) + "\n",
                timeout=self.timeout
            )
            
            if process.returncode != 0 and not stdout:
                raise RuntimeError(f"MCP调用失败: {stderr}")
            
            # MCP 服务器在 stdout 输出时会混入调试信息
            # 需要从输出中提取 JSON-RPC 响应
            # 查找包含 result 或 error 的 JSON 对象
            json_match = re.search(r'\{"(?:result|error|jsonrpc)":', stdout)
            
            if not json_match:
                logger.error(f"[zhihu] 无法找到JSON响应: {stdout[:300]}")
                raise ValueError(f"MCP响应中未找到JSON: {stdout[:300]}")
            
            json_str = stdout[json_match.start():]
            
            # 找到 JSON 结尾 (匹配最后一个完整的 JSON 对象)
            # 处理可能的尾部文本 (如 "Exiting with code: 0")
            try:
                response = json.loads(json_str.strip())
            except json.JSONDecodeError:
                # 尝试去掉尾部非 JSON 内容
                json_end = json_str.rfind('}')
                if json_end != -1:
                    response = json.loads(json_str[:json_end + 1])
                else:
                    raise
            
            if "error" in response:
                raise RuntimeError(f"MCP错误: {response['error']}")
            
            # 从 result.content 中提取内容
            mcp_result = response.get("result", {})
            if isinstance(mcp_result, dict) and "content" in mcp_result:
                content_list = mcp_result.get("content", [])
                if content_list and isinstance(content_list, list):
                    # 返回第一个 text 类型的内容
                    for item in content_list:
                        if item.get("type") == "text":
                            return {"content": item.get("text", "")}
            
            return mcp_result
            
        except subprocess.TimeoutExpired:
            process.kill()
            raise TimeoutError(f"MCP调用超时 ({self.timeout}秒)")
        except json.JSONDecodeError as e:
            logger.error(f"[zhihu] JSON解析失败: {e}, 原始输出: {stdout[:300] if 'stdout' in dir() else 'N/A'}")
            raise ValueError(f"MCP响应解析失败: {e}")
            
    def search(self, query: str, max_results: int = 20) -> MCPResponse:
        """
        搜索知乎内容
        
        使用 scrape-webpage 工具抓取知乎搜索页面
        
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
            
            # 构造知乎搜索URL
            import urllib.parse
            encoded_query = urllib.parse.quote(query)
            search_url = f"https://www.zhihu.com/search?type=content&q={encoded_query}"
            
            logger.info(f"[知乎] 抓取搜索页: {search_url}")
            
            # 使用 scrape-webpage 工具抓取搜索结果页
            raw_result = self._retry_with_backoff(
                self._execute_tool,
                "scrape-webpage",
                {"url": search_url, "autoInteract": True}
            )
            
            # 解析 markdown 格式的搜索结果
            results = self._parse_scraped_results(raw_result, max_results)
            
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
    
    def _parse_scraped_results(self, raw_result: Any, max_results: int = 20) -> List[MCPSearchResult]:
        """解析 scrape-webpage 返回的 markdown 结果"""
        results = []
        
        # 获取 markdown 内容
        content = ""
        if isinstance(raw_result, dict):
            content = raw_result.get("content", raw_result.get("markdown", ""))
        elif isinstance(raw_result, str):
            content = raw_result
            
        if not content:
            logger.warning("[知乎] 抓取结果为空")
            return results
            
        # 解析 markdown 中的链接和标题
        import re
        
        # 匹配 markdown 链接格式: [title](url)
        link_pattern = r'\[([^\]]+)\]\((https?://(?:www\.)?zhihu\.com/[^\)]+)\)'
        matches = re.findall(link_pattern, content)
        
        seen_urls = set()
        for title, url in matches[:max_results]:
            if url in seen_urls:
                continue
            seen_urls.add(url)
            
            # 提取内容片段 (标题后的文本)
            excerpt = ""
            title_pos = content.find(title)
            if title_pos != -1:
                # 取标题后200字符作为摘要
                excerpt_start = title_pos + len(title)
                excerpt = content[excerpt_start:excerpt_start + 200].strip()
                # 清理 markdown 格式
                excerpt = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', excerpt)
                excerpt = re.sub(r'[#*_`]', '', excerpt)
            
            result = MCPSearchResult(
                title=title.strip(),
                content=excerpt,
                url=url,
                author="",
                likes=0,
                comments=0,
                shares=0,
                published_at=None
            )
            results.append(result)
            
        logger.info(f"[知乎] 解析到 {len(results)} 条搜索结果")
        return results
            
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
