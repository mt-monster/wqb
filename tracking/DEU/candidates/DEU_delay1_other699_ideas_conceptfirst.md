**Dataset**: other699
**Region**: DEU
**Delay**: 1

# Phased-mode ideas (concept-first, human-authored; source=s2_nested)

> 降级说明：GEM 的 LLM 通道（deepseek-v4-flash @ api.deepseek.com）返回 **402 Insufficient Balance**，
> phased / skeleton 两条生成路径均不可用。本文件由 Agent 按 GEM 概念优先契约人工产出
> （机制 → 具体字段 → Implementation Example），经 `--ideas-file` 注入，由 GEM 确定性渲染 + pregate + 落库。
> 数据语义：other699 = TipRanks 散户（个人投资者）交易事件流；7 个 VECTOR 字段，DEU/TOP500/D1 字段级覆盖率 0.506，
> 平台 users 0–1（零竞争，理论 prod_corr≈0）。稀疏事件流 → 必须 ts_backfill + trade_when 门控 + 平滑。

## Concepts

**Concept**: Retail net-buying pressure as a contrarian flow signal — the cumulative signed share volume transacted by retail accounts, cross-sectionally ranked and inverted.

- **Mechanism**: `sharestraded` is signed (positive = retail buy, negative = retail sell) and event-driven. Aggregating it over a long window converts isolated event noise into a persistent retail positioning measure. Retail flow is a well-documented contrarian indicator at the multi-month horizon: names that retail crowds into subsequently underperform, so the signal is inverted after ranking. Long standard windows (66 backfill / 252 aggregation) are used because the field is sparse and event-dated.
- **Fields**: `oth699_sharestraded`
- **Implementation Example**: `-rank(ts_sum(ts_backfill(vec_avg({sharestraded}), 66), 252))`

**Concept**: Retail net-buying pressure as a contrarian flow signal — a turnover-friendlier smoothed variant.

- **Mechanism**: Same economic mechanism as above; replacing the 252-day running sum with a 22-day mean plus decay-linear smoothing keeps the cross-sectional ordering while sharply cutting turnover, which is the binding constraint for sparse event fields with CONCENTRATED_WEIGHT risk.
- **Fields**: `oth699_sharestraded`
- **Implementation Example**: `-rank(ts_mean(ts_backfill(vec_avg({sharestraded}), 66), 22))`

**Concept**: One-sidedness of retail flow — net signed volume divided by gross absolute volume, isolating direction from sheer activity.

- **Mechanism**: Raw activity is dominated by how many users transacted, not by which way they leaned. Dividing the running sum of signed shares by the running sum of absolute shares yields an imbalance ratio in [-1, 1] that is invariant to event count. This is a ratio-type structural interaction (divide), not a weighted blend, so it does not mix signal families.
- **Fields**: `oth699_sharestraded`
- **Implementation Example**: `rank(divide(ts_sum(vec_avg({sharestraded}), 22), add(ts_sum(abs(vec_avg({sharestraded})), 22), 0.001)))`

**Concept**: Relative position-change intensity — how much the retail holder base added or trimmed, scaled by the size of the pre-existing position.

- **Mechanism**: The difference between post-transaction and pre-transaction share counts is the actual position delta; dividing by the prior holding converts it into a proportional adjustment, so adding 100 shares to a 200-share position outranks the same absolute trade on a 100k-share position. A `+1` denominator guard prevents explosive values on near-zero prior holdings.
- **Fields**: `oth699_newnumofshares`, `oth699_prevnumofshares`
- **Implementation Example**: `rank(divide(subtract(vec_avg({newnumofshares}), vec_avg({prevnumofshares})), add(abs(vec_avg({prevnumofshares})), 1)))`

**Concept**: Relative position-change intensity — decay-smoothed variant to control turnover.

- **Mechanism**: Same mechanism, with `ts_decay_linear` over a standard 22-day window damping the event-day jumps that otherwise push turnover past the 70% platform gate for sparse event datasets.
- **Fields**: `oth699_newnumofshares`, `oth699_prevnumofshares`
- **Implementation Example**: `rank(ts_decay_linear(divide(subtract(vec_avg({newnumofshares}), vec_avg({prevnumofshares})), add(abs(vec_avg({prevnumofshares})), 1)), 22))`

