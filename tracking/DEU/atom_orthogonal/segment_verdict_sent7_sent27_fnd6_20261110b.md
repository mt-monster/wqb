# DEU 段台账（续）— SENTIMENT7 / SENTIMENT27 判死 · FUNDAMENTAL6 开矿 · 数据集全集重扫

> 上一册：`segment_verdict_psvalB_news17_20261110.md`
> 本册覆盖：数据集全集重扫、两个 sentiment 数据集判死、fundamental6 开波、PV 面板（analyst_earnings_ibes）开波

---

## 一、★★★ 数据集全集重扫：推翻「仅剩 7 个未测数据集」

### 1.1 事实修正

先前台账判断「DEU 单数据集出货能力枯竭，仅剩 sentiment7 / sentiment27 / other47 / other250 / insiders1 / other545 / stock_cluster_dl 未测」——**错误**。

用 172 个数据集的全表重新解析（`deu_datasets_all.txt` → `deu_ds_cov.csv`，脚本见附录 A）得到的真实分布：

| 项 | 数量 |
|---|---:|
| DEU 数据集总数 | **172** |
| coverage > 0 | **68** |
| coverage = 0 | 104 |
| **cov ≥ 0.33 且从未开波** | **20+** |

按 category：model 45 / other 41 / analyst 18 / news 17 / pv 16 / fundamental 12 / institutions 5 / risk 5 / sentiment 3 / earnings 2 / insiders 2 / socialmedia 2 / imbalance 1 / shortinterest 1 / option 1 / macro 1。

> **教训**：`get_datasets` 分 category 查询会漏，必须一次拉全表再本地解析。
> 本册之后所有选集都以 `deu_ds_cov.csv` 为准，不再依赖记忆里的「已判死清单」。

### 1.2 未开波的高覆盖数据集（按 cov 降序，★=优先级）

| 数据集 | category | cov | 字段数 | alphaCount | 备注 |
|---|---|---:|---:|---:|---|
| risk88 | risk | 1.0 | 1 | 64 | 单字段 |
| **pv29** | pv | 1.0 | 50 | **66** | ★ 全平台仅 66 个 alpha，严重欠挖 |
| **institutions6** | institutions | 1.0 | 11 | 270 | ★ 记忆里有冠军骨架（披露计数） |
| **analyst_earnings_ibes** | model | 0.9978 | 42 | 279 | ★★ 实为完整价量面板（见第五节） |
| model264 | model | 0.9973 | 380 | 203 | 已判死 |
| pattern_scores | pv | 0.9888 | **504** | 266 | ★ 图表形态，大表 |
| news104 | news | 0.963 | 11 | 100 | 已判死 |
| other455 | other | 0.9535 | 1500 | 219 | GROUP only |
| model53 | model | 0.905 | 22 | 9 | 已判死 |
| sentiment27 | sentiment | 0.9038 | 18 | 324 | 本册判死 |
| **fund_holdings_panel** | institutions | 0.9019 | 18 | 102 | ★ 基金持仓 |
| **news18** | news | 0.8046 | 70 | 137 | ★ 未测 |
| **news50** | news | 0.7644 | 37 | 42 | ★ 未测 |
| **pv30** | pv | 0.7273 | 285 | 287 | ★ 未测 |
| **fundamental22** | fundamental | 0.69 | **1** | 40 | 单字段，价值有限 |
| **analyst93** | analyst | 0.6373 | 100 | 193 | ★ 未测 |
| **analyst47** | analyst | 0.6234 | 5 | 112 | ★ 未测 |
| **fundamental6** | fundamental | 0.4923 | 196 | 1077 | ★★ 本册开波，已出 S1.15 |
| **analyst9** | analyst | 0.5825 | 51 | 106 | ★ 未测 |
| other47 | other | 0.577 | 18 | 62 | 未测 |
| **model30** | model | 0.5694 | 14 | 179 | 未测 |
| other250 | other | 0.6126 | 12 | 2 | 未测 |
| **insiders1** | insiders | 0.5343 | 8 (VECTOR) | — | 未测 |
| other545 | other | 0.5269 | 4 | — | 未测 |
| stock_cluster_dl | other | 0.4526 | 5 | — | 未测 |
| model144 / pv109 / model307 / model313 / model262 / model140 / institutions4 / analyst83 | — | 0.34–0.49 | — | — | 未测 |

