# DEU/D1 insiders 战役实证明细（2026-11-12）

> 来源：DEU 区域 insiders 战役，约 30 波 / 400+ 臂。全部为平台真实读数。

## 一、互相关矩阵实证：复合核心 = 共同因子

固定核心 S7 = `A×C + B×FR + C + B`（A=Δ66持仓变化，B=ts_ir，C=HHI集中度，FR=新鲜度），换 8 个搭档族：

| 搭档族 | 最好 S | 与基准件互相关 | 能否入篮 |
|---|---:|---:|---|
| analyst(MODEL) | 2.63 | 0.6416 | ✅（另一颗进） |
| analyst7(ANALYST) | 2.05 | **0.7973** | ❌ |
| OTHER 长窗 | 1.74 | — | ✅ |
| 机构+analyst | 2.07 | **0.5485** | ✅ |
| news(PV+NEWS) | 1.72 | 0.6587 | ⚠ 被更优件替换 |
| institutions | 1.57 | — | ❌ 差 0.01 |
| RISK | 1.37 | — | ❌ 族判死 |
| shortinterest 次级 | 1.11 | — | ❌ 族判死 |

**同族内部**：S 1.50 / 1.54 / 1.55 / 1.57 四颗彼此 **0.93-0.98**（S7 的不同外壳：幂次、cap 桶、哪条腿乘 FR）。
⇒ 174+ 臂里所有「S 1.50-1.57」形态实质是同一个信号。

## 二、换核心的实测收益

| 核心 | 构造 | S | 与 S7 家族相关 |
|---|---|---:|---:|
| S7 四腿 | A×C + B×FR + C + B | 1.50-1.57 | 基准 |
| **C 单腿** | HHI 集中度 | **1.74-2.20** | **0.35-0.49** |
| B 单腿 | ts_ir 持续性 | **1.81** | 0.6355 |
| F 单腿 | 新鲜度 | **2.04** | 0.7252（撞车）|
| A 单腿 | Δ66 变化 | 1.72 | — |

**关键数据点**：`C + AS3 + AS4` = S 2.20 / F 1.64 / 2Y 2.43 / sub 1.42 / **11 算子**，
十年逐年 Sharpe：1.03 / 3.47 / 1.24 / 2.42 / 2.52 / 2.47 / 1.67 / 2.43 / 2.29 / 2.62
⇒ **最差年 1.03，零负年，无单年依赖**。

## 三、C 定义的尖峰性（不能改定义造变体）

| 定义 | 窗口 | S |
|---|---:|---:|
| **HHI 比值 SV1/(SV1+SV2+SV3+SV4)** | **66** | **1.74 / 2.20** |
| HHI 比值 | 22 | 1.56 |
| HHI 比值 | 132 | 1.18 |
| sum（SV1+SV2）| 66 | 1.63 |
| std_dev（离散度）| 66 | 1.15 |

## 四、insiders 数据集完整判死清单

| 维度 | 字段 | 结论 | 最好读数 |
|---|---|---|---|
| 持仓存量 | `insd1_holdings` | ✅ **唯一强信号** | S 2.36 |
| 最大单笔集中度 | `significant_value_1` HHI | ✅ **最强单腿核心** | S 2.20 |
| 第 2/3/4 大交易 | `significant_value_2/3/4` | ❌ | 1.61（fail2）|
| 交易金额 | `insd1_valueeur` / `insd1_value` | ❌ | 1.14 |
| 股数占比 | `insd1_shares/holdings` | ❌ | 1.29 |
| 显著度 | `insd1_tradesignificance` | ❌ | 1.21 |
| 交易价 | `insd1_price` | ❌ | 1.13 |
| 方向指标 | `directional_indicator` | ⚠ 仅辅助 | 单腿 0.51 |
| 买卖股数比 | `total_buy/sell_shares` | ❌ | — |
| 高管维度 | `avg_top_buy/sell_shares` | ❌ | 0.73-0.83 |

**经济解释**：内部人 alpha 来自**持仓的持续性变化**与**最大单笔交易的集中度**，
不是单笔交易的规模/显著性/价格。后者在 53% 覆盖率的稀疏数据上噪声主导。

## 五、其它数据集的判死记录

