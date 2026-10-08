# 稳健性提升扫批报告 — pw5RbrYX 设置轴（2026-10-08）

> 目的：回答「稳健性指标可以提高吗」。基线 pw5RbrYX 被 `brain-alpha-robustness` Phase C 判 REJECT
> （衰减比 0.188 < 0.30；近 3 年 max/min 6.69 > 5；CV 0.575 贴线）。
> 本轮按 `wq-brain-alpha-optimization-v1` **Mode A**（恰好 8 候选、冻结字段与数据集）扫设置轴。

## 1 候选与设置（8 条，均以基线为核心，单点变更）

| tag | 变更 | universe | neutralization | decay |
|---|---|---|---|---|
| W40 | `ts_mean` 窗口 20→40 | TOP3000 | STATISTICAL | 500 |
| W60 | 窗口 20→60 | TOP3000 | STATISTICAL | 500 |
| W120 | 窗口 20→120 | TOP3000 | STATISTICAL | 500 |
| TDL20 | `ts_mean`→`ts_decay_linear` | TOP3000 | STATISTICAL | 500 |
| GZ20 | `group_rank`→`group_zscore` | TOP3000 | STATISTICAL | 500 |
| U1000 | universe TOP3000→TOP1000 | TOP1000 | STATISTICAL | 500 |
| NEU_IND | 中性化 STATISTICAL→INDUSTRY | TOP3000 | INDUSTRY | 500 |
| NEU_SLOW | 中性化 STATISTICAL→SLOW | TOP3000 | SLOW | 500 |

纪律说明：按 `platform_constraints.json: quantile_arity=1` 将 `quantile(x, sigma=1.0)` **无损归一为 `quantile(x)`**
（平台签名 `quantile(x, driver=gaussian, sigma=1.0)`，默认值即 1.0，语义不变）；
不扫 truncation（D5 零杠杆）；decay 轴已由 perf_max 演示批耗尽（DECAY_DBL_512≈baseline）；nanHandling/maxTrade 属强度闸不动。

## 2 结果（8/8 收齐；逐年经 `get_alpha_yearly_stats`）

