# intraday_pv_feats 字段画像与批次 23 预登记（USA / TOP3000 / D1）

as_of 2026-10-22　｜　平台：USA　｜　delay 1　｜　universe TOP3000
数据来源：`GET /data-fields?dataset.id=intraday_pv_feats&region=USA&delay=1&universe=TOP3000`（ds=389），全量 582 字段落盘 `logs/_tmp_ofi_fields.json` 同批临时件（一次性中间件，不入库）。
配套阅读：[`_usa-field-profile-playbook-20261018.md`](_usa-field-profile-playbook-20261018.md)（字段八问与 `risk_neutralized_sharpe` 判死口径）。

## 0. 数据集元信息

| 项 | 值 |
|---|---|
| 数据集 id | `intraday_pv_feats`（**PV 类别，未点亮塔**） |
| 字段数 | **582（全部 MATRIX，无 VECTOR）** ⇒ 不需要 `vec_*` 聚合，也不会有「vector 字段漏聚合 ⇒ 整批 ERROR」的连坐风险 |
| 覆盖率 | 区间 **0.4711 – 0.9996**；主力族（`mean_*` / `corr_*`）普遍 0.9993–0.9996，尾部稀疏件（`momentum3` / `slippage`）才落到 0.47–0.8 ⇒ 主线无需 `ts_backfill` 兜底 |
| 拥挤度 | 数据集级 aC **1524** / uC **487**（字段级 aC 之和 2608，多字段 alpha 重复计数）；**分布极度不均**：aC=0 的字段 **189 个**，aC≥10 的仅 **70 个** |
| valueScore / multiplier | 2 / 1.1（>1，平台按中高价值数据集计权） |
| 语义 | 日内价格－成交量微结构特征：把每个交易日切成交割前后（`pre_close`）/ 开盘后（`post_open`）两个会话窗，用多个价格基准（`last_trade` / `high` / `low` / `vwap` / `bid` / `ask` / `twap`）统计**区间收益**（`mean_*_return_*`）、**价量相关**（`corr_*_with_volume`）、**动量/偏度/峰度**（`momentum*` / `skew` / `kurtosis`）、**买卖价差与滑点**（`ask` / `bid` / `slippage` / `num_*`） |
| 是否点亮 | 未点亮（USA/D1 本季亮塔 = model 4 / analyst 1 / earnings 1；PV 塔 0） ⇒ **在此交付可点亮 PV 塔** |
| 入选理由 | ① 交付目标 5/10，剩余缺口需要**新机制**而非在老族上磨参数；② 本集是 PV 类别里唯一同时满足「高覆盖（0.999）＋大量 aC=0 字段（189）＋未点亮塔」的数据集；③ 会话切分（`pre_close` vs `post_open`）天然提供**日内时序对照轴**，可以做「同一字段、两套会话」的机制检验，而不是同族扫参数 |

## 1. 字段清单（582/582，全 MATRIX）

### 1.1 结构矩阵

- **前缀族**（按字段 id 首段）：`mean` 129 · `corr` 107 · `max` 52 · `min` 52 · `momentum` 46 · `momentum2` 36 · `std` 36 · `avg` 32 · `skew` 20 · `vwap` 9 · `ask` 8 · `bid` 8 · `kurtosis` 8 · `momentum3` 8 · `high` 6 · `last` 6 · `low` 6 · `momentum1` 5 · `num` 4 · `slippage` 2。
- **会话后缀**：`post_open` **84 个** / `pre_close` **14 个**。**这个不对称是本集最重要的事实** —— 尾盘（`pre_close`）字段只有 14 个，却容纳了本集全部可用的高信号候选；开盘后字段数量多但 aC 普遍 ≤ 6（拥挤度与可用度双低，见 §3 的对照臂）。
- **`corr_*` 族（107 个）**：prices/volume 的日内相关系数，值域天然 [−1, 1]（有界）⇒ 任何 zscore 壳层都不会造出极端权重。头部三个 `corr_bid_price_with_volume`（aC 88）、`corr_last_trade_price_with_volume`（aC **88** / uC 51）、`corr_ask_price_with_volume`（aC 86）是本集**最拥挤**的字段。

