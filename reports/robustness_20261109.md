# 稳健性审计 · 2026-11-09

> 口径：**Recent-3yr（2021/2022/2023）**，skill `brain-alpha-robustness` Phase B/C 现行判定表。
> 全历史 CV / max-min 只作信息软标记，**绝不据此 REJECT**。
> 今日配额：ET 11-09 全新 4/4（最后一颗 `bl6KwjwK` 提交于 ET 11-08 02:00）。

## 0 七颗候选全景（ΔSharpe 为平台 `performance_comparison` 实测）

| id | 区/池 | S | F | 2Y | TO | prod | 余量 | **ΔS** | 分区基准 | 近3年均 | 近3CV | 最差年 | <1.58 年数 | 判定 |
|---|---|---:|---:|---:|---:|---:|---:|---:|---|---:|---:|---:|---:|---|
| **P0obGoQJ** | ASI/MINVOL1M | 3.06 | 1.39 | 2.37 | .291 | .5973 | **.1027** | **+0.730** | ASI:1:PP (2.31) | 2.76 | 0.296 | 1.96 | **0** | **PASS** |
| **akK9ooZv** | GBR/TOP700 | 3.10 | 1.48 | 2.71 | .411 | .6282 | .0718 | **+0.710** | GBR:1:PP (3.56) | 2.89 | **0.092** | 2.23 | **0** | **PASS** |
| **RREPm361** | DEU/TOP500 | 2.02 | 1.25 | 1.82 | .251 | .6881 | **.0119** | **+0.730** | DEU:1:PP (1.73) | 2.19 | 0.394 | 1.06 | 4 | CONDITIONAL |
| **RREwqrNa** | DEU/TOP500 | 1.65 | 1.17 | 2.57 | .107 | .6684 | .0316 | **+0.080** | DEU:1 (3.30) | 1.85 | 0.829 | 0.18 | 7 | CONDITIONAL |
| mL617YPx | EUR | 1.82 | 1.25 | 2.23 | .068 | .5421 | **.1579** | **0.000** | EUR:1 (5.48) | 2.23 | 0.661 | 0.41 | 5 | 零增益备胎 |
| **QPvzNNGG** | DEU/TOP500 | 1.70 | 1.30 | 2.18 | .155 | .6777 | .0223 | **−0.050** | DEU:1 (3.30) | 2.23 | 0.311 | 0.93 | 4 | **硬闸阻断** |
| **N1NGbddg** | EUR | 1.69 | 1.05 | 2.17 | .051 | .6872 | .0128 | **−0.100** | EUR:1 (5.48) | 2.24 | 0.417 | −0.23 | 4 | **硬闸阻断** |

两两互相关**全部 < 0.27**（最大对 `RREPm361 ↔ N1NGbddg` 0.2682），独立子集 = 7。

---

## 1 `akK9ooZv` — GBR/TOP700/D1/FAST · **PASS（今日首选之一）**

- 表达式（9 ops，add 两腿）：
  `add(multiply(2, group_rank(ts_zscore(tm_15_r1_r5_r10_rh_glb_d1_r1_q1, 126), sector)), reverse(group_rank(ts_zscore(vec_sum(loaned_share_count_main), 504), sector)))`
- 平台闸：`checks.fail=[]`、`CLUSTER_TEST` PASS、`ra_failed=0`、`IS_LADDER_SHARPE` 过；塔 = `GBR/D1/SHORTINTEREST`(1.2) + `GBR/D1/OTHER`(1.6)。
- **逐年 Sharpe（2014–2023）**：4.84 / 4.25 / 2.23 / 3.06 / 2.70 / 2.73 / 3.46 / 3.06 / 2.58 / 3.02
  - **十年无一年低于 2.0**，无负年、无平年、无 late_start。
  - 近 3 年均值 **2.887 ≥ 1.58** ⇒ 主判 PASS；近 3 年 CV **0.092**（全库最低档）。
  - 末段 **+17%**（2022 2.58 → 2023 3.02），**无衰减**。
  - 单年最低 2016 = 2.23，仍是 1.58 线的 1.41 倍。
- 相关性：self **0.5022**（最高指向 `3qoGxkqZ`，11-08 提交）< 0.55 ⇒ 分散度闸走 light，不触发；prod **0.6282 PASS**（3.9h 权威读数，`all_passed=true`）。
- ΔSharpe **+0.710**（GBR 分区 3.56 → 4.27，F 2.45 → 2.82）。
- 混腿：`two_leg`，`coef_legs=1` ⇒ **需答三问**。
- **结论：PASS**

## 2 `P0obGoQJ` — ASI/MINVOL1M/D1/SLOW · **PASS（今日首选之一）**

- 表达式（4 ops，单腿）：
  `multiply(-1, group_rank(ts_rank(probability_label1_5quantile_60day_ohlcv, 5), country))`
- 平台闸：`checks.fail=[]`、`CLUSTER_TEST` PASS（同族 w5–w8 才进簇，w9 卡 1.55）。
- **逐年 Sharpe**：4.17 / 2.99 / 3.53 / 3.69 / 3.19 / 2.46 / 2.41 / 3.59 / 1.96 / 2.72
  - 无负年；全期最低 1.96（2022），仍 > 1.58。
  - 近 3 年均值 2.757；近 3 年 CV 0.296；末段 **+39%**（1.96 → 2.72）。
- 相关性：self 对 ASI 池 6 颗 ACTIVE 最高 **0.32**（`E5ReEnpP`），其余 |ρ|<0.05；prod **0.5973 PASS**（21.1h，48h 内）。
- ΔSharpe **+0.730**（ASI 分区 2.31 → 3.04，F 1.37 → 1.65）。
- 混腿：`none`（单腿）⇒ 不需三问。
- 同族 10 颗互相关 0.73–0.996，**提这颗后其余 9 颗永久淘汰**（newly submitted 会进 prod 池并顶高它们）。
- **结论：PASS**

## 3 `RREPm361` — DEU/TOP500/D1/FAST · **CONDITIONAL**

- 表达式（5 ops，add 两腿）：
  `group_rank(add(ts_zscore(est_12m_ebi_median, 240), ts_zscore(subtract(est_12m_ebt_mean, est_12m_ebt_mean_4wks_ago), 44)), sector)`
- **逐年 Sharpe**：3.06 / 2.43 / **1.28** / 2.40 / **1.52** / **1.06** / 2.10 / 3.01 / 2.26 / **1.29**
  - 无负年，但 **4 年低于 1.58**（2016/2018/2019/2023）。
  - 近 3 年均值 2.187 ≥ 1.58 ⇒ 主判 PASS；近 3 年 CV 0.394（REJECT 档边缘）。
  - **末段衰减 −43%**（2022 2.26 → 2023 1.29）⇒ 按 2026-11-07 口径记 `soft_flag` + 衰减提示。
