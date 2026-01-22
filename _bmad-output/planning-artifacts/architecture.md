---
stepsCompleted: [1, 2, 3, 4, 'complete']
inputDocuments:
  - /home/sunrise/SmartFish/_bmad-output/planning-artifacts/product-brief-SmartFish-2026-01-22.md
  - /home/sunrise/SmartFish/_bmad-output/planning-artifacts/prd.md
  - /home/sunrise/SmartFish/_bmad-output/planning-artifacts/ux-design-specification.md
  - /home/sunrise/SmartFish/docs/thinking-system-analysis.md
  - /home/sunrise/SmartFish/requests.md
workflowType: 'architecture'
project_name: 'SmartFish'
user_name: 'Jody'
date: '2026-01-22'
---

# Architecture Decision Document - SmartFish 思考决策系统

_本文档通过逐步协作发现构建。随着我们共同完成每个架构决策，章节将被追加。_

## 项目上下文分析

### 需求概览

**功能需求：**

SmartFish思考决策系统包含6个核心模块：

1. **条目管理（FR1-FR2）**：结构化思考条目CRUD，支持核心字段（Signal/Target/Problem/Hypothesis/MVA等）和Zero to Sold扩展字段（Audience/市场信号/问题强度评分），需要高效检索与筛选能力。

2. **Gate机制（FR3-FR5）**：四层过滤器（人性依赖/价值自证/反馈清洁度/角色消耗），否决式设计，不可篡改审计记录，支持复活机制。

3. **BMAD路由（FR6-FR9）**：三种路由类型（Quick/Standard/Enterprise），自动建议算法，工件模板生成（tech-spec/PRD/architecture等），支持导出Markdown/PDF。

4. **Agent集成（FR10-FR11）**：调用4个现有Agent（QueryEngine/MindSpider/InsightEngine/ReportEngine），支持市场声音采集，证据回填到条目和工件。

5. **周度评审（FR12）**：聚合最近7天条目，多维度打分，生成weekly-plan.md。

6. **Zero to Sold向导（FR13-FR16）**：Audience/Problem/Solution引导，问题强度评分，访谈脚本生成，市场转向复核。

**非功能需求：**

- **NFR1 可追溯性**：完整操作时间线，状态变更历史，审计日志不可篡改
- **NFR2 可复用性**：工件模板可配置，支持版本历史
- **NFR3 稳定性**：任务失败自动重试（最多3次），失败原因可见
- **NFR4 性能**：1000条目下列表加载<1秒，Gate检查<2秒，工件生成<5秒
- **NFR5 可测试性**：单元测试覆盖率>80%，集成测试覆盖核心流程
- **NFR6 可解释性**：所有自动建议显示依据和规则

**规模与复杂度：**

- **主要领域**：Web应用（生产力与决策支持）
- **复杂度等级**：中等
- **预估架构组件**：8-10个主要组件
  - Flask Blueprint（/thinking路由）
  - Gate服务层（规则引擎）
  - 路由服务层（决策算法）
  - 工件服务层（模板渲染）
  - 任务服务层（异步调度）
  - 数据模型层（4个核心表）
  - Agent集成层（4个Agent适配器）
  - UI模板层（6个关键页面）

### 技术约束与依赖

**现有技术栈（必须兼容）：**
- Flask 2.3.3（Web框架）
- SQLAlchemy 2.0.35（ORM）
- PostgreSQL/MySQL（数据库）
- Jinja2（模板引擎）
- 现有4个Agent（QueryEngine/MindSpider/InsightEngine/ReportEngine）

**新增依赖（Phase 3）：**
- Redis（任务队列，异步Agent调用）
- 任务调度框架（Celery或类似）

**集成约束：**
- 必须复用现有Agent接口，不能修改Agent内部实现
- 必须保持现有UI风格和组件库
- 必须兼容现有数据库schema（新增表，不修改现有表）

**部署约束：**
- 单体应用架构（不拆分微服务）
- 文件系统存储工件（docs/thinking/目录）
- 本地或单服务器部署

### 跨领域关注点

**1. 工作流引擎**
- Gate四层过滤的规则引擎设计
- 路由决策算法（基于影响范围/依赖/风险）
- 状态机管理（想法→评估中→已否决/已落地）

**2. 任务队列系统**
- 异步Agent调用（避免阻塞主线程）
- 任务状态追踪（pending/running/completed/failed）
- 失败重试机制（指数退避）
- 结果回填到条目

