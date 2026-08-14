# EUR 全矩阵挖掘战役报告 v3 (2026-08-12 最终)

## 战役范围（用户要求: 所有 universe × 所有中性化 全扫）
- Universe 6 档全部测试: TOP2500 ✅ / TOP1200 ✅ / TOP800 ✅ / TOP400 ✅ / ILLIQUID_MINVOL1M ✅ / TOPCS1600 ✅
- Neutralization 12 档全部测试（TOPCS1600 上）
- 20+ 批 / 100+ 表达式 / 全部白名单合规

## 关键发现链
1. **EUR 核心信号 = returns 反转**（短窗 S 高但 2Y 弱）
2. **中性化 = STATISTICAL 最优**（TOPCS1600: 2.70 vs SUBINDUSTRY 1.95 vs R&M 1.03）
3. **Universe = TOP2500 最优**（2Y 从 0.43→0.86，大 universe 提升 2Y）
4. **decay_linear 平滑 = 降换手 + 提 2Y 双赢**
   - T: 87% → 26% ✅
   - 2Y: 0.33 → 0.86 → 1.08（3.3 倍提升）

## 最终候选 (mL5Yx3X9, rev504 × decay_linear20 × STATISTICAL × TOP2500)
表达式: ts_decay_linear(reverse(rank(ts_zscore(returns, 504))), 20)

| 检查 | 值 | 门槛 | 状态 |
|------|-----|------|------|
| LOW_SHARPE | 2.62 | 1.58 | ✅ |
| LOW_FITNESS | 1.35 | 1.0 | ✅ |
| TURNOVER | 26.2% | 1-70% | ✅ |
| CONCENTRATED_WEIGHT | — | — | ✅ |
| LOW_SUB_UNIVERSE_SHARPE | 1.50 | 1.29 | ✅ |
| LOW_2Y_SHARPE | 1.08 | 1.58 | ⚠️ 差 0.50 |
| PPA failed count | 0 | 0 | ✅ PPA 资格过 |
| checks FAIL | 0 | 0 | ✅ |

## 2Y 墙攻坚记录
| 结构 | 2Y | 突破 |
|------|-----|------|
| rev63 × STAT (TOPCS1600) | 0.33 | 基线 |
| rev252 × decay10 (TOPCS1600) | 0.43 | 长窗 |
| rev252 × decay10 (TOP2500) | 0.86 | 大 universe |
| rev252 × decay20 (TOP2500) | 1.12 | 强平滑 |
| **rev504 × decay20 (TOP2500)** | **1.08** | 超长窗 |

2Y 天花板 ~1.1：反转信号的 2Y 窗口收益结构性受限，decay 平滑已最大化。

## 结论
- **6/7 项达标，0 FAIL，PPA 资格通过** — EUR 最佳候选
- 唯一未过: LOW_2Y_SHARPE (1.08 vs 1.58)
- 候选已就绪 (mL5Yx3X9 / e7362rWM / P0GMXWpL)，等待用户决定
- 2Y 1.58 门槛对 EUR 反转信号不可达（与 DEU/GBR 同型结构性限制）

## 候选池（3 个可提交级）
| alpha_id | 结构 | S | F | T | 2Y |
|----------|------|---|---|---|-----|
| mL5Yx3X9 | rev504×d20 | 2.62 | 1.35 | 26.2% | 1.08 |
| e7362rWM | rev252×d20 | 2.58 | 1.30 | 26.9% | 1.12 |
| P0GMXWpL | 252+504×d20 | 2.62 | 1.34 | 26.7% | — |