- 相关性：self **0.328**（最安全之一）；prod **0.6881**，**余量仅 0.0119**（17.1h 读数，已包含 11-08 提交的 `zq3eb7No` 影响）。
- ΔSharpe **+0.730**，但基准是 **`DEU:1:POWER_POOL`（S 1.73）** 而非常规 DEU 组合（S 3.30）——同样 +0.73 的含义与 `RREwqrNa` 的 +0.08 不可直接横比。
- 混腿：`two_leg` ⇒ **需答三问**。
- **结论：CONDITIONAL**——ΔS 硬闸通过，但 prod 余量 0.0119 薄且末段衰减，建议排在 4 颗之末或让位。

## 4 `RREwqrNa` — DEU/TOP500/D1/FAST · **CONDITIONAL**

- 表达式（13 ops，单腿乘积）：
  `winsorize(reverse(group_rank(multiply(multiply(rank(subtract(ts_sum(vec_avg(transaction_count_main),176),ts_sum(vec_avg(transaction_count_main),66))),rank(subtract(ts_sum(vec_avg(average_loan_duration_days_main),176),ts_sum(vec_avg(average_loan_duration_days_main),66)))),rank(subtract(ts_sum(vec_avg(loan_rate_volatility_main),176),ts_sum(vec_avg(loan_rate_volatility_main),66)))),industry)),std=4)`
- **逐年 Sharpe**：1.46 / 1.94 / 1.17 / 1.22 / 3.51 / 1.38 / **0.18** / **0.58** / **3.56** / 1.42
  - 无负年，但 **7 年低于 1.58**；2020 0.18 / 2021 0.58 近乎归零，2022 单年 3.56（全期均值 1.64 的 2.2 倍）。
  - 近 3 年均值 1.853（刚过线）；近 3 年 CV **0.829**（REJECT 档）；全期 CV 0.676。
  - **末段衰减 −60%** ⇒ 典型「交替 regime」结构（与 `zq3eb7No` 同类，MEMORY §4 已证此类静态配比不可修 CV）。
- 相关性：self **0.263**（最低，宽度贡献最好）；prod **0.6684 PASS**（16.1h）。
- ΔSharpe **+0.080**（DEU 常规分区 3.30 → 3.38）——低 S（1.65 < 3.30）但仍为正，是「低 ρ 补偿低 S」的 CAP 实证。
- 混腿：`none`（单腿乘积）⇒ 不需三问。
- **结论：REJECT（更正）**——本报告初稿写 CONDITIONAL，与正文「近 3 年 CV 0.829（REJECT 档）」
  自相矛盾。台账 `ledger_kv::robustness_RREwqrNa`（2026-11-08T23:11）判 **REJECT**：
  `Recent-3yr CV_Sharpe 0.68-0.83 >= 0.60（2022 尖峰 3.56 拉高离散度）`。
  ⇒ **提交链 Step 1 会直接拦下**（REJECT 是否决权威，`force` 不适用）。
  即便 ΔS +0.08 是「低 ρ 补偿低 S」的漂亮实证，它的稳健性口径本身不过关。

## 5 被硬闸阻断的两颗（记录留痕）

### `QPvzNNGG` — DEU/TOP500 · ΔS **−0.050**
- 逐年：1.56 / 1.54 / 0.93 / 1.26 / 1.15 / 1.52 / 2.37 / 2.34 / 2.32 / 2.03（近 4 年全 >2.0，CV 0.311 最稳）
- self **0.678**（贴 0.7 线，对已提交 `blRnKEk6`）+ prod .6777 余 .0223
- **ΔS −0.05 ⇒ 按 2026-11-08 硬闸 blocked，`force` 不豁免**。病因：S 1.70 < DEU 常规组合 3.30，且 self 0.678 说明增量信息被自家 `blRnKEk6` 吃掉。
- 这是「IS 看起来最稳但组合边际为负」的教科书案例——**稳健性再好也不能替代 ΔS 闸**。

### `N1NGbddg` — EUR · ΔS **−0.100**
- 逐年：2.76 / 2.15 / 1.50 / 3.21 / **−0.23** / 1.67 / −0.23... / 3.31 / 1.59 / 1.82（2020 负年）
- prod .6872 余 .0128 + self **0.660**
- **ΔS −0.10 ⇒ blocked**。EUR 组合 S 5.48 已极高，S 1.69 的候选无法补偿。
- 混腿 `two_leg`（本需三问，未走到那一步）。

## 6 今日 4 颗建议排布（按 IS 指标排序，**已由 §7.4 点塔优先版取代**）

> 用户 2026-11-09 追加指令：优先点亮未点亮的塔。最终排布见 §7.4 路径 B。

| 顺位 | id | 区 | ΔS | prod 余量 | 三问 | 理由 |
|---|---|---|---:|---:|---|---|
| 1 | `P0obGoQJ` | ASI | +0.730 | .1027 | 不需 | ΔS 与 prod 余量双优；ASI 仅 6 颗 ACTIVE，最空的区 |
| 2 | `akK9ooZv` | GBR | +0.710 | .0718 | **需** | 十年无 <1.58 年、近 3 年 CV 0.092；S/2Y 最高 |
| 3 | `RREPm361` | DEU | +0.730 | **.0119** | **需** | ΔS 最高档；但 prod 薄，提交前须终验 |
| 4 | `RREwqrNa` | DEU | +0.080 | .0316 | 不需 | **已作废：台账 REJECT（见 §4）**。备胎 `mL617YPx` 同样 REJECT（见 §7.3）⇒ 实际只有 2 颗可提 |

**执行注意**：
- `RREPm361` 若终验 prod ≥0.70 ⇒ 直接换 `mL617YPx`（余量 13 倍）。
- 两颗 DEU（`RREPm361` / `RREwqrNa`）互相关 **−0.0014**，同区不构成拥挤。
- 四颗两两 |ρ| ≤ 0.178，与昨日 ASI/DEU 已提交池亦无冲突。

---

## 7 金字塔塔账（Q4，`get_pyramid_alphas` + `get_pyramid_multipliers`）

### 7.1 关键实证：塔计数按季度重置

`get_pyramid_alphas` 的计数**不是累计值，是当季（Q4 = 10/11/12）提交且 ACTIVE 的数量**。

证据：ASI 有 6 颗 ACTIVE，但 `ASI/D1/OTHER` 只计 **2** —— 恰好是 Q4 提交的两颗
（`j28nKkQo` 10-05、`E5ReEnpP` 10-08），另 4 颗是 Q3 及更早（08-02/08-18/09-30×2）。

⇒ **点亮判据 = 当季 ACTIVE ≥ 3**（`category_lit`，2026-09-19 用户定案），每季重新挣。
⇒ Q4 只剩 7 周，现在点塔在窗口内；跨季要重来。

### 7.2 当季塔状态

| 区 | 已点亮（≥3） | 接近点亮（差 1–2 颗） |
|---|---|---|
| **ASI** | **无（0 塔）** | `other` 1.4 → **2/3** |
| **GBR** | model 1.5(6)、pv 1.4(4)、shortinterest 1.2(3)、news 1.6(3)、analyst 1.6(3)、fundamental 1.5(3) = **6 塔** | `other` 1.6 → **1/3** |
| **DEU** | analyst 1.8(5) = **1 塔** | `model` 1.8 → **2/3**、`other` 1.8 → 2/3、`shortinterest` 1.3 → **2/3**、institutions 1.6(1)、fundamental 1.8(1)、sentiment 1.8(1) |
| **EUR** | analyst 1.3(10)、model 1.3(3)、fundamental 1.1(3)、imbalance 1.0(3) = **4 塔** | `pv` 1.1 → **2/3**、insiders 1.1(2)、other 1.5(2)、risk 1.0(2)、sentiment 1.4(2)、news 1.4(1) |