**结论**：仍有 **20+ 个数据集可开波**。先前「枯竭」判断作废。

---

## 二、★ SENTIMENT7 判死（批次 `Vl0pSdjo4F9bmX85lISwP`，10/10 COMPLETE，10/10 REJECT）

设置：DEU / TOP500 / D1 / SUBINDUSTRY / decay 4 / **trunc 0.02**（复现 mLox6Mg2 的 provenance）。
数据集：sentiment7 仅 3 字段（`snt7_all_languages_views` 维基百科浏览量 cov 0.7539 / `snt7_views` cov 0.7357 / `snt7_timestamp`）。

| # | 模板 | alpha | S | F | 2Y | sub_u | TO | margin |
|---|---|---|---:|---:|---:|---:|---:|---:|
| S7-1 | `ts_quantile(ts_ir(ts_mean(max(x, delay(x,5)),5),22),252)` | LLM3eAEa | **0.77** | 0.40 | **2.16** | 0.56 | 0.1435 | 0.000534 |
| S7-2 | `group_rank(ts_ir(ts_mean(x,5),66), sector)` | O0AgeERp | 0.75 | 0.41 | 1.32 | 0.58 | 0.0645 | 0.001175 |
| S7-4 | 双字段 `ts_ir` rank add | JjerlZo2 | 0.74 | 0.41 | 0.96 | 0.69 | 0.0598 | 0.001310 |
| S7-5 | `ts_av_diff(ts_ir(...),66)` | wpQW6M2p | 0.68 | 0.35 | 1.34 | 0.31 | 0.0771 | 0.000861 |
| S7-7 | bucket 中性化 | KPJZej5g | 0.67 | 0.35 | 0.30 | 0.73 | 0.0650 | 0.001072 |
| S7-3 | `ts_zscore(vec_avg(snt7_views),5)` 252 | KPJZejvg | 0.56 | 0.19 | −0.16 | 0.08 | **0.2437** | 0.000233 |
| S7-9 | `ts_target_tvr_decay` 0.03 | akKGJqzv | 0.42 | 0.17 | 0.29 | 0.47 | 0.0418 | 0.001031 |
| S7-8 | 双视界 `multiply` | MPYVwoen | 0.39 | 0.16 | 0.67 | 0.50 | 0.0426 | 0.001025 |
| S7-10 | 数据集内 `vector_neut` | QPv6eLzG | 0.28 | 0.09 | 1.14 | 0.27 | 0.1513 | 0.000194 |
| S7-6 | `divide(rank(a), add(rank(b),1))` | LLM3eAmn | −0.23 | −0.08 | 0.70 | −0.41 | 0.0368 | −0.000864 |

**天花板 S = 0.77**（2Y 可达 2.16，但 S 差 0.81）。sentiment7 单数据集判死。

### ★★★ 但本波揭示了一个更重要的机理

`LLM3eAEa`（S7-1）就是已交付 `mLox6Mg2` 的**主腿原样**，只去掉了 `vector_neut(..., snl27_relpopularity08)`：
- 主腿单独：S **0.77**
- `vector_neut(主腿, snl27_relpopularity08)`：S **2.05**

而 `snl27_relpopularity08` 单独（SENTIMENT27 波）S 上限 **0.64**。

> **⇒ mLox6Mg2 的 S 2.05 几乎全部来自「两条高度相关的关注度指标之差」这个残差方向。**
> 两条腿单独都弱，残差却极强 ⇒ 这是一类**新的可复用机制**：
> **当两个指标高度相关但回答问题的角度不同（一个是全语言维基浏览、一个是 Tranco 域名排名），它们的正交残差可以是全新且强得多的信号。**
> 这类信号**必须保持双数据集**，不可能压缩成严格单数据集 ATOM。