**3. 模板渲染引擎**
- 工件模板管理（Jinja2变量替换）
- 动态内容生成（从条目字段填充）
- 版本管理（Git或数据库）

**4. 审计日志系统**
- 不可篡改的决策历史
- 完整操作时间线
- 支持追加说明但保留历史版本

**5. 证据链管理**
- Agent调研结果与条目关联
- 证据摘要回填到工件（PRD的"证据与洞察"章节）
- 来源追溯与置信度标注

**6. 性能优化**
- 数据库索引策略（user_id/status/created_at）
- 分页加载（每页20条）
- 缓存机制（模板/路由建议）

**7. 安全与权限**
- 条目私有性（仅本人可见）
- 文件路径白名单（防止路径穿越）
- LLM密钥管理（.env机制）

## Starter Template 评估

### 项目类型识别

**项目类型**: 棕地扩展（Brownfield Extension）

SmartFish 思考决策系统是在现有 Flask 应用基础上的功能扩展，而非全新项目。

### 技术栈决策

**现有技术栈（保持不变）：**

- **后端框架**: Flask 2.3.3
- **ORM**: SQLAlchemy 2.0.35
- **数据库**: PostgreSQL/MySQL（已配置）
- **模板引擎**: Jinja2
- **前端**: HTML/CSS/JS（复用现有组件）
- **Agent系统**: QueryEngine, MindSpider, InsightEngine, ReportEngine（已存在）

### 集成策略

**不使用 Starter Template，原因：**

1. **现有基础设施完善**：Flask 应用已运行，数据库已配置，Agent 系统已集成
2. **避免重构风险**：使用新 starter 需要大规模重构现有代码
3. **保持一致性**：新模块应与现有代码风格和架构保持一致
4. **降低复杂度**：扩展比重建更简单、风险更低

**集成方法：**

- 创建新的 Flask Blueprint（`thinking`）
- 扩展数据库 schema（新增表，不修改现有表）
- 复用现有 UI 组件库和样式系统
- 通过适配器模式集成现有 Agent

### 架构决策由集成驱动

由于是棕地扩展，架构决策将聚焦于：

1. **模块边界**：如何在现有代码库中清晰划分新模块
2. **数据模型扩展**：如何新增表而不影响现有功能
3. **服务层设计**：如何组织新的业务逻辑（Gate/路由/工件生成）
4. **Agent集成**：如何适配现有 Agent 接口
5. **UI集成**：如何复用现有模板和组件

**注意**：项目初始化不需要 starter 命令，而是在现有仓库中创建新目录和文件。

## 核心架构决策

### 决策 1: 模块组织架构

**决策：独立Blueprint + 服务层架构**

**目录结构：**
```
SmartFish/
├── thinking/                    # 新增模块
│   ├── __init__.py
│   ├── routes.py               # Flask Blueprint
│   ├── services/               # 业务逻辑层
│   │   ├── __init__.py
│   │   ├── gate_service.py     # Gate规则引擎
│   │   ├── routing_service.py  # 路由决策算法
│   │   ├── artifact_service.py # 工件生成
│   │   └── task_service.py     # 任务调度（Phase 3）
│   ├── models/                 # 数据模型
│   │   ├── __init__.py
│   │   ├── thinking_entry.py
│   │   ├── gate_review.py
│   │   ├── artifact.py
│   │   └── research_task.py
│   └── templates/              # UI模板
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
└── app.py                      # 注册thinking Blueprint
```

**理由：**
- 清晰的模块边界，易于维护
- 服务层封装业务逻辑，便于测试
- 符合Flask最佳实践
- 未来易于扩展或拆分

---

### 决策 2: 数据持久化策略

**决策：独立迁移脚本 + 文件系统工件存储**

**数据库迁移：**
```python
# 使用Alembic或SQL迁移脚本
# migrations/versions/xxx_add_thinking_tables.py

def upgrade():
    op.create_table('thinking_entries',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(255), nullable=False),
        sa.Column('status', sa.String(50), nullable=False),
        # ... 其他字段
    )
    op.create_table('gate_reviews', ...)
    op.create_table('artifacts', ...)
    op.create_table('research_tasks', ...)
```

**工件存储：**
- **位置**: `docs/thinking/`
- **命名**: `YYYY-MM-DD_<slug>_<type>.md`
- **元数据**: artifacts表存储path, checksum, created_at
- **版本控制**: Git管理

**理由：**
- 迁移脚本版本可控，可回滚
- 不影响现有数据库表
- 工件文件易于查看和编辑
- 支持Git版本管理

