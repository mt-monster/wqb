# 提交执行包 · GBR 新战役 8 条（2026-10-31，prod 全量刷新后终局）

> **适用范围**：本战役（`tg_e0slvzlz2lmvv5lwqs`）GBR 未点亮塔深挖产出的可提候选。
> **与旧包的关系**：旧包 `gbr_submit_execution_pack_20261031.md` 覆盖的是**上一轮** 21 条（GBR 15 + EUR 2 + IND 1 + USA 3），两包并行、互不覆盖。
> **提交状态**：**全部暂缓**，等用户明确授权。本文件只是把提交所需的全部要素备齐，不含任何提交动作。
> **★ 终局变更（10-31 全量 refresh）**：15 条全部 `check_correlation(refresh=True)` 重测后 **7 条漂死**（5 条漂到 0.95–1.00 生产池克隆级）⇒ **可提总数由 15 修正为 8**。变更链见 §0.1，死名单见 §4.1。

---

## 0. 一页摘要

| 项 | 值 |
|---|---|
| 可提总数 | **8 条**（10-31 全量 refresh 后存活，prod+self 当日双测全过；7 条漂死见 §4.1） |
| 目标 | 60 条 ⇒ **缺口 52 条（结构性达不到，见 §8）** |
| 全闸状态 | 8 条 `ra.failed_ra_count = 0` **且** `ra.failed_ppa_count = 0`（逐条平台实读，非本地缓存） |
| PR 红线 | 8 条 prod **0.5989 – 0.6932** 全 < 0.7（10-31 当场 `refresh=True` 实测）；7 条漂死：`d51O1kOX` **1.0** / `wp9m9MW1` **0.999** / `RR62bMje` **0.998** / `6XKwmQgE` **0.9633** / `MPYlNP8z` **0.9573** / `pwdQb78v` 0.7205 / `E56onL5r` 0.7033 |
| self 红线 | 8 条 self **0.4046 – 0.6364** 全 < 0.7（10-31 实测，池 19 条、排 4 条 PPAC） |
| 篮内互相关 | 新包 8 条内部 28 对全 < 0.7（最高 `O0AKLMKq`↔`vR1aEpa3` 0.6566）；**唯一超线对在跨包**：`O0AKLMKq`↔`leAJn9e2` **0.8493** ⇒ 二选一，两种取法都是 8 条（§7.1） |
| 新点亮塔 | **2 座**：`GBR/D1/PV`（1→**6**）、`GBR/D1/FUNDAMENTAL`（1→**6**） |
| 点不亮的塔 | `NEWS`（1→2，差 1，**最便宜的下一座**）、`ANALYST`（3→3，3 条 ANALYST 件全部漂死）、`SHORTINTEREST`（0→0，E3 族封盘）、`OTHER`（1→1） |
| 二选一 | `O0AKLMKq`（S2.28/prod 0.5989）vs `leAJn9e2`（S1.93/prod 0.5507）——互相关 0.8493 互斥，取谁都是 8 条（§7.1） |
| 提交前必做 | **提交当日逐条 `check_correlation(refresh=True)` 终验**——本轮实证 5 天内 prod 可从 0.55 漂到 1.00，本表数值同样只能撑到提交那一刻 |

### 0.1 变更记录（2026-10-31 补测，覆盖本文早前版本的数字）

| 时点 | 变更 | 依据 |
|---|---|---|
| 初版 | 可提 16 条 | 15 条冻结篮 + `leA23Jae`（当时 prod/self **均未测**） |
| 补测① | `leA23Jae` **self = 0.1034 通过**（池 19 条，排除 4 条 PPAC） | `check_self_correlation`，本地零配额 |
| 补测② | 篮内 17×17 互相关：**仅 1 对超线**，16 条即 `max_mutually_below_subset` 且 `max_subset_exact=true` | `compute_mutual_correlation`，本地零配额 |
| **补测③（决定性）** | **`leA23Jae` prod = 0.7445 ❌ 撞墙** ⇒ **可提降为 15 条**；`QPvj9m0K` 替补待测 | `check_correlation(production)` 实测 49s / 38 次轮询 |
| **补测④（封盘）** | **`QPvj9m0K` prod = 0.7044 ❌ 也撞墙** ⇒ 该族 **0 颗**，总数**落定 15**；两条 `n([0.7,0.8)) = 1` ⇒ 按 skill 判据「单钉子卡死」，**不做窗口救援** | `check_correlation(production)` 4.1s（平台已预热）+ `wq-window-valley-break-prod-wall` 前置判据 |
| **补测⑤（全量刷新，终局）** | **15 条全量 `refresh=True` 重测：7 条漂死（5 条漂至 0.95–1.00 生产池克隆级）、8 条存活 ⇒ 总数落定 8** | `check_correlation(production, refresh=True)` ×15，逐条落库 |
| **补测⑥** | self 补齐：8 条活口 + `leAJn9e2` 全测通过（0.3650–0.6364）；篮内互相关复核（9 活口）唯一超线对 `O0AKLMKq`↔`leAJn9e2` 0.8493 ⇒ 二选一，`max_mutually_below_subset=8` 且 exact | `check_self_correlation` ×9 / `compute_mutual_correlation` |

**教训（写进流程）**：只要篮里有**任意一条 prod 未测**，就不得对外宣称「N 条可提」。本次正是把「16 条」写在摘要里，直到补测才发现少 1 条。**prod 未测 = 未定，不是「大概能过」**。

**第二条教训**：同族两条**同时**撞墙时不要按「换一条替补」处理 —— 先查两条的 `n([0.7,0.8))`。都为 1 说明是**同一条生产 alpha 在挡**，换窗口/换参数只是在自锁空间里打转（skill 实证 16/16 零例外，n≥1 族的谷底永远卡在 0.7019–0.7031，本次 0.7044 与之吻合）。

