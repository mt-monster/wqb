# IND × Institutions — `institutions6` 全字段画像与回测档案

> 区域：**IND**（固定）｜数据集：`institutions6`（IND 全 `institutions` 类别**唯一**数据集）
> 权威回测档位：`IND / TOP500 / D1 / STATISTICAL / decay 126 / truncation 0.08 / nanHandling OFF / maxTrade OFF / unitHandling VERIFY / pasteurization ON / P0Y0M0D / FULL`
> 最后更新：2026-10-23 ｜ 证据来源：平台元数据 + `data/wqb.db`（`backtest_results` / `field_profile_perf`）+ wave232 共 48 行实测，其中 **31 颗过闸（29 个不同表达式）** + 公开论坛/论文线索（§4.1；完整引文见交付报告 §4.6）
> 交叉引用：`docs/reference/field_profile_ind_inst_fund_20261019.md`（10-19 首轮画像，waves 376–392）

---

## §0 数据集清单（IND × institutions）

| 数据集 | 语义 | 字段 | 覆盖 | 平台用户 | 平台 alpha 数 | valueScore | 金字塔倍率 |
|---|---|---:|---:|---:|---:|---:|---:|
| **`institutions6`** | Institutions and Beneficial Stake Ownership（机构/受益股东持股；IND 为季度申报口径，美国同类为 13F） | 11 | 0.992 | 2038 | 12378 | 1.0 | 1.0 |

- IND 该类别**只有 1 个数据集**，不存在“换数据集”选项；本轮回测全部锁定该集。
- 金字塔：`IND/D1/INSTITUTIONS`（×1.0）+ `IND/D1/PV`（×1.1），实测 effective = 2。
  **本族用 `returns` 作因变量仍同时点亮两塔**（`MATCHES_PYRAMID` PASS），但按严格 ATOM 口径**不是 ATOM**：
  `returns` 是 PV 字段，本族为 `returns + institutions6` 双数据集（DB `atom_flag=combined`，`atom_n_datasets=2`）。
  纯 IND institutions6 ATOM 形态已实测 46 条记录（40 个唯一表达式），最高 S=1.10，未产出合格 ATOM（§2.4）。

---

## §1 字段画像（11/11，全部 MATRIX）

| # | 字段 | 类型 | 覆盖 | 用户 | alpha 数 | 经济含义 | 主画像裁决 |
|---|---|---|---:|---:|---:|---|---|
| 1 | `quantity_institutional_shares_disposed` | MATRIX | 0.992 | 590 | 1009 | 季度内机构卖出**股数** | **ALIVE**（本轮 3.20 / 3.10 / 3.07） |
| 2 | `quantity_institutional_shares_acquired` | MATRIX | 0.992 | 784 | 1679 | 季度内机构买入**股数** | **ALIVE**（本轮 3.12） |
| 3 | `count_institutional_sellers_security` | MATRIX | 0.992 | 621 | 1187 | 季度内卖出机构**家数** | **ALIVE**（本轮 3.10；旧画像 DEAD=0.32） |
| 4 | `market_value_institutional_shares_acquired` | MATRIX | 0.992 | 971 | 2499 | 季度内机构买入**金额** | **ALIVE**（本轮 2.92；旧画像 WEAK=1.10） |
| 5 | `aggregate_equity_value_institutions` | MATRIX | 0.992 | 629 | 1144 | 期末机构持股**市值** | **ALIVE**（比率化 2.90；旧画像 DEAD=0.88） |
| 6 | `count_institutional_holders_security` | MATRIX | 0.992 | 614 | 1167 | 期末持有机构**家数** | **ALIVE**（本轮 2.87） |
| 7 | `aggregate_share_count_institutions` | MATRIX | 0.992 | 568 | 1031 | 期末机构持股**股数** | **ALIVE**（比率化 2.86；旧画像 3.45） |
| 8 | `count_institutional_buyers_security` | MATRIX | 0.992 | 921 | 2171 | 季度内买入机构**家数** | **ALIVE**（本轮 2.82） |
| 9 | `market_value_institutional_shares_disposed` | MATRIX | 0.9915 | 523 | 933 | 季度内机构卖出**金额** | **ALIVE**（本轮 2.81） |
| 10 | `aggregate_equity_value_all_owners` | MATRIX | 0.992 | 795 | 1547 | 全体股东持股**市值**（母子去重） | **ALIVE**（本轮 2.76 / 2.41） |
| 11 | `aggregate_share_count_all_owners` | MATRIX | 0.992 | 578 | 1013 | 全体股东持股**股数**（母子去重） | **ALIVE**（本轮 2.53） |

