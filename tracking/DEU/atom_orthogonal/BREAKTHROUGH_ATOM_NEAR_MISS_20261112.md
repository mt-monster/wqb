# ★ATOM 路线首次逼近：qM78pjkV S1.80/2Y1.51，只差 2Y 0.07

日期：2026-11-12
BE183 multisim 3PzAfg8rX4nKc2FHS7chIRp（predictive_starmine 单集 ATOM，10 臂）

## 一、结果（按 S 排序）

| 臂 | 构造 | S | F | 2Y | sub | TO | verdict |
|---|---|---:|---:|---:|---:|---:|---|
| **Q6 五腿+降级反** | qM78pjkV | **1.80** | **1.45** | **1.51** | **1.29** | 16.0% | BLOCKED（**仅 LOW_2Y 1.51<1.58**）|
| Q5 四腿 | pwamkjJv | 1.48 | 1.13 | 1.15 | 1.15 | 15.4% | BLOCKED（SHARPE+2Y）|
| Q2 修正30d双窗 | A1x95lqX | 1.36 | 0.95 | 0.38 | 0.89 | — | 3 项 |
| Q1 fy1%+f12m% | 78YWrjgZ | 1.29 | 0.93 | **1.72** | 1.12 | 14.1% | BLOCKED（SHARPE+F）|
| Q8 正交意外/修正 | ZYa697qZ | 1.20 | 0.67 | 0.34 | 0.89 | — | 3 项 |
| Q4 意外rank+修正 | P05Nb7rw | 1.17 | 0.59 | 0.57 | 1.17 | 24.4% | BLOCKED（3 项）|
| Q7 Δ+IR+降级 | E5Q1Ml09 | 1.05 | 0.67 | 0.09 | 1.06 | — | 3 项 |
| Q3 意外Δ+修正IR | 1YWeRwVQ | 0.61 | 0.34 | −0.15 | 0.94 | — | 3 项 |
| Q9 意外IR单腿 | 58Jx1l3M | 0.35 | 0.15 | −0.01 | 0.74 | — | 3 项 |
| Q10 修正Δ单腿 | N1P0G7q7 | −0.12 | −0.03 | −0.14 | −0.14 | — | 4 项 |

## 二、★★口径修正（重要）

**`checks.fail = []` 不等于「全闸通过」。**

三颗件用 `submit_verdict` 权威判定：
| alpha | checks.fail | metrics.failed_ra | **submit_verdict** |
|---|---|---|---|
| 78YWrjgZ | `[]` | 2 | **BLOCKED（LOW_SHARPE, LOW_FITNESS）** |
| P05Nb7rw | `[]` | 3 | **BLOCKED（LOW_SHARPE, LOW_FITNESS, LOW_2Y）** |
| qM78pjkV | LOW_2Y | 1 | **BLOCKED（LOW_2Y）** |

⇒ **`submit_verdict` 才是权威**（模拟层 checks + Failed-count 资格门 + 区域阈值）。
⇒ 只看 `checks.fail` 会误判。今后一律用 `submit_verdict` 做终判。

## 三、qM78pjkV 的完整画像（本轮最有价值的件）

```
S 1.80  |  F 1.45  |  2Y 1.51  |  sub 1.29  |  TO 16.0%
塔 MODEL（单塔）⇒ 真 ATOM  |  IS_LADDER_SHARPE 不出现  |  eff=1
唯一 fail: LOW_2Y_SHARPE 1.51 < 1.58（差 0.07）
```

**构造**（全部来自 predictive_starmine = 单数据集）：
```
fy1 意外% (5日) + f12m 盈利意外% (22日) + fy1 修正30d (5日)
  + f12m 修正30d (66日) + reverse(降级计数60d)  ⇒ 五腿朴素相加
```

## 四、与其它数据集单集上限的对比

| 数据集 | 单集最好 S | 2Y | 卡在哪 |
|---|---:|---:|---|
| **predictive_starmine** | **1.80** | **1.51** | **仅 2Y 差 0.07** |
| insiders1 | 1.33 | 1.16 | S 差 0.25 |
| insider_agg_matrix | 0.93 | 1.89 | S 差 0.65 |
| analyst7 | 0.80 | 0.93 | S 差 0.78 |

⇒ **starmine 是唯一逼近闸线的 ATOM 数据集**，且缺口从 0.25 缩到 0.07。

## 五、冲 2Y 的方向（BE184 已派）

既然 S 1.80 已过、只差 2Y 0.07，应针对「2Y」而非「S」优化。2Y 只看 2022-2023，
所以要加强**近两年有效的成分**：
- 降级计数 / 下调计数（近两年分析师修正更剧烈）→ 已在基线里，考虑加倍权重
- 短窗（5日）意外成分（近两年反应更快）
- fy2 意外、60d 修正（补时间维度）

BE184 `1i3wMd4uM4yBcwS19TLUk6wo` 10 臂：基线复现 + 逐项加腿 + 双计数加权 + 短窗为主。