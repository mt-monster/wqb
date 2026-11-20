# EUR pv47 字段画像（2026-11-19，全字段探测 2/2）

> 数据集：`pv47`（PV 塔，EUR/D1 塔位 0/2 未点亮）。平台目录：`tracking/EUR/reference/eur_pv47_fields.json`（`get_datafields` EUR/TOP2500/D1 全量拉取，`complete=true`）。
> 本档案在归档时点**无任何 EUR 回测读数**（`backtest_results` 中 `code LIKE '%pv47%'` 且 region=EUR 零行）——分布特征栏标注「待实测」，回测读数栏将在探针波后补录。

## 字段全表（2 字段，逐字段实测栏位）

| 字段 | 类型 | 覆盖率 | userCount / alphaCount | onboard | 更新频率 | 分布特征 | 可用性 | 潜在 alpha 适用性 | EUR 实测读数 |
|---|---|---|---|---|---|---:|---|---|---|
| `pv47_spret` | MATRIX | 1.0 | 241 / 589 | 2025-11-01 | 日频（日度特异收益，描述明示 daily） | 待实测（GBR 同字段家族呈重尾、均值≈0，短窗求和后近似对称） | 中等拥挤（aC 589）；无判死记录 | **主信号**（特异收益反转 / 残差动量-反转混合）；短窗求和后取反=反转，长窗=残差动量延续 | 无（EUR 首测见探针波） |
| `pv47_for_statssimple_only_spret` | MATRIX | 1.0 | 307 / 712 | 2025-11-01 | 日频 | 待实测（与上字段同源，量纲为小数而非百分比） | 中等拥挤（aC 712）；无判死记录 | 主信号（与 `pv47_spret` 同源双口径，ATOM 时只能取一席）；量纲差异 ⇒ 同模板不可直接换用 | 无 |

## 结构判定（画像阶段）

- **两字段是同一机制的两套量纲**（percent vs fraction），互相关预期 ≈1 ⇒ ATOM 有效信息源 = **1 个**；取更冷门的 `pv47_spret`（aC 589）作主读数，另一字段只作量纲稳健性对照。
- **机制先验**：日度特异（非系统性）收益 ⇒ 两条已实证机制族：
  1. **短窗反转**（5–22 日求和取反）——GBR 侧 68 臂最好 S 1.78（`-rank(ts_sum(pv47_spret,22))` 族，多为 STATISTICAL 档）；论文锚：Jegadeesh (1990) 短周期反转、Lehmann (1990) 周反转。
  2. **残差动量**（长窗求和，22–252）——Blitz, Huij & Martens (2011) *Residual Momentum*（J. Empirical Finance）：残差动量比原始动量波动更低、回撤更小。
- ⚠ STATISTICAL/SLOW_AND_FAST 档读数不可作交付依据（EUR SOP §8 / 2026-11-13 定案）——GBR 那 68 臂的读数**只作机制先验**，EUR 探针一律用标准档（SUBINDUSTRY/INDUSTRY/MARKET/COUNTRY）。

## 探针计划（形态驱动，族探针优先）

1. 族探针 2 臂（判「时序型 vs 截面型」）：`group_rank(ts_sum(F,22))` 反转向 + `ts_rank(ts_sum(F,22),252)`；
2. 方向对照 1 臂：反转臂取反（对称性验证）；
3. 窗口梯度 3 档（5 / 22 / 66）；
4. 边界算子档按 `tracking/EUR/reference/boundary_ops_eur.json` 合法档执行。

设置：EUR/TOP2500/D1、SUBINDUSTRY、decay 4、trunc 0.08、nan ON、maxTrade OFF（区域缺省）。