**更新频率**：**季度**（机构持股季度披露：IND 为季度申报口径，美国同类为 13F；季内数值为阶梯常数，季末跳变；含修正案）。
平台未暴露频率字段，此判定由季度披露制度 + 实测指纹（原始水平族 TO 0.06–0.16）交叉确认。

**分布特征（可确证部分）**：
1. **全部非负**；金额/股数为重尾（右偏），计数类为右偏 + **零膨胀**（低流动股票整季 `buyers/sellers = 0`）。
2. **时序阶梯**：季内自相关≈1，季度边界跳变 ⇒ 任何 `ts_*` 长窗都在“跨季平均”，窗口语义 ≠ 日频字段。
3. **横截面**：`rank()` 后均匀；原始尺度不可直接线性相加（量纲：CSShare vs USD vs 计数）。
4. **量纲陷阱（本轮实证）**：`unitHandling=VERIFY` 下 `add(<CSShare 字段>, 1)` 触发 `UNITS` warning
   （`expected Unit[CSShare:1], found Unit[]`）。比率化必须先 `divide` 成无量纲再加常数；否则只能 `add(同量纲, 同量纲)`。
5. **偏度/峰度/分位数/正负比**：平台元数据不提供，需 Labs 原始面板；**附录 A 脚本待跑**（本轮无 Labs 会话）。

**可用性**：
- 覆盖率 0.9915–0.992（全库最高档），11 字段无 VECTOR，`ts_*` / `group_*` / `trade_when` 全部可直接用。
- 分组字段实测可用：`sector` / `industry` / `market` / `exchange` / `country` / `india_top500_method*_groupN`。
- 禁用算子（本轮实测）：`ts_decay_exp_window`（IND 不可用）、`ts_max`（toolkit 静态闸判 `INACCESSIBLE_OP`，用 `ts_rank` 替代）。

---

## §2 机制层：什么有效、什么已被证伪

### 2.1 唯一稳定有效族：`returns` 对慢变量残差化后取反

```text
rank(-ts_regression(ts_zscore(returns, W), ts_zscore(<F>, W), W, rettype=0))
# rettype=0 = 残差；W ∈ {63,126,252,378,504}；decay=126；STATISTICAL；trunc=0.08
```

`<F>` 可以是 11 个字段中**任意一个**（含全体股东字段），也可以是其比率/差分/滞后/秩变换。

### 2.2 已证伪（本轮 3 批 24 条，全部 |S| ≤ 0.58）

| 机制 | 代表表达式 | 实测 | 结论 |
|---|---|---|---|
| 原始净流量 | `rank(acq_q − dis_q)` | S ≤ 0.58，TO 0.06 | 季频流量无横截面预测力 |
| 买入广度 | `rank((buyers − sellers)/(buyers+sellers+1))` | S ≤ 0.58 | Griffin-Xu 经典信号在 IND 失效 |
| 换手/churn | `rank((buyers+sellers)/holders)` | S ≤ 0.58 | 同上 |
| 机构占比水平 | `rank(share_inst / share_all)` | S ≤ 0.58 | 水平量被 size 主导 |
| 净价差（成交价） | `rank(mv/qty_acq − mv/qty_dis)` | S ≤ 0.58 | 价差方向无信息 |
| 时序相关 | `rank(-ts_corr(ts_zscore(flow,63), returns, 252))` | S 0.34–0.49 | 相关结构不稳 |
| **反向**残差（flow 对 returns） | `rank(-ts_regression(flow, returns, rettype=0))` | S −0.13~0.13 | 方向必须固定为“returns 对 F” |
| 增长门 `greater(ts_delta(F))` | 论坛迁移 | S 0.49–0.58 | 论坛结论在 IND 复现失败 |

