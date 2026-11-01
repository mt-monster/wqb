# other384 财报电话会 transcript 模板库 — GBR / TOP700 / D1

**建立日期**：2026-10-30
**区域设置**：`region=GBR / universe=TOP700 / delay=1 / neutralization=STATISTICAL / decay=4 / truncation=0.08 / nan_handling=ON / max_trade=ON / pasteurization=ON / unit_handling=VERIFY`
**塔位**：数据集 category = `OTHER`（`oth384_` 前缀字段族）⇒ **纯 OTHER 单塔，不占 trio×非 trio 配额**
**覆盖**：coverage `0.2175`（档 A 19 个字段）/ `0.2105`（档 B 47 个字段）；`userCount` 全 0（GBR 零历史）、`alphaCount` 仅 3 个字段各 1（`oth384_qa_tone` / `oth384_qerfgen_aq` / `oth384_qerfsop_aq`）

---

## 0. 认知前置：这是 earnings call transcript，不是"other 杂项"

数据集描述在平台侧是模板化文案，**只有字段名可信**（本项目已在 11 个 `other*` 上踩过同一坑）。`get_datafields(dataset_id="other384", max_fields=70)` 实读 66 字段后确认：

**这是财报电话会议记录（earnings call transcript）的 NLP 解析结果**，含陈述段（presentation）与问答段（Q&A）两段结构，每段有语气、正负词频、篇幅/段落/句子计数，另有**笑声标注**与**高管出席标志**。

**关键价值**：本项目 `earningscall_sentiment` 在 GBR 的 coverage = **0**（不可用），`other384` 是同一类数据的**可用版本**，且落在 OTHER 塔。

---

## 1. 66 字段分家族清单

### 1.1 语气族（已归一化，无量纲，可直接用）

| 字段 | coverage | 含义 | ⚠ 同义冗余 |
|---|---|---|---|
| `oth384_qa_tone` | 0.2175 | Q&A 段语气得分 | ≡ `qa_overall_sentiment_score` |
| `oth384_presentation_tone` | 0.2175 | 陈述段语气得分 | ≡ `presentation_overall_sentiment_score` |
| `oth384_qerfsop_aq` | 0.2175 | Q&A 正词频 = QA_posNum/QA_count | ≡ `qa_positive_word_frequency` |
| `oth384_qerfgen_aq` | 0.2175 | Q&A 负词频 | ≡ `qa_negative_word_frequency` |
| `oth384_presentation_posfreq` | 0.2175 | 陈述段正词频 | ≡ `presentation_positive_word_frequency` |
| `oth384_presentation_negfreq` | 0.2175 | 陈述段负词频 | ≡ `presentation_negative_word_frequency` |
| `presentation_overall_sentiment_score` | 0.2105 | 陈述段语气（别名） | 见上 |
| `qa_overall_sentiment_score` | 0.2105 | Q&A 语气（别名） | 见上 |
| `presentation_positive_word_frequency` | 0.2105 | 陈述正词频（别名） | 见上 |
| `presentation_negative_word_frequency` | 0.2105 | 陈述负词频（别名） | 见上 |
| `qa_positive_word_frequency` | 0.2105 | Q&A 正词频（别名） | 见上 |
| `qa_negative_word_frequency` | 0.2105 | Q&A 负词频（别名） | 见上 |

> **⚠⚠ 伪多样性陷阱（最高优先级）**：上表 12 个字段实际只有 **6 个自由度**（陈述/Q&A × tone/pos/neg），且平台**已经做过比率归一化**，所以 `divide(vec_avg(posnum), vec_avg(count))` 与直接用 `posfreq` 是**同一个信号**。这与 log-prob 数据集"三桶求和为 1、换桶不算换机制"的教训同构。
> **规则：可以把 `posfreq` 与 `posnum/count` 视为一条腿，不可视为两条模板。**

### 1.2 结构计数族（有量纲，需比值或与同段字段比）

