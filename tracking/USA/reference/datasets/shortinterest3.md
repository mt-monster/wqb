# shortinterest3 · USA/D1/TOP3000 字段画像与机制库

> 数据集：`shortinterest3`（Securities Lending Files — 证券借贷交易文件，费率/借券/利用率/期限）
> 区域/宇宙/Delay：USA / TOP3000 / D1 · 塔位：**SHORTINTEREST（1/3，未点亮）** · 倍率 ×1.0
> 平台规模：31 字段（**全 VECTOR**）· coverage 1.0 · alphaCount 8–2053 · 建档：2026-11-22
> 状态：**挖掘中**（存量 OS 件占「借券费率水平」；本波攻「费率离散度/波动率」）

---

## §0 数据集选择

| 候选 | 覆盖 | 字段 | 平台 aC | 判断 |
|---|---|---|---|---|
| **shortinterest3** | **1.0** | 31 | 8–2053 | ✅ 存量 OS 池只占 `mean_loan_rate` **水平**族；`max−min` 离散度 / `loan_rate_volatility` / 利用率 / 期限族**未占**（self 实测 0.30–0.33） |
| short_interest_pred | 0.9987 | 10 | 12–295 | 已测 30 臂 ⇒ PROVISIONAL（F 墙，见 `short_interest_pred.md`） |
| shortinterest29 | 0.8838 | 32 | 295 | `usa_dead_datasets.md`：RA 全过 0/68，max|S| 0.79 |
| shortinterest43 | 0.9994 | 32 | 1582 | 已有画像 `_usa-shortinterest43-field-profile-20261115.md` |
| us_short_sale | 1.0 | 4 | 375 | 已判死（日频做空量=噪声） |
| shortinterest24 | 0.2573 | 1 | 449 | 覆盖仅 1/4 宇宙，未测 |

**为什么选速率离散度而不是速率水平**：
- 存量 OS 件 `akKW0Lax` 属 **institutions20**（做空占比），不是 shortinterest3；
  shortinterest3 侧的 OS 池相关最高仅 0.33（MPYwqvLn self 0.3292）⇒ 头寸空间充足。
- 水平族（`mean_loan_rate` 的 ts_mean/reverse）已在前批实测 prod 0.7767 墙；
  **离散度 = 借券市场摩擦/分歧**，经济机制不同，实测 S1.98 / F2.53 / ret20.4%。

---

## §0.1 字段全表（分母 = 平台 31 字段，逐字段真实 id，无通配）

| # | 字段 id | 类型 | 覆盖 | aC | 族 |
|---|---|---|---|---|---|
| 1 | `loaned_share_count_r2` | VECTOR | 1.0 | 8 | V1 借出量（bin） |
| 2 | `loaned_market_value_usd_main` | VECTOR | 1.0 | 12 | V1 借出市值 |
| 3 | `loaned_share_count_r2_d1` | VECTOR | 1.0 | 13 | V1 借出量（bin） |
| 4 | `loaned_market_value_usd` | VECTOR | 1.0 | 17 | V1 借出市值 |
| 5 | `loaned_share_count_main` | VECTOR | 1.0 | 21 | V1 借出量 |
| 6 | `new_loaned_share_count_d1` | VECTOR | 1.0 | 21 | V1 新借出量 |
| 7 | `average_loan_duration_days_main` | VECTOR | 1.0 | 28 | V5 期限 |
| 8 | `average_loan_duration_days` | VECTOR | 1.0 | 29 | V5 期限 |
| 9 | `loaned_share_count` | VECTOR | 1.0 | 40 | V1 借出量 |
| 10 | `available_market_value_usd` | VECTOR | 1.0 | 44 | V6 可借市值 |
| 11 | `rate_bin_lower_limit_d1` | VECTOR | 1.0 | 45 | V3 费率 bin 下界 |
| 12 | `rate_bin_upper_limit_d1` | VECTOR | 1.0 | 52 | V3 费率 bin 上界 |
| 13 | `rate_bin_lower_limit` | VECTOR | 1.0 | 63 | V3 费率 bin 下界 |
| 14 | `transaction_count` | VECTOR | 1.0 | 64 | V1 交易笔数 |
| 15 | `new_loaned_share_count` | VECTOR | 1.0 | 65 | V1 新借出量 |
| 16 | `transaction_count_main` | VECTOR | 1.0 | 66 | V1 交易笔数 |
| 17 | `rate_bin_upper_limit` | VECTOR | 1.0 | 74 | V3 费率 bin 上界 |
| 18 | `borrow_activity_score` | VECTOR | 1.0 | 80 | V4 借券需求分 1–10 |
| 19 | `loan_utilization_ratio_d1` | VECTOR | 1.0 | 98 | V4 利用率 |
| 20 | `max_loan_rate_main` | VECTOR | 1.0 | 105 | V2 费率上界 |
| 21 | `loan_rate_volatility_main` | VECTOR | 1.0 | 113 | V3 费率波动 |
| 22 | `max_loan_rate` | VECTOR | 1.0 | 115 | V2 费率上界 |
| 23 | `mean_loan_rate_main` | VECTOR | 1.0 | 128 | V2 费率均值 |
| 24 | `loan_rate_volatility` | VECTOR | 1.0 | 150 | V3 费率波动 |
| 25 | `available_share_count` | VECTOR | 1.0 | 151 | V6 可借股数 |
| 26 | `min_loan_rate` | VECTOR | 1.0 | 163 | V2 费率下界 |
| 27 | `loan_utilization_ratio` | VECTOR | 1.0 | 200 | V4 利用率 |
| 28 | `min_loan_rate_main` | VECTOR | 1.0 | 254 | V2 费率下界 |
| 29 | `mean_loan_rate` | VECTOR | 1.0 | 295 | V2 费率均值 |
| 30 | `shrt3_utilizationpercent_units` | VECTOR | 1.0 | 1095 | V4 利用率（%） |
| 31 | `shrt3_bar` | VECTOR | 1.0 | 2053 | V4 借券需求评级 1–10 |

