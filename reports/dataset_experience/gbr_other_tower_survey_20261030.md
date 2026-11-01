# GBR OTHER 塔数据集普查与死路清单

> 区域 GBR / universe TOP700 / delay 1
> 生成日期：2026-10-30
> 数据来源：`get_datasets(region="GBR", category="other", delay=1, universe="TOP700")` 全量 41 条 + 各数据集实测回测

---

## 一、塔位口径与本文定位

GBR D1 塔位共 5 个：`PV` / `MODEL` / `OTHER` / `ANALYST` / `FUNDAMENTAL`。
`OTHER` 塔的 alpha 必须只使用 **category = other** 的字段（单数据集）。

**硬约束**（用户口径）：`{PV, MODEL, OTHER}` 三者之间**禁止两两组腿**（含 `PV+PV`）。
⇒ OTHER 塔的 alpha **不能**借 PV / MODEL 的字段做门控或正交腿。
⇒ 可用组合伙伴只有：`ANALYST` / `FUNDAMENTAL` / `NEWS` / `MACRO` / `RISK` 等非 trio category（且总量 ≤5 个）。

**本文结论先行**：GBR 的 OTHER 塔已实测排除 **8 条**路径，其中 2 条是「**平台有字段但 GBR 无数据**」（回测 TO 恒 0.00%），其余为噪声或已知饱和。**该塔在 GBR 呈现结构性枯竭**。

---

## 二、41 个 `other` 数据集全景（按可挖性排序）

`valueScore` 是平台的 OS/IS Sharpe 质量分（越高越好），`userCount` / `alphaCount` 是拥挤度。

### 2.1 高价值 + 低拥挤（valueScore ≥ 6 且 alphaCount ≤ 25）— 理论富矿

| dataset | 名称 | 字段 | u / a | valueScore |
|---|---|---|---:|---:|
| `workforce_flow_skills` | Global Workforce Flow and Skills | 10（全 VECTOR） | 3 / 3 | 6 |
| `other546` | Institutional Network Analysis | 22（全 VECTOR，边表） | 3 / 3 | **7** |
| `other128` | Global Executive Performance Factors | 14 | 4 / 12 | **7** |
| `event_relation` | Text-Based Event Relationship | 12 | 4 / 12 | 6 |
| `other327` | Sensitivity to Interest Rates Model | 3 | 3 / 4 | 6 |
| `other635` | Thomson Reuters News Analytics | 3 | 2 / 2 | 6 |
| `other425` | Supply Chain Data | 13 | 8 / 22 | 6 |
| `other545` | Linked Firms Momentum | 4 | 18 / 25 | 6 |
| `other571` | Wikipedia Viewing | 23 | 3 / 3 | 7 |

★ **`other571` 已核**：23 字段的描述全部写成 "in the USA module" ⇒ **GBR 无覆盖**，勿再试。

### 2.2 中等（valueScore 5–6，拥挤度中等）

`ai_news_scores`(105) · `earningscall_sentiment`(167) · `event_sentiment_signals`(52) · `news_sentiment_nlp`(23) · `other696`(220) · `other78`(112) · `other296`(10) · `other566`(112) · `search_interest`(7) · `stock_search_trends`(12) · `stock_cluster_dl`(5) · `insider_trx_matrix`(33) · `other699`(7)

### 2.3 低价值或已知饱和

| dataset | 字段 | u / a | valueScore | 说明 |
|---|---|---:|---:|---|
| `techindi_model` | 399 | 1818 / 25667 | 2 | 极度饱和，等同死路 |
| `acquisition_model` | 15 | 502 / 1537 | 2 | 饱和 |
| `dl_riskfree_returns` | 133 | 453 / 928 | 3 | 全族已判死 |
| `insider_matrix` | 33 | 280 / 530 | 4 | 高拥挤 |
| `other335` | 10 | 155 / 255 | 3 | 弱 |

---

## 三、已判死路径（8 条，全部有实测数字）

### ✗ 3.1 `workforce_flow_skills` —— 有数据但无信号 / 部分字段根本无数据

设置：`SUBINDUSTRY / decay 10 / trunc 0.05`，骨架 `ts_quantile(·, 252)`

| alpha | 机制 | S | F | 2Y | TO | margin | 判 |
|---|---|---:|---:|---:|---:|---:|---|
| `leAJEePl` | 净招聘率 `divide(subtract(vec_sum(inflow), vec_sum(outflow)), vec_sum(headcount))` | 0.02 | 0.00 | −0.42 | 9.29% | 5e-6 | **持仓真实、信号为零** |
| `2rAP9ro5` | `ts_delta(vec_avg(adjusted_employee_headcount), 252)` | 0.00 | — | — | **0.00%** | 0.0 | **该字段 GBR 无数据** |

**关键分辨法**：`TO = 0.00%` 且 `returns = 0.0` ⇒ **字段无覆盖**；`TO 正常但 margin ≈ 0` ⇒ **有数据但无信号**。两者必须分开判。
⇒ `employee_inflow_count_2` / `employee_outflow_count_2` / `employee_headcount_2` **有数据无信号**；`adjusted_employee_headcount` **无数据**。

### ✗ 3.2 `other327` —— GBR 无数据

