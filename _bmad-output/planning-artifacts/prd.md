---
stepsCompleted: ['step-01-init', 'step-02-discovery', 'step-03-success', 'step-04-journeys', 'step-05-domain', 'step-06-innovation', 'step-07-project-type', 'step-08-scoping', 'step-09-functional', 'step-10-nonfunctional', 'step-11-polish', 'step-12-complete']
inputDocuments:
  - /home/sunrise/SmartFish/_bmad-output/planning-artifacts/product-brief-SmartFish-2026-01-22.md
  - /home/sunrise/SmartFish/requests.md
  - /home/sunrise/SmartFish/docs/thinking-system-analysis.md
workflowType: 'prd'
briefCount: 1
researchCount: 0
brainstormingCount: 0
projectDocsCount: 3
projectType: 'web-application'
domain: 'productivity-decision-support'
projectContext: 'brownfield-extension'
domainComplexity: 'medium'
technicalStack: 'flask-postgresql-jinja2'
integrationScope: 'deep-agent-integration'
---

# Product Requirements Document - SmartFish 思考决策系统

**Author:** Jody
**Date:** 2026-01-22

---

## 1. 项目概述

### 1.1 项目背景

SmartFish V1当前定位为多智能体舆情分析系统，用户通过对话方式触发Insight/Media/Query/Report等Agent产出分析报告。但在实际使用中，用户的商业思考和策略想法存在两个关键断点：

1. **缺少强约束筛选**：想法进入分析或开发前没有系统化的筛选机制，导致投入在高不确定、强人性依赖或不可证伪的方向上
2. **思考无法落地**：思考很难沉淀为可执行的交付物（需求、拆解、Story、验证清单），从"想法"到"落地"存在断层

### 1.2 项目目标

引入「每日商业思考 + 决策宪法Gate + BMAD落地路由」并融合《Zero to Sold》的方向选择/市场情绪研究实践，将SmartFish从"舆情分析工具"升级为"思考-决策-执行完整闭环系统"。

**核心价值主张：** "不让你高效地把错误方向做完整"

### 1.3 项目分类

| 维度 | 分类 |
|-----|------|
| 项目类型 | Web Application (Flask-based) |
| 领域 | Productivity & Decision Support |
| 项目上下文 | Brownfield Extension |
| 领域复杂度 | Medium |
| 技术栈 | Flask + PostgreSQL + Jinja2 |
| 集成范围 | Deep Agent Integration |

### 1.4 目标用户

**主要用户：**
1. **独立创业者** - 需要快速验证想法，避免浪费时间
2. **产品经理** - 需要结构化决策流程，可追溯
3. **研究员** - 需要严格的验证工具和方法论

**用户规模目标：**
- Phase 1: 10-20个种子用户
- Phase 2: 50-100个用户
- Phase 3: 200-500个用户
- Phase 4: 1000+个用户

---

## 2. 产品愿景

### 2.1 问题陈述

**核心问题：** 想法很多，但90%都是错的，而且很难提前知道哪个是对的。

**问题强度：** 8/10（重要且紧急）
- 重要性：错误决策成本极高，可能导致项目失败
- 紧迫性：创业窗口期有限，每个决策都关键
- 频率：每周都会遇到需要决策的场景

**问题影响：**
- 对创业者：时间和资源浪费，试错成本极高
- 对产品经理：优先级难定，决策不可追溯
- 对研究员：缺少验证工具，证据链不完整

### 2.2 解决方案

**四大支柱：**

#### 支柱1: 决策宪法Gate（强筛选）
- 四层过滤器：人性依赖/价值自证/反馈清洁度/角色消耗
- 否决式设计：任一层不通过即终止
- 审计追踪：所有决策可回溯

#### 支柱2: BMAD工作流路由（自动化）
- 智能路由：Quick/Standard/Enterprise三档
- 工件生成：自动生成tech-spec/PRD/architecture
- 模板可配置：适应不同需求

#### 支柱3: AI证据补强（智能化）
- 多Agent集成：QueryEngine/MindSpider/InsightEngine/ReportEngine
- 市场声音采集：自动抓取tribe/water cooler反馈
- 证据链回填：验证结果自动关联

#### 支柱4: Zero to Sold方法论（系统化）
- Audience → Problem → Solution → Product顺序
- 访谈脚本生成：避免偏差
- 市场转向复核：持续监测信号

### 2.3 差异化优势

1. **唯一能说"不"的系统** - Gate机制提供强约束筛选
2. **完整闭环** - 从想法到工件一站式
3. **AI辅助证据补强** - 自动调用4个Agent验证
4. **内置验证方法论** - Zero to Sold产品化
5. **为SmartFish用户定制** - 复用现有能力

