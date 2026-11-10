# `mLovbnm2` op-min 报告 · 2026-11-10

> `wq-alpha-gate-push-op-min`｜DEU/TOP500/D1｜**10 条仿真 / 1 批**，零提交（`ALLOW_ALPHA_SUBMIT=False`）。

## 0 结论

**8 → 7 算子，压缩成功；7 是地板。两颗 7-ops 件全闸通过且 prod 已复检。**

| | 原件 `mLovbnm2` | **`2rAYpJKx`** | **`rKRx2Alj`（推荐）** |
|---|---|---|---|
| 改写 | — | `multiply(A,B,C)` 变参合并 | 变参 + `ts_mean`→`ts_sum` |
| ops | 8 | **7** | **7** |
| S / F | 1.94 / 1.79 | 1.94 / 1.79 | **1.95 / 1.80** |
| 2Y | 2.18 | 2.18 | **2.23** |
| TO / margin | 0.1401 / 16.98bp | 0.1401 / 16.98bp | 0.1401 / 17.08bp |
| `failed_ra` | 0 | 0 | 0 |
| **prod** | 0.6572 | **0.6572（逐位相同）** | **0.6561（低 0.0011）** |
| self | 0.5620 | 0.5620（逐位相同） | 0.5637 |
| ΔSharpe | +0.68 | +0.68 | +0.68 |
| mix_audit | `none` | `none` | `none` |
| 分区 | `DEU:1:POWER_POOL` | 同左 | 同左 |

- `2rAYpJKx` 是**纯语法改写**（乘法结合律）：PnL 12,280,273 逐位相同，prod 直方图逐位相同、self 逐位相同 ⇒ **零风险压缩**。
- `rKRx2Alj` 指标与 prod 都略优；按 skill ④b 采纳判据「prod 更低 / 指标更好」⇒ **优先采纳**。
- 两颗与原件同族 ρ≈1 ⇒ **最终只保留 1 颗**，其余标 SUPERSEDED。

## 1 起点：这颗已经全闸通过

`mLovbnm2` 是 11-10 01:55 写入 `tracking/DEU/atom_orthogonal/final_delivery_20261109.md` §8.1 的
**首个全闸通过件**：RA `failed_ra=0`、`IS_LADDER_SHARPE` PASS、prod 0.6572、self 0.5620、
ΔSharpe +0.68、稳健 Recent-3yr 均值 2.177 无负年、`submit_staging_mLovbnm2.json` 已装。
⇒ 本轮**不做目标 A（推指标）**，只做目标 B（压算子），且任何改写不得破坏已验的 6 项读数。

```
multiply(
  multiply(group_rank(ts_mean(mean_estimate_change_pct_f12m_earnings_7d_4, 10), sector),
           group_rank(ts_mean(netprofit_y1_estimate_change_3mo, 50), industry)),
  group_rank(ts_mean(mean_estimate_change_pct_f12m_ebitda_90d_3, 30), industry))
```
`op_count.py` 数出 **8 个算子调用点**（`group_rank`×3 + `ts_mean`×3 + `multiply`×2）；战役台账写 9 ops，系口径差，以调用点为准。
设置：`decay2 / SUBINDUSTRY / trunc0.08 / nanOFF / 2014-01-01~2023-12-31 / TOP500 / D1`。
塔 `DEU/D1/MODEL`(1.8) + `DEU/D1/ANALYST`(1.8)，effective=2。

## 2 批 A：10 条压缩消融

| # | 改写 | ops | alpha | S | F | 2Y | 判定 |
|---:|---|---:|---|---:|---:|---:|---|
| **A1** | **`multiply(A,B,C)` 变参** | **7** | **`2rAYpJKx`** | **1.94** | **1.79** | **2.18** | ✅ **全过，逐位相同** |
| **A10** | 变参 + `ts_sum` | **7** | **`rKRx2Alj`** | **1.95** | **1.80** | **2.23** | ✅ **全过，prod 更低** |
| A2 | 合并两条同 `industry` 腿 | 7 | `E56dGkw1` | 0.93 | 0.48 | 0.46 | ❌ 3 fail |
| A3 | 删腿1 `ts_mean` | 6 | `rKRx2AoE` | 1.74 | 1.15 | 2.16 | ❌ `CONCENTRATED_WEIGHT` + `LOW_SUB_UNIVERSE_SHARPE` |
| A4 | 删腿2 `ts_mean` | 6 | `P0oVGvpp` | 1.71 | 1.36 | 1.28 | ❌ `IS_LADDER_SHARPE` |
| A5 | 删腿3 `ts_mean` | 6 | `pwdLN86x` | 1.81 | 1.46 | 1.45 | ❌ `IS_LADDER_SHARPE` + CW |
| A6 | 三腿去轴 `rank×rank×rank` | 7 | `j2Y761ZO` | 1.97 | 1.92 | 1.49 | ❌ `IS_LADDER_SHARPE` |
| A7 | 全裸字段 4 ops | 4 | `mLov5Z8E` | 0.55 | 0.15 | 0.15 | ❌ 4 fail |
| A8 | 删腿1（两腿版） | 5 | `xArZNRkg` | 1.68 | 1.46 | 1.40 | ❌ ladder |
| A9 | 删腿3（两腿版） | 5 | `d5WGZd0E` | 1.88 | 1.57 | 1.55 | ❌ ladder 差 0.03 |

