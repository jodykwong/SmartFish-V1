# 需求文档（需求.md）——SmartFish-V1：引入「每日商业思考 + 决策宪法 Gate + BMAD 落地路由」并融合《Zero to Sold》的“方向选择/市场情绪（市场声音）研究”实践

## 1. 背景与问题
SmartFish-V1 当前定位为多智能体舆情分析系统，用户以“像聊天一样提出分析需求”的方式触发 Insight / Media / Query / Report 等 Agent 产出分析报告。

但在实际使用中，用户的“商业思考/策略想法”往往存在两个断点：
1) 想法进入分析或开发前缺少强约束筛选，导致投入在高不确定、强人性依赖或不可证伪的方向上；
2) 思考很难沉淀为可执行的交付物（需求、拆解、Story、验证清单），从“想法”到“落地”断层。

此外，《Zero to Sold》强调创业方向选择与问题验证应遵循 **Audience → Problem → Solution → Product** 的顺序，并通过访谈、社区（tribe / water coolers）与口碑讨论来捕捉“市场声音”，并在后续持续复核市场是否“转坏/转好”。因此 SmartFish-V1 需要把“市场方向判断/市场声音采集/问题验证方法论”产品化，以便与每日思考、Gate、BMAD 工件无缝衔接。

为此，需要在 SmartFish-V1 中加入：
- 「个人决策宪法」作为强门槛（Gate），在进入分析/规划前进行否决式筛选；
- 「每日商业思考」结构化记录与复盘机制；
- 与 BMAD-METHOD 的四阶段/多轨道工作流路由对接，把通过 Gate 的想法转化为可落地工件（Artifacts），并可进一步触发 SmartFish 的舆情/数据 Agent 做证据补强；
- 融合《Zero to Sold》的“方向选择/市场声音/问题强度与验证/持续复核”能力，作为 Research 轨道的标准化产出。

## 2. 目标（Goals）
G1. 将“每日商业思考”标准化为可复用输入，保证每天产出最小可执行工件（MVA/验收标准/证据需求）。
G2. 将「个人决策宪法」嵌入为前置 Gate：未通过则终止，避免系统高效地“把错误方向做完整”。
G3. 引入 BMAD 路由：通过 Gate 的条目自动选择 Quick / Standard / Enterprise（或对应等价）流程深度，产出对应文档模板（tech spec / product brief / PRD / story）。
G4. 与 SmartFish 现有多 Agent 架构集成：把“证据需求/研究问题”转为 QueryEngine / MindSpider 等可执行任务，自动补齐事实与舆情证据链。
G5. 支持长期沉淀：所有条目、Gate 结果、路由选择、产出文档可检索、可导出（Markdown/PDF），可追溯。
G6. 将《Zero to Sold》的方向分析方法产品化：提供 Audience/Problem/Solution 的研究向导、问题强度评分、访谈脚本与偏差控制、以及 tribe/口碑（市场声音）监测面板。
G7. 支持“市场转向复核”：按月/季度回顾目标市场是否出现饱和、价格战、市场收缩、监管加强、或技术/结构变化带来新机会等信号，并把结果回填到条目与工件。

## 3. 非目标（Non-Goals）
NG1. 不在本期实现 BMAD-METHOD 的完整安装/运行环境（例如外部 CLI/IDE 插件）。本需求聚焦“在 SmartFish 内部实现可用的工作流路由与工件输出”。
NG2. 不实现“全自动决策/全自动商业判断”。系统只做结构化引导、证据补强与工件化输出，最终裁决仍由用户负责。
NG3. 不扩展 SmartFish 的爬虫覆盖面、平台适配或情感模型本体能力（除非为集成所必需）。
NG4. 不以“问卷/大规模调查（survey）”作为核心验证手段（本期以定性研究、社区声音与可证伪实验为主）。

## 4. 用户与使用场景
### 4.1 目标用户
- 个人创业者 / 产品负责人 / 研究员：需要每日沉淀商业判断，并快速把想法落地为计划与执行任务。
- SmartFish 现有用户：已经用舆情分析做“观察”，希望升级为“策略规划与落地”。

### 4.2 核心场景（User Journeys）
S1. 每日思考（10–20 分钟）
1) 新建“今日思考条目”
2) 先跑「决策宪法 Gate」
3) Gate 通过 → 填写结构化思考字段 → 选择/自动路由 BMAD 流程 → 生成工件
4) Gate 未通过 → 记录否决层级与原因 → 结束

