# USA · `earnings7` 字段画像

> 由 `tools/fields/profile_dataset_fields.py` 生成，输入为 `get_datafields` 原始返回。零平台配额。

## 1 规模与完整性

| 项 | 值 |
|---|---|
| 本次返回字段数 | 40 |
| 平台声明数 `platform_count` | 40 |
| 返回 `count` | 40 |
| 是否完整 `complete` | True |
| 类型分布 | {'VECTOR': 40} |
| 平均 coverage | 0.6479 |
| 判定 | ✅ 完整 |

## 2 可用性分档

### 2.1 coverage

| 档 | 字段数 |
|---|---|
| ≥0.90（可直接做尽） | 15 |
| 0.40–0.70（稀疏，慎用） | 14 |
| <0.40（枯竭） | 6 |
| 0.70–0.90（sub/robust 需关注） | 5 |

### 2.2 拥挤度（决定 prod 相关性风险）

| 档 | 字段数 |
|---|---|
| 低拥挤（≤50 alpha） | 33 |
| 中拥挤（51–500） | 7 |

零竞争字段（`userCount==0`）：**0** / 40；描述带单位标注：0

## 3 语义结构

| 语义族 | 字段数 | 示例字段 |
|---|---|---|
| 盈利能力 | 18 | `eps_fiscal_quarter`, `eps_fiscal_quarter_fast_d1`, `eps_fiscal_year`, `eps_fiscal_year_fast_d1` |
| 未归类 | 12 | `confcall_financial_year`, `confcall_financial_year_fast_d1`, `confcall_fiscal_quarter`, `confcall_fiscal_quarter_fast_d1` |
| 分红/回购 | 6 | `dividend_amount_original_currency`, `dividend_amount_original_currency_fast_d1`, `dividend_payment_frequency_2`, `dividend_payment_frequency_2_fast_d1` |
| 每股口径 | 4 | `ern7_div_amount`, `ern7_div_amount_fast_d1`, `ern7_div_amount_usd`, `ern7_div_amount_usd_fast_d1` |

**时间朝向**（`forecast`=前瞻/预测，`realized`=已实现/事后，`mixed`=差值构造）：

| 朝向 | 字段数 |
|---|---|
| unknown | 32 |
| realized | 6 |
| forecast | 2 |

## 4 名字前缀聚类（前 15）

| 前缀 | 字段数 |
|---|---|
| `ern7_div` | 6 |
| `earnings_date` | 4 |
| `eps_fiscal` | 4 |
| `prelim_eps` | 4 |
| `confcall_financial` | 2 |
| `confcall_fiscal` | 2 |
| `dividend_amount` | 2 |
| `dividend_payment` | 2 |
| `earnings_announcement` | 2 |
| `eps_original` | 2 |
| `ern7_co` | 2 |
| `ern7_dsu` | 2 |
| `ern7_spe` | 2 |
| `estimated_earnings` | 2 |
| `next_earnings` | 2 |

## 5 候选短名单（Top 25，按打分排序）

打分 = 覆盖 40 + 低拥挤 25 + 语义可解释 20 + 前瞻 5（非信号 −30）。**只做排序参考**，仍须过单位闸与机制假设。

