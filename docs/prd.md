---
stepsCompleted: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
inputDocuments: [docs/product-brief.md]
documentCounts:
  briefs: 1
  research: 0
  brainstorming: 0
  projectDocs: 1
workflowType: 'prd'
lastStep: 11
project_name: 'SmartFish'
user_name: 'Jody'
date: '2026-01-10'
---

# Product Requirements Document - SmartFish

**Author:** Jody  
**Date:** 2026-01-10

---

## Executive Summary

SmartFish 是 BettaFish 舆情分析系统的增强版本，核心目标是将 BMAD 结构化分析方法论注入数据引擎，使报告输出从"数据堆砌"升级为"有方法论指导的可行动洞察"。

### What Makes This Special

1. **双轨选择系统** - 用户可以选择报告模板（决定结构）+ 分析方法（决定思维框架），或两者结合
2. **38 种 BMAD 分析方法** - 从六顶思考帽到红队蓝队，提供结构化思维工具
3. **需求对齐验证** - 自动检查报告是否满足用户具体要求，解决"要求 5 个方向只给 2 个"的问题
4. **预览即决策** - 用户选择前可预览模板章节结构，消除盲选焦虑

## Project Classification

**Technical Type:** Web Application (Brownfield - 扩展现有 BettaFish 系统)  
**Domain:** Business Intelligence / Analytics  
**Complexity:** Medium  
**Project Context:** Brownfield - 在现有 Flask + LangGraph 架构上扩展

---

## Success Criteria

### User Success

| 指标 | 当前 | 目标 | 衡量方式 |
|-----|------|------|---------|
| 需求满足率 | ~40% | >90% | 用户要求 vs 实际输出对比 |
| 首次选择成功率 | 未知 | >80% | 用户不需要重新生成报告 |
| 模板理解度 | 0% (盲选) | >90% | 用户能说出选择原因 |

### Business Success

| 时间点 | 目标 |
|-------|------|
| 1 个月 | 需求对齐验证功能上线，报告质量投诉减少 50% |
| 3 个月 | 分析方法选择器上线，用户开始使用 BMAD 方法 |
| 6 个月 | 用户自定义分析方法，形成方法论社区 |

### Technical Success

- 模板预览加载时间 < 200ms
- 分析方法配置热加载，无需重启服务
- 需求验证节点不增加报告生成时间 > 5%

### Measurable Outcomes

- 报告含结论章节比例：0% → 100%
- 用户使用分析方法增强比例：0% → 30%
- 智能推荐准确率：>80%

---

## Product Scope

### MVP - Minimum Viable Product

1. **需求对齐验证** (P0)
   - 从用户 query 提取数量要求
   - 检查报告是否满足要求
   - 不满足时提示用户

2. **结论章节强制** (P0)
   - 所有模板包含结论章节
   - 结论必须有数据来源引用

3. **模板预览** (P0)
   - 模板卡片显示章节数量
   - 点击预览显示完整章节结构

4. **分析方法选择器** (P0)
   - 38 种方法分类展示
   - 方法详情悬浮提示
   - 多选并传递给后端

### Growth Features (Post-MVP)

5. **智能推荐** (P1)
   - 根据用户输入推荐模板
   - 根据场景推荐分析方法

6. **分析模式切换** (P1)
   - 舆情监控模式
   - 产品洞察模式
   - 竞品分析模式

7. **防偷懒检测** (P1)
   - 检测 Agent 是否复制 prompt 示例
   - 强制要求搜索结果作为来源

### Vision (Future)

8. **用户自定义方法** (P2)
   - 用户创建自己的分析方法
   - 方法论社区分享

9. **假设验证清单** (P2)
   - 标记无数据支撑的结论
   - 生成验证实验建议

---

## User Journeys

### Journey 1: 新手用户 - 纯模板模式

**用户:** 产品经理小王，第一次使用 SmartFish  
**目标:** 快速生成一份市场分析报告

```
1. 小王输入"宠物社交App市场分析"
2. 看到 8 个模板卡片，不知道选哪个
3. 注意到"市场竞争格局分析"有绿色推荐标记
4. 点击[预览]，看到 6 个章节结构
5. 确认这是想要的，点击[使用此模板]
6. 跳过分析方法选择（折叠状态）
7. 点击[生成报告]
8. 收到报告，包含完整的结论章节
```

**成功指标:** 小王在 30 秒内完成选择，报告满足预期

### Journey 2: 进阶用户 - 混合模式

**用户:** 市场分析师老李，熟悉各种分析框架  
**目标:** 用六顶思考帽方法分析品牌声誉

```
1. 老李输入"新能源汽车品牌声誉"
2. 选择"企业品牌声誉分析"模板
3. 展开"分析方法增强"区域
4. 在"头脑风暴"标签下选择"六顶思考帽"
5. 在"高级引导"标签下选择"五个为什么"
6. 悬停查看方法说明，确认适合
7. 点击[生成报告]
8. 收到报告，每个章节都用六顶帽视角分析
```

