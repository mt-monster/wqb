# 战略转折记录 · KOR ATOM（2026-11-07）

## 第三次转塔：analyst → PV

### 触发事实（平台权威，非推断）
`get_pyramid_alphas(KOR, D1)` 实测：

| 塔 | 已提交 | 点亮态 | 乘数 |
|---|---:|---|---:|
| analyst | **3** | **已点亮** | 1.6 |
| fundamental | 3 | 已点亮 | 1.6 |
| model | 3 | 已点亮 | 1.6 |
| shortinterest | 4 | 已点亮 | 1.4 |
| **pv** | **2** | 未点亮 | 1.4 |
| other | 1 | 未点亮 | 1.6 |
| insiders | 1 | 未点亮 | 1.2 |
| risk / earnings / institutions / macro / news / sentiment / socialmedia / imbalance | 0 | 未点亮 | 1.0–1.6 |

### 判定
Wave A1 押的 analyst 塔**已经点亮（3/3）**，按用户硬约束「已点亮塔的数据集一律不选」，analyst 线立即封盘。
（Wave A1 的 8 条读数仍作为该数据集的反面证据保留，见 `campaign_20261107_analyst_atom/waveA1_results.csv`。）

### Wave A1 读数摘要（analyst_consensus，10 条中 8 条可读）
| 机制 | S | F | 2Y | raFail |
|---|---:|---:|---:|---:|
| 4 周净利修正比（best） | 0.75 | 0.50 | **1.60** | 2 |
| 3 月净利修正比 | 0.75 | 0.50 | 1.47 | 3 |
| 双 surprise 乘积（反向臂） | **-1.27** | -1.03 | **-2.36** | 5 |
| surprise 水平 | 0.70 | 0.40 | 1.04 | 3 |
| count 差分 | 0.67 | 0.41 | 1.46 | 3 |
| surprise 66 日均值 | 0.62 | 0.33 | 0.91 | 3 |
| count 水平（反向） | -0.67 | -0.48 | -1.62 | 5 |
| 离散度/水平（反向） | -0.77 | -0.52 | -1.46 | 5 |

三条 FAIL：`add(x, 1)` 与带 `CSPrice×CSShare` 单位的字段冲突（净利、目标价族），后续遇单位型字段一律用 `divide(subtract(a,b), abs(b))` 而非 `add(abs(b), eps)`。

## 交付盘点（修正后）
| # | alpha | 数据集/塔 | S | F | 2Y | self | prod | 状态 |
|---|---|---|---:|---:|---:|---:|---:|---|
| 1 | `omERn83n` | risk70 / RISK | 1.62 | 1.23 | 2.27 | 0.4211 | 0.6898 | UNSUBMITTED，可提交 |
| 2 | `qMLOooX1` | analyst10 / ANALYST | **1.94** | 1.74 | 1.76 | 0.3939 | 0.6941 | UNSUBMITTED，可提交（prod 余量 0.006） |
| 3 | `RRE9NkVj` | insiders5 / INSIDERS | 1.76 | 1.63 | **2.77** | 0.3104 | 0.6605 | **ACTIVE（已提交上线）** |

⇒ 实质产出 **3 颗**（1 已提交 + 2 待提交），缺口 **7 颗**。
⚠ 前次会话曾把 `RRE9NkVj` 记为「未提交」；本次 `get_alpha_details` 实测 status=ACTIVE，pending 只剩 POWER_POOL_CORRELATION / MATCHES_THEMES ⇒ 已提交。

## 新一轮选集（PV 塔）
依据：PV 未点亮（2/3）、覆盖满分、拥挤度低。
Wave B = `continuation_score`（形态相似度）；Wave C 备选 = `pv106`（价差/交易成本）、`pv47`（特质收益）。