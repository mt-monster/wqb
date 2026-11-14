# ★替换方案：xAvK73Qg 取代 Jj8VQwoe（2026-11-11 23:30）

## 一、方案可行性已验证

用 `xAvK73Qg` 替换 `Jj8VQwoe` 后的 11 件组合：

```
all_below_threshold = True
max_mutually_below_subset_size = 11
pairs_over_threshold = 0
max_pair = zq3eb7No ~ RREPm361 = 0.6879
```

⇒ **替换后仍是 11 颗合法交付，且质量大幅提升。**

## 二、质量对比（同一位置）

| 项 | Jj8VQwoe（原） | xAvK73Qg（替换） | 变化 |
|---|---:|---:|---|
| Sharpe | 1.65 | **2.04** | **+0.39** |
| Fitness | 1.24 | **1.77** | **+0.53** |
| sub_universe | 1.22 | **1.45** | +0.23 |
| two_year | 2.42 | **2.81** | +0.39 |
| Turnover | 0.147 | 0.140 | 更优 |
| self | 0.565 | **0.542** | 更优 |
| 最差年 | **2016 -0.52（负年）** | **零负年**（最低 2017 +0.22） | **结构性更优** |

## 三、xAvK73Qg 四闸已验证

| 闸门 | 值 | 判定 |
|---|---|---|
| S | **2.04** | ✅ |
| F | **1.77** | ✅ |
| TO | 0.1401 | ✅ |
| sub | 1.45 | ✅ |
| 2Y | 2.81 | ✅ |
| self | **0.5424** | ✅ |
| 逐年 | 2014-2023 零空窗、**零负年** | ✅ |
| 与替代后 11 件互相关 | 全部 <0.7 | ✅ |
| **prod** | **终验中** | ⏳ |

**逐年明细**：

```
2014:3.26 2015:2.86 2016:0.68 2017:0.22 2018:2.13
2019:1.61 2020:1.27 2021:2.45 2022:3.37 2023:2.13
```

## 四、表达式

```
group_zscore(add(
  -group_rank(ts_delta(ts_backfill(vec_avg(max_loan_rate_p5_d1), 132), 220), sector),
  group_rank(ts_zscore(ts_backfill(vec_avg(oth47_organic_traffic), 132), 252), sector)
), market)
```

**与 Jj8VQwoe 的差别**：
- 第一腿：shrt3_bar Δ220 → **max_loan_rate_p5_d1 Δ220**（换更强的借券字段）
- 第二腿：oth47_organic_traffic **Δ66 quantile** → **水平 zscore252**（换矩：变化面→水平面）

有趣的是：BE26 之前测过「换字段」全部失败（0.719-0.785 撞 Jj8VQwoe），
但这一颗因为**同时换掉了第一腿**（shrt3_bar → max_loan_rate_p5_d1），才降到 0.762 以下可用区间。
⇒ 再次印证：**必须换数据集/换腿，换字段无效**。

## 五、待决

**是否用 xAvK73Qg 替换 Jj8VQwoe？**
- 支持：S/F/sub/2Y 全面更高、零负年、self 更低
- 代价：Jj8VQwoe 的 prod 0.6124 已实测通过；xAvK73Qg 的 prod 尚待测

建议：**若 xAvK73Qg prod <0.7，用替换方案**；否则保留 Jj8VQwoe。