| # | 字段 | 类型 | cov | user | alpha | 语义族 | 朝向 | 分 | 描述（截断） |
|---|---|---|---|---|---|---|---|---|---|
| 1 | `eps_fiscal_quarter` | VECTOR | 0.953 | 37 | 48 | 盈利能力 | - | 80.0 | Fiscal quarter to which the reported EPS relates (1-4) |
| 2 | `eps_fiscal_year` | VECTOR | 0.953 | 14 | 19 | 盈利能力 | - | 80.0 | Fiscal year to which the reported EPS relates |
| 3 | `eps_fiscal_year_fast_d1` | VECTOR | 0.952 | 14 | 16 | 盈利能力 | - | 80.0 | Fiscal year to which the reported EPS relates |
| 4 | `eps_original_currency` | VECTOR | 0.934 | 11 | 11 | 盈利能力 | - | 79.3 | Currency code for the original currency in which EPS was reported |
| 5 | `eps_original_currency_fast_d1` | VECTOR | 0.933 | 15 | 15 | 盈利能力 | - | 79.3 | Currency code for the original currency in which EPS was reported |
| 6 | `ern7_dsu_spe_fast_d1` | VECTOR | 0.913 | 17 | 23 | 盈利能力 | realized | 78.5 | Reported earnings per share in US Dollars |
| 7 | `ern7_co_spe_fast_d1` | VECTOR | 0.899 | 14 | 17 | 盈利能力 | realized | 77.9 | Reported earnings per share in original currency |
| 8 | `estimated_earnings_fiscal_year` | VECTOR | 0.871 | 64 | 81 | 盈利能力 | forecast | 73.7 | Estimated fiscal year for which the EPS is provided |
| 9 | `estimated_earnings_fiscal_year_fast_d1` | VECTOR | 0.869 | 92 | 156 | 盈利能力 | forecast | 73.6 | Estimated fiscal year for which the EPS is provided |
| 10 | `eps_fiscal_quarter_fast_d1` | VECTOR | 0.952 | 49 | 54 | 盈利能力 | - | 72.0 | Fiscal quarter to which the reported EPS relates (1-4) |
| 11 | `ern7_dsu_spe` | VECTOR | 0.914 | 72 | 185 | 盈利能力 | realized | 70.5 | Reported earnings per share in US Dollars |
| 12 | `ern7_co_spe` | VECTOR | 0.900 | 47 | 82 | 盈利能力 | realized | 69.9 | Reported earnings per share in original currency |
| 13 | `dividend_payment_frequency_2` | VECTOR | 0.503 | 3 | 5 | 分红/回购 | - | 61.2 | How often the dividend is paid (e.g., annual, quarterly) as an integer frequency code |
| 14 | `dividend_payment_frequency_2_fast_d1` | VECTOR | 0.503 | 5 | 7 | 分红/回购 | - | 61.2 | How often the dividend is paid (e.g., annual, quarterly) as an integer frequency code |
| 15 | `ern7_div_amount` | VECTOR | 0.504 | 22 | 28 | 每股口径 | - | 61.2 | Dividend amount paid per share in the issuer's local currency |
| 16 | `ern7_div_amount_fast_d1` | VECTOR | 0.504 | 16 | 17 | 每股口径 | - | 61.2 | Dividend amount paid per share in the issuer's local currency |
| 17 | `ern7_div_amount_usd` | VECTOR | 0.504 | 30 | 48 | 每股口径 | - | 61.2 | Dividend amount paid per share, converted into US dollars |
| 18 | `ern7_div_amount_usd_fast_d1` | VECTOR | 0.504 | 14 | 14 | 每股口径 | - | 61.2 | Dividend amount paid per share, converted into US dollars |
| 19 | `dividend_amount_original_currency` | VECTOR | 0.499 | 9 | 9 | 分红/回购 | - | 61.0 | The currency code (integer) representing the original currency in which the dividend amou… |
| 20 | `dividend_amount_original_currency_fast_d1` | VECTOR | 0.499 | 6 | 6 | 分红/回购 | - | 61.0 | The currency code (integer) representing the original currency in which the dividend amou… |
| 21 | `ern7_div_amount_oc` | VECTOR | 0.498 | 32 | 45 | 分红/回购 | - | 61.0 | dividend amount |
| 22 | `ern7_div_amount_oc_fast_d1` | VECTOR | 0.499 | 26 | 30 | 分红/回购 | - | 61.0 | dividend amount |
| 23 | `earnings_announcement_time_of_day` | VECTOR | 1.000 | 23 | 25 | 未归类 | - | 60.0 | Numeric code indicating the expected time of day when the earnings announcement is schedu… |
| 24 | `earnings_date_fiscal_quarter` | VECTOR | 1.000 | 23 | 24 | 未归类 | - | 60.0 | Numeric value (1-4) indicating which fiscal quarter the earnings date pertains to |
| 25 | `earnings_date_fiscal_year` | VECTOR | 1.000 | 27 | 31 | 未归类 | - | 60.0 | Numeric value representing the fiscal year associated with the scheduled or reported earn… |

