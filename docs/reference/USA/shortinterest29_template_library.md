# USA · `shortinterest29` 模板库（SHORTINTEREST 塔 · D1 · TOP3000）

> 建立于 2026-10-29。来源标注：`forum` = 平台论坛帖；`paper` = 学术文献机制（**未在线核验**，模型知识）；`自建` = 由字段语义一阶推导。
> 结构互异判据：骨架结构 / 算子几何 / 矩阶数 / 分组轴 / 非线性变换 至少一项不同。**只换窗口或换常数不计为不同模板。**

## 0 为什么从 shortinterest3 转过来（数据集选型证据）

`get_datasets(USA/D1/TOP3000/category=shortinterest)` 返回 **6 个数据集，全部 pyramidMultiplier 1.1**（都计入 SHORTINTEREST 塔）：

| dataset | 名称 | 字段 | coverage | userCount | alphaCount | valueScore |
|---|---|---|---|---|---|---|
| **shortinterest29** | Group Short Sale Data | 32 | 0.8838 | **133** | **247** | **4.0** |
| shortinterest43 | Short Sell Dataset | 32 | 0.9994 | 492 | 1527 | 3.0 |
| short_interest_pred | Short Interest Forecast Signals | 10 | 0.9987 | 204 | 446 | 3.0 |
| us_short_sale | US Equity Short Sale Volume | 4 | 1.0 | 161 | 299 | 3.0 |
| shortinterest24 | Short Sale Circuit Breaker | 1 | 0.2573 | 176 | 444 | 3.0 |
| shortinterest3（已挖） | Securities Lending Files | 31 | 1.0 | **1241** | **4566** | **2.0** |

**结论**：`shortinterest3` 是类目里**最拥挤（1241 用户 = shortinterest29 的 9.3 倍）且 valueScore 最低（2.0）** 的数据集。波 144–146 在其上 21 条仿真只得到 2 个全闸候选且互相关 0.9336（只能提交 1 颗）⇒ **继续在该集追加模板的边际产出已接近 0**。转 `shortinterest29`：valueScore 4.0（类目最高）、拥挤度低 9 倍、32 字段**全 MATRIX**（无 VECTOR 聚合歧义）。

## 1 字段结构（32 字段全 MATRIX，五族 + 一个充分统计量结构）

这 32 个字段不是 32 个独立信号，而是**同一批做空交易记录的若干汇总口径**。真正的价值在于它给出了**和（ΣX）、平方和（ΣX²）、计数（n）** 三种充分统计量 ⇒ 可以**解析地**算出均值与方差，不需要 VECTOR 也不需要近似。

| 族 | 字段 | 说明 |
|---|---|---|
| **股数量 ΣX** | `short_sale_volume` / `sum_short_sale_volume` / `actual_month_short_volume` / `arca_short_volume` / `amex_short_volume` / `shrt29_data1` / `shrt29_monthly_data1` / `shrt29_truemonth_data1` / `shrt29_monthly_truemonth_data1` | 做空股数（不同聚合口径/场所） |
| **金额 ΣP** | `sum_trade_price` / `actual_month_sum_trade_price` / `shrt29_data2` / `shrt29_monthly_data2` / `shrt29_truemonth_data2` | Σ(价×股) = 做空名义金额 |
| **计数 n** | `short_volume_count` / `trade_price_count`（**0 用户**）/ `actual_month_trade_price_count` / `actual_month_short_volume_count` / `shrt29_data3` / `shrt29_monthly_data3` / `shrt29_truemonth_data3` | 记录条数 |
| **平方和 ΣX²** | `sum_squared_short_volume` / `actual_month_sum_squared_short_volume` / `sum_squared_trade_price` / `actual_month_sum_squared_trade_price` | **解析方差的分子** |
| **交叉项 Σ(P·V)** | `sum_trade_price_times_short_volume`（**0 用户**）/ `actual_month_sum_trade_price_times_volume` | 未定用途，单位混杂，慎用 |

**零竞争字段（userCount = 0 / alphaCount = 0）**：`sum_trade_price_times_short_volume`、`trade_price_count`。这是本仓见过的极少数真正无人开采字段。

**解析二阶矩公式**（本库的核心工具）：

```
E[X]  = ΣX / n
E[X²] = ΣX² / n
Var(X) = E[X²] − E[X]² = divide(ΣX², n) − power(divide(ΣX, n), 2)
CV²    = Var(X) / E[X]² = divide(ΣX²·n, (ΣX)²) − 1
HHI    = ΣX² / (ΣX)²      ← 赫芬达尔集中度，无量纲
E_加权[X] = ΣX² / ΣX       ← 规模加权均值（大单主导的平均值）
```

