# IND × `institutions6` — 10 颗 REGULAR Alpha 交付报告

> 区域：**IND**（全程固定，未换区）｜数据集：**`institutions6`**（IND `institutions` 类别唯一数据集）
> 日期：2026-10-23｜口径：`REGULAR / IND / TOP500 / D1 / STATISTICAL / decay 126 / truncation 0.08 / nanHandling OFF / maxTrade OFF / unitHandling VERIFY / pasteurization ON / P0Y0M0D / FULL`
> 结论：**10 颗全部 IS 阶段 RA 0 失败、平台硬线全过、prod 相关 0.59–0.67（<0.70）、self 相关 0.27–0.34（<0.70）**；**未提交**（无不可逆动作）。
> ⚠ 必读边界：10 颗属**同一信号簇**（互相关 avg 0.723 / max 0.953），**不构成 self-correlation 合规篮子**。本文交付的是“10 颗独立通过验证的候选”，不是“10 颗可同时提交”。
> 两项补充复核：**invest_S** — 平台提交层 `/check` 未下发 `LOW_INVESTABILITY_CONSTRAINED_SHARPE`（10/10 无该检查）；按 0.70×S 风险口径 3/10 通过（2 颗临界、5 颗明显低于，见 §2.5）。**ATOM** — 10 颗为 `returns + institutions6` 双数据集（`atom_flag=combined`），不是 ATOM；纯 IND institutions6 的 46 条 ATOM-only 回测记录（40 个唯一表达式）最高 S=1.10，未产出合格 ATOM（见 §2.6）。

---

## 1. 交付清单（按 Sharpe 降序）

| # | alpha | 核心字段 | 机制 | S | F | TO | 2Y | sub | robust | prod | self |
|---:|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | `E5VNe67L` | disposed / (acq+dis) | 卖出占比 + lag21 残差 | **3.20** | 2.52 | 0.2497 | 3.00 | 1.64 | 1.80 | 0.6459 | 0.3437 |
| 2 | `JjP0Ja5l` | `quantity_institutional_shares_acquired` | 买入股数水平残差 | 3.12 | 2.42 | 0.2461 | 2.82 | 1.92 | 1.97 | 0.6651 | 0.3043 |
| 3 | `9qEPO5K2` | `count_institutional_sellers_security` | 卖出家数水平残差 | 3.10 | 2.38 | 0.2413 | 2.87 | 1.58 | 1.68 | 0.6280 | 0.3182 |
| 4 | `KPmvEYeE` | `quantity_institutional_shares_disposed` | 卖出股数 + industry 中性 | 3.07 | 2.36 | 0.2387 | 3.14 | 1.65 | 1.49 | 0.6162 | 0.3094 |
| 5 | `qMEkJ2zj` | `market_value_institutional_shares_acquired` | 买入金额水平残差 | 2.92 | 2.18 | 0.2460 | 2.66 | 1.77 | 1.74 | 0.6631 | 0.3005 |
| 6 | `9qE8r85r` | `aggregate_equity_value_institutions` / `..._all_owners` | 机构市值占比残差 | 2.90 | 2.15 | 0.2471 | 3.18 | 1.60 | 1.54 | 0.6546 | 0.3022 |
| 7 | `0mjk2ZQv` | `count_institutional_holders_security` | 持有家数水平残差 | 2.87 | 2.14 | 0.2403 | 2.08 | 1.36 | 1.55 | 0.5925 | 0.2663 |
| 8 | `j2eo0oMO` | `aggregate_share_count_institutions` / `..._all_owners` | 机构股数占比残差 | 2.86 | 2.13 | 0.2432 | 2.94 | 1.48 | 1.55 | 0.6333 | 0.2925 |
| 9 | `O0JwXdk7` | `count_institutional_buyers_security` | 买入家数水平残差 | 2.82 | 2.06 | 0.2475 | 2.40 | 1.32 | 1.63 | 0.6659 | 0.3116 |
| 10 | `QPYrpRlp` | `market_value_institutional_shares_disposed` | 卖出金额水平残差 | 2.81 | 2.06 | 0.2433 | 2.98 | 1.34 | 1.38 | 0.6635 | 0.3332 |

**字段覆盖 11/11**（含两条“全体股东”分母字段）。每条都是 `REGULAR`、`UNSUBMITTED`、`stage=IS`。
`prod` / `self` 为 2026-10-23 平台实测（`check_correlation(refresh=True)`），已落库 `alphas.prod_correlation` / `self_correlation`。

