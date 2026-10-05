# 区域快照（2026-08，历史数据，**不是行动指令**）

> 来源：`wq-brain-ppa-mining` SKILL 旧 §8（2026-08-05 / 08-23 的平台实测与离线包分析），挪出以免被当作指令。
> **失效条件**：数据集数、覆盖率、倍率与拥挤度都会随平台更新变化，超过一个季度或换了 universe / delay 即失效；这里的「首选 / 头号目标 / 区域优先级」在当时的意思是「当时的候选」，**不是**现在的推荐。
> **此后的证据反向**：新闻 / 情绪族在 USA / EUR / IND 同型全灭（RA 跨区弱先验）、KOR 新闻三连判死、`alphaCount = 0` 的集多为伪白空间（toolkit `probe-scoring-v2`）。选区与选集以实时体检（SKILL §2）、`get_mining_yield` 与 registry 为准。

## 平台实测规模（2026-08-05）

| 区域（universe / delay） | 数据集数 | coverage 均值 | cov ≥ 0.90 的集 |
|---|---|---|---|
| KOR（TOP600 / D1） | 192 | 0.7046 | 54 |
| EUR（TOP1200 / D1） | 178（38609 字段） | 0.6616 | 35 |
| HKG（TOP800 / D1） | 209 | 0.6958 | 43 |

- KOR：此前「KOR_TOP600 低覆盖（仅 1 数据集）」的说法来自离线包，与平台实况不符，已作废。
- EUR：原战役失败的根因是**选集错误**而非区域无解（案例见 SKILL §3）。
- ASI：`model110` 经 `get_datafields` 取到 8 个 ASI 字段。
- USA / D1 / TOP3000：institutions18 有 3 个 PPA 提交（S = 2.23）；institutions6 / 20 信号弱；imbalance5 仅 2 字段；fund_holdings_panel 的 P6Y 不可用。b107–b128 战役：9+ 家族 15 批次，sharpe > 1.5 者全部被 **prod_corr > 0.7** 卡死（最佳 0.724，差 0.024），0 可提交——印证 `alphaCount ≤ 50` 门槛不是可选项。

## KOR 离线实证（2026-08-05）

- SECTOR 最佳中性化（0.562）；sweet datasets：news59（0.597）、insiders5（0.564）、shortinterest3（0.524）、risk71（OS 1.306）、analyst39；model253 退化。
- （news59 在 2026-08-23 之后被 KOR 新闻 / 情绪三连判死覆盖；此表只是当时的离线徽章。）

## 跨区域倍率差（2026-08，`pm` = pyramidMultiplier，`vs` = valueScore，`a` = alphaCount）

同一数据集在不同区域的倍率 / 拥挤度差异很大，同样的信号在不同区域收益可差 20%+。**方法**：新战役开打前，对 2–3 个候选区各跑一次体检再比倍率。当时的数字：

| 数据集 | EUR（TOP1200） | KOR（TOP600） | HKG（TOP800） |
|---|---|---|---|
| `news_sentiment_nlp` | pm 1.5 / vs 6.0 / a0 | pm 1.7 / vs 9.0 / a0 | pm 1.8 / vs 9.0 / a0 |
| `ml_factor_proj` | pm 1.5 / vs 5.0 / a0 | pm 1.7 / vs 6.0 / a10 | pm 1.8 / vs 6.0 / a38 |
| `ai_factor_transfer` | pm 1.3 / vs 4.0 / a0 | pm 1.7 / vs 6.0 / a8 | pm 1.7 / vs 5.0 / a9 |
| `analyst_earnings_ibes` | pm 1.3 / vs 5.0 / a1 | pm 1.7 / vs 6.0 / a6 | pm 1.7 / vs 6.0 / a11 |
| `price_signal_dl` | pm 1.3 / vs 5.0 / a2 | pm 1.7 / vs 6.0 / a6 | pm 1.7 / vs 6.0 / a1 |
| `global_seasonal_model` | pm 1.3 / vs 5.0 / a0 | pm 1.7 / vs 6.0 / a70 | pm 1.7 / vs 6.0 / a6 |

- 当时 EUR 未开发的候选：`ml_factor_proj`（333 字段全部 cov = 1.0，MATRIX，0 用户 0 alpha）、`news_sentiment_nlp`（23 字段）、`global_seasonal_model`（449 字段 0 alpha）、`continuation_score` / `pattern_scores`（各 500+ 字段 cov 0.99 零 alpha）。其中 `continuation_score` / `pattern_scores` 后来在 KOR 被图表形态族三连判死（天花板 0.49）。
- 当时 HKG 未开发的候选：`news_sentiment_nlp`（vs 9.0 / pm 1.8 / 0 alpha）、`news_sentiment_dl`（vs 7.0 / pm 1.8 / 1 alpha）、`mmp_nlp_sentiment`（521 字段 cov 0.9476 / vs 7.0 / pm 1.8 / 2 alpha）。

## 已知的红灯族（KOR，2026-08-23 之前；仅作历史，判死状态以 registry 为准）

图表形态（chart_cnn_alpha / continuation_score / pattern_scores 三连判死，天花板 0.49）；新闻 / 情绪（news79 / equity_forum_data / news_sentiment_transfer 三连判死，天花板 0.76）；AI / ML 因子库（ai_factor_transfer / ai_equity_alpha / ml_factor_proj 三连判死，天花板 0.86）；信用风险（quant_factor_lib / model313 双判死）；行为金融 / 论坛（behavioral_signals / equity_forum_data 全灭）。MEA：慢变基本面 / value / quality 红灯。判死条目以 `mcp__wqb-db__get_dead_ends(region)` 为准。
