# Audience First 功能改造设计文档

## 文档信息
- **版本**: v1.0
- **日期**: 2026-02-08
- **状态**: 设计评审中
- **目标**: 实现 Audience First 自动受众簇分析

---

## 一、需求概述

### 1.1 目标
从"痛点聚类"升级到"受众聚类"，实现：
- 自动识别 5-8 个受众簇
- 输出 6 项结构化卡片（受众画像/水边/痛点/土办法/付费信号/MVP切口）
- 4 维度评分（WTP/痛苦高频/Moat/GTM）
- Top2 推荐 + 90天验证计划

### 1.2 现状差距
| 功能 | 现状 | 目标 |
|------|------|------|
| 聚类对象 | 痛点 | 受众 |
| 输出格式 | 非结构化 | 结构化卡片 |
| 评分机制 | 无 | 4维度评分 |
| 证据归因 | 弱 | 强（可追溯） |

---

## 二、架构设计

### 2.1 新增模块

```
SmartFish/
├── audience_clustering_engine.py    # 新增：受众聚类引擎
├── thinking/
│   ├── models/
│   │   ├── audience_cluster.py      # 新增：受众簇模型
│   │   └── evidence_ref.py          # 新增：证据引用模型
│   └── services/
│       └── audience_service.py      # 新增：受众服务
├── ReportEngine/
│   └── report_template/
│       └── audience_first_report.md # 新增：受众优先报告模板
└── config/
    └── audience_dictionaries/       # 新增：词典配置
        ├── roles.yaml
        ├── scenarios.yaml
        └── kpi_constraints.yaml
```

### 2.2 数据模型

#### AudienceCluster（受众簇）
```python
class AudienceCluster:
    cluster_id: str              # 簇ID
    role: str                    # 角色（如：电商运营）
    scenario: str                # 场景（如：大促备战）
    kpi_constraints: List[str]   # KPI约束（如：GMV、转化率）
    waterholes: List[str]        # 水边（聚集地）
    pain_points: List[PainPoint] # 痛点列表
    workarounds: List[str]       # 土办法
    payment_signals: List[str]   # 付费信号
    evidence_refs: List[EvidenceRef]  # 证据引用
    score_card: ScoreCard        # 评分卡
```

#### EvidenceRef（证据引用）
```python
class EvidenceRef:
    platform: str      # 平台（微博/小红书/知乎）
    url: str          # 来源URL
    author: str       # 作者
    time: datetime    # 时间
    text: str         # 原文
    snippet: str      # 关键片段
    engagement: dict  # 互动数据（点赞/评论/转发）
```

#### ScoreCard（评分卡）
```python
class ScoreCard:
    wtp_score: float           # 付费意愿 (0-10)
    pain_frequency: float      # 痛苦高频 (0-10)
    moat_score: float         # 护城河 (0-10)
    gtm_score: float          # GTM难度 (0-10)
    total_score: float        # 总分
    evidence_count: int       # 证据数量
    confidence: float         # 置信度
```

---

## 三、核心功能实现

### 3.1 受众聚类引擎

#### 文件：`audience_clustering_engine.py`

**输入**:
```python
{
    "raw_data": [
        {
            "text": "用户原话",
            "platform": "微博",
            "metadata": {...}
        }
    ],
    "keywords": ["关键词列表"]
}
```

**输出**:
```python
{
    "clusters": [AudienceCluster],
    "total_count": 5,
    "clustering_method": "rule_based"
}
```

**聚类逻辑**（MVP版本 - 规则聚类）:

1. **标签提取**
   - 岗位标签：匹配 `roles.yaml`（运营/产品/设计/开发...）
   - 场景标签：匹配 `scenarios.yaml`（大促/日常/新品上线...）
   - KPI标签：匹配 `kpi_constraints.yaml`（GMV/转化率/ROI...）

2. **聚类分组**
   ```python
   cluster_key = (role, scenario, kpi)
   # 例如：("电商运营", "大促备战", "GMV")
   ```

3. **证据归集**
   - 每个簇收集相关的用户原话
   - 提取痛点/土办法/付费信号
   - 记录证据来源

