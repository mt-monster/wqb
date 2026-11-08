# s1_insider_feats Wave1 · 模板池与画像（EUR / TOP2500 / D1）

> 数据集：`insider_feats`（Global Insider Transaction Features）· category = **other**（OTHER 塔 2/3，本轮差 1 颗点亮）
> 波次：`s1_insider_feats_wave1` · 统一设置 **EUR / TOP2500 / delay 1 / decay 8 / neutralization STATISTICAL / truncation 0.08 / unit VERIFY / nan ON / pasteurization ON / maxTrade ON**
> 开波日：2026-11-06。上游：`insider_agg_matrix`（insiders 塔，S 1.96–2.00 但 prod 0.76–0.80 卡墙）⇒ 本波是「同经济族、**不同厂商构造**」的降 prod 主攻方向。

## 一、字段画像（118 字段，全 MATRIX）

| 族 | 代表字段 | 字段数 | cov | aC 范围 | 语义 |
|---|---|---|---|---|---|
| **A 金额买卖比** | `buy_sell_ratio_all_{5,10,20,60,250}d_filled`、`buy_sell_ratio_top{5,20}_{5,20,60,250}d_filled` | 13 | **0.9157** | 4–115 | 买入金额 ÷ 卖出金额（窗口内），top 口径只计最大 N 笔 |
| B 笔数买卖比 | `buy_sell_tx_count_ratio_{all,top5,top20}_{5,10,20,60,250}d[_filled]` | 24 | 0.34–0.9157 | 1–57 | 买入笔数 ÷ 卖出笔数 |
| C 复合比别名 | `buy_to_sell_ratio_*`、`buy_to_sell_txn_ratio_*`、`buy_to_sell_volume_ratio_*` | 21 | 0.34–0.9157 | 0–15 | 同 A/B 的另命名口径（部分为量比） |
| D 原始计数（买） | `top5/top20/total_buy_tx_count_*` | 30 | 0.16–0.72 | 0–17 | 买入笔数绝对值 |
| E 原始计数（卖） | `top5/top20/total_sale_tx_count_*`、`*_sale_volume_*` | 30 | 0.18–0.70 | 0–3 | 卖出笔数/量绝对值 |

**画像结论（三条硬筛）**：
1. **只用 A 族（cov 0.9157）**。D/E 族 cov 0.16–0.72，落在论坛实测的「cov<0.7 必死」区（子宇宙 S 0.16–0.25）；B/C 族只有 `_filled` 后缀的才达 0.9157。
2. **计数族（D/E）先验判死**：论坛同数据集实证计数类 S 0.29–0.66，比值类才 1.94。计数度量「发生了没有」，比值度量「方向有多强」。
3. **全 MATRIX** ⇒ 无需 `vec_*` ⇒ 核心表达式只需 2–3 个算子（本波最大优势）。
4. **稀疏**：即便 cov 0.9157，事件本身仍稀疏 ⇒ 一律 `ts_backfill(·, 250)`（论坛规则②）。
5. 窗口语义：5d 一周脉冲 / 10d 半月 / 20d 月 / 60d 季 / 250d 年。

## 二、10 个结构互异模板库