**成功指标:** 老李能找到并理解想要的方法，报告体现方法论

### Journey 3: 专家用户 - 纯方法模式

**用户:** 创业者小张，想用第一性原理分析机会  
**目标:** 不受模板限制，纯方法论驱动

```
1. 小张输入"AI伴侣产品机会"
2. 不选择模板（使用默认通用模板）
3. 展开"分析方法增强"
4. 选择"第一性原理" + "红队蓝队" + "利益相关者圆桌"
5. 点击[生成报告]
6. 收到报告，章节结构由方法论决定
```

**成功指标:** 报告结构反映选择的方法论组合

---

## Domain Requirements

### 数据分析领域特性

- **实时性要求:** 舆情数据需要近实时更新
- **多源整合:** 需要整合微博、小红书、抖音等多平台数据
- **情感分析:** 需要准确的中文情感分析能力

### 合规要求

- 数据来源必须标注
- 用户隐私数据脱敏
- 爬虫行为符合 robots.txt

---

## Functional Requirements

### 模板管理

- FR1: 用户可以查看所有可用报告模板列表
- FR2: 用户可以预览模板的章节结构
- FR3: 用户可以选择一个模板用于报告生成
- FR4: 系统可以根据用户输入推荐合适的模板
- FR5: 管理员可以添加新的报告模板

### 分析方法管理

- FR6: 用户可以查看所有可用分析方法列表
- FR7: 用户可以按分类（头脑风暴/高级引导/游戏化）筛选方法
- FR8: 用户可以查看分析方法的详细说明
- FR9: 用户可以选择多个分析方法组合使用
- FR10: 系统可以将选中的分析方法注入 Agent prompt
- FR11: 管理员可以添加新的分析方法配置

### 报告生成

- FR12: 用户可以输入分析主题
- FR13: 用户可以选择模板 + 方法组合生成报告
- FR14: 系统可以在报告生成后验证是否满足用户需求
- FR15: 系统可以强制生成结论章节
- FR16: 系统可以检测 Agent 是否偷懒使用示例内容

### 用户界面

- FR17: 用户可以在一个页面完成所有选择
- FR18: 用户可以清除已选择的分析方法
- FR19: 用户可以查看已选择的模板和方法摘要
- FR20: 用户可以在移动端完成基本操作

---

## Non-Functional Requirements

### 性能

- NFR1: 模板预览弹窗加载时间 < 200ms
- NFR2: 分析方法配置加载时间 < 100ms
- NFR3: 需求验证不增加报告生成时间 > 5%

### 可用性

- NFR4: 新用户在 30 秒内完成首次模板选择
- NFR5: 所有交互元素支持键盘访问
- NFR6: 颜色对比度符合 WCAG AA 标准

### 可维护性

- NFR7: 分析方法配置为 YAML 文件，支持热加载
- NFR8: 模板元数据与模板内容分离
- NFR9: 新增分析方法无需修改代码

### 兼容性

- NFR10: 支持 Chrome、Firefox、Safari 最新两个版本
- NFR11: 支持 1024px 以上屏幕宽度
- NFR12: 移动端支持基本查看和选择功能

---

## Technical Considerations

### 现有架构约束

- Flask 后端 + Jinja2 模板
- LangGraph 多 Agent 协作
- WeasyPrint PDF 渲染

### 集成点

| 集成点 | 修改内容 |
|-------|---------|
| `templates/index.html` | 添加模板预览、方法选择器 UI |
| `app.py` | 添加模板/方法配置 API |
| `ForumEngine/llm_host.py` | 注入选中的分析方法 prompt |
| `ReportEngine/nodes/` | 添加需求验证节点 |
| `ReportEngine/prompts/prompts.py` | 添加需求对齐约束 |

### 新增文件

```
config/
├── analysis_methods/
│   ├── six_thinking_hats.yaml
│   ├── five_whys.yaml
│   └── ... (38 个方法配置)
└── template_meta/
    ├── brand_reputation.yaml
    └── ... (8 个模板元数据)

ReportEngine/
└── nodes/
    └── requirement_validation_node.py
```

---

## Risks and Mitigations

| 风险 | 影响 | 概率 | 缓解措施 |
|-----|------|------|---------|
| 数量提取不准确 | 误判需求满足 | 中 | LLM 辅助提取 + 人工兜底 |
| 方法论注入导致报告过长 | 用户体验下降 | 中 | 设置章节字数上限 |
| 防偷懒误判 | 正常内容被拒绝 | 低 | 相似度阈值可配置 |
| 38 种方法选择困难 | 用户决策瘫痪 | 中 | 智能推荐 + 渐进式披露 |

---

## Open Questions

