-- BRAIN 挖掘战役数据库架构设计
-- 用于替代 JSON/CSV 文件存储

-- 1. 区域配置表
CREATE TABLE regions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(50) NOT NULL UNIQUE,  -- MEA, USA, KOR, etc.
    universe_legal JSON,               -- 合法 universe 档位
    delay_legal JSON,                  -- 合法 delay 档位
    neutralization_default VARCHAR(50), -- 默认中性化
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2. 数据集表
CREATE TABLE datasets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(100) NOT NULL,        -- model25, model31, etc.
    region_id INTEGER NOT NULL,
    category VARCHAR(50),              -- model, fundamental, analyst, etc.
    field_count INTEGER,
    coverage DECIMAL(5,4),
    alpha_count INTEGER,
    value_score DECIMAL(3,1),
    pyramid_multiplier DECIMAL(3,1),
    tier VARCHAR(10),                  -- tier1, tier2, excluded
    status VARCHAR(20),                -- untried, in_progress, exhausted
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(name, region_id)
);

-- 3. 字段表
CREATE TABLE fields (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    dataset_id INTEGER NOT NULL,
    field_name VARCHAR(200) NOT NULL,
    field_type VARCHAR(20),            -- MATRIX, VECTOR
    coverage DECIMAL(5,4),
    user_count INTEGER,
    alpha_count INTEGER,
    description TEXT,
    field_group VARCHAR(50),           -- growth, quality, valuation, etc.
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(dataset_id, field_name)
);

-- 4. 表达式表
CREATE TABLE expressions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    wave_id INTEGER NOT NULL,
    expression TEXT NOT NULL,
    fingerprint VARCHAR(100),
    status VARCHAR(20) DEFAULT 'pending',
    alpha_id VARCHAR(50),
    sharpe DECIMAL(8,4),
    fitness DECIMAL(8,4),
    margin DECIMAL(10,6),
    turnover DECIMAL(8,4),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(wave_id, expression)
);

-- 5. 回测结果表
CREATE TABLE backtest_results (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    expression_id INTEGER NOT NULL,
    alpha_id VARCHAR(50),              -- 平台返回的 alpha ID
    status VARCHAR(20),                -- COMPLETE, ERROR, FAILED, etc.
    sharpe DECIMAL(8,4),
    fitness DECIMAL(8,4),
    turnover DECIMAL(8,4),
    margin DECIMAL(10,6),
    returns DECIMAL(8,4),
    drawdown DECIMAL(8,4),
    two_year_sharpe DECIMAL(8,4),
    sub_universe_sharpe DECIMAL(8,4),
    long_count INTEGER,
    short_count INTEGER,
    pnl BIGINT,
    book_size BIGINT,
    concentrated_weight DECIMAL(8,4),
    ra_failed_count INTEGER,
    ra_failed_checks JSON,
    ppa_failed_count INTEGER,
    ppa_failed_checks JSON,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (expression_id) REFERENCES expressions(id)
);

-- 6. 多样性评估表
CREATE TABLE diversity_evaluations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    dataset_id INTEGER NOT NULL,
    region_id INTEGER NOT NULL,
    wave VARCHAR(20),
    total_expressions INTEGER,
    structural_metrics JSON,
    ppac_metrics JSON,
    avg_ppac DECIMAL(5,4),
    max_ppac DECIMAL(5,4),
    low_ppac_ratio DECIMAL(5,4),
    recommendation VARCHAR(50),        -- continue_extraction, enter_multi_dataset, adjust_strategy
    quality_score DECIMAL(5,4),
    estimated_high_quality_alphas INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (dataset_id) REFERENCES datasets(id),
    FOREIGN KEY (region_id) REFERENCES regions(id)
);

-- 7. 提交记录表
CREATE TABLE submissions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    expression_id INTEGER NOT NULL,
    alpha_id VARCHAR(50),
    status VARCHAR(20),                -- SUBMITTED, ACTIVE, FAILED, etc.
    submission_date TIMESTAMP,
    prod_correlation DECIMAL(5,4),
    self_correlation DECIMAL(5,4),
    pyramid_multiplier DECIMAL(3,1),
    tags JSON,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (expression_id) REFERENCES expressions(id)
);

-- 8. 战役状态表
CREATE TABLE campaign_states (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    region_id INTEGER NOT NULL,
    dataset_id INTEGER NOT NULL,
    status VARCHAR(20),                -- untried, in_progress, exhausted
    current_wave VARCHAR(20),
    total_waves INTEGER,
    successful_alphas INTEGER,
    submitted_alphas INTEGER,
    last_iteration_date TIMESTAMP,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (region_id) REFERENCES regions(id),
    FOREIGN KEY (dataset_id) REFERENCES datasets(id)
);