### 1.2 主力家族：`mean_*_return_<T>m_<session>`（24 个，覆盖 0.9993–0.9996）

| 字段 id | aC | 备注 |
|---|---|---|
| `mean_last_trade_price_return_60m_pre_close_2` | **53** | 尾盘 60 分钟成交价区间收益（族内最拥挤） |
| `mean_high_price_return_30m_pre_close_2` | **40** | 尾盘 30 分钟最高价区间收益（**交付候选 `wpZJPRql` 的字段**） |
| `mean_last_trade_price_return_30m_pre_close_2` | 37 | |
| `mean_high_price_return_60m_pre_close` | 36 | **无 `_2` 后缀**，与 30m 版本命名不一致，别当同一口径 |
| `mean_vwap_return_30m_pre_close_2` | 30 | |
| `mean_bid_price_return_60m_pre_close_2` | 28 | |
| `mean_vwap_return_60m_pre_close_2` | 20 | |
| `mean_ask_price_return_30m_pre_close_2` | 15 | |
| `mean_ask_price_return_60m_pre_close_2` | 15 | |
| `mean_bid_price_return_30m_pre_close_2` | 9 | |
| `mean_low_price_return_30m_pre_close_2` | 3 | 冷门（族内最低） |
| `mean_low_price_return_60m_pre_close_2` | 2 | 冷门 |
| 其余 12 个 `post_open` 变体 | ≤ 6 | 开盘后同构字段，**拥挤度接近白纸** |

族共性：`mean_*_return_*` 是**无量纲区间收益**，横截面可直比，不需要再除以价格；但**分布重尾**（尾盘 30 分钟最高价相对开盘的百分比变化，在极端行情日可达数十个百分点），这是 §4 CW 归因的根因。

### 1.3 冷门区（189 个 aC=0）

`momentum1/2/3`、`kurtosis`、`slippage`、多数 `num_*` 与 `post_open` 组合字段的 aC 都是 0 或个位数。**冷门 ≠ 可用**：这批字段多属比值/计数型（`num_*`）或高阶矩（`kurtosis`），在 USA 这种最深市场里，高阶矩通常被风格 beta 吸收（`risk_neutralized_sharpe` < 0.3，见 playbook 判死口径），**不作为本批主信号**，只在后续需要「同族正交腿」时再取。

## 2. 数据集切换理由（对齐「不得频繁切换数据集」约束）

前序已在 fnd67 / fnd93 / analyst_factor_signals / order_flow_imb / news_transformer_scores 上穷尽，结论分别是全灭 / 判死 / 交付 2 颗后判死 / 12 臂全灭（max S 0.73）/ 8 臂低产。**Fundamental 类别在 USA/D1 的「未判死 × 可开采」库存已归零**，继续停留等于零产出；PV 类别是本季唯一还有未点亮塔 × 高覆盖 × 大量 aC=0 字段的组合 ⇒ 切换有据，且只切这一次。

## 3. 本数据集已产出的 9 颗 alpha（全部 UNSUBMITTED，全部栽在 RA 闸上）

统一设置：USA / TOP3000 / D1 / SUBINDUSTRY / decay 6–10 / truncation 0.08 / 窗口 2014-01-01→2023-12-31（MCP 路径固定，见 AGENTS 记录的 MCP 无 startDate/endDate 事实）。

