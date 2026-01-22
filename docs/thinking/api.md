# Thinking System API 文档

## 认证
所有 API 需要在 session 中设置 `user_id`，否则返回 401。

## 端点

### GET /thinking/entries
列出用户的思考条目

**参数:**
- `status` (可选): 过滤状态
- `page` (可选): 页码，默认 1

**响应:** 200
```json
{
  "entries": [...],
  "total": 10,
  "pages": 2,
  "current_page": 1
}
```

### POST /thinking/entries
创建新条目

**请求体:**
```json
{
  "title": "标题 (必填, 最大255字符)",
  "signal": "信号",
  "problem": "问题描述"
}
```

**响应:** 201
```json
{
  "id": 1,
  "title": "标题",
  "status": "想法",
  ...
}
```

**错误:**
- 400: 标题为空或过长
- 401: 未授权

### GET /thinking/entries/<id>
获取单个条目

**响应:** 200 或 404

### POST /thinking/gate/<entry_id>
执行 Gate 评估

**请求体:**
```json
{
  "inputs": ["answer1", "answer2", "answer3", "answer4"]
}
```

**响应:** 200
```json
{
  "decision": "pass|fail",
  "fail_level": 2,
  "fail_reason": "原因",
  "results": [...],
  "warnings": [...]
}
```