---

### 决策 3: 异步任务处理

**决策：分阶段引入异步能力**

**Phase 1-2（MVP + 工作流完善）：**
- 不实现Agent集成
- 专注Gate机制和工件生成
- 无异步任务需求

**Phase 3（Agent集成）：**
```python
# 引入Celery + Redis
from celery import Celery

celery = Celery('smartfish', 
    broker='redis://localhost:6379',
    backend='redis://localhost:6379'
)

@celery.task(bind=True, max_retries=3)
def execute_research_task(self, task_id):
    try:
        task = ResearchTask.query.get(task_id)
        # 调用Agent
        result = call_agent(task.engine, task.query)
        # 更新任务状态
        task.status = 'completed'
        task.result_path = save_result(result)
    except Exception as exc:
        task.status = 'failed'
        task.error_message = str(exc)
        raise self.retry(exc=exc, countdown=60)
```

**理由：**
- 降低初期复杂度
- Phase 1-2已有足够价值
- Celery成熟稳定，支持重试和监控
- Redis轻量级，易于部署

---

### 决策 4: Gate规则引擎设计

**决策：策略模式 + 简单规则类**

**实现：**
```python
from abc import ABC, abstractmethod
from enum import Enum

class GateResult(Enum):
    PASS = 'pass'
    WARNING = 'warning'
    FAIL = 'fail'

class GateFilter(ABC):
    @abstractmethod
    def evaluate(self, entry, user_input):
        """返回 (GateResult, reason)"""
        pass

class HumanDependencyFilter(GateFilter):
    def evaluate(self, entry, user_input):
        if user_input == 'strong_dependency':
            return (GateResult.FAIL, '强依赖他人意愿/行动')
        elif user_input == 'partial_dependency':
            return (GateResult.WARNING, '有一定依赖但可控')
        return (GateResult.PASS, '不依赖他人')

class ValueSelfEvidentFilter(GateFilter):
    def evaluate(self, entry, user_input):
        if user_input == 'needs_explanation':
            return (GateResult.FAIL, '需要反复解释价值')
        return (GateResult.PASS, '价值自证')

class FeedbackCleanFilter(GateFilter):
    def evaluate(self, entry, user_input):
        if user_input == 'not_falsifiable':
            return (GateResult.FAIL, '反馈不可证伪')
        elif user_input == 'partially_quantifiable':
            return (GateResult.WARNING, '部分依赖主观判断')
        return (GateResult.PASS, '反馈可量化')

class RoleCostFilter(GateFilter):
    def evaluate(self, entry, user_input):
        if user_input == 'need_push':
            return (GateResult.WARNING, '需要推动事情发生')
        return (GateResult.PASS, '仅为判断负责')

# 使用
class GateService:
    def __init__(self):
        self.filters = [
            HumanDependencyFilter(),
            ValueSelfEvidentFilter(),
            FeedbackCleanFilter(),
            RoleCostFilter()
        ]
    
    def evaluate(self, entry, user_inputs):
        results = []
        for i, filter in enumerate(self.filters):
            result, reason = filter.evaluate(entry, user_inputs[i])
            results.append((i+1, result, reason))
            if result == GateResult.FAIL:
                return {'decision': 'fail', 'fail_level': i+1, 
                        'fail_reason': reason, 'results': results}
        
        warnings = [r for r in results if r[1] == GateResult.WARNING]
        return {'decision': 'pass', 'warnings': warnings, 'results': results}
```

**理由：**
- 简单直接，易于理解和测试
- 策略模式易于扩展新规则
- 满足需求（4层固定规则）
- 不需要复杂规则引擎

---

### 决策 5: 路由决策算法

**决策：基于规则的评分系统**