| 数据集 | category | cov | 最好 S | 判死依据 |
|---|---|---:|---:|---|
| model264（380 字段 ML 趋势概率）| model | 0.9973 | **0.74** | 8/10 臂为负；趋势方向已被价格反映 |
| pattern_scores（504 字段 K线形态）| pv | 0.9888 | **0.56** | 8/10 为负；形态相似度滞后且截面区分度低 |
| news50 事件新颖度/密度 | news | 0.7644 | 0.56 单腿负 | 事件结构维度无信息 |
| news18 叙事影响分 | news | 0.8046 | −0.38 单腿 | 同上 |
| risk60（rsk60_*）| risk | 0.835 | 1.37 | 单腿 −0.24 / −0.86 |
| shortinterest3 次级维度 | shortinterest | 0.7105 | 1.11 | 单腿 −1.12 / −0.79 |
| sentiment27 域名热度 | sentiment | 0.9038 | 1.37 | 单腿 0.72，sub 0.36 |
| institutions6 净买入比 | institutions | 1.0 | 1.57 | 与 C 配合只有 0.67-0.69 |
| other455 竞争 PCA | other | 0.9535 | 1.21 | 弱于关系 PCA（PC2）|

**唯一有效**：`news104` 的「情绪极性 × 相关度加权」（S 1.72）。

## 六、塔归属实证（易错字段）

| 字段 | 实际塔 | 直觉误判 |
|---|---|---|
| `predicted_surprise_f12m_ebitda_4` | **MODEL** | 以为 ANALYST |
| `mean_estimate_change_pct_f12m_ebitda_14d_4` | **MODEL** | 以为 ANALYST |
| `est_12m_ebi_raised_1wk` | ANALYST | 正确 |
| `rec_raisednum_4wks` | ANALYST | 正确 |
| `cap` | **PV** | 容易忘记它算一个 trio |

交叉验证方法：`get_alpha_details(alpha_id).pyramids.list` 的塔名反推分类构成。

## 七、算子压缩实测（详见 `wq-alpha-gate-push-op-min`）

| 档位 | 平台 operatorCount | S | F | 2Y | sub |
|---|---:|---:|---:|---:|---:|
| 原始 | 46 | 2.36 | 2.02 | 2.71 | 1.51 |
| 仅 n 元 add | 38 | 2.36 | 2.02 | 2.71 | 1.51 |
| n 元 add + 去 signed_power | 37 | 2.36 | **2.04** | 2.67 | **1.54** |
| **变量赋值去重** | **28** | **2.36** | **2.02** | **2.71** | **1.51** ← 逐位相同 |
| 变量合并 + 2AS + 去幂 | **23** | 2.28 | 1.95 | 2.44 | 1.53 |
| 纯 insiders | 19 | 1.42 | 1.16 | 2.17 | 0.73 ← 掉闸 |

**禁做**：删全部 analyst（S −0.94）、AS 先 add 再 rank（S −0.76，字段量纲差异）。

## 八、★闸5（equal_weight_leg_add）批量复核实证

**方法**：对 17 颗篮子逐颗读 `get_alpha_details().code`，跑
`gate._detect_equal_weight_leg_add(code, set())`。

**结果（2026-11-12 实测）**：

```
POISON_COUNT 13
POISON_IDS  leadEXnl, 0mPqGEgq, mLapKbd2, MP6OgoPr, npa9PKWw, bl6AvMkN,
            GrW9OxmG, zq3eb7No, qM7KxkQV, Jj8VQwoe, RREPm361, d5a2vxzY, 9qlz29Oe
CLEAN_IDS   WjlMlWJd, vR1oxZA3, rKRx2Alj, 78Yk8VR1
```

| 分类 | 颗数 | 说明 |
|---|---:|---|
| POISON（违反组合铁律）| **13** | 平台 checks 全过，但按铁律不可交付 |
| CLEAN | **4** | `WjlMlWJd` + 3 颗存量件（`vR1oxZA3` / `rKRx2Alj` / `78Yk8VR1`）|

### 判定边界实测

| 表达式 | 判定 |
|---|---|
| `signed_power(group_zscore(add(C腿, AS3腿, AS4腿),sector),1.3)`（leadEXnl）| **POISON** |
| `add(S7四腿, O4腿)`（npa9PKWw）| **POISON** |
| `add(ts_mean(close,22), ts_mean(close,66))` | OK（同形态不同窗）|
| `add(ts_mean(close,22), 0.01)` | OK（1 腿 + 标量）|

### 结论

**DEU insiders 战役的构造范式（单腿核心 + 跨族搭档）系统性违反闸5。**
整条路线的平台指标有效（S 2.20 / sub 1.42 / 十年无负年），但组合形态不合规。

⇒ 若要保留这些信号，必须**重构成单腿形态**：
- ❌ `add(C腿, AS3腿)`
- ✅ 单腿 + 同族多窗：`add(ts_mean(C,66), ts_mean(C,132))`
- ✅ 单机制内做时序/截面变换，不跨腿相加

⇒ 这也是「ATOM 优先」的真正价值：**坚持单数据集单塔，天然就不会去跨腿拼盘**。
