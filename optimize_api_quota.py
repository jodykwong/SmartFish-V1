#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SmartFish API 配额优化脚本
自动优化配置以减少 API 调用次数
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# 加载 .env 文件
env_path = Path(__file__).parent / '.env'
load_dotenv(env_path)

def optimize_for_free_tier():
    """优化配置以适应免费 API 配额"""
    
    print("=" * 60)
    print("🔧 SmartFish API 配额优化")
    print("=" * 60)
    print()
    
    # 读取当前配置
    env_lines = []
    if env_path.exists():
        env_lines = env_path.read_text(encoding='utf-8').splitlines()
    
    # 优化参数
    optimizations = {
        'MAX_REFLECTIONS': '1',  # 从 3 减少到 1
        'MAX_PARAGRAPHS': '4',   # 从 6 减少到 4
        'MAX_SEARCH_RESULTS_FOR_LLM': '50',  # 限制搜索结果
        'MAX_HIGH_CONFIDENCE_SENTIMENT_RESULTS': '30',  # 限制情感分析结果
    }
    
    # 查找并更新配置
    updated_count = 0
    added_count = 0
    
    for key, value in optimizations.items():
        found = False
        for i, line in enumerate(env_lines):
            if line.strip().startswith(f"{key}="):
                old_value = line.split('=', 1)[1] if '=' in line else ''
                env_lines[i] = f"{key}={value}"
                print(f"✅ 更新 {key}: {old_value} → {value}")
                updated_count += 1
                found = True
                break
        
        if not found:
            # 添加新配置
            env_lines.append(f"{key}={value}")
            print(f"➕ 添加 {key}={value}")
            added_count += 1
    
    # 写入文件
    env_path.write_text('\n'.join(env_lines) + '\n', encoding='utf-8')
    
    print()
    print("=" * 60)
    print(f"✅ 优化完成！")
    print(f"   更新: {updated_count} 项")
    print(f"   添加: {added_count} 项")
    print()
    print("📊 优化效果:")
    print("   - API 调用次数: 减少约 40%")
    print("   - 每次报告: 从 37 次 → 约 22 次")
    print("   - 每天可生成: 从 1 次 → 2-3 次")
    print()
    print("⚠️  注意:")
    print("   - 报告质量可能略有下降")
    print("   - 反思次数减少，分析深度降低")
    print("   - 适合快速生成和测试使用")
    print("=" * 60)

def restore_default():
    """恢复默认配置"""
    
    print("=" * 60)
    print("🔄 恢复默认配置")
    print("=" * 60)
    print()
    
    # 读取当前配置
    env_lines = []
    if env_path.exists():
        env_lines = env_path.read_text(encoding='utf-8').splitlines()
    
    # 默认参数
    defaults = {
        'MAX_REFLECTIONS': '3',
        'MAX_PARAGRAPHS': '6',
        'MAX_SEARCH_RESULTS_FOR_LLM': '100',
        'MAX_HIGH_CONFIDENCE_SENTIMENT_RESULTS': '50',
    }
    
    # 查找并更新配置
    updated_count = 0
    
    for key, value in defaults.items():
        for i, line in enumerate(env_lines):
            if line.strip().startswith(f"{key}="):
                old_value = line.split('=', 1)[1] if '=' in line else ''
                env_lines[i] = f"{key}={value}"
                print(f"✅ 恢复 {key}: {old_value} → {value}")
                updated_count += 1
                break
    
    # 写入文件
    env_path.write_text('\n'.join(env_lines) + '\n', encoding='utf-8')
    
    print()
    print("=" * 60)
    print(f"✅ 恢复完成！已恢复 {updated_count} 项配置")
    print("=" * 60)

def show_current_config():
    """显示当前配置"""
    
    print("=" * 60)
    print("📋 当前配置")
    print("=" * 60)
    print()
    
    config_keys = [
        'MAX_REFLECTIONS',
        'MAX_PARAGRAPHS',
        'MAX_SEARCH_RESULTS_FOR_LLM',
        'MAX_HIGH_CONFIDENCE_SENTIMENT_RESULTS',
    ]
    
    for key in config_keys:
        value = os.getenv(key, '未设置')
        print(f"  {key}: {value}")
    
    print()
    print("=" * 60)

def main():
    """主函数"""
    import sys
    
    if len(sys.argv) < 2:
        print("使用方法:")
        print("  python optimize_api_quota.py optimize   # 优化配置（减少 API 调用）")
        print("  python optimize_api_quota.py restore    # 恢复默认配置")
        print("  python optimize_api_quota.py show       # 显示当前配置")
        sys.exit(1)
    
    command = sys.argv[1].lower()
    
    if command == 'optimize':
        optimize_for_free_tier()
    elif command == 'restore':
        restore_default()
    elif command == 'show':
        show_current_config()
    else:
        print(f"❌ 未知命令: {command}")
        print("可用命令: optimize, restore, show")
        sys.exit(1)

if __name__ == '__main__':
    main()
