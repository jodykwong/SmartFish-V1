"""
多平台热榜 MCP 客户端

基于 @wopal/mcp-server-hotnews 封装的多平台热榜客户端。
GitHub: https://github.com/wopal-cn/mcp-hotnews-server

安装方式: npx -y @wopal/mcp-server-hotnews

支持平台:
1. 知乎热榜 (Zhihu)
2. 36氪热榜 (36Kr)
3. 百度热点 (Baidu)
4. B站热榜 (Bilibili)
5. 微博热搜 (Weibo)
6. 抖音热点 (Douyin)
7. 虎扑热榜 (Hupu)
8. 豆瓣热榜 (Douban)
9. IT新闻 (ITNews)
"""

import json
import subprocess
from typing import List, Dict, Any, Optional
from enum import IntEnum
from loguru import logger

from ..base import BaseMCPClient, MCPSearchResult, MCPResponse


class HotNewsPlatform(IntEnum):
    """热榜平台ID"""
    ZHIHU = 1      # 知乎热榜
    KR36 = 2       # 36氪热榜
    BAIDU = 3      # 百度热点
    BILIBILI = 4   # B站热榜
    WEIBO = 5      # 微博热搜
    DOUYIN = 6     # 抖音热点
    HUPU = 7       # 虎扑热榜
    DOUBAN = 8     # 豆瓣热榜
    ITNEWS = 9     # IT新闻


PLATFORM_NAMES = {
    HotNewsPlatform.ZHIHU: "知乎",
    HotNewsPlatform.KR36: "36氪",
    HotNewsPlatform.BAIDU: "百度",
    HotNewsPlatform.BILIBILI: "B站",
    HotNewsPlatform.WEIBO: "微博",
    HotNewsPlatform.DOUYIN: "抖音",
    HotNewsPlatform.HUPU: "虎扑",
    HotNewsPlatform.DOUBAN: "豆瓣",
    HotNewsPlatform.ITNEWS: "IT新闻",
}


