# 7 颗候选提交价值评估（2026-11-16 17:1x）

> 对象：MP6l68aa / 2rAQ6mQN / kqNb1g5d / zqrgna91 / N1eLE1de / bla2k0Jq(备选) / e7adKz7g
> 判序：台账 → 硬闸（prod≥0.7 / self≥0.7 / 提交孪生 / 2Y）→ 塔六元组 → 六维 → 指标。**本轮零提交。**

## 结论先行

**7 颗里没有一颗值得提交。** 2 颗已落地或被取代、1 颗提交孪生封死、1 颗三重贴线、3 颗 prod 贴线且塔边际 0。

## 逐颗判定表（全维度）

| id | 状态 | S/F/2Y/sub | prod（余量） | self | 塔席位｜倍率｜当季 | 塔边际 | 六维 | 判定 |
|---|---|---|---|---|---|---|---|---|
| **bla2k0Jq** | **ACTIVE** | 1.80/1.25/1.63/0.90 | .5138 | .2485 | USA/OTHER｜1.4｜4（已亮） | 0 | 已兑现 | **已提交**（11-15 13:53），排除 |
| **e7adKz7g** | UNSUB | 1.72/1.00/2.08/0.91 | .6753 | .5496 | USA/EARNINGS｜1.3｜2 | +1（理论） | — | **SUPERSEDED**：精调件 wponnkmd 已 ACTIVE，同骨架 >0.99，不可交 |
| **2rAQ6mQN** | UNSUB | 2.38/2.02/2.57/1.04 | 未测 | — | USA/RISK 1.1+OTHER 1.4（均亮） | 0 | — | **DEAD_TWIN**：与已交 `88N6OOP7` 互相关 **0.9969**（仅 ts_corr 窗口 1008 vs 504）⇒ SELF_CORRELATION 必 FAIL |
| **kqNb1g5d** | UNSUB | 3.32/3.29/3.65/1.76 | **.6972（.0028！）** | **.6835（.0165）** | USA/INSIDERS 1.1（0）+OTHER 1.4（亮）混塔短板 1.1 | 0（OTHER 已亮，INSIDERS 1→2 未点亮） | T4 +3 新字段 | **三重高危**：prod 余量 .0028 + self 贴线 + investability **−0.5**（负）⇒ 不可交 |
| **MP6l68aa** | UNSUB | 2.20/1.28/3.17/1.22 | **.6897（.0103）** | .2966 | USA/OTHER｜1.4｜4（已亮） | **0** | T4 +2 新字段（`eur_signal_value_2/4`） | 指标强但 prod 贴线 + 塔边际 0 ⇒ 不值得占配额 |
| **zqrgna91** | UNSUB | 2.67/1.66/**1.68**/1.47 | **.6877（.0123）** | .3541 | USA/MODEL｜1.3｜4（已亮） | **0** | T4 +2 新字段 | prod 贴线 + 2Y 仅余 .10 + 塔边际 0 ⇒ 次选不交 |
| **N1eLE1de** | UNSUB | 2.63/1.54/2.07/1.66 | **.6916（.0084）** | .2804 | USA/MODEL｜1.3｜4（已亮） | **0** | T4 +2 新字段 | prod 贴线 + 塔边际 0 ⇒ 次选不交 |

## 关键论证

1. **已落地/被取代（2 颗）**：`bla2k0Jq` 11-15 已 ACTIVE；`e7adKz7g` 的精调件 `wponnkmd`（tail 0.15/0.85→0.18/0.82，S 1.72→1.77、F 1.00→1.03）11-16 17:06 已 ACTIVE，同骨架互相关必 >0.99，原件封死。
2. **提交孪生（1 颗）**：`2rAQ6mQN` 与 `88N6OOP7`（11-16 已交）表达式几乎相同，只差 `ts_corr` 窗口 1008 vs 504，`compute_mutual_correlation` = **0.9969** ⇒ 平台 `SELF_CORRELATION` 必 FAIL。这是当日有提交动作时 self 快筛会漏的假低值型（本例直接用互相关确认）。
3. **三重高危（1 颗）**：`kqNb1g5d` 虽 S3.32/F3.29/2Y3.65 极亮眼，但 prod **.6972**（余量 0.0028，平台任何漂移即破线）、self **.6835**、investability_sharpe **−0.5**（负）——三重叠加，且塔边际 0（OTHER 已亮，INSIDERS 1→2 远未点亮）。典型"指标诱人但不可交"。
4. **贴线且塔边际 0（3 颗）**：MP6l68aa / zqrgna91 / N1eLE1de 全闸通过、self 安全、六维 T4 都有新字段硬收益，但 prod 全部贴线（.6877~.6916，余量 .008~.012），且塔席位（USA/OTHER 4、USA/MODEL 4）**均已点亮**，塔边际 0。按项目「塔边际优先 + prod 贴线不占配额」纪律，不值得提交。
5. **解耦确认**：这 5 颗与今日全部 ACTIVE（wponnkmd / bla2k0Jq / 88N6OOP7）互相关全部 <0.11，无同席冲突——**排除的不是相关性，而是 prod 贴线与塔边际 0**。zqrgna91 ↔ N1eLE1de 互相关 0.4289（<0.5），彼此不互斥但同席同结论。

## 若一定要从中选一颗

`MP6l68aa` 相对最优（2Y 3.17 最强、prod 缓存 32h 最新、self .2966 安全、T4 +2 新字段），
但**仅在用户明确要求"贴线件也交"时才考虑**，且提交前必须当刻 `check_correlation(refresh=True)` 复核 prod 未漂过 0.7。
按纪律建议：**这 7 颗都不交，把 ET 剩余 2 席留给 A 档塔点亮件 `omEdka3v`（GBR/OTHER 2→3）**。

## 附：数据源

全部读数走 MCP：`batch_get_alpha_metrics` / `get_alpha_details` / `check_self_correlation` / `check_correlation` /
`compute_mutual_correlation` / `get_pyramid_alphas`（显式季度日期）/ `genius_tiebreak.py`（既有 CLI 算六维）。
塔计数当日：USA/OTHER=4、USA/MODEL=4、USA/EARNINGS=2、USA/INSIDERS=0。