---

## 3. 成功指标

### 3.1 北极星指标

**"每周生成的可执行工件数"**

**目标：**
- Phase 1: 5个工件/周
- Phase 2: 20个工件/周
- Phase 3: 100个工件/周
- Phase 4: 500+个工件/周

### 3.2 关键指标

#### 使用指标
- 每周活跃用户（WAU）
- 每用户每周思考条目数：3-5条
- Gate通过率：60-70%
- 工件生成率：>80%

#### 质量指标
- 用户决策后悔率：<20%（当前基线60%）
- 工件被实际执行率：>60%
- 用户满意度（NPS）：>50

#### 效率指标
- 从想法到工件时间：<20分钟（当前基线3天）
- Gate完成时间：<5分钟
- 证据补强时间：<60分钟（异步）

### 3.3 反向指标

| 反向指标 | 阈值 | 说明 |
|---------|------|------|
| Gate否决率过高 | >50% | 可能过于严格 |
| Gate否决率过低 | <20% | 可能过于宽松 |
| 工件不执行率 | >50% | 质量问题 |
| 用户流失率 | >30%/月 | 学习成本过高 |

---

## 4. 用户画像与旅程

### 4.1 Persona 1: 独立创业者 Alex

**背景：**
- 30岁，技术背景，第一次创业
- 全栈开发者，独立运营2-3个项目
- 每天工作12小时，时间是最稀缺资源

**痛点：**
- 每天3-5个新想法，不知道哪个值得投入
- 经常浪费1-2周才发现方向错误
- 凭直觉决策，后悔率60%

**目标：**
- 快速验证想法，48小时内知道是否值得投入
- 建立可复用决策框架
- 把想法转化为可执行计划

**成功标志：**
- "这个系统帮我避免了至少3个错误方向"
- "决策时间从3天缩短到20分钟"

**使用频率：** 每天10-20分钟

### 4.2 Persona 2: 产品经理 Sarah

**背景：**
- 28岁，3年产品经验，负责B2B SaaS
- 管理2个开发团队，向VP汇报
- 每周收到10+个需求

**痛点：**
- 优先级难定，经常被质疑决策依据
- 决策不可追溯，3个月后无法解释
- 手动写PRD耗时2-3天

**目标：**
- 结构化决策流程，可向团队解释
- 快速生成PRD，节省时间
- 用数据和证据支撑决策

**成功标志：**
- "我的决策现在有完整证据链"
- "PRD生成从3天缩短到1小时"

**使用频率：** 每周2-3次，每次30-60分钟

### 4.3 Persona 3: 研究员 David

**背景：**
- 35岁，博士学历，关注方法论研究
- 既做研究也做实践
- 重视可复现性和证据链

**痛点：**
- 缺少系统化验证工具
- 证据链不完整
- 研究成果难以转化为实践

**目标：**
- 建立严格验证流程
- 所有假设有证据支撑
- 方法论可复现

**成功标志：**
- "这个系统让我的研究更严谨"
- "证据采集效率提升5倍"

**使用频率：** 不定期，每次2-3小时深度使用

### 4.4 核心用户旅程

#### 旅程1: Alex的每日思考（10-20分钟）

**场景：** 周一早上，想到一个新产品idea

1. **发现触发（0分钟）** - 打开SmartFish，点击"新思考"
2. **Gate检查（5分钟）** - 四层过滤，通过但有2个警告
3. **结构化思考（8分钟）** - 填写字段，系统建议Quick路由
4. **工件生成（10分钟）** - 一键生成tech-spec.md
5. **成功时刻（15分钟）** - "这比我自己想3天还清楚！"

#### 旅程2: Sarah的证据补强（30-60分钟）

**场景：** 需要向VP证明功能值得做

1. 打开已有条目
2. 点击"补强证据"
3. 选择QueryEngine + 市场声音采集
4. 30分钟后查看证据摘要
5. 一键回填到PRD
6. **成功时刻：** "这次VP没有质疑我的判断！"

#### 旅程3: David的市场研究（2-3小时）

**场景：** 研究"独立开发者的决策工具需求"

1. 进入Audience/Problem/Solution向导
2. 定义niche audience
3. 生成访谈脚本
4. 系统生成市场声音采集任务
5. 2小时后查看聚类结果
6. 生成market-research.md
7. **成功时刻：** "这个证据链可以直接用在论文里！"

---

## 5. 功能需求

### 5.1 条目管理（Daily Thinking Log）

**FR1: 思考条目CRUD**

**需求描述：** 支持创建/编辑/归档"思考条目"，作为所有决策的起点