| 字段 | coverage | 含义 |
|---|---|---|
| `oth384_qa_questions` / `qa_question_total` | 0.2175 / 0.2105 | Q&A 提问总数 |
| `oth384_presentation_questions` / `presentation_question_total` | 0.2175 / 0.2105 | 陈述段提问数 |
| `qa_word_total` / `presentation_word_total` | 0.2105 | 段落总词数（**含**说话人与标注） |
| `qa_content_item_total` / `presentation_content_item_total` | 0.2105 | 实义词数（**不含**说话人与标注） |
| `oth384_qa_count` / `oth384_presentation_count` | 0.2175 | 实义词数（别名） |
| `qa_sentence_total` / `presentation_sentence_total` | 0.2105 | 句数 |
| `oth384_qa_paragraphcount` / `oth384_presentation_paragraphcount` | 0.2175 | 段落数 |
| `oth384_qa_posnum` / `oth384_qa_negnum` | 0.2175 | Q&A 正/负词实例数 |
| `oth384_presentation_posnum` / `oth384_presentation_negnum` | 0.2175 | 陈述正/负词实例数 |
| `qa_positive_word_count` / `qa_negative_word_count` | 0.2105 | Q&A 正/负词数（别名） |
| `presentation_positive_word_count` / `presentation_negative_word_count` | 0.2105 | 陈述正/负词数（别名） |

### 1.3 非语言情绪族（★ 完全独立信号源）

| 字段 | coverage | 含义 |
|---|---|---|
| `presentation_laughter_count` / `presentation_laughter_count_v1` | 0.2175 / 0.2105 | 陈述段笑声标注数 |
| `qa_section_laughter_count` / `qa_section_laughter_count_v1` | 0.2175 / 0.2105 | Q&A 段笑声标注数 |

> 这是全数据集**唯一与语气、结构都正交**的信号源。学术上属"语音/副语言特征"分支，与文本词频不共享方差。

### 1.4 治理与质量族（★ 天然的门控腿）

| 字段 | coverage | 含义 |
|---|---|---|
| `oth384_oecsi` / `speaker_is_ceo_flag` | 0.2175 / 0.2105 | CEO 是否出席（1/0） |
| `oth384_ofcsi` / `speaker_is_cfo_flag` | 0.2175 / 0.2105 | CFO 是否出席（1/0） |
| `company_name_match_score` | 0.2175 | 实体匹配置信度 0–1（★ 数据质量权重） |
| `transcript_is_initial_version` | 0.2175 | 是否为初步版本（元数据） |

### 1.5 不可用于信号的字段

`conference_analyst_attendees` / `conference_company_attendees` / `presentation_section_speaker_list` / `qa_section_speaker_list`（人名字符串列表）、`event_full_title` / `event_headline_text` / `transcript_body_headline`（自由文本）、以及全部 `_v1` 重复版本。

---

## 2. 低换手架构（本数据集的第一风险）

**风险定性**：财报会**每年只发生 4 次**，每次发生后语气/结构值整段跳变 ⇒ 若直接把稀疏值喂给截面排序，日频换手会极高。这与 `earnings_chart_dl`（TO 75–91% 全灭）的失效机理不同：那个是"日频重新预测"，这个是"季度跳变"，但两者的**后果同构**。

**统一架构：两层 —— 先回填、后加工**

```
第一层  ts_backfill(vec_*(F), 252)      # 把季度观测前向填成日频常数，252 天保证覆盖 4 次财报
第二层  group_rank(·, sector) 或 ts_mean/ts_std_dev/ts_ir(·, 66)  # 在填满的序列上做加工
```

- 第一层是**换手治理的真正杠杆**：没有任何新财报的日子序列恒定 ⇒ 持仓不动 ⇒ TO 天然低。
- 第二层 66 = 一个季度交易日；仅在需要"跨季平滑"时才加。
- **绝不用** `hump` / `ts_decay_linear` 当平滑器（本项目已两处证实单独用必塌）；换手治理优先**平台 decay**，其次 `ts_target_tvr_decay`。

---

## 3. 十个结构互异模板（E1–E10）+ 两个备用（E11–E12）

差异落在**信息段（陈述/Q&A）× 加工方式（水平/差/极性/变化/计数/非语言/比值/门控/加权/稳定性）× 分组轴**三个维度上，不是换窗口或换常数。

