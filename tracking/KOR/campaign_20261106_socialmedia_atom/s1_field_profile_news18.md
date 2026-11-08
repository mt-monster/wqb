# S1 简档 · news18 Ravenpack News Data（KOR / TOP600 / D1）

> 双灭后备（Wave3b+Wave4 后再启用）。category=news，塔 0/3。cov≈0.57 aC1019。
> 论坛/业界：ESS/BSS/CSS×relevance；新颖度 ENS；勿裸情绪。

## TOP 字段（按 alphaCount）
| id | type | cov | aC | desc |
|---|---|---:|---:|---|
| rp_ess_earnings | MATRIX | 0.5 | 247 | Event sentiment score of earnings news |
| rp_css_business | MATRIX | 0.5 | 171 | Composite sentiment score of business-related news |
| rp_nip_business | MATRIX | 0.5 | 124 | News impact projection of business-related news |
| rp_ess_business | MATRIX | 0.5 | 112 | Event sentiment score of business-related news |
| rp_css_revenue | MATRIX | 0.5 | 69 | Composite sentiment score of revenue news |
| nws18_qep | VECTOR | 0.6339 | 60 | Equities sentiment polarity score derived from positive/negative words in news (typically -1, 0, +1) |
| rp_css_earnings | MATRIX | 0.5 | 52 | Composite sentiment score of earnings news |
| nws18_qcm | VECTOR | 0.6339 | 41 | News sentiment of relevant news with high confidence |
| rp_ess_revenue | MATRIX | 0.5 | 37 | Event sentiment score of revenue news |
| nws18_acb | VECTOR | 0.6339 | 31 | News sentiment specializing in corporate action announcements |
| nws18_nip | VECTOR | 0.6339 | 22 | Narrative impact score in [-1, 1] estimating the news item’s short-term market impact (e.g., next tw |
| nws18_relevance | VECTOR | 0.7006 | 21 | Score from 0 to 100 indicating how strongly the entity is related to the story higher is more releva |
| rp_nip_earnings | MATRIX | 0.5 | 21 | News impact projection of earnings news |
| nws18_ssc | VECTOR | 0.7006 | 20 | Granular sentiment score from -1.00 to +1.00 for the story, combining multiple sentiment analysis te |
| nws18_sse | VECTOR | 0.4845 | 20 | Continuous sentiment score between -1.00 and +1.00 for the entity-event |
| rp_nip_revenue | MATRIX | 0.5 | 19 | News impact projection of revenue news |
| nws18_event_relevance | VECTOR | 0.538 | 18 | Integer from 0 to 100 indicating the event’s relevance within the story |
| nws18_bee | VECTOR | 0.7006 | 17 | Earnings evaluation score indicating positive, neutral, or negative assessment (-1, 0, +1) |
| nws18_event_similarity_days | VECTOR | 0.4845 | 16 | Number of days since a similar event was last detected within the past 365 days, up to 5 decimals |
| nws18_bam | VECTOR | 0.7006 | 14 | Mergers and acquisitions sentiment indicator (e.g., -1 negative, 0 neutral, +1 positive) |

## 平台计数
- platform_count=29 complete=true total_returned=29
