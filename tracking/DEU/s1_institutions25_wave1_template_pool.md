# institutions25（基金做空行为）波 1 模板池 — 两读取证 + 方向定案

> 状态：设计定稿，**待 inst25p_20261103 探针（覆盖+方向）收批后派发**。纯单数据集 INSTITUTIONS 塔（非 trio）ATOM。
> 数据集：institutions25 Fund Short Selling Data（15+ VECTOR 字段，ac 7/uc 7，cov 0.0 系稀疏失真待逐年实测）。

## 一、论坛两读（2026-11-03）
- **WL27618《日度做空成交压力的释放：shortinterest18 杂谈》30 赞**：区分做市商对冲 vs 投机性做空；量比配合定位多空决战日。作者=si3 金帖同人（质量背书）。
- **ML10013《港股高拥挤度破局》**：⚠️ 「借贷利用率反转做多」踩价值陷阱（部分高拥挤=基本面真恶化）；正交架构=筹码枯竭×基本面预期。**未解决疑问面=如何分离价值陷阱腿**（受类别卡约束，只能条件/分组/残差）。
- **WL27618《融券借贷的隐形成本：risk59》29 赞**：借贷费率双面性=利空信号+轧空高危战场。
- **WL13229《18 个论文创意》**：做空行为主题——SRMIN5 极端低做空做多 0.468%/月持续≥2月（**照抄臂候选**）。
- **DA98440 多空不对称两帖（17+37 赞）**：归因纪律——分别看多/空仓 PnL，防单向噪声。

## 二、文献取证
- Huang-Ringgenberg-Zhang《The Information in Fire Sales》：基金经理优先卖高 short interest 股且未来**继续跌不反转** ⇒ 知情做空=负面信号代理。
- Boehmer-Jones-Zhang 2008：short interest 含预测信息（同向）。
- si3 反面实证：「极端拥挤反转做多」（T8 rank>0.9 门控）在 DEU/TOP500 = S −0.27 反噬 ⇒ 极限反转只留对照臂。

## 三、方向定案（探针 5/5 实测后**翻转**，2026-11-03 09:4x）
- **主轴=挤压效应正向**：探针反向臂 P1 crowding −0.22 / P3 concentration −0.28 / P4 activity −0.27 / P5 极限对照 −0.18 **四臂一致为负** ⇒ 正向 S +0.22~0.28 —— DEU/TOP500 上做空拥挤/集中/活跃的票未来偏强，**挤压效应一致压过知情做空效应**（与 si3 金帖「高利用率→轧空」一致，HRZ 文献方向在本区不成立）。
- age 0.07 平（P2，不带方向信息）。
- **水平面强度弱（正向 max 0.28）**：主攻面转**流面/动态面**（position_change/cover_count/short_count 突变——突变面出货规律），水平臂降为对照。
- 开放臂：manager_position_count 专注度、net 净开空流方向、trade_when 条件交互。

## 四、字段机制映射
- 知情深度面：age（空头年龄）、concentration（前三大）、manager_avg_trade_length（经理风格）。
- 拥挤面：crowding（分数）、manager_count（广度）、activity（笔数）。
- 流面：position_change（增减仓）、security_short_count（开空笔数）、security_cover_count（回补笔数）。
- 结构面：manager_position_count（专注度）、entry_position（建仓仓量）、is_open（开闭）。

## 五、模板清单（12 互异 · 家族 6 · 开放臂 ≥4）
- T1 crowding 反向水平 ts_mean22（探针 P1 同构）｜T2 age 反向｜T3 concentration 反向｜T4 activity 反向。
- T5 position_change 反向平滑（ts_mean22 后反向；稀疏字段先平滑）｜T6 short_count 反向突变（ts_delta(ts_mean(…,22),22)）｜T7 cover_count 正向水平（挤压臂）。
- T8 manager_position_count 专注度开放臂（正向）｜T9 manager_count 广度反向（拥挤数量维）。
- T10 cover_count 突增正向（挤压动态）｜T11 净开空流反向（subtract(short_count, cover_count) 同流净额合成 ✓）。
- T12 trade_when(age 高, crowding 反向, -1) 知情深度条件化（开放臂）。
- 窗口白名单 5/22/66/252；分组轴 subindustry/country 双轨（si3 实证杠杆有机制专属性，本波并行测）。

## 六、覆盖闸
- 全字段 cov 0.0 系稀疏失真不作判据（三证在案）；探针收批后逐颗 get_alpha_yearly_stats 验逐年 longCount+pnl 双零口径。

## 六·五、探针中途方向信号（inst25p 首批 2/5，2026-11-03 09:3x）
- P1 crowding 反向 S **−0.22**（VkxG1vOb）⇒ **拥挤度正向 +0.22 弱**：DEU/TOP500 挤压效应疑似压过知情做空（与 si3 金帖「高利用率→轧空」一致、与 HRZ 文献相反）。
- P2 age 反向 S 0.07（mLo5wPX5）平。
- 待 P3/P4/P5 收满后定案；若全批同向，模板池 T1-T4/T9/T11 方向翻正，负向降为对照。