| id | 核心表达式（缩写） | S | F | 2Y | SUB | TO | RET | rns | RA 失败项 |
|---|---|---|---|---|---|---|---|---|---|
| `wpZJPRql` | `-group_zscore(ts_decay_linear(mean_high_price_return_30m_pre_close_2,5), country)` | 1.66 | **1.05** | 2.00 | 1.15 | .3343 | **13.4%** | 1.13 | **CW only** |
| `levR9Vq7` | 同上，group 改 `industry` | 1.84 | 0.95 | 1.70 | 1.14 | .3304 | 8.82% | 1.36 | F + CW |
| `9qjAmw1o` | `corr_last_trade_price_with_volume` × `industry` | 1.94 | 0.86 | 1.71 | 1.01 | .3551 | 6.99% | 2.14 | F |
| `MPa5ZpRa` | 同字段 × `country` | 1.92 | 0.87 | — | — | — | — | — | F |
| `blbodl6Z` | `-group_rank(ts_decay_linear(corr…,5), industry)` | 1.72 | 0.74 | 1.67 | 0.90 | .3066 | 5.69% | 1.80 | F |
| `mLmrVLo2` | `signed_power(subtract(0.5, rank(ts_decay_linear(corr…,5))), 0.5)` | 1.72 | 0.73 | 1.63 | 0.94 | .3135 | 5.60% | 1.82 | F |
| `9qj9WAO9` | 同 `mLmrVLo2`，`rank`→`group_rank(...,industry)` | 1.69 | 0.74 | 1.69 | 0.91 | .2827 | 5.44% | 1.67 | F |
| `58zLgq1J` | `trade_when(volume 门控, signed_power(…), exit)` | 2.35 | 0.78 | 1.31* | 1.26 | **.6984** | 7.72% | **2.47** | F + IS_LADDER_SHARPE |
| `9qE7WOxr` | 尾盘族另一变体（详见 transcript） | — | — | — | — | — | — | — | 未过闸 |

\* `58zLgq1J` 的 2Y 是 ladder 口径读数，与其它行的日历 2Y 不完全同尺。

**读表结论**：
1. **`corr_*` 分支（6 颗）集体死在 Fitness（0.73–0.87）**，S 全部 ≥ 1.69。原因不是信号弱，而是 RET（5.4%–7.0%）撑不起 `F = S·sqrt(RET/max(TO,0.125))`：TO 0.28–0.36 时 F ≈ S·sqrt(RET/TO)，把 RET 抬上去的唯一合法途径是**降 TO 或抬 RET**，而 `corr_*` 的 RET 已被 SUBINDUSTRY 中性化削平。
2. **尾盘收益族（2 颗）**：`wpZJPRql` 是**唯一 F 过线（1.05）的 alpha**，但栽在 CW；`levR9Vq7` 换了 group 轴就同时丢 F 与 CW ⇒ 说明 **CW 不是 group 轴的问题**（见 §4）。
3. `58zLgq1J` 用 `trade_when` 门控把 TO 推到 **0.6984**（贴着 0.70 上限），rns 2.47 是全场最高 —— 门控确实筛出了更纯的信号，但换手爆炸让 F 与 ladder 双杀。

## 4. CONCENTRATED_WEIGHT 归因（**先归因再推进**，不盲扫）

平台行为：`CONCENTRATED_WEIGHT` **计入 `ra_failed_checks`**（RA 失败项），但在 `warning` 数组里**不给数值、不给阈值**，只有项名。

三条机械事实把根因锁死：

| 事实 | 证据 | 排除的假设 |
|---|---|---|
| **country 分组在美国退化为全市场** | `config.REGION_COUNTRY_SCOPE` 单一国家 ⇒ `group_zscore(x, country)` ≡ `zscore(x)` | 「换个分组就收敛权重」不成立 |
| **industry 分组同样 CW** | `levR9Vq7`（同字段 + industry）`ra_failed_checks = ["LOW_FITNESS","CONCENTRATED_WEIGHT"]` | 「细分行业就够了」不成立 |
| **`corr_*` 字段从不 CW** | 6 颗 corr alpha 的失败项里只有 F（无 CW） | 「壳层算子写错了」不成立 |

⇒ **CW 是字段值域属性**：`mean_*_return_*` 是无界重尾（尾盘 30 分钟收益可达数十 %），`group_zscore` / `zscore` 会把它**线性放大**到极端权重；`corr_*` 天然落在 [−1, 1]，同一壳层就不会集中。

**唯一可用于破 CW 的算子族 = 有界化**：`rank` / `quantile` / `group_rank` / `winsorize(..., std=)`。其中 `rank` 与 `group_rank` 完全有界（⇒ CW 必解），`winsorize` 只截尾（权重仍有界但保留重尾中心），`quantile` 分桶（有界且保序）。