### 2.3 本轮新增的增强轴（全部 RA failed=0）

| 轴 | 实证 | 最佳 |
|---|---|---|
| 窗口 W | 63 → 2.27；252 → 2.98；378 → 2.80；504 → 2.74；126 → 2.64 | **252**（63 明显偏弱） |
| 滞后 21 天 | `ts_delay(F,21)` → **3.10**；比率+滞后 → **3.20** | **有效**（削峰 + 抗修订） |
| 分组中性化 | sector → 3.00；industry → **3.07**；market → 2.98 | **industry** |
| 非线性变换 | `ts_rank(F,252)` 替代 `ts_zscore` → 2.81 | 同效，可作去极值替代 |
| 复合比率 | `dis/(acq+dis)`（无量纲）→ 3.14；+lag21 → **3.20** | **最佳单条** |
| 残差类型 | `rettype=0`（残差）唯一可用；1/2/3 未测（留给后续） | 0 |

### 2.4 ATOM-only 上限（2026-10-23 补；口径修正：IND-only）

`expressions` 表筛选 `region='IND' AND dataset='institutions6' AND atom_flag='atom' AND status='backtested'`（纯 IND institutions6、不含 `returns`）共 **46 条记录 / 40 个唯一表达式**；与 `backtest_results` 按 `expression_id` 关联后 46 条均有 Sharpe（跨 wave/设置，非本交付 10 颗的设置）：

- S 最高 **1.10**、平均 **0.07**、最低 **−1.06**；`S ≥ 1.25` **0 条**，`S ≥ 1.58` **0 条**。
- 最高 S=1.10 已低于平台 `LOW_SHARPE` 1.25 线，因此无需再逐条检查 F/2Y 即可判定不合格。
- 反向核对：IND `backtest_results` 中 `dataset='institutions6'` 且 `sharpe≥1.25` 的 31 条全部含 `returns`（全部为 wave232）；无一条纯 ATOM-only 达到平台线。46 条 ATOM-only 记录来自 wave175（40）与 `s2_institutions6_d1`（6），没有一条在 wave232 的交付设置下达到 1.25。
- ⚠ 全库 `dataset='institutions6' AND atom_flag='atom'` 共 86 条，是**跨区**（IND 46 / GBR 17 / EUR 15 / ASI 8），不能当 IND 证据；`expressions.sharpe` 在 IND 46 条里仅 6 条有值，故本表统一用 **IND + `backtest_results` 关联后的 46 条**。
- ⇒ 现有证据下 **IND institutions6 单独不能产出合格 ATOM**。本族 10 颗是 `returns + institutions6` 双数据集
  （`atom_flag=combined`，`atom_n_datasets=2`），按 `GLOSSARY.md` 严格口径**不是 ATOM**；
  `MATCHES_PYRAMID` PASS 只表示金字塔主题匹配，不是 ATOM 分类。
- 本数据集的价值在“`returns` 对机构慢变量残差化”的交互项，不在单数据集方向信号；若要 ATOM，
  需要另立机制并另发 ATOM-only 批次，不能把这 10 颗标成 ATOM。

---

## §3 回测台账（wave232，48 行；institutions6 过闸 31 颗 / 29 个不同表达式）

> wave232 混有两批：① 2026-10-17 的 **23 行跨数据集探针**（含本期 institutions6 前 10 颗，`dataset` 记为 NULL）；
> ② 2026-10-23 的 **25 行 institutions6 实测**（batch2/3/4 的 multisim + batch5 的 2 颗单发）。
> 48 行中 **31 行过闸**（RA failed=0 且 S≥1.58 & F≥1.0）；其余 17 行里 13 行是其他数据集对照探针、4 行是 institutions6 的反向/原始信号证伪件。
> 过闸件里有 2 对重复表达式：`KPmv9vpg`≡`O0JwXdk7`、`3qj1eYdz`≡`LL5bYolm`。

### 3.1 过闸候选（RA failed=0，按 Sharpe 降序）

