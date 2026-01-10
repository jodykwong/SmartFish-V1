---
stepsCompleted: [1, 2, 3, 4, 5, 6, 7, 8]
inputDocuments: [docs/prd.md, docs/ux-design.md]
workflowType: 'architecture'
lastStep: 8
project_name: 'SmartFish'
user_name: 'Jody'
date: '2026-01-10'
---

# Architecture Document - SmartFish

**Author:** Jody  
**Date:** 2026-01-10

---

## Executive Summary

SmartFish 是 BettaFish 舆情分析系统的增强版本，在现有 Flask + LangGraph 架构上扩展，添加双轨选择系统（模板 + 分析方法）和需求对齐验证功能。

### Project Context

**类型:** Brownfield - 扩展现有系统  
**技术栈:** Python Flask + LangGraph + WeasyPrint  
**复杂度:** Medium  

### Architectural Goals

1. **最小侵入** - 不改变现有核心架构，通过配置和新增模块实现
2. **配置驱动** - 模板元数据和分析方法通过 YAML 配置，支持热加载
3. **向后兼容** - 现有 API 和功能保持不变

---

## Project Classification

### Scale Assessment

| 指标 | 值 | 影响 |
|-----|---|------|
| 功能需求数 | 20 FR | 中等规模 |
| 新增组件 | 7 个 | 前端为主 |
| 配置文件 | 46 个 | 8 模板 + 38 方法 |
| API 变更 | 1 个端点扩展 | 低风险 |

### Complexity Indicators

- ✅ 无实时功能需求
- ✅ 无多租户需求
- ✅ 无合规性要求变更
- ⚠️ 中等集成复杂度（需修改多个模块）

---

## Core Architectural Decisions

### Decision 1: 配置存储方案

**决策:** YAML 文件存储，启动时加载到内存

**选项分析:**
| 选项 | 优点 | 缺点 |
|-----|------|------|
| YAML 文件 | 简单、版本控制友好、无依赖 | 需重启加载 |
| 数据库存储 | 动态更新 | 增加复杂度 |
| Redis 缓存 | 高性能 | 过度设计 |

**理由:** 
- 配置变更频率低
- 与现有架构一致（无额外依赖）
- 支持 Git 版本控制

**影响:** FR5, FR11 (管理员添加模板/方法)

### Decision 2: 前端组件方案

**决策:** 原生 JavaScript + Jinja2 模板

**选项分析:**
| 选项 | 优点 | 缺点 |
|-----|------|------|
| 原生 JS | 与现有一致、无构建步骤 | 组件化较弱 |
| Vue.js | 组件化好 | 引入新依赖 |
| React | 生态丰富 | 架构变更大 |

**理由:**
- 保持与现有 `templates/index.html` 一致
- 新增组件数量有限（7 个）
- 避免引入前端构建流程

**影响:** FR17-FR20 (用户界面)

### Decision 3: 需求验证实现方案

**决策:** 新增 ReportEngine 节点

**选项分析:**
| 选项 | 优点 | 缺点 |
|-----|------|------|
| 新增节点 | 符合现有架构、可插拔 | 需理解节点机制 |
| 后处理脚本 | 简单 | 不在主流程中 |
| Prompt 约束 | 无代码改动 | 不可靠 |

**理由:**
- LangGraph 节点机制已成熟
- 可在报告生成后、渲染前执行
- 验证失败可触发重试或警告

**影响:** FR14, FR15, FR16 (报告生成验证)

### Decision 4: 分析方法注入点

**决策:** ForumEngine 主持人 Prompt 注入

**选项分析:**
| 选项 | 优点 | 缺点 |
|-----|------|------|
| ForumEngine 注入 | 影响所有 Agent 讨论 | 需修改 llm_host.py |
| 各 Agent 单独注入 | 精细控制 | 改动点多 |
| ReportEngine 注入 | 只影响报告 | 分析阶段无效 |

**理由:**
- ForumEngine 是 Agent 协作的中枢
- 主持人 Prompt 影响整体讨论方向
- 单点修改，效果全局

