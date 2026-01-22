-- 创建thinking_entries表
CREATE TABLE IF NOT EXISTS thinking_entries (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    title VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(50) NOT NULL DEFAULT '想法',
    tags TEXT,
    routing_type VARCHAR(50),
    
    -- 核心字段
    signal TEXT,
    target_segment TEXT,
    problem TEXT,
    hypothesis TEXT,
    evidence_needed TEXT,
    mva TEXT,
    success_metric TEXT,
    constraints TEXT,
    dependencies TEXT,
    
    -- Zero to Sold扩展字段
    audience_definition TEXT,
    audience_size_estimate TEXT,
    payability_notes TEXT,
    tribes_watercoolers TEXT,
    market_signals TEXT,
    problem_intensity_score INTEGER
);

-- 创建索引
CREATE INDEX IF NOT EXISTS idx_entries_user_status ON thinking_entries(user_id, status);
CREATE INDEX IF NOT EXISTS idx_entries_created_at ON thinking_entries(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_entries_user_date ON thinking_entries(user_id, created_at DESC);


-- 创建gate_reviews表
CREATE TABLE IF NOT EXISTS gate_reviews (
    id SERIAL PRIMARY KEY,
    entry_id INTEGER NOT NULL REFERENCES thinking_entries(id),
    reviewed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- 四层过滤结果
    human_dependency_pass BOOLEAN,
    value_self_evident_pass BOOLEAN,
    feedback_clean_pass BOOLEAN,
    role_cost_pass BOOLEAN,
    
    -- 决策结果
    decision VARCHAR(20) NOT NULL,
    fail_level VARCHAR(50),
    fail_reason TEXT,
    notes TEXT,
    version INTEGER DEFAULT 1
);

-- 创建索引
CREATE INDEX IF NOT EXISTS idx_gate_entry ON gate_reviews(entry_id);
CREATE INDEX IF NOT EXISTS idx_gate_decision ON gate_reviews(decision);


-- 创建artifacts表
CREATE TABLE IF NOT EXISTS artifacts (
    id SERIAL PRIMARY KEY,
    entry_id INTEGER NOT NULL REFERENCES thinking_entries(id),
    type VARCHAR(50) NOT NULL,
    path TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    checksum VARCHAR(64)
);

-- 创建索引
CREATE INDEX IF NOT EXISTS idx_artifacts_entry ON artifacts(entry_id);
CREATE INDEX IF NOT EXISTS idx_artifacts_type ON artifacts(type);


-- 创建research_tasks表
CREATE TABLE IF NOT EXISTS research_tasks (
    id SERIAL PRIMARY KEY,
    entry_id INTEGER NOT NULL REFERENCES thinking_entries(id),
    engine VARCHAR(50) NOT NULL,
    task_type VARCHAR(50),
    query TEXT NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'pending',
    result_path TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP,
    error_message TEXT,
    retry_count INTEGER DEFAULT 0
);

-- 创建索引
CREATE INDEX IF NOT EXISTS idx_research_entry ON research_tasks(entry_id);
CREATE INDEX IF NOT EXISTS idx_research_status ON research_tasks(status);
CREATE INDEX IF NOT EXISTS idx_research_engine ON research_tasks(engine);
CREATE INDEX IF NOT EXISTS idx_research_entry_status ON research_tasks(entry_id, status);
