# RReNkLv0 双目标优化报告（2026-11-17 09:2x）

> 目标 A = 推到全闸；目标 B = 压算子。**结论：REJECT_STRUCTURAL——16 条实测证明 S/F 与 2Y 反向权衡到顶，无剩余杠杆。原件 3 项 FAIL（S1.40/F0.93/2Y1.33），最优变体 `qM7govkP` 仍 2 项 FAIL（S1.42/F0.86，2Y 已救到 1.81）。本轮零提交。**
> 全程 MCP `create_multi_simulation` + `lookINTO_SimError_message` + `batch_get_alpha_metrics`，零临时脚本。

## 0 原件快照

`ts_target_tvr_decay(subtract(group_rank(<edgx_svol/edgx_total − (bats+byxx)_svol/(bats+byxx)_total>, industry), 0.5), target_tvr=0.1)`；USA/TOP3000/d1/decay1/CROWDING。8 算子、无重复子式（compress 0 候选、delete 0 候选）。

- FAIL：LOW_SHARPE 1.40<1.58｜LOW_FITNESS 0.93<1.0｜LOW_2Y_SHARPE 1.33<1.58
- PASS：TO 10.23%、CW、sub（LOW_SUB_UNIVERSE 0.78 过）
- self **.6592** 贴线过（top `PYGjZVx` 是 2025-06 老 OS 件已 DECOMMISSIONED，读数可信，非当日假低值）
- 塔 `USA/D1/SHORTINTEREST` ×1.1，当季 3 已亮 ⇒ **塔边际 0**（即使修好也不值得占配额）

## 1 四轮 16 条实测矩阵（全部同 settings 族）

| 通道 | 代表 id | S | F | 2Y | sub | 结论 |
|---|---|---:|---:|---:|---:|---|
| 原件（industry 轴） | RReNkLv0 | 1.40 | 0.93 | 1.33 | 0.78 | 3 FAIL |
| **L1 sector 轴** | omaVM1Pn | 1.06 | 0.70 | 1.21 | 0.59 | **反向失效**（又一次实证：group_rank 类信号换粗轴不保证涨） |
| **L1 subindustry 轴** | d5adA29x | **1.51** | **0.98** | 1.44 | 0.76 | 更好（+0.11 S），唯一正向杠杆 |
| L1 market 轴 | pwa8ArK6 | 0.96 | 0.68 | 1.08 | 0.60 | 崩 |
| ts_mean22 形态（11-15 交付对照） | RRednJ51 / GrmkpAeG | 1.08/1.33 | — | — | — | 差 |
| 中点 0.45 / 0.55 | 78YJEke5 / xAvR0KlN | 1.40 | 0.93 | 1.33 | 0.78 | **与 0.5 逐位相同**——group_rank 输出对称，中点平移不改变截面序（④d 邻域无效应的数学解释） |
| tvr 0.08 | LLKkALPa | 1.37 | 0.91 | 1.36 | 0.77 | 压 TO 反降 S |
| **tvr 0.12** | MP6koRL8 | 1.53 | 0.98 | 1.42 | 0.75 | subindustry 轴下最优组合 |
| tvr 0.14 | rK7AvJqj / mLaZMJ2X | 1.42 | 0.86 | 1.81 | 0.93 | 与 0.12 逐位同（**可达下限回退**，TO 已低于 target） |
| 无 tvr 包装 | d5adA52X | 1.67 | 0.29 | 1.30 | 0.69 | **TO 116% 爆表** ⇒ `ts_target_tvr_decay` 承重 |
| **ts_mean 平滑 66（+decay4）** | 2r5JbQqZ | 1.50 | 0.89 | **1.61** | 0.77 | **2Y 过闸**（+0.28） |
| **ts_mean 平滑 126（+decay4）** | **qM7govkP** | 1.42 | 0.86 | **1.81** | **0.93** | **2Y/sub 双过**，S 反降 |
| ts_mean 189 / 252 | O0WoEbLp / 1YWJQa8z | 1.31/1.17 | — | 1.82/1.65 | — | 126 是尖峰 |
| L2 双窗级联 multiply | 78YJE0qx | 1.10 | 0.74 | 1.38 | 0.77 | 失败 |
| decay 4（vs 1） | 全第四/五批 | — | — | — | — | fit 无净增益 |

## 2 根因：S/F ↔ 2Y 反向权衡，信息量天花板

- **2Y 的杠杆 = 时间平滑窗**：无平滑 1.33 → 66 日 1.61 → 126 日 1.81（+0.48）。但平滑同时把 S 从 1.51 压到 1.42——原始差分信号（edgx 空-short 占比 − (bats+byxx) 空-short 占比）的短期信息就是 S 的主要来源。
- **S 天花板 ≈1.4~1.5**：所有 16 条无一突破 1.53；差分结构（单数据集两腿）信息量决定。
- `industry` 轴下中点 0.45/0.55 逐位相同 ⇒ group_rank 对称性，中点参数无自由度。
- self .6592 贴线：任何同族变体相关只会 ≥ 原件，优化空间被 self 进一步锁死。

## 3 压算子（目标 B）

8 算子无自动压缩点（无重复子式、无冗余包裹）。`ts_target_tvr_decay` 承重（删它 TO 116%）；`subtract 0.5` 中点无自由度。**压缩终止：无可删算子。**

## 4 建议

1. **判死不提交**：塔边际 0（×1.1 低倍率 + 当季已亮）+ self 贴线 + 2 项 FAIL 修不掉。
2. 若重启此方向：换腿结构（非 `edgx−(bats+byxx)` 差分，如加第三腿或换 shrt43 其它字段对），或接受 subindustry+ts_mean126 形态做 SUPER 组合腿。
3. 建议 `seal_dead_end`：shrt43 单数据集两腿差分骨架（USA/TOP3000/CROWDING）。
4. 16 条变体全部标 `SUPERSEDED`（同骨架互相关 >0.99，只留原件与最优件中指标较好者，但均不可交故无实际保留意义）。

台账 `opmin_RReNkLv0`（USA, REJECT_STRUCTURAL）已落。