-- 9. 算子表
CREATE TABLE operators (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(100) NOT NULL UNIQUE,
    category VARCHAR(50),              -- ts, cross-sectional, group, etc.
    scope VARCHAR(20),                 -- REGULAR, COMBO, SELECTION
    parameters JSON,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 10. 表达式算子关联表
CREATE TABLE expression_operators (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    expression_id INTEGER NOT NULL,
    operator_id INTEGER NOT NULL,
    usage_count INTEGER DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (expression_id) REFERENCES expressions(id),
    FOREIGN KEY (operator_id) REFERENCES operators(id)
);

-- 11. 多样性潜力表
CREATE TABLE diversity_potential (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    region_id INTEGER NOT NULL,
    dataset_id INTEGER NOT NULL,
    diversity_score DECIMAL(5,4),
    recommended_rounds INTEGER,
    field_categories JSON,
    operator_buckets JSON,
    parameter_space JSON,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(region_id, dataset_id)
);

-- 12. 战役状态表（简化版）
CREATE TABLE campaign_state (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    region_id INTEGER NOT NULL,
    current_wave VARCHAR(20),
    submit_ready_count INTEGER DEFAULT 0,
    target_count INTEGER DEFAULT 10,
    status VARCHAR(20) DEFAULT 'active',
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(region_id)
);

-- 13. 波次表
CREATE TABLE waves (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    region_id INTEGER NOT NULL,
    wave_number VARCHAR(20) NOT NULL,
    dataset_id INTEGER,
    expression_count INTEGER DEFAULT 0,
    status VARCHAR(20) DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(region_id, wave_number)
);

-- 14. Alpha 表
CREATE TABLE alphas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    alpha_id VARCHAR(50) NOT NULL UNIQUE,
    expression TEXT NOT NULL,
    region_id INTEGER NOT NULL,
    dataset_id INTEGER NOT NULL,
    universe VARCHAR(20),
    delay INTEGER,
    neutralization VARCHAR(50),
    sharpe DECIMAL(8,4),
    fitness DECIMAL(8,4),
    margin DECIMAL(10,6),
    turnover DECIMAL(8,4),
    two_year_sharpe DECIMAL(8,4),
    status VARCHAR(20) DEFAULT 'UNSUBMITTED',
    prod_correlation DECIMAL(5,4),
    self_correlation DECIMAL(5,4),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 索引
CREATE INDEX idx_datasets_region ON datasets(region_id);
CREATE INDEX idx_datasets_tier ON datasets(tier);
CREATE INDEX idx_fields_dataset ON fields(dataset_id);
CREATE INDEX idx_fields_group ON fields(field_group);
CREATE INDEX idx_expressions_wave ON expressions(wave_id);
CREATE INDEX idx_expressions_status ON expressions(status);
CREATE INDEX idx_backtest_results_expression ON backtest_results(expression_id);
CREATE INDEX idx_backtest_results_status ON backtest_results(status);
CREATE INDEX idx_backtest_results_sharpe ON backtest_results(sharpe);
CREATE INDEX idx_diversity_evaluations_dataset ON diversity_evaluations(dataset_id);
CREATE INDEX idx_submissions_expression ON submissions(expression_id);
CREATE INDEX idx_submissions_status ON submissions(status);
CREATE INDEX idx_campaign_states_region ON campaign_states(region_id);
CREATE INDEX idx_campaign_states_dataset ON campaign_states(dataset_id);
CREATE INDEX idx_expression_operators_expression ON expression_operators(expression_id);
CREATE INDEX idx_expression_operators_operator ON expression_operators(operator_id);
CREATE INDEX idx_waves_region ON waves(region_id);
CREATE INDEX idx_waves_number ON waves(wave_number);
CREATE INDEX idx_alphas_region ON alphas(region_id);
CREATE INDEX idx_alphas_dataset ON alphas(dataset_id);
CREATE INDEX idx_alphas_status ON alphas(status);
CREATE INDEX idx_diversity_potential_region ON diversity_potential(region_id);
CREATE INDEX idx_diversity_potential_dataset ON diversity_potential(dataset_id);
CREATE INDEX idx_campaign_state_region ON campaign_state(region_id);

-- 15. 跨区域经验表
CREATE TABLE cross_region_lessons (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    lesson_id VARCHAR(100) NOT NULL UNIQUE,  -- GLB-EMOTION-DEAD 等
    family VARCHAR(200),
    finding TEXT,
    rule TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 16. 账本键值表
CREATE TABLE ledger_kv (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    region VARCHAR(50) NOT NULL,
    key VARCHAR(200) NOT NULL,
    value JSON NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(region, key)
);

-- 17. 实证注册表
CREATE TABLE registry_empirical (
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

-- 18. 波次结果表
CREATE TABLE wave_results (
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

-- 索引
CREATE INDEX idx_ledger_kv_region ON ledger_kv(region);
CREATE INDEX idx_registry_empirical_region ON registry_empirical(region);
CREATE INDEX idx_registry_empirical_layer ON registry_empirical(layer);
CREATE INDEX idx_wave_results_region ON wave_results(region);
CREATE INDEX idx_wave_results_status ON wave_results(status);
CREATE INDEX idx_wave_results_archived ON wave_results(archived);