| alpha | 核心字段 | 机制 | S | F | TO | 2Y | sub | robust |
|---|---|---|---:|---:|---:|---:|---:|---:|
| `E5VNe67L` | disposed / (acq+dis) | 卖出占比 + lag21 | **3.20** | 2.52 | 0.2497 | 3.00 | 1.64 | 1.80 |
| `mLYdVKap` | disposed / (acq+dis) | 卖出占比（无滞后） | 3.16 | 2.45 | 0.2507 | 3.07 | 1.80 | 1.80 |
| `VkdZ3wKM` | disposed / (acq+dis) | 卖出占比（+1 脏版，仅存档） | 3.14 | 2.41 | 0.2532 | 3.29 | 1.81 | 1.82 |
| `gJWXMXNl` | acq_q − dis_q | 净流量残差 | 3.13 | 2.41 | 0.2487 | 3.04 | 1.87 | 1.70 |
| `JjP0Ja5l` | quantity_acquired | 水平残差 | 3.12 | 2.42 | 0.2461 | 2.82 | 1.92 | 1.97 |
| `9qEPO5K2` | count_sellers | 水平残差 | 3.10 | 2.38 | 0.2413 | 2.87 | 1.58 | 1.68 |
| `RRA91Z01` | quantity_disposed | lag21 残差 | 3.10 | 2.39 | 0.2424 | 2.98 | 1.81 | 1.86 |
| `KPmvEYeE` | quantity_disposed | industry 中性 | 3.07 | 2.36 | 0.2387 | 3.14 | 1.65 | 1.49 |
| `78o31b2Q` | quantity_disposed | sector 中性 | 3.00 | 2.28 | 0.2428 | 2.87 | 1.64 | 1.69 |
| `bl8210Wq` | quantity_disposed | 水平残差 | 2.98 | 2.25 | 0.2435 | 2.79 | 1.64 | 1.70 |
| `N1eLRWML` | quantity_disposed | market 中性 | 2.98 | 2.25 | 0.2435 | 2.80 | 1.64 | 1.70 |
| `qMEkJ2zj` | market_value_acquired | 水平残差 | 2.92 | 2.18 | 0.2460 | 2.66 | 1.77 | 1.74 |
| `9qE8r85r` | equity_inst / equity_all | 机构市值占比 | 2.90 | 2.15 | 0.2471 | 3.18 | 1.60 | 1.54 |
| `2rj9L9ob` | ts_delta(holders,63) | 季度持股增长 | 2.88 | 2.17 | 0.2427 | 2.30 | 1.18 | 1.50 |
| `0mjk2ZQv` | count_holders | 水平残差 | 2.87 | 2.14 | 0.2403 | 2.08 | 1.36 | 1.55 |
| `j2eo0oMO` | share_inst / share_all | 机构股数占比 | 2.86 | 2.13 | 0.2432 | 2.94 | 1.48 | 1.55 |
| `O0JwXdk7` | count_buyers | 水平残差 | 2.82 | 2.06 | 0.2475 | 2.40 | 1.32 | 1.63 |
| `KPmv9vpg` | count_buyers | 水平残差（重复） | 2.82 | 2.06 | 0.2475 | 2.40 | 1.32 | 1.63 |
| `npAm2mGx` | ts_rank(disposed,252) | 秩变换残差 | 2.81 | 2.06 | 0.2449 | 2.73 | 1.69 | 1.78 |
| `QPYrpRlp` | market_value_disposed | 水平残差 | 2.81 | 2.06 | 0.2433 | 2.98 | 1.34 | 1.38 |
| `RRA91Z00` | quantity_disposed | W=378 | 2.80 | 2.06 | 0.2455 | 2.87 | 1.33 | 1.45 |
| `E5VNENMr` | (buyers+sellers)/holders | churn 残差 | 2.78 | 2.03 | 0.2439 | 2.50 | 1.46 | 1.54 |
| `LL5bYolm` | equity_value_all_owners | 水平残差 | 2.76 | 1.97 | 0.2553 | 2.41 | 1.44 | 1.43 |
| `3qj1eYdz` | equity_value_all_owners | 重复（同 LL5bYolm） | 2.76 | 1.97 | 0.2553 | 2.41 | 1.44 | 1.43 |
| `N1eLrm2X` | quantity_disposed | W=504 | 2.74 | 2.00 | 0.2463 | 2.71 | 1.11 | 1.11 |
| `pwvJebEX` | share_count_institutions | 水平残差 | 2.68 | 1.92 | 0.2433 | 2.53 | 1.36 | 1.61 |
| `VkdwbQqM` | equity_value_institutions | 水平残差 | 2.65 | 1.88 | 0.2466 | 2.24 | 1.22 | 1.14 |
| `3qj1RrJ0` | quantity_disposed | W=126 | 2.64 | 1.92 | 0.2386 | 2.52 | 1.44 | 1.36 |
| `LL5Edbee` | share_count_all_owners | 水平残差 | 2.53 | 1.78 | 0.2366 | 2.79 | 1.42 | 1.28 |
| `ZYmgngv0` | 成交价差（acq−dis） | 实现价差残差 | 2.39 | 1.69 | 0.2291 | 2.23 | 1.06 | 1.09 |
| `2rj9NqEY` | quantity_disposed | W=63 | 2.27 | 1.51 | 0.2561 | 2.21 | 1.17 | 1.07 |