**核心字段：**
- Signal（信号）- 触发思考的事件或观察
- Target/Segment（对象/细分用户）- 目标用户群体
- Problem/JTBD（问题/待完成任务）- 要解决的核心问题
- Hypothesis（可证伪假设）- 可验证的假设陈述
- Evidence Needed（证据需求）- 需要什么证据来验证
- MVA（48小时最小行动）- 最小可执行动作
- Success Metric（成功指标）- 如何衡量成功
- Constraints/Dependencies（约束/依赖）- 限制条件
- Routing（路由选择）- Quick/Standard/Enterprise
- Status（状态）- 想法/评估中/已否决/已落地/已归档

**FR1.1: 方向研究扩展字段（Zero to Sold）**
- Audience定义（niche约束）
- Audience规模估算（方法/假设/来源）
- Can they pay / will they pay（支付能力与意愿）
- Water coolers/Tribes（主要聚集地）
- 市场信号（饱和/价格战/收缩/监管/技术变化）
- 问题强度评分（重要性×紧迫性）

**FR2: 检索与筛选**
- 按日期筛选
- 按状态筛选（想法/评估中/已否决/已落地/已归档）
- 按路由类型筛选
- 按主题标签筛选
- 全文搜索

**验收标准：**
- ✅ 用户可以在5分钟内创建一个完整的思考条目
- ✅ 所有必填字段有清晰的提示和示例
- ✅ 条目列表支持分页（每页20条）
- ✅ 检索响应时间<1秒（1000条目）

---

### 5.2 决策宪法Gate（强门槛）

**FR3: Gate校验机制**

**需求描述：** 每条思考条目在进入BMAD路由与后续任务前，必须完成Gate校验并生成不可篡改的审计记录

**FR4: 四层过滤器**

**层1: 人性依赖过滤器**
- 问题：这个想法是否强依赖他人的意愿/行动/情绪/持续动力？
- 高危信号：需要用户持续主动使用、需要他人改变行为、依赖情绪驱动
- 判定：是 → ⚠️ 警告或 🚫 否决

**层2: 价值自证过滤器**
- 问题：是否需要反复向用户解释/教育市场才能理解价值？
- 高危信号：需要长篇解释、用户不理解为什么需要、市场教育成本高
- 判定：是 → 🚫 否决

**层3: 反馈清洁度过滤器**
- 问题：用户反馈是否可量化/可证伪？还是主要依赖情绪反馈？
- 高危信号：只有主观感受、无法量化、不可证伪
- 判定：不可证伪 → 🚫 否决

**层4: 角色消耗过滤器**
- 问题：你的角色是"推进事情发生"还是"为判断负责"？
- 高危信号：需要你持续推动、需要你协调多方、需要你解决冲突
- 判定：需要推进 → ⚠️ 警告或 🚫 否决

**FR5: 否决处理**

**否决规则：**
- 任一层触发否决 → 条目状态自动置为"已否决"
- 必须填写：触发层级 + 一句话原因
- 后续BMAD/调研入口关闭
- 仅允许"复活/重新提交"走完整Gate

**审计记录：**
- 不可篡改的决策历史
- 可追加说明，但保留历史版本
- 记录时间戳、决策结果、原因

**验收标准：**
- ✅ Gate检查在5分钟内完成
- ✅ 任一层否决后，无法生成工件
- ✅ 否决原因必须填写才能保存
- ✅ 审计记录完整可追溯
- ✅ Gate否决率在30-40%之间（证明有效）

---

### 5.3 BMAD路由与工件输出

**FR6: 工作流路由**

**需求描述：** Gate通过后，系统将条目路由到"最小可落地"工作流，并生成对应Markdown工件

**路由类型：**

**Quick（小改动/快速试验）**
- 适用场景：48小时内可完成的小试验
- 生成工件：tech-spec.md
- 内容包含：
  - 目标（从条目自动填充）
  - 范围（In Scope / Out of Scope）
  - 验收标准（Success Metric）
  - 风险与止损（Gate警告 + 约束）
  - 时间表（48小时）
  - 影响面分析

**Standard（产品/大功能）**
- 适用场景：需要团队协作的产品功能
- 生成工件：product-brief.md 和/或 PRD.md
- 内容包含：
  - 问题与用户
  - 差异化价值
  - MVP范围
  - ROI假设
  - 风险与未决问题

**Enterprise（高约束/多依赖/强合规）**
- 适用场景：复杂系统、多团队协作、强合规要求
- 生成工件：Standard基础上增加
  - architecture.md（技术架构）
  - implementation-readiness.md（实施就绪检查）
  - NFR清单（非功能需求）
  - 依赖分析
  - 审计点
  - 验收门槛