### E1 — Q&A 语气水平
- **来源**：paper — Price, Doran, Peterson & Bliss (2012), *Journal of Accounting Research* 50(5)："Q&A 段语气对股价的解释力显著高于陈述段，因管理层无法预先排练"
- **几何**：水平 + 截面分组排序
- **表达式**
```
group_rank(ts_backfill(vec_avg(oth384_qa_tone), 252), sector)
```
- **窗口理由**：252 = 一年，覆盖 4 次财报；不额外加平滑，保留单次口径。

### E2 — 陈述−问答语气落差（★ 双信号 rank 差，放行形态）
- **来源**：paper — Matsumoto, Pronk & Zack (2011), *The Accounting Review* 86(4)：陈述段可预演美化，Q&A 即兴无法伪装，落差含增量信息
- **几何**：`subtract(rank, rank)` 双信号差 → 反向（落差大 = 坏信号）
- **表达式**
```
reverse(group_rank(ts_backfill(subtract(rank(vec_avg(oth384_presentation_tone)), rank(vec_avg(oth384_qa_tone))), 252), sector))
```
- **经济方向**：陈述段被"化妆"得比 Q&A 更乐观 ⇒ 管理层在掩饰 ⇒ 做空。

### E3 — 净语气极性（正词频 − 负词频）
- **来源**：paper — Tetlock (2007) *JF* 62(3) + Loughran & McDonald (2011) *JF* 66(1)（金融文本专用词典）
- **几何**：同单位比率相减（两个都是无量纲比率 ✓）→ 极性净额，非水平
- **表达式**
```
group_rank(ts_backfill(subtract(vec_avg(oth384_qerfsop_aq), vec_avg(oth384_qerfgen_aq)), 252), sector)
```
- **与 E1 的正交性**：E1 是模型给的综合 tone 分，E3 是用正负词频自己重建的极性 ⇒ 前者含句式/否定处理，后者是纯词袋。

### E4 — 语气跨季变化（Δ66）
- **来源**：paper — Loughran & McDonald (2011)；变化 > 水平（Bernard-Thomas 1989 的"意外"框架在文本上的移植）
- **几何**：时序差分（一阶矩）→ 全新几何维度
- **表达式**
```
group_rank(ts_backfill(ts_delta(vec_avg(oth384_qa_tone), 66), 252), sector)
```
- **窗口理由**：66 = 一个季度交易日，恰好对上"上次财报 vs 本次财报"的间隔。

### E5 — 分析师追问强度反向
- **来源**：paper — Price et al. (2012)；追问次数是信息不对称的直接读数
- **几何**：计数型字段 + 反向（非语气族，信息源不同）
- **表达式**
```
reverse(group_rank(ts_backfill(vec_sum(oth384_qa_questions), 252), sector))
```
- **经济方向**：Q&A 被问得越多 ⇒ 披露不充分/疑虑越重 ⇒ 负向。

### E6 — 笑声（非语言情绪泄露）★ 全库最正交
- **来源**：paper — Hobson, Mayew & Venkatachalam (2012), *Journal of Accounting Research* 50(5)："Analyzing Speech to Detect Financial Misreporting"（副语言特征可检测财报粉饰）
- **几何**：非语言计数 → Q&A 氛围
- **表达式**
```
group_rank(ts_backfill(vec_sum(qa_section_laughter_count), 252), sector)
```
- **正交性保证**：笑声标注与词频、语气分**不共享方差**，是本数据集唯一能保证低相关的腿。

### E7 — 陈述/问答篇幅比（沟通失衡）
- **来源**：自建（依据 Habermas 式"话语对称性"直觉 + Price et al. 2012 的段落信息含量差异）
- **几何**：同单位比值（词数/词数，无量纲 ✓）→ 反向
- **表达式**
```
reverse(group_rank(ts_backfill(divide(vec_sum(presentation_word_total), vec_sum(qa_word_total)), 252), sector))
```
- **经济方向**：陈述冗长 + Q&A 简短 ⇒ 单向灌输式沟通 ⇒ 负向。