---

## 2. 验证口径与证据

### 2.1 平台 IS 阶段 RA（10/10 全过）

`get_alpha_details` 逐颗返回 `ra.failed_ra_count = 0`、`checks.fail = []`；通过的硬闸：

`LOW_SHARPE`、`LOW_FITNESS`、`LOW_SUB_UNIVERSE_SHARPE`、`IS_LADDER_SHARPE`、`LOW_ROBUST_UNIVERSE_SHARPE`、`CONCENTRATED_WEIGHT`、`CLUSTER_TEST`、`MATCHES_PYRAMID`、`LOW_TURNOVER` / `HIGH_TURNOVER`。

平台官方线（`src/wqb/config.py::PLATFORM_CHECK_LINES`，Delay-1）：LOW_SHARPE ≥ 1.25、LOW_FITNESS ≥ 1.0、2Y / IS_LADDER ≥ 1.58、turnover ∈ (0.01, 0.70)。本批最低 S 2.81、最低 2Y 2.08、最低 F 2.06，余量充足。

### 2.2 提交层 `/check` 复核（只读，不是提交）

`get_alpha_details` 的 IS checks 对 SELF/PROD/DATA_DIVERSITY/REGULAR_SUBMISSION/POWER_POOL 仍显示 pending；为拿到提交层视图，2026-10-23 对 10 颗逐一调用 **只读** `GET /alphas/{id}/check`（不触发 `POST /submit`），返回：

- `SELF_CORRELATION` 0.2608–0.3417 PASS、`PROD_CORRELATION` 0.5925–0.6659 PASS（limit 0.70）；
- `DATA_DIVERSITY` PASS、`REGULAR_SUBMISSION` PASS（0/4）、`POWER_POOL_CORRELATION` PASS（0.1554–0.2218，limit 0.5）；
- RA 硬闸（`LOW_SHARPE` / `LOW_FITNESS` / `LOW_SUB_UNIVERSE_SHARPE` / `IS_LADDER_SHARPE` / `LOW_ROBUST_UNIVERSE_SHARPE` / `CONCENTRATED_WEIGHT` / `CLUSTER_TEST` / `MATCHES_PYRAMID` / 换手）10/10 PASS；无 FAIL，仅 4 类 WARNING。
- WARNING：`MATCHES_THEMES`、`OSMOSIS_ALLOCATION`、`POWER_POOL_DESCRIPTION_LENGTH`、`POWER_POOL_DESCRIPTION_FORMAT`，均非 RA 硬闸。

> `/check` 的 SELF/PROD 值与 §2.3 的 `check_correlation` 快照略有差异（平台两套计算时点/池），但均 <0.70；真实提交前以 `refresh=True` 复测为准。
> 端点首次可能返回 200 + 空 body（异步计算），稍后重试即可拿到完整 JSON；证据保存在本地 `logs/_check_results.json`（未入库）。

### 2.3 相关性实测（2026-10-23）

| 指标 | 范围 | 墙 | 结论 |
|---|---|---|---|
| prod correlation | 0.5925 – 0.6659 | < 0.70 | 10/10 通过 |
| self correlation | 0.2663 – 0.3437 | < 0.70 | 10/10 通过 |

> ⚠ prod 是**对当前生产池的快照**，平台池变动会让数值漂移；真实提交前必须逐颗 `check_correlation(refresh=True)` 复测，不得直接引用本表。

### 2.4 “通过验证”的准确含义

- ✅ 已验：IS 回测的 RA 硬闸、平台指标线、prod / self 相关、字段与算子合法性；**提交层 `/check` 10/10 RA PASS，且 SELF/PROD/DATA_DIVERSITY/REGULAR_SUBMISSION/POWER_POOL 均有实际 PASS 值**（§2.2）。
- ℹ️ `submit_verdict` 预检仍返回 `UNVERIFIABLE_404`（`GET /alphas/{id}/submit` 死端点），但 `/check` 已提供提交层 checks；两者不冲突，404 不再是“视图不可用”的唯一证据。
- ℹ️ S4 预筛工具 `batch_get_alpha_metrics` 对这 10 颗返回 `REVIEW` 而非 `READY`，原因是 `get_alpha_details` 的 `prodCorrelation` 为 null（工具内部按 1.0 保守处理），**不是指标失败**；最终判定以 DB 的 prod/self 与 `/check` 为准。
- ❌ 未验：OS（样本外）表现、提交后的平台终审、真实 `POST /submit` 的返回。
- ❌ 未做：`POST /alphas/{id}/submit`（不可逆），本报告不构成提交决定。