**代价预判（这一条决定下一批怎么发）**：`wpZJPRql`（有尾，RET 13.4% / F 1.05）vs `levR9Vq7`（无尾，RET 8.82% / F 0.95）—— **尾部收益贡献了约 4.6pp 的 RET**。有界化会削掉一部分尾部 ⇒ F 大概率掉到 0.85–0.95 区间。所以**破 CW 与保 F 是一对冲突目标**，下一批必须同时带上 F 的补偿杠杆，不能只发「有界化」一族。

**F 的补偿杠杆（已核过公式）**：`F = S·sqrt(|RET| / max(TO, 0.125))`。
- TO 从 0.33 降到 0.25 ⇒ F × sqrt(0.33/0.25) = **×1.15**；
- 降 TO 的合法手段：`hump(x, hump=0.01)`（keyword-only）、提高 `decay`（6→10/15）、拉长 `ts_decay_linear` 窗口（5→10）；
- ⚠ `hump` / `decay` **不改持仓结构**（只平滑换手），所以在 D0-P 语境里它们**不是**「换概念」的替代品，但用于**过 Fitness** 是合规的（不是调 prod、不是混信号）。

## 5. prod 相关性三角（决定是否值得继续）

| id | prod | 判定 |
|---|---|---|
| `9qjAmw1o` | **0.8693** | corr-reversal 分支 **D0-P 判死**（≥ 0.75，无变体、无重试） |
| `MPa5ZpRa` | **0.8739** | 同上，**group 轴换成 country 也没用** |
| `wpZJPRql` | **0.7156**（写入时点，需 refresh 复核） | 落在 D0-P 的 **0.70–0.75 带**：只允许**一次**诊断性结构尝试，失败即 `dead_end` |

⇒ **corr-reversal 分支封存**（6 颗 alpha 全部作废，不再发同族变体）。**尾盘收益反转是唯一活着的探针**，且其 prod 空间只剩「一次尝试」。

**这次尝试的候选杠杆**（按证据强度排序）：

| 杠杆 | 证据 | 用途 |
|---|---|---|
| `CROWDING` 中性化 | USA 实证 0.644–0.676（level-divergence 族，−0.03~−0.06 通用）；且 rns 1.13/1.36 说明本信号不是纯反转暴露 | **本批唯一的结构尝试**（D0-P 的「一次」） |
| `SECTOR` 中性化 | 文档记录 F +0.13、margin ×2.7 | Fitness 补偿杠杆 |

⚠ **反向证据（如实记录）**：KOR risk71 实测 CROWDING 对**反转族**的 2Y 有 −0.02 的损害；RAM 更差（−0.40）。本信号 rns 1.13 说明它不是纯反转，所以仍值得赌这一次，但**如果 2Y 掉到 1.58 以下，就是这条杠杆的真实代价，不得再换第二把**。

## 6. 批次 23 / 23b / 23c 预登记（发批前写死判据）

三批共 13 臂，全部 ATOM（单数据集 `intraday_pv_feats`，无跨集混信号），全部过 `preflight_expressions`（无未知字段、无 vector 字段）与本地 `wqb.expression.op_arity.check_expression`（全 `[]`）。

### 批次 23（9 臂，SUBINDUSTRY / decay 6 / trunc 0.08）`aImb13lq56zc08OiM00ijB`

| # | 表达式 | 假设 |
|---|---|---|
| 1 | `-group_zscore(ts_decay_linear(mean_high_price_return_30m_pre_close_2,5), subindustry)` | 最省事的 CW 修：细分行业是否能压住权重 |
| 2 | `-quantile(ts_decay_linear(mean_high_price_return_30m_pre_close_2,5))` | 有界且保序，看 RET 掉多少 |
| 3 | `-rank(ts_decay_linear(mean_high_price_return_30m_pre_close_2,5))` | 完全有界 ⇒ CW 必解；F 是唯一悬念 |
| 4 | `-rank(ts_decay_linear(mean_last_trade_price_return_30m_pre_close_2,5))` (aC37) | 换价格基准（成交价 vs 最高价） |
| 5 | `-rank(ts_decay_linear(mean_last_trade_price_return_60m_pre_close_2,5))` (aC53) | 换窗口 30→60m |
| 6 | `-rank(ts_decay_linear(mean_vwap_return_30m_pre_close_2,5))` (aC30) | VWAP 基准（抗瞬时价毛刺） |
| 7 | `-rank(ts_decay_linear(mean_low_price_return_30m_pre_close_2,5))` (aC3) | 族内最冷门，测拥挤度红利 |
| 8 | `-group_rank(ts_decay_linear(mean_high_price_return_30m_pre_close_2,5), exchange)` | **exchange 轴**（用户点名，中性化列表无 EXCHANGE ⇒ 只能走 group） |
| 9 | `-rank(ts_decay_linear(mean_high_price_return_30m_post_open,5))` | **开盘后对照臂**（aC4）：若也无信号 ⇒ 尾盘效应真实 |