- [ ] 分析方法是否支持用户自定义？（P2 考虑）
- [ ] 需求验证不通过时，自动重试还是提示用户？
- [ ] 是否需要保存用户的方法偏好？
- [ ] 纯方法模式下，章节结构如何自动生成？

---

## Appendix A: 完整 BMAD 分析方法清单 (38 种)

### A.1 头脑风暴技术 (20 种)

| ID | 方法 | 描述 |
|----|------|------|
| what_if | What If 场景 | 提出假设性问题，探索可能性 |
| analogy | 类比思维 | 从其他领域寻找类似解决方案 |
| reverse | 逆向/反转思维 | 反向思考问题，发现新视角 |
| first_principles | 第一性原理 | 回归基本原理，从根本分析 |
| scamper | SCAMPER | 替代/合并/调整/修改/另用/消除/重排 |
| six_hats | 六顶思考帽 | 白/红/黑/黄/绿/蓝六种思维视角 |
| mind_map | 思维导图 | 从中心概念向外发散 |
| yes_and | "Yes, And..." 构建 | 接受并扩展他人想法 |
| round_robin | 轮流贡献 | 每人依次贡献想法 |
| random_stimulus | 随机刺激 | 引入随机元素激发创意 |
| five_whys | 五个为什么 | 连续追问找到根本原因 |
| morphological | 形态分析 | 列出参数，探索组合可能性 |
| provocation | 挑衅技术 (PO) | 提出挑衅性陈述激发新想法 |
| forced_connection | 强制关联 | 连接不相关概念寻找创新 |
| assumption_reversal | 假设反转 | 挑战核心假设，重新构建 |
| role_play | 角色扮演 | 从不同利益相关者角度思考 |
| time_shift | 时间转移 | "1995年/2030年如何解决？" |
| resource_constraint | 资源约束 | "只有10元和1小时怎么办？" |
| metaphor_mapping | 隐喻映射 | 用隐喻理解复杂概念 |
| question_storming | 问题风暴 | 生成问题而非答案 |

### A.2 高级引导方法 (15 种)

| ID | 方法 | 描述 |
|----|------|------|
| expand_contract | 扩展或收缩 | 根据受众调整内容深度 |
| chain_of_thought | 解释推理 (CoT) | 逐步展示思考过程 |
| critique_refine | 批评与精炼 | 审查输出，识别改进点 |
| logic_flow | 逻辑流程分析 | 检查内容结构和依赖关系 |
| goal_alignment | 目标对齐评估 | 评估内容是否服务于目标 |
| risk_identification | 风险识别 | 从专业角度识别潜在风险 |
| devils_advocate | 批判性挑战 | 扮演魔鬼代言人挑战方案 |
| tree_of_thought | 思维树深潜 | 分解问题，探索多条推理路径 |
| premortem | 事后诸葛亮反思 | 假设回顾，提取教训 |
| agile_perspectives | 敏捷团队视角 | PO/SM/Dev/QA 多角色轮换 |
| stakeholder_roundtable | 利益相关者圆桌 | 多方虚拟会议，综合观点 |
| meta_prompting | 元提示分析 | 反思当前方法，优化流程 |
| self_consistency | 自一致性验证 | 多次生成取共识 |
| rewoo | ReWOO 推理 | 推理-观察-优化循环 |
| role_pattern_hybrid | 角色-模式混合 | 结合角色扮演与模式匹配 |

### A.3 游戏化方法 (3 种)

| ID | 方法 | 描述 |
|----|------|------|
| red_blue_team | 红队 vs 蓝队 | 攻防对抗，发现漏洞 |
| innovation_tournament | 创新锦标赛 | 多方案竞争评分 |
| escape_room | 密室逃脱挑战 | 在约束中寻找创意解决方案 |

---

## Appendix B: 现有报告模板清单 (9 种)

| ID | 模板名称 | 章节数 | 适用场景 |
|----|---------|-------|---------|
| brand_reputation | 企业品牌声誉分析报告 | 7 | 品牌监测、声誉管理 |
| market_competition | 市场竞争格局舆情分析报告 | 6 | 竞品分析、市场研究 |
| policy_industry | 特定政策或行业动态舆情分析报告 | 5 | 政策解读、行业趋势 |
| user_product | 用户中心化产品与体验分析报告 | 6 | 产品优化、用户研究 |
| crisis_pr | 突发事件与危机公关舆情报告 | 5 | 危机应对、公关策略 |
| daily_monitor | 日常或定期舆情监测报告 | 4 | 日常监控、周报月报 |
| social_hotspot | 社会公共热点事件分析报告 | 5 | 热点追踪、舆论分析 |
| business_strategy | 专业商业战略与深度洞察报告 | 8 | 战略规划、深度研究 |
| narrow_door | 窄门创业机会发现报告 | 7 | 创业机会、利基市场、Zero to Sold |
