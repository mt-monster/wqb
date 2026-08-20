-- Phase 2 增量 schema：registry 实证层 + wave 结果台账
-- 在现有 schema.sql 基础上追加，不改动既有表

-- 15. registry 实证层表（dead_ends / wins / orphans / campaigns 状态）
CREATE TABLE IF NOT EXISTS registry_empirical (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    region VARCHAR(50) NOT NULL,        -- MEA / USA / KOR / ASI
    layer VARCHAR(20) NOT NULL,         -- dead_end / win / orphan / campaign
    entry_id VARCHAR(100),              -- dead_end.id / win.id / orphan alpha_id / campaign dataset
    family VARCHAR(200),                -- dead_end.family / win.what / campaign.dataset
    payload JSON NOT NULL,              -- 完整条目 JSON（reason/rule/salvage/key/date/note 等）
    dead_at VARCHAR(20),                -- dead_end.dead_at / win.date
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(region, layer, entry_id)
);

-- 16. wave 结果台账表（waveXX_results.json 摘要）
CREATE TABLE IF NOT EXISTS wave_results (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    region VARCHAR(50) NOT NULL,
    wave_number INTEGER NOT NULL,
    focus TEXT,                         -- wave 主题
    context TEXT,                       -- 背景
    key_findings JSON,                  -- 关键结论数组
    candidates JSON,                    -- 候选 alpha 摘要（id/sharpe/fit/tvr/status）
    batches JSON,                       -- 批次信息
    verdict TEXT,                       -- 最终裁决
    status VARCHAR(20),                 -- open / closed
    source_file VARCHAR(200),           -- 原 JSON 文件路径（追溯）
    archived INTEGER DEFAULT 0,         -- 是否已归档
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(region, wave_number)
);

-- 17. 跨区教训表（index.json 的 cross_region_lessons）
CREATE TABLE IF NOT EXISTS cross_region_lessons (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    lesson_id VARCHAR(100) NOT NULL UNIQUE,  -- GLB-EMOTION-DEAD 等
    family VARCHAR(200),
    finding TEXT,
    rule TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 索引
CREATE INDEX IF NOT EXISTS idx_registry_empirical_region ON registry_empirical(region);
CREATE INDEX IF NOT EXISTS idx_registry_empirical_layer ON registry_empirical(layer);
CREATE INDEX IF NOT EXISTS idx_wave_results_region ON wave_results(region);
CREATE INDEX IF NOT EXISTS idx_wave_results_status ON wave_results(status);
CREATE INDEX IF NOT EXISTS idx_wave_results_archived ON wave_results(archived);

-- 18. 战役台账通用 kv 表（LedgerStore 的 SQLite 后端）
-- 替代 <region>_d1_campaign_state.json 的任意 kv 结构
CREATE TABLE IF NOT EXISTS ledger_kv (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    region VARCHAR(50) NOT NULL,        -- MEA / USA / KOR / ASI
    key VARCHAR(200) NOT NULL,          -- wave46_verdict / submit_ready / pv1_dead 等
    value JSON NOT NULL,                -- 任意 JSON 值
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(region, key)
);

CREATE INDEX IF NOT EXISTS idx_ledger_kv_region ON ledger_kv(region);
