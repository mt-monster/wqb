**Dataset**: analyst7
**Region**: MEA
**Delay**: 1

# MEA analyst7 S1 ideas（TOP300/d1，Broker Estimates 辅线，VECTOR）

数据集理解：券商一致预期与修正数据。
禁入：est_q_*_raisednum/lowerednum_1mth 升降差族（自家池 14+ 高分变体，SELF 蚕食铁律）。
只做幅度型修正/快闪背离/目标价变化等正交方向。

**Concept**: 4 周修正幅度动量（区别于广度型升降差）
- **Mechanism**: 一致预期均值相对 4 周前的修正幅度，捕捉分析师集体转向强度
- **Fields**: `est_q_pre_mean`, `est_q_pre_mean_4wks_ago`
- **Implementation Example**: `rank(divide(subtract({est_q_pre_mean},{est_q_pre_mean_4wks_ago}),abs({est_q_pre_mean_4wks_ago})))`
- **Direction**: 正

**Concept**: 快闪-稳定共识背离（短期情绪裂口）
- **Mechanism**: 28 天窗口预期与稳定共识的裂口代表新信息冲击
- **Fields**: `est_q_pre_mean_28d`, `est_q_pre_mean`
- **Implementation Example**: `rank(subtract({est_q_pre_mean_28d},{est_q_pre_mean}))`
- **Direction**: 正

**Concept**: 盈利预期加速度（3 个月修正速率）
- **Mechanism**: EPS 预期三个月变化相对基准的速率
- **Fields**: `est_q_eps_mean`, `est_q_eps_mean_3mth_ago`
- **Implementation Example**: `rank(divide(subtract({est_q_eps_mean},{est_q_eps_mean_3mth_ago}),abs({est_q_eps_mean_3mth_ago})))`
- **Direction**: 正

**Concept**: 目标价修正动量（MATRIX 短窗）
- **Mechanism**: 分析师目标价 21 日变化，机构定价意图
- **Fields**: `analyst_price_target_mean`
- **Implementation Example**: `rank(ts_delta({analyst_price_target_mean},21))`
- **Direction**: 正
