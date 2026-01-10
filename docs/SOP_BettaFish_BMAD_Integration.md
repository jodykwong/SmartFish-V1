# BettaFish x BMAD-METHOD 深度分析与集成方案报告

> **版本:** 1.0  
> **角色:** 产品经理 & 系统架构师  
> **目标:** 探索如何将 BMAD 的敏捷分析方法论注入 BettaFish 数据引擎  
> **创建日期:** 2026-01-10

---

## 第一部分：竞品分析 (Competitive Analysis)

### 1. 定位差异

| 维度 | BettaFish (微舆) | BMAD-METHOD (Analysis Agent) |
|------|------------------|------------------------------|
| **本质定位** | 垂直行业 AI 应用（舆情/市场洞察） | 通用软件开发方法论（SDLC 辅助） |
| **核心能力** | 实时数据抓取 (Active Data Retrieval) | 逻辑推理与需求建模 (Logic Modeling) |
| **典型产出** | 深度分析报告 (HTML/PDF) | 需求文档、User Stories (Markdown) |
| **协作机制** | 多智能体论坛辩论 (Forum Engine) | 状态流转与上下文传递 (Phase-based) |
| **数据依赖** | 极度依赖外部实时数据（必须有 Source） | 主要依赖 LLM 内建知识（逻辑推理） |

### 2. 架构对比

**BettaFish** 采用的是 **"数据驱动"** 架构：
- 核心在于 MindSpider（爬虫）获取真实世界信号
- 通过 ForumEngine 实现多视角消歧
- 强调"每一句话都必须有 Source"

**BMAD-METHOD** 采用的是 **"意图驱动"** 架构：
- 核心在于将模糊的 Idea 通过 Analysis → Architect → Developer 链路转化为可执行的代码资产
- 强调"基于上一轮结果动态调整下一轮策略"的灵活性（Refinement Loop）

### 3. 核心差异总结

```
BettaFish = 高性能显卡 (GPU) - 数据挖掘能力强
BMAD = 操作系统 (OS) - 调度逻辑/分析方法论强

融合目标：用 BMAD 的调度逻辑去驱动 BettaFish 的算力
```

---

## 第二部分：现状诊断 - 为什么 BettaFish 显得"固定"？

### 问题 1：Prompt 层 (Static Prompts)
- 在 `ReportEngine/prompts/` 和 `ForumEngine` 中，Prompt 主要是指向性的指令
- 例如："请总结这段评论的情感倾向"
- **缺乏推理过程和方法论引导**

### 问题 2：Workflow 层 (Linear Pipeline)
- 流程是锁死的：`用户提问 → 拆解关键词 → 搜索 → 总结 → 生成报告`
- 缺少 BMAD 中那种"基于上一轮结果动态调整下一轮策略"的灵活性

### 问题 3：模板驱动 vs 需求驱动
- 系统先选模板 → 再按模板章节填充内容
- 而不是先理解需求 → 再组织内容结构
- 导致输出与用户具体需求不对齐

---

## 第三部分：移植 SOP (Standard Operating Procedure)

### 阶段一：资产结构映射 (Structure Mapping)

**目标:** 将输出目标从"舆情汇总"转为"产品决策"。

#### 1.1 定义新的文档标准 (Artifact Definition)

参考 BMAD 的 docs 目录，确定 BettaFish 需要生成的三类核心分析模块：

| 模块 | 对应 Agent | 输出内容 |
|------|-----------|----------|
| **模块 A - 市场定位 (Product Brief)** | QueryEngine | 目标受众、痛点分析、价值主张 |
| **模块 B - 竞品分析 (Competitive Analysis)** | InsightEngine | 竞品列表、功能对比矩阵、SWOT 分析 |
| **模块 C - 需求验证 (User Story Validation)** | MediaEngine | 用户真实反馈佐证、负面情绪预警 |

#### 1.2 创建"混合型"报告模版

**位置:** `ReportEngine/report_template/`

**新建文件:** `bmad_discovery.md`

**章节结构参考:**

```markdown
## 1.0 执行摘要 (Executive Summary)
- 核心发现
- 关键建议
- 风险提示

## 2.0 市场真实现状 (Market Reality)
- 利用 QueryEngine 聚合实时新闻
- 行业规模与趋势
- 政策环境

## 3.0 用户痛点挖掘 (Pain Point Extraction)
- 利用 MediaEngine 提取评论区的负面反馈
- JTBD (Jobs to be Done) 分析
- 用户画像

## 4.0 竞品机会点 (Competitor Gaps)
- 对比分析私有库与公开数据
- 功能对比矩阵
- SWOT 分析

## 5.0 MVP 功能建议 (Feature Recommendations)
- 基于上述数据进行逻辑推导
- 优先级排序
- 技术可行性评估

## 6.0 风险评估与下一步行动 (Risk & Next Steps)
- 关键假设验证清单
- 建议的验证实验
- 时间线建议
```