---

## §0.2 机制假设与模板白名单

| 机制 | 经济逻辑 | 预期符号 | 首选模板 | 实测/备注 |
|---|---|---|---|---|
| **M1 费率离散度** | 成交费率 max−min 大 = 借贷双方定价分歧/摩擦大 ⇒ 未来负收益 | 负（reverse） | `reverse(group_zscore(ts_mean(subtract(vec_avg(max_loan_rate), vec_avg(min_loan_rate)), 22), industry))` | **Grm9LXbZ S1.98/F2.53/TO6.19%/2Y3.11；仅 SUB 0.84 vs 0.86 差 0.02** |
| **M2 费率相对离散度** | (max−min)/mean，去规模 | 负 | 同上加 `divide(..., vec_avg(mean_loan_rate))` | gJaLMXbQ S1.31/F1.12/SUB 0.41 FAIL |
| **M3 费率波动率** | 费率的时序方差（stress） | 负 | `reverse(group_zscore(ts_covariance(vec_stddev(loan_rate_volatility), vec_stddev(loan_rate_volatility), 22), industry))` | 78Yl13Lx S1.58/F1.77/2Y2.52/SUB 0.57 FAIL |
| **M4 借券需求分** | borrow_activity_score 高 = 需求旺 | 负 | `reverse(group_zscore(ts_mean(vec_avg(borrow_activity_score), 22), industry))` | rK78l9eo S1.13/F1.10/SUB 0.42 FAIL |
| **M5 利用率** | 借出/可借比例高 = 拥挤 | 负 | `reverse(group_zscore(ts_mean(vec_avg(loan_utilization_ratio), 22), industry))` | XgaMnVJx S0.87/F0.76 |
| **M6 期限** | 平均借券期限长 = 结构性看空 | 待实测 | `reverse(group_zscore(ts_mean(vec_avg(average_loan_duration_days), 22), industry))` | 1YW0dOjJ S0.02 |
| **M7 新借出占比** | 新借出/存量 = 边际做空需求 | 待实测 | `reverse(group_zscore(ts_mean(divide(vec_avg(new_loaned_share_count), vec_avg(loaned_share_count)), 22), industry))` | QP06VOYW S−0.67 |
| **M8 可借覆盖** | 可借/已借 = 空头回补余量 | 待实测 | `reverse(group_zscore(ts_mean(divide(vec_avg(available_share_count), vec_avg(loaned_share_count)), 22), industry))` | 58JYOrjX S−0.66 |
| **M9 市值利用率** | 借出市值/可借市值 | 负 | `reverse(group_zscore(ts_mean(divide(vec_avg(loaned_market_value_usd), vec_avg(available_market_value_usd)), 22), industry))` | kqa90vNl S1.20/F1.26 |

