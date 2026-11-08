# S0 · KOR Risk 全数据集扫描（2026-11-06）

> 来源：MCP `get_datasets(region=KOR, delay=1, universe=TOP600, category=risk)` → **count=7**（平台全量，无遗漏）
> 字段：MCP `get_datafields(dataset_id=..., region=KOR, universe=TOP600, delay=1, **filter_sharpe=false**)`
> 设置基准：KOR / TOP600 / Delay=1（平台唯一合法 universe = TOP600，`get_platform_setting_options` 实测）

## 1. 七个 Risk 数据集总表

| # | dataset | 名称 | 字段 | 类型 | cov | aC | user | 历史结论（证据出处） | 本轮裁定 |
|---|---|---|---:|---|---:|---:|---:|---|---|
| 1 | **risk70** | Multi-Factor Model (MFM2 / ASETRD) | **96** | MATRIX | .967 | **8018** | 1230 | 只测过 8 腿、全打在 `srisk/srisku` IVOL 轴（max\|S\| **0.73**）；路线图复核 §「③ 最优 S 已超闸值 40% 豁免线 ⇒ 应重开」；`risk70.md` §6.3 明确写「下一步该打载荷轴」 | ⭐ **主攻** |
| 2 | **risk88** | Other Multi-Factor Risk Models (MFM ASE1) | **64** | MATRIX | .967–1.0 | 1418 | 495 | 只测过 `ri_*` 9 个风格载荷的裸横截面（dead_end `KOR-RSK88-STYLOAD-WEAK`）；`rsk88_mfm_ase1_dsrt`(aC297) / `srisk`(102) / 50 个 `ind_*` 从未测 | ⭐ **次攻（独立模型口径）** |
| 3 | **risk59** | Securities Lending & Short Market Dynamics | 16 | **VECTOR** | .9806 | 564 | 222 | level 族上界 **1.04 / 2Y 2.02**（`d5W8Pn7X`）；variance 族 0.39；**2014 整年零数据（仅 9 年）** | ⚠ **备选**（十年覆盖不达标，用户约束 6 存疑） |
| 4 | risk60 | Securities Lending Insight | 5 | **VECTOR** | 1.0 | 211 | 83 | `KOR-RISK60-CROWDING-NOSIGNAL`：水平 S −0.06、时序 z-score −0.18 | ✗ 判死（不重开） |
| 5 | risk68 | Forecast Data (vol/beta/ADV 权重) | 5 | MATRIX | .9914 | 770 | 347 | 4/4 全灭 max\|S\| 0.50；W7 成交量加速比 0.66 / 2Y −0.07 | ✗ 判死（不重开） |
| 6 | risk71 | Daily Specific Return Profiling | 7 | MATRIX | .6658 | 349 | 152 | `KOR-RISK71-RESIDUAL-REVERSAL-2Y-DEAD`：2Y 修法九种全灭；全族 2Y ≤0.16 | ✗ 判死（不重开） |
| 7 | risk72 | Specific return of extended factors | 5 | MATRIX | .6246 | 402 | 164 | 5 字段 description 逐字相同（同一 `dsrt` 的 5 个宇宙拷贝）⇒ 0 槽 | ✗ 不投 |

## 2. 字段级事实（本轮实拉，`filter_sharpe=false`）

### 2.1 risk70 — 96 字段的三层结构

| 层 | 条数 | 字段形态 | 经济角色 | 可否作信号 |
|---|---:|---|---|---|
| **A 风格载荷** | 27 | `rsk70_mfm2_asetrd_<style>` | 个股对 MFM2 风格因子的**回归载荷**（可正可负、无量纲） | ✅ 主战场（但注意 STATISTICAL 中性化会剥离） |
| **B 行业载荷** | 20 | `rsk70_mfm2_asetrd_<industry>` | 行业因子载荷（近乎 0/1 哑变量） | ⛔ 只作分组轴 |
| **C 特异风险 / 收益** | 4 | `srisk` / `srisku` / `resvol` / `dsrt` | 年化特异风险 `%²`（3 支）+ 特异收益（1 支） | ⛔ `srisk/srisku/resvol` 已实测 0.57/0.73 判死；`dsrt` 与 risk71/72 同源 |
| **D 风险模型辅件** | 21 | `sector_exposure_*`(21) / `*_flag` / `apacm6_total_market_cap_usd` / `current_market_cap_usd` | 分组轴 / 规模轴 / 国家哑变量 | ⛔ 仅作分组或规模壳 |
| **E 非载荷经济字段（★ 从未测）** | **8** | `hedge_fund_ownership_percentage`(aC22) / `hedge_fund_number_owners`(20) / `sector_relative_momentum`(22) / `short_term_industry_country_factor`(44) / `broad_market_exposure_factor`(10) / `country_adjustment_factor_2`(12) / `industry_adjustment_factor_3`(13) / `us_equity_short_interest_ratio`(10) | **对冲基金持股、行业内相对动量、短周期行业×国家因子** | ✅ **本轮新增攻击面** |