---

## 三、★ SENTIMENT27 判死（批次 `32qm4XaVi5ejcIY1hsubs6Lt`，10/10 COMPLETE，10/10 REJECT）

数据集 sentiment27 = **Tranco 网站域名排名 / 数字足迹**，18 字段（15 个可用 VECTOR 数值 + 3 个 SYMBOL 不可用），cov 0.9022–0.9118。

5 个信息维度：流行度水平（`relpopularity08/1`、`avgranking`、`topranking`）／高阶矩（`skewness`、`kurtosis`）／分位结构（`top50pct*`、`top75pct*`）／域数量（`totaldomains`、`totalcountrydomains`）／排名秩（`snt27_rank`）。

| # | 模板 / 经济机制 | alpha | S | F | 2Y | sub_u | TO |
|---|---|---|---:|---:|---:|---:|---:|
| S27-9 | 头尾落差 `top50pctavg/avgranking`（分位比） | **A1VE6GLe** | **0.64** | 0.36 | 1.60 | **0.95** | 0.0324 |
| S27-7 | 数字足迹广度 `totaldomains` 66 | e75EA31g | 0.41 | 0.19 | **1.71** | 0.32 | **0.0149** |
| S27-4 | 关注度信息比率 `ts_ir` | zq3eaNdd | 0.10 | 0.02 | 0.64 | −0.07 | 0.0533 |
| S27-2 | 504 日时序分位 | e75EA3ag | −0.03 | −0.00 | −1.16 | −0.14 | 0.0625 |
| S27-3 | 关注度变化 `ts_delta` 66 | npvr0Na8 | −0.28 | −0.09 | 1.07 | 0.01 | 0.0615 |
| S27-8 | 国际化域占比 | GrW9VGQG | −0.39 | −0.17 | −0.56 | −0.22 | 0.0183 |
| S27-6 | 峰度（四阶矩） | 3qoJdpGQ | −0.42 | −0.18 | −0.24 | −0.04 | 0.0422 |
| S27-10 | 双视界变化乘积 | QPv6eGWw | −0.52 | −0.22 | 0.72 | −0.30 | 0.0559 |
| S27-1 | 关注度水平 **反向** | 1YN0vpNM | −0.60 | −0.35 | **−1.74** | −0.49 | 0.0176 |
| S27-5 | 偏度（三阶矩）反向 | E56x3GQL | −0.61 | −0.31 | −0.36 | −1.07 | 0.0413 |

**天花板 S = 0.64**。sentiment27 单数据集判死。

### ★ 符号修正（重要，别记反）

`1YN0vpNM` = `-group_rank(ts_mean(vec_avg(snl27_relpopularity08),22), sector)` → **S −0.60 / 2Y −1.74**。
⇒ **正向**（不加负号）约为 **S +0.60 / 2Y +1.74**。

> **DEU 的网络关注度是「品牌价值/无形资产」逻辑（正向），不是 Barber-Odean 的「注意力过度定价」逻辑（反向）。**
> 星号：这正是「先查论文方向先验、再让实测纠正」的典型案例——原始论文（USA）方向在 DEU 相反。

另：`e75EA31g`（`totaldomains` 66 日）给出 **TO 0.0149 / 2Y 1.71**，是全 DEU 见到的最低换手 + 最高 2Y 组合之一；`A1VE6GLe` 给出 **sub_u 0.95**（极健康的子宇宙项）。这两个是「若未来能组腿」的优质素材。

---

## 四、★★ FUNDAMENTAL6 开矿（Wave 1，批次 `2Wns5e4px4rbaiLUuVwP63G`，10/10 COMPLETE）

### 4.1 字段画像

