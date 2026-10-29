# 波 183 —— earnings6 两条探针：USA 侧数据只有 2018+，整集判死

> 日期：2026-10-30 · 区域 USA / TOP3000 / D1 / INDUSTRY / decay 4 / trunc 0.08 / nanHandling ON
> multisim `3t3XTl7ER4xebbWlqMiPy71`，2 条全 COMPLETE、0 错误、耗时约 2 分钟
> 台账：`upsert_wave_result(183, FAIL, n_pass=0, n_near=0)`

---

## 1. 为什么只跑 2 条

`earnings6` 是 EARNINGS 塔第 2/3 颗的候选之一。但开工前已有两条强烈警告：

1. **平台论坛 `42570430097175`（JC78366，「EUR/TOP2500 字段避坑系列（一）earnings6」，2026-08-08，1 赞 2 评）**逐字段列出了 earnings6 全部 34 个字段的禁用原因，其中：
   - `eps_change_absolute_value` / `eps_change_percentage_value` = **all NaN data**
   - `ern6_actual_eps` / `ern6_estimated_eps` / `ern6_actual_fiscal_year` / `preliminary_eps_range_*` = **data since 2019 too short**
   - `ern6_confnumber` = phone number、`ern6_confpasscode` = passcode、`ern6_eps6stock_symbol` = symbol
   - `ern6_transcript_fiscal_year` / `ern6_wqreceivetimestamp` = data NaN
   - 评论 HS65681 补充判别技巧：可直接查字段 `dateCoverage` 与 `coverage`，**coverage = 0 可直接排除**；应把「all NaN data」（彻底不能用）与「data too short」（未来可能补全）分开标注
2. **本会话的历史教训**：波 176 的 `earnings_chart_dl` 直接开 10 条模板波，结果 7/7 全灭；波 177 的 `mfm_model_output` 开 10 条出 1 颗。**探针成本 2 条 vs 整波 10 条，差 5 倍。**

所以本波先用 2 条最廉价探针在 **USA 侧**复核论坛的 EUR 结论 —— 论坛说的是 EUR/TOP2500，USA 是否一致必须实测。

### 探针选择逻辑

| 探针 | 字段 | 选它的理由 |
|---|---|---|
| `npv0Pg9E` | `ern6_actual_eps`（cov 0.9278 / 99 users / 157 alphas） | 论坛说「data since 2019 too short」，但它是**拥挤度最高、最可能有信号**的字段（157 alphas）⇒ 若它连十年数据都没有，整集必死 |
| `A1V6vwWd` | `eps_change_percentage_value`（cov — / 2 users / 3 alphas） | 论坛说「all NaN data」⇒ 用最低成本的裸水平验证是否真的空 |

两条都用最标准的水平骨架（不做任何加工），把变量降到最少：

```
npv0Pg9E  group_rank(ts_backfill(vec_avg(ern6_actual_eps), 252), industry)
A1V6vwWd  group_rank(ts_backfill(vec_avg(eps_change_percentage_value), 252), industry)
```

`vec_avg` 是必需的手包（earnings6 全 52 字段都是 VECTOR，平台要求先经 `vec_*` 聚合才能被常规算子使用）。`preflight_expressions` 返回 `any_changed: false`，确认手包正确。

---

## 2. 结果

| alpha | 表达式 | S | F | TO | 2Y | SUB | invest_S | risk_neut_S | longCount | shortCount | fRA |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `npv0Pg9E` | `ern6_actual_eps` 水平 | 0.45 | 0.28 | 2.26% | 0.79 | 0.24 | 0.48 | **−0.21** | 1493 | 1597 | 3 |
| `A1V6vwWd` | `eps_change_percentage_value` 水平 | **0.00** | — | **0.00%** | — | — | — | — | **0** | **0** | **5** |

---

## 3. ★ 决定性证据：`npv0Pg9E` 的逐年年表

`get_alpha_yearly_stats(npv0Pg9E)`：

| 年 | longCount | shortCount | pnl | S | R | margin | F |
|---|---|---|---|---|---|---|---|
| 2014 | **0** | **0** | **0** | 0.00 | 0.00% | 0 | 0 |
| 2015 | **0** | **0** | **0** | 0.00 | 0.00% | 0 | 0 |
| 2016 | **0** | **0** | **0** | 0.00 | 0.00% | 0 | 0 |
| 2017 | **0** | **0** | **0** | 0.00 | 0.00% | 0 | 0 |
| 2018 | 1 | 59 | −48,482 | −0.20 | −0.48% | −0.78bp | — |
| 2019 | 1367 | 1658 | 220,755 | 0.50 | 2.19% | 1.27bp | — |
| 2020 | 1517 | 1550 | **−2,496,146** | **−3.57** | **−27.01%** | −27.38bp | — |
| 2021 | 1528 | 1611 | 2,659,139 | 2.09 | 26.38% | 30.12bp | — |
| 2022 | 1556 | 1593 | 2,237,777 | 1.40 | 22.29% | 29.90bp | — |
| 2023 | 1565 | 1582 | −231,908 | −0.24 | −2.32% | −3.14bp | — |

> **2014–2017 四年 `longCount = 0` 且 `pnl = 0`，2018 只有 1 只做多 / 59 只做空（半年数据）。**

十年回测窗口（2014-01-01 ~ 2023-12-31）实际只覆盖 **2018 年末–2023 = 约 5 年**。

**这直接违反「数据集必须近十年都有数据」的硬约束 ⇒ `earnings6` 整集判死。**

对照波 182 的 `ZYQZAEW8`（risk65）：逐年 `longCount` 1547–1587，2014–2023 全 10 年都有数据 —— 这就是合格与不合格的分界线。

