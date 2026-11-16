# `1YWLbqMQ` 双目标优化（op-min）· 2026-11-15

> 目标 A = 推到平台全闸；目标 B = 压 `operatorCount`。**本轮零提交**。

## 0 结论：双目标均失败，建议判死（或转 repair 换骨架）

| 目标 | 结果 | 依据 |
|---|---|---|
| **A 推全闸** | **失败（结构性）** | 7 条实测，最优变体 `YPamlq9A`（`ts_quantile 840→252`）S **1.40** / F **0.73** / sub **0.49** / 2Y **1.45**，**仍是 4 项 FAIL**。差距：S −0.18、F −0.27、sub −0.10、2Y −0.03 |
| **B 压算子** | **部分成功但不够** | 变量合并零损失：`vec_sum(holder_account_total)` 出现 2 次 ⇒ 10 → **9**；仍 **> 8**（项目硬闸）。再省 1 个只能删承重块，实测一律崩 |

**根因是门控与换手/子宇宙的硬耦合**：
- 门控在（`trade_when(ts_arg_max(a,90) < 33, …)`）⇒ sub **0.38**（限 0.59）FAIL，但 TO 只 19.8%
- 门控去 ⇒ sub **0.92 过线**，但 TO 翻倍到 **38.4%** ⇒ F 掉到 **0.47**，S 仍 1.35
- 不存在中间档：门控是 0/1 事件窗口，无部分生效形态

## 1 采集（平台实值）

- 表达式：`trade_when(ts_arg_max(vec_sum(holder_account_total), 90) < 33, signed_power(ts_quantile(divide(vec_sum(stable_boundary_trade_count_21d), ts_mean(vec_sum(holder_account_total), 72)), 840, driver=gaussian), 3.0), -1)`
- settings：USA / TOP3000 / delay 1 / **decay 9** / SUBINDUSTRY / trunc .08 / nanHandling ON
- 指标：S **1.36** / F **0.69** / TO 19.84% / Ret 5.13% / DD 4.89% / margin 5.17bp / sub **0.38** / 2Y **1.53**
- checks：**4 项 FAIL** = `LOW_SHARPE`(1.36/1.58)、`LOW_FITNESS`(0.69/1.0)、`LOW_SUB_UNIVERSE_SHARPE`(0.38/0.59)、`LOW_2Y_SHARPE`(1.53/1.58)；`CLUSTER_TEST` 0.80 WARNING（软线 1.58）
- `ra_failed_count = 4`，`ppa_failed_count = 1`
- **self = .3495**（安全，top `dK5ExGg` .3495）；塔 `USA/D1/INSTITUTIONS` 1.0
- 算子（本地口径 **9**，skill 解析器不支持中缀 `<` 故正则给出）：`trade_when` / `ts_arg_max` / `vec_sum`×3 / `less` / `signed_power` / `ts_quantile` / `divide` / `ts_mean`

## 2 实测矩阵（7 条单条仿真，settings 除注明外与原件逐位一致）

| # | 通道 | 变体 | alpha | S | F | TO | sub | 2Y | FAIL 数 | 判定 |
|---|---|---|---|---:|---:|---:|---:|---:|---:|---|
| 0 | 基线 | 原件 | `1YWLbqMQ` | 1.36 | 0.69 | .198 | 0.38 | 1.53 | 4 | — |
| 1 | **合并** | 变量合并（零损失） | `XgaLa69m` | **1.36** | **0.69** | **.198** | **0.38** | **1.53** | 4 | **指标逐位相同，10→9** |
| 2 | 删 | 删门控 `trade_when`+`ts_arg_max`+`less`（−3） | `78YQYzGb` | 1.35 | **0.47** | **.384** | **0.92** | 1.55 | 3 | sub 过线但 F 崩 |
| 3 | 删 | 删 `signed_power`（−1） | `wpo1oWl1` | **0.98** | 0.33 | .198 | 0.51 | 0.81 | 3 | **全崩，幂 3.0 承重** |
| 4 | 参 | `ts_quantile 840→252` | **`YPamlq9A`** | **1.40** | **0.73** | .197 | **0.49** | 1.45 | 4 | **本轮最优（仍不达标）** |
| 5 | 参 | `signed_power 3.0→2.0` | `zqdjAPzd` | 1.33 | 0.60 | .196 | 0.43 | 1.44 | 4 | 更差 ⇒ 3.0 最优 |
| 6 | 设置 | `decay 9→20` | `LLK68wdv` | **1.16** | 0.68 | .126 | 0.32 | 1.23 | 4 | 更差 ⇒ 9 最优 |
| 7 | 参 | `ts_mean 72→21` | `d5amYEvY` | 1.34 | 0.68 | .194 | 0.39 | 1.48 | 4 | 持平略差 ⇒ 72 最优 |

