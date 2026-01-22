---
stepsCompleted: [1, 2]
inputDocuments:
  - /home/sunrise/SmartFish/_bmad-output/planning-artifacts/prd.md
  - /home/sunrise/SmartFish/_bmad-output/planning-artifacts/architecture.md
  - /home/sunrise/SmartFish/_bmad-output/planning-artifacts/ux-design-specification.md
---

# SmartFish - Epic Breakdown

## Overview

This document provides the complete epic and story breakdown for SmartFish思考决策系统, decomposing the requirements from the PRD, UX Design, and Architecture into implementable stories.

## Requirements Inventory

### Functional Requirements

**FR1**: 思考条目CRUD - 支持创建/编辑/归档思考条目，包含核心字段（Signal/Target/Problem/Hypothesis/MVA/Success Metric/Constraints）

**FR1.1**: 方向研究扩展字段 - 支持Zero to Sold扩展字段（Audience定义/规模估算/支付能力/Tribes/市场信号/问题强度评分）

**FR2**: 检索与筛选 - 按日期/状态/路由类型/主题标签筛选，支持全文搜索

**FR3**: Gate校验机制 - 每条思考条目必须完成Gate校验并生成不可篡改审计记录

**FR4**: 四层过滤器 - 人性依赖/价值自证/反馈清洁度/角色消耗四层过滤

**FR5**: 否决处理 - 任一层触发否决则条目状态置为"已否决"，必须填写原因

**FR6**: 工作流路由 - Gate通过后路由到Quick/Standard/Enterprise工作流并生成对应工件

**FR6.1**: Research工件 - 生成market-research.md和interview-guide.md

**FR7**: 路由选择方式 - 支持手动选择和自动建议（基于影响范围/依赖/风险）

**FR8**: 工件输出规范 - 文件命名规范、保存位置可配置

**FR9**: 导出功能 - 单条或多条条目导出Markdown/PDF

**FR10**: 调研任务生成 - 对Evidence Needed生成调研任务并调用Agent（QueryEngine/MindSpider/InsightEngine/ReportEngine）

**FR10.1**: 市场声音任务 - 基于Tribe/Water cooler列表生成搜索/抓取计划

**FR11**: 证据回填 - 调研结果可回填到条目并与工件联动

**FR12**: 周度评审页面 - 聚合最近7天条目，支持打分和生成weekly-plan.md

**FR13**: Audience/Problem/Solution/Product向导 - 引导用户按正确顺序定义

**FR14**: 问题强度评分 - 用Eisenhower框架打分（重要性×紧迫性）

**FR15**: 访谈脚本生成与偏差控制 - 生成访谈提纲，包含禁问清单和偏差检测

**FR16**: 市场转向复核 - 按月/季度回顾市场信号并生成market-review.md

### Non-Functional Requirements

**NFR1**: 可追溯性 - 完整操作时间线，状态变更历史，审计日志不可篡改

**NFR2**: 可复用性 - 工件模板可配置，支持二次编辑和版本历史

**NFR3**: 稳定性 - 任务失败自动重试（最多3次），失败原因可见

**NFR4**: 性能 - 1000条目下列表加载<1秒，Gate检查<2秒，工件生成<5秒

**NFR5**: 可测试性 - 单元测试覆盖率>80%，集成测试覆盖核心流程

**NFR6**: 可解释性 - 所有自动建议显示依据和规则

### Additional Requirements

**Architecture Requirements:**

- 独立Blueprint + 服务层架构（thinking模块）
- 数据库迁移脚本（4个新表：thinking_entries/gate_reviews/artifacts/research_tasks）
- 文件系统工件存储（docs/thinking/目录）
- Gate规则引擎（策略模式 + 规则类）
- 路由决策算法（基于规则的评分系统）
- 工件模板系统（Jinja2 + 文件系统）
- RESTful API设计（8个核心端点）
- 分层架构（Routes → Services → Models → DB）
- 多层安全防护（认证/授权/输入验证/文件路径安全）
- 数据库索引优化（3个核心索引）
- 分层测试策略（单元/集成/E2E）
- Phase 3引入Celery + Redis（异步任务处理）

**UX Requirements:**

- 渐进式披露交互模式
- 即时反馈（Gate检查实时显示结果）
- 智能建议（路由选择自动推荐）
- 键盘导航支持
- 响应式设计（Phase 1仅支持桌面≥768px）
- WCAG 2.1 AA可访问性标准
- 性能目标（首屏<2秒，交互<100ms）
- 6个关键页面（列表/详情/Gate/结构化思考/路由选择/工件生成）

### FR Coverage Map

| Epic | FRs覆盖 | NFRs覆盖 | Phase |
|------|---------|----------|-------|
| Epic 1 | FR1, FR2, FR1.1 | NFR4, NFR5 | Phase 1 |
| Epic 2 | FR3, FR4, FR5 | NFR1, NFR6 | Phase 1 |
| Epic 3 | FR6, FR7, FR8, FR9 | NFR2, NFR4 | Phase 1-2 |
| Epic 4 | FR12 | NFR4 | Phase 2 |
| Epic 5 | FR10, FR10.1, FR11 | NFR3, NFR4 | Phase 3 |
| Epic 6 | FR13, FR14, FR15, FR16, FR6.1 | NFR6 | Phase 4 |

**覆盖率：** 16/16 FRs ✅ | 6/6 NFRs ✅

## Epic List

### Epic 1: 基础思考条目管理
用户可以记录和管理每日商业思考，包括创建、编辑、查看和筛选思考条目。
**FRs covered:** FR1, FR2, FR1.1

### Epic 2: 决策宪法Gate机制
用户可以通过四层Gate筛选想法，避免在错误方向上投入，所有决策可追溯。
**FRs covered:** FR3, FR4, FR5

### Epic 3: BMAD工作流路由与工件生成
用户可以将通过Gate的想法转化为可执行工件（tech-spec/PRD/architecture），支持三种路由类型。
**FRs covered:** FR6, FR7, FR8, FR9

### Epic 4: 周度评审与复盘
用户可以定期评审最近思考，打分并选择Top N进入执行计划。
**FRs covered:** FR12

### Epic 5: Agent集成与证据补强
用户可以调用AI Agent自动补强证据，支持异步任务和结果回填。
**FRs covered:** FR10, FR10.1, FR11

### Epic 6: Zero to Sold方法论向导
用户可以使用结构化方法论进行市场研究，包括受众分析、问题验证和市场复核。
**FRs covered:** FR13, FR14, FR15, FR16, FR6.1