### 7.3 候选 → 塔动作

| id | 塔归属（`pyramids.list`） | 当季 → 提后 | 动作 | 可提交性 |
|---|---|---|---|---|
| **P0obGoQJ** | `ASI/D1/OTHER` 1.4 | 2 → **3** | **点亮**（ASI 首个） | ✅ ΔS +0.73 / prod 余 .1027 |
| **RREwqrNa** | `DEU/D1/SHORTINTEREST` 1.3 | 2 → **3** | **点亮** | ✅ ΔS +0.08 / prod 余 .0316 |
| **mL617YPx** | `EUR/D1/FUNDAMENTAL` 1.1 ＋ `EUR/D1/PV` 1.1 | 3→4 ／ 2 → **3** | **点亮 PV** | ❌ **不可提**：台账 `robustness_mL617YPx` = **REJECT**（2026-10-11，近3CV 0.641，2 轮 repair 16 条变体同判）/ ΔS 0 / CLUSTER 1.18 |
| **akK9ooZv** | `GBR/D1/SHORTINTEREST` 1.2 ＋ `GBR/D1/OTHER` 1.6 | 3→4 ／ 1 → 2 | 推进 OTHER | ✅ ΔS +0.71 / prod 余 .0718 |
| O0AX7Zw1 | 同 akK9ooZv（同族） | 3→4 ／ 1 → 2 | 推进 OTHER | ⚪ 与 ak 同族 ρ .6845 |
| QPvzNNGG | `DEU/D1/MODEL` 1.8 | 2 → 3 | 本可点亮 | ❌ **ΔS −0.05 阻断** |
| RREPm361 | `DEU/D1/ANALYST` 1.8 | 5 → 6 | 塔已亮，**零贡献** | ✅ 但 prod 余 .0119 |
| N1NGbddg | `EUR/D1/INSTITUTIONS` 1.1 ＋ `EUR/D1/ANALYST` 1.3 | 0→1 ／ 10→11 | **点不亮（差 3）** | ❌ ΔS −0.10 阻断 |

### 7.4 两条点塔路径（今日 4 颗）

**路径 B（推荐，1 颗 = 1 个点亮）**

`P0obGoQJ` + `akK9ooZv` + `RREwqrNa` + `mL617YPx`
⇒ 点亮 **3 塔**：`ASI/D1/OTHER`、`DEU/D1/SHORTINTEREST`、`EUR/D1/PV`；`GBR/D1/OTHER` 推到 2/3。
⇒ 无 force、无贴线（4 颗跨 4 区，两两 |ρ| ≤ 0.18）。

**路径 A（备选，倍率更高但要 force）**

`P0obGoQJ` + `akK9ooZv` + `O0AX7Zw1` + `RREwqrNa`
⇒ 点亮 **3 塔**：`ASI/D1/OTHER`、`GBR/D1/OTHER`(1.6，GBR 最高档)、`DEU/D1/SHORTINTEREST`。
⇒ 代价：GBR 两颗同族 ρ **.6845**，第二颗 prod 必贴 .6845（余 .0155）；
第二颗 self .6845 ≥ 0.55 触发分散度软闸，**须 force**，且 ΔS 需在池含第一颗后重算。

**弃 `RREPm361` 的理由**：它是七颗里唯一「塔已亮（ANALYST 5/3）+ prod 余量最薄（.0119）」的，
在点塔维度贡献为零；`mL617YPx` 用同一颗配额换取点亮 `EUR/D1/PV`。

---

## 8 今日实际提交（2026-11-09，用户点名两颗）

用户指令：**「提交 P0obGoQJ，akK9ooZv，免查 prod」**。两颗均单次 POST 成功，平台回 201 async → 轮询翻 **ACTIVE**。

| 项 | `P0obGoQJ` | `akK9ooZv` |
|---|---|---|
| 名称 | `ASI_R_lbl5q60d_01` | `GBR_R_tm15lend_01` |
| 区域 / universe | ASI / MINVOL1M / D1 / SLOW | GBR / TOP700 / D1 / FAST |
| 标签 | `CH_REG` `SRC_dl_riskfree_returns` `CORR_MID` | `CH_REG` `SRC_techindi_model` `CORR_MID` |
| Step 1 submit_gate | passed（RA/PPA fail=0，robustness=PASS 台账命中） | passed（同左） |
| Step 1.2 mix | `none` 单腿，无需三问 | `two_leg`，**三问已答**（holders/polarity/prior） |
| Step 1.4 quota | 0/4 → 4（**平台滞后的低估读法**，见 §9） | 0/4 → 4（同上，真实应为 1/4） |
| **Step 1.6 prod** | **0.5973**，`from_cache=true`，缓存 2026-11-08T18:09（21.5h） | **0.6282**，`from_cache=true`，缓存 2026-11-09T11:34（4.1h） |
| Step 1.7 ΔSharpe | **+0.730**（`EQUITY:ASI:1:POWER_POOL` 2.31→3.04，F 1.37→1.65） | **+0.710**（`EQUITY:GBR:1:POWER_POOL` 3.56→4.27，F 2.45→2.62） |
| Step 1.8 分散度 | `available=false`（平台未回填 is.selfCorrelation）→ fail-open | 同左 fail-open |
| Step 5 prod 恒等式 | 闸门 0.5973 = 平台冻结 0.5973，Δ0.0000 | 0.6282 = 0.6282，Δ0.0000 |
| Step 6 标签处置 | 平台自动追加 `PowerPoolSelected`，`kept` 留痕 | 同左 |
| 平台最终态 | **ACTIVE**，`dateSubmitted=2026-11-09T02:41:01-05:00` | **ACTIVE**，`2026-11-09T02:41:54-05:00` |
| 提交后 self | **0.2815**（pool 6） | **0.5029** |

**「免查 prod」的执行口径**：`_prod_gate` 默认 `refresh=False`（缓存优先），未设
`WQB_PROD_GATE_REFRESH` ⇒ 两颗都命中 48h 内权威缓存，**没有重打平台相关性队列**，
且 `provisional=false`（不是「不知道多久前算的」预读值）。合规语义不变：
读数均 < 0.7，`prod_snapshot` 与平台冻结值逐位一致。

**提交后的池效应**：今日两颗互不相关（跨 ASI/GBR，历史 |ρ| < 0.01），
但会推高同族未提交候选的 prod——`GBR/D1/SHORTINTEREST+MODEL` 一族（`O0AX7Zw1`/`88RxORpX`/
`ZYQv7j2Q`/`58EdlON6`）与 `akK9ooZv` 相关 0.68–0.95，**其余 4 颗永久出局**。

---

## 9 配额闸漏计缺陷（本次实证 + 已修）