### 批次 23b（2 臂，**CROWDING** / decay 6）`4hilFzepY55ocyByWUXfp1F`

| # | 表达式 | 假设 |
|---|---|---|
| 1 | `-rank(ts_decay_linear(mean_high_price_return_30m_pre_close_2,5))` | **D0-P 唯一一次结构尝试**：降 prod |
| 2 | `-group_zscore(ts_decay_linear(mean_high_price_return_30m_pre_close_2,5), subindustry)` | 同时看 CROWDING 对 CW 有无副作用 |

### 批次 23c（2 臂，SUBINDUSTRY / decay 6）`5Dw5VdlY59WanrrSSVvcL8`

| # | 表达式 | 假设 |
|---|---|---|
| 1 | `-group_zscore(winsorize(ts_decay_linear(mean_high_price_return_30m_pre_close_2,5), std=4), country)` | **最小改动修 CW**：只截掉 4σ 以外的尾，保留中心分布 ⇒ 若 F 保住 1.0 且 CW 消失，这是最优解 |
| 2 | `-group_zscore(winsorize(ts_decay_linear(mean_high_price_return_30m_pre_close_2,5), std=4), industry)` | 同上 + 行业轴 |

### 收批读数（2026-10-22，10/13 臂已落）

| 臂 | 表达式 | S | F | 2Y | SUB | TO | RET | rns | CW |
|---|---|---|---|---|---|---|---|---|---|
| 1 `E5V6znJm` | `-group_zscore(…, subindustry)` | **1.71** | 0.77 | 1.50 | 1.20 | .3161 | 6.46% | 1.25 | **FAIL** |
| 2 `KPmJzARl` | `-quantile(…)` | 1.48 | 0.61 | 1.35 | 0.94 | .3032 | 5.11% | 1.26 | FAIL |
| 3 `j2eYGkQZ` | `-rank(…)` | 1.39 | 0.53 | 1.19 | 0.90 | .3026 | 4.46% | 1.28 | FAIL |
| 4 `QPYvzRdp` | `-rank(last_trade 30m)` | 0.99 | 0.33 | 0.02 | 0.23 | .3606 | 4.04% | 0.65 | FAIL |
| 5 `9qExM5o1` | `-rank(last_trade 60m)` | 1.28 | 0.52 | 0.44 | 0.64 | .3643 | 5.93% | 1.01 | FAIL |
| 6 `3qjoPmdg` | `-rank(vwap 30m)` | 1.15 | 0.42 | 0.24 | 0.35 | .3630 | 4.87% | 0.89 | FAIL |
| 7 `0mjYgZo8` | `-rank(low 30m)` | 0.62 | 0.17 | −0.09 | 0.51 | .3008 | 2.30% | 0.37 | FAIL |
| 8 `wp9QG76Q` | `-group_rank(…, exchange)` | 1.38 | 0.53 | 1.31 | 0.90 | .2910 | 4.30% | 1.27 | **PASS** |
| 9 `qMELG2bV` | `-rank(post_open)` | 0.53 | 0.21 | 1.44 | 0.35 | .2958 | 4.72% | 0.40 | PASS |
| 23b-1 `vRO1Gbdd` | `-rank(…)` @ **CROWDING** | 1.04 | 0.42 | 1.11 | 0.65 | .2905 | 4.63% | — | FAIL |

**四条硬归因（这一批最有价值的产出）**：

