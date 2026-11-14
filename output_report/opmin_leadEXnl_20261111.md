# `leadEXnl` 优化：FASTEXPR 11→9 ops（S 2.17）+ Python 形式首测

**时间**：2026-11-12 00:30 GMT+8｜**区**：DEU / TOP500 / delay 1 / decay 0 / SUBINDUSTRY / trunc 0.08
**政策**：只挖不提交。

---

## 0 基线

| 项 | 值 |
|---|---|
| `regular.operatorCount` | **11**（本就很省） |
| Sharpe / Fitness | 2.20 / 1.64 |
| Turnover / Returns / DD | .1941 / 10.76% / 4.66% |
| sub_universe | 1.42（lim 1.04） |
| IS_LADDER | 2.43（lim 2.02） |
| CLUSTER_TEST | 1.81（lim 1.0） |
| 其余 IS 闸 | 全 PASS |

表达式（3 腿：内幕人最大单笔占比 + 两档 EBITDA 预期修正）：

```
signed_power(group_zscore(add(
  group_rank(ts_mean(divide(significant_value_1,
    add(significant_value_1, significant_value_2, significant_value_3, significant_value_4)), 66), sector),
  rank(ts_mean(mean_estimate_change_pct_f12m_ebitda_14d_4, 5)),
  rank(ts_mean(mean_estimate_change_pct_f12m_ebitda_90d_3, 22))), sector), 1.3)
```

字段类型核实：`significant_value_1..4` = **MATRIX**，`mean_estimate_change_pct_f12m_ebitda_14d_4` / `_90d_3` = **MATRIX**
⇒ 无 Vector 字段，**Python alpha 形式在字段层面可行**。

---

## 1 FASTEXPR 优化（8 条实测，全 IS 闸 PASS）

| 变体 | id | oc | S | F | TO | sub / lim | ladder | 判定 |
|---|---|---:|---|---|---|---|---|---|
| F1 基线 | `leadEXnl` | 11 | 2.20 | 1.64 | .1941 | 1.42 / 1.04 | 2.43 | PASS |
| **F2 删 `signed_power`** | `0mPqNdWk` | **10** | **2.19** | 1.64 | **.1822** | 1.44 / 1.04 | 2.44 | **PASS（几乎无损，TO 更低）** |
| F3 删外层 `group_zscore` | `LLKWm6x2` | 10 | 2.16 | 1.63 | .176 | 1.40 / 1.02 | 2.33 | PASS |
| F4 两 `rank` 合并 | `QP0MNjer` | 11 | 1.81 | 1.50 | .1108 | 1.11 / 0.86 | 2.49 | PASS（指标明显变差） |
| **F5 删 `signed_power`+`group_zscore`** | **`Jj8qWmlx`** | **9** | **2.17** | **1.65** | .177 | 1.38 / 1.03 | 2.32 | **PASS ★ 最优** |
| F6 删 sp + 合并 rank | `zqdZ2jaV` | 10 | 1.79 | 1.44 | .1059 | 1.14 / 0.85 | 2.46 | PASS（差） |
| F7 三者全删 | `rK7YNLQE` | 9 | 1.80 | 1.46 | .1029 | 1.12 / 0.85 | 2.39 | PASS（差） |
| F8 内幕窗 66→126 | `N1P0J6ke` | 11 | 1.88 | 1.33 | .1823 | 1.31 / 0.89 | 2.54 | PASS（差） |

### 结论

- **最优交付 `Jj8qWmlx` = 9 ops**（-18%），S 2.17（vs 2.20）、F 1.65（vs 1.64），全闸 PASS。
  ```
  add(group_rank(ts_mean(divide(significant_value_1,
      add(significant_value_1, significant_value_2, significant_value_3, significant_value_4)), 66), sector),
    rank(ts_mean(mean_estimate_change_pct_f12m_ebitda_14d_4, 5)),
    rank(ts_mean(mean_estimate_change_pct_f12m_ebitda_90d_3, 22)))
  ```