**禁止**：跨集组腿（本波 ATOM 单集）；`mean_loan_rate` 水平族已 prod 0.7767 墙，不再作主核；
`rate_bin_*` 是 bin 边界（非信号），只作探针完整性。

---

## §1 全字段实测读数（31/31，零抽样）

> 设置：USA/TOP3000/D1，SUBINDUSTRY，decay 5，trunc 0.08，nanHandling ON，maxTrade OFF。

| 字段 | 探针/机制表达式 | Sharpe | Fitness | Turnover | 备注 |
|---|---|---|---|---|---|
| `mean_loan_rate` | `reverse(group_zscore(ts_mean(abs(ts_delta(vec_avg(mean_loan_rate),1)),22),industry))` | 1.74 | 1.37 | 0.1410 | omE2vmZn；2Y 3.06 / invest 0.925 / prod 0.7793 |
| `mean_loan_rate_main` | 待回填 | — | — | — | — |
| `max_loan_rate` | `reverse(group_zscore(ts_mean(subtract(vec_avg(max_loan_rate),vec_avg(min_loan_rate)),22),industry))` | 1.98 | 2.53 | 0.0619 | Grm9LXbZ；SUB 0.84 vs 0.86 |
| `min_loan_rate` | 同 Grm9LXbZ | 1.98 | 2.53 | 0.0619 | 与 max 同式 |
| `max_loan_rate_main` | 待回填 | — | — | — | — |
| `min_loan_rate_main` | 待回填 | — | — | — | — |
| `loan_rate_volatility` | `reverse(group_zscore(ts_covariance(vec_stddev(loan_rate_volatility),vec_stddev(loan_rate_volatility),22),industry))` | 1.58 | 1.77 | 0.1041 | 78Yl13Lx；SUB 0.57 FAIL |
| `loan_rate_volatility_main` | 待回填 | — | — | — | — |
| `borrow_activity_score` | `reverse(group_zscore(ts_mean(vec_avg(borrow_activity_score),22),industry))` | 1.13 | 1.10 | 0.0322 | rK78l9eo；SUB 0.42 FAIL |
| `shrt3_bar` | 待回填 | — | — | — | — |
| `loan_utilization_ratio` | `reverse(group_zscore(ts_mean(vec_avg(loan_utilization_ratio),22),industry))` | 0.87 | 0.76 | 0.0215 | XgaMnVJx；SUB 0.36 FAIL |
| `loan_utilization_ratio_d1` | 待回填 | — | — | — | — |
| `shrt3_utilizationpercent_units` | 待回填 | — | — | — | — |
| `average_loan_duration_days` | `reverse(group_zscore(ts_mean(vec_avg(average_loan_duration_days),22),industry))` | 0.02 | 0.00 | 0.0338 | 1YW0dOjJ；无信号 |
| `average_loan_duration_days_main` | 待回填 | — | — | — | — |
| `new_loaned_share_count` | `reverse(group_zscore(ts_mean(divide(vec_avg(new_loaned_share_count),vec_avg(loaned_share_count)),22),industry))` | -0.67 | -0.33 | 0.0657 | QP06VOYW；反号 |
| `new_loaned_share_count_d1` | 待回填 | — | — | — | — |
| `loaned_share_count` | 同 QP06VOYW | -0.67 | -0.33 | 0.0657 | 与 new 同式 |
| `loaned_share_count_main` | 待回填 | — | — | — | — |
| `loaned_share_count_r2` | 待回填 | — | — | — | — |
| `loaned_share_count_r2_d1` | 待回填 | — | — | — | — |
| `loaned_market_value_usd` | `reverse(group_zscore(ts_mean(divide(vec_avg(loaned_market_value_usd),vec_avg(available_market_value_usd)),22),industry))` | 1.20 | 1.26 | 0.0308 | kqa90vNl；S 未过闸 |
| `loaned_market_value_usd_main` | 待回填 | — | — | — | — |
| `available_market_value_usd` | 同 kqa90vNl | 1.20 | 1.26 | 0.0308 | 与 loaned 同式 |
| `available_share_count` | `reverse(group_zscore(ts_mean(divide(vec_avg(available_share_count),vec_avg(loaned_share_count)),22),industry))` | -0.66 | -0.42 | 0.0336 | 58JYOrjX；反号 |
| `transaction_count` | 待回填 | — | — | — | — |
| `transaction_count_main` | 待回填 | — | — | — | — |
| `rate_bin_lower_limit` | 待回填 | — | — | — | bin 边界，非信号 |
| `rate_bin_upper_limit` | 待回填 | — | — | — | bin 边界，非信号 |
| `rate_bin_lower_limit_d1` | 待回填 | — | — | — | bin 边界，非信号 |
| `rate_bin_upper_limit_d1` | 待回填 | — | — | — | bin 边界，非信号 |

