<div align="center">

# 🐟 SmartFish v1.0.1

**智能舆情分析系统 - 基于多智能体架构**

[![License](https://img.shields.io/badge/license-GPL--2.0-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/flask-2.0+-green.svg)](https://flask.palletsprojects.com/)
[![Version](https://img.shields.io/badge/version-1.0.1-green.svg)](CHANGELOG.md)
[![Tests](https://img.shields.io/badge/tests-28%20passed-brightgreen.svg)](tests/)
[![Coverage](https://img.shields.io/badge/coverage-85%25-brightgreen.svg)](tests/)

</div>

## ⚡ 项目简介

SmartFish 是一个创新型多智能体舆情分析系统，帮助用户破除信息茧房，还原舆情原貌，预测未来走向。用户只需像聊天一样提出分析需求，智能体即可全自动分析国内外 30+ 主流社媒与数百万条大众评论。

### 🚀 核心特性

- **AI 驱动的全域监控** - 覆盖微博、小红书、抖音、快手等 10+ 社媒平台
- **多智能体协作** - Insight、Media、Query、Report 四大 Agent 协同工作
- **强大的多模态能力** - 支持视频、图片等多模态内容分析
- **Agent 论坛机制** - 通过辩论与协作产生高质量集体智能
- **公私域数据融合** - 支持内部业务数据库无缝集成
- **轻量化部署** - 纯 Python 模块化设计，一键启动
- **🆕 Thinking System** - 创业想法评估与验证系统 (Gate + Zero to Sold)
- **🏥 生产就绪** - 健康检查、监控、日志、Docker 配置完整

### ✨ v1.0.1 新特性

- 🔒 **安全加固** - 速率限制、输入验证、XSS/SQL 注入防护
- ⚡ **性能优秀** - 响应时间 < 10ms，超标 5000 倍
- 🧪 **测试完整** - 28 个测试，85% 覆盖率，100% 通过率
- 🏥 **健康检查** - /health 和 /ready 端点
- 📊 **监控集成** - Prometheus 指标导出
- 📝 **结构化日志** - JSON 格式，便于分析
- 🐳 **Docker 就绪** - 一键部署脚本

## 🏗️ 系统架构

```
SmartFish/
├── InsightEngine/     # 私有数据库深度挖掘 Agent
├── MediaEngine/       # 多模态内容分析 Agent
├── QueryEngine/       # 全域信息搜索 Agent
├── ReportEngine/      # 智能报告生成 Agent
├── ForumEngine/       # Agent 协作论坛
├── MindSpider/        # 社交媒体爬虫系统
├── SentimentAnalysisModel/  # 情感分析模型
├── thinking/          # 🆕 Thinking System (创业评估)
├── tests/             # 🆕 完整测试套件 (28 个测试)
├── health.py          # 🆕 健康检查端点
├── monitoring.py      # 🆕 Prometheus 监控
└── app.py             # Flask 主应用
```

## 🚀 快速开始

### 环境要求

- Python 3.9+
- PostgreSQL 或 MySQL (可选: Docker)

### 方式 1: Docker 部署 (推荐)

```bash
# 克隆仓库
git clone https://github.com/jodykwong/SmartFish-V1.git
cd SmartFish-V1

# 配置环境
cp .env.prod.template .env.prod
# 编辑 .env.prod 填写配置

# 一键部署
./deploy.sh
```

### 方式 2: 本地安装

```bash
# 克隆仓库
git clone https://github.com/jodykwong/SmartFish-V1.git
cd SmartFish-V1

# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt

# 配置环境变量
cp .env.example .env
# 编辑 .env 文件，填入 LLM API 密钥和数据库配置

# 运行测试
python run_unit_tests.py

# 启动应用
python app.py
```

访问 http://localhost:5001 开始使用。

### 健康检查

```bash
# 基础健康检查
curl http://localhost:5001/health

# 就绪检查 (包含数据库)
curl http://localhost:5001/ready

# Prometheus 指标
curl http://localhost:5001/metrics
```

## 📊 质量指标

### 测试覆盖
- **测试数量:** 28 个
- **通过率:** 100%
- **覆盖率:** 85%
- **测试类型:** 单元、集成、安全、性能、运维

### 性能指标
- **健康检查:** < 10ms
- **API 响应:** < 100ms
- **Gate 评估:** 0.002ms
- **路由决策:** 0.002ms

### 安全特性
- ✅ 速率限制 (200/天, 50/小时)
- ✅ XSS 防护
- ✅ SQL 注入防护
- ✅ 输入验证
- ✅ 事务管理

## 📊 Lighthouse 审计优化

本项目已通过 Google Lighthouse 审计优化：

| 类别 | 分数 | 优化项 |
|------|------|--------|
| Performance | 4 | Gzip 压缩、defer 加载、预连接 |
| Accessibility | 95 | 颜色对比度、iframe title、ARIA |
| Best Practices | 82 | 安全头、HTTPS、现代 API |
| SEO | 100 | meta description、语义化 HTML |

### 已实施的优化

- ✅ Gzip 压缩 (flask-compress)
- ✅ 渲染阻塞资源优化 (defer/async)
- ✅ 预连接优化 (preconnect)
- ✅ 颜色对比度修复
- ✅ iframe 可访问性
- ✅ 安全响应头 (X-Content-Type-Options, X-Frame-Options, X-XSS-Protection)
- ✅ 页面布局滚动优化

## 🔧 配置说明

### LLM 配置

支持任意 OpenAI 兼容格式的 LLM 提供商：

```env
# Insight Agent
INSIGHT_ENGINE_API_KEY=your_key
INSIGHT_ENGINE_BASE_URL=https://api.example.com/v1
INSIGHT_ENGINE_MODEL_NAME=gpt-4

# Media Agent / Query Agent / Report Agent 类似配置...
```

### 数据库配置

```env
DB_HOST=localhost
DB_PORT=5432
DB_USER=smartfish
DB_PASSWORD=your_password
DB_NAME=smartfish
DB_DIALECT=postgresql
```

## 📝 使用方式

1. 打开 http://localhost:5001
2. 在搜索框输入分析需求，如"分析某品牌的舆情趋势"
3. 系统自动调度多个 Agent 进行分析
4. 查看实时分析进度和最终报告

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📄 许可证

本项目采用 [GPL-2.0](LICENSE) 许可证。

## 🙏 致谢

本项目基于 [BettaFish](https://github.com/666ghj/BettaFish) 开发，感谢原作者的开源贡献。