`fundamental6` = Company Fundamental Data for Equity（Compustat 式点对点基本面），**196 字段全是 MATRIX**（无需 `vec_*`），cov 0.15–0.66，无 VECTOR、无 SYMBOL。

核心科目覆盖率（用于选集）：

| 科目 | 字段 | cov |
|---|---|---:|
| 总资产 | `fnd6_cptnewq_atq` | 0.6557 |
| 股东权益（季） | `fnd6_newq_seqq` | 0.6595 |
| 负债+权益 | `fnd6_newq_lseq` | 0.6561 |
| 税前利润（年） | `fnd6_piy` | 0.6613 |
| 净利润（年） | `fnd6_iby` | 0.6600 |
| 营业收入（年） | `fnd6_revty` | 0.6587 |
| 现金及短投 | `fnd6_newq_cheq` | 0.6531 |
| 股东权益-母公司 | `fnd6_newa2_seq` | 0.6525 |
| 营业收入（半年） | `fnd6_revtsa` | 0.6513 |
| 毛利（年） | `fnd6_gpy` | 0.5515 |
| 经营现金流（年） | `fnd6_oancfy` | 0.5419 |
| 资本开支 | `fnd6_capxy` | 0.5130 |
| 总负债 | `fnd6_cptnewq_ltq` | 0.5395 |
| R&D（年） | `fnd6_newa2_xrd` | 0.3639 |
| 融资现金流 | `fnd6_fincfy` | 0.5390 |

**注意**：`fnd6_adesinda_curcd` / `fnd6_idesindq_curcd` cov=1.0 但内容是 **ISO 货币代码**（分类量），不可作信号，只可当分组轴。

### 4.2 十个学术基本面异象（模板来源：全部有论文出处）

| # | 经济机制（论文） | 表达式骨架 | 算子数 |
|---|---|---|---:|
| F6-1 | 毛利溢价 Novy-Marx 2013 | `group_rank(divide(gpy, atq), sector)` | 2 |
| F6-2 | 投资异象 Cooper-Gulen-Schill 2008 | `-group_rank(divide(ts_delta(atq,252), ts_delay(atq,252)), sector)` | 4 |
| F6-3 | 应计 Sloan 1996 | `-group_rank(divide(subtract(iby, oancfy), atq), sector)` | 3 |
| F6-4 | 净经营资产 Hirshleifer-Hou-Teoh 2004 | `-group_rank(divide(subtract(atq, cheq), revty), sector)` | 4 |
| F6-5 | **经营现金利润率（现金盈利）** | `group_rank(divide(oancfy, revty), sector)` | 2 |
| F6-6 | 研发强度（无形资本） | `group_rank(divide(newa2_xrd, newa2_sale), sector)` | 3 |
| F6-7 | 杠杆率反向 | `-group_rank(divide(cptnewq_ltq, atq), sector)` | 3 |
| F6-8 | 毛利率同比变动（质量动量） | `group_rank(ts_delta(divide(gpy, revty), 252), sector)` | 4 |
| F6-9 | 资本开支强度反向（过度投资） | `-group_rank(divide(capxy, atq), sector)` | 3 |
| F6-10 | 规模桶内资产周转率（自定义分组轴） | `group_neutralize(divide(revty, atq), bucket(rank(atq), range="0,1,0.1"))` | 4 |

### 4.3 Wave 1 结果

