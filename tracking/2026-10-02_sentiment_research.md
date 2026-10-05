# SENTIMENT 塔 USA — 骨架原理 / category 适配 / 实测结论（2026-10-02）

## 1. 骨架原理（回答用户提问）

统一骨架：`ts_decay_linear(group_rank(ts_zscore(ts_backfill(F,252),60),subindustry),200)`

| 算子 | 作用 | 语义 |
|---|---|---|
| `ts_backfill(F,252)` | 用最近有效值回填 | 处理稀疏/事件字段 |
| `ts_zscore(·,60)` | 60 日时序标准化 | **"当前值相对自身历史的偏离"**（异常/意外） |
| `group_rank(·,subindustry)` | 行业内截面排序 | 剥离行业效应，输出 0–1 秩 |
| `ts_decay_linear(·,200)` | 线性衰减平滑 | 压换手 |

⇒ 本质是 **「时序自标准化 + 截面排序」的"水平信号"**。
**它的局限**：把 `_std`（分歧度）、`_mean`（水平）、`_conf`（置信度）一视同仁——**对语义不同的字段不做区分，是错的**。

## 2. Category 适配（论坛 + 外部文献）

**论坛高票模板**
- **sentiment 模板（18 票）**：`group_neutralize(reverse(ts_max(<snt21_pos> − <snt21_neg>, days)), group)`
  - ⚠ 关键：`snt21_POS/NEG` = 正/负面情感的**标准差（分歧度）**，非水平值 ⇒ 须用 `_std` 字段
  - 逻辑：净分歧度高＝过度炒作 → 反向做空；行业中性化剥离"科技股舆论天然波动大"的偏差
- **条件动量模板（50 票）**：`ts_mean(if_else(<condition>, returns, 0), days)`
  - 只累计"情绪条件成立日"的收益；帖子称 EUR 明显、其他区弱

**外部金融文献**
- **BBVA/GDELT 五因子**：Tone / Optimism / **Attention（新闻数，与收益负相关）** / **Tone Dispersion（文章情绪 std，负相关）** / Emotional Polarity
- **开源证券**：**「过去 N 日舆情均值的变化量」**＝强因子（多空 IR 2.0–2.3），**ICIR 为负 ⇒ 情绪变化是反向的**（回看 20 日）
- **CoSENT（2026）**：情绪**共动/背离**（个股 vs 截面组的条件概率）比情绪水平更有预测力；**下行共动/背离最强**

## 3. 平台算子坑（重要）

**平台无 `ts_max` / `ts_min`**（`operator_audit` 实测 live 算子只有 `ts_arg_max`/`ts_max_diff`/`ts_mean`/`ts_rank`/`ts_quantile`）。
⇒ 论坛模板里的 `ts_max(...)` 会报 `unknown operator`，**已替换为 `ts_mean` / `ts_rank`**。（本地 `src/wqb/config.py` 声明有 ts_max，与平台不一致 —— 待修。）

## 4. 适配结构实测（25 条，sentiment21/22）

| 结构 | 主 Sharpe | 换手 | 2Y | 判定 |
|---|---|---|---|---|
| 论坛18 分歧度极性 + `ts_rank` | **1.07** | **1.5785 ✗** | 1.93 P | 换手爆炸（无衰减） |
| 论坛18 分歧度极性 + `ts_mean(5)` | 0.63 | 0.386 | 1.35 F | 弱 |
| 分歧度 rank（reverse pos_std−neg_std）+ decay | 0.57–0.64 | 0.018 | 0.88–1.01 F | 弱 |
| **条件动量 `ts_mean(if_else(pos−neg>0, returns,0),126)`** | **0.03** | 0.02 | — | **无信号** |
| 条件动量 group_rank/sum | 0.20 | 0.02 | — | 无信号 |

## 5. 结论

把论坛模板按 category 语义适配后，**USA sentiment 仍无可用信号**：
- 分歧度模板有 Sharpe 但**换手爆炸**（group_neutralize/ts_rank 无衰减层，T=1.58）；
- 条件动量模板在 **USA 完全不成立**（S≈0），与帖子"EUR 明显、其他区弱"一致。

⇒ **SENTIMENT 塔 USA 判弱**。与同日其他塔（news 拥挤 0.80–0.96 / shortinterest 弱 / socialmedia 弱 / insiders 弱或拥挤）合起来，**USA 几乎全域不可点**。