| # | 模板 | 结构 | 几何族 | 算子 | 来源 |
|---|---|---|---|---|---|
| T-01 | 基线比值 | `group_neutralize(rank(ts_backfill(ratio_all_10d,250)), sector)` | 横截面秩（水平） | 3 | 论坛原式 |
| T-02 | 长窗比值 | 同上，`ratio_all_250d` | 同上（窗口轴） | 3 | 论坛 |
| T-03 | 大额口径 | `ratio_top20_20d_filled` 代入 T-01 | 参与者过滤 | 3 | 论坛 |
| T-04 | 极值口径 | `ratio_top5_60d_filled` 代入 T-01 | 参与者过滤（最知情 5 笔） | 3 | 论坛 + Seyhun 1986 量级效应 |
| T-05 | 短−长窗差 | `group_neutralize(rank(subtract(ts_backfill(all_10d,250), ts_backfill(all_250d,250))), sector)` | 一阶差分（方向变化） | 5 | 自建（二阶信息） |
| T-06 | 自身历史异常度 | `group_neutralize(rank(ts_zscore(ts_backfill(all_60d,250), 252)), sector)` | 时序标准化 | 4 | 文献（surprise）；⚠ EUR 先验弱 |
| T-07 | 双口径确认 | `group_neutralize(multiply(rank(ts_backfill(all_10d,250)), rank(ts_backfill(tx_count_ratio_all_10d_filled,250))), sector)` | 交互项（金额 × 笔数） | 5 | KOR 实证 multiply(rank,rank) 到 S1.67 |
| T-08 | 买入日占比 | `group_neutralize(rank(ts_mean(greater(ts_backfill(all_10d,250), 1), 66)), sector)` | 符号占比（非线性） | 5 | 文献（persistence） |
| T-09 | 集中 vs 分散 | `group_neutralize(rank(divide(ts_backfill(all_60d,250), ts_backfill(top5_60d_filled,250))), sector)` | 比之比（结构分歧） | 5 | 自建（小额跟随大额？） |
| T-10 | 波动调整比值 | `group_neutralize(rank(divide(subtract(ts_backfill(all_60d,250),1), ts_std_dev(ts_backfill(all_60d,250),66))), sector)` | 信息比率式 | 6 | 自建（SNR） |

**结构差异落点**：横截面水平（T-01/02）/ 参与者过滤（T-03/04）/ 一阶差分（T-05）/ 时序标准化（T-06）/ 双字段交互（T-07）/ 符号占比（T-08）/ 比之比（T-09）/ 波动调整（T-10）——覆盖 8 个互异几何族，满足「≥10 模板、结构互异」硬约束（其中 T-03/04 为口径轴而非几何轴，已在备注中标注）。

## 三、外部溯源

**论坛（已读全文）**：`43585639794967` ·《内部人买卖流量比：把「知情交易」这个老故事，翻译成 AMR 市场能跑的一个模板》· YS12717 · 2 票 · 2026-09-18。可迁移结论 7 条：
1. 比值类活着、计数类全灭（S 0.29–0.66）；2. cov<0.7 字段必死；3. `ts_backfill(·,252)` 必做；4. 中性化档差 3 倍（STATISTICAL 1.94 / SUBINDUSTRY 1.51 / INDUSTRY 0.96 / MARKET 0.56）；5. 短窗强于长窗；6. 同族只容 2–3 条（同步闸）；7. **换同经济族、不同厂商构造的数据集是降 prod 的唯一有效手段**——本波的存在理由。

**学术先验（未联网核对，仅作方向约束）**：
- Lakonishok & Lee (2001)：内部人**买入**有预测力，卖出几乎没有 ⇒ 比值的信息应主要来自分子（买入侧）。**可检验推论：比值与「买入侧单独量」应同号，且纯卖出侧字段无效。**
- Seyhun (1986)：内部人交易的**量级**信息含量高于笔数 ⇒ T-03/T-04 的 top 口径应对 all 口径有增益。
- Jeng-Metrick-Zeckhauser (2003)：买入组合年化异常收益约 11% ⇒ 信号应偏慢（换手不宜过高），与 decay 8 + 250 日 backfill 相容。
- Cohen-Malloy-Pomorski (2012)：**机会型**内部人交易有预测力、**例行型**无 ⇒ 高波动/异常期的内部人买入更有信息；T-10 波动调整是该假设的最简代理。
- Rozeff & Zaman (1998)：内部人在价格下跌后买入（反向）⇒ 若 T-01 与动量负相关，属预期内，不等于失效。

## 四、第 41 批（已派发）

`3V9FWi28v5fnclKmEAH4x5K` · STATISTICAL / decay 8 / trunc 0.08 / nan ON / maxTrade ON · 各 3 算子 · 三闸全过（`valid=true`，字段平台存在，unknown_fields=[]）

```
F1 = group_neutralize(rank(ts_backfill(buy_sell_ratio_all_10d_filled, 250)), sector)
F2 = group_neutralize(rank(ts_backfill(buy_sell_ratio_all_250d_filled, 250)), sector)
```