> 平台闸线（IND/TOP500/D1）：LOW_SHARPE ≥ 1.25、LOW_FITNESS ≥ 1.0、2Y / IS_LADDER ≥ 1.58、sub ≥ 0.1、robust ≥ 1.0。
> 以上 31 颗**全部** RA failed=0（`LOW_SHARPE`/`LOW_FITNESS`/`LOW_SUB_UNIVERSE_SHARPE`/`IS_LADDER_SHARPE`/`LOW_ROBUST_UNIVERSE_SHARPE`/`CONCENTRATED_WEIGHT`/`CLUSTER_TEST`/`MATCHES_PYRAMID` 全 PASS）。
> `SELF_CORRELATION` / `PROD_CORRELATION` 在 IS 阶段为 **pending**（平台提交时才评），已另行实测，见 §5。
> 未过闸的 17 行（13 行跨数据集对照 + 4 行 institutions6 证伪）见 §3.2。

### 3.2 不过闸记录（机制证伪证据）

| alpha | 机制 | S | RA failed |
|---|---|---:|---:|
| `xA1Vk8Ww` | `ts_corr(净流量, returns)` | 0.34 | 5 |
| `1YjOdbPX` | `ts_corr(buyers, returns)` | 0.49 | 4 |
| `YPx80KJR` | flow 对 returns 残差（反向） | −0.13 | 5 |
| `A1QePZEg` | 同上取正 | 0.13 | 4 |
| `LL5bYoG2` / `wp9wk7al` / `P0MrmL7E` 等 | 原始水平/广度/churn | 0.09–1.18 | 3–5 |

> 另 13 行是 2026-10-17 的**跨数据集对照探针**（`opt1_*` / `insd1_*` / `snt26_*`，`dataset` 记为 NULL），
> 不属于 institutions6，未计入本节证伪结论；它们只用于确认“残差模板换数据集后是否同样有效”，结果 S 0.09–1.18（无效）。

---

## §4 归因（决定性证据）

**证据链：字段无关性。**
用 `aggregate_share_count_all_owners` / `aggregate_equity_value_all_owners`（**不含任何机构信息**的全体股东字段）做同样的残差化，同样得到 S 2.53 / 2.76；11 个字段两两之间做同一模板，S 全部落在 2.3–3.2。

⇒ 该族的收益**不来自机构流方向**，而来自：

1. `ts_zscore(returns, 252)` 先取收益的时序标准化；
2. 对 `<F>`（季频慢变量）回归、取残差 ⇒ 剥掉“与慢速持股趋势共动的收益部分”；
3. 取反 ⇒ 押注** idiosyncratic 短期反转**；
4. `decay=126` + `rank` 把换手压到 0.24，使反转信号以半年尺度换手。

