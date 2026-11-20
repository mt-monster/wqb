# news73 — Story by Story Sentiment（KOR / TOP600 / D1）— 判死档案

> 画像：2026-11-17 · `get_datafields(dataset_id=news73, region=KOR, universe=TOP600, delay=1, filter_sharpe=false, 不传 max_fields)`。
> 三重对账：`count=22 == platform_count=22`，`complete=true`。全字段 22/22。
> 归属：平台 `category=news`（未点亮塔）。

## 1. 字段全表（22 个，全 VECTOR，coverage 0.2395–0.269，aC 0–2）

- **全局情绪 9 个**：`globalsent_positivescore`(aC2) / negativescore / fearscore / certaintyscore /
  `finhypescore`(aC1) / finupscore / findownscore / finvolatilescore / uncertainty score
- **逐实体情绪 9 个**：`entitiessent_*partscr`（pos/neg/fear/certainty/finhype(aC2)/finup(aC1)/findown/finvolatile/uncertainty）
- 其它：`djnindustry`/`djnsubject`（行业/主题 tag，编码）、`entitiescounter`（实体数）、`headlines`（文本）

## 2. 判决：**不投入仿真配额（机制层 PROVISIONAL 停投）**

理由（不依赖数据集级 coverage）：
1. **机制与已判死集同族**：22 个字段全是「新闻情绪分」——与 SOP 附录 B 的 **news85 / news84 / news3 / news79**
   （情绪水平、语调、DNN 转移情绪）是同一信息机制；那几集在 KOR 实测 max\|S\| 0.25–0.67 全灭。
   按 §F.1，探针 <10 条**不产生终判死**，此处也无新探针 —— 结论只能是 PROVISIONAL 停投，不得引用为邻接数据集先验。
2. **aC 0–2 = 极冷门**，但冷门 only necessary, not sufficient：W1/W2 两个冷门集（news23/news29）已实测无信号。
3. **coverage 0.269** 只作截面稀疏的佐证，**不作「无数据」判据**（AGENTS.md §8.11 ⑥ fail-closed）。
4. 若将来要翻案：需先跑 field 级探针（`tools/probe/dataset_data_probe.py`）确认 longCount>0，
   再用**不同于情绪水平**的机制（例如「多实体情绪分歧度」，本数据集独有的 entitiessent_* 逐实体分散度）——
   那才构成新机制，而非换窗口重试。

## 3. 归档路径

`tracking/KOR/reference/datasets/news73.md`（本文件，按规范命名）。
