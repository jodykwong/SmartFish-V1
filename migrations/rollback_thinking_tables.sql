-- 回滚 thinking 模块数据库表
-- 按依赖顺序删除

DROP TABLE IF EXISTS research_tasks;
DROP TABLE IF EXISTS artifacts;
DROP TABLE IF EXISTS gate_reviews;
DROP TABLE IF EXISTS thinking_entries;