**现象**：`akK9ooZv` 提交时报 `ET 今日 REGULAR 0/4 → 剩余 4`，而 `P0obGoQJ` 已在 **67 秒前**
提交成功并 ACTIVE（`dateSubmitted=2026-11-09T02:41:01-05:00`）。真实用量是 **1/4**。

**根因**：
1. `_quota_gate` 只数平台 `stage=OS` 池；
2. 当天刚提交的 alpha 在 **OS 批次开跑前仍留在 `stage=IS`**，OS 池看不到它（约 1 小时后才收录，
   实测 15:44 CST 查 OS 池已含这两颗）；
3. 补一条反向验证：**不传 stage 时 MCP 默认 `stage=IS`**（响应 `next` 链接带 `stage=IS`），
   而 IS 列表按 `-dateSubmitted` 排序时未提交项（null）排在最前，同样捞不到今天的提交。
   ⇒ 「换个查询」补不了，必须另建口径。

**影响**：低估用量 ⇒ 连续提报时会把第 5 颗放过去，白撞平台 403
（不扣配额，但污染 attempt 记录），并让 agent 向用户**误报剩余配额**。

**修法**（`src/wqb/workflow/nodes/submit_alpha.py`）：
- 新增 `_local_today_quota()`：只读打开本地 `submission_ledger`，取当日 `status='ACTIVE'` 行，
  用与平台**同一口径**的 `probe_today()` 计数（ET 日历日、REGULAR/SUPER 分流）。
- `_quota_gate` 取 **`used = max(平台, 本地)`**——**只抬不降**，不会放松既有闸门；
  平台读不到时保持原 fail-open 语义（本地不接管阻断）。
- 测试隔离：pytest 下未显式传库路径时不读生产库（首版实测打挂了
  `test_submit_gate_p0_20261002::test_quota_gate_allows_when_slots_free` 的 `used==1` 断言）。

**验证**：新增 `tests/unit/05_submit_quota/test_quota_gate_local_floor_20261109.py` **8 passed**；
`05_submit_quota` 全量 **283 passed / 1 skipped / 24 errors**（errors 为既有基线：缺 pydantic/mcp/requests）。
真实库读数：`_local_today_quota()` → `regular_used=2`（P0obGoQJ + akK9ooZv），`super_used=0`。

---

## 18:3x 截图 5 颗候选评估（GLB×2 / IND×2 / KOR×1）

截图：`RA候选因子` 面板顺位前 5（顶注「24 颗相关性未测或已超 24h，本轮只验证顺位最前的 5 颗，其余 19 颗留后续」）。
今日 ET 2026-11-09 REGULAR 配额 **2/4 已用、剩 2**（`P0obGoQJ` + `akK9ooZv`）；SUPER 0/1 不适用。

### ★ 截图 Δ 与平台符号相反（第二次复现）

| id | 截图 Δ | 平台 `performance_comparison` ΔSharpe | 分区 |
|---|---:|---:|---|
| `P0oolrZq` | −0.112 | **+0.69** | `EQUITY:GLB:1:POWER_POOL` |
| `vR11NmNr` | −0.083 | **+0.35** | `EQUITY:IND:1:POWER_POOL` |
| `akKGqOmx` | −0.204 | **+0.42** | `EQUITY:KOR:1:POWER_POOL` |
| `rKRRjM51` | −0.082 | **+0.38** | `EQUITY:IND:1:POWER_POOL` |
| `A1VGKqOe` | −0.129 | **+0.53** | `EQUITY:GLB:1:POWER_POOL` |

5 颗 ΔS **全为正** ⇒ 11-08 硬闸全部通过。5 颗 `mix_audit kind=none`（不需三问）。
分散度：`P0oolrZq` self .568 / `rKRRjM51` .6516 / `A1VGKqOe` .5651 均 `dense_justified`（ΔS≥0.02 补偿）放行；`vR11NmNr`/`akKGqOmx` 预检 `unknown` fail-open，后补本地实测 **.6628 / .1549**。
⇒ **按截图 Δ 判死会全批错杀**（11-09 首次实证后的第二次复现）。

### 同族锁死：5 颗只有 3 个独立席位

`compute_mutual_correlation(years=4, threshold=0.7)`：
- `vR11NmNr ↔ rKRRjM51` **0.9485**（两式逐位只差 `ts_zscore` 窗口 252↔504）
- `P0oolrZq ↔ A1VGKqOe` **0.7622**（同为 `rsk60_offer` 门控 + `ohlcv_img` 主腿）
- 其余跨族 |ρ| ≤ 0.0705；最大独立子集 = {`P0oolrZq`, `vR11NmNr`, `akKGqOmx`}

⇒ 每席只留 1 颗；提交后自家兄弟会进 prod 池把另一颗顶过 0.7。

### 稳健性真审（5 颗台账全 `NO_RECORD`，按纪律逐颗补审）

| id | 近 3 年 Sharpe | CV | 衰减比 | 平年 | max/min | 10 年负年 | 判定 |
|---|---|---:|---:|---:|---:|---:|---|
| `P0oolrZq` | 3.30 / 5.07 / 2.40 | **0.309** | 0.70 | 0 | 2.11 | 0 | **PASS**（2020 的 0.49 属早年软标记） |
| `vR11NmNr` | 1.74 / 3.41 / 3.28 | **0.270** | 1.00 | 0 | 1.96 | 0 | **PASS**（10/10 正、最稳） |
| `akKGqOmx` | **0.01** / 2.92 / **5.62** | **0.804** | 2.93 | 1 | 562 | 0 | **REJECT**（CV≥0.60、max/min>5、2021 平年） |

`akKGqOmx` 虽 2Y 4.28 亮眼，但全靠 2022/2023 撑起，2021 完全归零 ⇒ 与 `RREwqrNa` 同型（收益集中单一段），按 Phase C 表单个硬标记即 REJECT。

### prod 缓存时效与终验

| id | 截图 Prod | 权威缓存 | 时龄 | 状态 |
|---|---:|---:|---:|---|
| `P0oolrZq` | 0.66 | **0.6578** `all_passed=true` | 27.7h | ✅ 有效（`refresh=True` 触发后平台挂起 241s、`inflight=true`，按纪律未重复触发，回落缓存） |
| `akKGqOmx` | 0.55 | **0.5459** `all_passed=true` | 44h | ✅ 有效，余量 .154 最大（0.5–0.6 桶仅 1 颗） |
| `vR11NmNr` | 0.67 | 0.674 `stale=true` | **97.6h** | ❌ 作废；终验两次被账号级单并发槽 `holder=corr:get_production_correlation(P0oR7vYw)` 挡回，**未拿到新值** |
| `rKRRjM51` | 0.68 | 74.0h | ❌ 作废（同族淘汰，未重测） |
| `A1VGKqOe` | 0.64 | 97.6h | ❌ 作废（同族淘汰，未重测） |

`P0oolrZq` 直方图 `0.6–0.7` 桶仅 **2 颗** ⇒ 余量 .042 由极少数第三方顶住；今日已提交两颗（ASI/GBR）会进池，终验仍有必要。