4. **评分计算**
   - WTP: 付费信号词频 × 强度权重
   - 痛苦高频: 痛点提及次数 × 情绪强度
   - Moat: 土办法复杂度评分
   - GTM: 水边集中度评分

**最小实现**（~200行）:
```python
class AudienceClusteringEngine:
    def __init__(self):
        self.role_dict = load_yaml('roles.yaml')
        self.scenario_dict = load_yaml('scenarios.yaml')
        self.kpi_dict = load_yaml('kpi_constraints.yaml')
    
    def cluster(self, raw_data, max_clusters=5):
        # 1. 标签提取
        tagged_data = self._tag_data(raw_data)
        
        # 2. 聚类分组
        clusters = self._group_by_tags(tagged_data)
        
        # 3. 评分排序
        scored_clusters = self._score_clusters(clusters)
        
        # 4. 返回Top N
        return sorted(scored_clusters, 
                     key=lambda x: x.score_card.total_score, 
                     reverse=True)[:max_clusters]
```

---

### 3.2 ReportEngine 模板扩展

#### 文件：`ReportEngine/report_template/audience_first_report.md`

**模板结构**:
```markdown
# Audience First 分析报告

## 执行摘要
- 分析时间：{{date}}
- 数据来源：{{platforms}}
- 受众簇数量：{{cluster_count}}
- Top2 推荐：{{top2_names}}

## 一、受众簇分析

### 簇1：{{cluster.role}} - {{cluster.scenario}}

#### 1.1 受众画像
- **角色**：{{cluster.role}}
- **场景**：{{cluster.scenario}}
- **KPI约束**：{{cluster.kpi_constraints}}
- **规模估算**：{{cluster.size_estimate}}

#### 1.2 水边（Waterholes）
{{#each cluster.waterholes}}
- {{this}}
{{/each}}

#### 1.3 核心痛点
{{#each cluster.pain_points}}
- **痛点{{@index}}**：{{this.description}}
  - 证据：{{this.evidence_snippet}}
  - 来源：[{{this.platform}}]({{this.url}})
{{/each}}

#### 1.4 土办法
{{#each cluster.workarounds}}
- {{this}}
{{/each}}

#### 1.5 付费信号
{{#each cluster.payment_signals}}
- {{this}}
{{/each}}

#### 1.6 评分卡
| 维度 | 得分 | 说明 |
|------|------|------|
| 付费意愿 (WTP) | {{cluster.score_card.wtp_score}}/10 | {{wtp_reason}} |
| 痛苦高频 | {{cluster.score_card.pain_frequency}}/10 | {{pain_reason}} |
| 护城河 (Moat) | {{cluster.score_card.moat_score}}/10 | {{moat_reason}} |
| GTM难度 | {{cluster.score_card.gtm_score}}/10 | {{gtm_reason}} |
| **总分** | **{{cluster.score_card.total_score}}/40** | 置信度: {{cluster.score_card.confidence}}% |

---

## 二、Top2 推荐

### 推荐1：{{top1.role}} - {{top1.scenario}}
- **总分**：{{top1.score_card.total_score}}/40
- **核心优势**：{{top1.advantages}}
- **关键风险**：{{top1.risks}}

### 推荐2：{{top2.role}} - {{top2.scenario}}
- **总分**：{{top2.score_card.total_score}}/40
- **核心优势**：{{top2.advantages}}
- **关键风险**：{{top2.risks}}

---

## 三、90天验证计划

### Top1 验证计划
**目标**：验证 {{top1.role}} 的付费意愿

| 周期 | 实验 | 成功指标 | 资源需求 |
|------|------|----------|----------|
| Week 1-2 | {{experiment1}} | {{metric1}} | {{resource1}} |
| Week 3-4 | {{experiment2}} | {{metric2}} | {{resource2}} |
| Week 5-8 | {{experiment3}} | {{metric3}} | {{resource3}} |
| Week 9-12 | {{experiment4}} | {{metric4}} | {{resource4}} |

### Top2 验证计划
（同上结构）

---

## 四、证据附录

### 证据清单
{{#each all_evidence}}
- [{{@index}}] {{this.platform}} - {{this.author}} - {{this.time}}
  - 原文：{{this.text}}
  - 链接：{{this.url}}
{{/each}}
```