## 七、派发实录（2026-11-03 inst25w1_20261103 · pid 57696 · 12 臂）
方向按 §三 定案（挤压正向）执行；探针已测的 w22 反向臂不原样重跑，升级为结构变体。双预检：preflight valid=true / unknown_fields=[]（warning=分页重试噪声，inst25_position_change 已实证在册）+ verify_expr 12/12 PASS。
- T1 `group_rank(ts_mean(vec_avg(inst25_crowding), 66), subindustry)` 拥挤水平正向·慢窗（家族1）
- T2 `group_rank(ts_mean(vec_avg(inst25_activity), 66), subindustry)` 活跃水平正向·慢窗（家族1）
- T3 `group_rank(ts_mean(vec_avg(inst25_manager_count), 22), subindustry)` 广度正向（家族1）
- T4 `group_rank(ts_mean(vec_avg(inst25_position_change), 22), subindustry)` 流面正向平滑（家族2·主攻）
- T5 `group_rank(ts_mean(subtract(vec_avg(inst25_security_short_count), vec_avg(inst25_security_cover_count)), 22), subindustry)` 净开空流反向（家族2·同流净额合成 ✓）
- T6 `group_rank(ts_delta(ts_mean(vec_avg(inst25_security_short_count), 22), 22), subindustry)` 开空笔数突增（家族3·突变面）
- T7 `group_rank(divide(ts_mean(vec_avg(inst25_security_cover_count), 22), add(...cover..., ...short...)), subindustry)` 回补占比（家族3·比率结构）
- T8 `group_rank(subtract(ts_mean(vec_avg(inst25_position_change), 5), ts_mean(vec_avg(inst25_position_change), 66)), subindustry)` 流加速度 5-66（家族3）
- T9 `trade_when(ts_mean(vec_avg(inst25_crowding), 22) > 0.7, group_rank(ts_mean(vec_avg(inst25_position_change), 22), subindustry), -1)` 拥挤条件化流面（家族4 开放臂）
- T10 `trade_when(ts_mean(vec_avg(inst25_age), 22) > 0.5, group_rank(ts_mean(subtract(...short..., ...cover...), 22), subindustry), -1)` 知情深度条件化（家族4 开放臂）
- T11 `group_rank(ts_mean(vec_avg(inst25_concentration), 22), country)` 分组轴双轨（家族5 · si3 心得①迁移）
- T12 `group_rank(ts_mean(vec_avg(inst25_manager_position_count), 22), subindustry)` 专注度开放臂（家族6）
- 窗口 5/22/66 白名单 ✓；trade_when 槽位（条件, 核心, -1）✓；量纲：全部 vec_avg 聚合后进算子 ✓。
- 待收批归因（按模板编号）+ 逐年覆盖闸 get_alpha_yearly_stats。

## 八、收批归因（2026-11-03 全 12/12 落 — 判弱封组合）
| 臂 | 表达式族 | S | 判 |
|---|---|---:|---|
| T1 crowding 慢窗66 | 家族1 水平 | 0.18 | 弱（w22 推断 0.22 → w66 更弱） |
| T2 activity 慢窗66 | 家族1 水平 | **0.52** | 水平面最佳，仍远低于 1.58 |
| T3 manager_count 广度 | 家族1 | 0.12 | 弱 |
| T4 position_change 流面 | 家族2 主攻 | 0.17 | 弱 |
| T5 净开空流 | 家族2 | 0.32 | 弱 |
| T6 开空笔数突增 | 家族3 突变 | 0.15 | 弱 |
| T7 回补占比 | 家族3 | **−0.44** | 死（比率结构反噬） |
| T8 流加速度 5-66 | 家族3 | 0.07 | 死 |
| T9 trade_when(crowding>0.7, 流面) | 家族4 开放 | 0.43 | 条件化有微弱信息 |
| T10 trade_when(age>0.5, 净开空流) | 家族4 开放 | **0.61** | **全批最佳**——信息住在条件交互里 |
| T11 concentration country | 家族5 | 0.23 | country 轴无增益（vs sub 0.28 推断） |
| T12 专注度 | 家族6 | −0.08 | 死 |

**结论**：① 突变/动态面全灭（T6-T8），推翻探针后「主攻流面/动态面」预案——inst25 流面在 DEU/TOP500 无突变信息；② 条件交互臂（T9/T10）全批最佳但天花板 0.61 < 1.58/2；③ country 分组轴对 inst25 无 si3 式增益（杠杆×机制面专属性再证）。**inst25 判弱封组合，不再追投**；与 snt7/sn12/snt27/sm12/si3 合并为「做空行为+注意力/情绪族 DEU 系统性弱」证据链（6 集）。覆盖闸免跑（判死不入库）。