**实现：**
```python
class RoutingService:
    # 评分规则
    IMPACT_SCORES = {
        'small': 0,
        'medium': 2,
        'large': 4
    }
    
    DEPENDENCY_THRESHOLD = 5
    
    # 路由阈值
    QUICK_THRESHOLD = 3
    STANDARD_THRESHOLD = 7
    
    def suggest_routing(self, entry):
        score = 0
        reasons = []
        
        # 1. 影响范围
        impact = self._assess_impact(entry)
        score += self.IMPACT_SCORES.get(impact, 0)
        reasons.append(f'影响范围: {impact}')
        
        # 2. 依赖数量
        dep_count = self._count_dependencies(entry)
        if dep_count > self.DEPENDENCY_THRESHOLD:
            score += 3
            reasons.append(f'依赖数量: {dep_count}')
        
        # 3. Gate警告数
        warnings = entry.gate_warnings_count or 0
        score += warnings
        if warnings > 0:
            reasons.append(f'Gate警告: {warnings}个')
        
        # 4. 证据缺口
        if entry.evidence_needed:
            score += 1
            reasons.append('需要证据补强')
        
        # 5. 技术复杂度
        if entry.constraints and 'high_complexity' in entry.constraints:
            score += 2
            reasons.append('技术复杂度高')
        
        # 决策
        if score <= self.QUICK_THRESHOLD:
            routing = 'Quick'
        elif score <= self.STANDARD_THRESHOLD:
            routing = 'Standard'
        else:
            routing = 'Enterprise'
        
        return {
            'routing': routing,
            'score': score,
            'reasons': reasons
        }
    
    def _assess_impact(self, entry):
        # 基于字段分析影响范围
        if not entry.target_segment or 'small' in entry.target_segment.lower():
            return 'small'
        elif 'enterprise' in entry.target_segment.lower():
            return 'large'
        return 'medium'
    
    def _count_dependencies(self, entry):
        if not entry.dependencies:
            return 0
        return len(entry.dependencies.split(','))
```

**理由：**
- 满足NFR6可解释性要求
- 规则透明，用户可理解
- 阈值可根据反馈调整
- 用户可覆盖系统建议

---

### 决策 6: 工件模板系统

**决策：Jinja2模板 + 文件系统管理**

**模板示例：**
```jinja2
{# docs/templates/tech-spec.md.j2 #}
---
title: {{ entry.title }}
date: {{ date }}
author: {{ user_name }}
entry_id: {{ entry.id }}
---

# Tech Spec: {{ entry.title }}

## 目标

{{ entry.problem }}

## 范围

**In Scope:**
- {{ entry.mva }}

**Out of Scope:**
- 待定义

## 验收标准

{{ entry.success_metric }}

## 风险与止损

{% if entry.gate_warnings %}
**Gate警告：**
{% for warning in entry.gate_warnings %}
- {{ warning }}
{% endfor %}
{% endif %}

{% if entry.constraints %}
**约束条件：**
{{ entry.constraints }}
{% endif %}

## 时间表

- 开始时间：{{ date }}
- 目标完成：48小时内

## 影响面分析

- 影响范围：{{ routing_info.impact }}
- 依赖数量：{{ routing_info.dependencies }}
```

**渲染服务：**
```python
from jinja2 import Environment, FileSystemLoader
import os

class ArtifactService:
    def __init__(self, template_dir='docs/templates', 
                 output_dir='docs/thinking'):
        self.env = Environment(loader=FileSystemLoader(template_dir))
        self.output_dir = output_dir
    
    def generate_artifact(self, entry, artifact_type, user_name):
        # 加载模板
        template = self.env.get_template(f'{artifact_type}.md.j2')
        
        # 准备数据
        context = {
            'entry': entry,
            'user_name': user_name,
            'date': datetime.now().strftime('%Y-%m-%d'),
            'routing_info': self._get_routing_info(entry)
        }
        
        # 渲染
        content = template.render(**context)
        
        # 保存
        filename = self._generate_filename(entry, artifact_type)
        filepath = os.path.join(self.output_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        # 记录元数据
        artifact = Artifact(
            entry_id=entry.id,
            type=artifact_type,
            path=filepath,
            checksum=self._calculate_checksum(content)
        )
        db.session.add(artifact)
        db.session.commit()
        
        return filepath
    
    def _generate_filename(self, entry, artifact_type):
        date = datetime.now().strftime('%Y-%m-%d')
        slug = self._slugify(entry.title)
        return f'{date}_{slug}_{artifact_type}.md'
    
    def _calculate_checksum(self, content):
        import hashlib
        return hashlib.sha256(content.encode()).hexdigest()
```

**理由：**
- 复用现有Jinja2技术栈
- 模板与代码分离，易于维护
- 用户可自定义模板（满足NFR2）
- 支持Git版本管理
- 模板语法强大，支持复杂逻辑

---

## 架构决策记录（ADR）总结