---

## 6 人工判读（自动打分不可直接采信，本节是结论）

### 6.1 自动榜前三名是伪信号，必须剔除

第 5 节的打分只看了「coverage × 低拥挤」，**完全不识别字段语义是元数据**。前 5 名全部是分类码而非经济量：

| 字段 | 真实含义 | 为什么不能做信号 |
|---|---|---|
| `eps_fiscal_quarter` | 财季编号 1–4 | 分类码。`group_rank` 后得到「谁的财报在第 4 季度」= 季节性伪信号 |
| `eps_fiscal_year` | 财年（如 2023） | 逐年递增的序号。`ts_delta` 或 `ts_rank` 会得到「时间流逝」，对所有股票一致 ⇒ 零横截面差异 |
| `eps_original_currency` | 货币码（整数枚举） | 分类码。rank 后等于「按货币编号排序」= 纯噪声 |
| `earnings_date_fiscal_quarter` / `earnings_date_fiscal_year` | 公告所属财季/财年 | 同上 |
| `earnings_announcement_time_of_day` | 盘前/盘中/盘后编码 | 3 值分类码。理论上可当「公告时点」条件变量，但不能单独成信号 |
| `confcall_fiscal_quarter` / `confcall_financial_year` / `next_earnings_quarter` | 电话会财季/财年 | 同上 |

**结论**：上表 8 个字段（及其 `_fast_d1` 副本共 15 个）**一律不进信号腿**。它们最多能当 `trade_when` 的条件变量（如「只在盘后公告时持仓」），在 ATOM 单数据集约束下价值极低。

### 6.2 `_fast_d1` 是重复版本，不是新字段

40 个字段里 **20 个带 `_fast_d1` 后缀**，与对应主字段描述逐字相同，coverage 差 ≤0.002。这是同一数据的「快速更新版」，**不构成独立信息维度**。

⇒ 数据集的**有效独立字段数 = 20**，不是 40。评估可点塔能力时按 20 算。
⇒ 同族已两次实测「换版本零收益」（波 178 `momentum_factor_score ≡ relative_momentum_factor`；波 184 `trsd_3mfte ≡ trsd_4mfte` 指标逐位相同）⇒ **不要用 `_fast_d1` 当第二个载体**。

### 6.3 唯一「几乎全空」的字段族

`prelim_eps_lower_bound` / `prelim_eps_upper_bound`（及两个 `_fast_d1`）：coverage **0.0091**，即 99% 的股票日没有值。

这与 earnings6 的 `eps_change_percentage_value`（实测 `longCount=0` / `pnl=0` / `fRA=5`）同型 ⇒ **直接判死，不投入仿真**。

### 6.4 真正可做信号的只有 3 族，且都很薄

| 族 | 字段 | cov | 经济含义 | 可构造的机制 |
|---|---|---|---|---|
| **EPS 实际值** | `ern7_dsu_spe`（美元，72/185） | 0.9145 | 季报报出的每股收益 | 时序自身标准化（SUE 的次优版）、同比差分、加速度 |
| | `ern7_co_spe`（原币，47/82） | 0.9005 | 同上，但币种不同 | 同上；与美国公司冗余，对跨国股才有增量 |
| | `ern7_spe`（本币，23/33） | **0.2975** | 同上 | **太稀疏，弃** |
| **股息金额** | `ern7_div_amount_usd`（30/48） | 0.504 | 每股股息（美元） | 股息变化、股息率代理（但无股价字段，ATOM 下只能做时序） |
| | `ern7_div_amount` / `ern7_div_amount_oc` | 0.504 / 0.499 | 同上，币种口径不同 | 三者为同一现象的三种计价 ⇒ 只能取一个 |
| **股息频率** | `dividend_payment_frequency_2`（3/5） | 0.5033 | 年/季/月付编码 | 分类码，价值极低 |