**第三条教训（本轮最贵）**：**prod 历史读数只能排序，永远不能放行。** 15 条 10-26~10-30 测得 0.55–0.69 全绿，**5 天内全量重测 7 条漂死**——`d51O1kOX` 0.6793→**1.0**、`wp9m9MW1` 0.5480→**0.999**，5 条漂到生产池克隆级。若不刷新直接授权提交，会连爆 7 条。⇒ **对外报「N 条可提」的当天就应全量 `refresh=True`**；「15 条可提」这个口径只存活了几个小时。


---

## 1. 全量清单（16 条筛过闸 → 刷新后 **8 条可提**，按 S 降序）

> **★ 10-31 全量 refresh 终局**：下表 prod 列是 10-26~10-30 的**旧读数，只可作历史留痕**。刷新后**仅 8 条存活**（`vR1aEpa3` / `O0AKLMKq` / `rKRkL9QE` / `0mYoANkv` / `MPYq0819` / `P0gvv5gE` / `WjOkLGWx` / `9qWwZ3go`）；**7 条漂死名单见 §4.1**；`leA23Jae` 因 prod 0.7445 出局（§5.1）。**可提者 = 8 条，下表 prod 数值不得引用放行。**

塔位均为**平台实读**（`get_alpha_details` → `pyramids`），不是按字段名推断。

| # | alpha | 机制族 | S | F | TO | 2Y | SUB | dd | 塔位（×multiplier） | prod | self | 相关性测于 |
|---:|---|---|---:|---:|---:|---:|---:|---:|---|---:|---:|---|
| 1 | `vR1aEpa3` | 营收收益率 + 量能门控 | **2.32** | **2.11** | 12.33% | 2.29 | 1.38 | 5.08% | PV×1.4 + FUND×1.6 | 0.6632 | — | 10-30 05:49 |
| 2 | `O0AKLMKq` | 营收收益率 + 波动门控 | 2.28 | 2.00 | 8.83% | 2.21 | 1.46 | 4.34% | PV×1.4 + FUND×1.6 | **0.5989** | — | 10-30 05:50 |
| 3 | `rKRkL9QE` | capxy 收益率 | 2.21 | 2.05 | 8.33% | 2.51 | **1.77** | 5.44% | PV×1.4 + FUND×1.6 | 0.6783 | — | 10-30 02:26 |
| 4 | `wp9m9MW1` | 情绪 + 短期反转 | 2.14 | 1.10 | 19.10% | 2.05 | 1.49 | **1.92%** | PV×1.4 + ANALYST×1.6 | **0.5480** | — | **10-14 19:41** |
| 5 | `MPYlNP8z` | EBIT 收益率 | 2.00 | 1.64 | 14.75% | 1.92 | 1.35 | 5.79% | FUND×1.6 | 0.6191 | — | 10-30 14:42 |
| 6 | `pwdQb78v` | 净利收益率 | 1.99 | 1.57 | 13.90% | 2.10 | 1.50 | 4.77% | FUND×1.6 | 0.6460 | — | 10-30 05:34 |
| 7 | `d51O1kOX` | 分析师修订广度 | 1.97 | 1.29 | 8.14% | 1.71 | 1.06 | 3.77% | ANALYST×1.6 | 0.6793 | **0.1129** | **10-08 11:58** |
| 8 | `E56onL5r` | 营收收益率 + 双中性 | 1.91 | 1.45 | 17.39% | 2.02 | 1.61 | 7.41% | PV×1.4 + FUND×1.6 | 0.6708 | — | 10-30 05:36 |
| 9 | `0mYoANkv` | cap/RE 收益率（反向） | 1.89 | 1.54 | 11.66% | 2.08 | 1.12 | 4.74% | PV×1.4 + FUND×1.6 | **0.6932** | — | 10-29 22:12 |
| 10 | `MPYq0819` | 新闻事件相关性 | 1.88 | 1.15 | **7.94%** | 2.32 | 1.57 | 3.13% | NEWS×1.6 | 0.6507 | — | 10-30 19:38 |
| 11 | `leA23Jae` | 借券 days-to-cover | 1.72 | 1.08 | 9.95% | **2.60** | **1.79** | 6.86% | **SHORTINT×1.2 + PV×1.4** | **0.7445 ❌** | **0.1034** | 10-31（prod 实测 49s） |
| 12 | `P0gvv5gE` | EP 收益率加速度 | 1.72 | 1.03 | 12.23% | 1.84 | 1.00 | 4.60% | MODEL×1.5 | 0.6905 | 0.6364 | **10-08 11:52** |
| 13 | `WjOkLGWx` | cheq 收益率 | 1.72 | 1.26 | 9.31% | 2.09 | 0.94 | **3.38%** | PV×1.4 + FUND×1.6 | 0.6577 | — | 10-29 23:29 |
| 14 | `9qWwZ3go` | MDL28 资产漂移加速度 | 1.67 | 1.09 | 13.40% | 2.21 | 0.93 | 4.53% | MODEL×1.5 | 0.6890 | 0.5952 | **10-08 11:46** |
| 15 | `RR62bMje` | EP 收益率加速度（f12m） | 1.67 | 1.02 | 12.61% | 1.86 | 0.80 | 4.19% | MODEL×1.5 | 0.6573 | 0.6066 | **10-06 15:05** |
| 16 | `6XKwmQgE` | 预期股息率加速度 | 1.62 | 1.04 | 13.54% | 2.19 | 1.31 | 3.40% | ANALYST×1.6 | **0.5956** | **0.4148** | **10-08 11:45** |
| — | `QPvj9m0K` | 借券 days-to-cover（备选） | 1.71 | 1.06 | 9.16% | **2.73** | 1.80 | 5.64% | SHORTINT×1.2 + PV×1.4 | 未测 | 未测 | — |

### 1.0 ATOM 核查（2026-11-01，本地库逐条读表达式判定）

**可提 8 条 + 替补 `leAJn9e2` 全部为单数据集 ATOM**（表达式数据字段只出自一个 dataset；`returns` / `cap` / `volume` 为平台内建字段，不计数据集）：