| # | alpha | S | F | 2Y | sub_u | TO | margin | 判定 |
|---|---|---:|---:|---:|---:|---:|---:|---|
| **F6-5 现金利润率** | **gJeLvb8O** | **1.15** | **0.98** | 0.43 | 0.79 | **0.0265** | **0.006856** | **REVIEW** ★本波唯一 |
| F6-1 毛利溢价 | E56x3peG | 0.59 | 0.36 | 0.44 | 0.51 | 0.0328 | 0.002775 | REJECT |
| F6-3 应计 | omEZ2LgJ | 0.49 | 0.27 | 0.21 | 0.42 | 0.0310 | 0.002395 | REJECT |
| F6-4 NOA | 1YN0vXzM | 0.34 | 0.15 | −0.72 | 0.27 | 0.0311 | 0.001467 | REJECT |
| F6-8 毛利率变动 | A1VE6NGe | 0.31 | 0.14 | −0.20 | 0.70 | 0.0452 | 0.001157 | REJECT |
| F6-10 桶内周转 | 3qoJdXlQ | 0.23 | 0.09 | 0.21 | 0.19 | 0.0434 | 0.000818 | REJECT |
| F6-2 资产增长 | 9qxkoj7x | 0.13 | 0.04 | **1.59** | −0.09 | 0.0371 | 0.000578 | REJECT（2Y 强 S 弱） |
| F6-6 研发强度 | e75EAb3g | 0.03 | 0.00 | 0.69 | 0.45 | 0.0182 | 0.000355 | REJECT |
| F6-7 杠杆率 | npvr0dN8 | 0.03 | 0.00 | −0.64 | 0.20 | 0.0187 | 0.000186 | REJECT |
| F6-9 capex 强度 | O0AgeNGd | −0.39 | −0.19 | −0.04 | −0.10 | 0.0305 | −0.002023 | REJECT（方向反了） |

### 4.4 ★★★ 核心结论：**现金利润率是 fundamental6 的唯一强维度**

`gJeLvb8O = group_rank(divide(fnd6_oancfy, fnd6_revty), sector)`

- **S 1.15 / F 0.98 / margin 0.006856 / TO 0.0265 / drawdown 0.1235 / sub_u 0.79**，只用 2 个算子。
- **margin 0.006856 是全 DEU 遍历下来最高的一档**（已交付的 QPvzNNGG 是 0.002041）。
- 短板：**2Y 只有 0.43**（差 1.15）。

对比同批：所有其他基本面科目（毛利、应计、NOA、研发、杠杆、capex、周转）S 全部 ≤0.59。
⇒ **在 fundamental6 里，「现金口径相对收入/资产的比率」是唯一能把 S 推到 1 以上的构造；表内其他科目都不行。**

这与论坛帖《基于低换手市场因子拥挤与资产负债表效应的因子挖掘研究报告》（LC73254, 17 赞）的说法一致：「**基本面6 留存 54% 显著领先**……基本面线聚焦稳健资产负债表综合因子」。

**下一步（Wave 2 已派发）**：围绕现金流利润率族做 10 个结构互异变体，目标把 S 从 1.15 推到 1.58 且保住/抬高 2Y。

---

## 五、★★ PV 面板新发现：`analyst_earnings_ibes` 名不副实

数据集 ID 叫 `analyst_earnings_ibes`，category 标 `model`，cov **0.9978**，42 字段——但**实际内容是一整套价量面板**，没有任何分析师预期字段：

| 家族 | 字段（×dlr1/dlr2/dlr3 三变体） |
|---|---|
| 价格 | `opening_price_*` / `highest_price_*` / `lowest_price_*` / `closing_price_*` |
| 均价 | `volume_weighted_avg_price_*`（cov 0.9996） |
| 成交量 | `trading_volume_*` |
| 市值 | `market_capitalization_*` |
| 股本 | `shares_outstanding_*` |
| **多视界收益** | `one_day_total_return_*` / `five_day_*` / `twenty_day_*` / `sixty_day_*` / `one_twenty_day_*` / `two_fifty_day_*` |

> `dlr2` = Europe region 口径（覆盖最好、用户最多）；`dlr1` = Americas；`dlr3` = 精简 PIT。
> **DEU 必须用 `_dlr2`**（`_dlr1` 描述里明确写「Americas-region equities」）。

**价值判断**：cov 近 1.0 + 多视界收益已预计算 + 每字段 alphaCount 仅 1–96（严重欠挖）⇒ DEU 目前**最未被开采**的富矿。

### PV 波 10 个模板（已派发 `36nVszarj5bA9yXISfuqNor`）

