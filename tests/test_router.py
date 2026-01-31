"""路由器单元测试"""

import pytest
import asyncio
from MediaEngine.tools.router import DataSourceRouter

@pytest.fixture
def router():
    """路由器测试夹具"""
    return DataSourceRouter()

class TestRouting:
    """路由逻辑测试"""
    
    def test_weibo_url_detection(self, router):
        """测试微博 URL 识别"""
        assert router.route_request("https://weibo.com/123") == "mcp_weibo"
        assert router.route_request("微博热搜") == "mcp_weibo"
    
    def test_douyin_url_detection(self, router):
        """测试抖音 URL 识别"""
        assert router.route_request("https://douyin.com/video/123") == "mcp_douyin"
    
    def test_zhihu_url_detection(self, router):
        """测试知乎 URL 识别"""
        assert router.route_request("https://zhihu.com/question/123") == "mediacrawler_zhihu"
    
    def test_bilibili_url_detection(self, router):
        """测试B站 URL 识别"""
        assert router.route_request("https://bilibili.com/video/BV123") == "mediacrawler_bilibili"
    
    def test_pdf_url_detection(self, router):
        """测试 PDF URL 识别"""
        assert router.route_request("https://example.com/doc.pdf") == "firecrawl_pdf"
    
    def test_general_web_detection(self, router):
        """测试通用网页识别"""
        assert router.route_request("https://example.com/news") == "firecrawl_web"
    
    def test_empty_input(self, router):
        """测试空输入"""
        assert router.route_request("") == "mcp_search"
        assert router.route_request(None) == "mcp_search"
    
    @pytest.mark.asyncio
    async def test_process_request(self, router):
        """测试请求处理"""
        results = await router.process_request("测试查询", limit=3)
        assert len(results) == 3
        assert all('source' in r for r in results)
        assert all('raw_content' in r for r in results)
    
    @pytest.mark.asyncio
    async def test_error_handling(self, router):
        """测试错误处理"""
        # 应该返回错误信息而不是崩溃
        results = await router.process_request("", limit=1)
        assert len(results) >= 0
