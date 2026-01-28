#!/bin/bash
# MCP 社交媒体工具安装脚本
# SmartFish Project - MCP Clients Installation

echo "=========================================="
echo "SmartFish MCP 工具安装脚本"
echo "=========================================="

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 检查 npm
check_npm() {
    if command -v npm &> /dev/null; then
        echo -e "${GREEN}✓ npm 已安装${NC}"
        return 0
    else
        echo -e "${RED}✗ npm 未安装，请先安装 Node.js${NC}"
        return 1
    fi
}

# 检查 Python
check_python() {
    if command -v python3 &> /dev/null || command -v python &> /dev/null; then
        echo -e "${GREEN}✓ Python 已安装${NC}"
        return 0
    else
        echo -e "${RED}✗ Python 未安装${NC}"
        return 1
    fi
}

# 安装 npm 包
install_npm_package() {
    local package=$1
    echo -e "\n${YELLOW}正在安装 $package...${NC}"
    npm install -g "$package" 2>&1 | grep -E "(added|up to date|error)" || true
}

echo ""
echo "1. 检查环境..."
check_npm
check_python

echo ""
echo "2. 安装 npm 全局包..."

# 小红书 MCP
echo -e "\n${YELLOW}[1/3] 小红书 MCP${NC}"
install_npm_package "xiaohongshu-mcp"

# 微博 MCP
echo -e "\n${YELLOW}[2/3] 微博 MCP${NC}"
install_npm_package "mcp-server-weibo"

# B站 MCP
echo -e "\n${YELLOW}[3/3] B站 MCP${NC}"
install_npm_package "bilibili-mcp"

echo ""
echo "3. 安装 Python 工具..."

# 安装 uv (提供 uvx 命令)
echo -e "\n${YELLOW}安装 uv (提供 uvx 命令)...${NC}"
pip install uv 2>&1 | grep -E "(Successfully|already)" || pip3 install uv 2>&1 | grep -E "(Successfully|already)" || true

echo ""
echo "=========================================="
echo "安装完成！"
echo ""
echo "已安装的工具:"
echo "  ✓ xiaohongshu-mcp (npm 包)"
echo "  ✓ mcp-server-weibo (npm 包)"
echo "  ✓ bilibili-mcp (npm 包)"
echo "  ✓ uv/uvx (Python 工具)"
echo ""
echo "可选安装 (需要手动配置):"
echo ""
echo "  知乎 MCP (npx 运行):"
echo "    npx github:morrain/zhihuMcpServer"
echo ""
echo "  抖音 MCP (uvx 运行):"
echo "    uvx douyin-mcp-server"
echo "    需要配置环境变量: DASHSCOPE_API_KEY"
echo ""
echo "  多平台 MCP (需要克隆):"
echo "    git clone https://github.com/brucehe3/video-sum-mcp.git"
echo "    cd video-sum-mcp && pip install -r requirements.txt"
echo "=========================================="
