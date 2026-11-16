# `e7aeJoEd` 双目标优化（op-min）· 2026-11-15

> 目标 A = 推到平台全闸通过；目标 B = 压 `operatorCount` 到最少。**本轮零提交**（提交权归用户）。

> **【15:14 状态更新】`O0Wkvqgd` 已由用户点名提交、平台落地 `ACTIVE`**，`dateSubmitted` = ET 2026-11-15 02:14:06，命名 `IND_R_earnresid_01`，tags `CH_REG/SRC_earnings3/W115/EXPRFAM_regression_resid`。塔 **`IND/D1/EARNINGS` 2→3 点亮**（`IND/D1/PV` 11→12）。提交时 `prod_gate` .4741（delta 0.0 诚实）、`quota_gate` REGULAR 1/4 剩 3、方案 D ΔS +0.11/ΔF +0.03/ΔRet +0.0019 放行、稳健台账 `PASS`。原点 `e7aeJoEd` 与其余 11 个参数/消融变体全部标 `SUPERSEDED`（同骨架互相关 ≥0.99，提交后自动封死）。ET 11-15 REGULAR 实际 2/4（bla2k0Jq + 本件），剩 2。

## 0 结论（先看这个）

| 目标 | 状态 | 依据 |
|---|---|---|
| **A 全闸** | **已达成，无需改动** | 10 项 checks 全 PASS，仅 `MATCHES_COMPETITION`/`MATCHES_THEMES` 两个评奖类 WARNING；最薄一环 `IS_LADDER_SHARPE` **2.13 / limit 2.02**（余量 +0.11） |
| **B 压算子** | **不可压缩，6 已是下限** | 平台 `operatorCount = 6`（清单里记的 8 是旧口径，需更正）。仅有的两个可删项全部承重：删 `reverse` → S **−2.38**（精确反号、5 闸 FAIL）；删 `rank` → S **1.30** / F 0.91 / 2Y 0.76（3 项 RA fail）。触发终止条件「再删会掉闸」 |
| **参数通道（意外收获）** | **`ts_backfill 20→10` 全面更优** | `O0Wkvqgd`：S **2.45** / F **1.83** / 2Y **2.22** / robust **1.94** vs 原件 2.38 / 1.72 / 2.13 / 1.91；算子数不变（6）；全闸 PASS、0 RA FAIL；self **.4744** 低于原件 .5074 |
| **相关性复检（回源实测）** | **`O0Wkvqgd` prod/self 双低** | prod **.4741**（余量 .226）vs 原件 **.5124**（余量 .188）；self **.4744** vs .5074 ⇒ 双口径均更安全，prod 直方图 0.4–0.5 桶仅 11 颗、非单钉 |

## 1 采集（平台实值）

- 表达式：`rank(-ts_regression(ts_zscore(returns, 252), ts_zscore(ts_backfill(ern3_pre_interval, 20), 252), 252, rettype=0))`
- settings：IND / TOP500 / delay 1 / **decay 126** / **STATISTICAL** / truncation .08 / **nanHandling OFF** / pasteurisation ON
- 指标：S 2.38 / F 1.72 / TO 22.26% / Ret 11.62% / DD 4.84% / margin 10.44bp / 2Y 2.13 / ladder 2.13(限 2.02) / sub 1.83 / robust 1.91
- `operatorCount`（平台 `regular.operatorCount`）= **6**：`ts_zscore×2`、`rank`、`reverse`(=`-x` 语法糖)、`ts_regression`、`ts_backfill`
- 塔：`IND/D1/PV` 1.1 + `IND/D1/EARNINGS` 1.1（effective 2，木桶短板按 1.1）
- self 复核（OS 池 55 / 全池 63，排除 PPAC 8）：**max .5074**（top `RREnK5R1`）；13:53 新提交的 `bla2k0Jq` **未毒化**，同骨架无提交孪生 ⇒ 无封死风险

## 2 实测矩阵（全部单条 `create_simulation`，settings 与原件逐位一致）

| # | 通道 | 变体 | alpha | S | F | 2Y/ladder | sub | robust | 全闸 | 判定 |
|---|---|---|---|---:|---:|---:|---:|---:|---|---|
| 0 | 基线 | 原件重跑 | `ZYaxejgZ` | 2.38 | 1.72 | 2.13 | 1.83 | 1.91 | PASS | 复现一致 |
| 1 | 删 | 删 `reverse` | `j2aXbnoo` / `blaMZjVl` | **−2.38** | −1.72 | −2.00 | −1.83 | −1.91 | 5 FAIL | **回滚（承重）** |
| 2 | 删 | 删 `rank` | `QP0jk8Rp` / `omavMnJ2` | 1.30 | 0.91 | 0.76 | 1.63 | 1.51 | 3 RA fail | **回滚（承重）** |
| 3 | 换 | `rank`→`zscore` | `VkNEgMa0` / `QP0jLnNQ` | 1.92 | 1.32 | **0.49** | 1.47 | 1.58 | ladder WARN → RA fail | 不采纳 |
| 4 | 换 | `ts_regression`→`ts_corr` | `O0Wkevxb` / `e7aKonVN` | −0.22 | −0.06 | −0.20 | −0.27 | −0.36 | 5 FAIL | 不采纳（残差≠相关） |
| 5 | 参数 | `bf 20→63` | `mLaA30Zp` | 2.34 | 1.62 | 2.04 | 1.91 | 1.93 | PASS | 略逊原件 |
| 6 | 参数 | **`bf 20→10`** | **`O0Wkvqgd`** / `Grm6pnzZ` | **2.45** | **1.83** | 2.22 | 1.75 | **1.94** | **PASS / 0 RA fail** | **最优** |
| 7 | 参数 | `rettype=0→1` | `xAvQ62Rw` | **−0.49** | −0.20 | −0.81 | −1.17 | −0.84 | 5 FAIL | 回滚（`rettype=0` 承重） |
| 8 | 参数 | 三窗同降 126 | `npaoMneE` | 1.68 | 1.02 | 2.22 | 1.38 | 1.18 | PASS（cluster .98 贴线） | 不采纳（S 掉 0.70） |
| 9 | 参数 | 三窗同升 504 | `omavMnG2` | 2.32 | 1.65 | **2.50** | 1.55 | 1.44 | PASS | 次优（2Y 最高，S/sub 更低） |
| 10 | 参数 | zscore 窗 126 | `QP0jLnzQ` | 2.22 | 1.54 | 2.27 | 1.71 | 1.64 | PASS | 不采纳 |
| 11 | 参数 | zscore 窗 504 | `e7aKonGN` | 2.21 | 1.52 | 2.07 | 1.72 | 1.67 | PASS | 不采纳 |