**为什么字段仍然重要**：`<F>` 决定残差里保留什么。季频阶梯变量的长窗自相关高，回归主要剥掉“长期趋势/规模暴露”，保留季度级别的收益偏离。不同字段剥离的尾部不同（金额 vs 股数 vs 家数 vs 全体），因此 S 在 2.3–3.2 之间浮动，但共同成分占主导（见 §5）。

**与旧画像的冲突解释**：旧画像把 `count_institutional_sellers_security` 判 DEAD（best S 0.32）、`aggregate_equity_value_institutions` 判 DEAD（0.88），是**用原始水平/方向信号**测的；本轮换成“returns 对其残差化”后同样字段给出 3.10 / 2.90。⇒ 旧 `DEAD` 标签的适用范围是“该字段作原始信号”，**不适用于残差化模板**。`field_profile_perf` 的 verdict 字段不能跨模板外推。

### 4.1 外部证据（论坛 / 论文，2026-10-23 检索）

只用于校准机制解释与失败边界，**不替代本轮回测**；完整引文与关系表见交付报告 §4.6。

- **IND 披露滞后**（[机构广度：institutions6 印度市场的独特视角](https://support.worldquantbrain.com/hc/zh-cn/community/posts/43497507223191)，WL27618，2026-09-15）：新兴市场报告落地有滞后，回测应设保守延迟；按市值/板块分组做横截面排序是规避行业偏差的标配。与本档 `delay=1` + `rank` + `group_neutralize(..., industry)` 一致。
- **参与广度门控**（[机构参与"新鲜度门"：IND 机构持股广度在机构撤退期的逆势吸筹尝试](https://support.worldquantbrain.com/hc/zh-cn/community/posts/43358755666967)，LC97552，2026-09-09）：`institutions6` 计数类字段覆盖充足；其冠军 `trade_when(ts_arg_max(holders,90)<33, signed_power(ts_quantile(divide(buyers, ts_mean(holders,72)),840,gaussian),1.6), -1)` 得 S 1.62 / F 1.37 / 2Y 2.47。可复用结论：① `ts_arg_max` **作信号**是信号摧毁器、**作门控**才有效；② 四条失败边界 `ts_corr(buyers,holders,66)=0.38`、美元净流 0.44、渗透率 0.20、`sellers` 反向 0.71，与本档 §2.2 的证伪清单同向；③ 其设置（SUBINDUSTRY / decay 9 / trunc 0.03）与本档不同，S 不可直接横比。
- **13F 披露时滞**（[13F 披露时滞下的思考：institutions18 数据启示](https://support.worldquantbrain.com/hc/zh-cn/community/posts/43497524382231)，2026-09-15）：13F 季末后最长 45 天申报，回测须按**申报生效日**而非报告期截止日；高频换手机构的披露参考价值低。支持本档“季频阶梯 + 252 长窗 + 保守 delay”的处理，也解释慢变量更适合当回归锚而非方向信号。
- **Anchor + Residual**（[【alpha灵感】双字段 alpha 构建提示词](https://support.worldquantbrain.com/hc/zh-cn/community/posts/40433238987159)，2026-05-13）：`A - expected(A|B)` 是高级双字段结构，`ts_regression` 取残差属统计关系类算子。为本档模板提供结构合法性，但帖中无 IND/institutions6 参数与实证。

> 论文线索（转引自“新鲜度门”帖，未逐篇复核）：Gabaix & Koijen (2023) 非弹性市场；Feng, He, Wang & Xiao (2026) 共同持有网络；Da, Larrain, Sialm & Tessada (2016) 养老金再配置；Gabaix et al. (2005) 机构交易与波动率。本轮结论不依赖这些论文，决定性证据仍是 §4 的字段无关性与 §3 的 48 行实测。

---

## §5 相关性现实（必须随交付一起读）

### 5.1 全池（31 颗过闸件 → 29 个不同表达式）

本地 PnL 计算（1023 个日观测，2026-10-23）：

- **avg pairwise 0.685，median 0.701，min 0.325，max 0.9999**；406 对中 **204 对 ≥ 0.70**。
- max pair = `bl8210Wq` × `N1eLRWML`（同一 `quantity_disposed` 残差，仅差 `group_neutralize(..., market)` 外壳）= **0.9999**。
- 同字段不同窗口：`3qj1RrJ0`(W126) × `bl8210Wq`(W252) = 0.705，与 `N1eLrm2X`(W504) = 0.716。
- **跨字段反而更高**：`JjP0Ja5l`(买入股数) × `qMEkJ2zj`(买入金额) = **0.953**。
- 全体股东字段（无机构信息）× 机构字段 ≈ 0.70–0.80。
- **两两 < 0.70 的最大子集只有 9 颗**（`2rj9NqEY`、`ZYmgngv0`、`3qj1RrJ0`、`LL5Edbee`、`N1eLrm2X`、`0mjk2ZQv`、`LL5bYolm`、`E5VNe67L`、`KPmvEYeE`）⇒ **本族不可能产出 10 颗自相关合规篮子**。

### 5.2 最终交付 10 颗

- **avg 0.723，median 0.713，min 0.609，max 0.953**（`JjP0Ja5l` × `qMEkJ2zj`）；45 对中 30 对 ≥ 0.70。
- 两两 < 0.70 的最大子集只有 **3 颗**（`E5VNe67L`、`KPmvEYeE`、`0mjk2ZQv`）。
- ⇒ 10 颗是**一个簇**，不是 10 个独立 alpha。**不构成 self-correlation 合规篮子**（平台自相关墙 0.70）。
- 真实提交必须逐颗比 `SELF_CORRELATION`；本交付的定位是“10 颗独立通过 RA + 指标验证的候选”，不是“10 颗可同时提交”。
  若目标是尽量多落地，应改从 §5.1 的 9 颗低相关子集里挑，并逐颗实测 self-corr。

---

## §6 结论与边界

1. IND × Institutions（`institutions6`，11 字段）**存在稳定可复现的残差反转族**：31/48 行过全部 RA 闸（29 个不同表达式），S 2.27–3.20，2Y 2.08–3.29，sub 1.06–1.92，robust 1.07–1.97。
2. 有效性的必要条件是 **`returns` 作因变量 + `rettype=0` + 取反 + decay126**；字段只作慢趋势代理。
3. 原始机构流、广度、churn、净价差、`ts_corr` 五类机制在本区**全部证伪**（|S| ≤ 0.58）。
4. 增强轴已实测：窗口 252 最优（63 明显弱）、lag21 有效、industry 分组最优、无量纲比率最强。
5. **不承诺可提交**：同族互相关 avg 0.72 / max 0.95，10 颗不构成 self-corr 合规篮子；`prod_correlation` 已逐颗实测 0.5925–0.6659（均 < 0.70），但仅在 2026-10-17 / 10-23 快照有效，提交前需 `refresh=True` 复测。
6. **ATOM 边界**：本族 10 颗是 `returns + institutions6` 双数据集（`atom_flag=combined`），**不是 ATOM**；纯 IND institutions6 的 46 条 ATOM-only 回测记录（40 唯一表达式）最高 S=1.10、`S≥1.25` 为 0，现有证据下不能产出合格 ATOM（§2.4）。

---

## §7 存档索引

| 内容 | 路径 |
|---|---|
| 本文（字段画像 + 回测档案） | `docs/reference/IND/institutions6_field_profile.md` |
| 交付报告（10 颗） | `reports/ind_institutions6_alpha_delivery_20261023.md` |
| 回测事实源 | `data/wqb.db` → `backtest_results`（region=IND, wave=232，48 行） |
| 表达式台账 | `data/wqb.db` → `expressions`（wave232，46 条唯一表达式；`KPmv9vpg`≡`O0JwXdk7`、`3qj1eYdz`≡`LL5bYolm` 按表达式去重合并） |
| ATOM-only 证据（IND，历史 wave175/s2） | `data/wqb.db` → `expressions`（`region='IND'`, `dataset='institutions6'`, `atom_flag='atom'`, `status='backtested'`，46 条记录 / 40 唯一表达式）JOIN `backtest_results`（`expression_id`，46 条均有 Sharpe；max S=1.10，`S≥1.25`=0） |
| Alpha 指标 / 相关性 | `data/wqb.db` → `alphas`（prod_correlation / self_correlation / two_year_sharpe / corr_checked_at） |
| 字段画像视图 | `data/wqb.db` → `field_profile_perf`（重建：`python tools/fields/field_profile.py --build --region IND`） |
| 表达式批次脚本（本地，非版本控制） | `logs/_tmp_ind_inst_batch_exprs.py`（batch1）、`..._batch2.py`、`..._batch3.py`、`..._batch4.py`、`..._batch5.py` |
| 平台元数据拉取 | `get_datasets(region=IND, universe=TOP500, delay=1, category=institutions)` / `get_datafields(region=IND, universe=TOP500, delay=1, dataset_id=institutions6)`（**必须带 universe/delay**；缺省 TOP3000 会返回空） |
| 外部证据（论坛 / 论文） | 本文 §4.1（4 条论坛帖 URL + 论文线索；完整表见交付报告 §4.6） |
| 相关性复测 | MCP `check_correlation(alpha_id, refresh=True)` / `compute_mutual_correlation(alpha_ids, threshold=0.7)` |
| 2Y 数据修复 | `python tools/data-repair/backfill_bt_two_year_from_ladder.py --region IND --wave 232 --infer-dataset`（`--apply` 才写） |

---

## 附录 A：Labs 原始面板分布脚本（待跑）

> 本轮无 BRAIN Labs 会话，以下脚本**未执行**。执行后把 JSON 回填到 §1「分布特征」。
> API 依据：`labs_data_analysis_agent.py`（`Brain(region=..., delay=..., universe=...)` → `get_data_field` → `get_data_frame`）。

```python
# 在 BRAIN Labs JupyterLab 中运行；输出 institutions6_panel_stats.json
import json
import numpy as np
import pandas as pd
from brain import Brain

FIELDS = [
    "quantity_institutional_shares_disposed", "quantity_institutional_shares_acquired",
    "count_institutional_sellers_security", "count_institutional_buyers_security",
    "count_institutional_holders_security", "market_value_institutional_shares_acquired",
    "market_value_institutional_shares_disposed", "aggregate_share_count_institutions",
    "aggregate_share_count_all_owners", "aggregate_equity_value_institutions",
    "aggregate_equity_value_all_owners",
]

brain = Brain(region="IND", delay=1, universe="TOP500")
out = {}
for fid in FIELDS:
    try:
        df = brain.get_data_frame(brain.get_data_field(fid))
    except Exception as exc:            # noqa: BLE001
        out[fid] = {"error": str(exc)}
        continue
    v = df.to_numpy(dtype=float)
    finite = np.isfinite(v)
    flat = v[finite]
    if flat.size == 0:
        out[fid] = {"error": "no finite values"}
        continue
    q = np.percentile(flat, [1, 5, 25, 50, 75, 95, 99])
    s = pd.Series(flat)
    # 季频指纹：同一 instrument 相邻有效观测的变动率
    diff = np.diff(v, axis=0)
    both = np.isfinite(diff)
    chg = float(np.mean(np.abs(diff[both]) > 0)) if both.any() else None
    out[fid] = {
        "coverage_cell": round(float(finite.mean()), 6),
        "zero_ratio": round(float((flat == 0).mean()), 6),
        "neg_ratio": round(float((flat < 0).mean()), 6),
        "mean": float(np.mean(flat)), "std": float(np.std(flat)),
        "skew": float(s.skew()), "kurt": float(s.kurt()),
        "p01": float(q[0]), "p05": float(q[1]), "p25": float(q[2]),
        "p50": float(q[3]), "p75": float(q[4]), "p95": float(q[5]), "p99": float(q[6]),
        "max": float(flat.max()),
        "nonzero_change_rate": chg,
    }

with open("institutions6_panel_stats.json", "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=2)
print(json.dumps({k: {"cov": d.get("coverage_cell"), "skew": d.get("skew"), "kurt": d.get("kurt")}
                  for k, d in out.items()}, ensure_ascii=False, indent=2))
```
