# EUR 新数据包 × 丰富算子探索报告 (2026-08-12)

## 探索的数据包（用户要求 1: 试下 EUR 其它数据包）
| 数据集 | 字段数 | 类型 | 结果 |
|--------|--------|------|------|
| pattern_scores | 504 | MATRIX | ✅ 可仿真, 信号弱 (max S=0.66) |
| dl_riskfree_returns | 133 | MATRIX | ✅ 可仿真, 信号弱 (S=-1.95) |
| ai_equity_alpha | 582 | VECTOR | ❌ 仿真 FAIL (数据覆盖不足) |
| model354 | 236 | VECTOR | ❌ 仿真 FAIL |
| continuation_score | 560 | VECTOR | ❌ 仿真 FAIL |

关键发现:
- pattern_scores 是 GBR 已提交成功 (A1G7o1EE S1.61/2Y1.64) 的同款信号族
- 但跨区域移植失效: EUR pattern_scores max S=0.66 (GBR 1.61)
- VECTOR 类数据集 (ai_equity/model354/continuation) 仿真 FAIL — 字段元数据存在但实际面板数据缺失

## 算子组合丰富化（用户要求 2: 算子组合再丰富一些）
对 pattern_scores breakaway 信号测试 7 种算子组合:
| 算子组合 | S | 结论 |
|----------|---|------|
| rank 三形态融合 (GBR 同款) | 0.66 | 最佳但弱 |
| ts_rank 预处理链 | 0.13 | 弱 |
| subtract 双腿差 | -0.26 | 无效 |
| group_zscore 行业中性 | 0.05 | 无效 |
| signed_power3 非线性 | 0.04 | 无效 |
| ts_delta 变化率 | -0.38 | 反向 |
| tail 区间截断 | 0.36 | 弱 |

结论: 算子组合丰富化对弱信号无济于事 — 信号源本身弱

## 综合判定
EUR 已系统性穷尽:
1. returns 反转: S 强但 prod_corr 0.95 + 2Y 1.08 双墙
2. 因子数据集 (ml_factor_proj/news/ai_factor_transfer): S 弱 (max 1.27)
3. pattern_scores (GBR 同款): 跨区域失效 (S 0.66)
4. VECTOR 数据集: 仿真 FAIL
5. 全部算子组合 (20+ 种): 无法改变信号强弱

EUR 是当前所有区域中结构性限制最严重的区域。