| alpha | 数据集 | 数据字段 | 内建字段 |
|---|---|---|---|
| `vR1aEpa3` / `O0AKLMKq` / `rKRkL9QE` / `0mYoANkv` / `WjOkLGWx` / `leAJn9e2` | fnd6（291） | `annual_revenue_value` / `current_enterprise_value` 等 | `returns` `cap` `volume` |
| `MPYq0819` | news17 | `nws17_*` | — |
| `P0gvv5gE` | predictive_starmine（108） | `ep_yield_pct_smest_fy1_3` | — |
| `9qWwZ3go` | model28 | `mdl28_*` | — |

塔位与 ATOM 不冲突：一条单数据集 alpha 可借内建字段点亮第二座塔（如 fnd6 + `volume` ⇒ FUND×1.6 + PV×1.4）。平台 ATOM 徽章以提交后平台判定为准，本地口径=「数据字段单源」。

### 1.1 完整表达式（提交时逐字核对）

```
vR1aEpa3  trade_when(greater(rank(ts_zscore(ts_backfill(volume, 22), 66)), 0.8), rank(ts_quantile(ts_av_diff(divide(annual_revenue_value, current_enterprise_value), 252), 22, driver=gaussian)), -1)
O0AKLMKq  trade_when(greater(rank(ts_std_dev(returns, 5)), 0.8), rank(ts_quantile(ts_av_diff(divide(annual_revenue_value, current_enterprise_value), 252), 22, driver=gaussian)), -1)
rKRkL9QE  rank(ts_quantile(ts_av_diff(divide(fnd6_capxy, cap), 252), 84, driver=gaussian))
wp9m9MW1  subtract(winsorize(signed_power(ts_quantile(anl47_rawsentiment,504),0.3), std=2.0), multiply(rank(ts_sum(pv47_for_statssimple_only_spret, 22)), 0.5))
MPYlNP8z  rank(ts_quantile(ts_zscore(divide(quarterly_ebit_value, current_enterprise_value), 504), 22, driver=gaussian))
pwdQb78v  rank(ts_quantile(ts_av_diff(divide(quarterly_net_income_3, current_enterprise_value), 504), 22, driver=gaussian))
d51O1kOX  group_rank(ts_target_tvr_decay(winsorize(rank(ts_mean(group_neutralize(last_diff_value(subtract(rank(est_12m_pre_raisednum_4wks), rank(est_12m_pre_lowerednum_4wks)),250), sector), 100)), std=0.2), lambda_min=0, lambda_max=1, target_tvr=0.08), sector)
E56onL5r  vector_neut(vector_neut(rank(ts_quantile(ts_av_diff(divide(annual_revenue_value, current_enterprise_value), 252), 22, driver=gaussian)), rank(cap)), rank(ts_zscore(ts_backfill(volume, 22), 66)))
0mYoANkv  reverse(rank(ts_quantile(ts_av_diff(divide(cap, fnd6_newa2_re), 252), 84, driver=gaussian)))
MPYq0819  ts_target_tvr_decay(group_neutralize(-ts_rank(ts_mean(vec_sum(nws17_multiple_comp_event_relevance), 60), 120), densify(market)), target_tvr=0.05, lambda_max=5, lambda_min=0)
leA23Jae  -rank(ts_rank(ts_backfill(divide(vec_sum(loaned_share_count_p5_d1), ts_mean(volume, 22)), 120), 504))
QPvj9m0K  -rank(ts_rank(ts_backfill(divide(vec_sum(loaned_share_count_p5_d1), ts_mean(volume, 126)), 120), 504))
P0gvv5gE  group_rank(ts_target_tvr_decay(rank(ts_delta(ts_backfill(ep_yield_pct_smest_fy1_3,500),20)), lambda_min=0, lambda_max=1, target_tvr=0.13), industry)
WjOkLGWx  group_rank(ts_quantile(ts_av_diff(divide(fnd6_newq_cheq, cap), 252), 84, driver=gaussian), subindustry)
9qWwZ3go  group_zscore(ts_target_tvr_decay(-rank(ts_delta(ts_backfill(mdl28_sm_structural_credit_structural_asset_drift_pct,250),8)), lambda_min=0, lambda_max=1, target_tvr=0.15), industry)
RR62bMje  group_rank(ts_av_diff(ts_backfill(ep_yield_pct_smest_f12m, 126), 40), industry)
6XKwmQgE  group_zscore(ts_target_tvr_decay(rank(ts_delta(ts_backfill(expected_dividend_yield,500),11)), lambda_min=0, lambda_max=1, target_tvr=0.15), industry)
```

### 1.2 口径警示：这两条不是「混信号调参」

- `wp9m9MW1` 含 `subtract(A, multiply(rank(...), 0.5))` —— **固定权重 0.5 的减法**，是既有候选（wave `W63` 产出），非本轮新增的权重网格扫描。它通过了全部五道闸，但**在提交说明里必须显式写明 「情绪主信号 − 0.5×短期反转」的双腿结构**，不要包装成单信号。
- `O0AKLMKq` / `vR1aEpa3` 用 `trade_when(条件, 信号, -1)` —— `-1` 是「条件不满足时强制空仓」，不是信号混合，合规。

---

## 2. 塔位账：能点亮 2 座新塔，点不亮 3 座

**当前 GBR D1 塔位**（出包时实读）：`MODEL 5 / ANALYST 3 / NEWS 1 / OTHER 1 / PV 1 / FUNDAMENTAL 1`，其余 0。
**点亮口径：同一塔累计 ≥ 3 条 alpha。**