**FR6.1: Research工件（方向研究/问题验证）**
- market-research.md
  - Audience/Problem/Solution研究结论
  - 市场声音摘要
  - 问题强度评分
  - 证据链与引用
  - 偏差与反证
- interview-guide.md
  - 访谈脚本
  - 追问路径
  - 禁问清单
  - 偏差检测与终止条件

**FR7: 路由选择方式**

**手动选择：**
- 用户明确选择Quick/Standard/Enterprise
- 系统提供每种路由的适用场景说明

**自动建议：**
- 基于条目字段分析：
  - 影响范围（用户数、系统模块数）
  - 依赖数量（外部系统、团队）
  - 风险等级（Gate警告数、技术复杂度）
  - 证据缺口（Evidence Needed字段）
- 给出默认推荐，用户可覆盖

**FR8: 工件输出规范**

**文件命名：**
- YYYY-MM-DD_<slug>_tech-spec.md
- YYYY-MM-DD_<slug>_product-brief.md
- YYYY-MM-DD_<slug>_prd.md
- YYYY-MM-DD_<slug>_market-research.md
- YYYY-MM-DD_<slug>_interview-guide.md

**保存位置：**
- 默认：docs/thinking/
- 可配置：通过config.yaml设置

**FR9: 导出功能**
- 单条或多条条目导出Markdown
- 导出PDF（复用现有export_pdf能力）
- 批量导出（选中多条）

**验收标准：**
- ✅ Gate通过后，可一键生成至少一种工件
- ✅ 工件生成时间<5秒
- ✅ 工件内容完整，格式正确
- ✅ 文件自动命名并保存到指定目录
- ✅ 工件生成率>80%（通过Gate的条目中）

---

### 5.4 SmartFish Agent集成（证据补强）

**FR10: 调研任务生成**

**需求描述：** 对条目中的Evidence Needed/研究问题，支持一键生成"调研任务"并调用现有Agent

**支持的Agent：**

**QueryEngine：** 全域信息搜索
- 输入：研究问题/关键词
- 输出：公开信息/新闻/论坛搜索结果
- 时间范围：可配置
- 来源白名单：可配置

**MindSpider：** 社媒爬取
- 输入：平台+关键词+时间窗
- 输出：社媒内容+情感分析
- 支持平台：微博、小红书等（如项目已支持）

**InsightEngine：** 私有数据库挖掘
- 输入：查询条件
- 输出：历史数据分析
- 数据源：已配置的数据库

**ReportEngine：** 证据摘要报告
- 输入：调研结果
- 输出：证据摘要报告
- 包含：来源列表、时间范围、置信度说明

**FR10.1: 市场声音（Word-of-mouth）任务**

**需求描述：** 基于Tribe/Water cooler列表生成默认搜索/抓取计划

**输入：**
- Tribe/Water cooler列表（论坛/群组/平台/博客）
- 关键词组
- 时间窗（默认最近3个月）
- 去重规则

**输出：**
- 主要抱怨/摩擦点（Top themes）
- 典型原话片段（短引用，带来源链接/时间）
- 语气倾向（正/中/负）与强度线索（频次、措辞、紧迫性）
- 关联的替代方案/竞品被提及情况

**FR11: 证据回填**

**需求描述：** 调研结果需可回填到条目，并与工件联动

**回填流程：**
1. 调研任务完成后，生成证据摘要
2. 用户点击"回填到条目"
3. 证据摘要自动添加到Evidence Needed字段
4. 如果已生成PRD，自动更新"证据与洞察"章节
5. 更新假设置信度（用户可调整）

**验收标准：**
- ✅ Evidence Needed可触发至少一个引擎（QueryEngine）
- ✅ 调研任务在60分钟内完成（异步）
- ✅ 证据摘要可一键回填到条目
- ✅ PRD的"证据与洞察"章节自动更新
- ✅ Agent调用成功率>90%

---

### 5.5 周度评审与复盘

**FR12: 周度评审页面**

**需求描述：** 提供"周度评审"页面，帮助用户从最近思考中选择Top N进入执行

**功能：**

**自动聚合：**
- 最近7天的所有条目
- 按状态分组显示
- 统计Gate通过/否决数

**打分维度：**
- 影响力（1-10分）：对目标的影响程度
- 可行性（1-10分）：实现的难易程度
- 证据充分度（1-10分）：证据是否充分
- 执行成本（1-10分）：时间和资源成本

**选择Top N：**
- 根据综合得分排序
- 用户选择Top 1-3进入"本周落地计划"
- 支持手动调整顺序

**生成weekly-plan.md：**
- 选题列表
- 目标与验收标准
- Stories拆解（如适用）
- 风险与止损计划

