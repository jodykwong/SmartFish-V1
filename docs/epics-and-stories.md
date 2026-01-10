---
stepsCompleted: [1, 2, 3]
inputDocuments: [docs/prd.md, docs/architecture.md]
workflowType: 'epics-and-stories'
lastStep: 3
project_name: 'SmartFish'
user_name: 'Jody'
date: '2026-01-10'
---

# Epics & User Stories - SmartFish

**Author:** Jody  
**Date:** 2026-01-10

---

## Epic Overview

| Epic | 名称 | 故事数 | 优先级 | 依赖 |
|------|------|-------|-------|------|
| E1 | 配置基础设施 | 3 | P0 | - |
| E2 | 模板选择系统 | 4 | P0 | E1 |
| E3 | 分析方法选择器 | 4 | P0 | E1 |
| E4 | 需求验证系统 | 3 | P0 | E1 |
| E5 | 智能推荐 | 2 | P1 | E2, E3 |

---

## Epic 1: 配置基础设施

**目标:** 建立 YAML 配置加载机制，为模板和方法选择提供数据基础

### Story 1.1: 配置加载器

**作为** 系统  
**我想要** 启动时自动加载所有 YAML 配置  
**以便** API 和各模块可以访问模板/方法数据

**验收标准:**
- [ ] 创建 `config/loader.py` 单例类
- [ ] 扫描 `config/template_meta/*.yaml` 加载模板元数据
- [ ] 扫描 `config/analysis_methods/**/*.yaml` 加载方法配置
- [ ] 提供 `get_templates()` 和 `get_methods(category)` 方法
- [ ] 启动时加载，缓存到内存

**技术说明:**
- 使用 PyYAML 解析
- 单例模式确保只加载一次
- 错误处理：配置文件格式错误时记录日志但不阻止启动

**文件:** `config/__init__.py`, `config/loader.py`

---

### Story 1.2: 模板元数据配置

**作为** 管理员  
**我想要** 通过 YAML 文件定义模板元数据  
**以便** 前端可以展示模板信息和预览

**验收标准:**
- [ ] 为 8 个现有模板创建元数据文件
- [ ] 每个文件包含: id, name, icon, tags, description, chapter_count, chapters, recommended_keywords
- [ ] 文件位于 `config/template_meta/` 目录

**示例配置:**
```yaml
# brand_reputation.yaml
id: brand_reputation
name: 企业品牌声誉分析报告
icon: 🏢
tags: [品牌监测, 声誉管理, 公关评估]
description: 全面分析企业品牌在各渠道的声量、情感和风险
chapter_count: 7
chapters:
  - "1.0 摘要与核心发现"
  - "2.0 品牌声量与影响力分析"
  - "3.0 本周期关键事件回顾"
  - "4.0 品牌形象与用户认知"
  - "5.0 用户画像分析"
  - "6.0 声誉风险与机遇洞察"
  - "7.0 结论与战略建议"
recommended_keywords: [品牌, 声誉, 口碑, 形象, 公关]
```

**文件:** `config/template_meta/*.yaml` (9 个文件，含新增 narrow_door.yaml)

---

### Story 1.3: 分析方法配置

**作为** 管理员  
**我想要** 通过 YAML 文件定义分析方法  
**以便** 前端可以展示方法列表和详情

**验收标准:**
- [ ] 为 38 种方法创建配置文件
- [ ] 按分类组织: brainstorming/, advanced/, gamification/
- [ ] 每个文件包含: id, name, category, icon, short_description, full_description, suitable_for, prompt_template

**示例配置:**
```yaml
# six_hats.yaml
id: six_hats
name: 六顶思考帽
category: brainstorming
icon: 🎩
short_description: 用六种不同视角分析问题
full_description: |
  🎩 白帽 - 客观事实与数据
  ❤️ 红帽 - 直觉与情感反应
  🖤 黑帽 - 风险与潜在问题
  💛 黄帽 - 价值与积极面
  💚 绿帽 - 创意与新想法
  💙 蓝帽 - 流程与总结
suitable_for: [全面分析, 团队讨论, 决策评估]
prompt_template: |
  请使用六顶思考帽方法分析以下问题，从六个视角依次展开：
  白帽（事实）、红帽（情感）、黑帽（风险）、
  黄帽（价值）、绿帽（创意）、蓝帽（总结）
```

