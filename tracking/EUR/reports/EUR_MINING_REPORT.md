# EUR PPA/RA 挖掘战役报告 (2026-08-12)

## 战役配置
- Region: EUR / D1 / TOP1200 / EQUITY / P6Y / trunc 0.08
- PPA 主题: GLB/D1 Power Pool Aug'26 2 (EUR 不在主题 → 走 RA 通道)
- 中性化: REVERSION_AND_MOMENTUM / SUBINDUSTRY / MARKET / STATISTICAL 四档对比
- 数据集: ml_factor_proj (0α) + news_sentiment_nlp (0α) + ai_factor_transfer (0α) + returns 信号
- 执行: 7 轮 / 44 表达式 / 全部白名单合规

## 结果演进
| 轮次 | 策略 | 最佳 Sharpe |
|------|------|------------|
| R1 | 因子单腿基线 (ts_rank+backfill+winsorize) | 0.47 |
| R2 | 方向修正 + 窗口扫描 | 0.50 |
| R3 | returns 反转组合 (V9 范式) | 0.73 |
| R4 | 参数扫描 (权重/窗口/decay) | 0.77 |
| R5 | 纯 returns 反转 + 中性化对比 | 1.11 |
| R6 | 反转 × SUBINDUSTRY 换挡 | **1.60** |
| R7 | decay/平滑降换手 | 1.45 (T 达标) |

## 最终候选
| ID | Sharpe | Fitness | Turnover | 2Y | 状态 |
|----|--------|---------|----------|-----|------|
| m6i rev63×SUBIND (0mpjmGnG) | 1.60 ✅ | 0.49 ❌ | 85.8% ❌ | — | S 达标, F/T 不过 |
| m6c 双反转×SUBIND (QPGYPWmQ) | 1.59 ✅ | 0.47 ❌ | 87.1% ❌ | — | S 达标, F/T 不过 |
| rev63 decay10 (d5ZKkZpj) | 1.34 | 0.47 ❌ | 57.9% ✅ | **-0.09 ❌** | T 达标, 2Y 崩 |

## 关键结论
1. **EUR 核心信号源 = returns 反转** (与预筛 REVERSION_AND_MOMENTUM 结论吻合)
2. **中性化 = SUBINDUSTRY 最优** (R&M 1.11 → SUBIND 1.60, +44%)
3. **结构性矛盾**: 反转信号近期 S 1.6 但 2Y 衰减至负 (-0.09) → LOW_2Y_SHARPE 墙不可破
4. **Turnover 矛盾**: decay4 S 最高但 T 85.8% 超限; decay10 T 达标但 2Y 崩
5. 因子数据集 (ml_factor_proj/news/ai) 单独信号弱 (0.2-0.5), 需反转腿加成

## 未达标判定
- RA 通道: 3 项硬门槛 (Fitness≥1.0 / Turnover≤70% / 2Y>1.58) 无法同时满足
- PPA 通道: 当期主题 GLB, EUR 无 PPA 机会
- 结论: **EUR 零竞争数据集当前无达标候选** (与 DEU/GBR 结构性限制同型)

## 下一步建议
1. 等待 EUR PPA 主题窗口 (历史轮动: 6月 USA+GLB, 7月 USA, 8月 GLB → 9月可能 EUR)
2. 或尝试 EUR/TOP2500 或 EUR/TOPCS1600 其他 universe 档
3. 或换 EUR 特有数据集 (analyst_earnings_ibes 价格类 / fundamental 类)