class HotNewsMCPClient(BaseMCPClient):
    """
    多平台热榜 MCP 客户端
    
    使用 @wopal/mcp-server-hotnews 获取多平台热门话题。
    """
    
    PLATFORM_NAME = "hotnews"
    
    def __init__(
        self,
        mcp_command: str = "npx",
        mcp_args: list = None,
        max_retries: int = 3,
        retry_delay: float = 1.0,
        timeout: int = 60,
        cookie_path: Optional[str] = None
    ):
        """
        初始化热榜客户端
        
        Args:
            mcp_command: MCP命令路径 (默认使用 npx)
            mcp_args: MCP命令参数
            max_retries: 最大重试次数
            retry_delay: 重试延迟
            timeout: 超时时间 (热榜可能较慢)
            cookie_path: Cookie文件路径 (此MCP不需要)
        """
        super().__init__(max_retries, retry_delay, timeout, cookie_path)
        self.mcp_command = mcp_command
        self.mcp_args = mcp_args or ["-y", "@wopal/mcp-server-hotnews"]
        
    def _init_server(self) -> bool:
        """初始化热榜MCP"""
        if self._initialized:
            return True
            
        try:
            result = subprocess.run(
                ["which", "npx"],
                capture_output=True,
                text=True,
                timeout=5
            )
            
            if result.returncode != 0:
                logger.error("npx 未安装，请先安装 Node.js")
                return False
            
            logger.info("[热榜] 使用 @wopal/mcp-server-hotnews")
            self._initialized = True
            return True
            
        except Exception as e:
            logger.error(f"初始化热榜MCP失败: {e}")
            return False
            
    def _execute_tool(self, tool_name: str, args: Dict) -> Any:
        """执行MCP工具调用"""
        if not self._initialized and not self._init_server():
            raise RuntimeError("热榜MCP未初始化")
            
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
    
    def get_hot_news(
        self, 
        platforms: List[int] = None,
        max_results: int = 20
    ) -> MCPResponse:
        """
        获取多平台热榜
        
        Args:
            platforms: 平台ID列表, 默认获取知乎和微博
                - 1: 知乎, 2: 36氪, 3: 百度, 4: B站
                - 5: 微博, 6: 抖音, 7: 虎扑, 8: 豆瓣, 9: IT新闻
            max_results: 每个平台的最大结果数
            
        Returns:
            统一格式的响应
        """
        if platforms is None:
            platforms = [HotNewsPlatform.ZHIHU, HotNewsPlatform.WEIBO]
            
        try:
            if not self._init_server():
                return MCPResponse(
                    success=False,
                    platform=self.PLATFORM_NAME,
                    query=f"热榜: {platforms}",
                    error="MCP未初始化"
                )
            
            platform_names = [PLATFORM_NAMES.get(p, str(p)) for p in platforms]
            logger.info(f"[热榜] 获取平台: {', '.join(platform_names)}")
            
            raw_result = self._retry_with_backoff(
                self._execute_tool,
                "get_hot_news",
                {"sources": platforms}
            )
            
            results = self._parse_hot_news(raw_result, max_results)
            
            return MCPResponse(
                success=True,
                platform=self.PLATFORM_NAME,
                query=f"热榜: {', '.join(platform_names)}",
                results=results,
                answer=self._generate_summary(results, "热门话题")
            )
            
        except Exception as e:
            logger.error(f"[热榜] 获取失败: {e}")
            return MCPResponse(
                success=False,
                platform=self.PLATFORM_NAME,
                query=f"热榜: {platforms}",
                error=str(e)
            )
    
    def _parse_hot_news(self, raw_result: Any, max_results: int) -> List[MCPSearchResult]:
        """解析热榜结果"""
        results = []
        
        # 获取 markdown 内容
        content = ""
        if isinstance(raw_result, dict):
            content = raw_result.get("content", raw_result.get("markdown", ""))
        elif isinstance(raw_result, str):
            content = raw_result
            
        if not content:
            logger.warning("[热榜] 结果为空")
            return results
            
        import re
        
        # 匹配 markdown 链接格式: [title](url)
        link_pattern = r'\[([^\]]+)\]\((https?://[^\)]+)\)'
        matches = re.findall(link_pattern, content)
        
        # 尝试匹配热度指数 (如果有)
        heat_pattern = r'(\d+(?:\.\d+)?[万亿]?)\s*热度'
        
        seen_urls = set()
        for title, url in matches[:max_results]:
            if url in seen_urls:
                continue
            seen_urls.add(url)
            
            # 检测平台
            platform = self._detect_platform(url)
            
            result = MCPSearchResult(
                title=title.strip(),
                content=f"来源: {platform}",
                url=url,
                author="",
                likes=0,
                comments=0,
                shares=0,
                published_at=None
            )
            results.append(result)
            
        logger.info(f"[热榜] 解析到 {len(results)} 条热门话题")
        return results
    
    def _detect_platform(self, url: str) -> str:
        """根据URL检测平台"""
        if "zhihu.com" in url:
            return "知乎"
        elif "weibo" in url:
            return "微博"
        elif "bilibili" in url:
            return "B站"
        elif "douyin" in url:
            return "抖音"
        elif "36kr" in url:
            return "36氪"
        elif "baidu" in url:
            return "百度"
        elif "hupu" in url:
            return "虎扑"
        elif "douban" in url:
            return "豆瓣"
        else:
            return "其他"
    
    def search(self, query: str, max_results: int = 20) -> MCPResponse:
        """
        热榜不支持搜索，返回热榜内容
        
        注意: 此MCP不支持关键词搜索，仅返回热榜内容
        """
        logger.warning("[热榜] 不支持关键词搜索，返回默认热榜")
        return self.get_hot_news(max_results=max_results)
    
    def get_zhihu_hot(self, max_results: int = 20) -> MCPResponse:
        """获取知乎热榜"""
        return self.get_hot_news([HotNewsPlatform.ZHIHU], max_results)
    
    def get_weibo_hot(self, max_results: int = 20) -> MCPResponse:
        """获取微博热搜"""
        return self.get_hot_news([HotNewsPlatform.WEIBO], max_results)
    
    def get_bilibili_hot(self, max_results: int = 20) -> MCPResponse:
        """获取B站热榜"""
        return self.get_hot_news([HotNewsPlatform.BILIBILI], max_results)
    
    def get_all_hot(self, max_results: int = 10) -> MCPResponse:
        """获取所有平台热榜"""
        all_platforms = list(range(1, 10))
        return self.get_hot_news(all_platforms, max_results)