| alpha | 机制 | S | TO | 判 |
|---|---|---:|---:|---|
| `9qxg8JY9` | `ts_quantile(ts_delta(oth327_sirc_lev, 252), 252)`（利率敏感度变化） | 0.00 | **0.00%** | **无数据** |

3 个字段：`oth327_mktcap`（市值）/ `oth327_sirc_lev`（美债曲线水平敏感度）/ `oth327_sirc_sl`（斜率敏感度）。**GBR 无覆盖。**

### ✗ 3.3 `other546` —— 有数据但纯噪声

| alpha | 机制 | S | F | 2Y | TO | margin | 判 |
|---|---|---:|---:|---:|---:|---:|---|
| `LLMOEkW9` | `ts_quantile(vec_sum(shared_executive_count), 252)`（高管网络中心度） | 0.49 | 0.08 | −0.56 | 9.37% | 0.72bp | 噪声 |

22 字段全部 VECTOR，是**边表结构**（每行一个「主体—同业」对 + 相似度权重）。只有结构特征可用，**没有 peer return ⇒ 无法构造真正的网络动量**。

### ✗ 3.4–3.8 历史已判死（本轮之前）

| dataset | 判死理由 |
|---|---|
| `other567` Employee Review | T1/T3 双灭 |
| `other169` CDS | 截面秩几何最佳仅 S 0.66 |
| `event_ml_signals` | 104 字段全 VECTOR、coverage 0.0，低先验 |
| `tm_16` + `tm_17` | 全族 prod 0.7343–1.0（相关性墙） |
| `other47` / `other384` / `other455` | 各 8 模板 / 全族判死 |
| `quant_factor_lib` + `risk60` | prod 墙 |
| `annualized_pd_*` | prod 0.99+ |
| `other571` Wikipedia | 23 字段描述全写 "in the USA module" |
| `other699` Individual Investor Transactions | 7 字段，实测无货 |

---

## 四、未测候选池与先验评估

只剩这些没实测过，且**先验都偏弱**：

| dataset | 可挖点 | 先验 | 风险 |
|---|---|---|---|
| `other128` Global Executive Performance Factors | 高管绩效因子（u4/a12，valueScore 7） | 管理质量 → 未来收益（cf. 管理能力文献） | 14 字段，描述可能又是 BBID/RIC 映射污染；需先 `get_datafields` 核实 |
| `event_relation` | 文本事件关系强度 | 事件网络传导 | 12 字段，u4/a12 极低 ⇒ 可能无数据 |
| `other425` Supply Chain | 供应链关系 | 供应链冲击传导 | 13 字段，需配对价格才能用 |
| `other545` Linked Firms Momentum | **已含**网络动量信号（4 字段，u18/a25） | 链接企业动量传导（Cohen-Frazzini 2008） | 仅 4 字段；若已内建动量则可能直接可用 |
| `stock_cluster_dl` | DL 聚类标签（5 字段，coverage 0.4739） | 聚类轴做 `group_neutralize` | **other 字段不能与 PV/MODEL 组合**，只能配 FUND/ANALYST |

### ★ 下一优先序（若继续攻 OTHER）

1. **`other545` Linked Firms Momentum**（4 字段，已内建网络动量，先验最实）— 单数据集即可，不触塔混禁令。
2. **`other128`**（valueScore 7，字段数适中）— 先 `get_datafields` 核实描述是否被 BBID/RIC 文案污染。
3. `stock_cluster_dl` + ANALYST/FUND 组合（消耗 trio×非 trio 的 ≤5 配额）。

---

## 五、结构性结论

1. **OTHER 塔在 GBR 的核心困难是「数据在、信号不在」**：`workforce_flow_skills` 与 `other546` 都有真实持仓（TO ≈ 9%），但 S ≤ 0.49、margin ≤ 0.72bp ⇒ 这些替代数据对 GBR 大盘股没有可交易的信息含量。
2. **另有一类是「字段在、数据不在」**：`adjusted_employee_headcount`、`oth327_*` 回测 TO 恒 0.00%。用 `get_datafields` 无法分辨这两类，**只能靠一次最小回测的 `turnover` 判别**。
3. **GBR TOP700 的替代数据价值集中在 PV 与 FUNDAMENTAL**：本会话 40+ 批里唯一产出全闸 alpha 的四个机制（估值位移 / 换手率 / pattern 缺口 / continuation gap 反转）**全部来自 PV 或 FUND**。
4. ⇒ **不要再用 GBR 的 OTHER 塔消耗仿真配额**，除非在 `other545` 上有新的具体理由。

---

## 六、判「字段是否有 GBR 数据」的零成本升级路径

本会话验证过的最快判别（按成本从低到高）：

1. `get_datafields(dataset_id=..., region="GBR", universe="TOP700", delay=1, filter_sharpe=False)` — 只能确认**字段注册存在**，**不能**确认覆盖。
2. `preflight_expressions(..., dataset_id=...)` — 确认字段名 + VECTOR 类型，仍是零成本，**不含覆盖**。
3. **一次最小回测看 `turnover`** — 唯一可靠的覆盖判据：
   - `TO ≈ 0.00%` 且 `returns = 0.0` ⇒ 无覆盖
   - `TO` 正常（5%–20%）但 `margin ≈ 0` ⇒ 有覆盖、无信号
4. `get_alpha_details` 的 `longCount + shortCount` 是持仓数口径，**与覆盖相关但不等价**（有持仓也可能是极少数股票）。