| tag | alpha_id | S | F | 2Y | sub | TO | 2021/2022/2023 Sharpe | max/min | 衰减比 | CV₀ | 平台 FAIL | 结局 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **基线 pw5RbrYX** | pw5RbrYX | 2.07 | 1.21 | 1.67 | 0.90 | .0375 | 1.78/2.61/**0.39** | 6.69 | 0.188 | 0.575 | — | 稳健性 REJECT |
| W40 | omWWG8WJ | 2.08 | 1.21 | 1.57 | 0.91 | .0363 | 1.67/2.56/0.22 | 11.64 | 0.106 | 0.65 | — | 更差（2Y 破线） |
| W60 | N1VVzQOE | 2.05 | 1.17 | 1.52 | 0.89 | .0354 | 1.70/2.61/0.06 | 43.50 | 0.029 | 0.72 | — | 更差 |
| W120 | kqggGnX6 | 2.01 | 1.11 | 1.43 | 0.89 | .0338 | 1.91/2.59/**-0.20** | — | -0.100 | 0.83 | — | 更差（2023 转负） |
| TDL20 | leKKGb9l | 2.04 | 1.19 | **1.66** | **0.92** | .0378 | 1.82/2.58/0.39 | 6.62 | 0.191 | 0.57 | — | **闸保持（横向平移）** |
| GZ20 | wpbbG69Y | **0.34** | 0.08 | -0.02 | 0.26 | — | — | — | — | — | LOW_SHARPE/FITNESS/2Y | **崩盘** |
| **U1000** | 9qWWMEde | 1.05 | 0.48 | **2.59** | 0.76 | .0527 | 0.59/3.10/**1.98** | **5.25** | **1.886** | 0.54 | — | 稳健性大幅改善，**S/F 跌出闸线** |
| NEU_IND | omWWGdlv | 1.86 | **1.33** | 1.57 | 0.74 | .0145 | 2.32/2.46/**0.63** | **3.90** | **0.339** | **0.46** | LOW_SUB_UNIVERSE_SHARPE, LOW_2Y_SHARPE | 稳健性达标，**平台双闸破** |
| NEU_SLOW | blOOzeMp | 1.86 | 1.06 | 1.34 | 0.61 | .0402 | 1.46/2.36/0.10 | 23.60 | 0.054 | 0.71 | LOW_SUB_UNIVERSE_SHARPE, LOW_2Y_SHARPE | 更差 |

## 3 结论（可迁移）

1. **★ 稳健性与平台闸之间存在真实前沿，没有免费午餐**。真正能拉近窗的只有两条杠杆，且各自付出不同代价：
   - **universe 收窄（TOP3000→TOP1000）**：2023 Sharpe **0.39→1.98**，衰减比 0.188→**1.886**，max/min 6.69→5.25，
     2Y 1.67→**2.59** —— 稳健性全面反转。代价：S 2.07→1.05、F 1.21→**0.48**，**跌破内部闸线（S≥1.25 / F≥1.0）**，不可提交。
   - **中性化换 INDUSTRY**：2023→**0.63**、衰减比→**0.339**（脱离 REJECT）、max/min→**3.90**、CV₀→**0.46**，
     且 Fitness **反升** 1.21→**1.33**（8 条最高）。代价：平台 `LOW_SUB_UNIVERSE_SHARPE` + `LOW_2Y_SHARPE` **双 FAIL**
     （2Y 1.57 仅差 0.01），sub 0.90→0.74。
2. **★ 窗口加长是反向杠杆（推翻本轮前的假设）**：W40/W60/W120 的 2023 Sharpe 依次降到 0.22 / 0.06 / **-0.20**，
   衰减比 0.106 / 0.029 / -0.100，2Y 依次 1.57 / 1.52 / 1.43（全部跌破 1.58）。
   这与 perf_max 演示批「窗口微扫是真业绩杠杆」并不矛盾——**窗口提升的是全期 S/F，牺牲的是近窗响应**；
   两个目标（总业绩 vs 近窗一致性）在本族上**方向相反**。
3. **`ts_decay_linear` 是安全但中性的替换**：TDL20 S 2.04 / F 1.19 / 2Y 1.66 / sub 0.92（sub 略优于基线）、
   2023 与基线同值 0.39，稳健性三指标无实质变化 ⇒ 只能作**横向替代**（唯一过闸入队的一条）。
4. **`group_rank`→`group_zscore` 在本族是灾难**（S 2.07→**0.34**，F→0.08，3 项平台 FAIL）：
   再次印证「非保序替换必须实测」，不可按等价算子默认放行。
5. **可实现性判定**：目标「两条硬线脱离 REJECT」在本族**已被实证可达**（NEU_IND 的 max/min 3.90 + 衰减 0.339），
   但**代价是平台 SUB/2Y 破**；反过来保住全部平台闸的 TDL20 拿不到任何稳健性增益。
   ⇒ 本族**不存在同时满足「平台全闸 + 稳健性三指标」的纯设置解**，出路只剩：
   (a) 组合腿救援（`salvage_pool boost_cw / boost_2y` 补 NEU_IND 的 SUB/2Y 缺口）；
   (b) Mode B 结构轴（改条件腿/分组轴/字段）；
   (c) 接受现状，pw5RbrYX 按知情放宽提交。

## 4 产物与去向

- 8 条 alpha 已全部落库/可查：见本目录 `score.json`、`sim_status.json`、`plan.json`。
- 可交付入队：**TDL20 = `leKKGb9l`** 已走 `submit_queue.py add` 补录 submit_ready（唯一过闸者）。
- 其余 7 条不入队（2Y 破线 / S-F 不足 / 平台 FAIL）。
