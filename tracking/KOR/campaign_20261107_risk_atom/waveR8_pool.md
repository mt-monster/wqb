# Wave R8 池（risk59 深扫 · 8 个互异几何 · preflight 待跑）

> 依据 gate_correction_and_attribution.md §D：risk59 aC ≤122，比 risk70(8018) 白一个量级。
> risk59 全字段为 **VECTOR** ⇒ 必须 vec_avg 包裹。机制：M2 融券约束溢价 / M3 空头挤压。
> 预算：算子数全部 ≤ 7（上限 12）。

| # | 机制 | 几何 | 算子 | 表达式 |
|---|---|---|---:|---|
| R8-01 | M2 费率 | w22 水平 · sector | 5 | subtract(0.5, group_rank(ts_mean(vec_avg(rsk59_bid_rate), 22), sector)) |
| R8-02 | M2 利用率 | w22 水平 · sector | 5 | subtract(0.5, group_rank(ts_mean(vec_avg(rsk59_s3utilization), 22), sector)) |
| R8-03 | M2 回补天数 | w66 **ts_rank 时序分位** | 5 | subtract(0.5, group_rank(ts_rank(vec_avg(rsk59_daystocover10day), 66), sector)) |
| R8-04 | **M3 挤压反臂** | 做多高挤压（R4 只测了做空臂 −0.17） | 5 | subtract(group_rank(ts_mean(vec_avg(rsk59_squeeze_risk), 22), sector), 0.5) |
| R8-05 | M2 拥挤分 | **ts_zscore 252** 时序标准化几何 | 5 | subtract(0.5, group_rank(ts_zscore(vec_avg(rsk59_crowded_score), 252), sector)) |
| R8-06 | M2 借券稀缺度 | **经济比值** 利用率÷可借量 | 6 | subtract(0.5, group_rank(ts_mean(divide(vec_avg(rsk59_s3utilization), add(vec_avg(rsk59_indicativeavailability), 1)), 22), sector)) |
| R8-07 | M2 费率-存量联动 | **交叉 ts_corr 几何** | 6 | subtract(0.5, group_rank(ts_corr(vec_avg(rsk59_bid_rate), vec_avg(rsk59_short_interest), 66), sector)) |
| R8-08 | M2 双维度**合取** | 费率 ∧ 利用率（同集，乘非加） | 7 | multiply(subtract(1, group_rank(ts_mean(vec_avg(rsk59_bid_rate), 22), sector)), subtract(1, group_rank(ts_mean(vec_avg(rsk59_s3utilization), 22), sector))) |

## 预案（若 R8 全灭）— 已修正（2026-11-07 实查字段）

⛔ **不能用 risk71 / risk72 兜底**：实查其全部字段均为 `*_dsrt`（残差收益）：
- risk71: asi_top1000_liquidity_dsrt / asi_top1500_liquidity_dsrt / rsk71_eqy_asi_supported_minvol1m_dsrt / rsk71_eqy_xjpci_supported_minvol1m_dsrt … 覆盖仅 **0.378–0.908**
- risk72: rsk72_asi_top1000/1500/2000_eqy_dsrt / rsk72_eqy_asi_supported_minvol1m_dsrt … 覆盖仅 **0.353–0.759**
⇒ 这两集**只有反转族字段**，而反转族已按 two-year-sharpe-playbook §4 正式判死（RAM/CROWDING 也无效）⇒ 派了必空。

可用兜底顺序：
1. **risk70 剩余非风格字段**：`cnt_kor`（韩国国家因子载荷，aC 428，KOR 专属，**从未做信号**）、`srtindcnt`（仅当过中性化轴）、`resvol`（试过 w66，S 0.66/2Y 1.32，可换几何再试）
2. **risk68 未试字段**：`weight_dadv`(aC 95) / `weight_edadv`(aC 99) —— 流动性/规模壳，宜做门控而非主信号
3. **risk88**（aC 1418）：`ri_*` 风格载荷与 `ind_*` 行业载荷**从未做信号**（`ase1_dsrt` 属反转族，不再用）
4. 若上述亦空 ⇒ 按 wq-brain-ra-kor 决策表记录「KOR Risk 单数据集无 10 颗可达 S≥1.58/F≥1.0/2Y≥1.58」并出**达成上限报告**，而不是硬凑。

## 合规自检
- 全部单数据集（risk59）⇒ **ATOM 合规**，不占两塔配额。
- 无 PV/MODEL/OTHER/FUNDAMENTAL 字段 ⇒ 不触碰禁混集合。
- 无 inst_pnl() / convert()。
