# USA / insider_matrix（内部人增减持矩阵）字段画像与机制实证

> 快照：2026-10-23（`get_datafields` region=USA universe=TOP3000 dataset=insider_matrix，33/33 字段实测）
> 状态：**在挖**（波 `insd_w1` 设计完成，10 臂待发）
> 前置：`insider_matrix` 在 USA **不是新数据集** —— DB 里已有 21 条回测（全部来自 2026-10-01 的
> GEM idea 波 `s2_insider_matrix_d1`），且 `cells.json` 有一条 **bound=inferred** 的判死
> `USA-INSIDER-MATRIX-SPARSE-EVENT-WALL`。本文件第 4/5 节交代「为什么旧证据不构成本轮结论」，
> 不靠绕过判死闸推进（闸会 WARN，见 §7.3）。

## 1. 为什么换到 insider_matrix（不换 region）

前序未点亮塔路线已逐条判死（详见 `_usa-risk60-field-profile-20261023.md` §1 与
`output_report/USA_regular_alpha_delivery_20261021.md` §8 起）：risk60（prod 0.9917）、other143（prod 0.8658）、
pv106 / pv149、fhp、uen、techindi_model、chart_return_model、other416/635/596、board_gov_stats、
fundamental14/93/1、acquisition_model。塔位现状（USA/D1，2026-10-23 平台快照）：analyst 6 颗、model 4 颗
已点亮（**不优选**）；earnings 1、institutions 0、pv 0、risk 0、news 0、option 0、sentiment 0、fundamental 0。

**insider_matrix 入选的四个交集**：

| 判据 | 实测 |
|---|---|
| 塔归属 | `get_alpha_details` pyramids = **USA / D1 / OTHER ×1.4** —— 未点亮，且 1.4 是全塔最高倍率档 |
| USA 本地已挖程度 | 21 条回测（1 波），**只有 1 条** S > 2（`zqbvOmOR` S 4.30），其余 20 条全部 S ≤ 2.89 且多数 ≤ 1.13 |
| 字段规模 | 33 个 MATRIX 字段，8 个总体切片 × 4 个度量，无 VECTOR（不需要 `vec_*` 预处理） |
| 覆盖 | 0.7652（`_1`/`_2`/`_4` 族）/ 0.7715（`_3` 族），**无 SUB 覆盖风险**（远超 0.4 线） |

**为什么不是「随便换个数据集」**：这一轮换的理由是上一条路线（risk60）被 prod 0.9917 结构性挡死，
属任务约束里「确实无计可施才换」的情形；换的是数据集，region 始终 USA。

## 2. 字段全表（33/33，MATRIX）

平台语义：每条内部人交易记录在「某个总体切片 × 某个度量」上聚合。**8 个切片 × 4 个度量**：

- 度量：`_value_1` = 买入均值；`_value_2` = 买入合计（**强度**）；`_value_3` = 卖出均值；`_value_4` = 卖出合计。
- 切片（宽 → 窄）：`eur_aggregated_*`（全部内部人）→ `eur_signal_*`（有显著交易者）
  → `eur_director_signal_*`（显著交易的董事）→ `eur_top_director_signal_*`（显著交易的高管）
  → `eur_director_*`（全部董事）→ `eur_top_director_*`（特定董事）→ `eur_top_*`（特定高管，最窄）。

| 字段（代表） | 覆盖 | userCount | **alphaCount** | 语义 | 本轮用途 |
|---|---:|---:|---:|---|---|
| `eur_aggregated_value_1` | 0.7652 | 65 | **173** | 全部内部人买入**均值** | **主信号**（锚点字段） |
| `eur_aggregated_value_3` | 0.7652 | 11 | **13** | 全部内部人卖出均值 | 已实测无信号（§4.2），本轮不作主腿 |
| `eur_aggregated_value_2` | 0.7652 | — | — | 全部内部人买入**合计** | 强度变体（A2/A10 族） |
| `eur_signal_value_2` | 0.7715 | 113 | **225** | 显著交易者买入合计 | 对照切片（A10） |
| `eur_signal_value_1` | 0.7715 | 74 | **186** | 显著交易者买入均值 | 待第二轮 |
| `eur_top_director_signal_value_1` | 0.7715 | — | — | 高管显著买入均值 | 旧波最优低换手臂（S 0.90） |
| `director_intensity_score` | 0.7652 | 4 | 4 | **平台描述文明示「timing/bookkeeping indicator … not a trading signal」** | **排除**（语义闸已拦，见 §3.1） |