| 塔 | 现有 | 本包贡献 | 提交后 | 结论 |
|---|---:|---:|---:|---|
| **PV** | 1 | **+5** | **6** | ✅ **新点亮** |
| **FUNDAMENTAL** | 1 | **+5** | **6** | ✅ **新点亮** |
| MODEL | 5 | +2 | 7 | ✅ 保持点亮 |
| ANALYST | 3 | **0** | 3 | ➖ **3 条 ANALYST 件全部 prod 漂死**（`d51O1kOX` / `6XKwmQgE` / `wp9m9MW1`），零增量 |
| NEWS | 1 | +1 | **2** | ❌ 差 1 —— 只差 1 条，**这是本区最便宜的下一座塔** |
| OTHER | 1 | 0 | 1 | ❌ 差 2 —— 本战役未产出 OTHER 塔候选 |
| SHORTINTEREST | 0 | 0 | 0 | ❌ 差 3 —— shortinterest3 E3 族 prod 双撞墙封盘（§5.1） |
| INSIDERS / INSTITUTIONS / SENTIMENT / RISK / SOCIALMEDIA / OPTION / EARNINGS / MACRO | 0 | 0 | 0 | ❌ 本战役实测全灭（见 `unlit_tower_field_profile_20261031.md` §15） |

**⇒ 净收益：8 条换来 2 座新点亮塔（PV、FUNDAMENTAL）+ 1 座加深（MODEL）。**

**⇒ 塔组合配额**：8 条里 PV+FUND 双塔件恰 **5 条**（`vR1aEpa3` / `O0AKLMKq` / `rKRkL9QE` / `0mYoANkv` / `WjOkLGWx`），**正好打满 trio×非trio 组合 ≤5 的上限**；MODEL 单塔 2 条、NEWS 单塔 1 条不占该配额。`O0AKLMKq`↔`leAJn9e2` 二选一后仍是 5 条不超（两者同为 PV+FUND）。

**⇒ 最有价值的单点缺口是 NEWS 差 1 条**——只要再出 1 条 NEWS 塔的全闸 alpha，就能点亮第 3 座新塔。这条线索优先于继续在 fundamental 家族加条数（那里已 6 条，边际塔位收益为零）。

---

## 3. 命名与标签映射（`set_alpha_properties` 直接用）

命名规范 `<REGION>_<R|S>_<family>_<NN>`，禁空格、禁用 prod 数值命名。
标签规范：`CH_REG` + `SRC_<数据集>` 必打，可选 `EXPRFAM_<族>`，**上限 5 个**。
颜色：`BLUE`（已提交 · 待观察）。`GREEN` 须由 OS 结果挣得，不得作默认。

| alpha | name | SRC 数据集（按字段前缀推定） | EXPRFAM |
|---|---|---|---|
| `vR1aEpa3` | `GBR_R_rev_yield_volgate_01` | `SRC_fundamental6` | `EXPRFAM_rev_yield` |
| `O0AKLMKq` | `GBR_R_rev_yield_vargate_01` | `SRC_fundamental6` | `EXPRFAM_rev_yield` |
| `rKRkL9QE` | `GBR_R_capxy_yield_01` | `SRC_fundamental6` | `EXPRFAM_cashflow_yield` |
| `wp9m9MW1` | `GBR_R_sent_reversal_01` | `SRC_analyst47` | `EXPRFAM_sent_mix` |
| `MPYlNP8z` | `GBR_R_ebit_yield_01` | `SRC_fundamental` | `EXPRFAM_earnings_yield` |
| `pwdQb78v` | `GBR_R_ni_yield_01` | `SRC_fundamental` | `EXPRFAM_earnings_yield` |
| `d51O1kOX` | `GBR_R_rev_breadth_01` | `SRC_analyst7` | `EXPRFAM_est_revision` |
| `E56onL5r` | `GBR_R_rev_yield_neut_01` | `SRC_fundamental6` | `EXPRFAM_rev_yield` |
| `0mYoANkv` | `GBR_R_cap_re_yield_01` | `SRC_fundamental6` | `EXPRFAM_asset_yield` |
| `MPYq0819` | `GBR_R_news_event_01` | `SRC_news17` | `EXPRFAM_news_event` |
| `leA23Jae` | `GBR_R_dtc_rank_01` | `SRC_shortinterest3` | `EXPRFAM_days_to_cover` |
| `P0gvv5gE` | `GBR_R_epyield_accel_01` | `SRC_predictive_starmine` | `EXPRFAM_est_yield_accel` |
| `WjOkLGWx` | `GBR_R_cheq_yield_01` | `SRC_fundamental6` | `EXPRFAM_cash_yield` |
| `9qWwZ3go` | `GBR_R_mdl28_drift_01` | `SRC_model28` | `EXPRFAM_structural_accel` |
| `RR62bMje` | `GBR_R_epyield_accel_02` | `SRC_predictive_starmine` | `EXPRFAM_est_yield_accel` |
| `6XKwmQgE` | `GBR_R_divyield_accel_01` | `SRC_predictive_starmine` | `EXPRFAM_est_yield_accel` |

> **`SRC_` 标签的可靠性**：`analyst7` / `model28` / `analyst47` / `shortinterest3` / `news17` 有本地 dataset 字段佐证或字段前缀唯一；`predictive_starmine` / `fundamental` / `fundamental6` 是按字段前缀（`ep_yield_pct_smest_*` / `fnd6_*` / `quarterly_*`）推定。**提交前用平台数据集页核对一次再落标签**，标签错了不影响闸，但会污染后续的 SRC 归因。

---

## 4. 相关性：8 条当日刷新全过，7 条漂死

### 4.1 10-31 全量 `refresh=True` 终局（15 条 → 8 活 7 死）

