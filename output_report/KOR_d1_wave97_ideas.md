# KOR wave97 特征工程 ideas — analyst10 + fundamental86

> S2 合规文档（source=skill）。wave96 未点亮族（intraday_pv_feats/risk59/shortinterest38/mmp_nlp_sentiment）8 条裸信号全 RED 判死（KOR-WAVE96-UNLIT-BARE-SIGNAL-DEAD），wave97 按 KOR 实证金矿转向 analyst 系 + 低拥挤质量评分。

## 1. 数据集理解

### analyst10（IBES 分析师预测明细，297 字段，MATRIX+VECTOR 混合）
- **创新修正计数**（MATRIX）：`*_innovation_score_*`（= innovate_increase − innovate_decrease 的净评分）、`*_innovate_increase/decrease_*`（创新性修正的分析师人数）、`*_normal_increase/decrease_*`（常规修正人数）
- **修正幅度**（MATRIX）：`*_revise_value_*`（共识 delta = 新旧共识差）、`*_revise_ratio_to_consensus_*`（修正/共识比）、`*_revise_ratio_to_close_*`（修正/价格比）
- **标的线**：pre（税前/初步）、sal（销售）、dps（股息）、eps/net（净利）、gps（毛利）、ebi/ebt（息前/税前）、bps/nav/ndt（账面/NAV/净债）、cpx（资本开支）
- **期间**：fy1/fy2（年度）、fq1/fq2（季度）
- **事件明细**（VECTOR）：`*_past_det_*`（分析师 ID、公告时间、estage 修正链年龄、estvalue 快照、indicator 事件类型）——事件级链数据，可做 ts_event_* 持久化
- **KOR 实证**：评级修正族是 KOR 唯一金矿（88lr21xo/A1lb2KpR ACTIVE；ml_factor_proj 2y 金矿确认）。**注意**：PROD 饱和警告（KOR-MLPROJ-RATING-SH-SATURATED），新候选须本地互相关 <0.7

### fundamental86（质量/ESG 评分，8 字段 MATRIX，10 alpha 极低拥挤）
- `fnd86_average_score`：综合评分 decile 1-10
- `fnd86_earnings_score`：盈利质量 pillar（含修正/增长）
- `fnd86_risk_score`：风险 profile（高分=更优）
- `fnd86_relative_valuation_score`：相对估值（高分=更便宜）
- `fnd86_price_momentum_score`：价格动量（注意 KOR 动量判死，不用）
- `fnd86_insider_trading_score`：KOR cov 0.0（无数据，排除）

## 2. 字段解构

| 字段 | 测什么 | 为什么有意义 | 方向 |
|---|---|---|---|
| anl10_analyst_innovation_pre_innovation_score_fy1 | 税前 FY1 创新性修正净方向（增−减人数） | 创新修正=分析师主动偏离共识，信息含量高于常规跟随 | 高=看多 |
| anl10_analyst_innovation_pre_revise_value_fy1 | 税前 FY1 共识修正的绝对幅度（KRW） | 修正幅度=预期盈余变化强度 | 高=看多 |
| anl10_analyst_innovation_pre_revise_ratio_to_close_fy1 | 修正幅度/价格（标准化） | 消除市值量纲，跨股票可比 | 高=看多 |
| anl10_analyst_innovation_sal_innovation_score_fq1 | 销售 Q1 创新修正净方向 | 季度快腿，比年度更及时 | 高=看多 |
| anl10_analyst_innovation_pre_innovate_decrease_fy1 | 税前 FY1 创新性下调人数 | 下调侧单独信号（非对称） | 高=看空 |
| anl10_analyst_innovation_dps_innovation_score_fy1 | 股息创新评分 | 股息修正=管理层信心的滞后指标 | 高=看多 |
| fnd86_earnings_score | 盈利质量 decile | 质量 pillar 综合（修正+增长+质量） | 高=看多 |
| fnd86_risk_score | 风险 profile decile | 低风险溢价 | 高=看多 |

## 3. 候选池（8 条，1-2 字段/条，骨架多样性满足闸6）

| # | 表达式 | 数据集 | 骨架 | 经济机制 |
|---|---|---|---|---|
| 1 | rank(anl10_analyst_innovation_pre_innovation_score_fy1) | analyst10 | rank | 主信号：创新性修正净方向 |
| 2 | rank(anl10_analyst_innovation_pre_revise_ratio_to_close_fy1) | analyst10 | rank | 修正强度（价格标准化） |
| 3 | rank(anl10_analyst_innovation_pre_revise_value_fy1) | analyst10 | rank | 修正绝对幅度 |
| 4 | rank(ts_backfill(anl10_analyst_innovation_sal_innovation_score_fq1, 5)) | analyst10 | rank+ts_backfill | 销售季快腿（回填处理慢更新） |
| 5 | multiply(rank(anl10_analyst_innovation_pre_innovate_decrease_fy1), -1) | analyst10 | multiply 取反 | 下调侧反向（看空信号反转） |
| 6 | rank(group_rank(anl10_analyst_innovation_pre_revise_ratio_to_consensus_fy1, sector)) | analyst10 | group_rank | 行业内相对修正强度 |
| 7 | rank(fnd86_earnings_score) | fundamental86 | rank | 盈利质量评分 |
| 8 | rank(if_else(fnd86_risk_score > 6, fnd86_earnings_score, 0)) | fundamental86 | if_else | 风险过滤后的质量信号 |

## 4. 实现考量
- 全部 MATRIX 字段：直接 rank，无 VECTOR 包裹需求
- 慢变信号：decay=4 天然低换手（KOR 评级修正族实证 tvr ~4% 为亮点）
- 预处理：revise_value 用截面 rank 消除 KRW 量纲；salinnovation_score_fq1 季度更新需 ts_backfill 补缺
- 多样性：rank/group_rank/multiply/if_else/ts_backfill 5 种骨架；2 数据集；字段互异

## 5. 风险与后续
- **PROD 饱和风险（high）**：analyst10 修正族与 88lr21xo/A1lb2KpR 同族 → S4 必须查 prod_correlation，≥0.7 回 Mode B
- fundamental86 属质量风格：KOR-VALUE-QUALITY-SEEDS 判死的是 value/quality **草稿族**，fundamental86 是 decile 评分且 10 alpha 极低竞争，值得一探（1-2 条只占少量槽）
- 若 1/2/3 号强但 PROD 撞墙：Mode B 换腿方向 = 季度快腿（fq1/fq2）或 dps 线

## 6. 建议
- **字段名铁律（本次教训）**：候选表达式必须使用平台 get_datafields 返回的真实 id（analyst10 长名系列 `anl10_analyst_innovation_*`），禁止从描述推断短名；S1 字段白名单已按真实 id 入库
- **PROD 优先**：S3 回测前先对 1/2/3 号主信号腿查平台 prod_corr（同族 88lr21xo），≥0.7 提前换腿，不浪费 8 槽
- **辅助信号配比**：fnd86 两条作辅助腿（低拥挤 decile 评分），与 analyst10 主信号形成质量×修正双金字塔，两数据集策略间相关 <0.4 目标
- 回测后 S4 评审：先 batch_get_alpha_metrics 预筛，再逐个 get_alpha_details 拉全量；归因优先看 2Y sharpe 与 sub-universe