## 3 逐层归因（L1–L4）

| 层 | 算子 | 作用 | 删/换结果 ⇒ 结论 |
|---|---|---|---|
| L4 终算子 | `rank` | 全截面秩，压尾部、修 `CONCENTRATED_WEIGHT` | S 2.38→1.30、ladder 2.13→0.76 ⇒ **承重** |
| 符号层 | `reverse`（`-x`） | 整式取负，决定多空方向 | S 精确反号 −2.38 ⇒ **承重（删=翻信号）** |
| L3 | `ts_regression(..., rettype=0)` | 收益对事件强度回归后的**残差**＝去趋势后的异常反应 | `rettype=1` → S −0.49；换 `ts_corr` → S −0.22 ⇒ **残差语义不可替代** |
| L3 | `ts_zscore(·, 252)` ×2 | 两端一年期风险调整，使残差可比 | 换 `zscore`（截面）→ 2Y 0.49 崩 ⇒ **时序标准化必需** |
| L3 | `ts_backfill(·, 20)` | 事件型字段前向填充 | **非承重但可调优**：10 更好、63 略逊 ⇒ 20 非最优档 |
| L1/L2 | 字段/比率层 | 单一 `returns` + `ern3_pre_interval`，无冗余包裹、无重复子式 | 变量合并通道 **0 收益**（两处 `ts_zscore` 参数不同，非重复子式） |

## 4 采纳建议

1. **压缩：不采纳任何删除。** 6 个算子全部有用，`operatorCount=6` 是该骨架的物理下限；继续压只能靠换骨架（超出本 skill 边界）。
2. **参数：`O0Wkvqgd`（`bf 20→10`）为本轮最优参数变体。** 同算子数下 S +0.07 / F +0.11 / 2Y +0.09 / robust +0.03，self 由 .5074 降至 **.4744**（更优），代价是 sub 1.83→1.75（仍远超 0.78 线）。
3. **只能留 1 颗**：`O0Wkvqgd` 与 `e7aeJoEd` 同骨架、仅参数不同，互相关必然 >0.99；最终提交哪颗需二选一，另一颗标 `SUPERSEDED`。
4. **取舍结论（已完成回源）：建议改交 `O0Wkvqgd`**，`e7aeJoEd` 标 `SUPERSEDED`。三项判据全占优：

| 项 | `e7aeJoEd`（原点） | `O0Wkvqgd`（bf=10） | 方向 |
|---|---:|---:|---|
| Sharpe | 2.38 | **2.45** | +0.07 |
| Fitness | 1.72 | **1.83** | +0.11 |
| 2Y / ladder | 2.13 / 限 2.02（余量 .11） | **2.22**（余量 **.20**） | +0.09 |
| robust_universe | 1.91 | **1.94** | +0.03 |
| sub_universe | **1.83** | 1.75（限 .78） | −0.08 |
| **prod** | .5124（余量 .188） | **.4741**（余量 **.226**） | **更安全** |
| **self** | .5074 | **.4744** | **更安全** |
| operatorCount | 6 | 6 | 持平 |
| 塔归属 | PV + EARNINGS | PV + EARNINGS | 持平 |

   - 唯一退让项是 sub 1.83→1.75，仍为限值 0.78 的 2.2 倍，不构成阻碍。
   - **提交前置（本轮未做，属 skill 边界外）**：① 方案 D 边际贡献 `performance_comparison` 未测（新件无池内记录）；② 稳健台账 `robustness_O0Wkvqgd` 无记录，提交前需跑审计或显式声明；③ 提交后原点与全部参数变体同骨架互相关 ≥0.99，其余必须标 `SUPERSEDED`。

## 5 纪律与产物

- **只挖不提交**：本轮全部动作为 `create_simulation`（派发回测），零 `POST /submit`。
- 覆盖签核：`results/op_coverage_signoff.jsonl`（session `opmin-e7aeJoEd-20261115`，12 条，coverage 8.3%，7 类算子逐类过审结论见 note 字段）。
- ⚠ **新踩的坑（值得沉淀）**：`submit_batch` 的 10 条 multisim 返回 `201` 后**整批 0 children / 零 alpha 落地**（B 批 2 条正常），`batch_status`/`harvest_multisim_alphas` 均报 `No children found` 持续 6 分钟以上，无报错。改用单条 `create_simulation` 后 12 条全部正常返回全量指标。⇒ **多候选消融优先用单条 `create_simulation`，不要用 10 条 multisim 批**。
- ⚠ 平台对 `returns` 字段回带 `Overused data` WARNING，但**不影响指标产出**（harvest 已读到完整 metrics），可忽略。
- 参数变体与原件同骨架，注意 11-15 铁律：**一旦其中一颗被提交，同骨架其余变体 self 自动 ≥0.99 全族封死**。
