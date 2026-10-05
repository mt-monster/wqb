# USA 空白塔扫描报告 — 2026-10-02

> 目标：为「在不同 category 下累计 10 颗可提交 REGULAR alpha、均匀点塔」寻找新塔入口。
> 方法：论坛调研（短利息/news 模板）+ 冠军骨架 `ts_decay_linear(group_rank(ts_zscore(winsorize(F), W), subindustry), D)` 批量探针。

## 结论速览

| 塔 / 路径 | 数据集 · 字段 | 最优 S | 2Y | SUB | prod | 判定 |
|---|---|---|---|---|---|---|
| **news · USA 情绪** | news18 · `mean_merger_acquisition_sentiment` | **1.70** | 3.08 P | 0.53→0.69 P（winsorize 后 1.58） | **0.7989 ✗** | 拥挤判死 |
| **news · USA 换数据集 B** | news85 · `sentiment_overall_average` | 1.21 | 2.26 P | 0.84 P | **0.9598 ✗** | 拥挤判死 |
| news · USA 换数据集 B | news84 / news_sentiment_transfer | 0.62–0.73 | FAIL | P | — | 弱 |
| **news · GBR 换区 A** | GBR news18 · classifier（零拥挤 a=5） | \|0.51\| | FAIL | — | — | **弱** |
| **news · DEU 换区 A** | DEU news18 · classifier（零拥挤 a=0） | \|0.54\| | FAIL | — | — | **弱** |
| **shortinterest · USA** | shortinterest43 · `shvol/totalvolume` 比值 | \|1.09\| | FAIL | — | — | 弱（且反向） |
| **socialmedia · USA** | twitter_sentiment_l2 · `market_relevance_score_*` | 0.78 | FAIL | — | — | 弱 |
| **sentiment · USA（B 轮）** | other553 · `oth553_p_wordcnt`（财报电话会 NLP） | 1.23 | 2.29 P | 0.76 P | **0.9034 ✗** | 拥挤判死 |
| **insiders · USA（B 轮）** | insider_agg_matrix · `significant_value_2`（a=8） | 1.07 | 1.53 F | 0.44 F | **0.8156 ✗** | 拥挤（可救带） |
| insiders · USA（B 轮） | board_gov_stats · `min_chief_officer_tenure_days` | 0.98 | 1.12 F | 0.80 P | — | 弱 |
| **macro · USA** | macro27 · `mcr27_v2_company_duration_closed`（论坛 124 票帖主角） | 1.03 | **0.79 F** | — | — | **2Y 弱** |
| macro · USA（模板适配后） | mcr27 + `if_else(=0,nan)` + `ts_quantile` | 0.96 | 0.63 F | — | — | 2Y 弱 |
| imbalance · USA | imbalance5 · `imb5_score` | 0.98 | 1.39 F | — | — | 2Y 弱 |
| option · USA | option3 / order_flow_imb | 0.90 | 1.06 F | — | — | 2Y 弱 |
| **sentiment · USA（模板适配）** | 论坛18 分歧度极性 `ts_rank` | **1.07** | 1.93 P | **T=1.58 ✗** | — | 换手爆 |
| sentiment · USA（条件动量） | `ts_mean(if_else(pos−neg>0,ret,0),126)` | 0.03 | — | — | — | 无信号 |

## ★★ 系统性结论：USA 的「LOW_2Y_SHARPE × PROD」双向夹击

- **2Y 强的信号（news18 / news85 / analyst 族，2Y 2.1–3.1）→ prod 全在 0.80–0.96**（平台 REJECT）
- **prod 干净的信号（macro / imbalance / option / socialmedia / shortinterest）→ 2Y < 1.58**（平台 FAIL）

⇒ **在覆盖到的全部 USA 塔与数据集类型上，没有信号能同时过 2Y 闸与 prod 闸。** 这是 USA 对高活跃账户饱和的直接证据。

## 平台算子可用性（实测，重要）

| 算子 | 状态 |
|---|---|
| `to_nan` | **不可用**（Gold 段位无权限；替代 `if_else(x == 0, nan, x)`，实测可用） |
| `ts_max` / `ts_min` | **不可用**（只有 `ts_arg_max`/`ts_max_diff`） |
| `ts_quantile(...,driver=gaussian)` | 可用 |
| `group_neutralize` / `hump` / `reverse` / `densify` | 可用（但 `group_neutralize` 会让换手爆炸） |

## 核心洞察

1. **news「情绪水平」是概念级拥挤因子，不是数据集级。** 换数据集（news18→news85→news84→transfer）无法降低 prod 相关性（0.80→0.96）。
2. **换区（GBR/DEU）虽零拥挤但信号本身弱**（|S|≤0.54）；**拥挤度低 ≠ 有信号**。
3. **骨架必须按 category 语义适配**：sentiment 要区分 `_std`（分歧度）与 `_mean`（水平）；macro 要处理「0 值膨胀」（`to_nan`/`if_else` 把 0 变 NaN 再 backfill，否则 0 被当有效值）。
4. **失败的去相关手段（勿重复）**：`subtract(zscore(A),zscore(B))` → S 崩到 1.2–1.29；`group_neutralize(zscore,...)` → S 崩到 −0.2、换手 0.55。


## 可行的下一步（强烈建议换战场）

- **★ 转其他区域（GBR / DEU / ASI / AMR 等用户零提交区）** —— 那里 prod 池更小、无需赢拥挤战，**任何过闸 alpha 都能点亮新塔**，是性价比最高的路径。
- (a) 提交队列候选 `O08EjLVp` —— 全闸通过（S 2.45 / F 1.55 / 2Y 2.55 / prod 0.5626），但同 family、MODEL 塔已亮。
- (b) 在 USA 继续找"与既有池正交"的信号 —— 难度高，需从零反推。

## 附：本轮已落地提交
`d51A3nqY`（USA/TOP2000/D1/MODEL，S 2.45/F 1.47/prod 0.491）→ **ACTIVE**。累计 5 颗。