### 3.1 语义闸的一处真实修复（2026-10-23）

`director_intensity_score` 的描述是
`"Dataset-specific timing/bookkeeping indicator used for internal sequence logging; not a trading signal"`，
旧版 `tools/field_semantic_classify.py` 只按 indicator/flag 名词判，把它当信号字段放行。
本轮补了一条**描述文驱动的非信号规则**（要求显式措辞，两个分支都不得只靠裸 indicator 名词），并加回归
用例 `test_platform_declared_non_signal_indicator_blocked`（10 passed）。台账已重写：
**32 signal / 1 blocked**，`USA/s1_semantic_insider_matrix`（2026-10-23T15:04:52）。

对照：EUR 同一数据集是 33/33 信号（旧台账，未修此规则）—— 跨区差异只是描述文措辞不同，不影响 USA 结论。

## 4. 历史证据：21 条回测的精确读数（为什么不能直接当结论）

`backtest_results` 里 `region=USA AND dataset=insider_matrix` 共 **21 条**，全部 `wave=s2_insider_matrix_d1`
（2026-10-01 GEM idea 波；门禁 61 条过、实际回测 21 条）。按形态分三类，**每类都只覆盖了一种形状**：

### 4.1 原始幅度族（唯一有真信号的）—— 三条闸全撞

| alpha | 表达式 | S | F | TO | 2Y | SUB | RA 失败项 |
|---|---|---:|---:|---:|---:|---:|---|
| `zqbvOmOR` | `ts_zscore(eur_aggregated_value_1, 252)` | **4.30** | **3.28** | **1.7685** | **5.65** | 1.12 | HIGH_TURNOVER / CONCENTRATED_WEIGHT / LOW_SUB_UNIVERSE_SHARPE |
| `gJZYxMml` | `ts_zscore(eur_aggregated_value_1, 66)` | 2.89 | 2.10 | 1.7492 | 4.25 | 1.01 | 同上 |

### 4.2 平滑族（低换手但信号被磨平）

`group_rank(ts_mean(<字段>, W), <group>)`，W ∈ {22, 66, 252}，group ∈ {industry, subindustry}，
字段 ∈ {aggregated_value_1, top_director_signal_value_1}：**14 条，S 0.64 – 1.13，F 0.31 – 0.59，2Y −0.14 – 0.77**，
全部 `LOW_SHARPE + LOW_FITNESS + LOW_2Y_SHARPE`。最好的一臂 `omW1VlVk`（ts_mean 22, subindustry）S 1.13 / F 0.56 / TO 0.088。

### 4.3 净额族（买卖相减）—— 2Y 系统性为负

`group_rank(subtract(ts_backfill(买, 66), ts_backfill(卖, 66)), …)` 6 条：S 0.75 – 0.86，
**2Y −0.14 / −0.13 / −0.06 / −0.02 / +0.02**。净额把「买入强度」与「卖出强度」相减，而卖出侧本身无信号（见下），
等价于给主信号加了一层与它无关的噪声，并把衰减结构弄坏。

### 4.4 卖出侧单独实测：无信号（与本轮引用的论文一致）

`_value_3` 三条：S **0.07** / **−0.07** / **−0.78**（`QPK1ENxM` / `MP3jkeEk` / `P0gJvYRq`）。
与 Jeng-Metrick-Zeckhauser (2003) 的结论一致：**只有买方有信息**（其买入组合年化超额显著、卖出侧近零）。
⇒ 本轮**只用买入侧**，不再花配额在卖出/净额上。

### 4.5 为什么这 21 条不构成本轮的结论

