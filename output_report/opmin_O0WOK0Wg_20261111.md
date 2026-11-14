# op-min：`O0WOK0Wg` 双目标优化报告（2026-11-11 20:2x–20:3x）

> **只挖不提交**，本轮零提交。提交权归用户点名。

## 0 结论

| 目标 | 结果 |
|---|---|
| **A 推指标到全闸通过** | ✅ 起始已达成（S1.68/F1.06/2Y1.64/sub1.27），本轮守住并改善 |
| **B 算子压到最少** | ✅ **14 → 8 ops**（−6，−43%）；8 是最小可行集 |
| **可提交？** | ✅ 硬闸全绿，但 **prod 0.6964 贴线**（余量 0.0036）⇒ 提交前 refresh 风险高 |

**交付件 `ZYa6x531`（8 ops）**
```
a = ts_mean(overall_sentiment_score, 66);
m = ts_mean(likelihood_of_neutral_tone, 66);
k = ts_corr(a, m, 252);
group_neutralize(ts_zscore(multiply(a, subtract(add(k, 2), m)), 252), industry)
```

**额外收益**：原式 `two_leg` 需三问 → 交付件 **`single_leg` 免三问**；ΔS 从 +0.08 升到 **+0.17**；原式 **2019 = −0.30 负年** → 交付件**十年零负年**。

---

## 1 起始状态

| 项 | 值 |
|---|---|
| id / 状态 | `O0WOK0Wg` / UNSUBMITTED REGULAR |
| settings | EUR / TOP2500 / D1 / decay 1 / MARKET / truncation 0.05 / nanHandling ON |
| 原式 14 ops | `ts_decay_linear(group_neutralize(signed_power(ts_zscore(multiply(ts_mean(S,66), add(ts_mean(1−P,66), subtract(1,ts_corr(...)))),252), 1.5), industry), 11)` |
| 指标 | S 1.68｜F **1.06**｜2Y 1.64｜sub 1.27/0.87｜CLUSTER 1.22 WARNING｜TO 0.0905｜ret 4.98% |
| prod | **0.6314**（`prod_peek` @20:01 + 平台复检 `passes_check=true`），余量 0.0686 |
| self | **0.1647** |
| 预检 | gate passed / failed_any=0 / ATOM:LAST_2Y / **two_leg 需三问** / ΔS **+0.08**（`EQUITY:EUR:1` 常规） |
| 逐年 | **2019 = −0.30 负年**、末年 0.96、CV10 **0.628 > 0.60** ⇒ 稳健不合格 |
| 塔 | `EUR/D1/EARNINGS` ×1.2 |

**背景**（`results/notes_da.md`，DA 波「Fitness 地板破解」）：反推出
`Fitness = S × sqrt(|returns| / max(TO, 0.125))`，本轮验算 `1.68·sqrt(0.0498/0.125)=1.0604` 与观测 1.06 完全吻合。
TO < 0.125 时地板生效 ⇒ 降换手对 F 无效；`signed_power` 是靠把 ret 从 4.11% 提到 4.98% 破 F 闸的唯一杠杆。
> 注：notes 记「signed_power 2」，平台 `regular.code` 实为参数 **1.5**；按「判定只走平台」以 1.5 为准。

**缺口**：无 FAIL，但 14 ops 远超必要；稳健 2019 负年 + CV 超标；prod 虽好但结构可简化。

---

## 2 压缩阶梯（1 批 / 10 条 FULL 仿真，`3mm5wXgVq4zQc2Z13QRafnk8`）