### 2.2 risk70 风格载荷 · 按 alphaCount 降序（0.1 质量先验 TOP30 摘要）

| # | 字段 | aC | users | 描述 |
|---|---|---:|---:|---|
| 1 | `rsk70_mfm2_asetrd_anlystsn` | **2922** | **622** | Analysts' Sentiment Style Factor Loading |
| 2 | `rsk70_mfm2_asetrd_earnyild` | **1795** | **582** | Earnings Yield Style Factor Loading |
| 3 | `rsk70_mfm2_asetrd_srtindcnt` | **1431** | 225 | Industry factor loading |
| 4 | `rsk70_mfm2_asetrd_dsrt` | 1063 | 252 | Specific returns（⛔ 死） |
| 5 | `rsk70_mfm2_asetrd_resvol` | 1006 | 231 | Residual Volatility Style Factor Loading |
| 6 | `rsk70_mfm2_asetrd_btop` | 794 | 248 | Book-to-Price Style Factor Loading |
| 7 | `rsk70_mfm2_asetrd_season` | 703 | 107 | Season Style Factor Loading |
| 8 | `rsk70_mfm2_asetrd_earnvar` | 607 | 121 | Earnings Variability Style Factor Loading |
| 9 | `rsk70_mfm2_asetrd_srisku` | 588 | 189 | Unadjusted initial specific risk（⛔ 死） |
| 10 | `rsk70_mfm2_asetrd_growth` | 551 | 157 | Growth Style Factor Loading |
| 11 | `rsk70_mfm2_asetrd_invsqlty` | 530 | 123 | Investment Quality Style Factor Loading |
| 12 | `rsk70_mfm2_asetrd_size` | 508 | 132 | Size Style Factor Loading |
| 13 | `rsk70_mfm2_asetrd_beta` | 499 | 150 | Beta Style Factor Loading |
| 14 | `rsk70_mfm2_asetrd_srisk` | 473 | 150 | Final specific risk（⛔ 死） |
| 15 | `rsk70_mfm2_asetrd_profit` | 467 | 107 | Profit Style Factor Loading |
| 16 | `rsk70_mfm2_asetrd_momentum` | 460 | 123 | Momentum Style Factor Loading |
| 17 | `rsk70_mfm2_asetrd_ltrevrsl` | 434 | 127 | Long-Term Reversal Style Factor Loading |
| 18 | `rsk70_mfm2_asetrd_cnt_kor` | 428 | 117 | South Korea Country Factor Loading |
| 19 | `rsk70_mfm2_asetrd_indmom` | 427 | 102 | Industrial Momentum Style Factor Loading |
| 20 | `rsk70_mfm2_asetrd_othermat` | 425 | 128 | Other Materials Industry Factor Loading |
| 21 | `rsk70_mfm2_asetrd_leverage` | 416 | 120 | Leverage Style Factor Loading |
| 22 | `rsk70_mfm2_asetrd_midcap` | 414 | 94 | Midcap Style Factor Loading |
| 23 | `rsk70_mfm2_asetrd_indadj` | 307 | 101 | Industry factor loading |
| 24 | `rsk70_mfm2_asetrd_divyild` | 274 | 108 | Dividend Yield Style Factor Loading |
| 25 | `rsk70_mfm2_asetrd_earnqlty` | 255 | 86 | Earnings Quality Style Factor Loading |
| 26 | `rsk70_mfm2_asetrd_cntadj` | 249 | 93 | Country adjusted factor loading |
| 27 | `rsk70_mfm2_asetrd_shortint` | 248 | 91 | Short Interest Style Factor Loading |
| 28 | `rsk70_mfm2_asetrd_strevrsl` | 199 | 77 | Short-Term Reversal Style Factor Loading |
| 29 | `rsk70_mfm2_asetrd_primaryindustry` | 126 | 56 | Industry factor loading |
| 30 | `rsk70_mfm2_asetrd_metals` | 130 | 55 | Metals Industry Factor Loading |

**★ 0.1 读数**：头部 = `anlystsn`（αC 2922 = 第 2 名的 1.6 倍 = `srisk` 的 6.2 倍）
⇒ **该集最强经济轴是「分析师情绪风格载荷」，不是特异风险**。wave 214 恰恰只打了特异风险轴 ⇒ **方向从第一波就偏了**。
（`risk70.md` §0 已记录同一纠偏，但 wave 215 从未派发，本条至今未验证。）

