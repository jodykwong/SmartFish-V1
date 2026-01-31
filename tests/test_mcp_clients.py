"""MCP 客户端单元测试"""

import pytest
from MediaEngine.tools.mcp.weibo_mcp import WeiboMCP
from MediaEngine.tools.mcp.douyin_mcp import DouyinMCP

@pytest.mark.asyncio
class TestMCPClients:
    """MCP 客户端测试"""
    
    async def test_weibo_search(self):
        """测试微博搜索"""
        client = WeiboMCP()
        results = await client.search("测试", limit=5)
        
        assert len(results) == 5
        assert all(r['source'] == 'weibo' for r in results)
        assert all('raw_content' in r for r in results)
    
    async def test_weibo_comments(self):
        """测试微博评论获取"""
        client = WeiboMCP()
        comments = await client.get_comments("123456", limit=10)
        
        assert len(comments) == 10
        assert all(r['source'] == 'weibo' for r in comments)
    
    async def test_douyin_search(self):
        """测试抖音搜索"""
        client = DouyinMCP()
        results = await client.search("测试", limit=5)
        
        assert len(results) == 5
        assert all(r['source'] == 'douyin' for r in results)
    
    async def test_data_normalization(self):
        """测试数据标准化"""
        client = WeiboMCP()
        raw_data = {
            'url': 'https://weibo.com/123',
            'content': '测试内容',
            'author': '测试用户',
            'timestamp': 1640995200
        }
        
        normalized = client.normalize_data(raw_data)
        
        assert normalized['source'] == 'weibo'
        assert normalized['url'] == 'https://weibo.com/123'
        assert normalized['raw_content'] == '测试内容'
        assert normalized['author'] == '测试用户'
        assert normalized['publish_time'] == 1640995200