**判读标准**：
- F1 若 S ≥ 1.5 且 prod < 0.70 ⇒ **直接是 OTHER 塔点亮候选**（本战役第一条非 INSIDERS 塔的可提交件）。
- F1 与 F2 的 ΔS 决定窗口轴方向：F2 > F1 ⇒ 长窗（慢信号）在 EUR 更强，与论坛 AMR 结论相反（可解释：EUR 信息传导更快，长窗累积更多信息）。
- 若 F1 S < 1.0 ⇒ 比值机制在 EUR 不成立（与 insider_agg_matrix 净买量 S 2.00 冲突）⇒ 差别在「比值 vs 净量」，转 T-05/T-07 并补「净量口径」字段探针。
- 无论 S 高低，**F1 的 prod 是本波最关键读数**（论坛第 7 条的直接检验）：若同经济族换厂商后 prod 从 0.76–0.80 掉到 <0.70 ⇒ 该手段在 EUR 成立，可回灌给 insider_agg_matrix 族。

## 五、纪律

- 每批恰好 2 条、批级设置唯一；收批入库后才派下一批。
- 禁混：本条单数据集 ATOM（全 OTHER 字段）不占塔混配额；**禁止**引入 PV/MODEL/FUNDAMENTAL 字段（与 OTHER 同属禁混集合）。论坛建议的「+0.5 成交量腿」因此**不可用**，需改用本数据集内字段做稀释。
- 同族容量 2–3 条（论坛 + 平台同步闸）⇒ 本数据集最多产出 3 颗，冲塔需另开第 4 个数据集。
## 六、执行进度（2026-11-06）

| 批 | alpha | 模板 | 算子 | S | F | 2Y | sub | TO | margin | fRA | 判定 |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| 41 | `WjOlrz2o` | T-01 all_10d（论坛基线） | 3 | 0.64 | 0.21 | 0.28 | 0.53 | 10.57% | 2.53bp | 3 | ❌ 论坛基线不可迁移（AMR 1.94 → EUR 0.64） |
| 41 | `leAawGPn` | T-02 all_250d（长窗） | 3 | 0.12 | 0.01 | 0.72 | 0.21 | 3.46% | 1.10bp | 3 | ❌ 长窗更差 ⇒ 论坛「短窗强于长窗」方向成立 |
| 42 | `3qo0KWLN` | T-03 top20_20d | 3 | 1.31 | 0.60 | 0.93 | 0.82 | 7.80% | 6.66bp | 3 | ⚠ near 线，未过三闸 |
| 42 | **`58EJmVVo`** | **T-04 top5_60d** | **3** | **1.65** | 0.80 | 0.84 | **1.41** | **5.09%** | **11.65bp** | 2 | ★ **S 过线**，缺 F(+0.20) 与 2Y(+0.74)；**self 0.0934 PASS** |

**★ 量级效应单调成立**：all（S 0.64）→ top20（1.31）→ top5（1.65）。口径越集中、越接近「最知情的 5 笔」信号越强 —— 与 Seyhun (1986) 的「交易量级信息含量」先验一致，且是本数据集最强的结构轴。

**★ 三闸精确线（submit_verdict 原始 limit）**：`S ≥ 1.58` · `Fitness ≥ 1.00` · `2Y Sharpe ≥ 1.58`。`58EJmVVo` 触发 `LOW_FITNESS(1.00)` 与 `LOW_2Y_SHARPE(1.58)` 两条硬闸 ⇒ fRA=2 / BLOCKED。

**★ 下一步（本数据集内）**：T-04 的骨架已证明 S 可达 1.65，缺口在 **F 与 2Y** ⇒ 用「同机制、不同参与人/口径」的第二腿做加权合成（本文件 §二 的 T-03/T-04 互配），或跨厂商合成（见台账 §274-F：`add(multiply(2, STRONG), COLD)`）。

**已派后续**：
- 第 43 批 `2FFpVR4mx5iB9PTuxHrFFo6`（SLOW_AND_FAST / decay 8）：累计水平量形态 `group_rank(ts_sum(subtract(ts_backfill(ratio,250),1),63), industry)` × {all_10d, top20_20d}
- 第 44 批 `2kUeRzU94tvch4KpsurYj3`（SLOW_AND_FAST / decay 8）：跨厂商合成 `add(multiply(2, 净股数63d), 比值10d)`（2:1）与 `add(净股数63d, 比值10d)`（1:1）
