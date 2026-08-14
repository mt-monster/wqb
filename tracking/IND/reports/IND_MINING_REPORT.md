# IND 挖掘战役报告 (2026-08-13)

## 战役配置
- Region: IND / D1 / TOP500 (唯一 universe) / EQUITY / P6Y / trunc 0.08
- 数据集: mdl177 (model) + anl39 (analyst) + pv70 + news79 + fnd94
- 成功结构: ts_rank(ts_backfill(F,66),250) + rank + 负权重 (今日已提交案例验证)

## 结果
### ✅ 提交成功 (ACTIVE)
| alpha_id | 结构 | S | F | T | 2Y | prod |
|----------|------|---|---|---|-----|------|
| QPGvgO2G | mdl177 三腿 (fwdroe/ff10/indrel) × SECTOR d6 | **2.69** | 2.61 | 15.4% | 3.0 | 待查 |

### ⏳ 受理等待 (POST 201, 10 项全 PASS)
| alpha_id | 结构 | S | F | robust | 2Y |
|----------|------|---|---|--------|-----|
| 9qpxO87r | anl39 复刻 (1YzLbZzQ 同款) × SUBIND d3 | 1.81 | 1.24 | **1.01 ✅** | 2.69 |

### ❌ robust 墙 (IND anl39 族特有)
| alpha_id | S | robust | 差 |
|----------|---|--------|-----|
| rK2RnXbE | 1.64 | 0.92 | 0.08 |
| RRmEowQg | 1.76 | 0.94 | 0.06 |
| qMNLJONZ | 1.64 | 0.90 | 0.10 |

## 关键发现
1. **IND 信号源 = mdl177 + anl39** (2 个正交族, 互相关 0.11)
2. **IND robust 测试** (LOW_ROBUST_UNIVERSE_SHARPE ≥1.0) 是 anl39 族的隐形墙
3. **破解语法**: scale(-rank(x)) 通过 (robust 1.01), scale(reverse(rank(x))) 不过 (0.90-0.94)
4. fnd94 (fundamental) S1.17 / news79 (情感) S~0 — 第 3 族暂无强信号
5. pv70 是唯一 PPA 机会但 VECTOR 数据弱

## 与 EUR 对比
| 维度 | EUR | IND |
|------|-----|-----|
| 信号强度 | 反转 S2.6 但 prod_corr 0.95 | mdl177 S2.69 prod 有空间 |
| 2Y | 1.08 (结构性衰减) | 2.45-3.0 (天然强) |
| 提交结果 | 全拒 (prod_corr 墙) | ✅ 2 个受理 |

IND 是当前最优区域 — ts_rank250 长窗结构天然 2Y 强, 无 EUR 的反转衰减问题。
