#!/usr/bin/env python3
"""三层混合架构测试脚本"""

import asyncio
import sys
import os

# 添加项目路径
sys.path.append('/home/sunrise/SmartFish')

from MediaEngine.tools.router import DataSourceRouter

async def test_router():
    """测试路由器功能"""
    router = DataSourceRouter()
    
    test_cases = [
        "微博热搜",
        "https://weibo.com/123456",
        "https://douyin.com/video/123",
        "https://zhihu.com/question/123",
        "https://bilibili.com/video/BV123",
        "https://example.com/report.pdf",
        "https://example.com/news"
    ]
    
    print("=== SmartFish 三层混合架构测试 ===\n")
    
    for case in test_cases:
        route = router.route_request(case)
        print(f"输入: {case}")
        print(f"路由: {route}")
        
        try:
            results = await router.process_request(case, limit=3)
            print(f"结果: {len(results)} 条数据")
            if results:
                print(f"示例: {results[0]['source']} - {results[0]['raw_content'][:50]}...")
        except Exception as e:
            print(f"错误: {e}")
        
        print("-" * 50)

if __name__ == "__main__":
    asyncio.run(test_router())
