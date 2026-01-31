# SmartFish MCP + MediaCrawler + FireCrawl 融合重构计划 (v2.0)

> 创建日期: 2026-01-30
> 状态: 🔄 规划中
> 核心策略: 三层混合采集架构 (Tri-Layer Hybrid Architecture)

---

## 一、背景与目标

为解决单一采集方案无法同时满足"快速接入"、"深度挖掘"和"通用扩展"的问题，SmartFish v2.0 将采用**三层混合架构**。融合 FireCrawl 的强大能力，构建从中国本土深入到全球通用的全方位痛点挖掘引擎。

### 核心变更点
1.  **引入 FireCrawl**: 弥补 SmartFish 在"通用网页"和"国际化"方面的短板，提供 LLM-Ready 的高质量数据。
2.  **明确分层**: 将采集层划分为 Quick Win (MCP)、Deep Dive (MediaCrawler) 和 Universal (FireCrawl) 三个战区。
3.  **统一路由**: 升级 `DataSourceRouter` 以智能分发请求到最优采集器。

---

## 二、SmartFish 三层混合架构图 (v2.2)

```
═══════════════════════════════════════════════════════════════════════════
                    SmartFish 三层混合采集架构
═══════════════════════════════════════════════════════════════════════════

   ┌───────────────────────────────┐
   │        DataSourceRouter       │ ← 智能路由中心
   │    (MediaEngine/tools/router) │
   └───────────────┬───────────────┘
                   │
    ┌──────────────┼──────────────────────────────┐
    ▼              ▼                              ▼
┌─────────┐   ┌─────────┐                    ┌─────────┐
│  Tier 1 │   │  Tier 2 │                    │  Tier 3 │
│   MCP   │   │MediaCrawler                  │FireCrawl│
│ (快速层)│   │ (深度层)│                    │ (通用层)│
└────┬────┘   └────┬────┘                    └────┬────┘
     │             │                              │
     │             │                              │
┌────▼────┐   ┌────▼────┐                    ┌────▼────┐
│微博(Weibo)│   │知乎(Zhihu)│                    │通用网页 │
│抖音(Douyin)│   │B站(Bilibili)                   │PDF文档  │
└────┬────┘   └────┬────┘                    │国际社媒 │
     │             │                         │(Reddit) │
     │             │                         └────┬────┘
     │             │                              │
     └─────────────┼──────────────────────────────┘
                   ▼
          ┌───────────────────┐
          │  统一数据标准化层 │
          │ (Normalize Data)  │
          └────────┬──────────┘
                   ▼
          ┌───────────────────┐
          │ BMAD 被动信号挖掘 │
          │ (验证/评分/报告)  │
          └───────────────────┘
```

---

## 三、采集层分工详解

| 层级 | 工具 | 目标平台 | 优势 | 适用场景 |
|------|------|----------|------|----------|
| **Tier 1** | **MCP** | 微博, 抖音, 小红书 | ✅ 官方/活跃维护<br>✅ 配置简单<br>✅ 速度快 | **快速验证**：需要立刻拿到社交媒体热点和评论概览。 |
| **Tier 2** | **MediaCrawler** | 知乎, B站 | ✅ 深度爬取<br>✅ 抗反爬强<br>✅ 社区支持好 | **深度挖掘**：需要获取长文章、复杂评论区、视频弹幕。 |
| **Tier 3** | **FireCrawl** | 通用网页, PDF, Reddit, Twitter | ✅ **LLM-Ready Markdown**<br>✅ 结构化抽取 (Schema)<br>✅ 国际化支持 | **广度扩展**：分析竞品官网、行业报告(PDF)、海外用户声音。 |

---

## 四、实施路线图 (Roadmap)

### Phase 1: 夯实 MCP 基础 (进行中)
*目标：确保核心的微博、抖音、小红书 MCP 稳定运行。*
- [x] 代码迁移至 `MediaEngine/tools/mcp/`
- [ ] 配置微博 Cookie 和环境
- [ ] 验证数据连通性

### Phase 2: 集成 FireCrawl 能力 (新增)
*目标：引入通用网页采集能力，扩展数据边界。*
- [ ] **API 集成**: 在 `MediaEngine/tools/firecrawl/` 封装 FireCrawl API 客户端。
- [ ] **路由适配**: 更新 `DataSourceRouter`，将非社媒 URL 请求转发给 FireCrawl。
- [ ] **PDF 支持**: 增加对上传/链接 PDF 文件的解析处理。
- [ ] **自托管评估**: 决定使用 SaaS 版还是 Docker 本地部署版。

### Phase 3: 攻克 MediaCrawler (待定)
*目标：啃下知乎和 B 站这块硬骨头。*
- [ ] 集成 MediaCrawler 核心代码
- [ ] 开发 Python 调用适配器
- [ ] 统一数据格式

---

## 五、关键技术规范

### 1. 统一数据结构
无论数据来自 MCP、MediaCrawler 还是 FireCrawl，最终必须转换为统一格式供 BMAD 挖掘：

```python
class NormalizedContent:
    source: str          # e.g., "weibo", "firecrawl-web"
    url: str
    raw_content: str     # Markdown or Text
    author: str
    publish_time: int
    meta: Dict           # 原始元数据 (e.g. 转发数, PDF页码)
```

### 2. 路由逻辑 (Router Logic)
```python
def route_request(url_or_query):
    if is_weibo_url(url): return MCP_Weibo
    if is_douyin_url(url): return MCP_Douyin
    if is_zhihu_url(url): return MediaCrawler_Zhihu
    if is_pdf(url) or is_general_web(url): return FireCrawl
    return Default_Search_MCP
```

---

## 六、验证与测试

### FireCrawl 专项测试
```bash
# 测试通用网页抓取
python -m pytest tests/test_firecrawl_web.py

# 测试 PDF 解析
python -m pytest tests/test_firecrawl_pdf.py
```

### 验收标准
1.  **混合查询**: 同时输入微博链接和竞品官网链接，SmartFish 能分别调用 MCP 和 FireCrawl 并合并报告。
2.  **PDF解析**: 上传一份行业报告 PDF，系统能提取文本并挖掘出痛点信号。
