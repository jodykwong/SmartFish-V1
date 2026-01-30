#!/usr/bin/env python3
"""
SmartFish MCP 真实数据获取演示

使用保存的登录状态通过Playwright获取真实社媒数据，
然后进行被动信号挖掘分析。
"""

import os
import sys
import json
import subprocess
import time
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from user_validator import PassiveSignalMiner, PassiveValidator
from bmad_adapter import PainPoint


# 配置路径
AUTH_FILE = os.path.expanduser("~/.smartfish/mcp/browser_data/xiaohongshu_auth.json")


def get_xiaohongshu_data(keyword: str, max_results: int = 20) -> list:
    """
    使用保存的登录状态获取小红书搜索结果
    
    Args:
        keyword: 搜索关键词
        max_results: 最大结果数
        
    Returns:
        搜索结果列表
    """
    if not os.path.exists(AUTH_FILE):
        print(f"❌ 未找到登录状态文件: {AUTH_FILE}")
        print("   请先运行: npx playwright open --save-storage=<path> https://www.xiaohongshu.com")
        return []
    
    # 使用Playwright运行脚本获取数据
    script = f'''
const {{ chromium }} = require('playwright');

(async () => {{
    const browser = await chromium.launch({{ headless: true }});
    const context = await browser.newContext({{
        storageState: '{AUTH_FILE}'
    }});
    const page = await context.newPage();
    
    // 搜索
    const keyword = encodeURIComponent("{keyword}");
    await page.goto(`https://www.xiaohongshu.com/search_result?keyword=${{keyword}}&source=unknown`);
    await page.waitForTimeout(3000);
    
    // 提取搜索结果
    const results = await page.evaluate(() => {{
        const items = [];
        document.querySelectorAll('section.note-item, section').forEach(el => {{
            const title = el.querySelector('.title')?.innerText || el.querySelector('a')?.innerText;
            const author = el.querySelector('.author .name, .author')?.innerText;
            const link = el.querySelector('a.cover, a')?.href;
            if (title && title.length > 5) {{
                items.push({{ title, author: author || 'unknown', url: link }});
            }}
        }});
        return items.slice(0, {max_results});
    }});
    
    console.log(JSON.stringify(results));
    
    await browser.close();
}})();
'''
    
    try:
        result = subprocess.run(
            ['node', '-e', script],
            capture_output=True,
            text=True,
            timeout=30,
            cwd=os.path.dirname(__file__)
        )
        
        if result.returncode == 0 and result.stdout.strip():
            return json.loads(result.stdout.strip())
        else:
            print(f"⚠️ 获取数据失败: {result.stderr}")
            return []
    except Exception as e:
        print(f"❌ 执行失败: {e}")
        return []


def analyze_pain_point(keyword: str, domain: str = "ai_tools"):
    """
    分析指定关键词的痛点
    
    Args:
        keyword: 搜索关键词
        domain: 领域
    """
    print(f"\n🔍 搜索关键词: {keyword}")
    print("=" * 60)
    
    # 获取真实数据
    print("\n📡 获取小红书真实数据...")
    results = get_xiaohongshu_data(keyword)
    
    if not results:
        print("❌ 未获取到数据")
        return
    
    print(f"✅ 获取到 {len(results)} 条结果")
    
    # 转换为信号挖掘格式
    contents = [
        {
            "text": r.get("title", ""),
            "platform": "xiaohongshu",
            "url": r.get("url")
        }
        for r in results
    ]
    
    # 创建痛点
    pain_point = PainPoint(
        id=f"pp_{keyword[:10]}",
        title=keyword,
        description=f"从小红书搜索「{keyword}」获取的真实数据",
        domain=domain,
        keywords=keyword.split()
    )
    
    # 信号挖掘分析
    print("\n🔬 进行被动信号挖掘分析...")
    validator = PassiveValidator()
    summary = validator.validate_from_content(pain_point, contents)
    result = validator.results[pain_point.id]
    score = validator.calculate_pain_point_score(pain_point.id)
    
    # 输出结果
    print("\n" + "-" * 60)
    print("📊 分析结果:")
    print("-" * 60)
    print(f"   📝 分析内容: {summary.total_content_analyzed} 条")
    print(f"   📈 信号密度: {summary.signal_density:.1%}")
    print(f"   💰 付费意愿信号: {len(result.payment_signals)} 条")
    print(f"   🔥 绝望程度信号: {len(result.desperation_signals)} 条")
    print(f"   🔍 求解意愿信号: {len(result.solution_seeking_signals)} 条")
    print(f"   ✅ 验证状态: {'通过' if summary.is_validated else '未通过'}")
    print(f"   📊 置信度: {summary.confidence_level}")
    print(f"   🏆 综合评分: {score:.2f}/1.00")
    
    if summary.key_insights:
        print("\n📌 关键洞察:")
        for insight in summary.key_insights:
            print(f"   {insight}")
    
    # 保存结果
    output_path = validator.save_results()
    print(f"\n💾 结果已保存到: {output_path}")
    
    return summary, score


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="SmartFish MCP 痛点分析")
    parser.add_argument("keyword", nargs="?", default="ChatGPT 上下文丢失", help="搜索关键词")
    parser.add_argument("--domain", "-d", default="ai_tools", help="领域")
    
    args = parser.parse_args()
    
    print("=" * 60)
    print("🎯 SmartFish MCP 真实数据痛点分析")
    print("=" * 60)
    
    analyze_pain_point(args.keyword, args.domain)
    
    print("\n" + "=" * 60)
    print("✅ 分析完成!")
    print("=" * 60)