**验收标准：**
- ✅ 周度评审页面可自动聚合最近7天条目
- ✅ 打分界面友好，5分钟内完成
- ✅ 可生成weekly-plan.md
- ✅ 周度评审使用率>30%

---

### 5.6 Zero to Sold方法论向导

**FR13: Audience/Problem/Solution/Product向导**

**需求描述：** 引导用户先定义niche audience，再定义critical problem，再讨论solution，最后才进入product/实现工件

**Audience步骤：**
- 定义niche（越具体越好）
- 提供"太大/太小"的提示
- 要求记录"规模估算方法"
- 要求记录"专家/从业者访谈线索"

**Problem步骤：**
- 定义critical problem
- 评估问题强度（重要性×紧迫性）
- 识别现有解决方案的不足

**Solution步骤：**
- 讨论解决方案
- 评估差异化
- 识别关键假设

**Product步骤：**
- 进入实现工件生成
- 基于前面步骤的输入

**FR14: 问题强度评分**

**需求描述：** 用Eisenhower（重要/紧急）框架为问题强度打分

**评分维度：**
- 重要性（1-5分）：问题的影响程度
- 紧迫性（1-5分）：问题的时间敏感度
- 综合得分：重要性 × 紧迫性（1-25分）

**优先级标记：**
- 重要且紧急（20-25分）：优先处理
- 重要不紧急（15-19分）：计划处理
- 紧急不重要（10-14分）：委托或快速处理
- 不重要不紧急（<10分）：考虑放弃

**输出：**
- 分数与理由写入条目
- 进入market-research.md
- 进入product-brief.md

**FR15: 访谈脚本生成与偏差控制**

**需求描述：** 自动生成以"进展受阻/价值创造中的张力与摩擦"为核心的访谈提纲

**访谈脚本内容：**
- 开场白（建立信任）
- 核心问题（hindered progress / tension & friction）
- 追问路径（基于回答深入）
- 结束语（感谢与后续）

**禁问清单：**
- ❌ 避免过早问feature
- ❌ 避免陷入日常小烦恼清单
- ❌ 避免过度讨论现有策略战术（路径依赖）

**偏差检测：**
- 识别极端抱怨者（outlier detection）
- 识别高噪音对话（信噪比分析）
- 支持标注"疑似偏差原因"

**终止条件：**
- 建议延后几天复盘录音/记录
- 避免基于单一样本下结论
- 强调寻找extremes与overlaps

**FR16: 市场转向复核**

**需求描述：** 按月/季度回顾目标市场是否出现转向信号

**复核内容：**
- 市场饱和/价格战/同质竞争加剧
- 市场收缩（买方/代理减少、预算收紧）
- 监管变化带来的合规成本
- 技术/结构变化带来的新流程与新问题

**可选指标：**
- CAC（客户获取成本）趋势
- LTV（客户生命周期价值）趋势
- 或替代指标

**输出：**
- market-review.md
- 标记"继续/收缩/转向/终止"
- 回填到条目
- 保留历史版本

**验收标准：**
- ✅ Audience/Problem/Solution向导可用
- ✅ 问题强度评分可生成并回填
- ✅ 访谈脚本可自动生成
- ✅ 市场复核可生成market-review.md
- ✅ 市场研究使用率>20%

---

## 6. 非功能需求（NFR）

### 6.1 可追溯性（NFR1）

**需求：** 任一条目从Gate → 路由 → 调研 → 工件生成必须有完整时间线

**实现：**
- 每个操作记录时间戳
- 状态变更记录历史
- 审计日志不可篡改
- 支持时间线可视化

**验收标准：**
- ✅ 可查看任一条目的完整操作历史
- ✅ 时间线精确到秒
- ✅ 历史记录不可删除

### 6.2 可复用性（NFR2）

**需求：** 工件模板可配置，可被二次编辑并保留版本

**实现：**
- 工件模板放入docs/templates/
- 支持Jinja2变量替换
- 工件生成后可手动编辑
- 保留版本历史（Git）

**验收标准：**
- ✅ 模板可配置和自定义
- ✅ 工件可二次编辑
- ✅ 版本历史可追溯

### 6.3 稳定性（NFR3）

**需求：** 调研任务失败需可重试，失败原因可见

**实现：**
- 任务队列系统
- 失败自动重试（最多3次）
- 失败原因记录到日志
- 用户可手动重试

**验收标准：**
- ✅ Agent调用失败率<10%
- ✅ 失败原因清晰可见
- ✅ 可手动重试

### 6.4 性能（NFR4）

**需求：** 条目列表/周度评审页面在1k条目量级下仍可流畅

