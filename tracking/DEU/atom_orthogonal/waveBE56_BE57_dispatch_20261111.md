# BE56/BE57 派发（2026-11-11）

## BE56 · pv30 积压首批 10 臂（sim 1BGtSn81n4HQ8GFSTmVHekv）

波次 s2_pv30_d1 的 33 条从未回测表达式（PV 塔未点亮 ⇒ ATOM）：
4 条 days_from_last_change(sign(<PC 分量>)) + 6 条相对因子动量 divide(ts_delta(PC_i)-ts_delta(PC_j), |PC_i|+|PC_j|)。
全清单见 pv30_backlog_33_expressions.md。

## BE57 · institutions1 压缩版冠军配方 + 正交面 6 臂（sim 26bSES5Sz4T38A1199tJKDji）

| 臂 | 构造 | 目的 |
|---|---|---|
| 1 | 信念比值 × 显著性累计权重，industry | 复现冠军（压缩到 ≤12 算子） |
| 2 | 同上，sector | 分组轴对照 |
| 3 | 平均单笔金额（valueeur/笔数） | **正交面**：去掉 holdings 分母 |
| 4 | 股数分子比值 × 笔数门 | **正交面**：换分子 + 多笔协同（CMP 机会型） |
| 5 | 最大单笔/总单笔 | **正交面**：大额交易集中度 |
| 6 | 持仓存量水平 zscore252 | **正交面**：存量 vs 流量（论坛字段正交表空格） |

全部 ≤12 算子、全部单数据集 ATRIX（INSTITUTIONS 塔未点亮）、无禁混问题。
变量绑定（r = ...; t = ...）被 MCP 静态闸拒（validator 不识别赋值名），故全部改为无变量展开。