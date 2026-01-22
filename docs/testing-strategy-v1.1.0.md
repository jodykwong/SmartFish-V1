# SmartFish 测试策略 v1.1.0

## 测试金字塔

```
        /\
       /E2E\      10% - 端到端测试
      /------\
     /  集成  \    30% - 集成测试
    /----------\
   /   单元测试  \  60% - 单元测试
  /--------------\
```

## Phase 1: 关键路径测试 (Week 1)

### 1.1 Thinking System 集成测试
**优先级:** 🔴 CRITICAL (新功能)

```python
# tests/integration/test_thinking_flow.py
def test_complete_thinking_workflow():
    """测试从创建条目到 Gate 评估的完整流程"""
    # 1. 创建条目
    # 2. Gate 评估
    # 3. 路由决策
    # 4. 生成工件
    # 5. 验证数据一致性
```

### 1.2 舆情分析核心流程
**优先级:** 🔴 CRITICAL

```python
# tests/integration/test_sentiment_analysis_flow.py
def test_end_to_end_sentiment_analysis():
    """测试完整舆情分析流程"""
    # 1. 提交分析请求
    # 2. 4 个 Agent 协作
    # 3. 生成报告
    # 4. 验证报告质量
```

### 1.3 数据库事务测试
**优先级:** 🔴 CRITICAL

```python
# tests/integration/test_database_transactions.py
def test_gate_evaluation_rollback():
    """测试 Gate 评估失败时的回滚"""
    # 验证今日修复的事务管理
```

---

## Phase 2: 性能与负载测试 (Week 1-2)

### 2.1 性能基准
**工具:** pytest-benchmark

```python
# tests/performance/test_benchmarks.py
def test_entry_creation_performance(benchmark):
    """条目创建性能 < 100ms"""
    result = benchmark(create_entry, user_id=1, data={...})
    assert result.stats.mean < 0.1

def test_gate_evaluation_performance(benchmark):
    """Gate 评估性能 < 500ms"""
    result = benchmark(evaluate_gate, entry_id=1)
    assert result.stats.mean < 0.5
```

### 2.2 负载测试
**工具:** Locust

```python
# tests/load/locustfile.py
class SmartFishUser(HttpUser):
    @task(3)
    def create_entry(self):
        self.client.post("/thinking/entries", json={...})
    
    @task(1)
    def gate_evaluation(self):
        self.client.post("/thinking/gate/1", json={...})
```

**目标:**
- 100 并发用户
- 响应时间 P95 < 1s
- 错误率 < 0.1%

---

## Phase 3: 安全测试 (Week 1)

### 3.1 输入验证测试
```python
# tests/security/test_input_validation.py
def test_xss_protection():
    """验证 XSS 防护"""
    malicious_input = '<script>alert("xss")</script>'
    # 验证已转义

def test_sql_injection_protection():
    """验证 SQL 注入防护"""
    malicious_input = "1' OR '1'='1"
    # 验证 ORM 保护

def test_unicode_handling():
    """验证 Unicode 处理"""
    # 今日新增的边界测试
```

### 3.2 认证测试
```python
# tests/security/test_authentication.py
def test_unauthorized_access():
    """验证未授权访问返回 401"""
    # 验证今日修复的安全漏洞

def test_session_management():
    """验证会话管理"""
```

---

## Phase 4: 回归测试套件 (Week 2)

### 4.1 自动化回归测试
**CI/CD 集成:**

```yaml
# .github/workflows/test.yml
name: Test Suite
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Run unit tests
        run: pytest tests/unit -v
      - name: Run integration tests
        run: pytest tests/integration -v
      - name: Run security tests
        run: pytest tests/security -v
      - name: Coverage report
        run: pytest --cov=. --cov-report=html
```

---

## 测试覆盖率目标

| 模块 | 当前 | 目标 |
|------|------|------|
| thinking/ | 40% | 85% |
| InsightEngine/ | 未知 | 75% |
| MediaEngine/ | 未知 | 75% |
| QueryEngine/ | 未知 | 75% |
| ReportEngine/ | 未知 | 75% |
| ForumEngine/ | 未知 | 70% |
| app.py | 未知 | 90% |
| **总体** | **40%** | **80%** |

---

## 测试数据管理

### Fixtures
```python
# tests/conftest.py
@pytest.fixture
def test_db():
    """测试数据库"""
    # 使用 SQLite in-memory

@pytest.fixture
def sample_entry():
    """示例条目"""
    return {...}

@pytest.fixture
def authenticated_client():
    """已认证客户端"""
    # 今日修复后的认证逻辑
```

---

## 执行计划

**Day 1-2:** 编写关键路径集成测试
**Day 3:** 性能基准测试
**Day 4:** 安全测试
**Day 5:** CI/CD 集成 + 覆盖率报告

**验收标准:**
- ✅ 所有测试通过
- ✅ 覆盖率 ≥ 80%
- ✅ 性能基准达标
- ✅ 无高危安全漏洞