1. **收益全在尾部**。同一字段、同一窗口，`group_zscore(country)` RET **13.4%** → `group_zscore(subindustry)` 6.46% → `rank` 4.46% → `group_rank(exchange)` 4.30%。单调坍缩 ⇒ 有界化算子族（`rank`/`quantile`）**从机制上就不是 CW 的可行修法**，它们把 alpha 本身一起削掉了。S 也从 1.66 掉到 1.38–1.48。
2. **价格基准必须是 `high_price`**。同壳层（`rank` + 30m）换基准：high **1.39** / last_trade 0.99 / vwap 1.15 / low 0.62。`high_price` 独一档 ⇒ 机制是「尾盘 30 分钟创新高」的**极端贪婪读数**，不是一般价格收益。这也解释了为什么尾部承载收益：只有冲高到极端的那些票才有反转。
3. **CROWDING 在本族是负杠杆**（实测 S 1.39→1.04，−0.35），与 KOR risk71 文档一致（反转族被 CROWDING 伤）。⇒ D0-P 的那一次结构性尝试**已花掉且失败**，`wpZJPRql` 族按纪律记 `dead_end`。
4. **CW 与「有界化」不是同一件事**。`-rank(…)` 值域 [−1,0] 仍 FAIL，而 `-group_rank(…, exchange)` 与 `-rank(post_open)` PASS。⇒ CW 是**特定交易日 × 特定持仓簇**的边界事件，不是简单的值域问题；`exchange` 分组与 `post_open` 会话恰好避开了那簇。**这是本批唯一可复用的 CW 线索**（用户点名 exchange 轴的直觉在此得到回报）。
5. **`post_open` 对照臂 S 0.53 / retro 无信号** ⇒ 尾盘效应的会话特异性成立，开盘后同构字段不成立；机制解释（尾盘过度反应）未被推翻。

### 待收（3 臂）与判据

`5Dw5VdlY59WanrrSSVvcL8`（`winsorize(…, std=4)` × country/industry）与 `4hilFzepY55ocyByWUXfp1F` 第 2 臂仍在飞。**winsorize 是本轮最后一个未证伪的 CW 修法**：它截尾但保留中心分布，理论上比 `rank` 少伤 RET。

### 判据（读数前写死，读数后不得改口径）

**PASS 线**（USA/D1 RA 全闸）：S ≥ 1.58 · F ≥ 1.0 · 2Y ≥ 1.58 · SUB ≥ 0.43×S · TO ∈ [0.01, 0.70] · `CONCENTRATED_WEIGHT` 不在 `ra_failed_checks`。

**分支处置**：

| 读数形态 | 处置 |
|---|---|
| 有臂全过 IS 闸 | 取最优 1–2 颗 → `check_correlation(refresh=True)` 实测 prod → 按 D0-P：< 0.60 直接进提交判定；0.60–0.70 不发变体；**0.70–0.75 时 CROWDING 臂就是那一次尝试**，无论结果如何都收手；≥ 0.75 ⇒ `dead_end` |
| 无臂全过，但**只差 F 且 F ≥ 0.9** | 发**批次 24**：只对最优那 1–2 条做 TO 杠杆（`hump=0.01`、decay 6→12、`ts_decay_linear` 窗口 5→10），**不再加新字段/新壳层** |
| 无臂全过，且 S / 2Y 也掉（有界化连信号一起削没） | 尾盘族**低产**，datasets 记入 `dead_end` 队列（**不 seal**，forum-recon fail-closed 闸需人工确认，见 §7） |
| 批次 23 中 CROWDING 臂显著降 prod（< 0.65）但 IS 掉闸 | CROWDING 杠杆**记账但不复用**：它在本族的代价是 IS，不是 prod |
| `post_open` 对照臂反而更强 | 推翻「尾盘效应」机制解释，本画像的机制段作废重写，不得顺着数据改叙事 |

## 7. 终判（prod 复核后封板）

**`wpZJPRql` prod 复核 = 0.7429**（2026-10-22 `check_correlation(refresh=True)`，此前记的 0.7156 已过期）。直方图 `[0.7,0.8)` 桶 **n=2** ⇒ 属「已实质撞墙」形态，不是边界噪声。