**影响:** FR10 (方法论注入)

---

## Implementation Patterns

### Pattern 1: 配置加载模式

```python
# config/loader.py
class ConfigLoader:
    _instance = None
    _templates = {}
    _methods = {}
    
    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
            cls._instance._load_all()
        return cls._instance
    
    def _load_all(self):
        self._templates = self._load_yaml_dir('config/template_meta/')
        self._methods = self._load_yaml_dir('config/analysis_methods/')
    
    def get_templates(self):
        return self._templates
    
    def get_methods(self, category=None):
        if category:
            return {k: v for k, v in self._methods.items() 
                    if v.get('category') == category}
        return self._methods
```

### Pattern 2: 需求验证节点

```python
# ReportEngine/nodes/requirement_validation_node.py
class RequirementValidationNode:
    def __init__(self):
        self.rules = self._load_validation_rules()
    
    def validate(self, state):
        user_query = state.get('user_query')
        report_ir = state.get('report_ir')
        
        results = {
            'passed': True,
            'failures': [],
            'warnings': []
        }
        
        # 数量要求检查
        quantity_req = self._extract_quantity(user_query)
        if quantity_req:
            actual = self._count_sections(report_ir)
            if actual < quantity_req:
                results['passed'] = False
                results['failures'].append(
                    f"要求 {quantity_req} 个，实际 {actual} 个"
                )
        
        # 结论章节检查
        if not self._has_conclusion(report_ir):
            results['passed'] = False
            results['failures'].append("缺少结论章节")
        
        return results
```

### Pattern 3: 方法论 Prompt 注入

```python
# ForumEngine/llm_host.py
def build_host_prompt(self, selected_methods=None):
    base_prompt = self.HOST_SYSTEM_PROMPT
    
    if selected_methods:
        method_prompts = []
        for method_id in selected_methods:
            method = ConfigLoader.get_instance().get_method(method_id)
            if method:
                method_prompts.append(method['prompt_template'])
        
        if method_prompts:
            base_prompt += "\n\n## 分析方法论指导\n"
            base_prompt += "\n".join(method_prompts)
    
    return base_prompt
```

### Pattern 4: API 参数扩展

```python
# app.py
@app.route('/api/generate_report', methods=['POST'])
def generate_report():
    data = request.json
    query = data.get('query')
    template_id = data.get('template_id')  # 新增
    method_ids = data.get('method_ids', [])  # 新增
    
    # 传递给 ReportEngine
    result = report_engine.generate(
        query=query,
        template_id=template_id,
        method_ids=method_ids
    )
    return jsonify(result)
```

---

## Project Structure & Boundaries

### Complete Project Directory Structure