**操作要点:**
- 移除原有的"声量趋势图"、"词云"等纯统计章节
- 插入 BMAD 风格的章节标题
- 强制要求每个结论都有数据来源

---

### 阶段二：大脑逻辑注入 (Prompt Engineering)

**目标:** 改变 Agent 的思考方式，从"寻找数据"转变为"验证假设"。

#### 2.1 重塑"论坛主持人" (Forum Host Refactoring)

**位置:** `ForumEngine/llm_host.py`

**原逻辑:**
> "引导大家讨论舆情事件的看法。"

**新逻辑 (BMAD注入):**
> "你是一名基于 BMAD 方法论的首席产品官 (CPO)。你的目标是利用各方数据来定义一款成功的产品。请按照以下步骤引导讨论：
> 
> 1. **定义阶段:** 首先明确用户是谁？他们有什么未被满足的需求？
> 2. **发散阶段:** 基于需求，市面上有哪些现有解决方案（竞品）？它们的弱点是什么？
> 3. **收敛阶段:** 总结我们应该做什么功能来切入市场？
> 
> 在每轮辩论中强制 Agent 回答：'这个发现对我们的产品功能设计有什么具体影响？'"

#### 2.2 角色特化 (Agent Specialization)

赋予现有 Agent 新的 BMAD 角色卡（Persona）：

| 原角色 | 新角色 | 指令重点变化 |
|--------|--------|-------------|
| Query Agent (搜新闻) | **市场研究员 (Market Researcher)** | 从"搜新闻"改为"搜寻行业报告、白皮书和竞品官网" |
| Insight Agent (私库分析) | **业务分析师 (Business Analyst)** | 从"分析数据库"改为"基于现有数据进行 SWOT 推演" |
| Media Agent (多模态) | **用户体验师 (UX Researcher)** | 从"看视频内容"改为"从评论区提取用户抱怨（Pain Points）和期待（Wishlist）" |

#### 2.3 章节生成 Prompt 强化

**位置:** `ReportEngine/prompts/prompts.py`

**修改 `SYSTEM_PROMPT_CHAPTER_JSON`，增加以下约束:**

```
### 用户需求对齐要求 (CRITICAL)
1. 在生成任何内容之前，先提取用户原始 query 中的具体要求（如"5个方向"、"特定格式"等）
2. 确保输出内容完整覆盖用户的所有具体要求
3. 如果用户给了示例，必须将其视为"参考"而非"答案"，需要通过搜索发现新的内容
4. 每个章节结束前，自检是否满足了用户的具体要求
```

---

### 阶段三：工作流编排 (Workflow Orchestration)

**目标:** 打破线性的"搜索-总结"流程，引入 BMAD 的"规划-执行-验证"循环。

#### 3.1 引入"预分析"步骤 (Pre-computation Logic)

在用户输入 Prompt 之后，Agent 实际执行搜索之前，插入一个思维链 (Chain of Thought) 步骤：

**操作 SOP:**

1. 配置 LLM 在接收用户简单指令（如"我想做一个宠物社交App"）后，**先不要调用搜索工具**
2. 要求 LLM 先根据 BMAD 框架生成一份 **"研究大纲 (Research Plan)"**
3. 将这份大纲拆解为具体的搜索关键词列表

**示例:**
```
用户输入: "我想做一个宠物社交App"

研究大纲输出:
1. 市场规模: "宠物社交 市场规模 2025"
2. 用户痛点: "宠物App 用户 抱怨 差评"
3. 竞品分析: "宠物社交App 竞品 对比"
4. 技术趋势: "宠物AI 技术 趋势"
5. 政策风险: "宠物 数据隐私 法规"
```

#### 3.2 建立"证据校验"机制 (Evidence Check)

移植 BMAD 的严谨性，要求 BettaFish 在做结论时必须引用来源。

**操作 SOP:**

1. 修改 Prompt 约束，要求所有生成的"产品建议"必须附带 `[Source ID]`
2. 如果某个功能建议没有来自 Media Agent 的用户评论作为支撑，则标记为 `[Hypothesis - 待验证假设]`
3. 在报告末尾增加"假设验证清单"章节

#### 3.3 增加"需求-输出对齐验证"环节

**新增验证节点:** 在报告生成完成后，增加一个自动检查步骤：

```
验证清单:
□ 用户要求的数量是否满足（如"5个方向"）
□ 用户要求的格式是否符合
□ 是否有结论/总结章节
□ 每个结论是否有数据支撑
```

