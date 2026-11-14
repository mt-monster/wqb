# ★★★第 19 颗诞生 + 第 20 颗候选（互相关冲突）：MODEL 塔 2Y 边界突破

日期：2026-11-12

## 一、关键突破手段：`group_neutralize(·, subindustry)` 双重中性化

在 predictive_starmine 上，把 `group_zscore(X, sector)` 再包一层 `group_neutralize(·, subindustry)`：

| 构造 | S | F | Y2 | sub | fails |
|---|---:|---:|---:|---:|---:|
| 基线 `group_zscore(5腿, sector)` | 1.86 | 1.52 | **1.57** | 1.31 | 1 |
| **双重 `group_zscore(group_neutralize(group_zscore(5腿,sector),subindustry),sector)`** | 1.83 | 1.46 | **1.63** | 1.32 | **0** |

**⇒ 2Y 从 1.57 抬到 1.63，跨过 1.58 硬边界。**
**⇒ 这是唯一能让 2Y 破界的杠杆**（decay/nan/truncation/neutralization/腿数/窗口/幂次全部试过无效）。

## 二、第 19 颗：`2r50PAzJ`（MODEL 单塔 ATOM，13 项全过）

```
group_zscore(group_neutralize(
  group_zscore(add(
    group_rank(ts_mean(predicted_surprise_pct_fy1_ebitda,5), sector),
    group_rank(ts_mean(predicted_surprise_pct_f12m_earnings_5,22), sector),
    group_rank(ts_mean(mean_estimate_change_pct_fy1_ebitda_30d_4,5), sector),
    group_rank(ts_mean(mean_estimate_change_pct_f12m_earnings_30d_5,66), sector),
    reverse(group_rank(ts_mean(analyst_downgrade_count_60d_3,5), sector))
  ), sector),
subindustry), sector)
```

| 指标 | 值 | 闸 |
|---|---:|---:|
| Sharpe | **1.83** | 1.58 ✅ |
| Fitness | **1.46** | 1.00 ✅ |
| 2Y Sharpe | **1.63** | 1.58 ✅ |
| Sub-Universe | **1.32** | 0.70 ✅ |
| Turnover | 15.6% | ✅ |
| checks.fail | **[]** | ✅ |
| pyramids.effective | **1**（DEU/D1/MODEL）| ATOM ✅ |
| failed_ra | **0** | ✅ |

**设置**：decay=0 / SUBINDUSTRY / nan=ON / truncation=0.08 / TOP500
**互相关**：vs 6XM87Zb7 **0.2569** / vs d5apW38x 0.3955 / vs WjlMlWJd **0.048** / vs leadEXnl 0.4545 ⇒ 完全独立

## 三、第 20 颗候选：`VkN9waPY`（全闸过但与第 19 颗同源）

```
group_zscore(group_neutralize(group_zscore(add(
  group_rank(ts_mean(predicted_surprise_pct_fy1_ebitda,5),sector),
  group_rank(ts_mean(predicted_surprise_pct_f12m_earnings_5,22),sector),
  reverse(group_rank(ts_mean(analyst_downgrade_count_60d_3,5),sector)
),sector),subindustry),sector)
```

| 指标 | 值 |
|---|---:|
| S | **1.66** |
| F | **1.26** |
| Y2 | **2.30** |
| sub | **1.23** |
| TO | 14.7% |
| checks.fail | **[]** |
| pyramids.effective | **1**（MODEL ATOM）|

**问题：与 `2r50PAzJ` 互相关 0.8324 > 0.7 ⇒ 两者只能取一席。**

## 四、当前真实战绩

| 序号 | alpha | S | F | Y2 | sub | 塔 | 备注 |
|---|---|---:|---:|---:|---:|---|---|
| 1-17 | 篮子存量 | 1.60-2.36 | | | | 多塔 | 平台全闸过 |
| **18** | **6XM87Zb7** | **1.87** | 1.06 | 1.91 | 1.08 | ANALYST | 全闸 ✅ |
| **19** | **2r50PAzJ** | **1.83** | 1.46 | 1.63 | 1.32 | MODEL | 全闸 ✅ |
| 20 候选 | VkN9waPY | 1.66 | 1.26 | 2.30 | 1.23 | MODEL | 全闸但与 #19 相关 0.83 |

**⇒ 实际可入篮 = 19 颗。距 20 颗差 1 颗，且必须是「与全部 19 颗互相关 <0.7」的新件。**

## 五、本轮被证伪的方向（累计 9 个）

| 方向 | 最高 S | 判定 |
|---|---:|---|
| RISK 塔（risk60/risk88）| 0.72 | ❌ |
| SENTIMENT 塔（sentiment27/7）| 0.72 | ❌ |
| INSTITUTIONS 塔（institutions6 cov=1.0）| 0.72 | ❌ |
| NEWS 塔（news104/17/18）| 0.58 | ❌ |
| PEAD（act_q_*_surprisemean）| 0.30 | ❌ |
| rec 评级族 | 1.03 | ❌ |
| est_q 季度族 | 0.30 | ❌ |
| net/gps/nav/ent/opr/grm/roa 主轴族 | 1.54（Y2 崩）| ❌ |
| insiders 双重中性化 | 1.37（无变化）| ❌ |

## 六、可复用教训

1. **覆盖率 1.0 ≠ 信号强**：institutions6 覆盖 1.0 但最高 S 0.72；机构持仓季度低频已被定价。
2. **2Y 边界突破要靠"结构外"的中性化层**，不是参数微调。`group_neutralize(subindustry)` 是唯一有效杠杆。
3. **同塔换腿仍会高相关**：`2r50PAzJ` 与 `VkN9waPY` 腿数不同但相关 0.83 —— 因为共享 surprise 两腿。
4. **DECAY=0 是 starmine 最优**：decay=4 使 Y2 从 1.51 掉到 1.36。