| 结果 | alpha | 旧读数 → 刷新值 | 形态 |
|---|---|---|---|
| ❌ 漂死 | `d51O1kOX` | 0.6793 → **1.0000** | 生产池完全克隆 |
| ❌ 漂死 | `wp9m9MW1` | 0.5480 → **0.9990** | 生产池完全克隆 |
| ❌ 漂死 | `RR62bMje` | 0.6573 → **0.9980** | 生产池完全克隆 |
| ❌ 漂死 | `6XKwmQgE` | 0.5956 → **0.9633** | 生产池近克隆 |
| ❌ 漂死 | `MPYlNP8z` | 0.6191 → **0.9573** | 生产池近克隆 |
| ❌ 漂死 | `pwdQb78v` | 0.6460 → **0.7205** | 越线 |
| ❌ 漂死 | `E56onL5r` | 0.6708 → **0.7033** | 越线 |
| ✅ 存活 | `O0AKLMKq` | **0.5989**（10-31 刷后） | 全篮最低 |
| ✅ 存活 | `MPYq0819` | **0.6507** | |
| ✅ 存活 | `WjOkLGWx` | **0.6577** | |
| ✅ 存活 | `vR1aEpa3` | **0.6632** | |
| ✅ 存活 | `rKRkL9QE` | **0.6783** | |
| ✅ 存活 | `9qWwZ3go` | **0.6890** | |
| ✅ 存活 | `P0gvv5gE` | **0.6905** | |
| ✅ 存活 | `0mYoANkv` | **0.6932** | 最贴线 |

另：`leAJn9e2` prod **0.5507** ✅ / self **0.3650**（旧包唯一存活件，10-31 刷后确认）——见 §7.1 二选一。

**★ 漂移量级警示**：漂移窗口 ≤5 天，5 条从 0.55–0.68 直接漂到 0.95–1.00（生产池克隆级）。**上表 8 条的数值同样只能撑到提交当日**——提交执行时逐条 `refresh=True` 终验的规则不变，但现在有了「重测可能当场判死」的实证，撞墙不是小概率。

### 4.2 存活 8 条 self（10-31 实测，池 19 条、排 4 条 PPAC）

| alpha | self | alpha | self |
|---|---:|---|---:|
| `O0AKLMKq` | **0.4046** | `vR1aEpa3` | 0.5240 |
| `WjOkLGWx` | 0.4955 | `0mYoANkv` | 0.5210 |
| `rKRkL9QE` | 0.5456 | `9qWwZ3go` | 0.5952 |
| `MPYq0819` | 0.6005 | `P0gvv5gE` | 0.6364 |

8 条全部 < 0.7；`P0gvv5gE` 0.6364 / `MPYq0819` 0.6005 在 0.6 附近，提交后读回时重点盯。8 条 prod+self 已全部落库（`persist_correlation`，platform_sync，checked_at 2026-10-31）。

---

## 5. `leA23Jae` vs `QPvj9m0K`：取哪颗

两者同族，互相关 **0.8469** ⇒ 只能提 1 颗。

| alpha | S | F | TO | 2Y | SUB | dd | margin |
|---|---:|---:|---:|---:|---:|---:|---:|
| `leA23Jae`（ADV 22） | **1.72** | **1.08** | 9.95% | 2.60 | 1.79 | 6.86% | 9.85 bp |
| `QPvj9m0K`（ADV 126） | 1.71 | 1.06 | **9.16%** | **2.73** | **1.80** | **5.64%** | **10.51 bp** |

**原订取 `leA23Jae`** —— 理由是 S/F 略高，且 ADV 窗口 22 在 GBR 已验证为 E3 引擎的最优短窗。
**★★ 结论：两条全部撞墙 ⇒ 该族 0 颗，本包不取任何一条。** `leA23Jae` prod **0.7445**、`QPvj9m0K` prod **0.7044**，都 ≥ 0.7。原本「两者只能进 1 颗」，现在是 **0 颗**。

### 5.1 shortinterest3 E3 族 prod 撞墙实测（2026-10-31）

```
check_correlation(leA23Jae, production) → 0.7445  ❌  attempts=38  elapsed 49.3s
check_correlation(QPvj9m0K, production) → 0.7044  ❌  attempts=4   elapsed  4.1s
```

| alpha | ADV 窗 | prod | n([0.7,0.8)) | n([0.6,0.7)) | 判定 |
|---|---:|---:|---:|---:|---|
| `leA23Jae` | 22 | **0.7445** | **1** | 4 | ❌ |
| `QPvj9m0K` | 126 | **0.7044** | **1** | 14 | ❌ |

**直方图（`leA23Jae`，生产池逐桶条数）**——比单点值更有信息量：

| 桶 | 条数 |
|---|---:|
| 0.7 – 0.8 | **1** |
| 0.6 – 0.7 | **4** |
| 0.5 – 0.6 | 38 |
| 0.4 – 0.5 | 122 |
| 0.3 – 0.4 | 273 |
| 0.0 – 0.3 | 约 7.1 万 |
| < 0.0 | 约 2.9 万 |

**为什么不做窗口救援（这是结论，不是猜测）**

`wq-window-valley-break-prod-wall` 的前置判据是明确分档，实证 **16/16 零例外**：

| `n([0.7,0.8))` | 判定 |
|---|---|
| **0** | 该族存在过线窗口 ⇒ 可以扫窗口网格找谷 |
| **≥ 1** | **单钉子卡死**，无论怎么调 W 都过不了 ⇒ 弃，别扫窗口 |

本族两条都是 **n = 1** ⇒ 判「单钉子卡死」。硬旁证：该 skill 记录 n=1 族的谷底**永远卡在 0.7019–0.7031**（差 0.002–0.003），本次 `QPvj9m0K` 实测 **0.7044** 正落在同一窄带上，属同一种失败形态。

**「换窗口」这条路其实已经试过了**：ADV 22 → 126 的结果是 prod 0.7445 → 0.7044，只降 0.04，仍越线。继续沿 `ts_rank` 的 W 扫只是在同一条钉子周围打转，不值得再花回测配额。

**塔位影响**：该族原本能给 SHORTINTEREST 送 1 条（0→1，仍点不亮塔，需 3 条），现在归 0；PV 的增量也从 1→9 修正为 **1→8**。**塔位边际收益本来就是 0，所以这次损失只是条数 −1，已点亮的 2 座塔（PV / FUNDAMENTAL）不受影响。**