| 旧证据 | 为何过时/不足 | 本轮怎么办 |
|---|---|---|
| 21 条全部只用了 `ts_mean` / `subtract` / 裸 `ts_zscore` 三种形状 | 论坛已证 `ts_mean` 会**摧毁事件频率**（|ts_mean| 把稀疏事件摊平），`subtract` 又引入无信号腿 | 改用 `ts_sum`（保留事件强度）+ `ts_rank` / `ts_decay_linear` |
| `USA-INSIDER-MATRIX-SPARSE-EVENT-WALL`（bound=**inferred**） | 推论依据是「旧形状打不过稀疏墙」，而旧形状**从未测过** winsorize / tail 压缩 / `ts_target_tvr_*` | §6 的 10 臂正是这些未测形状；波后按实际结果重判该 dead-end |
| prod 证据 | 旧波**没有**任何 prod 记录；本轮已补：`zqbvOmOR` **prod 0.5155**（落库 2026-10-22T20:24:19）、`gJZYxMml` **0.619** | prod 远低于 0.7 ⇒ **不是拥挤族**，值得投入 |

**prod 直方图（`check_correlation` refresh=True，2026-10-22）**：
`[0.6,0.7)` 桶 **n=0**、`[0.7,0.8)` 桶 **n=0**，生产池 2,580,651 颗，`PROD {"max": 0.5155}`
；`SELF {"max_correlation": 0.10033, "passes_check": true}`。
按 D0-P：≥0.75 才判死，本族有 **0.23 的余量**。

## 5. 机制归因：三条失败闸各自的结构成因（先归因再推进）

锚点 `zqbvOmOR` 的真信号是**扎实的**，不是单年拟合 —— `get_alpha_yearly_stats` 实测 **10/10 年正 Sharpe**，
且逐年换手稳定在 1.72–1.81：

| 年 | 2014 | 2015 | 2016 | 2017 | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Sharpe | 3.60 | 3.93 | 3.59 | 4.91 | **2.67** | 4.10 | 4.58 | 4.52 | 6.00 | 5.26 |
| Fitness | 2.41 | 2.78 | 2.06 | 3.30 | 1.56 | 3.05 | 4.03 | 3.77 | 5.68 | 4.84 |
| 换手 | 1.78 | 1.79 | 1.81 | 1.72 | 1.74 | 1.76 | 1.77 | 1.80 | 1.79 | 1.72 |

⇒ 三条失败闸**全部是结构性的，不是信号弱**：

1. **CONCENTRATED_WEIGHT 0.5（2023-10-06）**：`ts_zscore` 保留的是**原始幅度**，极端内部人大额买入把权重推到
   单票 50%。`longCount 19 / shortCount 22` —— 只有 41 只票持有，在 TOP3000 里等于没分散。
2. **HIGH_TURNOVER 1.77**：事件驱动的原始幅度信号**每天在换名次**。论坛实证（post 43175786936087）：
   换手来自三个源（数据源高频翻转 → 时序聚合；构造放大 → 容忍结构；权重集中 → 截断/分组），
   而 **decay 只平滑数值抖动、修不了 rank 翻转**；对翻转型数据应优先 `ts_decay_linear` 长窗（保幅度、降翻转频次）
   或 `ts_target_tvr_*` 自适应。
3. **LOW_SUB_UNIVERSE_SHARPE 1.12 vs 1.86**：`nanHandling=ON` 下「无事件」被填成 0，
   **零值并列占横截面 ~72–80%、rank 落在中位（~0.4）** ⇒ 中位附近产生随机权重（论坛 post 43178926004887 实测），
   大市值子宇宙被这批噪声稀释。

## 6. 外部证据与波 `insd_w1` 的 10 臂设计

### 6.1 论坛（可复用结论，已记入本文件）