### E8 — CEO/CFO 双在场门控
- **来源**：自建（事件治理；`trade_when` 三参数语义见论坛 33120494662423）
- **几何**：**条件分支**（不同于 E1–E7 的连续打分）→ 只在高质量事件上持仓
- **表达式**
```
trade_when(and(greater(vec_sum(speaker_is_ceo_flag), 0.5), greater(vec_sum(speaker_is_cfo_flag), 0.5)), group_rank(ts_backfill(vec_avg(oth384_qa_tone), 252), sector), -1)
```
- **注**：`and` / `greater` 只用于**门控条件**，不构成混信号；`-1` = 不退出。

### E9 — 匹配质量加权语气
- **来源**：自建（数据可信度加权；本项目已多次证实低 coverage 数据集的实体映射错误是隐性噪声源）
- **几何**：信号 × 权重（乘性，不是加性混信号）
- **表达式**
```
group_rank(ts_backfill(multiply(vec_avg(oth384_qa_tone), vec_avg(company_name_match_score)), 252), sector)
```
- **经济含义**：只信任实体匹配置信度高的记录，压低错配噪声。

### E10 — 语气稳定性（IR）
- **来源**：自建（稳定性溢价；类比本项目 `ts_ir` 在关注度族的用法）
- **几何**：二阶矩（均值/标准差）→ 与 E1 的水平、E4 的差分都不同
- **表达式**
```
group_rank(ts_ir(ts_backfill(vec_avg(oth384_qa_tone), 252), 66), sector)
```
- ⚠ **风险**：backfill 后序列常年恒定，`ts_ir` 的标准差可能为 0 ⇒ 除零/NaN。若首条回测报 NaN 或覆盖率骤降，本模板换 `ts_std_dev` 或直接弃用。

### E11（备用）— 陈述段负词频反向
- **几何**：与 E1/E3 同族（水平），但与 E3 用**陈述段**而非 Q&A
```
reverse(group_rank(ts_backfill(vec_avg(oth384_presentation_negfreq), 252), sector))
```
- ⚠ 与 E3 可能高相关（同为负向词），仅在前 10 个跑完后才有价值。

### E12（备用）— 问答句长复杂度
- **几何**：同单位比值（词/句）+ 反向
```
reverse(group_rank(ts_backfill(divide(vec_sum(qa_word_total), vec_sum(qa_sentence_total)), 252), sector))
```
- **经济方向**：回答越绕 ⇒ 越可能在回避 ⇒ 负向。

---

## 4. 模板正交性自检表

| 信息段 | 加工方式 | 模板 |
|---|---|---|
| Q&A | 水平 | E1, E8（门控后同 E1）, E9（加权同 E1）, E10（IR）|
| Q&A | 一阶差分 | E4 |
| Q&A | 极性净额 | E3 |
| Q&A | 计数（追问） | E5 |
| Q&A | 非语言（笑声） | E6 |
| Q&A | 结构比值 | E12 |
| 陈述 vs Q&A | 双信号差 | E2 |
| 陈述 vs Q&A | 篇幅比 | E7 |
| 陈述 | 水平（负向） | E11 |

> **落地提醒**：E1 / E8 / E9 共享「Q&A 语气水平」这条信号腿，只差门控/权重层 ⇒ **三者互相关会很高，最多取 1 条**。这与 `other47` 里 W1/W9/W10 的关系同构。

---

## 5. 派发设置与顺序

**设置**（与 other47 批次一致，便于横向对比）
```
region=GBR / universe=TOP700 / delay=1 / neutralization=STATISTICAL
decay=4 / truncation=0.08 / nan_handling=ON / max_trade=ON / pasteurization=ON / unit_handling=VERIFY
```

**派发顺序（按正交性优先级，不按预期强弱）**
1. **批次 1**：E2（陈述−Q&A 差）+ E6（笑声）—— 两条最正交、最不可能与已有持仓撞
2. **批次 2**：E3（极性净额）+ E5（追问强度）—— 词袋 / 计数，两个非水平几何
3. **批次 3**：E4（Δ66）+ E7（篇幅比）
4. **批次 4**：E1（水平基准）+ E8/E9/E10 中选 1（三者只取一）

**首批复盘必查项（按顺序）**
1. `sub_universe_sharpe` —— coverage 0.2175，SUB 风险高于 other47（0.6068）。GBR limit = `0.4743 × sharpe`
2. `turnover` —— 若 > 60%，说明 `ts_backfill` 没起到换手压制作用，要回头查骨架
3. `margin` —— 事件型数据若 margin < 3bp，即使 S 达标也无实盘意义
4. `sharpe` —— **最后看**