---

## 6. 提交顺序建议（8 条，二选一后定稿）

排序原则：① prod 余量大的先走（先占塔位、先锁 OS 计息）；② 塔位贡献大的靠前；③ 同族相邻，便于 mid-batch 发现撞车时立即改换。

| 批次 | alpha | 理由 |
|---:|---|---|
| 1 | `O0AKLMKq`* | prod 0.5989 全篮最低，PV+FUND 双塔 |
| 2 | `MPYq0819` | prod 0.6507，**唯一 NEWS 件**，塔位最贵，优先保 |
| 3 | `WjOkLGWx` | prod 0.6577，PV+FUND |
| 4 | `vR1aEpa3` | prod 0.6632，S 2.32 全篮最高 |
| 5 | `rKRkL9QE` | prod 0.6783，PV+FUND |
| 6 | `9qWwZ3go` | prod 0.6890，MODEL |
| 7 | `P0gvv5gE` | prod 0.6905，MODEL（与 6 相邻，便于观测 self 抬升） |
| 8 | `0mYoANkv` | prod 0.6932 最贴线，放最后（万一撞墙，前面已落袋） |

\* 若 §7.1 二选一取 `leAJn9e2`，则第 1 位换它（prod 0.5507 / self 0.3650，余量最足），`O0AKLMKq` 出局，其余顺延不变。

**mid-batch 中止条件**：任一条终验 prod ≥ 0.7 ⇒ 立即跳过该条，**不要因为「只差一点」去试 refresh 第二次**（平台单并发槽，重试只会把自己顶成 busy）。连续 2 条撞墙 ⇒ 暂停整批，先查是否 prod 池整体漂移（本轮 7/15 的漂死率说明这不是小概率事件）。

---

## 7. 提交前三道终验（逐条，缺一不可）

```
① check_correlation(alpha_id, correlation_type="production", refresh=True)   # prod < 0.7 严格
② check_self_correlation(alpha_id, correlation_type="self", threshold=0.7)   # 本地免费，< 0.7
③ batch_get_alpha_metrics([alpha_id]) 复核 failed_ra_count == 0 && failed_ppa_count == 0
```

**顺序不可换**：② 免费先跑也合理，但 ① 决定要不要花塔位配额，所以 ① 优先。
**判据口径**：`checks.fail = []` **不等于**过闸（§1 已示警）——必须读 `failed_ra_count`。

**自相关注意**：`9qWwZ3go` self 0.5952 / `P0gvv5gE` 0.6364 / `MPYq0819` 0.6005 —— 都在 0.6 附近。**若已提交池里已有同族先提交的，后提交的 self 会抬升**，因此 §6 把 MODEL 两条放 6–7 相邻、贴线件放最后。

### 7.1 篮内互相关（2026-10-31 实测，本地零配额）

`compute_mutual_correlation(17 ids → 刷新后 9 活口重核, threshold=0.7, years=4)`，1021 个交易日。**这补的是 §7 三道终验之外的流程缺口**：平台 self-corr 比对的是「已提交 OS 池」，而候选们要**逐条提交**，后提交的会被拿去和**前面刚提交的**比 —— 篮内互相关就是自己给自己造 self-corr 墙。

**结论三条（10-31 全量刷新后重核）**：

1. **新包 8 条内部 28 对全部 < 0.7** —— 最高 `O0AKLMKq` ↔ `vR1aEpa3` = 0.6566（余量 0.0434）。旧贴线对 `vR1aEpa3` ↔ `E56onL5r`（0.6954）与 `MPYlNP8z` ↔ `pwdQb78v`（0.6868）**因对方漂死自动消解**——本轮唯一好消息。
2. **唯一超线对在跨包**：`O0AKLMKq` ↔ `leAJn9e2`（旧包唯一存活件）= **0.8493** ⇒ 两者只能取一。
3. **二选一都是 8 条**：新包 8 条 ↔ 新包 7 条 + `leAJn9e2`，两种取法 `max_mutually_below_subset` 都是 8 且 `max_subset_exact = true` ⇒ **数学上不存在第 9 条**，「是不是漏提了一条」在此封死。

| 取法 | 组成 | 权衡 |
|---|---|---|
| **A：取 `O0AKLMKq`** | 新包 8 条 | 指标更高（S 2.28 / F 2.00 / 2Y 2.21）；prod 0.5989 / self 0.4046 也过线，但余量不如 B |
| **B：取 `leAJn9e2`** | 新包 7 条 + 旧包 1 条 | 相关性最安全（prod 0.5507 / self 0.3650 全篮最低）；S 1.93 / F 1.60 略低 |

两者塔位完全相同（都是 PV+FUND），不影响 §2 塔位账与配额。

**新增中止条件（与 §6 并列）**：任一条提交后平台自相关 ≥0.7 ⇒ 立即查它在 §7.1 表里的配对伙伴，若伙伴已提交，则该族后续变体一律不进本批；不要靠反复 refresh 硬试。

---

## 8. 为什么凑不到 60 条（不在本包展开论证）

GBR 未点亮塔的可挖面被覆盖率与信号强度双重锁死，实测穷尽：9 塔 / 17 个候选数据集全部跑过，只有 `shortinterest3` 产出全闸 alpha（且族收敛到 1 颗）。
详见 `docs/reference/GBR/unlit_tower_field_profile_20261031.md` §15（穷尽盘点）与 §17（修 2Y 设置轴封盘）。
**唯一还能补量的方向是已点亮塔的深挖（MODEL / ANALYST / NEWS / OTHER / PV / FUNDAMENTAL），但那超出「未点亮塔」的原始目标范围，需用户单独授权。**

---

## 9. descriptions 三段式（英文，≤100 词，提交时逐条填）

格式固定三段，段间用真实换行：

