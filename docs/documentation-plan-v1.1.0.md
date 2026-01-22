# SmartFish 文档计划 v1.1.0

## 文档结构

```
docs/
├── getting-started/
│   ├── installation.md          # 完整安装指南
│   ├── quick-start.md           # 5分钟快速开始
│   └── configuration.md         # 配置说明
├── user-guide/
│   ├── sentiment-analysis.md    # 舆情分析使用
│   ├── thinking-system.md       # Thinking System 指南
│   └── report-generation.md     # 报告生成
├── api/
│   ├── openapi.yaml             # OpenAPI 规范
│   ├── thinking-api.md          # Thinking API (已完成)
│   └── sentiment-api.md         # 舆情分析 API
├── deployment/
│   ├── docker.md                # Docker 部署
│   ├── production.md            # 生产环境配置
│   ├── monitoring.md            # 监控设置
│   └── backup.md                # 备份策略
├── development/
│   ├── architecture.md          # 架构文档 (已存在)
│   ├── contributing.md          # 贡献指南 (已存在)
│   └── testing.md               # 测试指南
└── troubleshooting/
    ├── common-issues.md         # 常见问题
    └── faq.md                   # FAQ
```

---

## 优先级文档 (Week 2-3)

### 🔴 P0 - 必须完成

#### 1. 完整安装指南
**文件:** `docs/getting-started/installation.md`

**内容大纲:**
```markdown
# SmartFish 安装指南

## 系统要求
- OS: Ubuntu 20.04+ / macOS 12+ / Windows 10+
- Python: 3.9+
- 数据库: PostgreSQL 13+ 或 MySQL 8+
- 内存: 最低 4GB，推荐 8GB

## 安装步骤

### 1. 克隆仓库
### 2. 创建虚拟环境
### 3. 安装依赖
### 4. 配置数据库
### 5. 运行迁移
### 6. 启动应用

## 验证安装
- 健康检查
- 测试 API
- 访问 Web 界面

## 故障排查
- 常见错误及解决方案
```

#### 2. 快速开始教程
**文件:** `docs/getting-started/quick-start.md`

**目标:** 5 分钟内完成第一次舆情分析

```markdown
# 5 分钟快速开始

## 步骤 1: 启动应用
\`\`\`bash
docker-compose up -d
\`\`\`

## 步骤 2: 创建第一个分析任务
\`\`\`bash
curl -X POST http://localhost:5000/api/analysis \
  -H "Content-Type: application/json" \
  -d '{"topic": "人工智能", "platforms": ["weibo"]}'
\`\`\`

## 步骤 3: 查看结果
访问: http://localhost:5000/reports
```

#### 3. API 文档 (OpenAPI)
**文件:** `docs/api/openapi.yaml`

**工具:** 使用 Swagger/ReDoc 生成交互式文档

---

### 🟡 P1 - 重要但非阻塞

#### 4. 生产部署指南
**文件:** `docs/deployment/production.md`

**内容:**
- 环境变量配置
- SSL/TLS 设置
- 反向代理配置
- 数据库优化
- 性能调优

#### 5. 监控与告警
**文件:** `docs/deployment/monitoring.md`

**内容:**
- 日志配置
- 指标收集
- 告警规则
- 仪表板设置

---

### 🟢 P2 - 可选增强

#### 6. 架构决策记录 (ADR)
**目录:** `docs/adr/`

**示例:**
```markdown
# ADR-001: 使用独立 database.py 模块

## 状态
已接受 (2026-01-22)

## 背景
循环导入问题: app.py -> thinking -> models -> app.db

## 决策
创建独立 database.py 模块，解耦数据库初始化

## 后果
- 正面: 解决循环导入，代码更清晰
- 负面: 需要更新所有导入语句
```

---

## 文档质量标准

### 写作原则
1. **清晰优先:** 使用简单语言，避免行话
2. **示例驱动:** 每个概念都有代码示例
3. **可操作性:** 每个指南都可以直接执行
4. **最新性:** 与代码同步更新

### 验收标准
- [ ] 新用户可在 30 分钟内完成部署
- [ ] 所有 API 有示例和响应说明
- [ ] 常见问题有解决方案
- [ ] 文档无死链接
- [ ] 代码示例可运行

---

## 执行计划

**Week 2:**
- Day 1-2: 完整安装指南 + 快速开始
- Day 3: API 文档 (OpenAPI)
- Day 4: 生产部署指南

**Week 3:**
- Day 1: 监控与告警文档
- Day 2: 故障排查指南
- Day 3: 文档审核与测试

---

## 文档工具

- **Markdown:** 所有文档使用 Markdown
- **MkDocs:** 生成静态文档站点
- **Swagger UI:** API 交互式文档
- **Mermaid:** 架构图和流程图

---

## 文档维护

### 更新触发器
- 代码变更 → 更新相关文档
- 用户反馈 → 更新故障排查
- 新功能 → 更新用户指南

### 审核流程
1. 技术审核 (Amelia)
2. 用户体验审核 (Sally)
3. 最终批准 (BMad Master)