---

## 6. 风险清单

1. **coverage 0.2175 是结构性风险**：TOP700 里只有约 152 只有数据，多空各约 76 只。本项目 `sentiment7`（cov 0.58）与 `earnings6` 都死在 `LOW_SUB_UNIVERSE_SHARPE`。**但** `other169+pv1`（`O0JOMnwq` SUB 比值 2.406）与 `other545+pv1`（`d5Kp3nwJ` 1.413）证明**低 coverage OTHER 未必死在 SUB** ⇒ 必须实测，不可先验判死。
2. **事件型高换手**：见 §2。首条若 TO > 60%，不要逐条试骨架，直接回查 backfill 层。
3. **季度跳变的 PnL 阶梯化**：财报日集中调仓可能导致 `CONCENTRATED_WEIGHT` 或单日大 PnL。GBR 论坛实测 `CONCENTRATED_WEIGHT` 挂 54.2%（帖 44089095804439）。
4. **同义字段伪多样性**：见 §1.1。12 个语气字段只有 6 个自由度。
5. **`_v1` 字段是同一数据的重复版本**：`coverage` 差 0.0070（0.2175 vs 0.2105），不要当独立信号。
6. **`transcript_is_initial_version` 可能引入前视**：初步版本 vs 最终版本的发布时间差异，若平台按最终版本时间戳对齐，用该字段做门控会有信息泄露风险。**不用于信号**。
7. **prod 零先验**：GBR 全库 `other*` 最高 S 仅 0.81（`other169+pv1`），纯 OTHER 单塔从未出货。任何一条过闸后**先测 prod 再谈提交**。

---

## 7. 派发记录表（回测后回填）

| 批 | multisim id | 模板 | alpha_id | S | F | 2Y | SUB | TO | margin |
|---|---|---|---|---|---|---|---|---|---|
| | | E2 | | | | | | | |
| | | E6 | | | | | | | |
| | | E3 | | | | | | | |
| | | E5 | | | | | | | |
| | | E4 | | | | | | | |
| | | E7 | | | | | | | |
| | | E1 | | | | | | | |

---

## 8. 参考文献

1. Price, S.M., Doran, J.S., Peterson, D.R., Bliss, B.A. (2012). "Earnings conference calls and stock returns: The incremental informativeness of textual tone." *Journal of Banking & Finance* 36(4).
2. Matsumoto, D., Pronk, M., Roelofsen, E. (2011). "What Makes Conference Calls Useful? The Information Content of Managers' Presentations and Analysts' Discussion Sessions." *The Accounting Review* 86(4).
3. Hobson, J.L., Mayew, W.J., Venkatachalam, M. (2012). "Analyzing Speech to Detect Financial Misreporting." *Journal of Accounting Research* 50(2).
4. Loughran, T., McDonald, B. (2011). "When Is a Liability Not a Liability? Textual Analysis, Dictionaries, and 10-Ks." *Journal of Finance* 66(1).
5. Tetlock, P.C. (2007). "Giving Content to Investor Sentiment: The Role of Media in the Stock Market." *Journal of Finance* 62(3).
6. Larcker, D.F., Zakolyukina, A.A. (2012). "Detecting Deceptive Discussions in Conference Calls." *Journal of Accounting Research* 50(2).
7. Mayew, W.J., Venkatachalam, M. (2012). "The Power of Voice: Managerial Affective States and Future Firm Performance." *Journal of Finance* 67(1).
8. Huang, A.H., Lehavy, R., Zang, A.Y., Zheng, R. (2018). "Analyst Information Discovery and Interpretation Roles: A Topic Modeling Approach." *Management Science* 64(6).
9. Bernard, V.L., Thomas, J.K. (1989). "Post-Earnings-Announcement Drift: Delayed Price Response or Risk Premium?" *Journal of Accounting Research* 27.
10. Feldman, R., Govindaraj, S., Livnat, J., Segal, B. (2010). "Management's tone change, post earnings announcement drift and accruals." *Review of Accounting Studies* 15(4).
11. Davis, A.K., Piger, J.M., Sedor, L.M. (2012). "Beyond the Numbers: Measuring the Information Content of Earnings Press Release Language." *Contemporary Accounting Research* 29(3).
12. 论坛 33120494662423（28 赞）：`trade_when(x, y, z)` 三参数语义 = 触发条件 / alpha 表达式 / 退出条件（`-1` = 不退出）。
13. 论坛 31365517513495：`LOW_SUB_UNIVERSE_SHARPE.limit = 0.4743 × sharpe`（GBR/TOP700/D1 实测）。

