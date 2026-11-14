# intraday_pv_feats + pattern_scores 首轮 20 臂：intraday 出 S 1.72（fails=[]）（2026-11-12）

> 探针判决后按改后设计派发两波（并发 2）。
> 波 A `2teNh2dtB5ez99910eolta6O`（intraday 10 臂，6 WARNING 0 ERROR）
> 波 B `4kReJz9Mj4TSbCGudmcXNv0`（pattern_scores 10 臂，0 ERROR）
> 全部 DEU/TOP500/D1｜decay4 / INDUSTRY / trunc0.08 / nan ON

## 一、★intraday_pv_feats：10 臂结果（本波最强件在这里）

| 臂 | 构造 | id | S | F | TO | Y2 | sub |
|---|---|---|---:|---:|---:|---:|---:|
| **D7** | **`skew_bid_ask_size_to_volume_ratio` 水平矩** | `npaRgLbE` | **1.72** | 0.59 | 65.7% | 1.45 | 0.82 |
| D3 | `avg_volume_to_last_trade_ratio` Δ22 取反 | `1YWb7r5J` | 1.29 | 0.38 | 65.1% | 0.68 | 0.12 |
| D10 | `ask/vwap_first_half` Δ66 取反 | `A1xZwo6w` | 1.16 | 0.46 | 33.4% | **2.20** | 0.49 |
| D8 | `avg_bid_to_ask_price_ratio` 水平矩 | `qM7rAQb1` | 1.08 | 0.44 | 31.3% | 0.58 | 0.52 |
| D1 | `vwap/last` Δ22 取反 | `qM7rAQZ1` | 0.79 | 0.20 | 61.4% | 1.28 | 0.11 |
| D2 | `ask/vwap` Δ22 取反 | `zqd69wGo` | 0.73 | 0.19 | 47.2% | 1.50 | 0.14 |
| D6 | `bid/ask_q4` Δ22 取反 | `leaOVoZN` | 0.73 | 0.19 | 53.3% | 0.45 | −0.10 |
| D5 | `ask_size_q4` Δ22 取反 | `0mP371WG` | 0.68 | 0.18 | 51.5% | 0.21 | 0.01 |
| D4 | `bid/vwap_first_half` Δ22 取反 | `KPgdbWRN` | 0.53 | 0.11 | 47.5% | 1.55 | −0.07 |
| D9 | `vwap/last` 负向门控 | `vRAMLW0a` | 0.16 | 0.03 | 27.6% | −0.16 | 0.01 |

### ★D7 是唯一 `fails=[]` 的件

```
group_rank(ts_zscore(skew_bid_ask_size_to_volume_ratio,252),industry)
```

| 项 | 值 |
|---|---|
| alpha id | **`npaRgLbE`** |
| Sharpe | **1.72** |
| Fitness | 0.59 |
| 2Y | 1.45 |
| Turnover | 65.7% |
| margin | 0.0238% |
| lc/sc | **185/187** ✅ |
| returns | 7.84% |
| **checks.fail** | **[] （空）** |
| checks.pass | **7 项**（LOW_SHARPE / LOW_TURNOVER / HIGH_TURNOVER / CONCENTRATED_WEIGHT / LOW_SUB_UNIVERSE_SHARPE / CLUSTER_TEST / MATCHES_PYRAMID） |
| checks.warning | **2 项**：`LOW_FITNESS` 0.59/LIMIT 1、`LOW_2Y_SHARPE` 1.45/LIMIT 1.58 |
| 塔 | **DEU/D1/PV，倍率 1.6，eff=1（ATOM）** |

**★这是本战役第一个 `fails=[]` 的 PV 塔件，且塔倍率 1.6。**

### 机制解读

`skew_bid_ask_size_to_volume_ratio` = **买卖盘挂单总量 / 成交量 的偏度**。
- 偏度高 ⇒ 挂单/成交比的分布**右偏**（少数时段挂单量远大于成交）⇒ 存在大额挂单压单但未成交 ⇒ **潜在压力未释放**；
- 偏度低 ⇒ 分布均匀或左偏 ⇒ 流动性供给平稳。
⇒ 经济含义：**它测的是日内订单簿的不平衡程度**，不是价格方向。与 Humphery-Jenner (2012)、Berkman-Erench-Koch (2012) 的日内流动性/收盘压力文献一脉相承。
⇒ **这是 PV 塔从未有过的机制面**（此前 PV 全部是流动性水平/动量/形态相似度）。

### 与研究前预测的对照

探针阶段我判断「变化矩为主、水平矩取反无效」，D7 却证明**水平矩在另一个字段上有效（1.72）**。
⇒ 说明「取反无效」只对 V1/V2 两个价量比字段成立，**不能外推到全部 585 个字段**。
⇒ 我在探针判决里写「水平矩取反路线不做」是对的（针对 V1/V2），但**不该因此放弃水平矩**——D7/D8 都是水平矩。