```
Idea: <一句经济学假设>

Rationale for data used: <为什么这个字段能代理该假设>

Rationale for operators used: <算子几何为什么匹配>
```

| alpha | descriptions |
|---|---|
| `vR1aEpa3` | `Idea: Firms whose revenue yield versus enterprise value is improving outperform, but only when trading activity confirms the move is real.` `Rationale for data used: annual_revenue_value normalised by current_enterprise_value gives a scale-free operating yield; volume z-score filters out stale pricing.` `Rationale for operators used: ts_av_diff over 252 days measures the level shift, ts_quantile with gaussian driver compresses tails, trade_when gates on liquidity so signals fire only in liquid regimes.` |
| `O0AKLMKq` | `Idea: Revenue yield acceleration predicts returns conditional on realised volatility being elevated, when mispricing corrects fastest.` `Rationale for data used: annual_revenue_value over current_enterprise_value is an operating yield immune to capital-structure changes; 5-day return volatility proxies the correction regime.` `Rationale for operators used: trade_when activates only above the 80th volatility percentile, ts_av_diff captures the 252-day level shift, ts_quantile-gaussian bounds extreme values without clipping the tails.` |
| `rKRkL9QE` | `Idea: Capital expenditure scaled by market cap produces a real-options yield whose improvement signals under-priced growth.` `Rationale for data used: fnd6_capxy is reported capex, cap is a clean market denominator, so their ratio is a scale-free investment intensity.` `Rationale for operators used: ts_av_diff(252) extracts the trend rather than the level, ts_quantile with 84 buckets and gaussian driver produces a smooth bounded rank robust to outliers.` |
| `wp9m9MW1` | `Idea: Analyst sentiment on a stock is partly offset by short-term reversal; subtracting a reversal leg isolates the durable sentiment component.` `Rationale for data used: anl47_rawsentiment is an aggregated analyst tone score; pv47_for_statssimple_only_spret supplies the 22-day price reversal that contaminates naive sentiment signals.` `Rationale for operators used: ts_quantile(504) ranks tone over two years, signed_power(0.3) damps extremes while keeping sign, winsorize(2σ) bounds the mix, and a fixed 0.5 weight on the reversal leg neutralises it.` |
| `MPYlNP8z` | `Idea: Operating profit relative to enterprise value is a cleaner earnings yield than net income because it ignores financing decisions.` `Rationale for data used: quarterly_ebit_value captures operating profitability; current_enterprise_value aligns numerator and denominator on a pre-financing basis.` `Rationale for operators used: ts_zscore over 504 days normalises the yield against its own history, ts_quantile with gaussian driver bounds the cross-section, and the outer rank makes the signal scale-free.` |
| `pwdQb78v` | `Idea: Net income acceleration relative to enterprise value signals improving capital efficiency that the market under-reacts to.` `Rationale for data used: quarterly_net_income_3 is the bottom-line earnings series; current_enterprise_value keeps the ratio comparable across leverage profiles.` `Rationale for operators used: ts_av_diff(504) measures the long-horizon level shift, ts_quantile-gaussian bounds outliers, outer rank produces a bounded cross-sectional score.` |
| `d51O1kOX` | `Idea: The breadth of upward versus downward analyst estimate revisions predicts returns better than revision magnitude, because breadth reflects consensus dispersion.` `Rationale for data used: est_12m_pre_raisednum_4wks and est_12m_pre_lowerednum_4wks count how many analysts moved, giving a pure breadth measure free of estimate scale.` `Rationale for operators used: rank difference isolates net breadth, last_diff_value(250) tracks the change in breadth, group_neutralize removes sector bias, ts_target_tvr_decay caps turnover at 8%, winsorize bounds outliers.` |
| `E56onL5r` | `Idea: Revenue yield acceleration survives only after removing size and volume exposure, so a doubly neutralised version isolates the pure fundamental signal.` `Rationale for data used: annual_revenue_value over current_enterprise_value is an operating yield; cap and volume are the two contaminating exposures.` `Rationale for operators used: nested vector_neut orthogonalises the signal against size then against volume z-score, ts_av_diff(252) takes the level shift, ts_quantile-gaussian bounds the tails.` |
| `0mYoANkv` | `Idea: Firms trading cheap relative to their retained earnings book accumulate value; the reverse rank captures the cheapness.` `Rationale for data used: fnd6_newa2_re is the retained earnings balance, cap is market value, so cap/RE measures how much the market pays per unit of accumulated earnings.` `Rationale for operators used: ts_av_diff(252) tracks the trend of that ratio rather than its static level, reverse flips to a cheapness score, ts_quantile(84, gaussian) bounds the distribution.` |
| `MPYq0819` | `Idea: Sustained news coverage relevance of a firm predicts returns because media attention proxies information diffusion, and its fade is informative.` `Rationale for data used: nws17_multiple_comp_event_relevance scores how relevant multi-company events are to each firm, a continuous attention proxy rather than a raw count.` `Rationale for operators used: ts_mean(60) smooths daily noise, ts_rank(120) converts to a bounded percentile, group_neutralize by market removes index effects, ts_target_tvr_decay pins turnover near 5%.` |
| `leA23Jae` | `Idea: Days-to-cover, the loaned share balance normalised by average daily volume, measures how crowded a short position is and how violent an unwind would be.` `Rationale for data used: loaned_share_count_p5_d1 is the actual securities-lending balance aggregated across venues; ts_mean(volume, 22) converts it into days needed to cover, the standard short-interest metric.` `Rationale for operators used: ts_rank(504) ranks the ratio over two years for stability, ts_backfill(120) fills sparse vector data, minus rank makes high crowding a short signal.` |
| `P0gvv5gE` | `Idea: Acceleration in forward earnings yield, not its level, predicts returns because the market prices the rate of change of expectations.` `Rationale for data used: ep_yield_pct_smest_fy1_3 is the consensus FY1 earnings yield in percent, a forward-looking fundamental that updates on estimate revisions.` `Rationale for operators used: ts_delta after backfilling to 500 days isolates the change, rank normalises cross-sectionally, group_rank by industry removes sector bias, ts_target_tvr_decay keeps turnover near 13%.` |
| `WjOkLGWx` | `Idea: Cash plus short-term investments relative to market cap is a liquidity buffer yield; its improvement signals improving financial slack.` `Rationale for data used: fnd6_newq_cheq is the cash-and-equivalents balance from the quarterly file; cap gives a market-based denominator.` `Rationale for operators used: ts_av_diff(252) extracts the trend, ts_quantile(84, gaussian) bounds it, group_rank by subindustry neutralises the tightest peer group.` |
| `9qWwZ3go` | `Idea: A model-derived structural asset drift score, when decelerating, signals deteriorating balance-sheet quality ahead of reported fundamentals.` `Rationale for data used: mdl28_sm_structural_credit_structural_asset_drift_pct is a modelled structural credit metric unavailable from raw filings, giving forward-looking information.` `Rationale for operators used: minus rank inverts so deterioration is short, ts_delta(8) after backfilling to 250 days captures acceleration, group_zscore by industry removes sector scale, ts_target_tvr_decay caps turnover.` |
| `RR62bMje` | `Idea: Acceleration in the 12-month forward earnings yield predicts returns because expectation revisions propagate faster than reported earnings.` `Rationale for data used: ep_yield_pct_smest_f12m is the consensus 12-month-forward earnings yield, the most revision-sensitive fundamental series.` `Rationale for operators used: ts_backfill(126) handles sparse coverage, ts_av_diff(40) measures deviation from the 40-day mean as a short-horizon acceleration, group_rank by industry neutralises sectors.` |
| `6XKwmQgE` | `Idea: Acceleration in expected dividend yield signals management's forward confidence about sustainable cash generation.` `Rationale for data used: expected_dividend_yield is a consensus forward estimate, so its change reflects revised payout expectations rather than realised distributions.` `Rationale for operators used: ts_delta after backfilling to 500 days isolates the change, group_zscore by industry normalises scale, ts_target_tvr_decay holds turnover near 13.5% for tradability.` |