---

### 3.3 Thinking System 扩展

#### 3.3.1 数据库扩展

**新增表：`audience_clusters`**
```sql
CREATE TABLE audience_clusters (
    id INTEGER PRIMARY KEY,
    entry_id INTEGER NOT NULL,
    cluster_id VARCHAR(50) NOT NULL,
    role VARCHAR(100),
    scenario VARCHAR(200),
    kpi_constraints TEXT,  -- JSON array
    waterholes TEXT,       -- JSON array
    pain_points TEXT,      -- JSON array
    workarounds TEXT,      -- JSON array
    payment_signals TEXT,  -- JSON array
    score_card TEXT,       -- JSON object
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (entry_id) REFERENCES thinking_entries(id)
);

CREATE TABLE evidence_refs (
    id INTEGER PRIMARY KEY,
    cluster_id INTEGER NOT NULL,
    platform VARCHAR(50),
    url TEXT,
    author VARCHAR(100),
    time TIMESTAMP,
    text TEXT,
    snippet TEXT,
    engagement TEXT,  -- JSON object
    FOREIGN KEY (cluster_id) REFERENCES audience_clusters(id)
);
```

#### 3.3.2 新增 Service

**文件：`thinking/services/audience_service.py`**

```python
class AudienceService:
    @staticmethod
    def analyze_audiences(entry_id: int, keywords: List[str]) -> List[AudienceCluster]:
        """分析受众簇"""
        # 1. 调用 MindSpider 抓取数据
        raw_data = mindspider_crawl(keywords)
        
        # 2. 调用聚类引擎
        engine = AudienceClusteringEngine()
        clusters = engine.cluster(raw_data, max_clusters=5)
        
        # 3. 保存到数据库
        for cluster in clusters:
            db.session.add(AudienceCluster(
                entry_id=entry_id,
                **cluster.to_dict()
            ))
        db.session.commit()
        
        return clusters
    
    @staticmethod
    def generate_report(entry_id: int) -> str:
        """生成 Audience First 报告"""
        clusters = AudienceCluster.query.filter_by(entry_id=entry_id).all()
        
        # 调用 ReportEngine
        report = ReportEngine.render(
            template='audience_first_report.md',
            data={'clusters': clusters}
        )
        
        return report
```

#### 3.3.3 新增 API 路由

**文件：`thinking/routes.py`**

```python
@thinking_bp.route('/entries/<int:entry_id>/audience-analysis', methods=['POST'])
def analyze_audiences(entry_id):
    """触发受众分析"""
    data = request.get_json()
    keywords = data.get('keywords', [])
    
    clusters = AudienceService.analyze_audiences(entry_id, keywords)
    
    return jsonify({
        'success': True,
        'cluster_count': len(clusters),
        'clusters': [c.to_dict() for c in clusters]
    })

@thinking_bp.route('/entries/<int:entry_id>/audience-report', methods=['GET'])
def get_audience_report(entry_id):
    """获取受众分析报告"""
    report = AudienceService.generate_report(entry_id)
    
    return jsonify({
        'success': True,
        'report': report
    })
```

---

### 3.4 ForumEngine 标准化

#### 文件：`ForumEngine/audience_debate.py`

**角色设定**:
```python
DEBATE_ROLES = {
    "supporter": {
        "name": "支持方",
        "prompt": """你是支持方，需要论证这个受众簇值得投入。
        关注点：
        - 付费意愿证据
        - 市场规模
        - 竞争优势
        输出格式：
        {
            "support_evidence": ["证据1", "证据2"],
            "key_advantages": ["优势1", "优势2"],
            "confidence": 0.8
        }
        """
    },
    "opponent": {
        "name": "反对方",
        "prompt": """你是反对方，需要指出风险和不确定性。
        关注点：
        - 证据不足
        - 执行难度
        - 竞争风险
        输出格式：
        {
            "opposing_evidence": ["风险1", "风险2"],
            "key_risks": ["风险1", "风险2"],
            "confidence": 0.6
        }
        """
    },
    "moderator": {
        "name": "主持人",
        "prompt": """你是主持人，需要综合双方观点做出裁决。
        输出格式：
        {
            "decision": "proceed|hold|reject",
            "uncertainties": ["不确定性1", "不确定性2", "不确定性3"],
            "next_steps": ["步骤1", "步骤2"]
        }
        """
    }
}
```