**文件:** `config/analysis_methods/**/*.yaml` (38 个文件)

---

## Epic 2: 模板选择系统

**目标:** 用户可以查看、预览和选择报告模板

### Story 2.1: 模板列表 API

**作为** 前端  
**我想要** 获取所有模板的元数据  
**以便** 展示模板卡片列表

**验收标准:**
- [ ] 创建 `GET /api/templates` 端点
- [ ] 返回所有模板的元数据列表
- [ ] 响应时间 < 50ms（内存读取）

**响应格式:**
```json
{
  "templates": [
    {
      "id": "brand_reputation",
      "name": "企业品牌声誉分析报告",
      "icon": "🏢",
      "tags": ["品牌监测", "声誉管理"],
      "chapter_count": 7
    }
  ]
}
```

**文件:** `app.py`

---

### Story 2.2: 模板预览 API

**作为** 前端  
**我想要** 获取单个模板的完整信息  
**以便** 展示预览弹窗

**验收标准:**
- [ ] 创建 `GET /api/templates/<template_id>` 端点
- [ ] 返回完整元数据包括 chapters 列表
- [ ] 模板不存在时返回 404

**响应格式:**
```json
{
  "id": "brand_reputation",
  "name": "企业品牌声誉分析报告",
  "icon": "🏢",
  "tags": ["品牌监测", "声誉管理", "公关评估"],
  "description": "全面分析企业品牌...",
  "chapter_count": 7,
  "chapters": [
    "1.0 摘要与核心发现",
    "2.0 品牌声量与影响力分析",
    ...
  ]
}
```

**文件:** `app.py`

---

### Story 2.3: 模板卡片组件

**作为** 用户  
**我想要** 看到模板卡片列表  
**以便** 快速浏览可用模板

**验收标准:**
- [ ] 创建 TemplateCard 组件
- [ ] 显示: icon, name, tags, chapter_count
- [ ] 点击卡片选中（边框高亮）
- [ ] 包含 [预览] 按钮
- [ ] 响应式: 桌面 4 列，平板 2 列，手机 1 列

**文件:** `static/js/template-selector.js`, `static/css/smartfish.css`

---

### Story 2.4: 模板预览弹窗

**作为** 用户  
**我想要** 预览模板的章节结构  
**以便** 确认选择正确的模板

**验收标准:**
- [ ] 创建 TemplatePreviewModal 组件
- [ ] 显示: name, tags, description, chapters 树形结构
- [ ] 包含 [取消] 和 [使用此模板] 按钮
- [ ] 支持 ESC 键关闭
- [ ] 点击弹窗外关闭

**文件:** `static/js/template-selector.js`, `templates/index.html`

---

## Epic 3: 分析方法选择器

**目标:** 用户可以浏览、了解和选择分析方法

### Story 3.1: 方法列表 API

**作为** 前端  
**我想要** 获取分析方法列表  
**以便** 展示方法选择器

**验收标准:**
- [ ] 创建 `GET /api/methods` 端点
- [ ] 支持 `?category=brainstorming` 筛选
- [ ] 返回方法基本信息列表

**响应格式:**
```json
{
  "methods": [
    {
      "id": "six_hats",
      "name": "六顶思考帽",
      "category": "brainstorming",
      "icon": "🎩",
      "short_description": "用六种不同视角分析问题"
    }
  ]
}
```

**文件:** `app.py`

---

### Story 3.2: 方法详情 API

**作为** 前端  
**我想要** 获取方法的完整说明  
**以便** 展示悬浮提示

**验收标准:**
- [ ] 创建 `GET /api/methods/<method_id>` 端点
- [ ] 返回完整信息包括 full_description 和 suitable_for

**文件:** `app.py`

---

### Story 3.3: 方法选择器组件

**作为** 用户  
**我想要** 按分类浏览和选择分析方法  
**以便** 增强报告分析深度

**验收标准:**
- [ ] 创建 MethodSelector 组件
- [ ] 标签页切换: 头脑风暴(20) / 高级引导(15) / 游戏化(3)
- [ ] 复选框多选方法
- [ ] 底部显示已选方法摘要
- [ ] [清除全部] 按钮
- [ ] 默认折叠状态

