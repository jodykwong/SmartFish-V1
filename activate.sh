#!/bin/bash
# SmartFish 项目激活脚本

echo "🐟 激活 SmartFish 虚拟环境..."
source venv/bin/activate

echo "✅ 虚拟环境已激活"
echo "📁 当前目录: $(pwd)"
echo "🐍 Python 版本: $(python --version)"

echo ""
echo "🚀 可用命令:"
echo "  python app.py                    # 启动主应用"
echo "  streamlit run app.py             # 启动 Streamlit 界面"
echo "  python init_db_helper.py         # 初始化数据库"
echo "  deactivate                       # 退出虚拟环境"
echo ""
echo "📝 配置文件: .env (请根据需要修改API密钥等配置)"
echo ""