## 3 逐层归因

| 层 | 算子 | 作用 | 实测结论 |
|---|---|---|---|
| 门控 | `trade_when` + `ts_arg_max(a,90) < 33` + `less` | 只在「距 90 日持仓账户数峰值 ≤33 天」的事件窗口持仓 | **救 sub 的唯一手段，但代价是 TO 翻倍**；三算子合计 −3 |
| 尾部放大 | `signed_power(·, 3.0)` | 幂 3 放大两端尾部，是 S 的主要来源 | 删 → S **0.98**；降幂 2.0 → S 1.33 lower ⇒ **3.0 最优** |
| 时序分位 | `ts_quantile(·, 840, gaussian)` | 3.5 年窗口分位映射 | 缩短到 252 → S 1.40（+0.04）、sub 0.49（+0.11），**唯一正向**但仍不够 |
| 比率构造 | `divide(vec_sum(stable_boundary_trade_count_21d), ts_mean(a, 72))` | 稳定币边界交易数 / 持仓账户均值 = 人均活跃度 | ts_mean 21 持平略差 ⇒ 72 已优 |
| 聚合 | `vec_sum` ×3 | VECTOR 字段求和 | 两次 `vec_sum(holder_account_total)` 是**唯一零损失压缩点**（→ 变量合并） |

## 4 为什么推不上去（量化）

Fitness = `S × sqrt(|returns| / max(TO, 0.125))`。本件 `returns/TO = .0513/.1984 = .259` ⇒ sqrt = .509。
- 要 F ≥ 1.0 且 S ≥ 1.58，需 `returns/TO ≥ 0.40`；本件只有 **0.259**，缺口 55%
- 门控去掉后 `returns/TO = .046/.384 = .120` ⇒ 更差
- `decay 20` 降到 TO .126 但 S 同步掉到 1.16 ⇒ `ret/TO = .347`，F 仍 0.68

⇒ 该骨架的「单位换手收益」结构性偏低，不是旋钮能修的；**必须换信号结构**（例如把门控改成连续权重、或换掉 `stable_boundary_trade_count_21d` 这个高噪分子）。

## 5 判定与建议

- **判定：REJECT（结构性不达标）**，不属于「再调一轮就能过」的类型。
- 已完成 skill ⑥ 要求的杠杆扫描与消融扫描，触发止损条件。
- 建议路径（交用户决定）：
  1. **转 repair 换骨架**：门控改连续权重（`ts_rank(ts_arg_max(...), 90)` 作权重而非 0/1 门控），有望同时保住 sub 与 TO —— 这是唯一可能打破耦合的方向；
  2. 或直接判死该族，把预算投向 11-15 已确认的候选（`omEdka3v` / `rK7Qm6ld` / `6XdkW08J`）。
- 本件 self .3495 安全，**不是**相关性淘汰，纯指标问题。

## 6 产物

- 变量合并版：`XgaLa69m`（10→9，指标逐位相同，**唯一可采纳的压缩成果**）
- 最优指标版：`YPamlq9A`（`ts_quantile 252`，S 1.40 / F 0.73 / sub 0.49 / 2Y 1.45）
- 全部 7 颗新 alpha 均 `UNSUBMITTED`，无提交动作
- skill 自带解析器不支持 FASTEXPR 中缀 `<`（`op_count` 报「无法识别的字符」，`compress.py` 直接抛 `IndexError`），本轮改用人工消融；**该 bug 建议修 `scripts/` 的 tokenizer**