按 D0-P：0.70–0.75 只允许**一次**诊断性结构尝试 —— 该尝试已由批次 23b 的 CROWDING 臂消耗，实测 **S 1.39→1.04（−0.35）**，是负杠杆。⇒ **尾盘 `high_price` 反转族判 `dead_end`**（prod 0.7429 + 唯一结构杠杆反向）。

叠加 corr 分支（prod 0.8693 / 0.8739）与「收益全在尾部、有界化必杀 alpha」的双重约束，**`intraday_pv_feats` 对 REGULAR RA 的可用出口归零**：唯一能过 Fitness 的壳层（fat-tail zscore）恰好是 prod 最高的壳层，而任何降 prod/降 CW 的有界化都会把 RET 从 13.4% 砍到 4.3–6.5%，F 随之掉出 1.0。**这不是参数问题，是结构性互斥。**

**不 seal 的原因**：`seal_dead_end` 的 forum-recon 闸 fail-closed，需 `force_seal=True`/`require_forum_recon=False` 且人工确认。判死结论先落纸面，封存动作待用户点头。

## 8. 待收与遗留

1. `5Dw5VdlY59WanrrSSVvcL8`（`winsorize(std=4)` × country/industry）与 `4hilFzepY55ocyByWUXfp1F` 第 2 臂仍在飞 —— **即使 winsorize 能修 CW，也改不了 prod 0.7429 的结论**，故其读数只作「winsorize vs rank vs quantile 三类有界化对 RET 的伤害排序」证据，不改变数据集体检结论。
2. **`9qE7WOxr` 指标未取全**；如需引用须补 `get_alpha_details`。
3. **CW 的可复用线索**：`group_rank(x, exchange)` 与 `rank(post_open)` PASS 而 `rank(pre_close)` FAIL ⇒ CW 是特定交易日 × 持仓簇的边界事件，`exchange` 分组能避开。此线索留给**其它数据集**复用（本数据集已封）。

## 9. 批次 25（aC=0 尾部字段探针，10 臂）—— 全灭

壳层固定为 `±quantile(group_rank(winsorize(ts_backfill(ts_zscore(<core>, 252), 120), std=4), subindustry))`
（decay 10 / trunc 0.08 / SUBINDUSTRY / USA-TOP3000-D1）；唯一例外 E1 用 `ts_av_diff(…, 252)` 替 `ts_zscore`
（该字段是有界收益族，长窗 av_diff 才是「偏离自身慢基线」）。符号按机制先验预登记，未做符号扫描。

| 臂 | 核心字段 | alpha | S | F | 2Y | SUB | TO | 判定 |
|---|---|---|---:|---:|---:|---:|---:|---|
| A1 − | `skew_bid_ask_size_to_volume_ratio` | `d5KWol6K` | −0.09 | −0.01 | −0.91 | 0.17 | 54.0% | 无信号 |
| A2 + | 同上（镜像对照） | `vRO16Jbb` | 0.09 | 0.01 | 0.91 | −0.17 | 54.0% | 无信号 |
| B1 − | `corr_high_price_with_slippage` | `1YjNPnAk` | −2.05 | −0.76 | −2.45 | −1.59 | 66.6% | 镜像 |
| B2 + | 同上 | `58jEeqd6` | **2.05** | 0.76 | 2.45 | 1.59 | 66.6% | **prod 0.8843 ⇒ dead_end** |
| C1 − | `kurtosis_trade_volume_interval` | `pwvdZ1ej` | 0.90 | 0.18 | 0.02 | −0.15 | 59.9% | F/2Y/SUB 三闸掉 |
| D1 − | `std_low_price_last_half` | `mLYo1xW1` | −0.85 | −0.29 | −1.26 | −0.31 | 28.1% | 符号先验错，无信号 |
| E1 − | `ts_av_diff(mean_high_price_return_30m_pre_close_2, 252)` | `gJWedoNv` | −0.35 | −0.13 | −0.75 | −0.17 | 18.6% | 尾盘高价机制**第二次**被否 |
| F1 + | `skew_bid_to_ask_price_ratio` | `XgR9eYZ8` | 0.40 | 0.06 | 0.87 | −0.14 | 44.7% | 无信号 |
| G1 − | `corr_ask_price_with_bid_size` | `akVKwWmR` | 1.70 | 0.46 | 1.07 | 0.79 | 66.5% | F + 2Y 掉 |
| H1 − | `corr_interval_asksize_with_interval_bidsize` | `E5V6LrnP` | 0.02 | 0.00 | 0.39 | −0.24 | 52.4% | 无信号 |