### 2.5 invest_S（可投资性约束 Sharpe）实测

平台 `is.investabilityConstrained.sharpe`（本文简称 `invest_S`）逐颗有值；10/10 的 `/check` checks 中**均未出现** `LOW_INVESTABILITY_CONSTRAINED_SHARPE`（不是 PASS/FAIL，是平台未下发）⇒ 当前 IND 提交链不把它当硬闸。`0.70×S` 是 KOR/其他区历史实测口径（不在 `config.PLATFORM_CHECK_LINES`），这里只作风险监控。

| alpha | S | invest_S | invest_S/S | 0.70×S | 风险口径 |
|---|---:|---:|---:|---:|---|
| `JjP0Ja5l` | 3.12 | 2.33 | 0.7468 | 2.184 | ✅ |
| `0mjk2ZQv` | 2.87 | 2.25 | 0.7840 | 2.009 | ✅ |
| `qMEkJ2zj` | 2.92 | 2.11 | 0.7226 | 2.044 | ✅ |
| `O0JwXdk7` | 2.82 | 1.96 | 0.6950 | 1.974 | ⚠ 临界（低于线 0.014） |
| `E5VNe67L` | 3.20 | 2.21 | 0.6906 | 2.240 | ⚠ 临界（低于线 0.03） |
| `9qE8r85r` | 2.90 | 1.91 | 0.6586 | 2.030 | ❌ |
| `j2eo0oMO` | 2.86 | 1.86 | 0.6503 | 2.002 | ❌ |
| `9qEPO5K2` | 3.10 | 1.88 | 0.6065 | 2.170 | ❌ |
| `KPmvEYeE` | 3.07 | 1.74 | 0.5668 | 2.149 | ❌ |
| `QPYrpRlp` | 2.81 | 1.57 | 0.5587 | 1.967 | ❌ |

- 3/10 通过 0.70×S；2 颗临界（`O0JwXdk7` 0.6950、`E5VNe67L` 0.6906）；5 颗明显低于（0.5587–0.6586）。
- 结论：**平台当前不拦**，10 颗的 RA 通过结论不变；但按 0.70×S 风险口径只有 3/10 通过。若 IND 后续启用该检查，7 颗会被拦；若要 invest_S 合规，需要另开设置/结构优化批次，不能把这 10 颗直接标成 invest_S 合规。

### 2.6 ATOM 判定（严格口径）

按 `Claude/skills/GLOSSARY.md`：ATOM = 只用**单一数据集**字段（允许的分组字段除外）。`returns` 是 PV 内置字段，不是分组字段。

- 当前 10 颗表达式均含 `returns` + institutions6 字段；DB `expressions.atom_flag='combined'`、`atom_n_datasets=2`；平台 `classifications` 10/10 仅 `CLUSTER:CLUSTER`、`tags=[]`，无 `SINGLE_DATA_SET`/`ATOM`。
- ⇒ 当前 10 颗**不是 ATOM**；`MATCHES_PYRAMID` PASS 只表示金字塔主题匹配，不等于 ATOM。
- IND institutions6 单独：`expressions` 中 `region='IND' AND dataset='institutions6' AND atom_flag='atom' AND status='backtested'` 共 **46 条记录 / 40 个唯一表达式**；与 `backtest_results` 按 `expression_id` 关联后 46 条均有 Sharpe（跨 wave/设置，非本交付 10 颗的设置），S max **1.10**、avg **0.07**、min **−1.06**；S≥1.25 **0 条**、S≥1.58 **0 条** ⇒ 现有证据下**不能产出合格 ATOM**。
- 最高 S=1.10 已低于平台 `LOW_SHARPE` 1.25 线，因此无需再逐条检查 F/2Y 即可判定不合格。
- 反向核对：IND `backtest_results` 中 `dataset='institutions6'` 且 `sharpe≥1.25` 的 **31 条全部含 `returns`**（含本交付 10 颗与同族变体，全部为 wave232），无一条 ATOM-only；IND 的 46 条 ATOM-only 记录来自 wave175（40）与 `s2_institutions6_d1`（6），没有一条在 wave232 的交付设置下达到 1.25；这与 46 条 ATOM-only 的 S max=1.10 互相印证。
- ⚠ 口径修正：全库 `dataset='institutions6' AND atom_flag='atom'` 共 86 条，是**跨区**（IND 46 / GBR 17 / EUR 15 / ASI 8），不能当 IND 证据；且 `expressions.sharpe` 在 IND 46 条里仅 6 条有值，故本表统一用 **IND + `backtest_results` 关联后的 46 条**。
- 若仍要 ATOM：需要新机制/新字段组合，另发 ATOM-only 批次；不要把这 10 颗标成 ATOM。

