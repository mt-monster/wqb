# 用户指定六数据集探索（2026-11-10 12:2x）

用户指令：每个 category 各探一个数据集 —— ANALYST `analyst10` / FUNDAMENTAL `fundamental23` /
MODEL `model354` / OTHER `order_book_imbalance` / PV `continuation_score` / SENTIMENT `sentiment33`。

## 一、平台核实结果（MCP `get_datafields`，region=DEU / TOP500 / delay=1）

| 数据集 | category | DEU 是否存在 | 字段数 | 类型 | cov>0 字段 | maxcov | 状态 |
|---|---|---|---:|---|---:|---:|---|
| **analyst10** | analyst | ✅ | 53 | MATRIX 40 / VECTOR 8 / SYMBOL 5 | **0 / 53** | **0** | meta cov=0，**待探针验真** |
| **fundamental23** | fundamental | ❌ **不存在** | **0** | — | — | — | `count=0, platform_count=0` |
| **model354** | model | ❌ **不存在** | **0** | — | — | — | `count=0, platform_count=0` |
| **order_book_imbalance** | other | ✅ | 256 | VECTOR 256 | 256 / 256 | 0.2329 | **已实测判死（波 AE）** |
| **continuation_score** | pv | ✅ | 560 | MATRIX 560 | **0 / 560** | **0** | meta cov=0，**待探针验真** |
| **sentiment33** | sentiment | ✅ | 255 | VECTOR 255 | **255 / 255** | **0.3258** | **本轮唯一真实新候选** |

### 关键事实
1. **fundamental23 与 model354 在 DEU 平台不存在**（不是 cov=0，是 `count=0`）。
   本地 172 集目录也无这两个 id ⇒ 无法在 DEU 探索，需换 id 或换区（换区受 goal 约束）。
2. **analyst10 / continuation_score 的 cov 全为 0** —— 按 skill Phase D.6，
   `coverage=0` 可能是 **meta 造假**（字段真实存在可回测），也可能是真空集，
   **两者 cov 长得一样，只能靠探针仿真 + 逐年 longCount 判别** ⇒ 已派探针。
3. **sentiment33 是唯一有真实覆盖的新数据集**（255 字段全 VECTOR，cov 0.32），
   本轮从未测过 ⇒ 值得深挖；但 cov 0.32 偏低，需验「近十年是否都有数据」。
4. **order_book_imbalance 已在波 AE 实测判死**：8 条（auction_order_imbalance_pct_auction /
   mean_absolute_bid_ask_spread / quote_to_trade_ratio / ebbo_execution_to_order_ratio /
   closing_auction_dislocation_last / percentage_cancelled_ebbo_orders / bid_order_volume_deleted）
   S -0.48~+0.50、符号混乱 ⇒ 真噪声；且正反成对 lc 160 vs 290 ≈ 1:2 ⇒ 样本集分裂（判据 MQ），
   非方向问题。**不必重测**。

## 二、sentiment33 字段结构（唯一新候选）

255 字段全 VECTOR，按前缀分族：

| 字段族 | 数量 | 说明 |
|---|---:|---|
| `snt33_sefke1v1_fkw1` | 44 | SEFKE 模型 v1，关键词窗口 1 |
| `snt33_sefke1v1_fkw5` | 44 | 关键词窗口 5 |
| `snt33_sefke1v1_fkw4` | 41 | 关键词窗口 4 |
| `snt33_sefke1v1_fkw2` | 39 | 关键词窗口 2 |
| `snt33_sefke1v1_fkw3` | 39 | 关键词窗口 3 |
| `sentiment_model7_score1` | 5 | 情绪抽取方法 7 |
| `sentiment_model9_score4/5/3` | 11 | 方法 9 |
| `sentiment_model6_negative` | 3 | 方法 6 负向 |

高使用量字段（uc 最高）：
- `snt33_sefke1v1_fkw1_method_3_neg`（uc 5，cov 0.3258）— 文档级负向情绪加权均分
- `snt33_sefke1v1_fkw1_method_3_filtered_neg`（uc 4）— 额外 NLP 过滤后的负向分
- `snt33_sefke1v1_fkw1_method_2_filtered_neg`（uc 3）
- `sentiment_model7_score1_fkw4`（uc 3，cov 0.3214）

**机制**：文档级情绪分（正/负/客观三向 × 9 种抽取方法 × 5 个关键词窗口）。
与已判死的 RavenPack 事件级情绪（news104/18/50）**不同源**（SEFKE 模型 vs RavenPack），
且是**文档级加权均分**而非单条事件 ⇒ 值得独立测一轮。

## 三、已派探针（sim `3ufEWZ2pC52Zb9v1gF5dYPCC`，6 条）

目的：用 `longCount` 逐年判别 analyst10 / continuation_score 的 cov=0 是 meta 造假还是真空集，
并测 sentiment33 的覆盖起始年。

| # | 数据集 | 表达式 |
|---|---|---|
| 1 | analyst10 | `group_rank(ts_mean(ts_backfill(anl10_smartest_tbv_ff,132),22), subindustry)` |
| 2 | analyst10 | `group_rank(ts_mean(ts_backfill(anl10_analyst_innovation_tbv_innovation_score_fy1,132),22), industry)` |
| 3 | continuation_score | `group_rank(ts_mean(ts_backfill(ascending_channel_similarity_dispersion,132),22), subindustry)` |
| 4 | continuation_score | `group_rank(ts_mean(ts_backfill(avg_similarity_bullish_flag,132),22), industry)` |
| 5 | sentiment33 | `group_rank(ts_mean(ts_backfill(vec_avg(snt33_sefke1v1_fkw1_method_3_neg),132),22), subindustry)` |
| 6 | sentiment33 | `group_rank(ts_mean(ts_backfill(vec_avg(sentiment_model7_score1_fkw4),132),22), industry)` |

设置：DEU/TOP500/delay1/decay4/FAST/trunc0.08/nanON。preflight valid（1 条 soft 警告为 API 抖动）。

**判读标准**：`longCount > 0` 且覆盖近十个完整自然年 ⇒ 有供数可继续挖；
`longCount = 0` ⇒ 真空集，判死。

## 四、并发状态

- 波 AN（借券 2021 专项，sim `3j6Xeb1kz4WTbu232ZcS8po`）仍在平台队列（progress 0.1，全局拥堵）
- 本探针占第 2 槽（cap=2，符合并发纪律）
