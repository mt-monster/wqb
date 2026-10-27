# Robustness 归因报告（2026-10-24）— USA × insider_trx_matrix w9 交付候选

判定依据：`brain-alpha-robustness` Phase B/C（近窗制度：最近 3 个 IS 年为主判定）。
区域 USA / 宇宙 TOP3000 / delay 1 / decay 5 / truncation 0.08 / IS 2014-01-01–2023-12-31。
本波背景见 `tracking/USA/runs/usa_insd_trx_w9_notes.md`（w8 唯一存活臂 prod 0.6993 仅余 0.0007，w9 换内层分组轴加固）。

## 候选：`0mjaa2Ev`（sector 内层轴 + SLOW_AND_FAST 中性化，w9 赢家）

- 表达式：`group_neutralize(ts_zscore(ts_sum(total_top_secondary_buy_transaction_count, 126), 252), sector)`
- IS：S **3.24** / F **2.60** / 2Y **4.30** / TO 0.1622 / returns 10.46% / DD 2.91% / margin 12.9bp
- 相关性（`check_correlation(refresh=True)` 实测）：prod **0.6460** ✓ / self **0.0890** ✓（OS 池 135）
- 篮子两两（`compute_mutual_correlation`，4 年）：与 `O0Jgd7Y7` 0.3114 / `88vXxaqv` 0.4031 / `LL53QVvn` 0.4599 / `d5KzLo7v` 0.1203 ⇒ 全部 < 0.70 ✓
- WebDataScope：RA 全 PASS（`checks.fail = []`），failed_ra 0 / failed_ppa 0，无 RA 项 PENDING ✓
- 逐年 Sharpe：2014 3.75 / 2015 2.78 / 2016 1.93 / 2017 4.04 / 2018 4.32 / 2019 3.25 / 2020 2.06 / 2021 2.12 / 2022 4.62 / 2023 3.97
  - Recent-3yr（2021–23）：**2.12 / 4.62 / 3.97**，全正且 > 0.3，均值 **3.57** ≥ 1.58 ✓
  - CV_Sharpe = **0.297**（总体 sd）/ **0.363**（样本 sd）< 0.40 ✓（两种口径都 PASS）
  - 衰减比 = 3.97 / 3.24 = **1.225** ≥ 0.50 ✓；max/min = 4.62/2.12 = **2.18** ≤ 3 ✓；平年 **0** ✓
  - 最弱年 2016 = 1.93（全历史无 < 0.3 年）
- Sub-universe：平台 `LOW_SUB_UNIVERSE_SHARPE` **PASS**（1.40；limit ≈ 1.403，SubU/S = **0.432**）✓ **贴线**
- Margin @ turnover：整体 12.9bp @ TO 16.2%；逐年 6.92–20.19bp，最低 2016 6.92bp ≥ 5bp ✓
- 回撤日历（2494 个日频 PnL 点，40 个季度，book 20M）：
  - 平均季回撤 **0.596%**，最大季回撤 **1.455%（2021Q1）**
  - 超过 2× 平均的季度仅 **1 个**：2021Q1（1.455%）⇒ 软标记
  - 次高：2018Q4 1.177% / 2021Q3 1.063% / 2020Q3 1.043%
- 相对池贡献（`performance_comparison`，EQUITY:USA:1:POWER_POOL）：加入后池 Sharpe **4.37 → 5.53**、池回撤 0.98% → 0.86% ⇒ 边际贡献为正 ✓
- Top-5 个股集中度：MCP 的 PnL 接口不返回逐股分解 ⇒ **未测**（软标记，非 REJECT 项）
- 算子数：3（`ts_sum` / `ts_zscore` / `group_neutralize`）✓
- 经济可解释性：**内部人二级市场增持笔数（126 日累计）相对自身 252 日历史的 z-score，行业中性化**——内部人买入是管理层私有信息，市场对持续性增持反应不足 ⇒ 一句话可写 ✓
- **判定：PASS**（软标记：SubU 贴线 0.432；2016 margin 6.92bp；2021Q1 单季回撤超 2× 均值）

## 同波备选：`LL522ZRe`（industry 内层轴 + REVERSION_AND_MOMENTUM）