**性能指标：**
- 条目列表加载：<1秒
- Gate检查：<2秒
- 工件生成：<5秒
- 周度评审加载：<2秒

**实现：**
- 数据库索引优化
- 分页加载（每页20条）
- 缓存机制
- 异步任务队列

**验收标准：**
- ✅ 1000条目下，列表加载<1秒
- ✅ Gate检查<2秒
- ✅ 工件生成<5秒

### 6.5 可测试性（NFR5）

**需求：** 核心逻辑需有单元测试与集成测试

**测试覆盖：**
- Gate判定逻辑：单元测试
- 路由建议算法：单元测试
- 工件渲染：单元测试
- Agent集成：集成测试
- 端到端流程：E2E测试

**验收标准：**
- ✅ 单元测试覆盖率>80%
- ✅ 集成测试覆盖核心流程
- ✅ E2E测试覆盖主要用户旅程

### 6.6 可解释性（NFR6）

**需求：** 自动路由/强度评分/偏差提示必须给出规则说明与依据字段

**实现：**
- 路由建议显示依据（影响范围、依赖数、风险等级）
- 强度评分显示计算公式
- 偏差提示显示检测规则
- 避免"黑箱推荐"

**验收标准：**
- ✅ 所有自动建议都有解释
- ✅ 用户可理解决策依据
- ✅ 可追溯到具体字段

---

## 7. 数据模型

### 7.1 thinking_entries（思考条目表）

```sql
CREATE TABLE thinking_entries (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    title VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(50) NOT NULL, -- 想法/评估中/已否决/已落地/已归档
    tags TEXT[], -- 主题标签数组
    routing_type VARCHAR(50), -- Quick/Standard/Enterprise/Research
    
    -- 核心字段
    signal TEXT,
    target_segment TEXT,
    problem TEXT,
    hypothesis TEXT,
    evidence_needed TEXT,
    mva TEXT, -- 最小可行动作
    success_metric TEXT,
    constraints TEXT,
    dependencies TEXT,
    
    -- Zero to Sold扩展字段
    audience_definition TEXT,
    audience_size_estimate TEXT,
    payability_notes TEXT,
    tribes_watercoolers TEXT,
    market_signals TEXT,
    problem_intensity_score INTEGER, -- 1-25
    
    INDEX idx_user_status (user_id, status),
    INDEX idx_created_at (created_at),
    INDEX idx_routing_type (routing_type)
);
```

### 7.2 gate_reviews（Gate审查表）

```sql
CREATE TABLE gate_reviews (
    id SERIAL PRIMARY KEY,
    entry_id INTEGER NOT NULL REFERENCES thinking_entries(id),
    reviewed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- 四层过滤结果
    human_dependency_pass BOOLEAN,
    value_self_evident_pass BOOLEAN,
    feedback_clean_pass BOOLEAN,
    role_cost_pass BOOLEAN,
    
    -- 决策结果
    decision VARCHAR(20) NOT NULL, -- pass/fail
    fail_level VARCHAR(50), -- 触发否决的层级
    fail_reason TEXT, -- 否决原因
    notes TEXT, -- 补充说明
    version INTEGER DEFAULT 1, -- 版本号（支持复活重审）
    
    INDEX idx_entry_id (entry_id),
    INDEX idx_decision (decision)
);
```

### 7.3 artifacts（工件表）

```sql
CREATE TABLE artifacts (
    id SERIAL PRIMARY KEY,
    entry_id INTEGER NOT NULL REFERENCES thinking_entries(id),
    type VARCHAR(50) NOT NULL, -- tech-spec/product-brief/prd/market-research/interview-guide
    path TEXT NOT NULL, -- 文件路径
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    checksum VARCHAR(64), -- 文件校验和
    
    INDEX idx_entry_id (entry_id),
    INDEX idx_type (type)
);
```

### 7.4 research_tasks（调研任务表）

```sql
CREATE TABLE research_tasks (
    id SERIAL PRIMARY KEY,
    entry_id INTEGER NOT NULL REFERENCES thinking_entries(id),
    engine VARCHAR(50) NOT NULL, -- Query/MindSpider/Insight/Report
    task_type VARCHAR(50), -- evidence_research/word_of_mouth/market_turn_review
    query TEXT NOT NULL,
    status VARCHAR(20) NOT NULL, -- pending/running/completed/failed
    result_path TEXT, -- 结果文件路径
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP,
    error_message TEXT, -- 失败原因
    
    INDEX idx_entry_id (entry_id),
    INDEX idx_status (status),
    INDEX idx_engine (engine)
);
```

---

## 8. 技术架构

### 8.1 系统架构

