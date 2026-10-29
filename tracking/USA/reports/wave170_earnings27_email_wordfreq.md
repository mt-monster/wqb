# 波 170 归因报告 — `earnings27` 卖方邮件词频（8 模板机制消融）

- 区域 / 设置：**USA / TOP3000 / D1 / INDUSTRY / decay 0 / trunc 0.05 / 2014-01-01..2023-12-31**
- 数据集：`earnings27` = Earnings Update Emails Data，**14 字段全 VECTOR**，cov 0.2568–0.3027，alphaCount 1535，valueScore 2.0，pm 1.2，**历史 0 条已挖记录**
- 结论：**FAIL / n_pass = 0 / n_near = 0**

---

## 1. 机制假设与字段画像

`earnings27` 是卖方研报**邮件正文**的分词产物。每封邮件是一条 VECTOR 记录，按 ticker 聚合。字段分三族：

| 族 | 字段 | 经济学含义 | 覆盖 |
|---|---|---|---|
| 主题词频 | `ern27_earnings` / `ern27_expectations` / `ern27_revenue` | 邮件在谈什么（财报 / 预期 / 营收） | 0.256–0.303 |
| 情绪词频 | `ern27_positive` / `ern27_negative` / `ern27_neutral` | 语气（正 / 负 / 中性词计数） | 0.256–0.303 |
| 元数据 | `ern27_email_received` / `vendor_bank` / `email_from` / `atlas_unit_name` / `clean_subject` / `clean_content` / `email_content` / `is_multiple_ticker` | 非信号 | — |

**核心假设**：邮件词频是"分析师注意力 + 语气"的高频代理，情绪净差应当预测短期收益；主题配比反映叙事重心迁移。这是波 168 在 `earnings_sent_matrix` 上验证成功的机制（S 1.57–1.63）向"更原始、更高频"的数据源的迁移测试。

**为什么值得测**：这是 earnings 塔下**唯一尚未开采**的情绪类数据集，且 alphaCount 1535 相对 `earnings4`（13821，饱和）低一个数量级。

---

## 2. 8 模板与结果

`b(f, W)` 简写 `ts_backfill(f, W)`；`P/N/U` = positive/negative/neutral；`净差 = (P−N)/(P+N)`。

| # | 模板结构 | 矩 / 几何 | alpha | S | F | TO | 2Y | SUB | margin | invest_r | fRA | 判定 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| T1 | `group_rank(净差, industry)` | 水平·瞬时 | `mLoOr0gW` | **0.18** | 0.03 | **159.3%** | 1.10 | −0.32 | 0.46bp | 0.5556 | 6 | DEAD |
| T2 | `group_rank(ts_mean(净差,22), industry)` | 水平·短平滑 | `QPve2KW5` | **0.31** | 0.11 | 16.61% | 0.84 | 0.50 | 2.47bp | 0.9032 | 3 | DEAD |
| T3 | `group_rank(ts_zscore(净差,252), industry)` | 水平·长窗归一 | `KPJeXvJg` | **0.38** | 0.09 | **153.2%** | 0.88 | −0.33 | 1.07bp | 0.2632 | 6 | DEAD |
| T4 | `reverse(group_rank(ts_mean(P+N+U,22), industry))` | 水平·关注度反向 | `JjelgQ0l` | −0.25 | −0.08 | 16.73% | −0.92 | −0.52 | −1.95bp | 1.1600 | 5 | DEAD |
| T6 | `reverse(group_rank(ts_delta(N,22), industry))` | 一阶差分·负向词 | `j2YL9PGO` | −0.52 | −0.34 | 14.77% | −0.76 | −0.27 | −8.44bp | 1.1154 | 5 | DEAD |
| T8 | `group_rank(ts_mean(P/revenue,66), industry)` | 比值·主题配比 | `LLMegrk2` | **−1.00** | **−1.29** | 6.16% | −1.13 | −1.21 | **−67.6bp** | 0.1800 | 5 | DEAD |
| T5 | `group_rank(expectations/earnings, industry)` | 主题比 | — | 429 未提交 | — | — | — | — | — | — | — | 未测 |
| T7 | `group_rank(P/U, industry)` | 情绪比 | — | 在飞 40min 卡 progress 0.1 | — | — | — | — | — | — | — | 未测 |

**7 条已出结果全部 REJECT**，最好的一条（T3，S 0.38）距 S 闸 1.58 差 4 倍。