**`58jEeqd6` 是本次唯一 IS 近乎全过的臂**：S 2.05 / SUB 1.59（ratio 0.78）/ `risk_neutralized_sharpe` 3.54 /
`investability_sharpe` 2.08，唯一缺口是 `LOW_FITNESS`（0.76 vs 1.0），TO 66.6% 仍在线上。
按 §6 分支表本应发 TO 杠杆批（`hump=0.01` / decay 6→12）—— **但 prod 复核先做了**：
`check_correlation(refresh=True)` = **0.8843**，直方图 `[0.7,0.8)` n=5194、`[0.8,0.9]` n=323 ⇒ 族级饱和，
不是单邻居重叠。按 D0-P **≥0.75 即 `dead_end`、零变体** ⇒ TO 杠杆批**未发**（省 1 批配额）。

**归因（为什么 slippage 相关性必爆 prod）**：见 §10 —— 该概念已被论坛公开发表，且字段名逐字出现在论坛代码片段里。

## 10. 论坛取证：本数据集两个最强概念都已被公开发表

| 帖子 | 日期 | 命中的本数据集概念 | 证据形态 |
|---|---|---|---|
| `【Alpha灵感】开盘后执行滑点（Slippage）的非线性偏度特征构造`（XH93773） | 2026-09-10 | 滑点协偏度 / 滑点二阶矩 | 完整构思路径，与 `corr_high_price_with_slippage` 同族 |
| `【Quant101】…FastExpr…`（ZH87224） | 2026-06-27 | `mean_slippage_30m_post_open` | **字段名逐字出现在帖子代码片段**：`bucket(rank(mean_slippage_30m_post_open),range='0,1,0.2',NaNGroup=true)` ⇒ 该字段 aC 虽为 0，但概念已是公共品，**从候选池剔除** |
| `[Alpha Idea] 反转效应的精细化及其扩展`（YP17461） | 2026-09-11 | 尾盘高价反转 | 原文「其它指标（例如 volume，slippage）是不是也可以作为一个成功的代理变量？」+ 同族 GLB `bljZvjjK`（S 2.34）已在平台 |

**可复用纪律（候选池侧）**：「**aC=0 ≠ 未被挖过**」—— aC 只统计平台已提交 alpha 的字段引用，
**统计不到论坛帖子**。选字段前除查 `alphaCount` / `userCount`，还要按字段语义在论坛搜一次
（关键词 = 机制名，不是字段名，因为帖子往往用自然语言描述）；命中 `【Alpha Idea】` / `【Alpha灵感】` 系列的，
直接剔除，即使其 aC=0 且覆盖率完美。本数据集 2/2 最强概念均命中此条。

## 11. 数据集体检结论（终）

`intraday_pv_feats`（582 字段，全 MATRIX）**对 USA/D1 REGULAR RA 的可用出口 = 0**：

1. **能过 Fitness 的壳层（fat-tail zscore，`group_zscore(country)` RET 13.4%）恰好是 prod 最高的壳层**（0.87–0.88）；
2. **任何降 prod / 降 CW 的有界化都把 RET 从 13.4% 砍到 4.3–6.5%**（§6 第 1 条），F 随之掉出 1.0 ⇒ 结构性互斥；
3. 两个 IS 最强的候选（`wpZJPRql` prod 0.7429、`58jEeqd6` prod 0.8843）均已越过 D0-P 的 0.70 线；
4. 弱一些的臂（C1/G1）在 F 与 2Y 上直接掉闸，且它们的机制（成交量峰度 / 报价-挂单量相关）无经济先验支撑。

累计测试：批次 23（10）+ 23b/23c（含 winsorize 对照）+ 25（10）= **30+ 条**，S 上限 2.05、prod 地板 0.7429。
**判据已满足，按 §7 封板**（`seal` 动作待用户确认 `force_seal`）。