**辩论流程**:
```python
def debate_audience_cluster(cluster: AudienceCluster) -> dict:
    """对受众簇进行辩论"""
    # 1. 支持方发言
    support = llm_call(DEBATE_ROLES["supporter"]["prompt"], cluster)
    
    # 2. 反对方发言
    oppose = llm_call(DEBATE_ROLES["opponent"]["prompt"], cluster)
    
    # 3. 主持人裁决
    decision = llm_call(DEBATE_ROLES["moderator"]["prompt"], {
        "cluster": cluster,
        "support": support,
        "oppose": oppose
    })
    
    return {
        "cluster_id": cluster.cluster_id,
        "support": support,
        "oppose": oppose,
        "decision": decision
    }
```

---

## 四、配置文件

### 4.1 角色词典

**文件：`config/audience_dictionaries/roles.yaml`**

```yaml
roles:
  - name: "电商运营"
    keywords: ["运营", "电商", "店铺", "商家"]
    weight: 1.0
  
  - name: "产品经理"
    keywords: ["产品", "PM", "需求", "PRD"]
    weight: 1.0
  
  - name: "市场营销"
    keywords: ["市场", "营销", "推广", "投放"]
    weight: 1.0
  
  - name: "内容创作者"
    keywords: ["创作", "博主", "UP主", "自媒体"]
    weight: 1.0
  
  - name: "技术开发"
    keywords: ["开发", "程序员", "工程师", "技术"]
    weight: 0.8
```

### 4.2 场景词典

**文件：`config/audience_dictionaries/scenarios.yaml`**

```yaml
scenarios:
  - name: "大促备战"
    keywords: ["双11", "618", "大促", "活动"]
    weight: 1.2
  
  - name: "日常运营"
    keywords: ["日常", "常规", "维护"]
    weight: 0.8
  
  - name: "新品上线"
    keywords: ["新品", "上新", "发布"]
    weight: 1.0
  
  - name: "数据分析"
    keywords: ["数据", "分析", "报表", "指标"]
    weight: 1.0
```

### 4.3 KPI词典

**文件：`config/audience_dictionaries/kpi_constraints.yaml`**

```yaml
kpi_constraints:
  - name: "GMV"
    keywords: ["GMV", "销售额", "成交额"]
    weight: 1.2
  
  - name: "转化率"
    keywords: ["转化", "转化率", "CVR"]
    weight: 1.0
  
  - name: "ROI"
    keywords: ["ROI", "投产比", "回报率"]
    weight: 1.1
  
  - name: "用户增长"
    keywords: ["增长", "拉新", "获客"]
    weight: 1.0
```

---

## 五、实施计划

### 5.1 开发优先级

| 优先级 | 模块 | 工作量 | 依赖 |
|--------|------|--------|------|
| P0 | 数据模型定义 | 0.5天 | 无 |
| P0 | 词典配置文件 | 0.5天 | 无 |
| P0 | audience_clustering_engine.py | 1天 | 数据模型 |
| P0 | ReportEngine 模板 | 0.5天 | 无 |
| P1 | Thinking 数据库扩展 | 0.5天 | 数据模型 |
| P1 | AudienceService | 1天 | 聚类引擎 |
| P1 | API 路由 | 0.5天 | AudienceService |
| P2 | ForumEngine 标准化 | 1天 | 无 |
| P2 | 前端页面 | 1天 | API 路由 |

**总计**: 2-3天完成 MVP

### 5.2 里程碑

**Day 1**: 核心引擎
- ✅ 数据模型
- ✅ 词典配置
- ✅ 聚类引擎（规则版本）

**Day 2**: 系统集成
- ✅ Thinking 扩展
- ✅ ReportEngine 模板
- ✅ API 路由

