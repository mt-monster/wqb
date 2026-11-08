# KOR × insiders5 wave294/295：持股集中度族与 decay 档（2026-11-06）

## 1. wave293 结构改进（decay 4 基线）

| alpha | 表达式 | S | F | TO | 2Y |
|---|---|---:|---:|---:|---:|
| 78L3N852 | multiply(-1, group_rank(ts_mean(ratio,5), sector)) | 1.44 | 1.19 | .0577 | 1.68 |
| npvmP9Kq | 同上换 market | **1.45** | 1.25 | .0605 | 1.64 |
| E56NR1GL | multiply(-1, ts_mean(group_rank(ratio, sector),5)) 先rank后平滑 | 1.44 | 1.19 | .0573 | 1.67 |
| vR1Z28kw | signed_power(ratio,2) 平方放大 | 1.44 | 1.19 | .0577 | 1.68 |
| **0mYxrqRp** | **multiply(-1, group_rank(ts_mean(1/(ratio+0.01),5), sector))** | **-1.63** | -1.43 | .0575 | **-2.04** |
| N1NLV07g | ts_scale 替 ts_mean | -1.19 | -0.48 | **.4894** | -1.42 |
| 2rA9mMlw | ts_decay_linear 替 ts_mean | 1.34 | 1.04 | .1295 | 0.34 |
| ZYQgA60x | ts_rank(...,250) 年内分位 | 0.60 | 0.27 | .0677 | 1.00 |

**要点**：
1. `signed_power(ratio,2)` 与基线逐位相同 ⇒ 放大端方向不对（信号在低比例端）。
2. `ts_decay_linear` 完全等价于无平滑（1.34/0.34）⇒ 2Y 杠杆必须是**等权 ts_mean**。
3. `ts_scale` 把 TO 从 .058 推到 **.4894**（8.5 倍）⇒ 直接不可用。
4. nanH ON 与 OFF 逐位相同（1.44/1.68）⇒ 该档对本族无意义。

## 2. wave294：倒数变换取正（验证「取负不翻转」）

对 0mYxrqRp（-1.63）去负号，预期 +1.63，实测：

| alpha | 表达式 | S | 2Y |
|---|---|---:|---:|
| QPvOYKVK | group_rank(ts_mean(1/(ratio+0.01),5), sector) | **1.43** | 1.67 |
| zq3grbR8 | 同上换 market | 1.44 | 1.62 |
| e75N6QxJ / wpQ39bE5 | 窗口 22 / 66 | 1.41 / 1.37 | 1.66 / 1.66 |
| j2Yoe86Z | 换 source_real_ratio | 1.43 | 1.67 |
| d5WYK1ZY | eps 0.001 | 1.43 | 1.67 |
| WjO3LeAQ | 无平滑 | 1.34 | 0.34 |

⛔ **「取负不翻转」实证**：-1.63 的镜像只有 **+1.43**，差 0.20。
原因：truncation 0.08 截断极端权重 + R&M 残差回归 ⇒ 权重非线性，镜像后极端权重落在不同股票。
⇒ 看到强负向候选**不能**假定「取正即同强度」，两臂必须各自回测。

## 3. wave295：decay 档扫描（意外发现）

decay 2 / decay 6 下跑**不带负号**的原式（4 条）：

| alpha | 表达式 | S | 2Y |
|---|---|---:|---:|
| 1YNONedJ | group_rank(ts_mean(ratio,5), sector) [decay2] | **-1.64** | -2.07 |
| leAEAdlN | group_rank(ts_mean(ratio,22), sector) [decay2] | **-1.62** | -2.06 |
| WjO3OMGO | group_rank(ts_mean(ratio,5), market) [decay2] | **-1.62** | -1.98 |
| 9qx8xYw1 | group_rank(ts_mean(ratio,5), sector) [decay6] | **-1.63** | -2.04 |
| 2rA9AMN8 | 倒数版（本就正向）[decay2] | 1.43 | 1.68 |

⚠ **注意**：对比 decay 4 下带 `multiply(-1)` 的同一结构只有 1.44 —— 需区分是「decay 更优」还是「负向臂本身更强」。
由「取负不翻转」规律，负向臂 -1.63 取正后未必到 1.63，**必须实测**。
⇒ 已派 wave296：decay 2 / decay 6 各 8 条**取正版**（`1FR52V8JN5eL8G5HzUkQWsP` / `3WQWBt2IW4kJcaaS2FToV4B`）。

## 4. 已确认的天花板与剩余杠杆

| 维度 | 已试 | 最好读数 |
|---|---|---:|
| 平滑窗口 | 无 / 5 / 22 / 66 / 252 | W5 → 1.44（窗口不敏感） |
| 分组轴 | sector / market / industry / subindustry | market 1.45 |
| 降维算子 | vec_avg / vec_max / vec_sum | vec_avg（vec_max -0.39、vec_sum -0.25） |
| 非线性 | 倒数 / 平方 / ts_rank / ts_scale / decay_linear | 倒数 1.43 |
| 字段口径 | source_ratio / source_real_ratio / real_ratio | source_ratio 1.44 |
| 中性化层 | 单层 / 双层 group_neutralize | 单层更优 |
| decay | 2 / 4 / 6 | 待 wave296 定论 |

⛔ **库藏股全族判死**（wave290 批 A，8 模板 max|S| 0.88）。
⛔ **tnc（关联方数量）2Y 结构性不可达**：四个分组/中性化变体 S 1.46–1.55 但 2Y 全在 -0.34~0.26。
⭐ **source_ratio（持股集中度）是有效机制**：S 1.44 / 2Y 1.68，距 1.58 差 0.14。