S2. 证据补强（30–60 分钟）
1) 对条目中的“证据需求/研究问题”发起 SmartFish 调研任务（QueryEngine / MindSpider / InsightEngine）
2) 回填证据摘要与引用来源
3) 更新假设与验收标准

S3. 周度评审（60 分钟）
1) 从最近 7 天条目中选 Top 1–3
2) 进入“落地计划”视图：生成 stories / checklist
3) 标记本周执行状态与复盘结论

S4. 方向选择与市场声音研究（30–90 分钟）
1) 进入“Audience/Problem/Solution 向导”
2) 选择目标 niche（越具体越好）并完成受众规模/支付能力/可触达性检查
3) 生成“访谈脚本 + 社区/论坛/社媒搜索任务”
4) 汇总“市场声音（口碑/抱怨/摩擦）+ 问题强度评分 + 证据链”
5) 产出 `market-research.md` 并回填到 product-brief/PRD 的“洞察与证据”章节

S5. 市场转向复核（每月/每季度，30 分钟）
1) 复核目标市场是否出现饱和/价格战/收缩/监管/技术替代等信号
2) 复核 CAC/LTV 或替代指标的趋势（若可获取）
3) 输出 `market-review.md` 并标记“继续/收缩/转向/终止”

## 5. 功能需求（Functional Requirements）
### 5.1 条目管理（Daily Thinking Log）
FR1. 支持创建/编辑/归档“思考条目”，字段包含：
- Signal（信号）
- Target / Segment（对象/细分用户）
- Problem / JTBD
- Hypothesis（可证伪）
- Evidence Needed（证据需求）
- MVA（48 小时内最小行动）
- Success Metric（指标/验收）
- Constraints / Dependencies（约束/依赖）
- Routing（路由选择）
- Status（想法/评估中/已否决/已落地/已归档）

FR1.1（新增）支持“方向研究扩展字段”（用于《Zero to Sold》向导与研究工件）：
- Audience 定义（niche 约束）
- Audience 规模估算（方法/假设/来源）
- Can they pay / will they pay（支付能力与付费意愿线索）
- Water coolers / Tribes（主要聚集地：论坛/群组/平台/博客）
- 市场信号（饱和/价格战/收缩/监管/技术变化）
- 问题强度评分（重要性×紧迫性/Eisenhower）

FR2. 支持按日期、状态、路由、主题标签检索与筛选。

### 5.2 决策宪法 Gate（强门槛）
FR3. 每条思考条目在进入 BMAD 路由与后续任务前，必须完成 Gate 校验并生成不可篡改的审计记录（可追加说明，但保留历史）。
FR4. Gate 采用四层过滤：
- 人性依赖过滤器（强依赖他人意愿/行动/情绪/持续动力即高危）
- 价值自证过滤器（若必须反复解释/教育市场则红灯）
- 反馈清洁度过滤器（不可证伪/主要依赖情绪反馈则红灯）
- 角色消耗过滤器（需要你“推进事情发生”而非仅为判断负责则红灯）
FR5. 任一层触发否决 → 条目状态自动置为“已否决”，并要求填写：触发层级 + 一句话原因；后续 BMAD/调研入口关闭（仅允许“复活/重新提交”走完整 Gate）。

### 5.3 BMAD 路由与工件输出（Artifacts）
FR6. Gate 通过后，系统必须将条目路由到一个“最小可落地”工作流，并生成对应 Markdown 工件：
- Quick（小改动/快速试验）：生成 `tech-spec.md`（目标、范围、验收、回滚/止损、影响面）
- Standard（产品/大功能）：生成 `product-brief.md` 与/或 `PRD.md`（问题、用户、差异化、MVP、ROI 假设、风险、未决）
- Enterprise（高约束/多依赖/强合规）：在 Standard 基础上增加 `architecture.md`、`implementation-readiness.md` 等门禁清单（NFR、依赖、审计点、验收门槛）

FR6.1（新增）Research 工件：当条目处于“方向研究/问题验证”阶段时，生成：
- `market-research.md`（Audience/Problem/Solution 研究结论、市场声音摘要、问题强度评分、证据链与引用、偏差与反证）
- `interview-guide.md`（访谈脚本、追问路径、禁问清单、偏差检测与终止条件）

FR7. 路由选择支持两种方式：
- 手动选择：Quick/Standard/Enterprise
- 自动建议：基于条目字段（影响范围、依赖数量、风险等级、证据缺口）给出默认推荐，用户可覆盖。

