# NEWS 塔数据集级判死（P4/P5 收尾）· 2026-11-07

## 结论
**KOR/D1/TOP600 的 NEWS category（news50、news38）在标准 KOR 设置档下 S 天花板 ≈ 0.40**，与阈值 1.58 相差近 4 倍。
按「数据集级 prod 体检 → 深挖/封盘」打法升级为**塔级判死**：两批共 6 条 alpha、2 个独立数据集、5 种不同几何，全部 ≤0.40。

## 实测明细

| alpha | 数据集 | 表达式 | S | F | 2Y | sub | TO | raFail |
|---|---|---|---:|---:|---:|---:|---:|---:|
| 2rA6oWe8 | news50 | group_rank(vec_avg(composite_story_sentiment_score_d0), subindustry) | 0.40 | 0.12 | 1.10 | 0.43 | 0.3438 | 3 |
| LLMzYr36 | news50 | group_rank(vec_stddev(composite_story_sentiment_score_d0), subindustry) | 0.20 | 0.05 | 1.17 | 0.25 | 0.3098 | 3 |
| 1YNKAVMJ | news38 | group_rank(vec_avg(mws38_tone_score), subindustry) | 0.24 | 0.06 | 0.74 | 0.21 | 0.3961 | 3 |
| YP1zoweJ | news38 | 极性比率 (positive_freq / negative_freq) | 0.25 | 0.07 | 0.08 | 0.29 | 0.4153 | 5 |
| 2rA6oXL6 | news38 | group_rank(vec_stddev(mws38_tone_score), subindustry) | 0.20 | 0.05 | 0.80 | 0.19 | 0.3966 | 5 |
| vR1GXplQ | news38 | group_rank(vec_avg(mws38_d1_hotlevel), subindustry) | 0.04 | 0.00 | 0.50 | 0.09 | 0.3850 | 3 |

## 归因
1. **换手 0.31–0.42 全线偏高**：原始新闻事件逐日报道，几何上就是高噪声；sector/subindustry 中性化压不下来。
2. **2Y 普遍 > 全期 S**（news50 0.40→1.10、0.20→1.17；news38 0.20→0.80）⇒ 信号只在近年有效，2014–2019 基本无效。RA 要求 S 与 2Y 双过 1.58，历史段拖死不救。
3. **两数据集互不相同**（news50=71 个 VECTOR 事件情绪分；news38=36 个 VECTOR 语调/tone 分），字段语义相近但独立采样，同时落在同一天花板 ⇒ 不是字段问题，是**该塔在 KOR 的信息含量问题**。
4. news38 的 `mws38_hotlevel` 全 0（S 0.04），确认该字段空值，与历史画像一致。

## 决策
- **news50 / news38 / NEWS category 整塔封盘**（P4、P5 主动终止于第 1–3 批，省下 6 批）。
- 转 **SENTIMENT 塔**（news_sentiment_transfer，cov 0.9654，MATRIX 型）与 **INSTITUTIONS 塔**（institutions6 cov 1.0 / fund_holdings_panel cov 0.9553）——两者均为未点亮塔，且信号形态与 NEWS 事件流不同（连续标准化评分 / 持仓快照）。

## 复用的方法论
- 「数据集级 prod 体检」升级为「**塔级判死**」：同一 category 下 ≥2 个数据集、≥5 种几何全部落在同一低天花板 ⇒ 整塔封盘，不再换第 3 个数据集试。
- 判据阈值：若一塔最强件 S < 1.0（距 1.58 有 >35% 缺口），且跨数据集一致，即可判死，不必等满 10 模板。


---

## 追加：SENTIMENT 塔同样判死（P6b，2026-11-07）

news_sentiment_transfer（cov **0.9654**、MATRIX 型、aC 1–31 —— 按覆盖率与拥挤度是全 KOR 最优的新闻类数据集）实测同样崩：

| alpha | 表达式 | S | F | 2Y | sub | TO | raFail |
|---|---|---|---:|---:|---:|---:|---:|---:|
| xArG71wp | group_rank(ts_av_diff(sentiment_score_average, 66), sector) | 0.09 | 0.01 | 0.54 | 0.21 | 0.4259 | 3 |
| KPJzAmqj | group_rank(ts_av_diff(sentiment_score_average, 250), sector) | 0.04 | 0.00 | 0.53 | 0.16 | 0.4229 | 3 |

**关键否证**：这两条用的正是 KOR 当前**最强几何**（`group_rank(ts_av_diff(F,W), sector)`，在 dl_riskfree 上跑出过 S 2.09），
窗口 66/250 覆盖季度与年度两个尺度。同一几何、更高覆盖率的字段，S 只有 0.04–0.09。

⇒ **覆盖率 0.9654 完全不代表信号强度**。数据集覆盖高只说明「大部分票有值」，不说明值有预测力。
全 KOR news/sentiment 三数据集（news50 cov0.65 / news38 cov0.89 / news_sentiment_transfer cov0.97）合计 8 条 alpha、S 上限 0.40。

## 塔级判死最终名单（KOR/D1/TOP600）
- **NEWS**：news50, news38 —— 封盘
- **SENTIMENT**：news_sentiment_transfer —— 封盘
- 两者合计消耗 4 批、8 条 alpha，最强 S 0.40（阈值 1.58）

## 方法论升级（写入 Agent Memory）
「数据集级 prod 体检」之前应先做「**塔级信号强度体检**」：从该塔取覆盖率最高的数据集，用**本区已验证的最强几何**打 2 条探针。
若 S < 1.0 ⇒ 整塔封盘，不再换数据集。判据理由：几何已验证有效的前提下，剩余变量只有字段本身，
S 崩即字段无预测力，与覆盖/拥挤度无关。