## 2 模板库（14 条，结构互异）

| # | tag | 结构类别 | 表达式 | 经济机制 | 来源 | 状态 |
|---|---|---|---|---|---|---|
| **S1** | VOL_DISPERSION | 二阶矩·股数（解析方差） | `group_zscore(subtract(divide(sum_squared_short_volume, short_volume_count), power(divide(sum_short_sale_volume, short_volume_count), 2)), industry)` | 做空者**订单规模异质性**：散户小额 vs 机构大单混杂 ⇒ 信息含量差异 | 自建（复刻 shortinterest3 唯一出货机制） | 在飞 |
| **S2** | PRINCIPAL_DISPERSION | 二阶矩·金额（解析方差） | `group_zscore(subtract(divide(sum_squared_trade_price, trade_price_count), power(divide(sum_trade_price, trade_price_count), 2)), industry)` | 做空者**单笔金额异质性**：机构主导 vs 散户主导 | 自建 | 在飞 |
| **S3** | AVG_TRADE_SIZE | 水平（一阶矩） | `group_zscore(divide(sum_short_sale_volume, short_volume_count), industry)` | 平均单笔做空股数 = **机构足迹 / 冲击成本代理** | 自建 | 在飞 |
| **S4** | RECORD_COUNT_ANOM | 时序异常（相对自身 252 日） | `group_zscore(divide(trade_price_count, ts_mean(trade_price_count, 252)), industry)` | 做空**参与度异常**（零竞争字段） | 自建 | 在飞 |
| **S5** | ARCA_SHARE | 跨交易所结构 | `group_zscore(divide(arca_short_volume, short_sale_volume), industry)` | 做空**执行场所迁移**（显性 ARCA vs 其它） | 自建 | 在飞 |
| **S6** | HHI_CONCENTRATION | 集中度（无量纲二阶矩比） | `group_zscore(divide(sum_squared_short_volume, power(sum_short_sale_volume, 2)), industry)` | 做空**交易集中度**：集中砸盘 vs 分散试探。HHI ∈ (1/n, 1] | 自建 + paper（Herfindahl 集中度） | 待测 |
| **S7** | SIZE_WEIGHTED_MEAN | 规模加权一阶矩 | `group_zscore(divide(sum_squared_short_volume, sum_short_sale_volume), industry)` | **大单主导的平均单笔股数**（ΣX²/ΣX），与 S3 的等权均值形成对照 ⇒ 单笔规模分布的偏斜度 | 自建 | 待测 |
| **S8** | CV2_STABILITY | 标准化二阶矩的时序稳定性 | `group_zscore(divide(ts_std_dev(subtract(divide(sum_squared_short_volume, short_volume_count), power(divide(sum_short_sale_volume, short_volume_count), 2)), 66), ts_mean(subtract(divide(sum_squared_short_volume, short_volume_count), power(divide(sum_short_sale_volume, short_volume_count), 2)), 66)), industry)` | 订单规模异质性的**不稳定性**（二阶矩的二阶矩） | 自建 | 待测 |
| **S9** | SMOOTH_OF_S1 | 平滑杠杆 | `ts_decay_linear(<S1>, 22)` | 降噪（⚠ 须先判 S1 的信号半衰期；shortinterest3 实证：慢状态变量受益、快异常受害） | shortinterest3 波 145 实证 | 待 S1 结果 |
| **S10** | TRUEMONTH_GAP | 口径差（结构全新） | `group_zscore(divide(shrt29_monthly_truemonth_data1, shrt29_monthly_data1), industry)` | **真月 vs 报告月**做空量之差 = 报告滞后 / 数据修订方向。同单位相除 | 自建 | 待测 |
| **S11** | PRESSURE_CHANGE | 时序差分（边际） | `group_zscore(ts_delta(divide(sum_short_sale_volume, ts_mean(sum_short_sale_volume, 252)), 22), industry)` | 做空**压力边际变化**（占长期均值的比例再取差分） | 自建 | 待测 |
| **S12** | VWAP_ZS66 | 派生价格 + 长窗标准化 | `group_zscore(ts_zscore(divide(ts_mean(sum_trade_price, 66), ts_mean(short_sale_volume, 66)), 252), industry)` | 做空成交价相对自身历史（做空者择时/恐慌度）⚠ **与 PV 高度相关，prod 风险高** | 自建 | 待测（低优先） |
| **S13** | SUBIND_WINSOR_RANK | 分组轴×非线性 | `group_rank(winsorize(divide(sum_short_sale_volume, short_volume_count), std=4), subindustry)` | 抗极值 + 细分轴。**同时是对照组**：秩变换在 shortinterest3 上三次证伪，此处验证是否跨集成立 | 自建 | 待测 |
| **S14** | SECTOR_SCALE | 分组轴×尺度变换 | `group_scale(subtract(divide(sum_squared_trade_price, trade_price_count), power(divide(sum_trade_price, trade_price_count), 2)), sector)` | 金额方差在 **sector 粗轴**上归一化（与 S2 只差分组轴，作轴敏感性对照） | 自建 | 待测 |