### 塔账（当季 ACTIVE，`get_pyramid_alphas`）

| id | 塔 | 当季计数 | 提交后 | 点亮？ |
|---|---|---|---|---|
| `P0oolrZq` / `A1VGKqOe` | GLB OTHER + RISK | other 4 / risk 1 | 5 / 2 | ❌ other 已亮、risk 仍 <3 |
| `vR11NmNr` / `rKRRjM51` | IND PV + INSTITUTIONS | pv 11 / institutions 1 | 12 / 2 | ❌ pv 已亮、institutions 仍 <3 |
| `akKGqOmx` | KOR RISK | risk **2** | **3** | ✅ **唯一能点亮新塔** |

⇒ 截图 5 颗全标「可点新塔」**与平台当季账不符**，实际只有 `akKGqOmx` 能点亮。

### 结论（今日剩 2 个配额）

1. **`P0oolrZq`** — 首提。质量 .652 最高、ΔS +0.69、稳健 PASS、self .568、prod 有效、混腿 none；10/10 正年。塔仅推进 GLB/RISK 1→2，不点亮。
2. **`vR11NmNr`** — 次提，但**前提是先补 prod `refresh=True` 成功**（现 97.6h 作废 + 槽被占）。稳健最稳（CV .270、10/10 正）、ΔS +0.35；self .663 贴线是弱点。塔 IND/INSTITUTIONS 1→2，不点亮。
3. **`akKGqOmx`** — 唯一点亮 KOR/RISK 2→3，且 prod 余量 .154 / self .155 全场最优，**但稳健真审 REJECT** ⇒ 按现行判据不可提；若坚持塔优先，需用户明确豁免 CV 闸（同 `RREwqrNa` 流程）。
4. `rKRRjM51`（与 2 同族 ρ .9485，prod 余量更小、缓存作废）、`A1VGKqOe`（与 1 同族 ρ .7622，各档弱一档、缓存作废）⇒ 让位，标 SUPERSEDED。

**与用户「优先点亮未点亮的塔」指令的冲突**：唯一能点塔的那颗被稳健闸挡住。严守纪律则今日两颗都不点塔；要塔就必须豁免 CV 闸。此张力交由用户终审。

**未提交**（`ALLOW_ALPHA_SUBMIT=False`）；本轮 5 颗稳健性结论仅落本报告，未写 `ledger_kv`（REJECT 具阻断性，待用户确认后再落）。

---

## 19:4x 截图 2 颗 EUR 候选评估（P0oR7vYw / leAnKOEA）

**截图第 2 颗 id 是小写 `l` 开头**：`1eAnKOEA` 返回 404，平台实际为 **`leAnKOEA`**。

两颗同为 `EUR/TOP2500/D1/decay8/CROWDING/nanON` 的三腿 `add` 骨架（analyst + other 双塔，effective=2），RA 全过、IS_LADDER_SHARPE PASS。

### ★ 决定性阻断：ΔSharpe = −0.01（两颗都是）

`tools/gates/mcp_preflight_once.py` 预检：

| id | `mix_audit` | 分区 | ΔSharpe | diversity |
|---|---|---|---:|---|
| `P0oR7vYw` | `three_leg` legs=3, LADDER, 未拦 | `EQUITY:EUR:1`（常规） | **−0.01** | unknown / fail-open |
| `leAnKOEA` | `three_leg` legs=3, LADDER, 未拦 | `EQUITY:EUR:1`（常规） | **−0.01** | unknown / fail-open |

⇒ 命中 11-08 用户明令的 **ΔS<0 硬闸**（Step 1.7，早于 set_properties/POST，`force` 不豁免）。**按现行判据两颗都不该提。**
机理与 MEMORY §2 完全吻合：EUR 常规组合基准 S 5.48 极高，S 2.28/2.05 的候选只能靠极低 ρ 挣增量；两颗 self 0.535/0.462 不够低 ⇒ 挤不出正 ΔS。注意与 18:3x 那批（GLB/IND/KOR 全在 `POWER_POOL` 分区、ΔS +0.35~+0.69）**不可横比**。

### 其余判据（若用户豁免 ΔS 闸才用得上）

| 项 | `P0oR7vYw` | `leAnKOEA` |
|---|---|---|
| S / F / 2Y / TO | **2.28 / 1.61** / 2.42 / 9.24% | 2.05 / 1.39 / **2.48** / **7.15%** |
| sub / inv | 1.46 / 1.79 | 1.28 / 1.77 |
| 平台 checks | CLUSTER_TEST PASS | **CLUSTER_TEST 1.54 < 1.58 WARNING** |
| 近 3 年 | 3.59 / 2.00 / 3.26 | 3.84 / **0.96** / 3.78 |
| **CV(pop)** | **0.232 PASS** | 0.470 CONDITIONAL（max/min 4.0） |
| 衰减比 / 负年 | 1.43 / 0（10/10 正） | 1.84 / 0（2020 的 0.17 属早年软标记） |
| 稳健真审 | **PASS（很干净）** | **CONDITIONAL（不挡，需软标记）** |
| self（本地实测） | 0.535 | **0.462** |
| prod | **0.6881** `all_passed=true`，余量仅 **.0119**（0.6–0.7 桶 9 颗） | 截图 0.6476（余量 .052），但**终验挂起 240s、`last_known=null`、槽被 `WjOZYNEN` 占用**，本地无权威值 |
| 塔 | EUR OTHER 2→**3 点亮** ✅ | 同左（同席只能提 1 颗） |

`compute_mutual_correlation`：两颗 **ρ 0.7837 > 0.7** ⇒ 同一席位，最多提 1 颗。

台账两颗均 `NO_RECORD`，本轮补真审；今日 ET 2026-11-09 REGULAR **2/4 已用、剩 2**。

### 结论

1. **按现行判据：都不值得提交** —— ΔS −0.01 硬闸拦下，`force` 不豁免。要走必须用户明确改判据（同 CV 豁免流程）。
2. 若豁免，**优先 `P0oR7vYw`**：S/F 更高、稳健 PASS CV 0.232、10/10 正年、CLUSTER_TEST PASS、prod 有有效读数。但 prod 余量仅 .0119，且今日两颗新提交会进池 ⇒ **提交前必须 `refresh=True` 终验，>0.7 立即放弃**。
3. `leAnKOEA` 的优势是 prod 余量 .052、self 更低，但稳健只到 CONDITIONAL、CLUSTER_TEST WARNING、且 prod 终验没拿到值；按「prod 贴线时低 prod 变体优先」可作备胎，需先补终验。
4. 两颗都是 `three_leg` 等权 add，若真提还需答三问（holders / polarity / prior，各 ≥8 字符）。

**未提交**（`ALLOW_ALPHA_SUBMIT=False`）。

---

## 21:2x 三颗 DEU 候选复评（RREOz5qn / QPvzNNGG / RREwqrNa）

用户给：RREOz5qn prod .5834「全家族最净」、QPvzNNGG .6777、RREwqrNa .6684「待 CV 豁免」。今日 ET 11-09 REGULAR **2/4 已用、剩 2**。

### 结论：现行判据下 **0 颗可提**