### 6.5 ★ 最关键的机制缺陷：earnings7 没有 surprise 维度

earnings6 至少有 `ern6_estimated_eps`（分析师或公司给的估计值），能算标准 surprise = actual − estimate。**earnings7 没有**：

- `estimated_earnings_fiscal_year` 是**财年标签**（如「这是 2024 财年的估计」），**不是 EPS 估计数值**；
- 全 40 字段中没有任何 estimated / consensus EPS 数值字段。

⇒ **无法构造标准 SUE**。只能构造「actual vs 自己的历史」的时序标准化版本：
```
SUE_proxy = (EPS_t − mean(EPS, 过去 4 季)) / std(EPS, 过去 8 季)
```
这是**次优版本**——它把「公司自己的盈利趋势」当基准，而不是「市场预期」。经济含义从「超预期」退化为「盈利加速」，信号强度通常显著更弱（PEAD 文献里 surprise 的预测力主要来自「预期之外」的部分）。

**这是选 earnings7 点 EARNINGS 塔时必须先接受的代价**：它只能出「盈利加速度」型 alpha，出不了「盈利超预期」型 alpha。

### 6.6 ★ EPS 是水平值，必须时序标准化后才能横截面使用

EPS 绝对值不可跨股票比较（股价、股数、行业量级全不同）。`group_rank(vec_avg(ern7_dsu_spe), industry)` 得到的是「谁的 EPS 绝对值大」= 高价股偏差，不是信号。

**合规的加工顺序**（两层，缺一不可）：
1. **时序层**（把水平值变成无量纲的自身偏离）：`ts_av_diff(x, W) / ts_std_dev(x, W2)` 或 `ts_zscore(x, W)` 或 `ts_delta(x, 252)`
2. **横截面层**：`group_rank(...)` / `group_zscore(...)`

⚠ 单做第 2 层是错的。探针表达式 `group_rank(ts_backfill(vec_avg(ern7_dsu_spe), 252), industry)` **是有意为之的廉价存在性探针**（只验「这字段有没有十年数据、有没有任何信号」），**不是候选骨架**，不要照抄。

### 6.7 与 earnings6 同源，但【已实测：十年跨度 PASS】

`ern6_`（已判死）与 `ern7_` 同一数据商的连续版本。earnings6 在 USA 侧实测：`ern6_actual_eps` 只有 **2018 末–2023** 数据，2014–2017 四年 `longCount=0`，直接违反「近十年都要有数据」硬约束。

**earnings7 实测（波 186 探针 `RREXEaK0`，2026-10-29）：十年跨度 PASS，与 earnings6 完全不同。**

| 年 | longCount | shortCount | TO | S | R | margin |
|---|---|---|---|---|---|---|
| 2014 | 1010 | 1045 | 4.46% | 1.32 | 3.09% | 13.85bp |
| 2015 | 1026 | 1061 | 4.07% | 2.30 | 6.21% | 30.55bp |
| 2016 | 1022 | 1054 | 4.10% | 0.35 | 0.98% | 4.80bp |
| 2017 | 1012 | 1041 | 4.10% | 1.49 | 3.59% | 17.51bp |
| 2018 | 1019 | 1048 | 4.14% | 0.70 | 1.91% | 9.26bp |
| 2019 | 1017 | 1043 | 4.05% | 0.35 | 1.01% | 4.98bp |
| 2020 | 1012 | 1040 | 4.48% | **−0.84** | −6.33% | −28.29bp |
| 2021 | 1010 | 1057 | 4.08% | **2.35** | 17.17% | 84.20bp |
| 2022 | 1032 | 1056 | 3.96% | **2.12** | 10.54% | 53.25bp |
| 2023 | 1034 | 1060 | 3.85% | **−0.21** | −0.77% | −3.98bp |

