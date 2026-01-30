#!/bin/bash
# SmartFish MCP 一键登录脚本
# 使用方法: ./scripts/mcp_login.sh [platform]

set -e

PLATFORM=${1:-xiaohongshu}
COOKIE_DIR="$HOME/.smartfish/mcp/cookies"
mkdir -p "$COOKIE_DIR"

echo "=============================================="
echo "🔐 SmartFish MCP 登录工具"
echo "=============================================="
echo ""
echo "📡 平台: $PLATFORM"
echo ""

case $PLATFORM in
    xiaohongshu|xhs)
        echo "🚀 启动小红书 MCP (会弹出浏览器窗口)..."
        echo "📱 请在弹出的浏览器中扫码登录小红书"
        echo ""
        npx xiaohongshu-mcp
        ;;
    weibo)
        echo "🚀 启动微博 MCP..."
        npx mcp-server-weibo
        ;;
    zhihu)
        echo "🚀 启动知乎 MCP..."
        echo "📱 如需登录，请使用 login-with-qrcode 工具"
        npx -y zhihu-mcp-server
        ;;
    bilibili|bili)
        echo "🚀 启动B站 MCP..."
        npx bilibili-video-info-mcp
        ;;
    douyin)
        echo "🚀 启动抖音 MCP..."
        npx douyin-mcp-server
        ;;
    all)
        echo "🚀 启动所有 MCP 服务..."
        npx xiaohongshu-mcp &
        npx mcp-server-weibo &
        npx zhihuMcpServer &
        npx bilibili-video-info-mcp &
        wait
        ;;
    *)
        echo "❌ 未知平台: $PLATFORM"
        echo ""
        echo "支持的平台:"
        echo "  xiaohongshu, xhs - 小红书"
        echo "  weibo            - 微博"
        echo "  zhihu            - 知乎"
        echo "  bilibili, bili   - B站"
        echo "  douyin           - 抖音"
        echo "  all              - 全部启动"
        exit 1
        ;;
esac

echo ""
echo "✅ MCP 登录完成！"
echo "💾 Cookie 已保存，后续可直接使用"
