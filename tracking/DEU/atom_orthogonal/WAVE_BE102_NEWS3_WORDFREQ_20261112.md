# BE102 设计档：NEWS 塔最后漏洞补测（news3/news21 词频情绪面，2026-11-12 深夜）

> 起因：对「约束内全谱出清」结论做终检，发现处置图谱里 news21/29/3/54/76 五个 cov=0 集
> 只有先验排除、无实测。BE94 补了 news21 的 event_frequency_label（lc 36，S 弱），
> 但字段清单核实后仍有真实漏洞——**news3 的 19 个情绪分数字段与 news21 的 8 个词频/语气字段从未测过**。

## 五集裁定（先档案，后实测）

| 数据集 | 字段画像 | 裁定 |
|---|---|---|
| news76 | 2 字段：previous_score / score_value（**deprecated，恒 0**） | ❌ 零成本否决，无需仿真 |
| news54 | 39 字段全为时间戳/标志位/季度标签（事件日历元数据） | ❌ 无数值信号面，零成本否决 |
| news29 | 16 字段全为文本全文/主题代码/frontpage 标志 | ❌ 无横截面数值信号面，零成本否决 |
| **news3** | 19 字段归一化情绪分数（fear/finup/finhype/uncertainty/findown/certainty 及部分分） | ⏳ **BE102 在飞** |
| **news21** | 8 个 MATRIX 词频字段（pos_sc/neg_sc/tone/qerf_gen/qerf_sop/nws21_event_freq） | ⏳ **BE102 在飞**（词频面）+ BE94 已测 event_freq |

## BE102 十臂（1xr0ITbpU4AVbFg1dHxfPeRN）

| # | 字段 | 构造 | 机制 |
|---|---|---|---|
| 1 | nws3_fearnormscr | 水平 66 | 恐惧水平（避险溢价） |
| 2 | nws3_finupnormscr | 水平 66 | 财务乐观 |
| 3 | nws3_finhypenormscr | 水平 66 | 财务炒作（反向假设：炒作高→回调） |
| 4 | nws3_uncertaintynormscr | 水平 66 | 不确定性（风险折价） |
| 5 | nws3_findownnormscr | 水平 66 | 财务悲观 |
| 6 | nws3_certaintynormscr | 水平 66 | 确定性（信心溢价） |
| 7 | nws3_fearpartnormscr | Δ66 | 恐惧**变化**（情绪动量） |
| 8 | nws21_tone_tone_sc | 水平 66 | 净语气（正词−负词占比） |
| 9 | nws21_pos_sc | 水平 66 | 正词占比 |
| 10 | nws21_neg_sc | 水平 66 | 负词占比 |

设置：decay4/SUBINDUSTRY/nan ON（同 BE93/94 角落档）。

## 判读线（协议 v2 L1）

max |S| ≥1.2 满波 / 1.0-1.2 定向补 / <1.0 判死 + lc 证书。
注意：sentiment7/27/33（情绪塔）已判死，但 news3 是**不同供应商、不同情感维度**（词频归一化 vs 打分模型），
BE38 判死的是 news17/18/38/50/104 的**事件情绪通道**——news3 的词频面未被任何波覆盖，不是重试。