---

## 3. 数据集信息

| 项 | 值 |
|---|---|
| 数据集 | `institutions6`（dataset id 593） |
| 语义 | Institutions and Beneficial Stake Ownership（机构/受益股东持股；IND 为季度申报口径，美国同类为 13F） |
| 类别 | `institutions`（IND 全区**仅此 1 个**数据集） |
| 字段 | 11 个，全部 `MATRIX` |
| 覆盖率 | 0.9915 – 0.992 |
| 平台用户数 | 2038 |
| 平台 alpha 数 | 12378 |
| valueScore / 金字塔倍率 | 1.0 / 1.0 |
| 金字塔 | `IND/D1/INSTITUTIONS`（×1.0）+ `IND/D1/PV`（×1.1），实测 effective = 2 |
| 更新频率 | 季度（机构持股季度披露：IND 为季度申报口径，美国同类为 13F；季内阶梯常数、季末跳变，含修正案） |

11 个字段的逐个画像（覆盖 / 用户数 / alpha 数 / 经济含义 / 裁决）见
[`docs/reference/IND/institutions6_field_profile.md`](../docs/reference/IND/institutions6_field_profile.md) §1。

---

## 4. 核心机制与算子逻辑

### 4.1 统一模板

```text
rank( -ts_regression( ts_zscore(returns, W), ts_zscore(<F>, W), W, rettype=0 ) )
# W = 252（主流）；decay = 126；STATISTICAL；truncation = 0.08
```

- `ts_zscore(returns, 252)`：把收益变成时序标准分，消除个股波动率量纲。
- `ts_zscore(<F>, 252)`：把季频慢变量变成同尺度趋势代理。
- `ts_regression(y, x, 252, rettype=0)`：取**残差**——剥掉“与持股趋势共动”的那部分收益。
- 外层负号：押注残差的**反转**（idiosyncratic 短期偏离回摆）。
- `rank(...)`：横截面转均匀分布，压极端值。
- `decay=126`：半年尺度平滑，把换手压到 0.24 左右（平台线 0.70 以内）。

### 4.2 各算子的作用与实证

| 组件 | 作用 | 实证 |
|---|---|---|
| `returns` 作因变量 | 固定方向，残差才有“收益偏离”含义 | 反向（flow 对 returns 回归）S −0.13 ~ 0.13，全灭 |
| `ts_regression(..., rettype=0)` | 取残差，剥慢趋势 | rettype=1/2/3 未系统测，0 是唯一验证可用档 |
| 外层负号 | 反转 | 去负号后 S 掉到 0.13 量级 |
| `ts_zscore(F, 252)` | 尺度归一 | 换 `ts_rank(F,252)` 同效（2.81），可作去极值替代 |
| `decay=126` | 降换手、稳 PnL | 换手 0.24；无 decay 的短窗版本换手高、S 低 |
| `group_neutralize(..., industry)` | 行业内中性，削行业暴露 | 3.07（sector 3.00 / market 2.98 / 无分组 2.98） |

### 4.3 字段角色：慢趋势代理，而非“机构方向”

决定性证据是**字段无关性**：用 `aggregate_share_count_all_owners` / `aggregate_equity_value_all_owners`（**不含任何机构信息**的全体股东字段）套同一模板，仍得 S 2.53 / 2.76；11 个字段逐个套，S 全部落在 2.27–3.20。

⇒ 收益来源是“收益对慢变量的残差反转”，字段只决定剥离哪一类尾部暴露。**不要把本族解释成“跟着机构买卖”**。

### 4.4 逐颗表达式