| 来源 | 结论 | 本波如何用 |
|---|---|---|
| **post 43178926004887** | 稀疏事件 + `nanHandling=ON` ⇒ 零值并列占 72–80%、rank 卡中位 ⇒ `LOW_SUB_UNIVERSE_SHARPE` 崩塌。修法：`winsorize(group_rank(ts_sum(r, 66), group), std=2)` + `tail(w, lower=0.25, upper=0.75, newval=0.5)`，作者实测 **+0.24 S / +0.58 SUB** | 臂 A1–A4、A7–A10 直接采用；`ts_sum` 而非 `ts_mean`（同帖：`ts_mean` 把 S 从 1.44 打到 0.73） |
| 同上 | 66 = 季度窗，有经济含义（财报/窗口期披露节奏） | 事件腿统一 W=66 |
| **post 43175786936087** | 换手三源与对应处方；`group_zscore` 的换手比裸 rank 低 20–30%；`ts_target_tvr_*` 作自适应换手整形 | A5（`ts_decay_linear` 长窗）、A6（`ts_target_tvr_hump`） |

### 6.2 学术证据（解释为什么只用买方、为什么做尺度归一）

- **Jeng, Metrick & Zeckhauser (2003)**：内部人**买入**组合有显著超额、**卖出**侧接近零 ⇒ 只用 `_value_1`/`_value_2`。
- **Lakonishok & Lee (2001)**：内部人交易信号的收益主要来自**尺度归一后的横截面排序**（金额需除以公司规模/市值一类的量纲），
  不是绝对金额 ⇒ 用 `group_rank` 做组内归一（本数据集无市值字段，退化为行业组内 rank，并把尾部并列压到0.5）。
- **Cohen, Malloy & Pomorski (2012)**：区分 **routine vs opportunistic** 内部人交易，机会型才有预测力
  ⇒ 切片从 `aggregated_*`（全部）收到 `signal_*`（显著交易者）应保留/增强信号，故本轮设 A10 做切片对照。

### 6.3 10 臂（设置全部与锚点 `zqbvOmOR` **逐项一致**，差异只来自表达式）

统一设置：TOP3000 / D1 / SUBINDUSTRY / decay 5 / truncation 0.08 / pasteurization ON /
unitHandling VERIFY / nanHandling ON / maxTrade OFF / 2014-01-01 → 2023-12-31。这样任一臂的变化只能归因于表达式本身。

| # | 标签 | 表达式 | 验的假设 |
|---|---|---|---|
| 1 | `A1_forum_ind` | `tail(winsorize(group_rank(ts_sum(eur_aggregated_value_1, 66), industry), std=2), lower=0.25, upper=0.75, newval=0.5)` | 论坛骨架原样（industry 组）：同时修 CW / 换手 / SUB |
| 2 | `A2_forum_sub` | 同上，`subindustry` | 组粒度对照（本区历史 subindustry 略优） |
| 3 | `A3_z_tail_sub` | `tail(winsorize(group_rank(ts_zscore(eur_aggregated_value_1, 252), subindustry), std=2), lower=0.25, upper=0.75, newval=0.5)` | **只加尾部压缩**：是否足以把锚点从 3 闸失败救到全过（最小改动） |
| 4 | `A4_z_tail_ind` | 同上，`industry` | 组粒度对照 |
| 5 | `A5_z_decay_rank` | `group_rank(ts_decay_linear(ts_zscore(eur_aggregated_value_1, 252), 22), subindustry)` | 长窗线性衰减修 rank 翻转（不动幅度语义） |
| 6 | `A6_tvr_hump` | `ts_target_tvr_hump(ts_zscore(eur_aggregated_value_1, 252), target_tvr=0.5)` | 自适应换手整形，目标 0.5 ≪ 0.70 闸 |
| 7 | `A7_tsrank_tail` | `tail(winsorize(group_rank(ts_rank(eur_aggregated_value_1, 252), subindustry), std=2), lower=0.25, upper=0.75, newval=0.5)` | 用时序 rank 替代 zscore（有界、抗极端值） |
| 8 | `A8_sum66_z_tail` | `tail(winsorize(group_rank(ts_zscore(ts_sum(eur_aggregated_value_1, 66), 252), subindustry), std=2), lower=0.25, upper=0.75, newval=0.5)` | 先季度强度聚合、再长窗标准化（量纲两段归一） |
| 9 | `A9_net_buy` | `tail(winsorize(group_rank(ts_zscore(subtract(eur_aggregated_value_1, eur_aggregated_value_3), 252), subindustry), std=2), lower=0.25, upper=0.75, newval=0.5)` | 净额 + 尾部压缩（验证 §4.3 的失败是否只因缺压缩） |
| 10 | `A10_pop_sig2` | `tail(winsorize(group_rank(ts_zscore(eur_signal_value_2, 252), subindustry), std=2), lower=0.25, upper=0.75, newval=0.5)` | 切片换到「显著交易者 × 买入合计」（CM 2012 的机会型） |