FR8. 所有工件输出需落地到仓库可配置目录（默认 `docs/thinking/`），文件命名建议：
- `YYYY-MM-DD_<slug>_tech-spec.md`
- `YYYY-MM-DD_<slug>_product-brief.md`
- `YYYY-MM-DD_<slug>_prd.md`
- `YYYY-MM-DD_<slug>_market-research.md`
- `YYYY-MM-DD_<slug>_interview-guide.md`

FR9. 支持一键导出单条或多条条目的 Markdown/PDF（复用现有 export_pdf 能力，如存在）。

### 5.4 与 SmartFish Agent 集成（证据补强）
FR10. 对条目中的 Evidence Needed / 研究问题，支持一键生成“调研任务”并调用：
- QueryEngine：全域信息搜索（公开信息/新闻/论坛等）
- MindSpider：社媒爬取（如项目已支持）
- InsightEngine：私有数据库挖掘（如已配置）
- ReportEngine：生成“证据摘要报告”（附来源列表、时间范围、置信度说明）

FR10.1（新增）市场声音（Word-of-mouth）任务类型：支持基于“Tribe / Water cooler 列表”生成默认搜索/抓取计划（关键词组、平台、时间窗、去重规则），输出：
- 主要抱怨/摩擦点（Top themes）
- 典型原话片段（短引用，带来源链接/时间）
- 语气倾向（正/中/负）与强度线索（频次、措辞、紧迫性）
- 关联的替代方案/竞品被提及情况

FR11. 调研结果需可回填到条目，并与工件联动（例如 PRD 的“证据与洞察”章节自动更新）。

### 5.5 周度评审与复盘
FR12. 提供“周度评审”页面：
- 自动聚合最近 7 天条目
- 支持打分（影响力/可行性/证据充分度/执行成本）
- 选 Top N 进入“本周落地计划”
- 输出 `weekly-plan.md`（选题、目标、stories、验收、风险与止损）

### 5.6 《Zero to Sold》方法论向导（方向选择/问题验证/持续复核）
FR13. Audience/Problem/Solution/Product 向导
- 引导用户先定义 niche audience，再定义 critical problem，再讨论 solution，最后才进入 product/实现工件。
- 在 audience 步骤提供“太大/太小”的提示与约束建议（例如增加条件细分），并要求记录“规模估算方法”和“专家/从业者访谈线索”。

FR14. 问题强度评分（重要性×紧迫性）
- 用 Eisenhower（重要/紧急）框架为问题强度打分，并把“重要且紧急”标记为优先（可持续发生、无法延后/外包的痛）；
- 分数与理由写入条目并进入 `market-research.md` 与 `product-brief.md`。

FR15. 访谈脚本生成与偏差控制
- 自动生成“问进展受阻（hindered progress）/价值创造中的张力与摩擦（tension & friction）”为核心的访谈提纲；
- 明确“禁问清单”：避免过早问 feature、避免陷入日常小烦恼清单、避免过度讨论现有策略战术（路径依赖）；
- 提供“偏差检测”与“终止条件”：识别极端抱怨者/高噪音对话；支持标注“疑似偏差原因”，并建议延后几天复盘录音/记录后再下结论。

FR16. 市场转向复核（每月/季度）
- 提供 `market-review.md` 模板与定时提醒入口（可选），包含：
  - 市场饱和/价格战/同质竞争加剧
  - 市场收缩（买方/代理减少、预算收紧）
  - 监管变化带来的合规成本
  - 技术/结构变化带来的新流程与新问题
- 若用户提供可用指标（CAC/LTV 或替代指标），支持趋势记录与阈值预警。

## 6. 数据模型（建议）
- thinking_entries
  - id, title, created_at, updated_at, status, tags, routing_type, ...
  - signal, target_segment, problem, hypothesis, evidence_needed, mva, success_metric, constraints
  - audience_definition, audience_size_estimate, payability_notes, tribes_watercoolers, market_signals, problem_intensity_score
- gate_reviews
  - id, entry_id, reviewed_at
  - human_dependency_pass (bool), value_self_evident_pass (bool), feedback_clean_pass (bool), role_cost_pass (bool)
  - decision (pass/fail), fail_level, fail_reason, notes, version
- artifacts
  - id, entry_id, type (tech-spec/product-brief/prd/market-research/interview-guide/...), path, created_at, checksum
- research_tasks
  - id, entry_id, engine (Query/MindSpider/Insight/Report), query, status, result_path, created_at, completed_at
  - task_type (evidence_research / word_of_mouth / market_turn_review)