| ID | 决策 | 选择 | 理由 |
|----|------|------|------|
| ADR-1 | 模块组织 | 独立Blueprint + 服务层 | 清晰边界，易维护 |
| ADR-2 | 数据持久化 | 迁移脚本 + 文件系统 | 版本可控，易编辑 |
| ADR-3 | 异步任务 | 分阶段引入Celery | 降低初期复杂度 |
| ADR-4 | Gate引擎 | 策略模式 + 规则类 | 简单直接，易扩展 |
| ADR-5 | 路由算法 | 基于规则评分 | 可解释，可调整 |
| ADR-6 | 工件模板 | Jinja2 + 文件系统 | 复用技术栈，可自定义 |

## 补充架构决策

### 决策 7: API设计模式

**决策：RESTful API + 标准化错误处理**

**API端点：**
```
GET    /thinking/entries              # 列表（支持筛选）
POST   /thinking/entries              # 创建
GET    /thinking/entries/:id          # 详情
PUT    /thinking/entries/:id          # 更新
POST   /thinking/entries/:id/gate     # Gate检查
POST   /thinking/entries/:id/artifacts # 生成工件
POST   /thinking/entries/:id/research  # 调研任务（Phase 3）
GET    /thinking/weekly-review        # 周度评审
```

**错误响应格式：**
```json
{
  "error": "错误描述",
  "status": 400,
  "details": {}
}
```

**理由：** RESTful符合Flask惯例，清晰的资源层次，易于前端集成

---

### 决策 8: 数据流设计

**决策：分层架构 + DTO模式**

**数据流向：**
```
请求 → Routes（验证） → Services（业务逻辑） → Models（数据访问） → DB
                ↓              ↓                ↓
              DTO          Domain            ORM
```

**职责划分：**
- **Routes层**：请求验证、参数解析、响应格式化
- **Services层**：业务逻辑、规则引擎、工作流编排
- **Models层**：数据访问、ORM映射、基础查询
- **DTO**：数据传输对象，避免暴露内部模型

**理由：** 清晰的职责分离，易于测试，符合SOLID原则

---

### 决策 9: 安全策略

**决策：多层安全防护**

**安全措施：**

1. **认证与授权**
   - 复用现有用户系统
   - 装饰器验证登录状态
   - 条目所有权检查

2. **输入验证**
   - Marshmallow schema验证
   - 字段长度限制
   - 类型检查

3. **文件路径安全**
   - secure_filename清理文件名
   - 路径白名单检查
   - 防止路径穿越

4. **SQL注入防护**
   - 使用SQLAlchemy ORM
   - 避免原始SQL拼接
   - 参数化查询

**理由：** 多层防护，纵深防御，符合OWASP最佳实践

---

### 决策 10: 性能优化策略

**决策：数据库优化 + 分页 + 预加载**

**优化措施：**

1. **数据库索引**
   ```sql
   CREATE INDEX idx_entries_user_status ON thinking_entries(user_id, status);
   CREATE INDEX idx_entries_created_at ON thinking_entries(created_at DESC);
   CREATE INDEX idx_entries_user_date ON thinking_entries(user_id, created_at DESC);
   ```

2. **查询优化**
   - 分页加载（每页20条）
   - joinedload预加载关联数据
   - 避免N+1查询问题

3. **缓存策略（Phase 2+）**
   - 条目详情缓存5分钟
   - 路由建议缓存
   - 模板缓存

**性能目标：**
- 列表加载：<1秒（1000条目）
- Gate检查：<2秒
- 工件生成：<5秒

**理由：** 满足NFR4性能要求，索引覆盖核心查询

---

### 决策 11: 测试策略

**决策：分层测试 + 80%覆盖率**

**测试层次：**

1. **单元测试（服务层）**
   - Gate规则引擎
   - 路由决策算法
   - 工件生成逻辑
   - 覆盖率目标：>85%

2. **集成测试（API层）**
   - API端点测试
   - 数据库交互
   - 错误处理
   - 覆盖率目标：>75%

3. **E2E测试（关键流程）**
   - 完整工作流
   - Gate → 工件生成
   - 周度评审流程

**测试工具：**
- pytest（测试框架）
- pytest-flask（Flask集成）
- pytest-cov（覆盖率）
- factory_boy（测试数据）

**理由：** 满足NFR5测试要求，分层测试覆盖不同层次

---

## 技术栈总结

### 核心技术栈

| 层次 | 技术 | 版本 | 用途 |
|-----|------|------|------|
| Web框架 | Flask | 2.3.3 | 现有 |
| ORM | SQLAlchemy | 2.0.35 | 现有 |
| 数据库 | PostgreSQL/MySQL | - | 现有 |
| 模板引擎 | Jinja2 | - | 现有 + 工件模板 |
| 任务队列 | Celery + Redis | - | Phase 3新增 |
| 测试框架 | pytest | - | 新增 |
| 验证 | Marshmallow | - | 新增 |