**算子点数**：A1–A4、A7–A10 = 5 个调用点（tail / winsorize / group_rank / ts_sum 或 ts_zscore 或 ts_rank / subtract），
A5 = 3，A6 = 2 —— 全部 **< 10**（`gate.py::MAX_OP_CALLS`）。

## 7. 预注册判据（波后不得改判）

1. **任一臂 RA 全 PASS** ⇒ 立刻 `check_correlation(refresh=True)` 取 prod + `check_self_correlation` 取 self；
   **prod < 0.70 且 self < 0.70** 才算候选，再走稳健闸与用户确认。
2. **prod ≥ 0.75** ⇒ 按 D0-P 判死该机制；**`[0.70, 0.80)` 桶 n ≥ 1** ⇒ 记为该族拥挤，不再换窗口硬救。
3. **`LOW_SUB_UNIVERSE_SHARPE` 若仍是唯一失败项** ⇒ 说明尾部压缩没修到根，下一波才允许动 `nanHandling` /
   宇宙；不得靠调 decay 撞运气。
4. **`CONCENTRATED_WEIGHT` 若仍失败** ⇒ 直接看 `longCount`：< 60 判为结构性稀疏，停止单字段挖掘。
5. 臂间比较只看「同设置下的 S / SUB / TO」三列，**不做跨设置比较**（本轮设置已钉死）。

### 7.3 与既有判死的关系（不绕过）

`cells.json.cells.other.evidence.dead_ends[5]` = `USA-INSIDER-MATRIX-SPARSE-EVENT-WALL`
（`bound: inferred`，依据「稀疏事件价值字段需 trade_when+长窗平滑但会稀释信号至 <1.58」）。
本波执行时 `gate.py` 的 priors 闸会 **WARN（HIT）**，不会 FAIL（该闸只在 `--require-priors` 下升级）。
本文件给出**不沿用旧结论的两条新证据**：① 旧波 21 臂从未测过 `winsorize + tail` 骨架、`ts_sum`、`ts_target_tvr_*`；
② 补测的 prod 0.5155 / self 0.10033 说明该机制在生产池里**不拥挤**，堵点不在相关而在结构。
波后按 §7 判据重判该 dead-end（确认或推翻），不以旧 `inferred` 结论代替实测。

## 8. 存档索引

- 本文件：`Claude/skills/wq-brain-ra-usa/references/_usa-insider-matrix-field-profile-20261023.md`
- 字段目录（平台实测）：`USA/catalog_insider_matrix`（2026-09-29T23:21:59 抓取；本轮 2026-10-23 用 `get_datafields` 复核 33/33）
- 语义台账：`USA/s1_semantic_insider_matrix`（2026-10-23T15:04:52，32 signal / 1 blocked）
- 体检包：`tracking/mining/field_inspect_usa_insider_matrix.json`（`tools/gen_inspect_from_db.py` 生成）
- 历史波：`wave=s2_insider_matrix_d1`，21 条（`backtest_results`）
- 锚点逐年：`get_alpha_yearly_stats(zqbvOmOR)`（10/10 正年）
- prod：`zqbvOmOR` 0.5155、`gJZYxMml` 0.619（`alphas.prod_correlation`，2026-10-22T20:24）
- 本波：`tracking/USA/runs/usa_insd_w1_exprs.txt` + `usa_insd_w1_spec.json`，wave = `insd_w1`