### 2.3 risk88 — 64 字段的两层结构

| 层 | 条数 | 字段 | aC 范围 | 说明 |
|---|---:|---|---:|---|
| 风格载荷 `ri_*`（Barra 经典 9 因子） | 9 | `ri_value`(**247**) / `ri_volatility`(98) / `ri_growth`(85) / `ri_divyield`(73) / `ri_momentum`(53) / `ri_size`(52) / `ri_beta`(39) / `ri_nonlsize`(34) / `ri_leverage`(30) | 30–247 | 与 risk70 是**两个独立 vendor 模型**（ASE1 vs MFM2） |
| 行业载荷 `ind_*` | 50 | `rsk88_mfm_ase1_ind_*` | 3–70 | 哑变量型，只可作分组轴 |
| 特异量 | 2 | `rsk88_mfm_ase1_dsrt`(297) / `rsk88_mfm_ase1_srisk`(102) | 102–297 | `dsrt` 与 risk71/72 同源（⛔）；`srisk` 未测 |
| 辅件 | 3 | `alternative_market_cap_usd`(44) / `rsk88_mfm_ase1_market`(12) | 12–44 | 规模 / 市场成员哑变量 |

## 3. 候选裁定与理由

### ⭐ risk70（主攻）—— 三条独立理由
1. **头部轴从未被测**：αC 2922 的 `anlystsn` 与 αC 1795 的 `earnyild` 都从未进入任何一波（wave 214 只测 `srisk/srisku`）。
2. **8 个非载荷经济字段从未被测**：`hedge_fund_*`（smart money 持股）、`sector_relative_momentum`（行业内相对动量）、
   `short_term_industry_country_factor`（短周期行业×国家因子）都带独立经济含义，且 aC 10–44（**低拥挤**）。
3. **本轮换模板**：wave 214 用的是裸 `group_rank(ts_backfill(F,5), sector)`；本轮改用 KOR 已验证的
   **P-ATOM-1**（`signed_power ∘ winsorize ∘ group_rank ∘ ts_backfill` + `ts_target_tvr_decay`，shortinterest 实测 S 2.09）。

### ⭐ risk88（次攻）—— 独立模型口径
`ri_*` 已判死的是**裸横截面**；但 (a) `rsk88_mfm_ase1_srisk` 从未测，(b) 载荷**变化率**（style drift）从未测，
(c) ASE1 与 MFM2 的**同义载荷差分**（`ri_value` − `btop`）是跨模型测量分歧，属新机制。
⇒ 作为 risk70 的**平行对照模型**，用于验证「风格载荷在 KOR 是否有可交易残余」，且两集互不抢占 self 池。

### ⚠ risk59（备选，暂不主攻）
上界 1.04 / 2Y 2.02 是本塔唯一「近闸」件，但 **2014 整年 `longCount=0`**（数据自 2015 起，仅 9 年）
⇒ 违反用户约束 6「近十年都要有数据」。**只在 risk70/risk88 全部无计可施时才回补**，并须在交付里显式标注覆盖缺陷。

### ✗ 明确不投（继承判死，命中即禁入 quota）
risk60 / risk68 / risk71 / risk72 —— 判死证据充分（各自 ≥2 条独立读数），且都不满足「最优 S > 闸值 40%」的复核豁免线
（risk60 0.18 / risk68 0.66 / risk71 2Y 0.16 / risk72 0 槽）。

## 4. 用户约束映射

| 约束 | 本扫描的处置 |
|---|---|
| 固定 KOR | 全部 `region=KOR / TOP600 / delay=1`，不换区不换 universe |
| 不频繁切数据集 | 先吃透 risk70（96 字段 / 5 层结构），risk88 只作独立模型对照；risk60/68/71/72 直接继承判死，不消耗配额 |
| Risk 类 | 全部 7 个候选均 `category=risk`（塔乘数 1.3，KOR 该塔 0/3 未点亮） |
| 禁 PV/MODEL/OTHER 两两组腿 | 本轮全部 **单数据集 ATOM**；`risk70 + risk88` 属同类别（risk×risk），不在禁止域内，且为本轮唯一允许的组合形式 |
| 近十年有数据 | risk70/risk88 cov .967、2014–2023 覆盖待 `yearly_stats` 实测确认（risk70 wave214 实测 longCount 295–344/年 ✅）；risk59 2014 空年 ⇒ 降级 |
| 并发 2 | `create_multi_simulation` 同时最多 2 批在飞 |
| prod 用 MCP | `check_correlation(correlation_type="production", refresh=True)`；self 用 `check_self_correlation`（本地，不占槽） |
