-- Epic 6: Zero to Sold 扩展字段迁移
-- 添加日期: 2026-01-22

-- 检查字段是否已存在，避免重复添加
DO $$ 
BEGIN
    -- audience_definition
    IF NOT EXISTS (
        SELECT 1 FROM information_schema.columns 
        WHERE table_name='thinking_entries' AND column_name='audience_definition'
    ) THEN
        ALTER TABLE thinking_entries ADD COLUMN audience_definition TEXT;
    END IF;
    
    -- audience_size_estimate
    IF NOT EXISTS (
        SELECT 1 FROM information_schema.columns 
        WHERE table_name='thinking_entries' AND column_name='audience_size_estimate'
    ) THEN
        ALTER TABLE thinking_entries ADD COLUMN audience_size_estimate TEXT;
    END IF;
    
    -- payability_notes
    IF NOT EXISTS (
        SELECT 1 FROM information_schema.columns 
        WHERE table_name='thinking_entries' AND column_name='payability_notes'
    ) THEN
        ALTER TABLE thinking_entries ADD COLUMN payability_notes TEXT;
    END IF;
    
    -- tribes_watercoolers
    IF NOT EXISTS (
        SELECT 1 FROM information_schema.columns 
        WHERE table_name='thinking_entries' AND column_name='tribes_watercoolers'
    ) THEN
        ALTER TABLE thinking_entries ADD COLUMN tribes_watercoolers TEXT;
    END IF;
    
    -- market_signals
    IF NOT EXISTS (
        SELECT 1 FROM information_schema.columns 
        WHERE table_name='thinking_entries' AND column_name='market_signals'
    ) THEN
        ALTER TABLE thinking_entries ADD COLUMN market_signals TEXT;
    END IF;
    
    -- problem_intensity_score
    IF NOT EXISTS (
        SELECT 1 FROM information_schema.columns 
        WHERE table_name='thinking_entries' AND column_name='problem_intensity_score'
    ) THEN
        ALTER TABLE thinking_entries ADD COLUMN problem_intensity_score INTEGER;
    END IF;
END $$;

-- 添加索引以优化查询
CREATE INDEX IF NOT EXISTS idx_thinking_entries_problem_score 
ON thinking_entries(problem_intensity_score DESC) 
WHERE problem_intensity_score IS NOT NULL;

COMMENT ON COLUMN thinking_entries.audience_definition IS 'Zero to Sold: Niche定义';
COMMENT ON COLUMN thinking_entries.audience_size_estimate IS 'Zero to Sold: 受众规模估算';
COMMENT ON COLUMN thinking_entries.payability_notes IS 'Zero to Sold: 支付能力与意愿';
COMMENT ON COLUMN thinking_entries.tribes_watercoolers IS 'Zero to Sold: 受众聚集地';
COMMENT ON COLUMN thinking_entries.market_signals IS 'Zero to Sold: 市场信号追踪（JSON）';
COMMENT ON COLUMN thinking_entries.problem_intensity_score IS 'Zero to Sold: 问题强度评分（1-25）';
