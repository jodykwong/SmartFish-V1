#!/bin/bash
# 一键部署脚本

set -e

echo "🚀 SmartFish 生产部署"
echo "====================="

# 检查环境文件
if [ ! -f .env.prod ]; then
    echo "❌ 错误: .env.prod 不存在"
    echo "请复制 .env.prod.template 并配置"
    exit 1
fi

# 拉取最新代码（跳过，使用本地代码）
echo "📦 使用本地代码..."
# git pull

# 构建镜像
echo "🔨 构建 Docker 镜像..."
docker-compose -f docker-compose.prod.yml build

# 停止旧容器
echo "🛑 停止旧容器..."
docker-compose -f docker-compose.prod.yml down

# 启动新容器
echo "▶️  启动新容器..."
docker-compose -f docker-compose.prod.yml up -d

# 等待健康检查
echo "🏥 等待健康检查..."
sleep 10

# 检查健康状态
if curl -f http://localhost:5000/health > /dev/null 2>&1; then
    echo "✅ 部署成功！"
    echo "🌐 应用运行在: http://localhost:5000"
else
    echo "❌ 健康检查失败"
    docker-compose -f docker-compose.prod.yml logs --tail=50
    exit 1
fi