**文件:** `static/js/method-selector.js`, `static/css/smartfish.css`

---

### Story 3.4: 方法详情提示

**作为** 用户  
**我想要** 悬停查看方法详细说明  
**以便** 了解方法适用场景

**验收标准:**
- [ ] 创建 MethodTooltip 组件
- [ ] 悬停 [?] 图标显示提示
- [ ] 显示: full_description, suitable_for
- [ ] 延迟 200ms 显示，100ms 隐藏
- [ ] 支持 Focus 触发（键盘访问）

**文件:** `static/js/method-selector.js`

---

## Epic 4: 需求验证系统

**目标:** 自动检查报告是否满足用户需求

### Story 4.1: 需求验证节点

**作为** 系统  
**我想要** 在报告生成后验证是否满足需求  
**以便** 提高报告质量

**验收标准:**
- [ ] 创建 `RequirementValidationNode` 类
- [ ] 从用户 query 提取数量要求（如"5个方向"）
- [ ] 检查报告章节数是否满足
- [ ] 检查是否有结论章节
- [ ] 返回验证结果（通过/失败/警告）

**文件:** `ReportEngine/nodes/requirement_validation_node.py`

---

### Story 4.2: 结论章节强制

**作为** 系统  
**我想要** 确保所有报告都有结论章节  
**以便** 用户获得可行动的建议

**验收标准:**
- [ ] 修改所有模板，确保包含结论章节
- [ ] 验证节点检查结论章节存在
- [ ] 结论章节为空时标记为失败

**文件:** `ReportEngine/report_template/*.md`, `ReportEngine/nodes/requirement_validation_node.py`

---

### Story 4.3: 方法论注入

**作为** 系统  
**我想要** 将用户选择的分析方法注入 Agent prompt  
**以便** Agent 按方法论进行分析

**验收标准:**
- [ ] 修改 `ForumEngine/llm_host.py`
- [ ] `build_host_prompt()` 接收 `selected_methods` 参数
- [ ] 将方法的 `prompt_template` 追加到主持人 prompt
- [ ] 无选择时使用默认 prompt

**文件:** `ForumEngine/llm_host.py`

---

## Epic 5: 智能推荐

**目标:** 根据用户输入推荐合适的模板

### Story 5.1: 模板推荐逻辑

**作为** 系统  
**我想要** 根据用户输入推荐模板  
**以便** 降低用户决策负担

**验收标准:**
- [ ] 创建推荐函数
- [ ] 匹配用户输入与模板 `recommended_keywords`
- [ ] 返回匹配度最高的模板 ID
- [ ] 无匹配时不推荐

**匹配规则:**
- 用户输入包含"品牌"/"声誉" → brand_reputation
- 用户输入包含"竞品"/"市场" → market_competition
- 用户输入包含"危机"/"公关" → crisis_pr

**文件:** `static/js/smart-recommend.js` 或 `app.py`

---

### Story 5.2: 推荐标记展示

**作为** 用户  
**我想要** 看到推荐的模板标记  
**以便** 快速做出选择

**验收标准:**
- [ ] 用户输入时触发推荐计算
- [ ] 推荐模板显示 ✓推荐 标记
- [ ] 输入变化时更新推荐
- [ ] 防抖处理（300ms）

**文件:** `static/js/smart-recommend.js`, `static/css/smartfish.css`

---

## Implementation Order

```
Week 1:
├── E1.1 配置加载器
├── E1.2 模板元数据配置 (8 个文件)
└── E1.3 分析方法配置 (38 个文件)

Week 2:
├── E2.1 模板列表 API
├── E2.2 模板预览 API
├── E2.3 模板卡片组件
├── E2.4 模板预览弹窗
├── E3.1 方法列表 API
├── E3.2 方法详情 API
├── E3.3 方法选择器组件
└── E3.4 方法详情提示

Week 3:
├── E4.1 需求验证节点
├── E4.2 结论章节强制
├── E4.3 方法论注入
├── E5.1 模板推荐逻辑
└── E5.2 推荐标记展示
```

---

## Definition of Done

每个 Story 完成需满足:
- [ ] 代码实现并通过自测
- [ ] 符合架构文档约束
- [ ] 无新增外部依赖
- [ ] 与现有功能兼容