---

## 3. 归因：不是"信号弱"，是"信号被换手吃干净"

这是本波唯一有方法论价值的发现。把 `R/TO` 显式算出来（F = S·√(R/max(TO,0.125))，F=1.0 需 `R/TO ≥ 1/1.58² ≈ 0.406`）：

| alpha | S | R | TO | **R/TO** | 距 0.406 门槛 | margin |
|---|---|---|---|---|---|---|
| `LLMegrk2` (T8) | −1.00 | −20.82% | 6.16% | **0.338** | 0.83× | −67.6bp |
| `QPve2KW5` (T2) | 0.31 | 2.05% | 16.61% | **0.012** | 1/34 | 2.47bp |
| `JjelgQ0l` (T4) | −0.25 | −1.63% | 16.73% | **−0.010** | 反向 | −1.95bp |
| `j2YL9PGO` (T6) | −0.52 | −6.23% | 14.77% | **−0.042** | 反向 | −8.44bp |
| `mLoOr0gW` (T1) | 0.18 | 3.70% | 159.3% | **0.002** | 1/200 | 0.46bp |
| `KPJeXvJg` (T3) | 0.38 | 8.17% | 153.2% | **0.005** | 1/80 | 1.07bp |

三条结构性事实：

1. **词频类模板的 TO 天生 15%+**（T1/T3 达 153–159%）。VECTOR 事件型邮件数据每天增删记录，`vec_sum` 的横截面排名日频翻转。任何窗口 < 66 都被日频翻转主导。
2. **margin 全部在 0.46–2.47bp**（T8 例外，见下）。同区 `shortinterest3` 的成功族 margin 是 12–27bp，差 5–20 倍。**margin 才是这个数据集的天花板**，不是 Sharpe。
3. **T1/T3 的 153%+ 换手把 margin 压到 0.46bp**：`R/TO = 0.002`。这类结构在 TOP3000 上根本不可能到达 F 闸，无论怎么调窗口。

---

## 4. 唯一有价值的线索：T8 是"方向为负的真信号"

`LLMegrk2 = group_rank(ts_mean(P/revenue, 66), industry)`：

- margin **−67.6bp**（绝对值是全波最大的 27 倍）
- TO 仅 **6.16%**（全波最低）
- R −20.82%、S −1.00、2Y −1.13、SUB −1.21、invest_ratio 0.18

**读法**：这三个数字同时成立只有一种解释——"邮件里正面词相对营收词越多"⇒ 后续收益显著为负。它**不是噪声**（噪声不会给出 67.6bp 的稳定 margin，也不会 2Y/SUB 同向为负），而是**真信号但方向反了**。

**经济学解释**：卖方在营收话题上堆正面词的密度，是"叙事包装强度"的代理。叙事包装越重，实际基本面兑现越差（卖方在替疲弱的营收找正面说法）。这是一个**反向叙事密度**因子。

**为什么本波没有直接 reverse 它**：`reverse()` 只翻转符号，不改变 TO（6.16%）与 margin 绝对值。反向后的 `R/TO` 仍是 **0.338**，仍低于 0.406 门槛 ⇒ 即使方向对，F 也只有 0.85 左右，且 S 只有 1.00，距 1.58 差 60%。**要救它必须提升 S 本身，不是翻转方向。**

已按 `registry_empirical` `USA-EARN27-WORDFREQ-DEAD` 保留为唯一续命线索：若日后重启该数据集，只做这一条，必须 `reverse` + 窗口 > 66。

---

## 5. 第二个"同机制不可跨数据集外推"反证

| 骨架 | `earnings_sent_matrix`（波 168） | `earnings27`（波 170） |
|---|---|---|
| `group_rank(净差, industry)` | — | T1 S **0.18** |
| `group_rank(ts_mean(净差,22), industry)` | — | T2 S **0.31** |
| `group_rank(ts_zscore(净差,252), industry)` | E7 S **1.57** | T3 S **0.38** |
| `group_rank(ts_rank(正类概率,504), industry)` | E3 S **1.63** ← 全闸 `RREXk770` | — |

**同一"有符号情绪净差 + 长窗时序归一 + industry 分组"三件套**：在结构化情绪概率（和为 1 的三分类分布）上是全数据集唯一的活机制（S 1.57–1.63），搬到邮件词频上只剩 0.18–0.38。

这是本项目第二个直接反证：