| id | 台账 | ΔSharpe（`EQUITY:DEU:1` 常规） | self | prod（余量 / 缓存时龄） | 阻断 |
|---|---|---:|---:|---|---|
| `RREOz5qn` | **PASS** | **−0.02** | 0.5836 | .5834（.1166 / 4min，最新） | ΔS 硬闸 + 分散度软闸 |
| `QPvzNNGG` | **PASS** | **−0.05** | 0.678 | .6777（.0223 / 23.3h） | ΔS 硬闸 + 分散度软闸 |
| `RREwqrNa` | **REJECT** | 预检 Step 1 即拦，未走到 1.7 | 0.263 | .6684（.0316 / 22.3h） | 台账 REJECT（CV 0.68–0.83） |

`mcp_preflight_once` 三颗逐颗重跑（今日两颗新提交已进池，ΔS 需重算，不能沿用旧读数）：
- `RREOz5qn` ΔS **−0.02**、`QPvzNNGG` **−0.05** ⇒ 命中 11-08 明令硬闸（force 不豁免）。
- 两颗 self 分别 0.5836 / 0.678 均 ≥0.55 且 ΔS<+0.02 ⇒ 同时触发 Step 1.8 分散度软闸（force 可豁免）；预检显示 `diversity unknown / fail-open` 是因平台未回填 `is.selfCorrelation`，本地实测已补上。
- `RREwqrNa` `success=False blocked=True`，reason = `submit_gate blocked: robustness 台账 REJECT`。

### 互测与塔

`compute_mutual_correlation(years=4)`：
- `RREOz5qn ↔ QPvzNNGG` **ρ 0.8711 > 0.7** ⇒ 同席，只能留 1 颗（字段集虽不同：model/analyst vs shortinterest3，日收益仍高度同向）
- `RREwqrNa` 与两者 0.0708 / 0.0199 ⇒ 独立席位
- 最大独立子集 = {`RREOz5qn`, `RREwqrNa`}，正好 2 颗 = 剩余配额

塔账（当季 ACTIVE）：`DEU/D1/MODEL 2`（RREOz5qn → **3 点亮**）、`DEU/D1/SHORTINTEREST 2`（QPvzNNGG / RREwqrNa → **3 点亮**）。

### 若用户明确豁免，优先级

1. **`RREwqrNa` — 唯一「一道豁免即可放行」**。只需豁免 CV 闸（流程预设 `tracking/DEU/atom_orthogonal/submit_staging_RREwqrNa.json`），ΔS 历史 +0.08、self 0.263 全场最低、prod 余量 .0316、塔点亮。
   ⚠ **豁免后必须重测两件**：① ΔS（台账挡住时未走到 Step 1.7，且今日两颗新提交已进池，+0.08 可能漂移甚至转负）；② prod `refresh=True` 终验。
2. `RREOz5qn` — prod 最净、台账 PASS、S1.72/F1.31 最好，但需**两道**豁免：ΔS 硬闸（须改用户明令判据）+ 分散度软闸。且其 self 0.5836 不低 ⇒ **低 prod 不等于高组合增量**，正是 MEMORY §8「相关性/IS 指标不预测贡献」的又一例。
3. `QPvzNNGG` — **淘汰**：ΔS −0.05 最负、self 0.678 贴线、prod 余量 .0223 最薄，且与 RREOz5qn 同席而各项更弱。

**未提交**（`ALLOW_ALPHA_SUBMIT=False`）。台账未改动（RREwqrNa 保持 REJECT，待用户豁免）。

---

## KOR · 21:53 追加：E56jA0AP / QPvx8M1W（非 ATOM 组合线第 7/8 颗候选）

来源：W14 GN-industry 杠杆破壁（§29）。两候选均 MULTI_DATA_SET（anl10×rsk68 / anl10×insd5），走 IS Ladder 路径。Phase B 归因 + Phase C 反过拟合闸如下。

### QPvx8M1W — **PASS**
- 表达式：`group_neutralize(hump(subtract(group_rank(ts_av_diff(anl10_smartest_sal_fy2_pred_surps_v1,300),sector),group_rank(ts_delta(rsk68_weight_dadv,66),sector)),hump=0.003),industry)`
- 指标：S1.67 / F1.54 / 2Y2.02 / TO8.62% / margin24.5bp / sub1.64 / fRA=0 / fail=[]。（margin 原记 2.45bp 系 ×1000 单位错，已更正，下同）
- 逐年 2014–2023 无空窗（longCount>0/pnl≠0）；最近3年 [1.36,2.42,1.52] mean1.767≥1.58、CV0.264<0.40、衰减比0.91、平年0、max/min1.78。
- self corr 0.6447 PASS；互相关对篮子+E56 全对<0.7（max0.6435，E56↔QPvx0.6245）；边际 ΔSharpe **+0.28**（4.41→4.69，dilutive=false）。
- 软标记：仅算子数7>5；margin24.5bp≥5bp PASS。经济含义一句话可写（分析师营收惊喜长窗水平 − 风险模型交易权重漂移，industry 中性化残差）。
- **欠项：prod 读数**（账号级死锁，E56 排队优先）。

### E56jA0AP — **CONDITIONAL**（边界，呈用户终审）
- 表达式：`hump(subtract(group_rank(ts_av_diff(anl10_smartest_sal_fy2_pred_surps_v1,250),sector),group_rank(ts_mean(vec_stddev(insd5_vol_chg),55),sector)),hump=0.003)`
- 指标：S1.58 / F1.41 / 2Y2.15 / TO6.6% / margin30.0bp / sub1.65 / fRA=0。
- 逐年无空窗；最近3年 [2.13,3.57,1.18] mean2.293≥1.58、衰减比0.747、平年0。
- **两项 CONDITIONAL 带**：CV_Sharpe **0.428**∈[0.40,0.60)、max/min **3.03**∈(3,5]——均由 **2022 单年 3.57** 驱动，非多年失稳。
- self corr 0.6074 PASS；边际 ΔSharpe **+0.19**（dilutive=false）。
- 处置：E56 是该双腿族**唯一双达标前沿点**（§28.2 实证），repair 编辑预期破坏信号 ⇒ **不盲修**，CONDITIONAL 如实落台账，交用户终审（接受边界软标记并在 prod 解槽后逐颗确认提交，或指示一轮 repair）。
- **欠项：prod 读数**（死锁 ~6.5h）。

### 共性
- 两候选 prod 均待平台账号级单飞槽解死锁；`submit_verdict` 均 UNVERIFIABLE_404（GET /submit 恒404，真闸=prod<0.7+用户确认）。
- 台账已写 `robustness_QPvx8M1W=PASS`、`robustness_E56jA0AP=CONDITIONAL`。**未提交**（提交不可逆，须用户逐颗明确确认）。

---

## KOR · 22:32 追加：4 颗提交就绪 ATOM 首审（robustness 闸补账）

触发：§33 边际预检后 4 颗就绪，但提交链还欠 robustness 台账。逐颗 Phase B（逐年+指标取证，MCP）+ Phase C（近 3 个 IS 年口径，population CV）。

