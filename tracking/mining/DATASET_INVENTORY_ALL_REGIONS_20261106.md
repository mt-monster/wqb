# 跨区数据集全表清点（2026-11-06）—— 纠正「本面已穷尽」的系统性误判

## 一、为什么写这份文件

本 campaign 到目前为止所有「某区某 category 已穷尽 / 已封盘」的结论，都建立在本地缓存 `tracking/mining/field_coverage_{REGION}_d1_{UNIVERSE}.json` 之上。这些缓存**只覆盖曾经查询过的数据集**，不是平台的完整清单。

本轮用 `get_datasets` 实取平台全表后，发现缓存严重低估：

| region | 平台数据集总数 | OTHER 类 | 此前本地认知 |
|---|---:|---:|---|
| EUR (TOPCS1600) | 173 | **36** | 只列了 7 个 OTHER |
| USA (TOP3000) | 286 | **56** | 只测过 4 个 OTHER |
| GLB (MINVOL1M) | 138 | 25 | 只测过 3–4 个 |
| ASI (MINVOL1M) | 158 | 27 | 从未按 category 清点 |

**结论**：「EUR/OTHER 已穷尽」「USA/OTHER 四面封盘」这类判断在数据集层面就不成立 —— 不是模板不够，是数据集根本没数完。

## 二、纪律回写（硬约束）

1. 任何「本面已穷尽 / 封盘」的结论，必须先用 `get_datasets(region, universe, delay)` 取平台全表，按 category 分组计数，与本地缓存比对；缓存差额即「未测集合」。
2. `get_datafields` 的 `offset` 参数**不可用**（平台忽略，永远返回前 N 条，`truncated_reason=max_fields_cap`）。评估大集只能用前 200–800 字段的命名网格外推，并在台账里显式标注「只看到前 N 个」。
3. 判死一个数据集需要 ≥6 个结构互异骨架；判死一个 category 面需要先证明该面所有候选数据集都已判死。

## 三、USA / OTHER（56 个，已点亮条件：再提交 1 颗即 2→3）

未测且覆盖较好的候选（字段数 / aC / cov）：

| 数据集 | 字段 | aC | cov | 备注 |
|---|---:|---:|---:|---|
| other596 | 420 | 347 | **0.9796** | 未测，高覆盖 |
| other580 | 403 | 219 | **0.9119** | 未测，高覆盖 |
| other696 | 498 | 1412 | 0.7765 | 未测，偏拥挤 |
| earningscall_embed | 515 | 182 | 0.7596 | 未测 |
| nlp_news_scores | 84 | 68 | 0.9017 | 未测 |
| other685 | 72 | 264 | 0.7225 | 未测 |
| other699 | 19 | 250 | **0.9855** | 个人投资者交易，未测 |
| other546 | 13 | 50 | 0.6630 | 机构网络，未测 |
| us_equity_news | 8 | 171 | **0.9627** | 未测 |
| other623 | 6 | 38 | **0.9866** | 未测 |
| other359 | 10 | 87 | 0.7419 | 未测 |
| forum_sentiment | 13 | 51 | 1.0000 | 未测 |
| filing_sentiment | 21 | 51 | 0.5396 | 未测 |
| other685 / web_traffic_engage | 105 | 604 | 0.4330 | 未测（cov 低） |
| other143 | 126 | **20342** | 0.9974 | 饱和，弃 |

已判死（本 campaign 实测）：`mmp_nlp_sentiment`（8 构造最强 0.69）、`finnews_nlp_scores`（T1 −0.34 / T2 −0.01）、`techindi_model`（P4-P0 F 恒 0.48–0.59）、`sustainable_profit`（10 构造饱和 S1.13）。

## 四、EUR / OTHER（36 个）

详见 `tracking/EUR/eur_other_other455_competitor_net_20261106.md` §七。优先序：other567（已开波）→ acquisition_model（已开波）→ other545 → other315 → other546 → other128 → event_sentiment_signals → other250 → other296 → other635 → equity_forum_data → other384 → stock_search_trends → stock_cluster_dl → workforce_flow_skills。

## 五、GLB / ASI

GLB 138 个（model 39 / other 25 / pv 16 / news 15 / analyst 13 / fundamental 10 / earnings 5 / risk 4 / sentiment 4 / macro 3 / institutions 2 / insiders 1 / socialmedia 1）；GLB 当前 PV 塔 2/3、OTHER 塔 4/3（已点亮）。

ASI 158 个（model 41 / other 27 / news 22 / pv 19 / analyst 13 / fundamental 11 / sentiment 7 / socialmedia 5 / risk 4 / institutions 2 / insiders 2 / imbalance 1 / macro 1 / shortinterest 1 / broker 1 / earnings 1）；ASI 当前 OTHER 塔 2/3，只差 1 颗即点亮，且 **27 个 OTHER 数据集全部未按清单清点过**。

## 六、待补区域

DEU / GBR / KOR / HKG / IND / TWN / JPN / MEA / CHN / AMR 尚未做同样的全表清点；其中 DEU（SHORTINTEREST 2/3）、GBR（PV 2/3、OTHER 1/3）、KOR（PV 2/3）、HKG（PV 1/3）、IND（已 12 类里 8 类点亮）都还需要这一步。