---

## 10. 失效风险预估

| 风险 | 影响面 | 判据 / 观察点 |
|---|---|---|
| **★★ prod 5 天漂移 0.55→1.00（本批头号风险）** | 全部 8 条 | 15 条刷新 7 条漂死（47%）；**提交当日必须逐条 `refresh=True` 终验**，任何旧读数不得放行；连续撞墙即停批 |
| **PV + FUNDAMENTAL 集中** | 5/8 条同时挂这两塔（打满 trio×非trio ≤5 配额） | 提交后按月看这 5 条的 OS 相关性；若互相 > 0.5，说明只是同一因子的几何变体 |
| **营收收益率族同源** | `vR1aEpa3` / `O0AKLMKq` 共用 `annual_revenue_value ÷ current_enterprise_value` 主腿（互相关 0.6566） | 且 `O0AKLMKq` 与 `leAJn9e2` 0.8493 互斥（§7.1）；OS 可能收敛 |
| **`0mYoANkv` prod 0.6932 贴线** | 单条 | 终验 refresh 很可能越过 0.7；视为「高概率撞墙」，放最后提交 |
| **MODEL 塔两条 self 0.59–0.64** | `9qWwZ3go` / `P0gvv5gE` | 同族加速度骨架，先提交的会抬升后提交的 self；§6 相邻放尾部观测 |
| **`MPYq0819` CLUSTER_TEST 0.98 / limit 1** | 单条 | 贴线未卡（`failed_ra_count=0`），但 OS 阶段聚类测试收紧会翻 |
| **2Y 闸整体偏紧** | 全批 | 本批 2Y 1.84–2.51 都远超 1.58；说明这批不是「靠最近两年行情」撑起来的，稳健性尚可 |
| **~~shortinterest3 E3 族~~ 已封盘** | — | prod 0.7445 / 0.7044 双 ❌ + `n([0.7,0.8))=1` 判死（§5.1），既成事实不是风险 |
| **~~`wp9m9MW1` maxTrade=ON~~** | — | 该条已随 prod 漂死出局，风险作废 |

---

## 11. 待办（本包未完成项）

1. **二选一未定**：`O0AKLMKq` vs `leAJn9e2`（互相关 0.8493 互斥，两种取法都 8 条）——待用户定（§7.1）。
2. **提交授权**：8 条备齐（prod+self 当日双测、篮内互相关过、近十年逐年前置已核），等用户一句整体授权；授权后执行 = 逐条 `refresh=True` 终验 → 按 §6 顺序 POST submit → 贴线件相邻提交并读回平台自相关。
3. **`SRC_` 标签需平台核对** —— `predictive_starmine` / `fundamental` / `fundamental6` 三个是前缀推定（现存活 8 条里涉及 `fundamental` / `fundamental6` / `predictive_starmine`）。
4. **8 条均未做 OS 期归因** —— 提交后按月补。
5. ~~`wp9m9MW1` maxTrade=ON 是否改 OFF 重跑~~ —— 该条 prod 漂死出局，作废。
6. **NEWS 差 1 条点亮第 3 塔** —— 超「未点亮塔」原始范围，需单独授权后决定是否挖。

---

*本包于 2026-10-31 编制，同日经两次修正终局为 **8 条**：① `leA23Jae`/`QPvj9m0K` prod 双撞墙（16→15）；② 15 条全量 `refresh=True` 重测 7 条漂死（15→8）。8 条的 prod/self 均为 10-31 当场实测（prod 走平台 refresh、self 本地零配额）并落库（platform_sync），7 条死值同步落库留痕。**提交当日仍须逐条 refresh 终验**——本批实证 prod 5 天内可漂 0.4 以上。塔位与闸状态来自 `get_alpha_details` 平台实读，指标来自 `backtest_results` 与 `alphas` 双表交叉核对。*
