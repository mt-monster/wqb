# GBR news50 数据集经验（2026-11-08）

> 37 字段（mws50_*），aC 361，cov 0.691。category = NEWS。与 CHN news46 / mws46 同族（事件情绪指标）。

## 判死：双向都弱（±0.7 内）

rKRPAWv9 同款慢几何（tvr0.05/decay15/trunc0.05/densify(market) 反号）测 4 字段 × 双向 6 臂：

| 字段 | 反号 S | 翻正 S |
|---|---:|---:|
| mws50_ess | -0.44 | — |
| mws50_qmb | +0.55 | +0.65 |
| mws50_ens | -0.65 | +0.69 |
| mws50_nip | -0.69 | +0.65 |

⇒ 信号强度不足（非方向问题）。alpha id：N1NGXZbw / zq3EvVNO / xAroAM5m / gJe5JvLQ / leAYeQEO / 88RZ8aGX。

## GBR NEWS 塔终局
nws17（rKRPAWv9 在篮，prod 0.3998）是唯一出货面；nws18（论坛 2400 表达式 S0.05）、nws20（0.82）、news50（±0.7）、news104（0.81/0.90）全灭。**NEWS 塔不再扩。**
