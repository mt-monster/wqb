# `leAgQPO5` 优化报告：全闸已过、算子已到底、prod 是唯一约束

- 日期：2026-11-15
- 区域 / 设置：GBR / TOP700 / D1 / decay 5 / **SLOW** / trunc 0.06 / nanHandling ON / 2014–2023
- 表达式（5 算子）：
```
multiply(group_backfill(group_zscore(ts_av_diff(imb5_score, 126), industry), subindustry, 252),
         ts_rank(volume, 66))
```
- 实跑仿真 **36 条**（4 批 + 1 组设置矩阵）

## 1 结论

| 目标 | 结论 |
|---|---|
| 推全闸 | **已全过**，无需推（唯一 WARNING 是 `CLUSTER_TEST` 0.85/1.0，非硬闸） |
| 压算子 | **5 是下限**。压到 4 的路径存在（删 `group_backfill`）但 prod 余量从 .0134 塌到 **.0005**，净亏 |
| 真正瓶颈 | **prod 0.6866（余量 .0134）** —— 任何提升 S 的变体都把 prod 顶到 0.712–0.721 越线 |

⇒ **交付件维持原式不动（5 算子）。本轮零采纳。**

## 2 全闸现状（`leAgQPO5`）

| 闸 | 值 / 线 | 结果 |
|---|---|---|
| LOW_SHARPE | 2.16 / 1.58 | PASS |
| LOW_FITNESS | 1.18 / 1.0 | PASS |
| LOW_SUB_UNIVERSE_SHARPE | 1.69 / 1.02 | PASS |
| IS_LADDER_SHARPE | 1.87 / 1.75（2Y 窗） | PASS |
| LOW/HIGH_TURNOVER | .2382 / .01–.7 | PASS |
| CONCENTRATED_WEIGHT | — | PASS |
| CLUSTER_TEST | **0.85 / 1.0** | **WARNING**（非硬闸名单） |
| self | **0.1064** | PASS（池 29/34，最分散） |
| prod | **0.6866** | PASS（**余量仅 .0134**） |
| Failed RA / PPA | 0 / 0 | PASS |

## 3 压缩：5 算子已是下限

第 0 步变量合并：表达式内无重复子式 ⇒ **零收益**（`op_count.py` 亦确认「未发现自动可压缩点」）。

| 变体 | 改动 | oc | S | ladder | prod | 判定 |
|---|---|---:|---|---|---|---|
| base | — | **5** | 2.16 | 1.87 | **.6866** | 保留 |
| E3 | 删 `group_backfill`（industry 直轴） | **4** | 2.07 | 1.77 | **.6995** | ✗ 余量 .0005 + 新增 CW WARNING |
| E2 | `group_zscore(·, subindustry)` 直轴 | 4 | 1.58 | 1.31 | — | ✗ ladder 崩 |
| E1 | 同上但 `group_rank` | 4 | 1.19 | 1.42 | — | ✗ |
| E7 | `group_rank(ts_zscore(·), subindustry)` | 4 | 1.41 | 1.49 | — | ✗ |
| E8 | `group_rank` 保留 backfill | 5 | 1.56 | 1.40 | — | ✗ LOW_SHARPE/FITNESS WARNING |
| E4 | 删 volume 腿 | **2** | 0.81 | — | — | ✗ 三闸 FAIL |

**承重结构**：`group_backfill(group_zscore(x, industry), subindustry, 252)` 这个 3 算子块不可拆——拆一层（E3）伤 ladder 与 prod，换轴（E1/E2/E7）直接崩。

## 4 推指标：S 全都能推，**prod 全越线**

