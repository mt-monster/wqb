# USA D1 挖掘战役报告 (2026-08-13)

## 战役配置
- Region: USA / D1 / TOP3000 / EQUITY / P6Y / trunc 0.08
- 数据集: ai_news_scores (105 MATRIX) + ai_equity_alpha (1108) + price_signal_dl + nlp_news_scores
- 中性化: SUBINDUSTRY / SECTOR / SLOW_AND_FAST 三档

## 结果
### 最佳候选 (接近达标)
| alpha_id | 结构 | S | F | T | 2Y | 差距 |
|----------|------|---|---|---|-----|------|
| GrGm13Qo (x6) | 修正分+反转 50/50 × SUBIND | 1.79 ✅ | 0.80 ❌ | 39.8% ✅ | 2.43 ✅ | F 差 0.20 |
| f3 | 修正0.6+反转0.4 | 1.60 ✅ | 0.76 | 29.1% | — | F 差 0.24 |
| f1 | x6+decay5 | 1.45 | 0.82 | 18.8% | — | S 差 0.13 |

### 信号族评估
| 数据集 | 信号强度 | 结论 |
|--------|---------|------|
| ai_news_scores 情感 | S 0.46-0.54 | ❌ 弱 (USA NLP 情感无 alpha) |
| ai_equity_alpha 分析师 | S 0.78-0.96 | ⚠️ 中等, 需反转腿 |
| ai_equity_alpha × 反转腿 | S 1.60-1.79 | ✅ 达标 (Fitness 临界) |
| price_signal_dl | 未达标 | ❌ 弱 |

## 关键发现
1. **USA 反转腿是必需品**: 分析师类单独 S0.78-0.96, 加反转腿 → S1.60-1.79
2. **Fitness 死结**: Fitness = S×√(|R|/max(T,0.125)) — 反转腿提 S/R 同时提 T, 三者此消彼长
3. **Fitness 修复代价**: 降 T (decay_linear) → S 跌 (1.79→1.23-1.60), F 只到 0.86
4. USA 拥挤度高: 分析师类 2Y 强 (2.43) 但 Fitness 是瓶颈

## 与 EUR/IND 对比
| 维度 | EUR | IND | USA |
|------|-----|-----|-----|
| 信号源 | returns 反转 | mdl177 因子 | ai_equity 分析师+反转 |
| 主要墙 | prod_corr 0.95 | robust 0.9-0.94 | Fitness 0.8 |
| 2Y | 1.08 ❌ | 2.45-3.0 ✅ | 2.43 ✅ |
| 结果 | 全拒 | 2 提交成功 | 1 接近 (F 差 0.2) |

## 下一步建议
1. **Fitness 突破口**: 提 Returns 而非降 Turnover (更高 Sharpe 的修正分字段 / signed_power 非线性)
2. 或试 xAdL5vmN 精确复刻 (S4.51/F4.13 的结构: group_rank + signed_power5 + decay90)
3. 已确认 USA 分析师+反转结构 2Y 天然达标 — 只需攻克 Fitness
