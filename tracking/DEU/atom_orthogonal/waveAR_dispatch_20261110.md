# Wave AR dispatch 2026-11-10 (sentiment cov=0 probe, per user directive "优先挖掘sentiment")

sim_id: 29IEqCbwg4X3aKsb097Her1
dispatched: 2026-11-10 15:20 local, try 1 (no 429)
settings: DEU/TOP500/D1/decay4/SUBINDUSTRY/trunc0.08/pasteurON/unitVERIFY/nanON/maxTradeOFF
preflight: valid=true, unknown_fields=[] (tools/mcp_call.py restored MCP entry)

## Probe design (10 expr, 5 datasets x 2 fields, level-probe template; graduates to full template pool if S>=1.0)
| # | dataset | field | template |
|---|---|---|---|
| 1 | ai_news_scores | negative_score_average_value_3 (EUR prv23 RavenPack, uc6) | level group_rank subindustry |
| 2 | ai_news_scores | pos-neg diff (positive_score_average_value_3 - negative_score_average_value_3) | level group_rank subindustry |
| 3 | earningscall_sentiment | mean_polarity_profitability_summary (uc13) | level group_rank subindustry |
| 4 | earningscall_sentiment | mean_polarity_leverage_presentation (uc8) | level group_rank industry |
| 5 | earningscall_sentiment | mean_polarity_profitability_answer (uc6) | level group_rank subindustry |
| 6 | event_sentiment_signals | key_factor_score_section (uc12, VECTOR) | vec_avg level subindustry |
| 7 | event_sentiment_signals | sentiment_section_key_driver_score (uc4, VECTOR) | vec_avg level industry |
| 8 | news_sentiment_nlp | headline_sentence_sentiment_average (VECTOR) | vec_avg level subindustry |
| 9 | socialmedia12 | sentiment_score (uc17/ac25) | level group_rank subindustry |
| 10 | socialmedia12 | sentiment_expected_price_change (uc16/ac26) | level group_rank industry |

## Sentiment family coverage status (after AR)
- sentiment7 DEAD (S<=0.77, batch Vl0pSdjo4F9bmX85lISwP, 2026-11-07)
- sentiment27 DEAD standalone (S<=0.64; orthogonalization leg only -> mLox6Mg2 mechanism)
- sentiment33 DEAD (wave AQ, CW structural, cov 0.32 VECTOR)
- analyst10 DEAD (wave AP)
- AR probes: ai_news_scores / earningscall_sentiment / event_sentiment_signals / news_sentiment_nlp / socialmedia12 <- IN FLIGHT
- Unprobed sentiment-adjacent remainder: news21/23/29/3/31/52/54/7/73/76/81 (RavenPack news family, low priority), socialmedia39 (1 field cov 0.27)