**Concept**: Fresh-event gated retail flow — only act on names with a genuinely recent TipRanks event.

- **Mechanism**: `executiontimestamp` is the event clock. `days_from_last_change` measures staleness of the most recent event; conditioning on it keeps the position alive only while an event is fresh (within a standard 22-day window) and forces the alpha flat elsewhere. This is the mandatory preprocessing for zero-inflated/point-mass sparse event fields (CONCENTRATED_WEIGHT defence) and uses the dormant `days_from_last_change` operator.
- **Fields**: `oth699_executiontimestamp`, `oth699_sharestraded`
- **Implementation Example**: `trade_when(less(days_from_last_change(vec_avg({executiontimestamp})), 22), -rank(ts_mean(vec_avg({sharestraded}), 22)), 0)`

**Concept**: Experience-weighted retail conviction — co-movement between trade size and the user's prior transaction count.

- **Mechanism**: `priortransactionnumber` counts how many transactions that user had already made; a large trade from a highly experienced account carries different information than the same trade from a first-timer. Their rolling time-series correlation is a structural interaction (ts_corr) that reads whether aggressive size is coming from seasoned users, without blending two separate alpha legs.
- **Fields**: `oth699_sharestraded`, `oth699_priortransactionnumber`
- **Implementation Example**: `ts_corr(vec_avg({sharestraded}), vec_avg({priortransactionnumber}), 66)`

**Concept**: Retail breadth acceleration — change in the number of distinct prior trading days represented in the event stream.

- **Mechanism**: `priordistincttradingdays` proxies how broadly and how regularly the retail user base has been trading the name. Its 22-day change is an acceleration reading: a widening participation base marks attention build-up, a collapsing base marks attention exhaustion.
- **Fields**: `oth699_priordistincttradingdays`
- **Implementation Example**: `rank(ts_delta(vec_avg({priordistincttradingdays}), 22))`

**Concept**: Directional conviction versus participation breadth — correlation of the trade-direction balance with the breadth of the user base.

- **Mechanism**: Combining the signed-to-gross trade ratio (direction, event-count invariant) with `priordistincttradingdays` (breadth) via a rolling correlation distinguishes broadly-held directional consensus from a few large accounts moving the signed sum. Structural interaction (ts_corr), single dataset.
- **Fields**: `oth699_sharestraded`, `oth699_priordistincttradingdays`
- **Implementation Example**: `ts_corr(divide(vec_avg({sharestraded}), add(abs(vec_avg({sharestraded})), 0.001)), vec_avg({priordistincttradingdays}), 66)`

**Concept**: Corporate-action-gated flow — suppress flow readings on names whose share counts are distorted by split adjustments.

- **Mechanism**: `aggsplitfactor` records the split adjustment applied to share counts; when it is non-trivial the raw share deltas are mechanically distorted, so the flow reading is untrustworthy. Gating on the adjustment factor keeps the signal only on clean, comparable share counts — an event-conditioning leg rather than a blended signal.
- **Fields**: `oth699_aggsplitfactor`, `oth699_sharestraded`
- **Implementation Example**: `trade_when(greater(vec_avg({aggsplitfactor}), 0), rank(ts_mean(vec_avg({sharestraded}), 66)), 0)`

**Concept**: Time-series standardized retail flow — the slow cumulative flow measured against its own one-year distribution.

- **Mechanism**: Ranking alone is a pure cross-sectional statement; standardizing the 66-day cumulative signed flow by its own trailing 252-day mean and dispersion makes the signal relative to each name's own retail-flow history, so chronically retail-favoured names are not permanently penalised.
- **Fields**: `oth699_sharestraded`
- **Implementation Example**: `rank(ts_zscore(ts_sum(vec_avg({sharestraded}), 66), 252))`

**Concept**: Short-horizon retail flow imbalance — the same imbalance ratio read over a fast standard window.

