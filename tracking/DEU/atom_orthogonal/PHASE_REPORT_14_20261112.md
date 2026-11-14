# DEU 战役阶段报告（2026-11-12 收口）

## 一、交付实绩：合规 14 / 20

| # | alpha | 状态 | S | F | 2Y | sub | 塔 | eff | 来源 |
|---|---|---|---:|---:|---:|---:|---|---:|---|
| 1 | vR1oxZA3 | ✅ACTIVE | **3.27** | 3.09 | 4.39 | — | （无标记）| — | 存量 |
| 2 | XgaGb3J1 | 🆕待授权 | **2.36** | 2.02 | 2.71 | 1.51 | INSIDERS+MODEL | 2 | insiders×analyst |
| 3 | vRA82ogA | 🆕待授权 | **2.07** | 1.85 | 2.59 | 1.43 | INST+INS+ANALYST | 0 | insiders×机构×analyst |
| 4 | RREPm361 | 🟡待授权 | 2.02 | 1.25 | 1.82 | — | ANALYST | — | 存量 |
| 5 | zq3eb7No | ✅ACTIVE | 2.01 | 1.28 | 1.64 | — | ANALYST | — | 存量 |
| 6 | rKRx2Alj | ✅ACTIVE | 1.95 | 1.80 | 2.23 | — | MODEL+ANALYST | — | 存量 |
| 7 | 9qlz29Oe | 🟡待授权 | 1.86 | 1.34 | 2.02 | — | SHORT+NEWS | — | 存量 |
| 8 | npa9PKWw | 🆕待授权 | **1.74** | **1.52** | 2.66 | 0.94 | INSIDERS+OTHER | 2 | insiders×other455长窗 |
| 9 | qM7KxkQV | 🟡待授权 | 1.72 | 1.34 | 2.43 | — | SHORT+INSIDERS | — | 存量 |
| 10 | 78Yk8VR1 | ✅ACTIVE | 1.68 | 1.21 | 2.27 | — | SHORTINTEREST | — | 存量 |
| 11 | Jj8VQwoe | 🟡待授权 | 1.65 | 1.24 | 2.42 | — | SHORT+OTHER | — | 存量 |
| 12 | GrW9OxmG | ✅ACTIVE | 1.62 | 1.56 | 1.93 | — | ANALYST | — | 存量 |
| 13 | bl6AvMkN | ✅ACTIVE | 1.61 | 1.36 | 2.15 | — | MODEL+ANALYST | — | 存量 |
| 14 | d5a2vxzY | 🟡待授权 | 1.60 | 1.08 | 2.05 | — | SHORTINTEREST | — | 存量 |

**互相关**：全对 <0.7，`max_mutually_below_subset_size = 14`
**分类合规**：每颗 trio 成员 ≤1 ✓
**逐年**：本战役新件 10 年全覆盖无空窗

## 二、insiders 数据集已探明上限（这是核心结论）

### 2.1 只有 holdings 存量有 alpha

| insiders 维度 | 最好 S | 结论 |
|---|---:|---|
| **持仓存量** `insd1_holdings` | **2.36** | ✅ **唯一有效** |
| 集中度 `significant_value_1-4`(HHI) | 0.83 单腿 | ✅ 仅作 C 腿 |
| 交易金额 `insd1_valueeur` | 1.14 | ❌ 死 |
| 股数占比 `shares/holdings` | 1.29 | ❌ 死 |
| 显著度 `insd1_tradesignificance` | 1.21 | ❌ 死 |
| 交易价 `insd1_price` | 1.13 | ❌ 死 |

**机理**：内部人 alpha 来自**持仓的持续性变化**（存量一阶差分 + 信噪比），不是单笔交易的规模/显著性。后者在 DEU TOP500 噪声过大（insiders1 cov 仅 53%）。符合 CMP 2012：信号必须聚合到持仓层面。

### 2.2 S7/S3 核心是共同因子 ⇒ 独立件上限 3-4 颗

| 搭档族 | 最好 S | 与 npa9PKWw 相关 | 能否进篮子 |
|---|---:|---:|---|
| analyst(MODEL) | 2.63 | 0.6416 | ✅ XgaGb3J1 |
| analyst7(ANALYST) | 2.05 | **0.7973** | ❌ |
| OTHER(长窗) | 1.74 | — | ✅ npa9PKWw |
| 机构+analyst | 2.07 | **0.5485** | ✅ vRA82ogA |
| news(PV+NEWS) | 1.72 | 0.6587 | ⚠ 被 vRA82ogA 替换 |
| institutions | 1.57 | — | ❌ 差 0.01 |
| RISK | 1.37 | — | ❌ 族判死 |
| shortinterest 次级 | 1.11 | — | ❌ 族判死 |

⇒ **insiders 独立可交付上限 ≈ 4 颗**（已取 XgaGb3J1 / npa9PKWw / vRA82ogA + 存量的 qM7KxkQV）。

### 2.3 覆盖证书（无空格）

字段 42（insiders1 全 8 + insider_agg_matrix 30 可访问）× 矩 8 种 × 骨架 6 类 × 分组轴 4 × 非线性 6 × 配置 12 × 窗口 9 档（22/44/66/88/110/132/176/252/504）= 已穷尽。

## 三、判死清单（本战役累计）

| 族 / 数据集 | 判死依据 |
|---|---|
| insiders 非 holdings 维度 | 全灭，最高 1.29 |
| RISK（rsk60_crowding/offer/lending_fee_bid_rate）| 单腿 −0.24/−0.86，组合 ≤1.37 |
| SHORTINTEREST 次级（volatility/duration/count/min_rate）| 单腿 −1.12/−0.79，组合 ≤1.11 |
| other455 竞争PCA | 1.21（弱于关系PCA）|
| SENTIMENT 域名热度 | 单腿 0.72 |

## 四、距 20 颗还差 6 颗：路径

按 Goal 第 1 步「数据集全面扫描：针对当前 deu region 下的数据集逐一扫描」，DEU 高覆盖未用数据集：

| 数据集 | category | cov | 字段 | alpha 数 | 判断 |
|---|---|---:|---:|---:|---|
| **pattern_scores** | pv | 0.9888 | 504 | 277 | ★ K线形态，完全正交（BE151 已开探针）|
| **model264** | model | 0.9973 | 380 | 217 | trio 成员，需单独路线 |
| **pv29** | pv | 1.0 | 50 | 66 | ★ 聚类标签，可作分组轴 |
| **news18** | news | 0.8046 | 70 | 145 | ★ 非 trio，自由度高 |
| **pv30** | pv | 0.7273 | 285 | 325 | trio，需单独路线 |
| **analyst7** | analyst | 0.7207 | 608 | 4192 | 非 trio（已验证有效）|
| **fund_holdings_panel** | institutions | 0.9019 | 18 | 121 | 非 trio |
| **sentiment27** | sentiment | 0.9038 | 18 | 344 | 非 trio |

⇒ **6 颗的现实来源：pattern_scores / news18 / analyst7 / fund_holdings_panel / sentiment27 各出 1-2 颗。**
