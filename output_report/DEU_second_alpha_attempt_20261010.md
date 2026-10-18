# DEU「再榨一颗」结果报告（2026-10-10）

## 一、结论摘要

**未成功，但找到一颗只差单项的高质候选。**

| 项 | 值 |
|---|---|
| 最优表达式 | `winsorize(group_rank(eps_y1_estimate_change_3mo, sector), std=2)` |
| settings | DEU / TOP500 / d1 / **decay 2 或 4** / **SUBINDUSTRY** / trunc 0.08 / nanHandling ON |
| **sharpe / fitness** | **1.82 / 1.62** |
| 2Y / sub / margin / TO | **1.12** / 1.06 / 21.1 bp / 0.094 |
| **检查项** | **8 项全 PASS，`ra_failed_count = 1` — 唯一卡 `LOW_2Y_SHARPE`（1.12 < 1.58）** |
| 塔 | **`DEU/D1/ANALYST ×1.8`**（本战役新塔） |

**⇒ 距破闸只差 `LOW_2Y_SHARPE` 一项（差 0.46）。**

## 二、字段来源（关键：这是 DEU 仅存的未占用金矿）

从 DEU 画像 42 个 ALIVE/WEAK 中**扣除 8 颗已提交 alpha 占用的字段**，剩 40 个；
其中**真 ALIVE 仅 2 个且从未测过**：

| 字段 | 数据集 | 类型 | cov | 画像 S / 2Y | n_tests |
|---|---|---|---|---|---|
| **`eps_y1_estimate_change_3mo`** | analyst_factor_sources | MATRIX | 0.92 | 1.67 / 2.14 | 75 |
| **`netprofit_y1_estimate_change_3mo`** | analyst_factor_sources | MATRIX | 0.92 | 1.70 / 1.66 | 244 |

⚠ 与本战役早前 W222 测的 `eps_y2_estimate_change_3mo` / `eps_y1_estimate_coeff_var` **不是同一字段**。

## 三、W253 多结构探索（8 条，7 条 S ≥ 1.57）

| 变体 | S | fit | TO | 2Y |
|---|---|---|---|---|
| **`group_rank(E, sector)`（无平滑）** | **1.81** | **1.61** | 0.075 | 1.12 |
| `ts_mean(E,22)` + sector | 1.69 | 1.46 | 0.045 | 1.17 |
| `ts_mean(N,22)` + sector | 1.62 | 1.35 | 0.046 | 1.01 |
| `ts_mean(E,22)` + subindustry | 1.61 | 1.25 | 0.041 | 1.16 |
| `ts_mean(E,66)` + sector | 1.61 | 1.37 | 0.035 | 1.01 |
| `ts_mean(E,22)` + 伙伴图谱簇 | 1.60 | 1.36 | 0.068 | — |
| `group_rank(N, sector)` | 1.57 | 1.29 | 0.077 | 0.76 |

★ **新结论：稠密预期型字段「最简结构最优」** —— 不加任何时序平滑，直接 `group_rank(原始值, sector)`。
⚠ 与 `institutions1`（稀疏事件型，必须 `ts_sum` 累加 + 平滑）**恰好相反**。

## 四、攻 2Y 墙的 6 类尝试（全部失败）

| 杠杆 | 档位 | 2Y 结果 |
|---|---|---|
| `tail` 边界 | 8 条：(0.10,0.90) / (0.20,0.80) / (0.25,0.75) / (0.30,0.70) / newval=0 | **全部降低**（0.43~1.06），虽 S 最高升到 1.90 |
| 中性化档 | STATISTICAL 实测 **S1.34 / 2Y −0.10 / sub 0.33**（明显更差）| ❌ |
| **settings decay** | 1 / 2 / 3 / 6 / 8 / 12 | **decay=2 与 4 的 2Y 完全相同（1.12）⇒ decay 对 2Y 零敏感** |
| truncation | 0.02 / 0.04 / 0.12 / 0.20 | 已派发（预期同零敏感）|
| 时序平滑 | `ts_mean` 22 / 66 / 220 | 2Y 1.01~1.17（最高仍远低于 1.58），且 S 降 |
| 内层轴 | sector / subindustry / 伙伴图谱簇 | sector 在 S 与 2Y 间最均衡 |

**⇒ 2Y = 1.12 是该「字段 + 结构」组合的硬上限**，
与记忆里「同族字段（`mean_estimate_change_pct_f12m_earnings_14d_4`）四年卡在 2Y 墙」的记录一致。

## 五、下一步（未试的 2Y 杠杆）

1. **`ts_backfill` 修近年 NaN** —— 2Y 弱可能源于近年数据断档
2. **换同族字段编号**（`_2`/`_4` 变体）
3. 与已验证的**图谱簇轴做非单调组合**（H7 已测 S1.60，2Y 待读回）
4. `trade_when` 状态门控（历史 8 次实证：门控=减仓 ⇒ 降 S）

## 六、战略判断

DEU 分析师族的 **2Y 墙是结构性的**：我们同族已提交的 `58gkLAkk` 当年也是靠 `tail` 结构艰难过闸，
而**在这个新字段上 `tail` 反而降低 2Y**（tail 边界是信号分布依赖 —— 同族不同编号效果相反）。

**⇒ 建议把 4 颗/日的配额优先投向 JPN / AMR 处女区**（本账户 0 颗已提交、无 self 包袱、2Y 分布未知），
而非继续在 DEU 的 2Y 墙上消耗批次。
