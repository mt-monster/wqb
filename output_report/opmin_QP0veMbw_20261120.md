# `QP0veMbw` / `2r5ARLvw` 优化报告（KOR/D1 · ern3 + returns 回归）

- 日期：2026-11-20
- 区域/设置：KOR / TOP600 / Delay-1 / decay 4 / STATISTICAL / trunc 0.08 / nan OFF
- 字段：`returns`（内置）、`ern3_pre_interval`（earnings 类）
- 塔：`KOR/D1/EARNINGS ×1.1` + `KOR/D1/PV ×1.4`（混塔，取短板 **1.1**）

## 一、结论：**建议放弃，结构性无解**

原件 4 项 RA FAIL，且压换手实验证明**两难不可调和**：

| 件 | 做法 | S | F | TO | 2Y | sub | invest | RA FAIL |
|---|---|---|---|---|---|---|---|---|
| `QP0veMbw` | 原件 | 1.66 | **0.55** | **79.5%** | **−0.10** | 1.19 | 0.70 | **4** |
| `2r5ARLvw` | 原件（孪生） | 1.67 | **0.56** | **79.4%** | **−0.22** | 1.24 | 0.71 | **4** |
| **`P05oVpmL`** | **抽取+等价化简** | **1.66** | 0.55 | 79.5% | −0.10 | 1.19 | 0.70 | 4 |
| `pwadL6bg` | +`ts_target_tvr_decay` 0.30 | **0.29** | 0.08 | 19.8% | −0.06 | 0.10 | 0.12 | 5 |
| `qM7LRA2P` | +tvr 0.20 | **0.29** | 0.09 | 14.9% | −0.02 | 0.16 | 0.17 | 5 |
| `LLKMQpo9` | +tvr 0.15 | 0.29 | 0.10 | 12.4% | −0.18 | 0.16 | 0.20 | 4 |
| `E5Q6dwnL` | +tvr 0.10 | 0.29 | 0.09 | 9.7% | −0.45 | 0.17 | 0.24 | 3 |

### 1.1 死局机理

F 公式 `F = S·sqrt(|R| / max(TO, 0.125))`。原件 S 1.66、R 8.73%、TO 79.5% ⇒ F = 0.55 ✓。

要把 F 抬到 1.0 有两条路，**两条都堵死**：

| 路径 | 计算 | 结果 |
|---|---|---|
| 提 S | 需 S ≈ 3.0（保持 TO 79.5%） | 不可能 |
| 压 TO | 需 TO ≈ 24%（保持 S 1.66） | 实测压到 19.8% 时 **S 已崩到 0.29** ⇒ F 只剩 0.08 |

⇒ **信号的全部 alpha 来自高频成分**（`ts_quantile` 横截面分位每日重算），`ts_target_tvr_decay` 削掉的正是收益本身，不是噪声。

### 1.2 2Y 为负：独立的第二重死因

原件 2Y Sharpe **−0.10**；压换手后 -0.06 / -0.02 / -0.18 / -0.45 —— **任何参数都救不回来**。近两年（2022–2023）该关系已反向，与换手无关。`IS_LADDER_SHARPE` 在 year=2 直接 FAIL（限 1.58）。

### 1.3 第三重：KOR 的 investability 硬闸

`LOW_INVESTABILITY_CONSTRAINED_SHARPE` 限 = 0.70 × S。原件 invest 0.70 vs 限 1.16 = 保留率仅 **46%**（KOR 要求 ≥70%）。压换手虽把保留率抬到 0.20/0.29（69%），但此时 S 已崩，限降到 0.2 仍失败。

## 二、变量抽取验证（本轮的技术收获）

**抽取 + 等价化简对指标零影响，已逐位验证**：

```
r66  = ts_quantile(returns,66);
r252 = ts_quantile(returns,252);
e66  = ts_quantile(ern3_pre_interval,66);
e252 = ts_quantile(ern3_pre_interval,252);
group_rank(-ts_regression(divide(add(r66,r252),2), divide(add(e66,e252),2), 252, rettype=0), sector)
```

| 对比项 | 原件 `QP0veMbw` | **抽取版 `P05oVpmL`** |
|---|---|---|
| PnL | 9,032,921 | **9,032,921** |
| Sharpe / Fitness | 1.66 / 0.55 | **1.66 / 0.55** |
| Turnover / Drawdown | 79.5% / 11.58% | **79.5% / 11.58%** |
| sub / invest / 2Y | 1.19 / 0.70 / −0.10 | **1.19 / 0.70 / −0.10** |

**同时做了等价化简** `add(divide(a,2), divide(b,2))` → `divide(add(a,b),2)`：`divide` 调用从 2 次降为 1 次，`add` 保持 1 次 ⇒ 算术调用 −1（原件 4 个 divide，化简后 3 个）。指标逐位不变。

**工程注意**：`preflight_expressions` **不解析多语句**，会把赋值变量误报为 `unknown_fields`（`valid:false`）；但 `create_multi_simulation` 与平台均正常接受。遇到此误报应直接用仿真验证。

## 三、六维：价值为零

| 维度 | `QP0veMbw` | `2r5ARLvw` | 判定 |
|---|---|---|---|
| ops | 6 | 6 | ΔT1 **+0.0020**（worse） |
| fields | 2 | 2 | ΔT2 **−0.0006**（better） |
| T3 新算子 | — | — | **flat** |
| **T4 新字段** | — | — | **flat（两个字段当季已用过）** |

⇒ 六维只有 T1 轻微恶化 + T2 微改善，**净偏负**；T3/T4 零贡献。**即便能提交，对六维也无正收益。**

## 四、两颗的关系

`compute_mutual_correlation` = **0.9837**（阈值 0.7），`max_mutually_below_subset = ["QP0veMbw"]` ⇒ **孪生，只能交一颗**。两者仅权重写法不同（`divide(·,2)` vs `multiply(·,3)`），绩效差 0.01 以内。

## 五、建议

1. **放弃该族**，不要继续在 KOR/ern3 上投仿真额度。三重硬伤（高换手不可削、2Y 为负、investability 保留率 46%）任一都足以否决。
2. 若仍想用 `ern3_pre_interval`，必须**换机制**而非调参：例如把它作为 `trade_when` 门控条件、或 `bucket` 分组轴、或对其它主信号做 `neutralize` 残差（三种合规跨数据集形式），而不是让 `ts_quantile` 直接进主信号。
3. `KOR/D1/EARNINGS` 塔当季计数为 **0**，但本族不可达；KOR 侧应转 `shortinterest`（当季 4）或 `analyst`（4）。

## 六、仿真统计

7 颗（原件 2 + 抽取化简 1 + 压换手 4）。零 FAIL 件 **0** 颗。

## 七、附带产出（可复用件）

`P05oVpmL`（抽取+化简版，与原件逐位等价）保留为**模板**：证明「`p = expr; <末行>` 多语句 + 算术等价化简」在平台完全无损。后续所有含重复子式的表达式都应先做这两步再回测。
