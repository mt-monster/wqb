# analyst44 GEM Ideas (KOR / TOP600 / delay1)

## 字段

- 主信号：eps_estimate_4wk_change（users=0）、eps_gaap_estimate_4wk_change（users=0）、anl44_best_dps_4wk_chg（users=0）
- 辅助：eps_estimate_4wk_down_count（users=2）、anl44_best_dps_4wk_up（users=1）、anl44_best_eps_4wk_chg（users=3）
- 避开：anl44_second_*/anl44_2_* 低覆盖族；*_currency_code/*_period 元数据

## 特征

- VECTOR 滚动快照 → vec_avg + ts_backfill；计数字段非负偏态 → rank 强制；幅度字段有符号 → rank 后正向

## 建议

- 上调修订→正漂移（经典共识修订动量）；22 日持续性；sector 相对化；breadth（up-dn）作辅助信号

**Dataset**: analyst44
**Region**: KOR
**Delay**: 1

**Concept**: EPS Estimate Revision Momentum
- **Mechanism**: Analysts raising consensus EPS over 4 weeks signal improving fundamentals; revisions drift as the market underreacts to estimate updates. expected_exposure: earnings revision momentum.
- **Fields**: `eps_estimate_4wk_change`
- **Implementation Example**: `rank(ts_backfill(vec_avg({eps_estimate_4wk_change}), 22))`
- **Direction**: positive

**Concept**: GAAP EPS Revision Confirmation
- **Mechanism**: GAAP-basis revisions confirm adjusted-EPS moves; GAAP up-revisions are harder to engineer and mark genuine improvement. expected_exposure: earnings quality revision.
- **Fields**: `eps_gaap_estimate_4wk_change`
- **Implementation Example**: `rank(ts_backfill(vec_avg({eps_gaap_estimate_4wk_change}), 22))`
- **Direction**: positive

**Concept**: Dividend Estimate Momentum
- **Mechanism**: Rising consensus DPS signals management confidence in sustained cash flow; dividend revisions are sticky and slowly priced. expected_exposure: payout confidence.
- **Fields**: `anl44_best_dps_4wk_chg`
- **Implementation Example**: `rank(ts_backfill(vec_avg({anl44_best_dps_4wk_chg}), 22))`
- **Direction**: positive

**Concept**: Revision Persistence (22-day)
- **Mechanism**: Sustained positive revision flow over a month marks a durable re-rating trend rather than one-off noise. expected_exposure: persistent revision trend.
- **Fields**: `eps_estimate_4wk_change`
- **Implementation Example**: `rank(ts_mean(ts_backfill(vec_avg({eps_estimate_4wk_change}), 22), 22))`
- **Direction**: positive

**Concept**: Sector-Relative Revision
- **Mechanism**: Revision ranked within sector isolates firm-specific fundamental improvement from sector-wide cycles. expected_exposure: sector-neutral revision momentum.
- **Fields**: `eps_estimate_4wk_change`
- **Implementation Example**: `group_rank(rank(ts_backfill(vec_avg({eps_estimate_4wk_change}), 22)), sector)`
- **Direction**: positive

**Concept**: Event-Gated Revision Entry
- **Mechanism**: Trade the revision signal only when a fresh revision print arrives, avoiding stale positioning between analyst updates. expected_exposure: event-driven revision.
- **Fields**: `eps_estimate_4wk_change`
- **Implementation Example**: `trade_when(rank(ts_backfill(vec_avg({eps_estimate_4wk_change}), 22)), ts_delta(ts_backfill(vec_avg({eps_estimate_4wk_change}), 22), 1) != 0, 0)`
- **Direction**: positive
