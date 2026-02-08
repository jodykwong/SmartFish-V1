-- Audience First 数据库表
-- 新增受众簇和证据引用表

-- 受众簇表
CREATE TABLE IF NOT EXISTS audience_clusters (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    entry_id INTEGER NOT NULL,
    cluster_id VARCHAR(50) NOT NULL,
    role VARCHAR(100),
    scenario VARCHAR(200),
    kpi_constraints TEXT,  -- JSON array
    waterholes TEXT,       -- JSON array
    pain_points TEXT,      -- JSON array
    workarounds TEXT,      -- JSON array
    payment_signals TEXT,  -- JSON array
    wtp_score REAL DEFAULT 0.0,
    pain_frequency REAL DEFAULT 0.0,
    moat_score REAL DEFAULT 0.0,
    gtm_score REAL DEFAULT 0.0,
    total_score REAL DEFAULT 0.0,
    evidence_count INTEGER DEFAULT 0,
    confidence REAL DEFAULT 0.0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (entry_id) REFERENCES thinking_entries(id)
);

-- 证据引用表
CREATE TABLE IF NOT EXISTS evidence_refs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    cluster_id INTEGER NOT NULL,
    platform VARCHAR(50),
    url TEXT,
    author VARCHAR(100),
    time VARCHAR(50),
    text TEXT,
    snippet TEXT,
    engagement TEXT,  -- JSON object
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (cluster_id) REFERENCES audience_clusters(id)
);

-- 索引
CREATE INDEX IF NOT EXISTS idx_audience_entry ON audience_clusters(entry_id);
CREATE INDEX IF NOT EXISTS idx_evidence_cluster ON evidence_refs(cluster_id);