**Day 3**: 增强功能
- ✅ ForumEngine 辩论
- ✅ 前端页面
- ✅ 测试验证

---

## 六、测试验证

### 6.1 单元测试

```python
def test_audience_clustering():
    """测试受众聚类"""
    engine = AudienceClusteringEngine()
    raw_data = load_test_data()
    
    clusters = engine.cluster(raw_data, max_clusters=5)
    
    assert len(clusters) == 5
    assert all(c.score_card.total_score > 0 for c in clusters)
    assert clusters[0].score_card.total_score >= clusters[1].score_card.total_score

def test_evidence_attribution():
    """测试证据归因"""
    cluster = clusters[0]
    
    assert len(cluster.evidence_refs) > 0
    assert all(e.platform in ['微博', '小红书', '知乎'] for e in cluster.evidence_refs)
```

### 6.2 集成测试

**测试场景**: "AI工具"方向分析

**输入**:
```python
keywords = ["AI工具", "效率", "自动化", "办公"]
```

**预期输出**:
- 5个受众簇
- 每个簇有完整的6项卡片
- Top2推荐有明确理由
- 90天验证计划可执行

---

## 七、风险与缓解

| 风险 | 影响 | 概率 | 缓解措施 |
|------|------|------|----------|
| 词典覆盖不全 | 中 | 高 | 支持动态扩展 |
| 聚类质量不稳定 | 高 | 中 | 人工审核 + 迭代优化 |
| 数据抓取失败 | 高 | 低 | 降级到示例数据 |
| 评分算法不准 | 中 | 中 | 可配置权重 |

---

## 八、后续优化方向

### 8.1 短期（1-2周）
- [ ] Embedding 聚类（替代规则聚类）
- [ ] 评分算法优化
- [ ] 词典自动扩展

### 8.2 中期（1-2月）
- [ ] 多轮辩论机制
- [ ] 历史数据对比
- [ ] A/B测试框架

### 8.3 长期（3-6月）
- [ ] 机器学习评分模型
- [ ] 实时数据流处理
- [ ] 自动验证实验执行

---

## 九、附录

### 9.1 文件清单

**新增文件**（8个）:
1. `audience_clustering_engine.py`
2. `thinking/models/audience_cluster.py`
3. `thinking/models/evidence_ref.py`
4. `thinking/services/audience_service.py`
5. `ReportEngine/report_template/audience_first_report.md`
6. `config/audience_dictionaries/roles.yaml`
7. `config/audience_dictionaries/scenarios.yaml`
8. `config/audience_dictionaries/kpi_constraints.yaml`

**修改文件**（3个）:
1. `thinking/routes.py` - 新增2个路由
2. `thinking/models/__init__.py` - 导入新模型
3. `database.py` - 新增2个表

### 9.2 API 接口

**POST** `/thinking/entries/<id>/audience-analysis`
- 触发受众分析
- 参数: `keywords: List[str]`
- 返回: `clusters: List[AudienceCluster]`

**GET** `/thinking/entries/<id>/audience-report`
- 获取分析报告
- 返回: `report: str` (Markdown)

**POST** `/thinking/entries/<id>/audience-debate`
- 触发辩论
- 参数: `cluster_ids: List[str]`
- 返回: `debates: List[DebateResult]`

---

## 十、决策点

### 需要确认的问题

1. **受众簇数量**: 默认5个还是8个？
   - 建议: 5个（可配置5-8）

2. **聚类方法**: 规则聚类还是Embedding？
   - MVP: 规则聚类
   - 后续: Embedding优化

3. **评分权重**: 4个维度权重是否相等？
   - 建议: WTP×1.2, 痛苦高频×1.0, Moat×1.0, GTM×0.8

4. **数据存储**: JSON字段还是关系表？
   - 建议: 混合（核心字段关系表，详情JSON）

5. **前端页面**: 是否需要可视化？
   - MVP: 纯API + Markdown报告
   - 后续: 可视化Dashboard

---

**文档状态**: ✅ 完成，等待评审

**下一步**: 
- 选项1: 评审通过 → 开始开发
- 选项2: 需要调整 → 修改设计