## 7. UI/UX 需求（最小可用）
UX1. 在现有主页/输入框附近新增入口：“每日商业思考”。
UX2. 条目编辑页分为四段：
- Gate（必须先完成，未通过则锁后续）
- Thinking（结构化字段）
- Direction Research（Audience/Problem/Solution 向导，可选但推荐）
- Routing & Artifacts（生成与导出）
UX3. Gate 交互采用“逐层提问 + 否决即止”的单页表单，减少用户负担。
UX4. 周度评审页支持表格筛选、排序与一键生成 weekly-plan。
UX5（新增）市场声音面板：按 tribe/water cooler 分组展示“主题聚类 + 典型引用 + 频次/强度”，并提供“转为 Evidence Needed / PRD 洞察”的一键回填。

## 8. 权限与安全
SEC1. 若 SmartFish 已有用户体系：条目、Gate 记录、工件默认私有，仅本人可见；可选共享给团队（后续版本）。
SEC2. 工件写入磁盘目录需做路径白名单与文件名清理，避免路径穿越。
SEC3. LLM/数据库密钥沿用现有 `.env` 机制，不在前端暴露。

## 9. 非功能需求（NFR）
NFR1. 可追溯：任一条目从 Gate → 路由 → 调研 → 工件生成必须有完整时间线。
NFR2. 可复用：工件模板可配置，可被二次编辑并保留版本。
NFR3. 稳定性：调研任务失败需可重试，失败原因可见。
NFR4. 性能：条目列表/周度评审页面在 1k 条目量级下仍可流畅（分页/索引）。
NFR5. 可测试：核心逻辑（Gate 判定、路由建议、工件渲染、市场声音聚类摘要）需有单元测试与集成测试。
NFR6（新增）可解释：自动路由/强度评分/偏差提示必须给出规则说明与依据字段，避免“黑箱推荐”。

## 10. 验收标准（Acceptance Criteria）
AC1. 新建条目后，未完成 Gate 时无法生成任何 BMAD 工件或发起调研任务。
AC2. Gate 任一层否决后，条目状态变为“已否决”，并强制填写层级与原因；后续入口禁用。
AC3. Gate 通过后，可一键生成至少一种工件（tech-spec / product-brief / PRD / market-research / interview-guide），并落盘到指定目录。
AC4. Evidence Needed 可触发至少一个引擎（QueryEngine）执行，并将结果摘要回填到条目。
AC5. 市场声音任务可从 tribe/water cooler 列表自动生成搜索计划，并输出“主题 + 引用 + 强度线索”，可回填到 market-research/PRD。
AC6. 周度评审可从最近 7 天条目生成 `weekly-plan.md`。
AC7. 市场转向复核可生成 `market-review.md` 并回填到条目，同时保留历史版本。
AC8. 以上流程在无外部服务（仅本地 LLM mock/关闭爬虫）情况下可通过测试跑通。

## 11. 实施建议（Technical Notes）
- 后端：在 Flask 中新增 blueprint（例如 `/thinking`），复用现有模板体系 `templates/` 与静态资源 `static/`。
- 数据库：复用既有 DB 配置（PostgreSQL/MySQL），新增迁移脚本或 init helper。
- 工件模板：放入 `docs/templates/`，渲染时用 Jinja2 或简单字符串模板。
- 研究任务：将 Evidence Needed 映射为 QueryEngine 的查询请求；市场声音任务将 tribe/water cooler 映射为（平台×关键词×时间窗）的批量查询；结果落 `reports/` 并关联条目。
- 摘要与聚类：初期可用“基于 embedding 的相似度聚合 + LLM 主题命名”实现（可配置阈值，结果可编辑）。

## 12. 风险与对策
R1. Gate 过严导致“可用但不常用”
- 对策：保留“重新提交”机制；提供示例与默认答案；但不降低否决原则。
R2. 路由建议不准确
- 对策：先做可解释规则（依赖数、影响范围、风险字段、证据缺口），后续再引入模型评分。
R3. 调研任务噪音大
- 对策：引入时间范围、来源白名单、去重与置信度标注；并允许用户手动确认采信。
R4（新增）访谈/社区材料偏差
- 对策：内置“偏差标注与终止条件”；支持“延后复盘”提醒；强调寻找 extremes 与 overlaps（正向/负向/未意识群体）而不是单一样本结论。

## 13. 交付物清单
- 新增页面：每日思考列表、条目详情、Gate 表单、方向研究向导、市场声音面板、周度评审、市场复核
- 新增后端：thinking/gate/routing/artifacts/research 的 API 与服务层
- 新增数据表与迁移
- 工件模板与输出目录规范
- 测试：单元 + 集成
- 文档：使用说明（README 补充）与示例条目