---

## §2 结论（PROVISIONAL：prod 饱和，停止投放）

### 2.1 机制 × 闸门矩阵（全部实读）

| 机制 | 代表 alpha | S | F | TO | 2Y | invest比 | self | prod | 判读 |
|---|---|---|---|---|---|---|---|---|---|
| 费率波动（cov/abs delta） | MPYwqvLn | 1.74 | 1.40 | 0.1772 | 3.27 | 0.971 | 0.329 | **0.7342** | 只卡 prod |
| 费率波动（abs delta） | omE2vmZn | 1.74 | 1.37 | 0.1410 | 3.06 | 0.925 | 0.300 | **0.7793** | 只卡 prod |
| 费率离散度 max−min（22d/industry） | Grm9LXbZ | 1.98 | 2.53 | 0.0619 | 3.11 | 0.803 | — | — | SUB 0.84 vs 0.86 |
| 费率离散度 max−min（66d/industry） | LLK3denv | 1.95 | 2.53 | 0.0357 | 3.06 | 0.826 | **0.7135** | **0.9499** | self+prod 双挂（prod [0.9,1] 60 颗密墙） |
| 费率离散度（22d/market） | A1xE76gE | 2.72 | 5.63 | 0.0559 | 4.76 | 0.713 | — | **0.9091** | prod 挂 + CW 0.104 |
| 费率离散度（22d/sector） | VkNe3nXJ | 2.54 | 4.58 | 0.0601 | 4.04 | 0.717 | — | — | SUB 0.93 vs 1.1 |
| 离散度双窗 5+66 | KPgZEeLE | 1.95 | 2.52 | 0.0857 | 3.08 | 0.851 | — | — | CW fail |
| 离散度 5d | 1YW0zvJm | 1.88 | 2.19 | 0.1393 | 3.03 | 0.894 | — | — | CW warning（RA1） |
| vol-of-vol | 78Yl13Lx | 1.58 | 1.77 | 0.1041 | 2.52 | 0.987 | — | **0.8419** | prod 挂 + SUB 0.57 |
| 借券需求分 | rK78l9eo | 1.13 | 1.10 | 0.0322 | 1.83 | 0.956 | — | — | S/SUB 挂 |
| 利用率 | XgaMnVJx | 0.87 | 0.76 | 0.0215 | 1.54 | 0.943 | — | — | 全弱 |
| 期限 | 1YW0dOjJ | 0.02 | 0.00 | 0.0338 | 0.42 | — | — | — | 无信号 |
| 新借出占比 | QP06VOYW | -0.67 | -0.33 | 0.0657 | -1.35 | — | — | — | 反号 |
| 可借覆盖 | 58JYOrjX | -0.66 | -0.42 | 0.0336 | -1.06 | — | — | — | 反号 |
| 市值利用率 | kqa90vNl | 1.20 | 1.26 | 0.0308 | 2.00 | 0.850 | — | — | S 未过 |

### 2.2 结论

- **prod 是这个数据集的唯一墙**：level 0.7767 / vol 0.734–0.779 / vol-of-vol 0.842 / dispersion 0.909–0.950。
  prod 直方图在 [0.7,0.8) / [0.8,0.9) / [0.9,1] 都有数百颗 ⇒ **密墙，不是单钉**。
- **F/S/2Y/TO/invest 都能过**（LLK3denv RA=0 全绿：S1.95/F2.53/2Y3.06/SUB0.92/invest0.826），
  但 self 0.7135 + prod 0.9499 双挂 ⇒ 不可交付。
- 按 §7.6 记 **PROVISIONAL（prod 饱和）**，不判数据集级死；
  **重开条件**：production 池换季/该族 ACTIVE 退役，或出现全新字段（如 2026-03 上架的新字段未在池中）。
- **不再在本集堆同族变体**（prod 密墙下换窗口/分组轴已验证无效：22d industry 0.95、22d market 0.91）。

