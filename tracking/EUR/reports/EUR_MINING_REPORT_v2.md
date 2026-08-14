# EUR 全矩阵挖掘战役报告 v2 (2026-08-12)

## 战役范围（用户要求: 所有 universe × 所有中性化）
- Universe 6 档: TOP2500 / TOP1200 / TOP800 / TOP400 / ILLIQUID_MINVOL1M / TOPCS1600
- Neutralization 12 档: NONE / REVERSION_AND_MOMENTUM / STATISTICAL / CROWDING / FAST / SLOW / MARKET / SECTOR / INDUSTRY / SUBINDUSTRY / COUNTRY / SLOW_AND_FAST
- 核心信号: returns 反转 (rev21/rev42/rev63/rev126/rev252) + 因子混合
- 共 15 批 / 60+ 表达式 / 全部白名单合规

## 关键发现

### 1. TOPCS1600 中性化矩阵（rev63 单腿）
| 中性化 | Sharpe | Fitness |
|--------|--------|---------|
| **STATISTICAL** | **2.70** | 0.79 |
| SLOW_AND_FAST | 2.19 | 0.54 |
| SUBINDUSTRY | 1.95 | 0.65 |
| INDUSTRY | 1.73 | 0.57 |
| SECTOR | 1.53 | 0.51 |
| COUNTRY | 1.45 | 0.48 |
| MARKET | 1.34 | 0.44 |
| CROWDING | 1.30 | 0.40 |
| REVERSION_AND_MOMENTUM | 1.03 | 0.24 |
| NONE | -0.80 | -0.79 |

**结论**: EUR TOPCS1600 最优中性化 = STATISTICAL (+44% vs SUBINDUSTRY, +160% vs R&M)

### 2. 参数演进（TOPCS1600 × STATISTICAL）
| 变体 | S | F | T | 2Y | 突破 |
|------|---|---|---|-----|------|
| rev63 裸 | 2.70 | 0.79 | 87.3% | — | S 破 |
| rev63+decay_linear5 | 2.42 | 0.90 | 47.5% | 0.33 | T 破 |
| rev126 裸 | 2.76 | 0.82 | 87.8% | 0.61 | 2Y 改善 |
| **rev252+decay_linear10** | **2.43** | **1.11** | **35.1%** | **0.43** | **F 破 ✅ T 破 ✅** |

### 3. 最终候选状态 (KPGmYRE1, rev252+decay_linear10)
| 检查 | 值 | 门槛 | 状态 |
|------|-----|------|------|
| LOW_SHARPE | 2.43 | 1.58 | ✅ |
| LOW_FITNESS | 1.11 | 1.0 | ✅ |
| TURNOVER | 35.1% | 1-70% | ✅ |
| CONCENTRATED_WEIGHT | — | — | ✅ |
| LOW_SUB_UNIVERSE_SHARPE | 1.06 | 1.29 | ❌ 差0.23 |
| LOW_ROBUST_UNIVERSE_SHARPE | 0.63 | 0.70 | ❌ 差0.07 |
| LOW_2Y_SHARPE | 0.43 | 1.58 | ❌ 差1.15 |

## 结构性结论
1. **EUR 反转信号 4/7 项达标**（Sharpe 2.43/Fitness 1.11/Turnover/CW 全过）
2. **2Y Sharpe 是终极墙**: 反转信号 2Y=0.43 vs 1.58, 差 1.15 不可破
   - 近期反转强 (S 2.4-2.7) 但 2Y 窗口结构性衰减
   - 长窗反转 (252) 只把 2Y 从 0.33 提到 0.43
3. **Sub-universe 0.23 / Robust 0.07**: 次要墙, 若 2Y 破可再优化
4. 因子数据集 (ml_factor_proj/news/ai) 单独无解, 纯反转是 EUR 唯一强信号

## 判定
- RA 通道: 4/7 达标, 2Y 墙不可破 → **不提交**（诚实评估）
- PPA 通道: EUR 不在当期 GLB 主题
- 与 TOP1200 结论一致: EUR 反转信号的 2Y 结构性衰减是全区域特征

## 下一步
1. 等待 EUR PPA 主题窗口 (9月可能轮动)
2. 或 2Y 墙破解方向: 反转+长期因子融合 (u8/u9 已试 S 1.07 F 0.33 — 因子腿稀释反转, 不是方向)
3. 或换区域: EUR 已穷尽 (与 DEU/GBR 同型)
