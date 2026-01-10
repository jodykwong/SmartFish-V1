# Anspire 替换方案文档

## 当前配置
- **主搜索引擎**: Anspire AI Search (付费)
- **备用引擎**: Bocha AI Search (也是付费)

## ✅ 已实现：DuckDuckGo 免费替代方案

### 实现状态
代码已完成，DuckDuckGo 作为免费 fallback 自动启用。

### 使用方式
无需任何配置！当 `ANSPIRE_API_KEY` 和 `BOCHA_WEB_SEARCH_API_KEY` 都未设置时，系统自动使用 DuckDuckGo。

### 安装依赖
```bash
pip install duckduckgo-search
```

### 搜索引擎优先级
1. Anspire（如果配置了 `ANSPIRE_API_KEY`）
2. Bocha（如果配置了 `BOCHA_WEB_SEARCH_API_KEY`）
3. DuckDuckGo（免费 fallback，无需配置）

### 功能对比

| 功能 | Anspire/Bocha | DuckDuckGo |
|------|---------------|------------|
| 综合搜索 | ✅ | ✅ |
| 时间范围过滤 | ✅ | ✅ |
| AI 摘要 | ✅ | ❌ |
| 图片搜索 | ✅ | ❌ |
| 模态卡（天气/股票等） | ✅ | ❌ |
| 费用 | 付费 | 免费 |

### 限制说明
- DuckDuckGo 不支持多模态功能（图片、模态卡）
- 搜索结果质量略逊于专业 AI Search
- 添加了 0.5 秒延迟避免反爬限制

---

## 其他免费替代方案（备选）

### 方案 1：Tavily Search（已集成，推荐）⭐
**状态**: 代码中已安装 `tavily-python>=0.3.0`

**优点**:
- ✅ 每月 1000 次免费搜索额度
- ✅ 返回高质量、AI 优化的搜索结果
- ✅ 支持时间范围过滤
- ✅ 专为 AI Agent 设计

**操作步骤**:
1. 访问 https://tavily.com/ 注册账号
2. 获取 API Key（免费层）
3. 在 `.env` 添加 `TAVILY_API_KEY=你的密钥`
4. 修改 `MediaEngine/tools/search.py` 添加 Tavily 适配器

---

### 方案 2：SearXNG（自托管，完全免费）⭐⭐⭐
**优点**:
- ✅ 完全免费，开源
- ✅ 聚合多个搜索引擎结果（Google、Bing、DuckDuckGo等）
- ✅ 无 API Key 限制
- ✅ 可自建实例或使用公共实例

**实现**:
使用公共 SearXNG 实例（如 https://searx.be）或 Docker 自建

---

### 方案 3：Google Custom Search（低成本）
**优点**:
- ✅ 每天 100 次免费搜索
- ✅ Google 官方数据，质量高

**缺点**:
- ⚠️ 需要配置 Google Cloud 项目
- ⚠️ 超出免费额度后按次付费

---

## 推荐方案排序

1. **DuckDuckGo**（✅ 已实现，完全免费，自动 fallback）
2. **Tavily**（质量最高，有免费额度）
3. **SearXNG**（长期方案，需要一点配置）