### 新增依赖（Phase 1-2）

```txt
# requirements.txt 新增
marshmallow==3.20.1        # 数据验证
pytest==7.4.3              # 测试框架
pytest-flask==1.3.0        # Flask测试
pytest-cov==4.1.0          # 覆盖率
factory-boy==3.3.0         # 测试数据
```

### 新增依赖（Phase 3）

```txt
celery==5.3.4              # 任务队列
redis==5.0.1               # 消息代理
```

---

## 部署架构

### Phase 1-2 部署

```
┌─────────────────────────────────────┐
│         Nginx (反向代理)             │
└─────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────┐
│      Flask Application              │
│  (SmartFish + thinking模块)         │
└─────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────┐
│      PostgreSQL/MySQL               │
└─────────────────────────────────────┘
```

### Phase 3 部署

```
┌─────────────────────────────────────┐
│         Nginx (反向代理)             │
└─────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────┐
│      Flask Application              │
└─────────────────────────────────────┘
                 │
        ┌────────┴────────┐
        ▼                 ▼
┌──────────────┐  ┌──────────────┐
│ PostgreSQL   │  │    Redis     │
└──────────────┘  └──────────────┘
                         │
                         ▼
                 ┌──────────────┐
                 │Celery Worker │
                 └──────────────┘
                         │
                         ▼
                 ┌──────────────┐
                 │    Agents    │
                 └──────────────┘
```

**部署要求：**
- 单服务器部署
- 文件系统访问（docs/thinking/）
- 环境变量配置（.env）
- 数据库迁移脚本

---

## 监控与日志

### 日志策略

```python
import logging

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
    handlers=[
        logging.FileHandler('logs/thinking.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger('thinking')

# 使用
logger.info(f'Gate evaluated for entry {entry_id}: {result}')
logger.warning(f'Gate warning for entry {entry_id}: {warning}')
logger.error(f'Failed to generate artifact: {error}')
```

### 监控指标

**关键指标：**
- Gate通过率（目标：60-70%）
- 工件生成成功率（目标：>95%）
- API响应时间（目标：<1秒）
- 错误率（目标：<5%）

**Phase 3额外指标：**
- Agent调用成功率（目标：>90%）
- 任务队列长度
- 任务平均处理时间

---

## 架构演进路径

### Phase 1（4-6周）
- ✅ 基础模块结构
- ✅ Gate机制
- ✅ Quick路由 + tech-spec生成
- ✅ 基础UI

### Phase 2（4-6周）
- ✅ Standard/Enterprise路由
- ✅ 完整工件模板
- ✅ 周度评审
- ✅ 性能优化

### Phase 3（3-4周）
- ✅ Celery + Redis
- ✅ Agent集成
- ✅ 异步任务处理
- ✅ 证据回填

### Phase 4（4-6周）
- ✅ Zero to Sold向导
- ✅ 市场声音采集
- ✅ 高级分析
- ✅ 优化与完善

---

## 风险与缓解

| 风险 | 影响 | 概率 | 缓解措施 |
|-----|------|------|---------|
| Gate过严导致用户放弃 | 高 | 中 | 提供学习模式，可配置严格度 |
| 路由建议不准确 | 中 | 高 | 可解释规则，用户可覆盖 |
| Agent集成不稳定 | 高 | 中 | 完善错误处理，降级方案 |
| 性能不达标 | 中 | 低 | 数据库索引，分页加载 |
| 测试覆盖率不足 | 中 | 中 | 强制覆盖率检查，CI集成 |

---

## 总结

本架构文档定义了SmartFish思考决策系统的完整技术架构，包括：

✅ **11个核心架构决策**（模块组织、数据持久化、异步任务、Gate引擎、路由算法、工件模板、API设计、数据流、安全、性能、测试）

✅ **清晰的技术栈**（复用现有Flask/SQLAlchemy，Phase 3引入Celery/Redis）

✅ **分阶段实施路径**（4个Phase，15-22周）

✅ **完整的代码示例**（每个决策都有实现代码）

✅ **风险识别与缓解**（5个主要风险及应对措施）

**架构特点：**
- 棕地扩展，最小化对现有系统的影响
- 分层清晰，职责明确
- 可测试性强，覆盖率>80%
- 性能优化，满足NFR要求
- 安全可靠，多层防护

**下一步：** 进入Implementation阶段，创建Epics & Stories