---

### 阶段四：验证与迭代 (Validation)

**目标:** 确保移植后的"新物种"既懂分析，又懂数据。

#### 4.1 测试用例设计

准备一个全新的、模糊的创业点子进行测试（例如："面向老年人的AI伴侣"）。

**期望输出对比:**

| 维度 | 原版 BettaFish | BMAD 版 BettaFish |
|------|---------------|-------------------|
| 输出内容 | 最近关于老年人AI的新闻有哪些，哪家公司融资了 | 老年人的核心痛点是"孤独"而非"科技感"，市面上的竞品操作太复杂，建议产品核心功能应包含"语音优先交互"和"子女远程监控" |
| 可行动性 | 低（只是信息汇总） | 高（有具体的产品建议） |

#### 4.2 质量验收标准 (Definition of Done)

| 维度 | 验收标准 |
|------|---------|
| **结构性** | 报告是否包含 BMAD 标准的章节（User, Problem, Solution）？ |
| **逻辑性** | 结论是否由数据推导而来，而不是 LLM 的幻觉？ |
| **辩论质量** | Forum 中的 Agent 是否针对"产品可行性"发生了有价值的争论？ |
| **需求对齐** | 输出是否满足用户原始 query 中的所有具体要求？ |
| **完整性** | 报告是否有明确的结论/总结章节？ |

---

## 第四部分：具体代码/架构改造指南

### 修改清单

| 修改模块 | 文件路径 | 修改动作 |
|---------|---------|---------|
| **Forum Host (大脑)** | `ForumEngine/llm_host.py` | 替换 `HOST_SYSTEM_PROMPT`，将 BMAD 的 brainstorm-project prompt 逻辑加入 |
| **Templates (骨架)** | `ReportEngine/report_template/*.md` | 新增 `bmad_discovery.md`，参考 BMAD 的 product-brief 结构 |
| **Chapter Prompt (章节生成)** | `ReportEngine/prompts/prompts.py` | 修改 `SYSTEM_PROMPT_CHAPTER_JSON`，增加需求对齐约束 |
| **Validation Node (验证)** | `ReportEngine/nodes/` | 新增 `requirement_validation_node.py`，检查输出是否满足用户需求 |
| **Agent Prompts (角色)** | 各 Engine 的 prompts 文件 | 增加 BMAD 角色卡（Persona）定义 |

---

## 第五部分：架构师建议 (Architect's Insights)

### 1. 解耦分析逻辑
建议将分析逻辑从 Python 代码中抽离，放入独立的 `logic_config.yaml` 中，方便随时切换"舆情模式"和"BMAD 模式"。

### 2. 强化 GraphRAG
在移植过程中，应充分利用 BettaFish 现有的 GraphRAG 能力，将 BMAD 生成的知识实体存入图数据库，实现跨任务的经验复用。

### 3. 保留 BettaFish 的野性
BettaFish 最强大的地方是它的爬虫（MindSpider）。BMAD 逻辑是"脑"，BettaFish 是"眼"。**千万不要在重构 Prompt 时限制了它去全网爬取数据的能力**，否则就变成了一个普通的 ChatGPT 对话框。

### 4. 版本控制
建议 fork 一个新的分支 `feature/bmad-analysis-mode` 进行上述配置修改，保留 `main` 分支作为纯舆情分析版本。

---

## 第六部分：移植挑战与解决方案

### 核心冲突：数据源的差异

| 系统 | 数据依赖 |
|------|---------|
| BMAD Analysis Agent | 主要依赖 LLM 的内建知识（逻辑推理和常识） |
| BettaFish | 极度依赖外部实时数据（每一句话都必须有 Source） |

### 解决方案

在移植 BMAD 逻辑时，**必须保留 BettaFish 的 "Evidence Check" (证据校验) 机制**：

- 当 BMAD 逻辑推导出"用户可能喜欢低价产品"时
- 必须强制 BettaFish 的 SearchNode 去微博/小红书搜索"价格 敏感"相关的真实评论来佐证这一观点
- 而不是仅凭 LLM 瞎猜

---

## 附录：下一步行动建议

### 最小可行验证 (MVP Validation)

1. **第一步（成本最低）:** 在 `ReportEngine/report_template/` 中手写一个 `bmad_discovery.md` 模版文件
2. **第二步:** 尝试让 ReportEngine 调用这个模版，看看 BettaFish 能否用它爬取的数据填满这个模版
3. **第三步:** 根据结果调整 Prompt 强度

这不需要改动核心代码，只需要改动 Markdown 和 Prompt。

---

*文档结束*
