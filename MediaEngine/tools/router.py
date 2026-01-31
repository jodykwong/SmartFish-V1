"""数据源智能路由器"""

import re
import asyncio
import logging
from typing import Dict, List, Any, Optional
from urllib.parse import urlparse

logger = logging.getLogger(__name__)

class DataSourceRouter:
    """三层混合架构数据源路由器"""
    
    def __init__(self):
        # 延迟导入避免循环依赖
        from .mcp.weibo_mcp import WeiboMCP
        from .mcp.douyin_mcp import DouyinMCP
        from .mediacrawler.adapter import MediaCrawlerAdapter
        from .firecrawl.client import FireCrawlClient
        
        # Tier 1: MCP (快速层)
        self.weibo_mcp = WeiboMCP()
        self.douyin_mcp = DouyinMCP()
        
        # Tier 2: MediaCrawler (深度层)
        self.mediacrawler = MediaCrawlerAdapter()
        
        # Tier 3: FireCrawl (通用层)
        self.firecrawl = FireCrawlClient()
    
    def route_request(self, url_or_query: str) -> str:
        """智能路由逻辑"""
        if not url_or_query or not isinstance(url_or_query, str):
            return "mcp_search"
        
        url_or_query = url_or_query.strip()
        if not url_or_query:
            return "mcp_search"
            
        if self.is_weibo_url(url_or_query):
            return "mcp_weibo"
        elif self.is_douyin_url(url_or_query):
            return "mcp_douyin"
        elif self.is_zhihu_url(url_or_query):
            return "mediacrawler_zhihu"
        elif self.is_bilibili_url(url_or_query):
            return "mediacrawler_bilibili"
        elif self.is_pdf_url(url_or_query):
            return "firecrawl_pdf"
        elif self.is_general_web_url(url_or_query):
            return "firecrawl_web"
        else:
            return "mcp_search"  # 默认搜索
    
    async def process_request(self, url_or_query: str, limit: int = 20) -> List[Dict[str, Any]]:
        """处理请求并返回标准化数据（带降级机制）"""
        try:
            route = self.route_request(url_or_query)
            
            # 尝试主路由
            try:
                if route == "mcp_weibo":
                    return await self.weibo_mcp.search(url_or_query, limit)
                elif route == "mcp_douyin":
                    return await self.douyin_mcp.search(url_or_query, limit)
                elif route == "mediacrawler_zhihu":
                    return await self._with_fallback(
                        self.mediacrawler.search_zhihu(url_or_query, limit),
                        "tier2_zhihu"
                    )
                elif route == "mediacrawler_bilibili":
                    return await self._with_fallback(
                        self.mediacrawler.search_bilibili(url_or_query, limit),
                        "tier2_bilibili"
                    )
                elif route == "firecrawl_pdf":
                    result = await self._with_fallback(
                        self.firecrawl.scrape_pdf(url_or_query),
                        "tier3_pdf"
                    )
                    return [result] if result else []
                elif route == "firecrawl_web":
                    result = await self._with_fallback(
                        self.firecrawl.scrape_url(url_or_query),
                        "tier3_web"
                    )
                    return [result] if result else []
                else:
                    return await self.weibo_mcp.search(url_or_query, limit)
            
            except Exception as tier_error:
                # 降级到 Tier 1 (MCP)
                logger.warning(f"Tier 2/3 failed, fallback to Tier 1: {tier_error}")
                return await self.weibo_mcp.search(url_or_query, limit)
                
        except Exception as e:
            # 最终降级：返回错误信息
            logger.error(f"All tiers failed: {str(e)}", exc_info=True)
            return [{
                'source': 'error',
                'url': url_or_query,
                'raw_content': f'处理失败: {str(e)}',
                'author': 'system',
                'publish_time': 0,
                'meta': {'error': str(e), 'route': route if 'route' in locals() else 'unknown'}
            }]
    
    async def _with_fallback(self, coro, tier_name: str):
        """带超时和降级的协程执行"""
        try:
            return await asyncio.wait_for(coro, timeout=30)
        except asyncio.TimeoutError:
            logger.warning(f"{tier_name} timeout, triggering fallback")
            raise
        except Exception as e:
            logger.error(f"{tier_name} error: {e}")
            raise
    
    def is_weibo_url(self, url: str) -> bool:
        return "weibo.com" in url or "微博" in url
    
    def is_douyin_url(self, url: str) -> bool:
        return "douyin.com" in url or "抖音" in url
    
    def is_zhihu_url(self, url: str) -> bool:
        return "zhihu.com" in url or "知乎" in url
    
    def is_bilibili_url(self, url: str) -> bool:
        return "bilibili.com" in url or "b站" in url.lower()
    
    def is_pdf_url(self, url: str) -> bool:
        return url.lower().endswith('.pdf') or 'pdf' in url.lower()
    
    def is_general_web_url(self, url: str) -> bool:
        return url.startswith(('http://', 'https://'))