- **Mechanism**: A 5-day version of the net-to-gross imbalance isolates the most recent retail leaning at the cost of higher noise; it is kept as the fast leg of the two-horizon contrast (slow 22 / fast 5) so the wave carries both a structural and a timing reading.
- **Fields**: `oth699_sharestraded`
- **Implementation Example**: `rank(divide(ts_sum(vec_avg({sharestraded}), 5), add(ts_sum(abs(vec_avg({sharestraded})), 5), 0.001)))`

---

## Auto-appended mandatory sections (GEM 生成端兜底)

## 字段（Fields）

| Field ID | Type | Coverage | Role |
|---|---|---|---|
| oth699_sharestraded | VECTOR | 0.506 | 主信号（有符号份额，买正卖负） |
| oth699_newnumofshares | VECTOR | 0.506 | 主信号（交易后份额） |
| oth699_prevnumofshares | VECTOR | 0.506 | 主信号（交易前份额） |
| oth699_priortransactionnumber | VECTOR | 0.506 | 辅助信号（用户经验计数） |
| oth699_priordistincttradingdays | VECTOR | 0.506 | 辅助信号（参与广度） |
| oth699_executiontimestamp | VECTOR | 0.506 | 条件（事件新鲜度门控） |
| oth699_aggsplitfactor | VECTOR | 0.506 | 条件（公司行为洁净度门控） |

## 特征（Features）

- ts_backfill：稀疏事件字段强制回填（66），防 CONCENTRATED_WEIGHT
- trade_when：零膨胀/点质量字段的时间门控（新鲜度、洁净度）
- ts_sum / ts_mean / ts_decay_linear：事件流累积与平滑（降 turnover）
- rank：截面归一化；divide/subtract：比率型结构交互（禁加权混合）
- ts_corr：跨字段结构交互（方向 × 经验、方向 × 广度）
- ts_zscore / ts_delta / days_from_last_change：时序视角（沉睡算子激活）

## 建议（Implementation Examples）

- concept_1: `-rank(ts_sum(ts_backfill(vec_avg({sharestraded}), 66), 252))`
- concept_2: `-rank(ts_mean(ts_backfill(vec_avg({sharestraded}), 66), 22))`
- concept_3: `rank(divide(ts_sum(vec_avg({sharestraded}), 22), add(ts_sum(abs(vec_avg({sharestraded})), 22), 0.001)))`
- concept_4: `rank(divide(subtract(vec_avg({newnumofshares}), vec_avg({prevnumofshares})), add(abs(vec_avg({prevnumofshares})), 1)))`
- concept_5: `rank(ts_decay_linear(divide(subtract(vec_avg({newnumofshares}), vec_avg({prevnumofshares})), add(abs(vec_avg({prevnumofshares})), 1)), 22))`
- concept_6: `trade_when(less(days_from_last_change(vec_avg({executiontimestamp})), 22), -rank(ts_mean(vec_avg({sharestraded}), 22)), 0)`
- concept_7: `ts_corr(vec_avg({sharestraded}), vec_avg({priortransactionnumber}), 66)`
- concept_8: `rank(ts_delta(vec_avg({priordistincttradingdays}), 22))`
- concept_9: `ts_corr(divide(vec_avg({sharestraded}), add(abs(vec_avg({sharestraded})), 0.001)), vec_avg({priordistincttradingdays}), 66)`
- concept_10: `trade_when(greater(vec_avg({aggsplitfactor}), 0), rank(ts_mean(vec_avg({sharestraded}), 66)), 0)`
- concept_11: `rank(ts_zscore(ts_sum(vec_avg({sharestraded}), 66), 252))`
- concept_12: `rank(divide(ts_sum(vec_avg({sharestraded}), 5), add(ts_sum(abs(vec_avg({sharestraded})), 5), 0.001)))`

## 字段白名单（Field Whitelist）

```
oth699_aggsplitfactor
oth699_executiontimestamp
oth699_newnumofshares
oth699_prevnumofshares
oth699_priordistincttradingdays
oth699_priortransactionnumber
oth699_sharestraded
```