**结论**：三条 `ts_mean` 全部承重（删任一条都掉 `IS_LADDER_SHARPE` 或子宇宙闸）；三腿乘积共振承重（删任一腿 ladder 掉到 1.40–1.55）；
`group_rank` 轴也承重（去轴 2Y 2.18→1.49）。⇒ **7 ops 是地板**，唯一无损空间是 `multiply` 变参合并。

## 3 复检（两颗 7-ops 件）

| 项 | `2rAYpJKx` | `rKRx2Alj` | 方法 |
|---|---|---|---|
| prod | **0.6572** `all_passed=true` | **0.6561** `all_passed=true` | `check_correlation(production)` |
| self | **0.5619975666** | 0.5636882854 | `check_self_correlation`（本地） |
| ΔSharpe | **+0.68** | **+0.68** | `mcp_preflight_once.py`（`DEU:1:POWER_POOL`） |
| mix_audit | `none` legs=0 | `none` legs=0 | 同上 ⇒ **不需三问** |
| 逐年 | 与原件逐位相同 | `[2.05,3.59,1.43,1.92,0.36,2.85,1.10,3.07,2.30,1.29]` | `get_alpha_yearly_stats` |
| 近3年 | 3.07/2.30/1.29 → 均值 2.177 | 同形，均值 2.22、CV(pop) 0.328 | 10/10 正年、无空窗 |

`rKRx2Alj` 的 prod 首次查询挂起 251s（`inflight=true`，按纪律**未重复触发**），第二次 `refresh=false` join 到已有计算拿到 0.6561。

## 4 换将代价（需用户决策）

`mLovbnm2` 已装 `submit_staging_mLovbnm2.json`（含 name/tags/description/expression/correlations/marginal/gates）。
采纳 7-ops 件需要同步改 4 处：

1. `alpha_id` / `expression` → 新 id；
2. `correlations.production` / `.self` → 新读数；
3. `metrics` → 新指标（S/F/2Y 微变）；
4. `descriptions` 里的读数串 + 三腿描述（变参写法）。

且 `robustness_<新id>` 台账为 **NO_RECORD**，走提交链前须由 `brain-alpha-robustness` 补真审（原件 §8.1 的稳健结论不能直接继承到新 id）。
**本轮未改动 staging 文件**，等用户点名选颗。

## 5 与当日可提交清单的关系

`output_report/submittable_ranking_20261109.md` 结论是「ET 11-09 REGULAR 2/4 已用、剩 2；0 颗可零动作直接提交」。
`mLovbnm2`（或 7-ops 压缩件）是**该清单生成后新产出的第一颗全链闭环候选**：
RA / prod / self / ΔS / 稳健 / 塔全部实测通过，`mix_audit=none`，无需任何豁免。
⇒ 若用户要用掉剩余 2 个配额，这颗应排**第 1 位**；另一颗配额仍按原清单 `P0oolrZq`（需 prod 终验 + 补登台账）。

⚠ 提交前仍须按纪律对**提交那一颗**做 `prod refresh=True` 终验（当前读数是 01:51 缓存，今日两颗新提交已进池）。

## 6 记账

- 采纳建议：`rKRx2Alj`（最优）或 `2rAYpJKx`（零风险）；原件 `mLovbnm2` 保持 `UNSUBMITTED`。
- 其余 8 颗标 SUPERSEDED；3 颗关键派生已入 `mining_ledger`（wave `mlovbnm2-opmin`）。
- 覆盖签核 1 条入 `results/op_coverage_signoff.jsonl`（session `mlovbnm2-opmin-a-compress`）。
- **未提交**（`ALLOW_ALPHA_SUBMIT=False`）；本轮只做派发仿真与只读复核。