```
┌─────────────────────────────────────────────────────────┐
│                    SmartFish Web UI                      │
│  (Flask Templates + HTML/CSS/JS)                         │
└─────────────────────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────┐
│              Flask Application Layer                     │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │   /thinking  │  │   /api/gate  │  │  /api/tasks  │  │
│  │   Blueprint  │  │   Blueprint  │  │   Blueprint  │  │
│  └──────────────┘  └──────────────┘  └──────────────┘  │
└─────────────────────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────┐
│                  Service Layer                           │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │ Gate Service │  │Route Service │  │ Task Service │  │
│  └──────────────┘  └──────────────┘  └──────────────┘  │
└─────────────────────────────────────────────────────────┘
                           │
        ┌──────────────────┼──────────────────┐
        ▼                  ▼                  ▼
┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│  PostgreSQL  │  │ Task Queue   │  │ File System  │
│  Database    │  │ (Redis)      │  │ (docs/)      │
└──────────────┘  └──────────────┘  └──────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────┐
│              Existing SmartFish Agents                   │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │QueryEngine   │  │ MindSpider   │  │InsightEngine │  │
│  └──────────────┘  └──────────────┘  └──────────────┘  │
│  ┌──────────────┐                                       │
│  │ReportEngine  │                                       │
│  └──────────────┘                                       │
└─────────────────────────────────────────────────────────┘
```

### 8.2 技术栈

**后端：**
- Flask 2.3.3（复用现有）
- SQLAlchemy 2.0.35（ORM）
- PostgreSQL/MySQL（复用现有）
- Redis（任务队列，Phase 3新增）
- Jinja2（模板引擎）

**前端：**
- HTML/CSS/JS（复用现有模板体系）
- 复用static/目录资源
- 渐进增强，无需重构

**工件生成：**
- Jinja2模板
- Markdown格式
- 可选PDF导出（复用export_pdf）

**Agent集成：**
- 复用现有Agent接口
- 异步任务队列（Phase 3）
- 统一错误处理

### 8.3 目录结构

```
SmartFish/
├── thinking/                    # 新增模块
│   ├── __init__.py
│   ├── routes.py               # Flask Blueprint
│   ├── services/
│   │   ├── gate_service.py     # Gate逻辑
│   │   ├── routing_service.py  # 路由逻辑
│   │   ├── artifact_service.py # 工件生成
│   │   └── task_service.py     # 任务调度
│   ├── models/
│   │   ├── thinking_entry.py
│   │   ├── gate_review.py
│   │   ├── artifact.py
│   │   └── research_task.py
│   └── templates/              # 页面模板
│       ├── list.html
│       ├── detail.html
│       ├── gate.html
│       └── weekly_review.html
├── docs/
│   ├── thinking/               # 工件输出目录
│   └── templates/              # 工件模板
│       ├── tech-spec.md.j2
│       ├── product-brief.md.j2
│       ├── prd.md.j2
│       └── market-research.md.j2
├── templates/                  # 现有模板目录
├── static/                     # 现有静态资源
├── config.py                   # 配置文件（扩展）
└── app.py                      # 主应用（注册新Blueprint）
```

---

## 9. 实施计划

### 9.1 Phase 1: MVP核心（4-6周）

**目标：** 验证Gate机制的核心价值

**功能范围：**
- ✅ 思考条目CRUD（FR1）
- ✅ Gate四层过滤（FR3-FR5）
- ✅ Quick路由 + tech-spec生成（FR6部分）
- ✅ 基础UI（列表/详情/Gate表单）

**技术任务：**
- 数据库表设计与迁移
- Flask Blueprint创建
- Gate Service实现
- 工件模板系统
- 基础UI页面

**验收标准：**
- 5个种子用户每周使用
- Gate否决率30-40%
- 用户反馈Gate"有价值"

**时间表：**
- Week 1-2: 数据库 + 后端核心
- Week 3-4: Gate逻辑 + 工件生成
- Week 5-6: UI + 测试 + Beta发布

---

### 9.2 Phase 2: 工作流完善（4-6周）

**目标：** 扩展路由能力，支持更复杂场景

**功能范围：**
- ✅ Standard/Enterprise路由（FR6完整）
- ✅ 工件模板系统（FR8）
- ✅ 周度评审（FR12）
- ✅ 导出功能（FR9）

**技术任务：**
- 路由算法实现
- 模板系统扩展
- 周度评审页面
- PDF导出集成

**验收标准：**
- WAU >30
- 工件生成率>70%
- NPS >40

**时间表：**
- Week 1-2: 路由系统
- Week 3-4: 模板扩展 + 周度评审
- Week 5-6: 测试 + Public Beta

---

### 9.3 Phase 3: Agent集成（3-4周）