| # | id | ops | S | F | TO | ret | 2Y | sub | CL | 变体 |
|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| 1 | `A1x9bWWl` | 11 | 1.68 | 1.06 | .0905 | .0498 | 1.64 | 1.27/0.87 | 1.22 | **变量合并，逐位相同** ✅ |
| 2 | `e7amKpwp` | 10 | 1.72 | 1.04 | .1359 | .0500 | 1.94 | 1.25/0.89 | 1.10 | 再删 `ts_decay_linear` |
| 3 | `qM78d1rA` | **9** | 1.72 | 1.04 | .1359 | .0500 | 1.94 | 1.25/0.89 | 1.10 | **I1+I2 恒等式，逐位相同** ✅ |
| 4 | **`ZYa6x531`** | **8** | **1.74** | **1.01** | .0961 | .0425 | **1.88** | **1.33/0.90** | 1.16 | **删 `signed_power`，全闸仍过** ✅ |
| 5 | `lead2qbx` | 9 | **1.75** | **1.13** | .1212 | .0517 | **2.09** | **1.44/0.91** | 1.22 | `ts_zscore` 窗口 378（指标最佳但 2019 仍负年） |
| 6 | `E5Q1b7XR` | 9 | 1.61 | 0.88 | .1943 | .0587 | 1.83 | 1.10/0.84 | 0.96 | `signed_power` 参数 2.0 ⇒ F FAIL |
| 7 | `d5apmXAJ` | 9 | 1.74 | 1.06 | .1137 | .0461 | 1.94 | 1.30/0.90 | 1.15 | 参数 1.25 |
| 8 | `kqadX7lP` | 8 | 1.52 | 0.97 | .1050 | .0512 | 1.12 | 1.15/0.79 | 1.03 | 删 `group_neutralize` ⇒ 掉闸 |
| 9 | `O0WOkYv1` | 8 | 0.94 | 0.48 | .0602 | .0324 | 1.28 | 0.73/0.49 | 0.74 | 删 `ts_zscore` ⇒ 崩 |
| 10 | `MP6OXWAk` | 9 | 1.66 | 1.00 | .1359 | .0496 | 1.92 | 1.19/0.86 | 1.15 | `ts_corr` 窗口 504 |

本地：`op_count.py`、`plan.py`、`operator_coverage_audit.py --checklist`（84 算子逐类过审）、1 条 `op_coverage_signoff.jsonl` 签核。

---

## 3 三条实证

### ① 变量合并零损失 14 → 11

`ts_mean(S,66)` ×2、`ts_mean(1−P,66)` ×2、内层 `subtract(1,P)` ×2 ⇒ 单行 `a/b/c` 赋值合并后 `A1x9bWWl` 的 S/F/TO/ret/2Y/sub/CL **逐位相同**。再次验证「赋值不计数、重复调用才计数」，且 `--path` 按行解析必须用单行分号。

### ② Fitness 地板 × 删平滑 ⇒ `signed_power` 可删

- 原式 TO 0.0905 < 地板 0.125 ⇒ F 完全由 `S·sqrt(ret/0.125)` 决定，`signed_power` 靠提 ret 破闸。
- 删 `ts_decay_linear` 后 TO 升到 **0.1359 > 0.125**，地板不再锁死分母；同时 S 1.68→1.72、2Y 1.64→1.94。
- 于是删 `signed_power`（−1 op）后 F 仍 **1.01 ≥ 1.0**，全闸守住 ⇒ `ZYa6x531` 8 ops。
- 用公式验算：`1.74·sqrt(0.0425/0.125)=1.014` ≈ 观测 1.01；`lead2qbx` `1.75·sqrt(0.0517/0.125)=1.125` ≈ 1.13 ⇒ 公式在本族全程有效。

### ③ I1 + I2 恒等式（复用上一轮数学工具）

- **I1** `ts_mean(1−P,66)=1−ts_mean(P,66)` ⇒ `c=1−m`
- **I2** Pearson 仿射不变 ⇒ `ts_corr(a,1−m,252) = −ts_corr(a,m,252) = −k`
- 代入 `c+1−ρ = 2−m+k` ⇒ `multiply(a, subtract(add(k,2),m))`，**10→9 ops 且 `qM78d1rA` 与 `e7amKpwp` 逐位相同**。
- 常数 2 不可删（上一轮已证删后 S 1.74→0.41 全崩）。

### ④ 8 ops 是下限

删 `group_neutralize` / 删 `ts_zscore` 两条 8-ops 路径全部掉闸；再删任何算子会破坏 2Y 或 sub。