## 3 设计纪律（沿用波 142–145 已证实的判读）

1. **符号不预设**：探针一律不加 `reverse`，让平台给原始符号再按经济含义解释。已实测：`reverse()` 的 S/F/TO/2Y/SUB/margin 与原文逐位取负，只有 drawdown 不同 ⇒ 看到负 S 先取负再判，不必为了看符号而重跑（但要拿提交用的 alpha_id 仍需跑一次翻转版）。
2. **单因素对比**：同一批内只改一个变量（字段 / 矩阶数 / 分组轴 / 非线性），不做网格扫描、不做 `add(A,B)` 混信号。
3. **二阶矩不是普适规律**：shortinterest3 上只有「费率二阶矩」出货（1.81–1.90），股数/数量族的矩全部 ≤1.07。S1/S2 是否复现，取决于「做空订单规模异质性」本身是否有溢价，不能先验假定。
4. **平滑前先问半衰期**：`ts_decay_linear` 对慢状态变量（22 日方差）增益 S+0.09/F+0.30/TO−4.5pp；对快异常（60 日偏离）**反向** S−0.87/F−0.29。且 TO 一旦跌破 12.5%，fitness 分母被 `max(TO,0.125)` 锁死 ⇒ 继续平滑边际收益为 0。
5. **单位铁律**：比值一律**同单位相除**（股数÷股数、USD÷USD、USD²÷USD²），**绝不加 ε** ⇒ `add(x, 0.0001)` 会让整条表达式 `WARNING` 失败（本仓已实证整批 8 条全灭）。分母为 0 交给平台产生 Inf/NaN，由下游 `group_zscore` 吸收。
6. **分箱/口径变体先做去重**：本集 32 字段里 `shrt29_*` 系列（data1/2/3 × monthly / truemonth / monthly_truemonth）是同一量的多口径重发布，**并列测同一骨架等于白烧仿真槽**；只有 S10 这种「口径差」才是新信息。
7. **算子可用性以平台为准**：`preflight_expressions` + `operator_audit(expressions=...)` 双通过**不等于能跑**。`ts_max` / `ts_min` 在 USA 平台根本不存在（波 145 M8 因此 ERROR）。判断某算子存在要看 `operator_audit()` 的 `ghost + missing` 补集。

## 4 待验证清单（按预期价值排序）

| 优先 | 项 | 理由 |
|---|---|---|
| 1 | S1 vs S2 vs S3 的族强度排序 | 决定「做空股数维」还是「做空金额维」承载信号；与 shortinterest3 的「费率 > 股数」结论形成跨集对照 |
| 2 | S6 HHI 集中度 | 无量纲、经济含义最强、字段零竞争；若出货则 prod 相关性天然低 |
| 3 | S7 规模加权 vs S3 等权均值之差 | 直接度量单笔规模分布的偏斜，是 S3 的增量信息而非替代 |
| 4 | S10 truemonth vs monthly 口径差 | 结构全新，与所有其它模板正交 |
| 5 | 十年跨度 | 必须 `get_alpha_yearly_stats` 逐年 longCount 验证；`coverage=0.8838` 是股票覆盖率不是时间跨度 |
| 6 | S13/S14 轴敏感性 | 秩变换/尺度变换在本集是否与 shortinterest3 同样无效 |

## 5 复现命令

```powershell
$env:PYTHONPATH='src'
$env:PYTHONIOENCODING='utf-8'
# 字段清单（32 条，全 MATRIX）
# get_datafields(region="USA", universe="TOP3000", delay=1, dataset_id="shortinterest29", filter_sharpe=false)
```

统一设置：`USA / TOP3000 / D1 / decay 0 / truncation 0.08 / neutralization SLOW / nanHandling ON / maxTrade OFF / unitHandling VERIFY`。