| alpha | 数据集 | last3 S | mean | CV | 衰减比 | max/min | margin/TO | 判定 |
|---|---|---|---|---|---|---|---|---|
| omERn83n | risk70 | [1.48,3.74,0.98] | 2.067 ✓ | **0.581** | 0.605 ✓ | **3.82** | 11.5bp/13.2% | **CONDITIONAL** |
| qMLOooX1 | analyst10 | [3.66,2.95,0.69] | 2.433 ✓ | 0.520 | 0.356 ⚠ | **5.30 >5** | 20.7bp/9.7% | **REJECT**（本轮不合格） |
| d5Wvpmbx | risk68 | [0.94,3.46,4.69] | 3.030 ✓ | 0.515 | **2.58 增强** | 4.99 边界 | 9.4bp/24.6% | **CONDITIONAL** |
| ZYQ116ln | intraday_pv_feats | [1.32,2.77,0.98] | 1.690 ✓ | 0.459 | 0.527 | 2.83 ✓ | 7.0bp/22.1% | **CONDITIONAL** |

**qMLOooX1 REJECT 详情**：2021→2023 逐年 3.66/2.95/0.69 单调衰减，2023 年 Sharpe 不足 0.7——「近年失效现场」正是本闸要拦的形态（平台 S2Y=1.76 靠 2022 尾段撑过，掩盖衰减）。其 ΔS+0.23 亦系四颗中已被证实的矛盾点：本闸 fail-closed 拦截，出路三选一呈用户——①repair（放缓 sal/net 双 surps 腿治 2023 衰减，≤2 轮复审）②明令放宽留痕（soft_flags 记「按用户指令放宽」）③暂缓。

**共性形态**：4 颗 + E56 的 2023 年普遍走弱（0.69–1.52），唯 **d5Wvpmbx 2023=4.69 逐年增强**（risk68 波动-活跃度价差，KOR 2023 拥挤交易出清叙事）——其 ΔS+0.47 亦为全池最强，**优先级应最高**。CONDITIONAL 不阻断提交（仅 REJECT fail-closed），软标记已入台账，提交描述三段将如实带出。

**未审**：LLZ6wZO2（diversity 闸前置阻断，无需进提交链）。**未提交**（全部只读审计）。

---

## KOR · 22:34 追加：9qxnYPjd（E56 同机制字段替换救援代表，第 8 颗候选）首审 **PASS**
- 逐年 [0.38,0.84,1.62,2.48,1.52,2.28,0.20,2.28,3.29,1.45]，10 年无空窗；last3 [2.28,3.29,1.45] mean2.34 ✓、**CV 0.322 PASS**、衰减比 0.918 PASS、max/min 2.27 PASS、平年 0。
- margin 30.2bp≥5bp PASS；算子 7；经济解释一句可立（pre 预期惊喜水平 − 内部人申报量分歧的 sector 价差）。
- **优于母件**（E56 CV 0.428 CONDITIONAL 系），逐年形态更稳。欠项仅 **prod**（busy 排队，~22:47 复查）。prod<0.70 ⇒ 第 8 颗全链闭环呈用户。



---

## 22:2x 截图 5 颗 KOR 候选评估 —— 截图「就绪」漏了 prod 与台账

**id 坑**：截图 `d5WVpmbx`（大写 V）平台 404，实际为 **`d5Wvpmbx`**（小写 v）。5 颗全 `KOR/TOP600/D1`、RA 全过、平台 `failed_ra=0`。

### 复核结果

| id | 数据集 | 截图结论 | ΔS（平台，`KOR:1:POWER_POOL`） | 台账 | self | prod | 判定 |
|---|---|---|---:|---|---:|---|---|
| `d5Wvpmbx` | risk68 | 就绪（最强增量） | **+0.47** | CONDITIONAL | — | **0.9081 FAIL** | ❌ 判死 |
| `ZYQ116ln` | intraday_pv_feats | 就绪 | +0.24 | CONDITIONAL | **0.143** | 0.6981（余量 **.0019** / 33h） | ⚠ 唯一候选，终验未成功 |
| `qMLOooX1` | analyst10 | 就绪 | +0.23 | **REJECT** | — | 79.7h stale | ❌ 判死 |
| `omERn83n` | risk70 | 就绪 | +0.10 | CONDITIONAL | 0.421 | 77.4h **stale** + 终验挂起 | ⚠ 需补 prod |
| `LLZ6wZO2` | oth466 | diversity 阻断 | +0.0000 | 旧账（self=prod=.6762 撞 `0mrnWojG`） | 0.676 | 0.6762 | ❌ 分散度 blocked |

`mcp_preflight_once.py` 复核：ΔS 与截图**逐位一致**（+0.47/+0.24/+0.23/+0.10/0.0000，全在 PP 分区），`mix_audit kind=none` 无需三问。**但截图只跑了 submit_gate + ΔS，没跑 prod / 稳健台账 / 逐年**，故 4 个「就绪」里 2 个判死、2 个待补。

### 三个决定性发现

1. **第一名 `d5Wvpmbx` prod 0.9081 FAIL**（`all_passed=false`，直方图 0.9–1 桶 1 颗）。原因见 MEMORY §2：自家 `kqN92KpK` 进 prod 池把同族从 0.6906 顶到 0.9081。台账还标着「ΔS+0.47 全池最强增量——质量最高」，但 **prod 是硬闸，增量再强也不豁免**。与上一轮「prod 低 ≠ ΔS 高」正好构成反面对照。
2. **`qMLOooX1` 台账 REJECT**：`Recent-3yr max/min=5.30>5`（2021 3.66 → 2022 2.95 → 2023 0.69 连续衰减），预检 `success=False blocked=True`。截图完全未显示。
3. **`ZYQ116ln` prod 0.6981 余量仅 0.0019**，而今日已提交 `P0obGoQJ`/`akK9ooZv` 会进池 ⇒ 大概率已被推过 0.7。`refresh=True` 触发后平台挂起 241s（`inflight=true`，按纪律未重复触发），回落缓存仍 0.6981 `all_passed=true` 但**终验没拿到新值** ⇒ 不能按旧缓存提。

### 其余判据

- 互测：5 颗**全独立**（最大 ρ 0.2586 `qMLOooX1↔omERn83n`），无同席问题。
- 塔账 `KOR/D1`：`PV 2`（`ZYQ116ln` → **3 点亮**）、`RISK 2`（`d5Wvpmbx`/`omERn83n` → **3 点亮**）；`ANALYST 3`/`FUNDAMENTAL 3` 已亮。
- 台账 CONDITIONAL 软标记：`ZYQ116ln` CV 0.459、衰减比 0.527 贴 0.50、算子 3 最简；`omERn83n` CV **0.581 贴 0.60**、max/min 3.82、算子 9；`d5Wvpmbx` CV 0.515、max/min 4.99。
- `LLZ6wZO2` 预检 `diversity blocked`：self 0.6760 + ΔS 0.0000 <0.02 ⇒ 占相关预算却证明不了贡献（与截图一致）。
- 今日 ET 2026-11-09 REGULAR **2/4 已用、剩 2**。

### 结论

