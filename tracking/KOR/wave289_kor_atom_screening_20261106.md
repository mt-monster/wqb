# wave289 · KOR ATOM 数据集筛选排除表（2026-11-06）

## 背景
目标 10 颗 KOR 单数据集 ATOM REGULAR alpha。本文件记录**逐数据集筛选**的结论与证据，
避免重复开波。判据：先查该 category 参考页判死表 → 未判死的才派探针。

## 一、本轮新排除（有实测或判死证据）

| 数据集 | category | 结论 | 证据 |
|---|---|---|---|
| `fund_holdings_panel` | institutions | **判死（引用）** | `KOR-FUND-HOLDINGS-PANEL-DEAD`：do not probe again，event-aggregate flow 字段是噪声 |
| `institutions6` | institutions | **判死（引用）** | 跨区结论：institutions6 作主信号判死（KOR 红榜） |
| `insider_feats` | other | **判死（引用）** | `KOR-INSIDER-PROD-SATURATED`：30+ 条 prod 全 ≥0.75，地板 0.7185 不可修 |
| `risk59` | risk | **判死（引用）** | 证券借贷族判死；单腿全字段普查最优仅 **1.04**；16 字段全 VECTOR |
| `risk60` / `risk71` | risk | **判死（引用）** | `KOR-RISK60-CROWDDING-NOSIGNAL` / `KOR-RISK71-RESIDUAL-REVERSAL-2Y-DEAD` |
| `analyst11` | analyst | **判死（引用）** | ESG 族，四支柱实测 S **−0.19 ~ 0.01** |
| `other455` | other | **排除（族级判死）** | 1500 字段几乎全是 n2v/roam 的 PCA 分量与聚类标签，三族全部点名判死（NETWORK-EMBEDDING / GROUP-CLUSTER / RELATION-EMBED-DRIFT） |
| `news_sentiment_transfer` | sentiment | **判死（本轮实测）** | 16 条结构互异模板（12 骨架 × 两方向），最高 S **0.72**；见 wave288 |
| `analyst16` | analyst | **判死（本轮实测）** | 8 条模板最高 S **0.47**（SUE），其余 0.14–0.28；换手 0.85–1.47（VECTOR 事件型天然高换手） |

## 二、analyst16 实测明细（`2t10jA2EH4rmbBKbrXmaXqY`，8/8）

| alpha | S | F | TO | 模板 |
|---|---:|---:|---:|---|
| `YP18ga7A` | **0.47** | 0.14 | 0.85 | SUE 分数 |
| `e75Nxa3p` | 0.28 | 0.04 | 1.17 | 修正动量×分歧度（analyst10 骨架迁移） |
| `qMLO67jO` | 0.26 | 0.04 | 1.28 | 共识后分歧度×覆盖家数 |
| `LLMEdKdM` | 0.14 | 0.04 | **0.08** | 55d 平滑分歧度（唯一低换手，但无信号） |
| `vR1ZvANb` | -0.03 | 0.00 | 1.08 | 覆盖家数 |
| `j2Yora69` | -0.17 | -0.02 | 1.47 | 评级动量 66d |
| `58ErkJkn` | -0.25 | -0.04 | 1.08 | 分歧度水平（取负） |
| `QPvO907M` | -0.26 | -0.04 | 1.07 | high−low 区间（取负） |

**归因**：analyst10 的骨架（250 日修正动量双秩积）迁移到 analyst16 后 S 从 1.94 掉到 0.28
⇒ **该机制依赖 analyst10 特有的预测盈余字段（`*_pred_surps_v1`），不可跨数据集搬运**。
analyst16 的字段是事件型 VECTOR（结构变更/口径调整），换手天然高，不适合做 ATOM 主信号。

## 三、KOR 金字塔点亮现状（D1）

| 类别 | 已提交数 | 状态 |
|---|---:|---|
| fundamental | 3 | **已点亮**（不选） |
| model | 3 | **已点亮**（不选） |
| shortinterest | 4 | **已点亮**（不选） |
| analyst | 2 | 可挖（analyst_consensus/analyst11 死，analyst_base_ref 0.63，analyst9 1.09） |
| pv | 2 | 可挖 |
| other | 1 | 可挖（但大集全判死） |
| earnings / imbalance / institutions / macro / news / socialmedia / sentiment / risk / insiders | 0–1 | 绝大多数数据集已判死或实测弱 |

## 四、尚未探测的残余目标（候选池，优先级降序）

1. `analyst_factor_signals`（59 字段 / cov .577 / uC113）— 字段名即因子信号，未探
2. `analyst9`（48 字段 / cov .567）— 台账已知 best 1.09，离 1.58 差 0.49
3. `analyst46`（6 字段 / cov .421）、`analyst81`（5 字段 / cov .265）— 字段太少
4. `mmp_nlp_sentiment`（521 字段 / cov .619 / 仅 80 条 alpha）— 未探，但属情绪族
5. `news21`（13 字段 / cov .744）、`news7`（56 字段 / cov .633）、`news85`（23 字段 / cov .633）
6. `acquisition_model`（15 字段 / cov **.994**）、`equity_forum_data`（6 字段 / cov .895）
7. `other546`（10 字段 / 仅 9 条 alpha）、`other78`（11 字段 / cov .793）
8. `risk88`（64 字段 / cov .973）、`risk72`（5 字段）
9. `earnings3`（8 字段 / aC2624 极拥挤）、`imbalance5`（2 字段）、`macro63`（1 字段）

## 五、结论
KOR 的 ATOM 空间已高度枯竭：**26 个 other 数据集 + 17 个 analyst + 6 sentiment + 25 news + 7 risk
+ 1 earnings + 1 imbalance + 2 institutions + 2 macro + 2 socialmedia** 逐类筛过后，
有实测或判死证据排除的已占绝大多数。剩余候选多为「字段数 <15」或「已属情绪/新闻负先验族」。

现实产出预期：**KOR 单区可交付 3–5 颗全闸 ATOM alpha**，而非 10 颗。