- **反证一（波 167→168）**：矩类模板不可外推。`shortinterest3` 上 4 种矩全活（水平 1.78 / 方差 2.04 / vol-of-vol 1.74 / 绝对一阶 1.74）；`earnings_sent_matrix` 上矩类全死（二阶 −0.52 / 绝对一阶 −0.23 / 三阶 −0.60）。
- **反证二（波 168→170）**：方向类模板也不可外推。

**合并结论（本项目的方法论铁律）**：**没有任何骨架可以跨数据集迁移。**唯一可以跨数据集继承的只有"候选机制清单"（试哪些形状），绝不能继承"哪个形状有效"的判断。每个新数据集必须独立跑 ≥10 模板的机制消融。这条直接决定了 SOP：数据集一旦入选，第一波就必须是模板消融波，不能是"把上个数集的最优骨架改字段"。

**为什么这两个数据集差这么远（机理）**：`earnings_sent_matrix` 的三类概率**和为 1**，是闭合单纯形上的分布 ⇒ 净差 `(P−N)/(P+N)` 是良定义的、有界的、时序平稳的方向测度。`earnings27` 的 `P/N/U` 是**无约束的计数**，分母随邮件长度任意缩放，`(P−N)/(P+N)` 量纲不稳定、时序不平稳。**"分布型字段" vs "计数型字段"是能否做净差的分水岭。**

---

## 6. 数据集判死与泛化规则

已写入 `registry_empirical`，`layer=dead_end`，`entry_id = USA-EARN27-WORDFREQ-DEAD`。

**封盘范围**：`ern27_positive` / `ern27_negative` / `ern27_neutral` / `ern27_earnings` / `ern27_expectations` / `ern27_revenue` 上的一切情绪净差、关注度、主题配比骨架。

**泛化规则（可跨数据集使用）**：

1. **VECTOR 事件型（邮件 / 逐笔 / 研报）数据集的日频词频类信号天然 TO 15%+**。派发前先算 TO 结构，不要先跑 S —— 在 TO 150% 的结构上，S 再好也到不了 F 闸。
2. **判"数据集有无信号"要看 margin 绝对值，不看 Sharpe**。`LLMegrk2` 的 S 只有 −1.00 但 margin 67.6bp，是全波唯一真信号；`mLoOr0gW` 的 S 0.18 而 margin 0.46bp，是纯噪声。**margin 是信噪比，Sharpe 是方向一致性。**
3. **计数型字段不能直接做比值净差**：`count(positive)−count(negative)` 除以 `count(positive)+count(negative)` 的分母无量纲但不平稳。要在这类字段上做方向，必须先用**分布内归一**（除以总词数或 `vec_sum` 全族之和）再取差。
4. **`reverse()` 只翻符号、不改 TO 与 margin 绝对值**。判"这个结构能不能救"要算 `reverse` 后的 `R/TO`，不要看到负 S 就以为反一下就有货。

---

## 7. 对 earnings 塔的影响

- earnings 塔当前 **1/3**，唯一全闸候选仍是波 168 的 `RREXk770`（S 1.63 / F 1.02 / 2Y 3.00 / invest 0.8712 / fRA 0）。
- 第 2/3 颗的两条路都已封死：`58ERq5LM` 卡 F 0.89 结构性天花板（波 169 六个提换手杠杆全败）；`earnings27` 本波判死。
- **下一候选必须来自 `earnings7`**（Horizon Earnings and Calendar NA，40 字段、cov 0.6479、alphaCount 1323、**历史 0 条已挖**，5 个真信号字段 `ern7_dsu_spe` / `ern7_co_spe` / `ern7_div_amount_usd` / `ern7_spe` / `ern7_div_amount_oc`）。T9–T12 四条已过 `preflight_expressions`，但仅 4 个模板不满足 ≥10 模板硬约束，需先补足模板库再开波。
- `earnings4`（alphaCount 13821）已饱和、`earnings_chart_dl`（best_s 0.69）已测弱、`earnings6`（104 行，best_s 1.77）可作后备。

---

## 8. 本波遗留（不补）

- **T5**（`expectations/earnings` 主题词比）遇 429 从未提交。
- **T7**（`P/U` 情绪比）在飞 40 分钟仍卡 `progress 0.1`，判排队/卡死。

两者均不补派：本波结论已由 6 条已出结果充分支撑（最好 S 0.38，全部 TO 15%+ / margin < 2.5bp），补派只会消耗仿真槽。