| # | 异象（论文） | 表达式 |
|---|---|---|
| P1 | 短期反转 Jegadeesh 1990 | `-group_rank(twenty_day_total_return_dlr2, sector)` |
| P2 | 低波动 Ang-Hodrick-Xing-Zhang 2006 | `-group_rank(ts_std_dev(one_day_total_return_dlr2, 66), sector)` |
| P3 | 12-1 动量 Jegadeesh-Titman 1993 | `group_rank(subtract(two_fifty_day_total_return_dlr2, twenty_day_total_return_dlr2), sector)` |
| P4 | **隔夜收益溢价** Lou-Polk-Skouras 2019 | `group_rank(ts_mean(divide(opening_price_dlr2, ts_delay(closing_price_dlr2, 1)), 22), sector)` |
| P5 | Amihud 非流动性 2002 | `group_rank(ts_mean(divide(rank(abs(one_day_total_return_dlr2)), add(rank(trading_volume_dlr2), 1)), 22), sector)` |
| P6 | 异常成交量（关注度冲击） | `-group_rank(ts_mean(divide(trading_volume_dlr2, ts_mean(trading_volume_dlr2, 252)), 22), sector)` |
| P7 | **52 周高点接近度** George-Hwang 2004 | `group_rank(ts_rank(closing_price_dlr2, 252), sector)` |
| P8 | VWAP-收盘偏离（日内买卖压） | `-group_rank(divide(volume_weighted_avg_price_dlr2, closing_price_dlr2), sector)` |
| P9 | 净股票发行 Daniel-Titman 2006 | `-group_rank(divide(ts_delta(shares_outstanding_dlr2, 252), ts_delay(shares_outstanding_dlr2, 252)), sector)` |
| P10 | 日内振幅（高低价差波动率） | `-group_rank(ts_mean(divide(subtract(highest_price_dlr2, lowest_price_dlr2), closing_price_dlr2), 22), sector)` |

> P7 用 `ts_rank(closing, 252)` 替代被禁的 `ts_max`（DEU 静态门禁 `INACCESSIBLE_OP`），语义等价于「当前价在一年区间中的位置」＝52 周高点接近度。

---

## 六、算子可用性实测清单（103 个）

从算子目录产物解析确认可用（`0bc1b5a00d2a604d49bcaf26-*.txt`）：

```
abs add and bucket combo_a days_from_last_change densify divide equal generate_stats greater
greater_equal group_backfill group_cartesian_product group_count group_mean group_neutralize
group_rank group_scale group_std_dev group_sum group_zscore hump if_else in inverse is_nan
kth_element last_diff_value less less_equal log max min multiply normalize not not_equal or
pasteurize power quantile rank reduce_avg reduce_choose reduce_count reduce_ir reduce_kurtosis
reduce_max reduce_min reduce_norm reduce_percentage reduce_powersum reduce_range reduce_skewness
reduce_stddev reduce_sum reverse scale self_corr sign signed_power sqrt subtract tail trade_when
ts_arg_max ts_arg_min ts_av_diff ts_backfill ts_corr ts_count_nans ts_covariance ts_decay_linear
ts_delay ts_delta ts_ir ts_kurtosis ts_max_diff ts_mean ts_product ts_quantile ts_rank
ts_regression ts_returns ts_scale ts_std_dev ts_step ts_sum ts_target_tvr_decay ts_target_tvr_hump
ts_zscore universe_size vec_avg vec_count vec_max vec_min vec_range vec_stddev vec_sum vector_neut
winsorize zscore
```

**确认不存在**：`ts_max`（只有 `ts_max_diff` / `ts_arg_max` / `reduce_max` / `max`）、`ts_skewness`（只有 `ts_kurtosis` / `reduce_skewness`）、`ts_min`、`ts_median`、`ts_entropy`、`ts_percentage`、`ts_decay_exp_window`。

---

## 七、当前交付状态

### 严格单数据集 ATOM = 3 / 10

