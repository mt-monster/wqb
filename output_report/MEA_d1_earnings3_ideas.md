**Dataset**: earnings3
**Region**: MEA
**Delay**: 1

# MEA earnings3 S1 ideas（TOP300/d1，财报日历，MATRIX 直接可用）

数据集理解：财报日历字段（距上次/下次财报交易日数、时段码），MATRIX 直接横截面运算。
cov≈0.5 有 CONCENTRATED_WEIGHT 风险 → 表达式必须带横截面 rank + COUNTRY 中性；
整数字段用 rank，禁 ts_mean 平滑（抹掉离散信息）。

**Concept**: 财报临近漂移（财报前买入窗口效应）
- **Mechanism**: 即将发布财报的公司获得事件前超额关注与买入
- **Fields**: `ern3_next_interval`
- **Implementation Example**: `-1 * rank({ern3_next_interval})`
- **Direction**: 负 interval（越临近财报越强）

**Concept**: 财报刚发布的短窗动量
- **Mechanism**: 刚披露财报的公司在披露后数日延续信息消化
- **Fields**: `ern3_pre_interval`
- **Implementation Example**: `rank(ts_delta({ern3_pre_interval},5))`
- **Direction**: 正

**Concept**: 披露节奏异常（延迟披露=坏消息假说）
- **Mechanism**: 距上次财报时间显著拉长的公司倾向隐藏坏消息，反向
- **Fields**: `ern3_pre_interval`
- **Implementation Example**: `-1 * rank(subtract({ern3_pre_interval},ts_mean({ern3_pre_interval},252)))`
- **Direction**: 负