- 表达式：`group_neutralize(ts_zscore(ts_sum(total_top_secondary_buy_transaction_count, 126), 252), industry)`
- IS：S 2.99 / F 2.97 / 2Y 3.97 / TO 0.1247 / DD 3.76% / margin 19.8bp
- prod **0.6377** ✓（本波余量最大）/ self 0.1108 ✓；篮子最大 0.4977（`LL53QVvn`）✓
- Recent-3yr：1.37 / 3.94 / 4.07，均值 3.13；CV **0.398**（总体）/ **0.487**（样本）；衰减比 1.36；max/min **2.97**（贴 3 线）；平年 0
- SubU 1.38 vs limit 1.295（余量 +0.085，ratio 0.462）
- 回撤日历：平均季回撤 0.786%，最大 1.882%（2021Q1），超 2× 平均的季度 **4 个**（2014Q1 / 2018Q4 / 2021Q1 / 2021Q2）
- **判定：PASS（次优）**——时间稳定性弱于赢家，仅作为同族备选，不下第二颗（同核相关 0.98）

## 同波排除项

- `e76WWGQz`（industry + STATISTICAL）：S 3.10 / 2Y 4.35 最高，但 SubU 1.12 vs limit 1.34（ratio 0.361）⇒ **RA 硬 FAIL**。与 `tm_w2b` 同型：风险模型中性化把权重挤进主宇宙。
- `d5KPPrxx`（industry + SLOW_AND_FAST）：S 3.13 / F 2.46 / prod 0.6737 / SubU ratio 0.434；与赢家相关 **0.9837**、指标全面落后 ⇒ 弃。
- `88v2XRm7`（w8, subindustry + RAM）：prod 0.6993 贴线，降为同族备胎，不作为交付候选。

## 容量侧复核（invest_S，2026-10-24 补，推翻「可提交」结论）

`is.investabilityConstrained` 现已可从 `GET /alphas/{id}` 读到（`batch_get_alpha_metrics` 同时给出
`investability_ratio = inv_S / S`）。六颗同族候选实测：

| alpha | S | inv_S | ratio |
|---|---|---|---|
| `0mjaa2Ev`（本波赢家） | 3.24 | **0.29** | **0.0895** |
| `LL522ZRe`（备选） | 2.99 | 0.28 | 0.0936 |
| `d5KzLo7v` | 2.93 | 0.29 | 0.099 |
| `LL53QVvn` | 1.61 | 0.22 | 0.137 |
| `O0Jgd7Y7` | 2.27 | **−0.06** | −0.026 |
| `88vXxaqv` | 1.99 | **−0.29** | −0.146 |

对照：`insd_inv_w1`（2026-10-24）实测 USA 17 颗 ACTIVE 的 ratio 基准 **0.83–1.05**；本族全部落在
**−0.146…+0.137**。两个容量杠杆（TOP1000 宇宙迁移、maxTrade=ON）都救不回来：
`d5KzLo7v@TOP1000` S 2.93→1.19（ratio 0.099→0.513，强度崩塌）、`d5KzLo7v@TOP2000+maxTradeON`
S 2.93→0.32（三项 RA FAIL）。机制归因：内幕交易**笔数 / 金额聚合**的 z 分数极值集中在不可投资小盘，
按 ADV 约束后剩下的名字没有 alpha ⇒ 是信号本体，不是设置问题。

平台口径：`LOW_INVESTABILITY_CONSTRAINED_SHARPE` 在 `RA_CHECK_NAMES` / `PPA_CHECK_NAMES` 内，
线 ≈ **0.70 × S**（`src/wqb/gate_attribution.py::INVEST_RATIO`，KOR 实测 0.70–0.72）；
但提交层 `/check` 是否在 USA 下发该检查**未实测**（IND 实测未下发，见 `batch_get_alpha_metrics` docstring）。
**无论平台是否拦，ratio ≈ 0.09 的候选都不应占用提交名额。**

## 结论（2026-10-24 修订）

- **Robustness 判定不变：`0mjaa2Ev` PASS**，但该 PASS 的适用域仅为「IS 不过拟合 / 时间稳定 / 回撤与 margin」，
  **不覆盖容量**。
- **提交结论作废：本族六颗全部不提交**（含 `0mjaa2Ev` / `LL522ZRe` / 原四颗），依据 `insd_inv_w1` 的
  容量判死结论与上表实测。此前「作为第 5 颗交付候选」的表述撤回。
- 后续任何近闸候选进提交池前，须先跑一次 invest_S 预筛（`batch_get_alpha_metrics`），
  ratio 明显低于 USA ACTIVE 基准（0.83–1.05）的先做机制归因，再谈 robustness。