| 变体 | 改动 | oc | S | ladder | sub | prod | 判定 |
|---|---|---:|---|---|---|---|---|
| base | — | 5 | 2.16 | 1.87 | 1.69 | **.6866** | ✓ |
| **E5** | `ts_av_diff`→`ts_zscore` | 5 | **2.32** | **2.11** | 1.81 | **.7118** | ✗ prod |
| **F4** | volume 窗 66→21 | 5 | **2.33** | **2.14** | 1.81 | **.7122** | ✗ prod |
| **F6** | `ts_zscore(ts_backfill(imb5,22),126)` | 6 | 2.29 | 2.08 | 1.83 | **.7210** | ✗ prod |
| F1 | `ts_zscore(·,252)` | 5 | 2.30 | 1.47 | 1.78 | — | ✗ ladder |
| F3 | volume 窗 252 | 5 | 2.24 | 1.51 | 1.74 | — | ✗ ladder |
| F8 | volume 窗 132 | 5 | 2.31 | 1.58（贴线） | 1.81 | — | ✗ ladder WARNING |
| E6 | `ts_rank(imb5,126)` | 5 | 2.36 | 1.48 | 1.80 | — | ✗ ladder |
| G1 | `ts_delta(imb5,126)` | 5 | 1.90 | 0.68 | 1.31 | — | ✗ |
| G3 | 轴 `market` | 5 | 2.04 | 0.97 | 1.68 | — | ✗ |
| G4 | volume 腿取反 | 6 | −2.16 | −1.60 | — | — | 恒等反向（数学无新信息） |
| G2 | `ts_ir(imb5,126)` | 5 | 0.22 | −0.22 | — | — | ✗ |
| G5/G6/G7/G8 | 窗 252 / backfill 504 / group_neutralize / 延迟量 | 5–6 | 1.68–2.23 | 1.37–1.57 | — | — | ✗ 全 ladder |

**规律**：S 与 prod 在本骨架上**同向**——S 每 +0.15，prod +0.03，两次都刚好越 0.70。

## 5 设置扫描（7 档，全部跑完）

| 设置 | S | ladder | cluster | 判定 |
|---|---|---|---|---|
| **SLOW / decay 5（原设）** | **2.16** | **1.87** | 0.85 | ✓ 最优 |
| decay 8 | 2.08 | 1.47 | 0.84 | ✗ |
| decay 12 | 2.00 | 1.33 | 0.80 | ✗ |
| FAST | 1.98 | 1.31 | 0.94 | ✗ |
| SUBINDUSTRY | 2.04 | 1.58 贴线 | 1.10 | ✗ |
| INDUSTRY | 2.12 | 1.30 | 1.15 | ✗ |
| CROWDING | 2.15 | 1.28 | **1.32（唯一过 cluster）** | ✗ ladder |
| SLOW_AND_FAST | 2.01 | 1.54 | 0.82 | ✗ |
| maxTrade=ON | 1.54 | 0.58 | 0.85 | ✗ |
| `maxPosition=ON` | — | — | — | GBR **不支持**（400） |

⇒ 现设置（SLOW / decay 5 / trunc .06）就是该骨架的唯一可行点。**「换中性化档」在本族同样是降 S**，与技能库禁用表一致。

## 6 稳健性现状（台账既有记录，2026-11-11）

- 逐年 Sharpe：2.74 / 3.34 / 2.87 / 2.45 / 2.01 / 1.06 / 2.69 / 1.78 / 2.40 / **0.62**
- 近三年 1.78 / 2.40 / **0.62**，CV **.461**、衰减比 **.287** ⇒ 台账 **CONDITIONAL**（末年崩塌是主因）
- 本轮唯一把 2023 抬起来的变体是 E5（**0.62 → 0.72**，衰减比 .310），但 prod 0.7118 越线 ⇒ 不可用

## 7 建议

1. **交付维持 `leAgQPO5` 原式**（5 算子），不要为「4 算子」付 prod 余量归零的代价。
2. 本族已到 **prod 墙**：再提 S 必然越线。若后续 prod 池漂移（48h 失效）后余量变化，可复测 E5 / F4 两颗（`d5amYQZJ` / `d5am396x`，S 2.32–2.33、ladder 2.11–2.14），它们只差 prod 一项。
3. **2023 崩塌是独立问题**：与本轮所有结构杠杆正交（E5 仅 +0.10），需要换载体字段或换区才能解，不建议在同骨架继续投仿真。
4. `CLUSTER_TEST 0.85` 是唯一非硬闸 WARNING；CROWDING 档能把它抬到 1.32，但 ladder 同时崩（1.28）⇒ 不可两全。

## 8 数据来源

`GET /alphas/leAgQPO5` + `check_correlation`（self/prod）；4 批 multisim（`3aLU7fdIG4tL9exq5qeiOcw` / `aiKE67FQ4tR8C61a5k5qoWs` / `4lPnPfSD4ktci5xKSd5ecD`）+ `batch_create_simulations` 12 条（2 条被平台拒：429 并发 / GBR 不支持 maxPosition）。**零提交。**
