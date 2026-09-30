# pv37 探针波 W1 —— tick 级价格/成交量路径统计（8 机制快判死）

**Dataset**: pv37
**Region**: AMR
**Delay**: 1

> 战役纪律：AMR 新集 8 探针快判死（无 |S|>=0.5 即 dead_end）。每概念 1-2 字段、2-4 算子、
> 标准窗口（5/22/66/252）、禁 add(A,B) 加权混腿、禁 bid/ask 盘口与日内反转等跨区死结构。

**Concept**: 交易下行压力——trade downtick 计数持续偏高 = 卖压在交易层面聚集，截面上高卖压股随后反转修复
- **Implementation Example**: `group_rank(ts_mean({tdts_06_tss}, 22), subindustry)`
- **Rationale**: 字段 pv37_tdts_06_tss（Trade Downticks TSS 6M）；Expected Exposure=卖压/交易方向压力；形状族 group_rank；时间尺度 22；分组轴 subindustry；算子数 3。

**Concept**: 量比动量——累计量比 22 日变化抬升 = 量能扩张期动量延续，衰减 = 量能退潮
- **Implementation Example**: `ts_rank(ts_delta({cvr_06_tss}, 22), 252)`
- **Rationale**: 字段 pv37_cvr_06_tss（Cumulative Volume Ratio TSS 6M）；Expected Exposure=量能扩张/动量；形状族 ts_rank；时间尺度 22/252；算子数 3。

**Concept**: 量能方向不对称——上行量收益超过下行量收益 = 买盘主导的量能结构（单一价差信号，非混腿）
- **Implementation Example**: `subtract(rank({upvret}), rank({downvret}))`
- **Rationale**: 字段 pv37_upvret + pv37_downvret（2 字段）；Expected Exposure=买卖盘量能不对称；形状族 subtract 价差几何；算子数 3。

**Concept**: kink 密度变化——price kink 计数短窗突增 = 价格路径转折点变密，波动结构切换前兆，随后均值回归
- **Implementation Example**: `ts_zscore(ts_delta({pks_06_tss}, 5), 22)`
- **Rationale**: 字段 pv37_pks_06_tss（Price Kinks TSS 6M）；Expected Exposure=波动结构/路径转折；形状族 ts_zscore；时间尺度 5/22；算子数 3。

**Concept**: 量比期限结构——短窗量比超长窗 = 近期量能异常放大的结构，短期过度反应后回归
- **Implementation Example**: `subtract(rank({cvr_03_tss}), rank({cvr_06_tss}))`
- **Rationale**: 字段 pv37_cvr_03_tss + pv37_cvr_06_tss（2 字段）；Expected Exposure=量能期限结构/短期过度反应；形状族 subtract 价差几何；算子数 3。

**Concept**: 量价背离——累计量能 profile 抬升而每 downtick 累计收益走弱 = 量增价滞背离，反向为量价齐升
- **Implementation Example**: `divide(rank(ts_delta({cvp_06_tss}, 66)), rank(ts_delta({crpdts}, 66)))`
- **Rationale**: 字段 pv37_cvp_06_tss + pv37_crpdts（2 字段）；Expected Exposure=量价背离；形状族 divide 比率几何（实证优于 add 2.3 倍）；时间尺度 66/252；算子数 4。

**Concept**: tick 密度比值——trade tick / volume tick 计数比 = 单笔规模倒数代理，比值高 = 小单密集散户主导，拥挤反转
- **Implementation Example**: `rank(divide({tdts_03_tss}, {vdts_03_tss}))`
- **Rationale**: 字段 pv37_tdts_03_tss + pv37_vdts_03_tss（2 字段）；Expected Exposure=单笔规模/散户拥挤；形状族 divide 比率几何；算子数 3。

**Concept**: 累计下行收益衰减——每 downtick 累计收益长窗衰减 = 卖压耗尽反弹修复，持续抬升 = 卖压延续
- **Implementation Example**: `group_rank(ts_decay_linear(ts_delta({crpdts}, 22), 5), subindustry)`
- **Rationale**: 字段 pv37_crpdts（Cumulative Return per Downtick Sample）；Expected Exposure=卖压耗尽/修复；形状族 group_rank + ts_decay_linear；时间尺度 5/22；分组轴 subindustry；算子数 4。