| # | alpha | 数据集 | S | F | 2Y | TO | self | prod |
|---|---|---|---|---:|---:|---:|---:|---:|---:|
| 1 | QPvzNNGG | predictive_starmine | 1.70 | 1.30 | 2.18 | 0.155 | 0.678 | 0.6777 |
| 2 | LLMzYrZe | predictive_starmine | 1.61 | 1.16 | 1.69 | 0.153 | 0.670 | 0.6697 |
| 3 | MPY9VNY9 | shortinterest3 | 1.59 | 1.26 | 2.36 | 0.036 | 0.270 | 0.5986 |

双数据集件 2 颗（mLox6Mg2 S2.05 / E56pROb9 S1.79），不计入严格 ATOM。

### 新晋候选（待 Wave 2 提分）

| alpha | 数据集 | S | F | 2Y | margin | 缺口 |
|---|---|---:|---:|---:|---:|---|
| gJeLvb8O | fundamental6 | 1.15 | 0.98 | 0.43 | 0.006856 | S −0.43 / 2Y −1.15 |

### 在飞

- `QqFcgcDE4zxctXcoDZxd9m` — FUNDAMENTAL6 Wave 2（现金利润率族 10 变体）
- `36nVszarj5bA9yXISfuqNor` — PV 面板 Wave 1（10 个价量异象）

---

## 附录 A：DEU 数据集全表还原与解析脚本

```powershell
$ErrorActionPreference='Stop'
$src='C:\Users\MENGTAO\.minimax\v2\sessions\2026\11\06\20-32-59-762-session_bXZzXzE0MGU5YzRjYzA5YzQxM2I4NTQ5OTMxYjAyOTM4NDA3\reports\tool-outputs\dd1bac71442e2256e371f15d-e701cdf1a20584e806a6155358a58bb5ce44906fe8453e42dfa92ed379e15964.readable.v1.jsonl'
$sb=New-Object System.Text.StringBuilder
Get-Content -LiteralPath $src -Encoding UTF8 | Select-Object -Skip 1 | ForEach-Object { $o=$_|ConvertFrom-Json; if($o.text){[void]$sb.Append($o.text)} }
Set-Content -LiteralPath 'tracking\DEU\atom_orthogonal\deu_datasets_all.txt' -Value $sb.ToString() -Encoding UTF8

$t=Get-Content -LiteralPath 'tracking\DEU\atom_orthogonal\deu_datasets_all.txt' -Raw -Encoding UTF8
$ms=[regex]::Matches($t,'\{[^{}]*?"id"\s*:\s*"([A-Za-z0-9_]+)"[^{}]*?\}')
$rows=@()
foreach($m in $ms){
  $b=$m.Value; if($b -notmatch '"coverage"'){ continue }
  $rows += [pscustomobject]@{
    id=$m.Groups[1].Value
    cat=$(if($b -match '"category"\s*:\s*\{\s*"id"\s*:\s*"([a-zA-Z_]+)"'){$matches[1]}else{'?'})
    cov=$(if($b -match '"coverage"\s*:\s*([0-9.eE-]+)'){[double]$matches[1]}else{-1})
    fc =$(if($b -match '"fieldCount"\s*:\s*(\d+)'){[int]$matches[1]}else{-1})
    ac =$(if($b -match '"alphaCount"\s*:\s*(\d+)'){[int]$matches[1]}else{-1})
    uc =$(if($b -match '"userCount"\s*:\s*(\d+)'){[int]$matches[1]}else{-1})
  }
}
$rows | Where-Object {$_.cov -gt 0} | Sort-Object cov -Descending |
  Export-Csv -LiteralPath 'tracking\DEU\atom_orthogonal\deu_ds_cov.csv' -NoTypeInformation -Encoding UTF8
```

> 陷阱：该产物尾部带 `[MCP structured content]` 标记，整份 `ConvertFrom-Json` 会失败；只逐行拼 `.text`。