| alpha | 表达式 |
|---|---|
| `E5VNe67L` | `rank(-ts_regression(ts_zscore(returns, 252), ts_zscore(ts_delay(divide(quantity_institutional_shares_disposed, add(quantity_institutional_shares_acquired, quantity_institutional_shares_disposed)), 21), 252), 252, rettype=0))` |
| `JjP0Ja5l` | `rank(-ts_regression(ts_zscore(returns, 252), ts_zscore(quantity_institutional_shares_acquired, 252), 252, rettype=0))` |
| `9qEPO5K2` | `rank(-ts_regression(ts_zscore(returns, 252), ts_zscore(count_institutional_sellers_security, 252), 252, rettype=0))` |
| `KPmvEYeE` | `group_neutralize(rank(-ts_regression(ts_zscore(returns, 252), ts_zscore(quantity_institutional_shares_disposed, 252), 252, rettype=0)), industry)` |
| `qMEkJ2zj` | `rank(-ts_regression(ts_zscore(returns, 252), ts_zscore(market_value_institutional_shares_acquired, 252), 252, rettype=0))` |
| `9qE8r85r` | `rank(-ts_regression(ts_zscore(returns, 252), ts_zscore(aggregate_equity_value_institutions / aggregate_equity_value_all_owners, 252), 252, rettype=0))` |
| `0mjk2ZQv` | `rank(-ts_regression(ts_zscore(returns, 252), ts_zscore(count_institutional_holders_security, 252), 252, rettype=0))` |
| `j2eo0oMO` | `rank(-ts_regression(ts_zscore(returns, 252), ts_zscore(aggregate_share_count_institutions / aggregate_share_count_all_owners, 252), 252, rettype=0))` |
| `O0JwXdk7` | `rank(-ts_regression(ts_zscore(returns, 252), ts_zscore(count_institutional_buyers_security, 252), 252, rettype=0))` |
| `QPYrpRlp` | `rank(-ts_regression(ts_zscore(returns, 252), ts_zscore(market_value_institutional_shares_disposed, 252), 252, rettype=0))` |

### 4.5 量纲陷阱（已实证）

`unitHandling=VERIFY` 下 `add(<CSShare 字段>, 1)` 会触发 `UNITS` warning（`expected Unit[CSShare:1], found Unit[]`）。
比率化必须先 `divide` 成**无量纲**再加常数；`VkdZ3wKM`（3.14）就是带 `+1` 的脏版，只存档、不进交付。

### 4.6 外部证据（论坛 / 论文）

2026-10-23 用 `search_forum_posts` 检索 `institutions6` / `institutional holdings` / `13F` / `residual reversal`，取 4 条与本题直接相关的公开帖。**外部证据只用于校准机制解释与失败边界，不替代本轮回测**：