## 二、pattern_scores：10 臂全在噪声区（最高 0.82）

| 臂 | id | S | F | TO | Y2 | sub |
|---|---|---:|---:|---:|---:|---:|
| P4 v_bottom 正号 | `9ql1rZz1` | **−0.82** | −0.43 | 13.2% | −0.73 | −0.59 |
| P8 对称三角下行 正号 | `O0WPZQ0b` | **0.63** | 0.30 | 11.7% | 0.59 | 0.49 |
| P3 v_top 负号 | `zqd6mqlE` | −0.58 | −0.27 | 12.9% | −0.16 | −0.70 |
| P1 falling_wedge 正号 | `rK7glKZm` | 0.50 | 0.20 | 14.9% | 0.94 | 0.39 |
| P2 falling_wedge 负号 | `XgaQngdb` | −0.41 | −0.15 | 14.9% | −0.54 | −0.32 |
| P9 tri_dn Δ22 | `P05a3Q0M` | 0.33 | 0.10 | 15.7% | 0.37 | 0.37 |
| P5 gap_up 负号 | `O0WPZQ1b` | 0.26 | 0.06 | 20.5% | 0.13 | −0.04 |
| P7 tri_up 负号 | `balaZqGll`→`blaZqGll` | −0.24 | −0.07 | 15.7% | −0.55 | −0.48 |
| P10 wedge Δ22 | `kqar0Eq6` | 0.24 | 0.06 | 19.1% | 0.84 | 0.18 |
| P6 gap_dn 正号 | `WjlQG1EO` | 0.19 | 0.04 | 19.2% | 0.05 | −0.18 |

**读数特点**：
1. **TO 全部极低（11.7%-20.5%）** ⇒ 形态相似度是**慢变量**，日频变化很小。
2. **符号对照有效**：P1 wedge 正号 0.50 vs P2 负号 −0.41（差 0.91）；P8 tri_dn 正 0.63。
   ⇒ **方向可判**：楔形与下行对称三角是「正号」有效，V 型反转是「负号」方向（P4 正号 −0.82，说明该取负）。
3. **但天花板低**：最高的 P8 只有 0.63 / F 0.30，且 2Y 0.59。
4. **P4 的 −0.82 说明 V-bottom 相似度是反向信号**（越像底部反弹形态，后续越弱）——这是形态学的经典反直觉（形态被识别时往往已price in）。

⇒ **pattern_scores 首轮不进候选，但方向已探明**（wedge/tri_dn 取正、v_reversal 取负）。
  TO 11-20% 是它的优势（低换手 = 高 margin 潜力），值得二轮在正确方向上加组合。

## 三、两集对比

| | intraday_pv_feats | pattern_scores |
|---|---|---|
| 首轮最高 S | **1.72（fails=[]）** | 0.82（V-bottom 反号） |
| 正号最高 | 1.72 | 0.63 |
| TO 区间 | 16.7-65.7% | **11.7-20.5%** |
| margin 潜力 | 低（高 TO） | **高（低 TO）** |
| 机制 | 日内订单簿不平衡（**新机制**） | 技术形态相似度 |
| 结论 | **D7 进候选池，待破 F/2Y** | 方向已探明，二轮再做 |

## 四、D7 的两项 warning 与破法

| warning | 值/限 | 破法 |
|---|---|---|
| `LOW_FITNESS` | 0.59 / 1 | **降换手**（TO 65.7% → 目标 ≤30%）。按本战役纪律：**优先 `ts_mean` 外层平滑**（EUR 实证最有效），或 `ts_target_tvr_decay`（EUR 有效，`tvr_hump` 在 EUR 无效） |
| `LOW_2Y_SHARPE` | 1.45 / 1.58 | 差 0.13，**最接近的闸**。换分组轴（sector/subindustry）或 decay 档可能直接过 |

⇒ 二者可同时攻：**降换手会同时抬 margin→Fitness，且平滑对 2Y 的影响需实测**（本战役出现过长平滑杀 2Y 的反例）。

## 五、下一步（定向，不盲扫）

| 编号 | 动作 | 预期 |
|---|---|---|
| **G1** | D7 × `ts_mean` 外层 {5,8,12,22}，扫 TO–F–2Y 三角 | 找到 F≥1.0 且 2Y≥1.58 的点 |
| **G2** | D7 × `ts_target_tvr_decay` {τ=0.2,0.3,0.4} | EUR 有效手段，直接对齐换手 |
| **G3** | D7 × 分组轴 {industry, sector, subindustry} | 2Y 差 0.13，换轴可能直接过 |
| **G4** | D7 × decay {0,4,8,12} | 平台 decay 有单峰，必须扫 |

⇒ **G1+G2+G3 合并成 10 臂一波**，全部围绕 D7 单件定向优化。