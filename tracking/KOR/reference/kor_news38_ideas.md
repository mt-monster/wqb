# news38 GEM Ideas (KOR / TOP600 / delay1)

## 字段

- 主信号：mws38_tone_score（users=0）/ mws38_tc_tone_score（users=1）标题情绪 [-1,1]
- 辅助：mws38_d1_hotlevel（注意力，users=2）、mws38_positive_score / mws38_negative_score（情绪幅度 ≥0）
- 避开：mws38_score(users=19) / mws38_previous(users=18) 高拥挤；mws38_hotlevel 全零；*_time / *_entitlement 系统字段

## 特征

- VECTOR 事件流，每日多条 → vec_avg 聚合后横截面运算；事件稀疏用 trade_when 门控 / ts_backfill 补洞
- tone 有界 → rank 包裹；freq 偏态 → rank 强制；主辅信号区分明确（tone 主、hotlevel 辅权重）

## 建议

- 正向情绪为主；动量 5 日窗口；平滑 22 日窗口；sector 组内相对化参照 wave140 正面结构
- KOR 新闻情绪族历史死路（wave87/96）→ 小批量探针验证方向，幅度不足即判死

**Dataset**: news38
**Region**: KOR
**Delay**: 1

**Concept**: Headline Tone Level
- **Mechanism**: Positive headline tone signals favorable information flow; firms with the most positive recent headlines drift upward as sentiment diffuses slowly. expected_exposure: news sentiment.
- **Fields**: `mws38_tone_score`
- **Implementation Example**: `rank(vec_avg({mws38_tone_score}))`
- **Direction**: positive

**Concept**: Tone Momentum (5-day)
- **Mechanism**: Improving headline tone over 5 days marks an accelerating information trend; sentiment momentum continues short-term. expected_exposure: sentiment momentum.
- **Fields**: `mws38_tone_score`
- **Implementation Example**: `rank(ts_delta(vec_avg({mws38_tone_score}), 5))`
- **Direction**: positive

**Concept**: Attention-Weighted Tone
- **Mechanism**: High-attention stories (hotlevel) carry more market impact; tone weighted by attention isolates stories likely to move prices. Main signal = tone, auxiliary = hotlevel as weight. expected_exposure: attention-gated sentiment.
- **Fields**: `mws38_tone_score`, `mws38_d1_hotlevel`
- **Implementation Example**: `multiply(rank(vec_avg({mws38_tone_score})), rank(vec_avg({mws38_d1_hotlevel})))`
- **Direction**: positive

**Concept**: Positive-Negative Imbalance
- **Mechanism**: Magnitude gap between positive and negative headline features captures raw sentiment polarity beyond the composite tone; imbalance leaders outperform. expected_exposure: sentiment polarity.
- **Fields**: `mws38_positive_score`, `mws38_negative_score`
- **Implementation Example**: `rank(subtract(vec_avg({mws38_positive_score}), vec_avg({mws38_negative_score})))`
- **Direction**: positive

**Concept**: Smoothed Tone Persistence (22-day)
- **Mechanism**: Persistent positive tone over 22 days filters one-off noise; sustained favorable coverage reflects durable fundamentals. expected_exposure: persistent sentiment.
- **Fields**: `mws38_tc_tone_score`
- **Implementation Example**: `rank(ts_mean(vec_avg({mws38_tc_tone_score}), 22))`
- **Direction**: positive

**Concept**: Event-Gated Tone
- **Mechanism**: Trade only on days with fresh positive-narrative events; event gating avoids holding stale sentiment between news arrivals. expected_exposure: event-driven sentiment.
- **Fields**: `mws38_tone_score`, `mws38_positive_score`
- **Implementation Example**: `trade_when(rank(vec_avg({mws38_tone_score})), ts_delta(vec_avg({mws38_positive_score}), 2) != 0, 0)`
- **Direction**: positive