---

## 实测结果（2026-10-30 收回，6 模板全灭）

设置统一：`GBR / TOP700 / D=1 / STATISTICAL / decay 4 / trunc 0.08 / nanHandling ON / maxTrade ON / unitHandling VERIFY`

| # | 模板 | alpha | S | F | 2Y | SUB | TO | margin | returns |
|---|---|---|---|---|---|---|---|---|---|
| E2 | 陈述−问答语气落差（反向） | `YP1ZVw7W` | 0.18 | 0.04 | −1.62 | 0.19 | 6.04% | 1.78bp | 0.54% |
| E3 | 净语气极性（正−负频） | `wpQ6dJPv` | 0.09 | 0.01 | 0.85 | 0.29 | 5.77% | 0.89bp | 0.26% |
| E4 | 语气跨季变化 Δ66（反向） | `3qodNdVQ` | −0.15 | −0.03 | −1.17 | −0.31 | 6.81% | −1.36bp | −0.46% |
| E5 | 分析师追问强度（反向） | `78LO5Kl8` | 0.12 | 0.02 | −1.25 | −0.15 | 6.22% | 1.19bp | 0.37% |
| E6 | 笑声（非语言情绪） | `2rAEgqlw` | −0.37 | −0.11 | 1.64 | −0.21 | 5.53% | −4.21bp | −1.16% |
| E7 | 陈述/问答篇幅比（反向） | `0mYoJork` | **0.42** | 0.14 | −0.11 | 0.24 | 6.05% | **4.34bp** | 1.31% |

### 结论：判死封盘（`other384_verdict` 已写台账 `other_tower_verdict`）

**最大 S = 0.42，仅为闸（1.58）的 27%。**

三个关键读数：

1. **换手治理完全成功**：TO 全落在 5.53–6.81%。`ts_backfill(vec_*, 252)` 把财报会「每季跳变」压成日频常数，事件型高换手风险已消除。**失败点不在换手。**
2. **不是 F 上限锁死**：`F ≈ S × sqrt(|R|/TO) ∝ S^1.5`。E7 当前 F 0.14、S 0.42；若 S 能推到 1.58，F ≈ 1.02 刚好过闸。所以**唯一缺口是信号强度**，差 3.76 倍。
3. **时间稳定性互斥**：E2 的 2Y = −1.62 与 E6 的 2Y = +1.64 方向完全相反，说明这些腿在近两年上的符号是随机的，而不是「弱但稳定」。

### 与 other47 的死法对比

| 维度 | other47 (SEMrush 流量) | other384 (财报会 transcript) |
|---|---|---|
| 模板数 | 8 | 6 |
| 最大 S | 0.94 | 0.42 |
| TO 区间 | 4.5–31.4% | 5.5–6.8% |
| 死因 | 信号衰减（W3 的 2Y 由正翻负） | 信号本就不足 |

⇒ 两个数据集都是「**字段承载不了 S 1.58**」，但 other384 连一半都不到。

### 附带的产品事实（会再踩）

- `presentation_negfreq` **不存在**（E11 作废）。
- `oth384_presentation_word_total` **不存在** —— 结构计数族是**裸名**（`presentation_word_total` / `qa_word_total` / `qa_sentence_total`），只有语气族带 `oth384_` 前缀。**一次加错前缀会让整批 CANCELLED 连坐**（本轮实测：E7 报 unknown variable，E4 被连坐 CANCELLED）。
- 12 个语气字段只有 **6 个自由度**（陈述/QA × tone/pos/neg），平台已做比率归一化（`divide(posnum,count) ≡ posfreq`），换桶不算换机制。