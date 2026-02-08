# Audience First 分析报告

## 执行摘要
- **分析时间**: {{date}}
- **数据来源**: {{platforms}}
- **受众簇数量**: {{cluster_count}}
- **Top2 推荐**: {{top2_names}}

---

## 一、受众簇分析

{{#each clusters}}
### 簇{{@index_plus_1}}: {{this.role}} - {{this.scenario}}

#### 1.1 受众画像
- **角色**: {{this.role}}
- **场景**: {{this.scenario}}
- **KPI约束**: {{join this.kpi_constraints ", "}}
- **证据数量**: {{this.score_card.evidence_count}}

#### 1.2 核心痛点
{{#each this.pain_points}}
{{@index_plus_1}}. {{this}}
{{/each}}

{{#if this.workarounds}}
#### 1.3 土办法
{{#each this.workarounds}}
- {{this}}
{{/each}}
{{/if}}

{{#if this.payment_signals}}
#### 1.4 付费信号
{{#each this.payment_signals}}
- {{this}}
{{/each}}
{{/if}}

#### 1.5 评分卡
| 维度 | 得分 | 说明 |
|------|------|------|
| 付费意愿 (WTP) | {{this.score_card.wtp_score}}/10 | 基于付费信号数量 |
| 痛苦高频 | {{this.score_card.pain_frequency}}/10 | 基于证据数量 |
| 护城河 (Moat) | {{this.score_card.moat_score}}/10 | 基于土办法复杂度 |
| GTM难度 | {{this.score_card.gtm_score}}/10 | 市场进入难度 |
| **总分** | **{{this.score_card.total_score}}/40** | 置信度: {{this.score_card.confidence}}% |

#### 1.6 证据样本
{{#each this.evidence_refs}}
{{#if @first_three}}
- **[{{this.platform}}]** {{this.author}}: {{this.snippet}}
{{/if}}
{{/each}}

---

{{/each}}

## 二、Top2 推荐

### 推荐1: {{top1.role}} - {{top1.scenario}}
- **总分**: {{top1.score_card.total_score}}/40
- **核心优势**: 
  - 证据充分（{{top1.score_card.evidence_count}}条）
  - 痛点明确
  - {{#if top1.payment_signals}}存在付费信号{{/if}}
- **关键风险**: 需进一步验证市场规模

### 推荐2: {{top2.role}} - {{top2.scenario}}
- **总分**: {{top2.score_card.total_score}}/40
- **核心优势**:
  - 证据充分（{{top2.score_card.evidence_count}}条）
  - 痛点明确
  - {{#if top2.payment_signals}}存在付费信号{{/if}}
- **关键风险**: 需进一步验证市场规模

---

## 三、90天验证计划

### Top1 验证计划: {{top1.role}} - {{top1.scenario}}

**目标**: 验证付费意愿和市场规模

| 周期 | 实验 | 成功指标 | 资源需求 |
|------|------|----------|----------|
| Week 1-2 | 用户访谈（10人） | 8/10确认痛点 | 访谈脚本 |
| Week 3-4 | 落地页测试 | 转化率>5% | 简单落地页 |
| Week 5-8 | MVP原型 | 10个付费用户 | 最小可用产品 |
| Week 9-12 | 市场推广 | 50个付费用户 | 推广预算 |

### Top2 验证计划: {{top2.role}} - {{top2.scenario}}

**目标**: 验证付费意愿和市场规模

| 周期 | 实验 | 成功指标 | 资源需求 |
|------|------|----------|----------|
| Week 1-2 | 用户访谈（10人） | 8/10确认痛点 | 访谈脚本 |
| Week 3-4 | 落地页测试 | 转化率>5% | 简单落地页 |
| Week 5-8 | MVP原型 | 10个付费用户 | 最小可用产品 |
| Week 9-12 | 市场推广 | 50个付费用户 | 推广预算 |

---

## 四、证据附录

### 证据清单
{{#each all_evidence}}
**[{{@index_plus_1}}]** {{this.platform}} - {{this.author}} - {{this.time}}
> {{this.text}}

{{/each}}

---

**报告生成时间**: {{date}}
