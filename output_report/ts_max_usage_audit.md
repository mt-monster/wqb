# `ts_max` 算子使用审计（提交至平台的 alpha）

审计时间：2026-09-28 | 数据源：`data/wqb.db` + 平台实时 API 补全

## 结论：**没有。已提交的 alpha 从未使用过 `ts_max` 算子。**

| 检查口径 | 样本数 | 含 `ts_max` |
|---|---|---|
| 已提交 alpha（`platform_status` = ACTIVE 137 + DECOMMISSIONED 106）有表达式者 | 231 | **0** |
| 已提交但本地表达式为空（12 颗，均为 **SUPER 组合型**，已向平台取回校验） | 12 | **0** |
| `submission_ledger` status=ACTIVE | 83 | **0** |
| `submit_ready` status=SUBMITTED | 65 | **0** |
| **整个 `alphas` 表**（含未提交）有表达式者 | 8,442 | **0**（精确 `ts_max(`） |

## 关键辨析：`ts_max` ≠ `ts_max_diff`

全库 4 条含 `ts_max` 子串的记录，实际都是 **`ts_max_diff`（另一个算子）**，且全部未提交、全部失败：

| alpha_id | Sharpe | 区域 | 状态 |
|---|---|---|---|
| A10M1GWl | -0.68 | EUR | UNSUBMITTED |
| 3q9rvGWP | -0.43 | EUR | UNSUBMITTED |
| 0mR32GW1 | -0.38 | EUR | UNSUBMITTED |
| blR5lQkN | 0.02 | EUR | UNSUBMITTED |

生成池（`expressions`）中：精确 `ts_max(` 仅 **3 条**，全部停留在 `gem` 状态（从未入选/提交）：

- `divide(mass_index_indicator, ts_max(mass_index_indicator, 252))`
- `divide(money_flow_index_indicator, ts_max(money_flow_index_indicator, 252))`
- `divide(negative_volume_index_indicator, ts_max(negative_volume_index_indicator, 252))`

另有 146 条 `ts_max_diff(`（多为 dropped）。

## 已提交 alpha 实际使用的 `ts_*` 算子分布（231 条）

| 算子 | 次数 |
|---|---|
| ts_mean | 155 |
| ts_backfill | 112 |
| ts_std_dev | 110 |
| ts_rank | 34 |
| ts_sum | 34 |
| ts_zscore | 33 |
| ts_delta | 18 |
| ts_decay_linear | 16 |
| ts_arg_max | 2 |
| ts_delay | 2 |
| ts_av_diff / ts_corr / ts_ir | 各 1 |
| **ts_max** | **0** |
| **ts_min** | **0** |

## 判读

1. **`ts_max` 是完全未开垦的算子** —— 已提交 243 颗中 0 使用，全库 8,442 条表达式中 0 次精确使用。
2. 近亲算子里，`ts_arg_max` 已用过 2 次（说明极值类思路有过落地），`ts_max_diff` 试过 146 次但几乎全 dropped、4 次实跑全负 Sharpe —— **说明"最大值族"此前探索的切入点（`ts_max_diff` 差分）效果差，但不代表 `ts_max` 本身无效**。
3. 生成池仅有的 3 条 `ts_max` 都是 `divide(x, ts_max(x,252))` 归一化形态且未入选，**样本太小不足以判死**。
4. 可尝试的方向（尚未验证）：`ts_max(x,N) - x`（距峰值回撤）、`x / ts_max(x,N)`（滚动区间位置）、`ts_arg_max - ts_arg_min` 间距、与 `ts_min` 配对构造 `(x - ts_min)/(ts_max - ts_min)` 随机区间位置。