---

## 4. 四条结论

### 4.1 论坛的 EUR 警告在 USA 侧被完整复现

论坛帖说 `ern6_actual_eps`「data since 2019 too short」（EUR/TOP2500）。USA/TOP3000 实测起始 **2018 年末**，比 EUR 还早一点，但同样远不到十年。

> **该帖的字段级避坑结论可直接用于 USA。** 这是本会话第二次验证「论坛的区域性警告在换区后大概率仍然成立」（第一次是 `31365517513495` 的 DEU 0.4743 系数，虽然系数本身不可跨区套用，但「提前查论坛能拿到年代跨度」这条方法论成立）。

### 4.2 `eps_change_percentage_value` 是彻底的空字段

`A1V6vwWd`：S 0.00 / TO 0.00% / longCount 0 / shortCount 0 / pnl 0 / **fRA = 5**，且 `checks.pass` 里出现 `LOW_FITNESS:ERROR` / `LOW_SUB_UNIVERSE_SHARPE:ERROR` / `CLUSTER_TEST:ERROR`。

与论坛「all NaN data」一致。**这是本会话第三个「输入全 NaN」的实例**（另两个：波 177 `broad_market_factor_score_2` 整列为 0、波 182 `E563RGgm` 两字段相减全空），三者指纹完全一致：

```
longCount = 0  +  checks.pass 含 ":ERROR"  +  fRA = 5
```

> **判据固化为铁律**：看到这三条同时出现，直接判字段/表达式不可用，不再调骨架。

### 4.3 即使数据够也不能用：信号是两年行情而非 alpha

`npv0Pg9E` 的 `risk_neutralized_sharpe = −0.21` —— **风险中性化后信号反号**，说明原始 0.45 的 Sharpe 来自风险暴露而非独立 alpha。

年度 pnl 也剧烈翻转：

```
2020  −2,496,146  (S −3.57, R −27.01%)
2021  +2,659,139  (S  2.09, R +26.38%)
2022  +2,237,777  (S  1.40, R +22.29%)
2023    −231,908  (S −0.24, R  −2.32%)
```

连续两年 ±26–27% 的收益翻转，是典型的「2021 复苏行情 + 2022 加息行情」叠加，不是稳定的截面预测力。

> 这两条独立证据（risk_neut_S 反号 + 年度 pnl 翻转）意味着：**即使 earnings6 后来补齐了十年数据，`ern6_actual_eps` 也不该作为水平信号使用。**

### 4.4 ★ 方法论：新数据集必须先探针再整波

| 数据集 | 做法 | 结果 |
|---|---|---|
| `earnings_chart_dl`（波 176） | 直接 10 条模板 | 7/7 全灭 → 白烧 7 槽 |
| `mfm_model_output`（波 177） | 直接 10 条模板 | 1 颗出货 → 可接受 |
| `earnings6`（波 183） | **先 2 条探针** | 2 分钟判定整集死 → **省下 8 槽** |

> **探针优先级最高的三个问题**（按杀伤力排序）：
> 1. **十年跨度**（`get_alpha_yearly_stats` 看 `longCount = 0` 的年份）—— 覆盖不了十年直接死，无需再试任何骨架；
> 2. **字段是否全空**（`longCount = 0` + `:ERROR` + `fRA = 5`）—— 死字段直接换；
> 3. **信号是否只是风险暴露**（`risk_neutralized_sharpe` 是否与 S 同号同量级）—— 反号直接死。
>
> 这三条只要任意一条不过，整集不值得开整波。1 次廉价 sim + 1 次零配额查询（yearly stats）就能拦掉后续全部投入。

---

## 5. EARNINGS 塔的路径收窄

本波之后，EARNINGS 塔第 2/3 颗的候选面已经收缩到两条：

| 数据集 | 字段数 | cov | alphas | 状态 |
|---|---|---|---|---|
| `earnings_sent_matrix` | 7 | 0.70 | 1,431 | **只能交 1 颗**（波 180 相关矩阵 0.7576–0.9947，`max_mutually_below_subset` size = 1）→ 已定 `ZYQZbnYx` |
| `earnings6` | 52 | 0.9853 | 4,953 | **本波判死**（数据仅 2018+，唯一有数据字段 risk_neut_S −0.21） |
| `earnings_chart_dl` | 100 | 0.991 | 1,006 | 判死（波 176：换手 75–91%，平滑即杀信号） |
| `earnings27` | 14 | 0.2734 | 1,529 | 判死（cov 太低） |
| **`earnings7`** | 40 | 0.6479 | 1,317 | **下一个候选** — 必须先跑同样的 2 条探针验十年跨度 |
| `earnings4` | 375 | 0.9692 | **13,771** | 极饱和，最后手段 |

> **EARNINGS 塔的经验教训**：这个塔的数据集普遍是「季频事件型」，历史跨度短是通病。`earnings_sent_matrix`（cov 0.70 / 1,431 alphas）能出 2 颗全闸候选是例外，不是常态。开任何 EARNINGS 新数据集前，**十年跨度探针是强制前置**。

---

## 6. 待办

- [ ] `earnings7` 两条探针：`rank(vec_avg(<cov 最高字段>))` + `get_alpha_yearly_stats`，确认 2014–2023 每年 `longCount > 0`
- [ ] 若 `earnings7` 跨度合格，再开 10 模板整波（模板库需 ≥10 个结构互异，且必须先查论坛 + 论文）
- [ ] 若 `earnings7` 也判死，EARNINGS 塔第 2/3 颗只能押 `earnings4`（375 字段 / 13,771 alphas 极饱和），或接受 EARNINGS 塔只亮 1 颗