**目标：** 证据补强，AI辅助验证

**功能范围：**
- ✅ QueryEngine集成（FR10）
- ✅ 证据回填（FR11）
- ✅ 任务调度系统

**技术任务：**
- Redis任务队列
- Agent接口适配
- 异步任务处理
- 证据回填逻辑

**验收标准：**
- Agent调用成功率>90%
- WAU >100
- 月留存率>70%

**时间表：**
- Week 1: 任务队列系统
- Week 2: Agent集成
- Week 3-4: 测试 + Official Launch

---

### 9.4 Phase 4: 高级功能（4-6周）

**目标：** Zero to Sold方法论完整实现

**功能范围：**
- ✅ Zero to Sold向导（FR13-FR16）
- ✅ 市场声音采集（FR10.1）
- ✅ 市场转向复核
- ✅ 高级分析面板

**技术任务：**
- 向导流程实现
- 市场声音聚类算法
- 分析面板开发

**验收标准：**
- WAU >500
- 用户规模1000+
- 市场研究使用率>20%

**时间表：**
- Week 1-2: Zero to Sold向导
- Week 3-4: 市场声音采集
- Week 5-6: 分析面板 + Growth

---

## 10. 风险与缓解

### 10.1 高风险

**R1: Gate机制过严导致用户放弃**
- 概率：中 | 影响：高
- 缓解：
  - 提供"学习模式"（仅警告不阻止）
  - 详细的否决说明和示例
  - 可配置严格度参数
  - 复活机制

**R2: Agent集成不稳定**
- 概率：中 | 影响：高
- 缓解：
  - 完善错误处理和重试机制
  - 降级方案（手动补充）
  - 独立任务队列
  - 完整的日志和监控

### 10.2 中风险

**R3: 学习成本过高**
- 概率：中 | 影响：中
- 缓解：
  - 渐进式引导和教程
  - 交互式示例
  - 默认值和建议
  - 视频演示

**R4: 路由准确性不足**
- 概率：高 | 影响：中
- 缓解：
  - 可解释规则
  - 人工覆盖选项
  - 持续优化算法
  - 用户反馈收集

### 10.3 低风险

**R5: 存储成本上升**
- 概率：低 | 影响：中
- 缓解：
  - 归档策略
  - 数据清理机制
  - 压缩存储

---

## 11. 验收标准总览

### 11.1 Phase 1验收

- ✅ AC1: 未完成Gate时无法生成工件
- ✅ AC2: Gate否决后状态变为"已否决"，强制填写原因
- ✅ AC3: Gate通过后可一键生成tech-spec
- ✅ 至少5个用户每周使用
- ✅ Gate否决率30-40%

### 11.2 Phase 2验收

- ✅ 三种路由可正确选择和生成工件
- ✅ 工件模板可配置
- ✅ 周度评审可生成weekly-plan
- ✅ WAU >30

### 11.3 Phase 3验收

- ✅ AC4: QueryEngine可执行并回填结果
- ✅ Agent调用成功率>90%
- ✅ WAU >100
- ✅ 月留存率>70%

### 11.4 Phase 4验收

- ✅ AC5: 市场声音任务可生成并输出
- ✅ AC6: 周度评审可生成weekly-plan
- ✅ AC7: 市场复核可生成market-review.md
- ✅ WAU >500
- ✅ 用户规模1000+

### 11.5 系统级验收

- ✅ AC8: 无外部服务情况下可通过测试
- ✅ 单元测试覆盖率>80%
- ✅ 集成测试覆盖核心流程
- ✅ 性能指标达标（NFR4）
- ✅ 安全审计通过

---

## 12. 附录

### 12.1 术语表

| 术语 | 定义 |
|-----|------|
| Gate | 决策宪法门槛机制，四层过滤 |
| MVA | Minimum Viable Action，最小可行动作 |
| BMAD | Business Method & Agile Development |
| Artifact | 工件（tech-spec/PRD等） |
| Brownfield | 棕地项目，扩展现有系统 |
| Tribe/Water cooler | 用户聚集地（论坛/群组/平台） |

### 12.2 参考文档

- SmartFish V1现有架构文档
- BMAD Method工作流规范
- Zero to Sold书籍
- Product Brief (product-brief-SmartFish-2026-01-22.md)
- 原始需求文档 (requests.md)
- 技术分析报告 (thinking-system-analysis.md)

### 12.3 变更历史

| 版本 | 日期 | 变更内容 | 作者 |
|-----|------|---------|------|
| 1.0 | 2026-01-22 | 初始版本，Fast Mode生成 | Jody |

---

**文档状态：** ✅ PRD Complete (Fast Mode)
**下一步：** UX Design 或 Architecture
