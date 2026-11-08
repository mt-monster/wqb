# Wave R7 派发（锚点增强 + M5 机制首测）

- multisim: `3Ymarsc054gBcyD18KAsVEYc`（8 条，2026-11-07 派发）
- 设置与 R4 **完全一致**（KOR/TOP600/D1 · STATISTICAL · decay4 · trunc0.08）以隔离表达式变量
- preflight: `valid=true` / `unknown_fields=[]` / `any_changed=false`

| # | 机制 | 算子 | 表达式 |
|---|---|---:|---|
| R7-01 | 收缩幅度 w126（窗口顺延） | 4 | `subtract(0.5, group_rank(ts_mean(subtract(rsk70_mfm2_asetrd_srisku, rsk70_mfm2_asetrd_srisk), 126), sector))` |
| R7-02 | 收缩幅度 w252 | 4 | 同上 252 |
| R7-03 | 多窗乘积 66×252 | 7 | `subtract(0.5, group_rank(multiply(ts_mean(D,66), ts_mean(D,252)), sector))` |
| R7-04 | 收缩幅度 w66 · subindustry 轴 | 4 | `subtract(0.5, group_rank(ts_mean(D,66), subindustry))` |
| R7-05 | winsorize 放在 rank **之后**（真杠杆） | 5 | `winsorize(subtract(0.5, group_rank(ts_mean(D,66), sector)), std=2)` |
| R7-06 | **M5 低 beta（BAB）首测** | 4 | `subtract(0.5, group_rank(ts_mean(rsk68_beta, 66), sector))` |
| R7-07 | M5×M4 合取（beta ∧ idvol，同为 rsk68） | 7 | `multiply(subtract(1, group_rank(ts_mean(rsk68_beta,66), sector)), subtract(1, group_rank(ts_mean(rsk68_weight_volatility_short,66), sector)))` |
| R7-08 | M1 风险调整反转（rsk68，未测字段） | 5 | `subtract(0.5, group_rank(ts_mean(divide(rsk68_residual_return, rsk68_weight_volatility_short), 5), sector))` |

## 设计依据
- R7-01/02/03：R4 证 22→66 窗口延长同时抬 S 与 2Y ⇒ 顺延 126/252 及多窗乘积。
- R7-04：R4 证 industry 轴差（0.90/0.75）；subindustry 未测，补一格轴多样性。
- R7-05：按记忆「winsorize 放在 group_rank **之前**是幂等装饰算子、之后才真改权重几何」。
- R7-06/07：M5 低 beta **整族从未测过**；`rsk68_beta` aC 74 最不拥挤、cov 1.0；BAB 全球稳健。
- R7-07 两腿同属 rsk68 ⇒ ATOM 合规；为**合取**（乘）非 add，不触碰「禁混信号调参」。
- R7-08：`rsk68_residual_return`（aC 180）与 `rsk70_asetrd_dsrt` 是不同字段，且用波动率做分母 = 风险调整几何，新结构。

## 在飞占用
- 槽 1：R1 `1WgkXqald4WFcAc8YbicIWN`（单字段直用 8 条，child_count=0 已卡 30min+，疑似僵尸）
- 槽 2：R7 `3Ymarsc054gBcyD18KAsVEYc`
