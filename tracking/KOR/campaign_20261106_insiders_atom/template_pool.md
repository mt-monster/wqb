# 模板池 · KOR × insiders5（12 个结构互异模板）

> 用户硬约束：模板库 ≥10 个，且差异必须落在**骨架结构 / 算子几何 / 矩（水平·一阶差分·二阶方差）/ 分组轴 / 非线性变换**上，不能只换窗口或常数。
> 来源标注：`FM`=平台论坛、`PP`=外部论文、`SB`=本区自建（实证驱动）。
> 记号：`F`=insiders5 字段，`W`=窗口，`sector`=分组轴。

| # | 模板名 | 骨架 | 所测的「矩 / 几何」 | 来源 | 首次派发 |
|---|---|---|---|---|---|
| **T01** | 分歧度时序均值 | `subtract(0.5, group_rank(ts_mean(vec_stddev(F), W), sector))` | 二阶矩（横截面离散）× 一阶时序平滑 | PP（Miller 1977 分歧-高估）+ SB（wave290 实证 1.62/1.76） | Wave1-A |
| **T02** | 分歧度时序分位 | `subtract(0.5, group_rank(ts_rank(vec_stddev(F), 250), sector))` | 二阶矩 × **自身分布位置**（非水平） | SB | Wave2 |
| **T03** | 分歧度自身偏离 | `subtract(0.5, group_rank(ts_zscore(vec_stddev(F), 252), sector))` | 二阶矩 × 自身标准化（去公司基线） | SB | Wave2 |
| **T04** | 净增持流量比 | `group_rank(ts_mean(divide(vec_sum(signed), add(vec_sum(base), 1)), W), sector)` | **比值**（去规模），一阶 | FM（「计数全灭、比值活着」） | Wave1-B |
| **T05** | 单位持股交易额 | `subtract(0.5, group_rank(ts_mean(divide(vec_sum(trd_amt), add(vec_sum(holdings), 1)), W), sector))` | **强度标准化**（货币/存量） | SB | Wave1-B |
| **T06** | 增持加速度 | `subtract(0.5, group_rank(ts_delta(ts_sum(vec_avg(ghc_tr), W1), W2), sector))` | **二阶时序差分**（修正加速度） | SB | Wave1-B |
| **T07** | 极值聚合 | `subtract(0.5, group_rank(ts_mean(vec_max(F), W), sector))` | **极值**（vs 均值/方差，捕捉单笔主导） | SB（wave287 T7 曾用 vec_max） | Wave1-B |
| **T08** | 自身常态偏离（净流） | `subtract(0.5, group_rank(ts_zscore(vec_sum(F), 252), sector))` | 一阶 × 自身 252 日 z 分数（事件门槛化） | FM（「显著超出自身一年常态才开仓」） | Wave1-B |
| **T09** | 变异系数 | `subtract(0.5, group_rank(ts_mean(divide(vec_stddev(F), add(abs(vec_avg(F)), eps)), W), sector))` | **归一化二阶矩**（分歧/方向强度） | SB | Wave1-B |
| **T10** | 存量集中度倒数 | `group_rank(ts_mean(divide(1, add(vec_avg(F), eps)), 5), sector)` | **单调非线性变换**（压缩右尾） | SB（wave294 实证：倒数把 1.44 → 1.63 同向臂） | Wave2 |
| **T11** | P-ATOM-1 壳 | `ts_target_tvr_decay(signed_power(group_rank(winsorize(rank(ts_backfill(F, bf)), std=s), sector), p), target_tvr=0.22)` | **壳层**（winsorize + 幂 + 换手目标） | SB（risk70 战役 KOR 实测 1.1→1.63） | Wave2 |
| **T12** | 事件门控 | `trade_when(greater(vec_avg(officer), 0.5), <T01 信号>, -1)` | **条件门控**（高管子集） | PP（Cohen-Malloy-Pomorski 2012 机会型 vs 例行型） | Wave2 |

**辅助轴（不单独算模板，但按「等价算子替换」列入扫描）**
- 分组轴：`sector / industry / subindustry / market`（KOR 单国 ⇒ country 无效）
- 时序平滑器：`ts_mean`（2Y 专用杠杆，等权）/ `ts_decay_linear`（实测等价无平滑）/ `ts_rank`
- 降维：`vec_avg / vec_sum / vec_max / vec_stddev / vec_count`
- 中性化档：`REVERSION_AND_MOMENTUM`（insiders 家族基线）/ `STATISTICAL` / `CROWDING` / `SLOW` / `FAST`

**多样性自检（每波开波前）**：本波用到的模板编号数 ≥2；全战役累计覆盖 ≥10；同一模板最多 3 个变体进同波。