```
BettaFish/
├── app.py                              # Flask 主应用 [修改: 添加配置 API]
├── config.py                           # 全局配置
├── requirements.txt
│
├── config/                             # [新增目录]
│   ├── __init__.py
│   ├── loader.py                       # 配置加载器
│   ├── template_meta/                  # 模板元数据
│   │   ├── brand_reputation.yaml
│   │   ├── market_competition.yaml
│   │   ├── policy_industry.yaml
│   │   ├── user_product.yaml
│   │   ├── crisis_pr.yaml
│   │   ├── daily_monitor.yaml
│   │   ├── social_hotspot.yaml
│   │   ├── business_strategy.yaml
│   │   └── narrow_door.yaml            # 新增：窄门创业机会
│   └── analysis_methods/               # 分析方法配置
│       ├── brainstorming/              # 头脑风暴 (20)
│       │   ├── six_hats.yaml
│       │   ├── five_whys.yaml
│       │   ├── scamper.yaml
│       │   └── ... (17 more)
│       ├── advanced/                   # 高级引导 (15)
│       │   ├── chain_of_thought.yaml
│       │   ├── tree_of_thought.yaml
│       │   └── ... (13 more)
│       └── gamification/               # 游戏化 (3)
│           ├── red_blue_team.yaml
│           ├── innovation_tournament.yaml
│           └── escape_room.yaml
│
├── templates/
│   └── index.html                      # [修改: 添加选择器 UI]
│
├── static/
│   ├── css/
│   │   └── smartfish.css               # [新增: 选择器样式]
│   └── js/
│       ├── template-selector.js        # [新增: 模板选择器]
│       ├── method-selector.js          # [新增: 方法选择器]
│       └── smart-recommend.js          # [新增: 智能推荐]
│
├── ForumEngine/
│   ├── __init__.py
│   ├── monitor.py
│   └── llm_host.py                     # [修改: 添加方法论注入]
│
├── ReportEngine/
│   ├── agent.py                        # [修改: 接收模板/方法参数]
│   ├── nodes/
│   │   ├── base_node.py
│   │   ├── template_selection_node.py  # [修改: 支持指定模板]
│   │   ├── chapter_generation_node.py
│   │   └── requirement_validation_node.py  # [新增: 需求验证]
│   ├── prompts/
│   │   └── prompts.py                  # [修改: 添加需求对齐约束]
│   └── report_template/
│       └── *.md                        # 现有模板 (不变)
│
└── docs/
    ├── product-brief.md
    ├── prd.md
    ├── ux-design.md
    └── architecture.md
```

### Architectural Boundaries

**API 边界:**
```
POST /api/generate_report
  ├── query: string (必需)
  ├── template_id: string (可选)
  └── method_ids: string[] (可选)

GET /api/templates
  └── 返回所有模板元数据

GET /api/methods
  ├── category: string (可选筛选)
  └── 返回分析方法列表
```

**模块边界:**
```
config/           → 配置加载，只读访问
templates/        → 前端渲染，调用 API
ForumEngine/      → Agent 协作，接收方法论
ReportEngine/     → 报告生成，接收模板/验证
```

### Requirements to Structure Mapping

| FR | 文件位置 |
|----|---------|
| FR1-FR5 | `config/loader.py`, `config/template_meta/` |
| FR6-FR11 | `config/loader.py`, `config/analysis_methods/` |
| FR12-FR16 | `ReportEngine/nodes/requirement_validation_node.py` |
| FR17-FR20 | `templates/index.html`, `static/js/`, `static/css/` |

---

## Integration Points

### 内部通信

```
用户输入
    ↓
templates/index.html (前端)
    ↓ POST /api/generate_report
app.py (Flask)
    ↓ 调用
ReportEngine.agent.generate()
    ↓ 注入方法论
ForumEngine.llm_host.build_host_prompt()
    ↓ 生成后验证
ReportEngine.nodes.requirement_validation_node.validate()
    ↓ 渲染
ReportEngine.renderers.html_renderer.render()
```

### 配置加载流程

```
应用启动
    ↓
config.loader.ConfigLoader.get_instance()
    ↓ 扫描
config/template_meta/*.yaml
config/analysis_methods/**/*.yaml
    ↓ 缓存到内存
_templates, _methods
    ↓ 提供给
API 端点 / ReportEngine / ForumEngine
```

---

## Validation Checklist

### 架构一致性

- [x] 与现有 Flask + LangGraph 架构兼容
- [x] 不引入新的外部依赖
- [x] 配置驱动，支持扩展

### PRD 覆盖

- [x] FR1-FR5 (模板管理) → config/template_meta/
- [x] FR6-FR11 (方法管理) → config/analysis_methods/
- [x] FR12-FR16 (报告生成) → ReportEngine/nodes/
- [x] FR17-FR20 (用户界面) → templates/, static/

### UX 支持

- [x] 模板预览 → API 返回 chapters 列表
- [x] 方法分类 → YAML category 字段
- [x] 智能推荐 → recommended_keywords 匹配

### NFR 满足

- [x] NFR1 (预览 <200ms) → 内存缓存
- [x] NFR7 (YAML 热加载) → ConfigLoader 单例
- [x] NFR9 (无需改代码) → 纯配置扩展
