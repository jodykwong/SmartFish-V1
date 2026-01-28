"""
MCP客户端集成测试

测试MCP客户端基础架构和各平台客户端的功能。
"""

import pytest
import sys
import os

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mcp_clients.base import (
    BaseMCPClient,
    MCPSearchResult,
    MCPResponse,
    DataSourceRouter,
    get_router,
    init_router
)


class TestMCPSearchResult:
    """测试MCPSearchResult数据结构"""
    
    def test_create_result(self):
        """测试创建搜索结果"""
        result = MCPSearchResult(
            title="测试标题",
            content="这是测试内容",
            url="https://example.com",
            platform="xiaohongshu",
            author="测试用户",
            likes=100,
            comments=50
        )
        
        assert result.title == "测试标题"
        assert result.platform == "xiaohongshu"
        assert result.likes == 100
        
    def test_to_dict(self):
        """测试转换为字典"""
        result = MCPSearchResult(
            title="测试",
            content="内容",
            url="https://example.com",
            platform="weibo"
        )
        
        data = result.to_dict()
        assert isinstance(data, dict)
        assert data["platform"] == "weibo"


class TestMCPResponse:
    """测试MCPResponse数据结构"""
    
    def test_create_success_response(self):
        """测试创建成功响应"""
        results = [
            MCPSearchResult(
                title="结果1",
                content="内容1",
                url="https://example.com/1",
                platform="xiaohongshu"
            )
        ]
        
        response = MCPResponse(
            success=True,
            platform="xiaohongshu",
            query="测试查询",
            results=results,
            answer="找到1条结果"
        )
        
        assert response.success is True
        assert len(response.results) == 1
        assert response.webpages == results  # 兼容性属性
        
    def test_create_error_response(self):
        """测试创建错误响应"""
        response = MCPResponse(
            success=False,
            platform="weibo",
            query="测试",
            error="连接超时"
        )
        
        assert response.success is False
        assert response.error == "连接超时"


class TestDataSourceRouter:
    """测试数据源路由器"""
    
    def test_init_router(self):
        """测试初始化路由器"""
        router = DataSourceRouter()
        assert router is not None
        
    def test_get_priority_platforms(self):
        """测试获取优先平台"""
        router = DataSourceRouter()
        platforms = router.get_priority_platforms()
        
        # 验证返回的是列表
        assert isinstance(platforms, list)
        
    def test_merge_results(self):
        """测试合并搜索结果"""
        router = DataSourceRouter()
        
        response1 = MCPResponse(
            success=True,
            platform="xiaohongshu",
            query="测试",
            results=[
                MCPSearchResult(
                    title="小红书结果",
                    content="内容",
                    url="https://xiaohongshu.com/1",
                    platform="xiaohongshu",
                    likes=100
                )
            ]
        )
        
        response2 = MCPResponse(
            success=True,
            platform="weibo",
            query="测试",
            results=[
                MCPSearchResult(
                    title="微博结果",
                    content="内容",
                    url="https://weibo.com/1",
                    platform="weibo",
                    likes=200
                )
            ]
        )
        
        merged = router.merge_results([response1, response2])
        
        assert merged.success is True
        assert len(merged.results) == 2
        # 验证按互动量排序（微博的likes更高，应该排在前面）
        assert merged.results[0].platform == "weibo"


class TestClientImports:
    """测试客户端模块导入"""
    
    def test_import_xiaohongshu(self):
        """测试导入小红书客户端"""
        from mcp_clients.xiaohongshu import XiaohongshuMCPClient
        assert XiaohongshuMCPClient is not None
        
    def test_import_weibo(self):
        """测试导入微博客户端"""
        from mcp_clients.weibo import WeiboMCPClient
        assert WeiboMCPClient is not None
        
    def test_import_zhihu(self):
        """测试导入知乎客户端"""
        from mcp_clients.zhihu import ZhihuMCPClient
        assert ZhihuMCPClient is not None
        
    def test_import_bilibili(self):
        """测试导入B站客户端"""
        from mcp_clients.bilibili import BilibiliMCPClient
        assert BilibiliMCPClient is not None
        
    def test_import_douyin(self):
        """测试导入抖音客户端"""
        from mcp_clients.douyin import DouyinMCPClient
        assert DouyinMCPClient is not None
        
    def test_import_video_sum(self):
        """测试导入多平台综合客户端"""
        from mcp_clients.video_sum import VideoSumMCPClient
        assert VideoSumMCPClient is not None


class TestClientInitialization:
    """测试客户端初始化（不执行实际MCP调用）"""
    
    def test_xiaohongshu_client_init(self):
        """测试小红书客户端初始化"""
        from mcp_clients.xiaohongshu import XiaohongshuMCPClient
        
        client = XiaohongshuMCPClient()
        assert client.PLATFORM_NAME == "xiaohongshu"
        assert client.max_retries == 3
        
    def test_weibo_client_init(self):
        """测试微博客户端初始化"""
        from mcp_clients.weibo import WeiboMCPClient
        
        client = WeiboMCPClient()
        assert client.PLATFORM_NAME == "weibo"
        
    def test_zhihu_client_init(self):
        """测试知乎客户端初始化"""
        from mcp_clients.zhihu import ZhihuMCPClient
        
        client = ZhihuMCPClient()
        assert client.PLATFORM_NAME == "zhihu"
        
    def test_bilibili_client_init(self):
        """测试B站客户端初始化"""
        from mcp_clients.bilibili import BilibiliMCPClient
        
        client = BilibiliMCPClient()
        assert client.PLATFORM_NAME == "bilibili"
        
    def test_douyin_client_init(self):
        """测试抖音客户端初始化"""
        from mcp_clients.douyin import DouyinMCPClient
        
        client = DouyinMCPClient()
        assert client.PLATFORM_NAME == "douyin"
        
    def test_video_sum_client_init(self):
        """测试多平台综合客户端初始化"""
        from mcp_clients.video_sum import VideoSumMCPClient
        
        client = VideoSumMCPClient()
        assert client.PLATFORM_NAME == "video_sum"
        assert "douyin" in client.SUPPORTED_PLATFORMS


class TestBMADAdapterIntegration:
    """测试BMAD适配器与MCP的集成"""
    
    def test_adapter_with_mcp_disabled(self):
        """测试禁用MCP的适配器"""
        from bmad_adapter import BMADPainPointDiscovery
        
        discovery = BMADPainPointDiscovery(use_mcp=False)
        assert discovery.use_mcp is False
        assert discovery._mcp_router is None
        
    def test_adapter_init(self):
        """测试适配器初始化"""
        from bmad_adapter import BMADPainPointDiscovery
        
        discovery = BMADPainPointDiscovery(use_mcp=True)
        assert discovery is not None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