- **十年 longCount 全部 1010–1034**，无任何 `longCount=0` 年份 ⇒ 数据完整，**不判死**。
- `risk_neutralized_sharpe = +0.40`（与 S 0.88 **同号**），不像 earnings6 的 −0.21（中性化后反号）⇒ 有真实风格中性后的残差信号。
- TO 恒定 3.85%–4.48%（方差极小）⇒ 换手是结构属性，不构成风险。

### 6.8 但信号弱：两个探针的实际读数

| alpha | 骨架 | S | F | TO | 2Y | SUB | DD |
|---|---|---|---|---|---|---|---|
| `mLoOoz71` | `group_rank(ts_backfill(vec_avg(ern7_dsu_spe), 252), industry)`（裸水平，仅存在性探针） | 0.36 | 0.18 | 1.94% | 0.63 | 0.29 | **46.34%** |
| `RREXEaK0` | `group_rank(divide(ts_av_diff(F, 252), ts_std_dev(F, 504)), industry)`（SUE 骨架） | 0.88 | 0.49 | 4.12% | 1.10 | 0.78 | 13.99% |

**三条读法**：
1. 裸水平 S 0.36 / DD 46.34% 印证 6.6：**EPS 绝对值直接横截面 rank 是错的**（高价股偏差）。
2. SUE 骨架 S 0.88（裸水平的 2.4 倍）/ DD 从 46% 收窄到 14% ⇒ **时序标准化确实有效**，方向正确。
3. 但 0.88 离 LOW_SHARPE 的 1.58 还差 79%，**当前骨架不足以上闸**，需要更强的机制（见 6.9）。

### 6.9 下一步该用什么机制（不是继续调 SUE 骨架）

`RREXEaK0` 已证明「时序偏离」方向对但强度不够。按本区已验证的判据，值得试的方向：

| 方向 | 依据 | 风险 |
|---|---|---|
| **EPS 二阶矩 / 加速度** | `ts_delta(SUE, W)` 或 `ts_std_dev(SUE, W)`：盈利加速比盈利水平更有预测力 | 季度数据稀疏，二阶差分可能过噪 |
| **EPS 持续性 × 方向** | 连续 N 季同号计数 / 盈利质量的持续性 | 需 `ts_backfill` 长窗，衰减严重 |
| **股息族独立机制** | `ern7_div_amount_usd`（cov 0.504）与 EPS 正交，可作 EARNINGS 塔第 2 颗 | cov 仅 0.50，持仓可能不足 1000 |
| **横截面轴换成 sector / subindustry** | 波 180 在 earnings_sent_matrix 上实测 subindustry 版 S 1.36 > industry 1.23 | 换轴通常只 ±0.1，救不了 0.88 → 1.58 |
| **平台 decay 取 0** | 季频事件型数据的既定结论（波 179/180 实测） | 已用 decay 0，无增益空间 |

⚠ **不要做的事**：不要把 `mLoOoz71`（裸水平）当作候选去调参数——DD 46% 是结构病，不是参数问题。

### 6.10 综合评级（实测后更新）

| 维度 | 评价 |
|---|---|
| 字段数（有效） | 40 名义 / **20 独立** / **3 个可用信号族** |
| 拥挤度 | 低（7 个字段在 51–500 alpha 档，33 个 ≤50）——这是唯一优势 |
| coverage | 0.6479 平均，可用族 0.90–0.91，合格 |
| 机制完整性 | **残缺**：无 surprise 维度 ⇒ 只能做「盈利加速度」 |
| 数据跨度 | **未知，高风险**（与 earnings6 同源） |
| 十年后能否点塔 | 单集最多出 1–2 颗（EPS 族 + 股息族，且需相关性 <0.7） |

**判据：earnings7 是「低拥挤但机制残缺」的集。若探针证明它只有 2018+ 数据，立即判死；若数据完整，值得用「盈利加速度」机制开一整波（10 模板），但预期最多贡献 EARNINGS 塔 1 颗。**
