# Wave N6 破墙战报（0mYgpJzK 家族，进行中）— 2026-11-07

## 基准与验收状态
冠军 0mYgpJzK = multiply(group_rank(ts_delta(P5,5),sector), group_rank(ts_mean(P20_22),sector))
S 1.89 / F 1.28 / 2Y 2.21 / TO 0.279 / **raFail 0**；逐年 10/10 全正（2014-2023，pnl 全>0）；self 0.5368 过。
**prod = 0.8182 未过**（[0.8,0.9)=1 单钉 + [0.7,0.8)=11）⇒ 按「n=1 单钉先归因后破墙」纪律开 N6。

## N6 已收（4/12）

| 变体 | alpha | S | F | 2Y | TO | raFail | prod |
|---|---|---:|---:|---:|---:|---:|---:|
| delta10 × level22 | ZYQz7XZx | 1.79 | 1.31 | 2.03 | 0.2223 | 0 | **0.8271** ✗ |
| **delta5 × level60** | 6Xd0lGxE | 1.79 | 1.20 | 2.11 | 0.2748 | 0 | **0.7946** ✗（[0.8,0.9) 清空） |
| subindustry 合取 | vR1GkKOQ | 1.53 | 0.83 | 1.73 | 0.2852 | 2 | - |
| zscore×zscore | 1YNKxqNQ | -1.05 | -0.42 | -1.08 | 0.4798 | 5 | - |

## 归因
1. delta 窗口位移（5→10）不动 prod（0.8182→0.8271）——TO 变化不改变与 prod 池的信号重叠。
2. **换合取腿（level22→level60）有效**：prod −0.024 且 [0.8,0.9) 清空——60d 概率与 20d 概率在被占用的 prod 构建里不同族。
3. zscore 几何翻转方向（−1.05）——rank 乘法的方向依赖分位几何，zscore 直接弃用。
4. subindustry 在此轴 hurt（与估值轴相反）。

## 待收杠杆（在飞）
winsorize 后置 / delta3 / delta10×level60 / decay8 合取 / trunc04 合取。
下一波 N7 = 组合最强去相关杠杆（level60 + decay/trunc 赢家 + 混合几何）。

附：N5 全谱——smooth22 1.19、subindustry 1.09 均劣于合取；N4b5——region 估值 subindustry 1.26（≈global 1.28，同一底层）、估值散度 0.64。