| 来源 | 可复用结论 | 与本轮的关系 |
|---|---|---|
| [机构广度：institutions6 印度市场的独特视角](https://support.worldquantbrain.com/hc/zh-cn/community/posts/43497507223191)（WL27618，2026-09-15，29 赞） | 新兴市场披露滞后 ⇒ 回测设保守延迟；按市值/板块分组做横截面排序是规避行业偏差的标配 | 与本轮 `delay=1` + `rank` + `group_neutralize(..., industry)` 一致；也解释季频阶梯字段需长窗平滑 |
| [【Alpha Idea】机构参与"新鲜度门"：IND 机构持股广度在机构撤退期的逆势吸筹尝试](https://support.worldquantbrain.com/hc/zh-cn/community/posts/43358755666967)（LC97552，2026-09-09，23 赞） | `institutions6` 计数类字段覆盖充足；冠军 `trade_when(ts_arg_max(holders,90)<33, signed_power(ts_quantile(divide(buyers, ts_mean(holders,72)),840,gaussian),1.6), -1)` 得 S 1.62 / F 1.37 / 2Y 2.47；失败边界：`ts_corr(buyers,holders,66)` 0.38、美元净流 0.44、渗透率 0.20、`sellers` 反向 0.71；`ts_arg_max` 作信号是“信号摧毁器”、作门控才有效；`greater(ts_delta)` 增长门 0.49–0.58 已证伪 | 其失败边界与本轮 §8 第 6 条、画像 §2.2 的“原始机构流 / 买卖广度 / churn / `ts_corr` / 反向残差”证伪清单**同向**；其冠军机制（参与度门控）与本轮（残差反转）不同，且设置不同（SUBINDUSTRY / decay 9 / trunc 0.03），S 1.62 不能与本轮 2.8–3.2 直接横比 |
| [13F 披露时滞下的思考：institutions18 数据启示](https://support.worldquantbrain.com/hc/zh-cn/community/posts/43497524382231)（2026-09-15，28 赞） | 13F 季末后最长 45 天申报；回测必须按**申报生效日**而非报告期截止日更新；高频换手机构的披露参考价值低，长线机构才有跟踪价值 | 支持本族“季频阶梯 + 252 长窗 + 保守 delay”的处理；也说明慢变量更适合当回归锚而非方向信号 |
| [【alpha灵感】双字段 alpha 构建提示词](https://support.worldquantbrain.com/hc/zh-cn/community/posts/40433238987159)（2026-05-13，99 赞） | 把 `A - expected(A\|B)`（Anchor + Residual）列为高级双字段结构；`corr` / `regression residual` 属独立的统计关系类算子 | 为本轮 `ts_regression(returns, F)` 取残差提供**结构合法性**；帖中无 IND/institutions6 参数与实证 |

> 论文线索（转引自“新鲜度门”帖，未逐篇复核原文，仅作机制假设来源）：Gabaix & Koijen (2023) 非弹性市场假说；Feng, He, Wang & Xiao (2026) 机构共同持有网络；Da, Larrain, Sialm & Tessada (2016) 养老金再配置的协调噪声交易；Gabaix et al. (2005) 机构交易与波动率。
> **本轮不依赖这些论文的结论**：决定性证据仍是 §4.3 的字段无关性 + 画像 §3 的 48 行实测；外部资料只解释“为什么慢披露/慢变量值得残差化”，并与公开失败边界交叉验证。

---

## 5. 逐颗说明（字段 → 机制 → 指标）

1. **`E5VNe67L`（3.20）** — 卖出占比 `dis/(acq+dis)` 先无量纲化、滞后 21 天再残差化。滞后削掉季末跳变的尖峰，是本批最高 S；2Y 3.00、robust 1.80。
2. **`JjP0Ja5l`（3.12）** — 买入股数水平残差；sub 1.92 / robust 1.97，全批最稳的子宇宙与稳健宇宙表现。
3. **`9qEPO5K2`（3.10）** — 卖出**家数**；与卖出股数不同维度（广度 vs 数量），S 仍 3.10，说明“剥离慢趋势”不依赖金额量纲。
4. **`KPmvEYeE`（3.07）** — 卖出股数 + `group_neutralize(..., industry)`；industry 是实测最优分组（sector 3.00 / market 2.98），换手最低（0.2387）。
5. **`qMEkJ2zj`（2.92）** — 买入**金额**；与 `JjP0Ja5l`（买入股数）互相关 0.953，二者只留其一作代表也合理。
6. **`9qE8r85r`（2.90）** — 机构市值 / 全体股东市值；2Y 3.18 为本批最高，比率化把“规模”除掉。
7. **`0mjk2ZQv`（2.87）** — 期末持有机构**家数**；2Y 2.08 为本批最低（仍高于 1.58 线）。
8. **`j2eo0oMO`（2.86）** — 机构股数 / 全体股东股数；与 `9qE8r85r` 互相关 0.904（同一“占比”语义的股数版 vs 市值版）。
9. **`O0JwXdk7`（2.82）** — 买入**家数**；与 `KPmv9vpg` 是同表达式重复件，后者已从交付集剔除。
10. **`QPYrpRlp`（2.81）** — 卖出**金额**；drawdown 0.0948 为本批最大，但 2Y 2.98 补偿。

---

## 6. 相关性现实（必须随交付一起读）

### 6.1 全池（31 颗过闸 → 29 个不同表达式）

- avg pairwise **0.685**，median **0.701**，min 0.325，max **0.9999**；406 对中 **204 对 ≥ 0.70**。
- max pair：`bl8210Wq` × `N1eLRWML` = 0.9999（同一 `quantity_disposed` 残差，仅差 `group_neutralize(..., market)` 外壳）。
- 跨字段并不更低：`JjP0Ja5l`（买入股数）× `qMEkJ2zj`（买入金额）= 0.953。
- **两两 < 0.70 的最大子集只有 9 颗** ⇒ 本族**不可能**产出 10 颗自相关合规篮子。

### 6.2 交付 10 颗

- avg **0.723**，median 0.713，min 0.609，max **0.953**（`JjP0Ja5l` × `qMEkJ2zj`）；45 对中 30 对 ≥ 0.70。
- 两两 < 0.70 的最大子集只有 **3 颗**（`E5VNe67L`、`KPmvEYeE`、`0mjk2ZQv`）。
- 结论：10 颗是**一个簇**。真实提交若要求“互相 < 0.70”，这 10 颗里最多只能取 3 颗；若目标是尽量多落地，应改用 §6.1 全池里那组 9 颗两两 <0.70 的子集（清单见字段画像 §5.1）并逐颗实测 self-corr。

---

## 7. 存档索引

| 内容 | 路径 / 位置 |
|---|---|
| 字段画像 + 回测档案（主文档） | `docs/reference/IND/institutions6_field_profile.md` |
| 本文（交付报告） | `reports/ind_institutions6_alpha_delivery_20261023.md` |
| 回测事实源 | `data/wqb.db` → `backtest_results`（`region=IND`, `wave=232`，48 行，31 颗过闸） |
| 表达式台账 | `data/wqb.db` → `expressions`（wave232，46 条唯一表达式；`KPmv9vpg`≡`O0JwXdk7`、`3qj1eYdz`≡`LL5bYolm` 按表达式去重合并） |
| Alpha 指标 / 2Y / 相关性 | `data/wqb.db` → `alphas`（`two_year_sharpe` / `is_ladder_sharpe` / `prod_correlation` / `self_correlation` / `corr_checked_at`） |
| DB 归档口径 | `alphas.status=COMPLETE` 表示**仿真完成**；平台提交状态看 `platform_status=UNSUBMITTED`。10 行的 `alpha_type/stage/platform_status/is_ladder_sharpe` 已于 2026-10-23 与平台对齐（REGULAR / IS / UNSUBMITTED / 2Y） |
| S4 预筛工具修复 | `world-quant-brain-mcp/tools_alpha.py`（`batch_get_alpha_metrics` 先走 `_slim_alpha_response`，以 `failed_ra_count=0` 作 READY 前置，并输出 `investability_sharpe` / `investability_fitness` / `investability_ratio`）；回归 `world-quant-brain-mcp/tests/test_tools_alpha_batch_metrics.py`（5 例） |
| 字段画像视图 | `data/wqb.db` → `field_profile_perf`（重建：`python tools/fields/field_profile.py --build --region IND`） |
| 平台元数据 | `get_datasets(region=IND, universe=TOP500, delay=1, category=institutions)`、`get_datafields(region=IND, universe=TOP500, delay=1, dataset_id=institutions6)`（**必须带 universe/delay**；缺省 TOP3000 会返回空） |
| 外部证据（论坛 / 论文） | 本文 §4.6（4 条论坛帖 URL + 论文线索；字段画像 §4.1 为摘要） |
| 表达式批次脚本（本地，非版本控制） | `logs/_tmp_ind_inst_batch_exprs.py`、`..._batch2.py`、`..._batch3.py`、`..._batch4.py`、`..._batch5.py`（canonical 存档以 `expressions` 表为准） |
| 相关性复测 | MCP `check_correlation(alpha_id, refresh=True)` / `compute_mutual_correlation(alpha_ids, threshold=0.7)` |
| 2Y 数据修复 | `python tools/data-repair/backfill_bt_two_year_from_ladder.py --region IND --wave 232 --infer-dataset`（默认 dry-run，`--apply` 才写） |
| 2Y 采集修复 + 回归 | `tools/harvest_multisim.py` / `wqb_db_mcp.py`（ladder 回落）；`tests/unit/06_wave_pipeline/test_harvest_two_year_from_ladder.py` |
| 提交层 checks | 只读 `GET /alphas/{id}/check`（10/10 RA PASS；SELF/PROD/DATA_DIVERSITY/REGULAR_SUBMISSION/POWER_POOL 实际值）；本地 `logs/_check_results.json`（未入库） |
| invest_S 口径 | `get_alpha_details` → `is.investabilityConstrained.sharpe`；`/check` 未下发 `LOW_INVESTABILITY_CONSTRAINED_SHARPE`；0.70×S 仅作风险监控 |
| ATOM-only 证据（IND，历史 wave175/s2） | `data/wqb.db` → `expressions`（`region='IND'`, `dataset='institutions6'`, `atom_flag='atom'`, `status='backtested'`，46 条记录 / 40 唯一表达式）JOIN `backtest_results`（`expression_id`，46 条均有 Sharpe；max S=1.10；`S≥1.25`=0） |

### 7.1 本批平台批次 ID

- batch2：multisim `1QW2e26Wz5glaRmJCV88FFd`（3 颗过闸）
- batch3：multisim `33LI325Hv4jx9Pp1c6zZd5Vx`（8/8 过闸）
- batch4：multisim `14zLjk8034Blc8diUoVcUxB`（7 过闸 + 1 带 UNITS warning）
- batch5：2 颗单发（`mLYdVKap` 3.16、`E5VNe67L` 3.20）

---

## 8. 边界、未完成项与后续

1. **未提交**：10 颗均为 `UNSUBMITTED`，无 `POST /submit`、无 OS 数据。提交是不可逆动作，需用户逐颗确认。
2. **prod 是快照**：0.59–0.67 为 2026-10-23 实测；生产池变动会漂移，提交前必须 `refresh=True` 复测。
3. **字段分布未在线取数**：无 BRAIN Labs 会话，偏度/峰度/分位/零膨胀未实测；`docs/reference/IND/institutions6_field_profile.md` 附录 A 已备好脚本，待有 Labs 权限后回填。
4. **同族高相关**：见 §6；不建议把 10 颗当篮子一起提交。
5. **未设置平台 name / color / tags / descriptions**：如需进入提交队列，应按 `wqb.alpha_properties.build_name/build_tags` 规范补设。
6. **机制层面已证伪**（可复用结论）：原始机构流、买入/卖出广度、churn、净价差、`ts_corr(flow, returns)`、反向残差（flow 对 returns）六类在 IND 全部无效（|S| ≤ 0.58）；`ts_regression` 的方向必须是“returns 对 F”。
7. **2Y 双载体缺陷已修（本轮附带，全链路）**：平台按 alpha 代际只发 `LOW_2Y_SHARPE` 或 `IS_LADDER_SHARPE` **之一**（`wqb.config.RA_2Y_NAMES` 两者都算 2Y），而多处代码此前只认前者 ⇒ wave232 有 **23/48 行** `two_year_sharpe` 落空，其中 10 行连 `dataset` 也为 NULL。已修：①采集 `tools/harvest_multisim.py::_extract_two_year_sharpe`、`wqb_db_mcp._flatten_platform_alpha`（并透传 `is_ladder_sharpe`）；②评审 `toolkit/metrics_cache.py`（ladder-only 曾判 `2Y_UNKNOWN`）、`brain-alpha-judge/judge_alpha.py`（内部 2Y 硬闸）；③提交层 `SUBMIT_HARD_GATE_WARNINGS`（ladder 的 WARNING 同属硬闸）；④修数 `tools/data-repair/backfill_bt_two_year_from_ladder.py`、`backfill_alpha_metrics_from_platform.py`、`tools/backfill_2y_from_platform.py`；⑤文档同步 `GLOSSARY.md`、`worldquant-submit-alpha/references/submit-chain.md`、`brain-how-to-pass-alpha-test/references/scenarios.md` / `gate-rules.md`、`docs/experience/01_platform_gates.md`、`wq-brain-ra-pipeline/references/decision-table.md` / `step7-diagnose.md`。存量回填：23 行补 2Y、10 行补 `dataset=institutions6`、13 行跨数据集探针按设计留 NULL。字段画像已重建，修复后 `best_2y` 如 `count_institutional_sellers_security` = 2.87（原 −0.15）、`market_value_institutional_shares_disposed` = 2.98（原 NULL）。回归用例见 §7。
8. **`query_field_profile` 的已知局限**：MCP 读 `field_profile_full`，该表当前只有 EUR 数据 ⇒ `query_field_profile(region="IND")` 返回 0 行；IND 画像需直接读 `field_profile_perf`（或视图 `field_profile_ind`）。本轮未改该工具，登记为缺口。
9. **invest_S 不是 IND 当前平台硬闸**：10/10 `/check` 未下发 `LOW_INVESTABILITY_CONSTRAINED_SHARPE`；按 0.70×S 风险口径 3/10 通过（2 颗临界、5 颗明显低于，§2.5）。不要把这 10 颗称为“invest_S 全过”；若用户要求 invest_S 合规，需要另开优化批次。
10. **ATOM**：10 颗为 `returns + institutions6` 双数据集（`atom_flag=combined`），不是 ATOM；纯 IND institutions6 46 条 ATOM-only 回测记录（40 唯一表达式）max S=1.10，未产出合格 ATOM（§2.6）。`MATCHES_PYRAMID` 不是 ATOM。