- **`signed_power(x,1.3)` 与 `group_zscore(·,sector)` 在这颗上都是纯包装**：连删两个只掉 0.03 S，
  且 F 微升（1.64→1.65）、TO 从 .1941 降到 .177 ⇒ 六维和交易成本双赢。
- **两个 `rank` 不能合并**（F4/F6/F7 全部掉到 1.8 附近）：两档修正信号的**独立截面归一**是承重件。
- 窗口 66→126 反向（S 1.88），说明内幕人占比的短期均值（66 日）是甜点。
- F2（10 ops）保留 `group_zscore`、TO 最低 .1822，若偏好更平滑可作备选。

---

## 2 Python alpha 形式：机制打通，指标未对齐

### 2.1 已确认的平台事实（本轮亲手验证）

| 项 | 结果 |
|---|---|
| 能否提交 | **能**（`language="PYTHON"` + `lookback=70`，平台直接返回 alpha id） |
| `operatorCount` | 返回 `null`（不计数）→ 与论坛「不影响 Operators per Alpha/used」一致 |
| 点塔 | **正常**，`pyramid_short = insiders/model`，`effective=2` |
| 字段限制 | 本颗 6 个字段全 MATRIX，无阻塞 |
| 输出要求 | 必须 `float32`；**输出含 NaN 会报 `Inconsistent result resuming simulation from alpha store`**（平台内部状态错误，非语法错）⇒ 必须 `nan_to_num` |

### 2.2 首测结果（`oma7GMzk` / `YPa6zaMo`，两次同结果）

| 指标 | FASTEXPR F5 | Python 版 | 差 |
|---|---|---|---|
| Sharpe | 2.17 | **0.92** | **−1.25** |
| Fitness | 1.65 | 0.53 | −1.12 |
| Turnover | .177 | .0783 | **−0.10** |
| sub_universe | 1.38 | 0.49 | −0.89 |
| 2Y | — | 1.57 | 差 0.01 触线 FAIL |
| long / short | ~131 / 145 | **101 / 145** | 多头少 30 |

**判定：复刻不等价，不可交付。** 换手只有一半、多头少 30 只，说明**信号覆盖/平滑度与 FASTEXPR 不同**。

### 2.3 已排除与待查

- **已排除**：`sector` 整型哨兵（加 `_group_to_float` 后指标**逐位不变**，PnL 完全相同 4228226）⇒ 分组字段不是问题。
- **待查（按可能性）**：
  1. **`ts_mean` 对稀疏序列的语义**——`divide(sv1, sv1+sv2+sv3+sv4)` 在内幕人无交易的日子大量 NaN，
     平台 `ts_mean` 可能要求窗口覆盖度，而我用 `nanmean` 过于宽松 ⇒ `q` 腿覆盖过广、稀释了两条修正腿。
     这就是「换手腰斩 + 多头减少」最合理的解释。
  2. `rank` 归一化常数（`order/(n-1)` vs `order/n` 或 [-0.5,0.5]）——线性差异应被中性化吸收，但会改三腿相对权重口径。
  3. `divide` 在分母为 0/负时的返回（我置 NaN，平台可能返回 inf→NaN 或 0）。
- **下一步**：用两条最小对照定位——(a) Python `rank(close)` vs FASTEXPR `rank(close)`；(b) Python `ts_mean(close,22)` vs FASTEXPR 版。
  两者指标对上后，再把 `q` 腿的 `ts_mean` 覆盖度阈值调到与平台一致。

---

## 3 交付建议

- **首选 `Jj8qWmlx`（9 ops，S 2.17 / F 1.65）**：现在就能用，六维成本比原 11 ops 低 18%。
- 若确定要走 Python 通道（Operators 两维清零），**必须先完成 §2.3 的三步对齐**，否则交出去的是 S 0.92 的残品。

## 4 数据来源

`GET /alphas/{id}` ×9（oc + is.checks + metrics）、`get_datafields`（字段类型 ×2 次）、
multisim `1nlICN30x5fO8J1qjgKUt4L`（8 条）、单条 Python 仿真 `oma7GMzk` / `YPa6zaMo` / `20j4e241e4HM9ZW136fSl9gx`。
**零提交。**
