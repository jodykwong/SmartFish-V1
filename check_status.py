#!/usr/bin/env python3
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

print("=" * 60)
print("🐟 SmartFish 配置状态检查")
print("=" * 60)
print()

# 检查 LLM 配置
openrouter_key = os.getenv('OPENROUTER_API_KEY', '')
if openrouter_key and openrouter_key.startswith('sk-or-v1-'):
    print("✅ LLM 配置: OpenRouter 统一模式已启用")
    print(f"   API Key: {openrouter_key[:20]}...")
else:
    print("❌ LLM 配置: 未配置")

print()

# 检查数据库配置
db_host = os.getenv('DB_HOST', '')
db_user = os.getenv('DB_USER', '')
db_name = os.getenv('DB_NAME', '')

if db_host not in ['your_db_host', '']:
    print(f"✅ 数据库配置: {db_user}@{db_host}/{db_name}")
else:
    print("❌ 数据库配置: 未配置（使用默认占位符）")
    print("   这是唯一需要修复的配置项！")

print()

# 检查搜索工具
tavily_key = os.getenv('TAVILY_API_KEY', '')
if tavily_key and tavily_key.startswith('tvly-'):
    print(f"✅ 搜索工具: Tavily 已配置")
else:
    print("⚠️  搜索工具: 未配置")

print()
print("=" * 60)

if db_host in ['your_db_host', '']:
    print("⚠️  需要配置数据库才能启动项目")
    print()
    print("快速配置步骤:")
    print("1. 编辑 .env 文件")
    print("2. 修改以下配置:")
    print("   DB_HOST=localhost")
    print("   DB_USER=smartfish")
    print("   DB_PASSWORD=your_password")
    print("   DB_NAME=smartfish_db")
    print("   DB_DIALECT=postgresql  # 或 mysql")
else:
    print("🎉 配置完整！可以启动项目了！")
    print()
    print("启动命令:")
    print("  source venv/bin/activate")
    print("  python app.py")

print("=" * 60)