---

## 4 交付件与备选：prod 贴线的权衡

| 项 | **`ZYa6x531`（交付）** | `qM78d1rA`（备选） | `d5apmXAJ` |
|---|---|---|---|
| ops | **8** | 9 | 9 |
| S / F / 2Y | 1.74 / 1.01 / 1.88 | 1.72 / 1.04 / 1.94 | 1.74 / 1.06 / 1.94 |
| sub / CL | 1.33/0.90 / 1.16 | 1.25/0.89 / 1.10 | 1.30/0.90 / 1.15 |
| **prod（余量）** | **0.6964（0.0036 ⚠）** | **0.6509（0.0491）** | 0.6802（0.0198） |
| self | **0.1987** | 继承原式族 | — |
| ΔS | **+0.17**（`EUR:1:POWER_POOL` 4.80→4.97） | +0.08 量级（原式常规分区） | — |
| mix | **`single_leg` 免三问** ✅ | `two_leg` 需三问 | `two_leg` 需三问 |
| 逐年 | 零负年、min **0.61**、末年 1.10、CV **0.578** ✅ | 零负年但 2019 **0.23** 极弱、CV 0.546 | 零负年、2019 0.43、CV 0.555 |
| 稳健 | **PASS** | CONDITIONAL（极弱年） | CONDITIONAL |

`lead2qbx`（W378，指标数字最佳）因 **2019 = −0.04 负年**淘汰。

**取舍说明**：按铁律「op-min 交付件取全闸通过且算子最少那颗」⇒ `ZYa6x531`。
它同时免三问、ΔS 更高、逐年最健康，唯一代价是 prod 余量只有 0.0036（是 `qM78d1rA` 的 1/13.6）。
按项目记忆「prod 漂移猛、48h 作废」，**提交前 `refresh=True` 终验是硬要求**；若翻到 ≥0.7 ⇒ 递补 `qM78d1rA`（9 ops、prod 0.6509、需补三问）。

---

## 5 完整判据（`ZYa6x531`）

| 项 | 值 | 判定 |
|---|---|:---:|
| `submit_gate` | passed / failed_any=0 / hard_gate_warns=[] | ✅ |
| S / F / 2Y / sub | 1.74 / 1.01 / 1.88 / 1.33(0.90) | ✅ |
| CLUSTER | 1.16/1.58 WARNING（非 FAIL，gate 不拦） | ⚠ |
| 数据使用 | `SINGLE_DATA_SET` → ATOM 免 Ladder | ✅ |
| mix | `single_leg`，**narrative_required=false** | ✅ |
| ΔS | **+0.17**，`EQUITY:EUR:1:POWER_POOL`，dilutive=false | ✅ |
| self / prod | 0.1987 / **0.6964** | ✅ / ⚠ 贴线 |
| 逐年 | 十年零负年，min 0.61、末年 1.10、CV10 0.578 | ✅ PASS |
| 算子 | **8**（原式 14） | ✅ |

### 提交前置（用户点名后）

1. **prod `refresh=True` 终验**（余量仅 0.0036，最容易翻脸的一项）
2. 若翻脸 ⇒ 递补 `qM78d1rA`，并补三问（holders / polarity / prior）
3. 三段式属性；提交后复核 `status=ACTIVE` + prod 快照恒等式

---

## 6 产物与来源

- 报告：`output_report/opmin_O0WOK0Wg_20261111.md`
- 批次：`results/wp_O0WOK0Wg_A_20261111.txt`、`results/wp_O0WOK0Wg_batchA_20261111.json`；签核 `results/op_coverage_signoff.jsonl`（+1）
- 台账：`ledger_kv[EUR].robustness_ZYa6x531`
- 平台：10 条 FULL 仿真、`get_alpha_yearly_stats` ×5、`check_correlation(production)` ×4、`check_self_correlation` ×2、`workflow_submit_alpha(confirm_submit=false)` ×2、`results/notes_da.md`（Fitness 公式）

**本轮零提交、零平台写操作**（仅本地台账 1 条）。