**严格按现行判据，0 颗可立即提交。**
- `d5Wvpmbx` / `qMLOooX1` / `LLZ6wZO2` ⇒ 弃（prod FAIL / 台账 REJECT / 分散度）。
- `ZYQ116ln` ⇒ 唯一「prod 有效且全闸过」的候选（self 0.143 全场最低、ΔS +0.24、PV 塔点亮、算子 3），但**必须等 prod 终验成功且 <0.7** 才能提；余量 .0019 下大概率 FAIL。
- `omERn83n` ⇒ 备选，需先补 prod 终验（77.4h stale），且 CV 0.581 贴线。

**未提交**（`ALLOW_ALPHA_SUBMIT=False`）。

---

## 23:1x 截图 3 颗 EUR risk60 借券费率族 —— **评估过，但族级 prod 深墙判死**

用户问「这 3 颗评估过吗」。答：**评估过 IS 与 prod 墙，但从未进提交评审链**；本次补齐实测后三颗全部判死。

### id 校正（今日第四次形近字符坑）

| 截图 | 平台实际 | 校验 |
|---|---|---|
| `qML2RxrZ` | `qML2RxrZ` | ✅ 一致 |
| `zYQVJj8n` | **`ZYQVJj8n`**（首字母大写 Z） | `zYQVJj8n` 404 |
| `2rAWW7eW` | **`2rAVV7ew`**（`W`→`V`、尾部 `W`→`w`） | `2rAWW7eW` 404 |

三颗均 `EUR/TOP2500/D1/SUBINDUSTRY/trunc0.08/nanON`，同族 `rsk60_last` 翻号 + `group_zscore(country)` + `ts_mean(...,5)`；`qML2RxrZ` 与 `ZYQVJj8n` **代码逐位相同，只差 decay 8 / 4**，`2rAVV7ew` 只少一层 `signed_power(1.5)`。

### 已评估过的部分（今天 14:42–14:51，EUR 挖掘战役）

来源 `tracking/EUR/WAVE_LEDGER.md` §S4「降 prod 备选批 A/B」；`results/prod_peek_2rAVV7ew.json`（11-09 14:51）。
IS 指标与截图逐位吻合（1.62/1.48/2.39/6.19%/33.86bp/fRA0；1.58/1.44/2.38/7.48%/27.96bp/fRA0；1.56/1.31/2.28/6.74%/26.22bp/fRA1）。
**这是挖掘产线内部的选优，不是提交评审** ⇒ 三颗都不在 22:5x 那份 40 颗总清单里。

### 本次新增实测（决定性）

| id | prod | RA | 稳健逐年 | 台账 | 互测 |
|---|---:|---|---|---|---|
| `qML2RxrZ` | **0.8608 FAIL**（computed） | fRA=0，`CLUSTER_TEST 1.3` W | 近3 [1.98, 2.99, 1.77] **CV 0.237 PASS**、10/10 正年、衰减比 1.09、max/min 1.69 | `NO_RECORD` | ρ .9952 / .9799 |
| `ZYQVJj8n` | **0.8707 FAIL**（computed） | fRA=0，`CLUSTER_TEST 1.2` W | 未取（同族同形） | `NO_RECORD` | ρ .9952 / .9794 |
| `2rAVV7ew` | **0.9156**（peek；本地权威缓存 null、`inflight=true`） | **fRA=1 = `LOW_SHARPE 1.56 < 1.58`**（`checks.fail=[]` 但 `ra_failed=true`） | 台账已逐年：10 年零空窗零负年 | `NO_RECORD` | ρ .9799 / .9794 |

**三颗全撞 prod 硬闸（>0.7）**，且 ρ 0.979–0.995 ⇒ **三颗只有 1 个席位**（`max_mutually_below_subset = [qML2RxrZ]`）。

### 两个结案结论

1. **台账悬案「`group_scale` 能否改变 PC 路径」= 不能**。`ZYQVJj8n` 是唯一解耦尝试，实测 prod **0.8707** 仍在深墙。降 prod 全套杠杆（group_scale −0.057 / 幂次 −0.027 / ts_mean 窗 5→66 / decay 4→8）在这族**全部无效**，只把 S 从 1.56 推到 1.62，prod 一档没动 ⇒ 坐实 MEMORY §10「单信号字段集高 prod 不可逆，prod 由列定不由形定」。
2. **稳健性救不了 prod**：`qML2RxrZ` 的 CV 0.237 是今天所有候选里最好的档之一，但 prod 0.8608 直接一票否决。塔位也无效——三颗都是 `EUR/D1/RISK`（当季 2/3，本可点亮），prod 硬闸优先于塔。

### 结论

**3 颗都不值得提交，不进可提交排序清单**，也无需再补 ΔS / 稳健台账 / prod 终验（终验只会把 0.86–0.92 重算一遍）。
`2rAVV7ew` 更是一开始就 `failed_ra=1`，连 RA 闸都没过。
要在这方向继续产出，唯一出路是**换信息源**（换读数族 / 新数据集），不是继续在这张 `rsk60` 面板上变形。

**未提交**（`ALLOW_ALPHA_SUBMIT=False`）。

---

## 10 追加提交（2026-11-10 02:2x CST = ET 11-09 13:18）

用户点名提交，判据「同等绩效下算子越少越好 = 硬指标」⇒ 取 7-ops 压缩件 `rKRx2Alj`（`mLovbnm2` 8 ops 的 `multiply` 变参 + `ts_sum` 版）。

| 项 | 值 |
|---|---|
| 名称 / 状态 | `DEU_R_anlrev3_01` / **ACTIVE** / `stage=OS` / `dateSubmitted 2026-11-09T13:18:39-05:00` |
| 平台算子数 | **7**（`regular.operatorCount`） |
| IS | S1.95 / F1.80 / 2Y2.23 / `IS_LADDER_SHARPE` PASS(2.23≥2.02) / `CLUSTER_TEST` 1.64 PASS / `failed_ra=0` |
| prod / self / ΔS | **0.6561**（冻结值 ≡ 闸门，Δ0.0000）/ 0.5634 / **+0.68**（`DEU:1:POWER_POOL`） |
| 台账 / 混腿 | `robustness_rKRx2Alj`=CONDITIONAL / `mix_audit kind=none` 免三问 |
| 塔 | `DEU/D1/MODEL`(1.8) + `DEU/D1/ANALYST`(1.8)，effective=2 |
| 标签 | `CH_REG` `SRC_analyst_estimate_revision` `CORR_MID`；平台**未挂** `PowerPoolSelected` |

`refresh=True` 终验被账号级槽 busy 挡回（holder `MPYEEwj8`），但 02:09:45 本轮实算的 0.6561 仅 0.14h、`stale=false`、`inflight=false` ⇒ 按纪律未重复触发；Step 5 快照恒等式 Δ0 已验证。
同族 `mLovbnm2`(8ops) / `2rAYpJKx`(7ops) 互相关≈1 ⇒ SUPERSEDED。
ET 11-09 REGULAR **3/4 已用、剩 1**；SUPER 0/1。详见 `output_report/opmin_mlovbnm2_20261110.md` 与当日日志。
