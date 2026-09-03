# pv106 GEM Ideas (KOR / TOP600 / delay1)

## 字段

- 主信号：transaction_cost_estimate（users=0）、pv106_lastspreadbp（users=3）、korean_market_slippage（users=3）
- 辅助：group_order_slippage（users=2）、slippage_commission_estimate（users=3）
- 避开：pv106_wli_* 族（users 36-58 高拥挤）、slippage_at_spread_20、transaction_cost_maximum、bid_ask_price_gap

## 特征

- MATRIX 连续、成本类正偏 → rank 强制；覆盖 1.0 无需 backfill；bp 归一化变体优先于裸点差

## 建议

- 流动性溢价（低成本→跑赢）方向待实证；动量 5 日 / 平滑 22 日标准窗口；sector 相对化参照 wave140 正面结构

**Dataset**: pv106
**Region**: KOR
**Delay**: 1

**Concept**: Transaction Cost Liquidity Premium
- **Mechanism**: Low estimated transaction cost marks liquid, institutional-grade names that compound outperformance; cost leaders drift. expected_exposure: liquidity.
- **Fields**: `transaction_cost_estimate`
- **Implementation Example**: `rank({transaction_cost_estimate})`
- **Direction**: negative (low cost better; rank ascending gives long-low)

**Concept**: Tight Spread Quality
- **Mechanism**: Basis-point normalized spread isolates liquidity from price level; tightest spreads mark deepest order books. expected_exposure: liquidity/quality.
- **Fields**: `pv106_lastspreadbp`
- **Implementation Example**: `multiply(-1, rank({pv106_lastspreadbp}))`
- **Direction**: negative

**Concept**: Liquidity Momentum (5-day)
- **Mechanism**: Names whose transaction cost is falling (liquidity improving) attract flow; liquidity momentum persists short-term. expected_exposure: liquidity momentum.
- **Fields**: `transaction_cost_estimate`
- **Implementation Example**: `multiply(-1, rank(ts_delta({transaction_cost_estimate}, 5)))`
- **Direction**: negative

**Concept**: Sector-Relative Liquidity
- **Mechanism**: Liquidity ranked within sector isolates firm-level marketability from sector-wide flow; relatively liquid peers outperform. expected_exposure: sector-neutral liquidity.
- **Fields**: `transaction_cost_estimate`
- **Implementation Example**: `multiply(-1, group_rank(rank({transaction_cost_estimate}), sector))`
- **Direction**: negative

**Concept**: Persistent Liquidity (22-day smoothing)
- **Mechanism**: Persistently low cost over a month filters transient prints; structurally liquid names are institutional favorites. expected_exposure: persistent liquidity.
- **Fields**: `pv106_lastspreadbp`
- **Implementation Example**: `multiply(-1, rank(ts_mean({pv106_lastspreadbp}, 22)))`
- **Direction**: negative

**Concept**: Cost-Spread Divergence
- **Mechanism**: When modeled cost is cheap but spread is wide (or vice versa), microstructure mispricing resolves; divergence flags names where cost model sees through spread noise. expected_exposure: microstructure divergence.
- **Fields**: `transaction_cost_estimate`, `pv106_lastspreadbp`
- **Implementation Example**: `rank(subtract(rank({pv106_lastspreadbp}), rank({transaction_cost_estimate})))`
- **Direction**: positive
