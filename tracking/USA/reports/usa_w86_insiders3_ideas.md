# USA / insiders3 / D1 / TOP3000 机制优先 ideas（wave86：内部人事件结构，8 探针快判死 + 形状配额试点）

**Dataset**: insiders3
**Region**: USA
**Delay**: 1

背景：insiders3 为 untried 新集（USA 零回测），按 8 探针快判死预算执行。死路约束（勿触）：insider_conviction 流量÷存量（insiders1 判死）、buy_sell_ratio 买卖比族（insider_feats 判死）、热字段（users≥50）只做方向验证不入候选——本波全部取 mid 字段（users 10-49）；标识符字段（*_cik/cikmap）与 filing_text_sentiment（sentiment 红榜戒备）排除。**形状配额（v2.3 SOP）**：≥3 shape family、trade_when ≤40%——本波 7 族 / trade_when 0；事件条件化用 `if_else` 状态机 / `ts_arg_max` 时点 / `days_from_last_change` 新鲜度替代 trade_when（ts_event_* 未验证不可用）。cv<0.5 字段 ts_backfill；VECTOR 字段 vec_avg 包裹；占位符置末位字段（模板前缀唯一）。

**Concept**: 减持事件幅度状态：内部人减持幅度相对自身历史升高 → 供给压力状态
- **Implementation Example**: `group_rank(ts_zscore({insd3_xzhou_insider_disposal_raw}, 252), subindustry)`
- **Expected Exposure**: insider_event_activity
- **Rationale**: 单侧减持幅度的状态信号（非买卖比、非流量÷存量）；252 慢窗稳 2Y；候选主字段 insd3_xzhou_insider_disposal_raw

**Concept**: 衍生品行权规模状态：期权行权/衍生品底层规模相对历史升高 → 内部人兑现行为状态
- **Implementation Example**: `group_rank(ts_zscore(vec_avg({insd3_underlyingamount}), 252), subindustry)`
- **Expected Exposure**: derivative_exercise
- **Rationale**: 行权规模是独立于买卖申报的兑现行为轴；候选主字段 insd3_underlyingamount

**Concept**: 减持峰值时点：窗口内减持峰值发生在第几天 → 事件新鲜度几何（TPL-A101-002 形状）
- **Implementation Example**: `group_rank(ts_arg_max({insd3_xzhou_insider_disposal_raw}, 22), subindustry)`
- **Expected Exposure**: insider_event_activity
- **Rationale**: 峰值位置=时点信息（Alpha101 #1 形状）；非窗口网格变体；候选主字段 insd3_xzhou_insider_disposal_raw

**Concept**: 申报频率趋势状态机：减持申报笔数的趋势段顺势、非趋势段反向（TPL-A101-001 形状）
- **Implementation Example**: `if_else(greater(ts_delta(ts_backfill(insd3_form4_snum, 22), 5), 0), ts_delta(ts_backfill({insd3_form4_snum}, 22), 22), multiply(-1, ts_delta(ts_backfill(insd3_form4_snum, 22), 22)))`
- **Expected Exposure**: insider_event_activity
- **Rationale**: 单侧申报频率（非买卖比）的趋势状态机；if_else 替代 trade_when 降同质化；cv 0.55 故 ts_backfill；候选主字段 insd3_form4_snum

**Concept**: 交易新鲜度：距上次内部人交易的天数 → 注意力/信息衰减（TPL-A101-004 形状）
- **Implementation Example**: `group_rank(days_from_last_change(sign(vec_avg({insd3_edgar_insider_shares}))), subindustry)`
- **Expected Exposure**: insider_event_activity
- **Rationale**: 事件流新鲜度几何，稀疏事件的低换手形态；候选主字段 insd3_edgar_insider_shares

**Concept**: 交易×持仓变化共振：交易股数与交易后持股变化共振过高 = 拥挤供给状态 → 反向（TPL-A101-003 形状）
- **Implementation Example**: `scale(-rank(ts_corr(vec_avg(insd3_holdingaftertrade), ts_delta(vec_avg({insd3_edgar_insider_shares}), 5), 22)))`
- **Expected Exposure**: insider_stake_structure
- **Rationale**: ts_corr 共振腿（内生双腿非 add 拼腿）；双腿均 VECTOR（v2 注：原设计用 MATRIX 减持腿，因 fetch_dataset 按类型过滤导致混型模板无法渲染，改纯 VECTOR 组合，分 MATRIX/VECTOR 两批渲染同一波）；候选主字段 insd3_edgar_insider_shares

**Concept**: 内部人/鲸鱼持股差：内部人交易股数与鲸鱼持股的 rank 差 → 持股结构几何（双几何对照的一半）
- **Implementation Example**: `group_rank(subtract(rank(vec_avg(insd3_edgar_insider_shares)), rank(ts_backfill(vec_avg({insd3_whalewisdom_shares}), 22))), subindustry)`
- **Expected Exposure**: insider_stake_structure
- **Rationale**: subtract(rank,rank) 合规价差形态；鲸鱼持股 cv 0.45 故 ts_backfill；候选主字段 insd3_whalewisdom_shares

**Concept**: 内部人持股占比（市值分桶）：内部人持仓市值/证券市值 = 存量占比几何（非 conviction 流量÷存量）
- **Implementation Example**: `group_rank(divide(vec_avg(insd3_holding_holding_value), ts_backfill(vec_avg({insd3_market_value}), 22)), bucket(rank(ts_backfill(vec_avg(insd3_market_value), 22)), range="0,1,0.2"))`
- **Expected Exposure**: insider_stake_structure
- **Rationale**: 存量占比（level 型）与 conviction（flow/stock）构造不同；市值分桶内比较救 sub；候选主字段 insd3_market_value

生成约束：窗口只用 1/5/22/66/252/504（按字段更新频率取最小）；每条 1–2 个字段；禁止 add(A,B) 腿混合与加权混合；cv<0.4-0.5 字段必须 ts_backfill；单边恒正字段不做原始水平多空；禁用幽灵算子（ts_event_* 未验证禁用）；形状配额 ≥3 族（本波 7 族）、trade_when ≤40%（本波 0）；不生成同字段窗口网格变体（8 探针预算）。
