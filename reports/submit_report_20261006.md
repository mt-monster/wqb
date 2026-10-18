# 提交报告 · ET 2026-10-06（4 REGULAR + 1 SUPER）

> 用户授权批次：「按每日可提 4 个 regular + 1 个 super alpha，按优选顺序提交至平台」。
> 结果：**5/5 全部 `ACTIVE`**。配额 REGULAR **4/4**、SUPER **1/1**。

## 一、提交结果

| 序 | alpha_id | 区 | 塔 | IS S | IS F | 2Y | 实测 self | 实测 prod | 结果 |
|---|---|---|---|---|---|---|---|---|---|
| R1 | `O08EjLVp` | USA | USA/D1/MODEL | 2.45 | 1.55 | 2.55 | 0.3321 | 0.5626 | ✅ ACTIVE |
| R2 | `N1VnJjXg` | EUR | EUR/D1/MODEL | 1.75 | 1.17 | 1.76 | 0.1954 | 0.5378 | ✅ ACTIVE |
| R3 | `JjQbYdGW` | GBR | GBR/D1/MODEL (×1.6) | 1.62 | 1.00 | 2.41 | — | 0.6072 | ✅ ACTIVE |
| R4 | `omWVV6Y2` | GBR | GBR/D1/MODEL (×1.6) | 1.62 | 1.02 | 1.76 | — | 0.6579 | ✅ ACTIVE |
| S1 | `9qWJv1do` | KOR | SUPER | 4.45 | 5.54 | 5.13 | — | 0.6521 | ✅ ACTIVE |

- 属性均已按规范设置：name `<REGION>_<R|S>_<family>_<seq>`、color `BLUE`（待观察）、tags 4 个（`CH_*`·`SRC_*`·`EXPRFAM_*`·`W_*`）、三段式 description。
- 平台复算的 `REGULAR_SUBMISSION` 计数随提交递增（0→1→…），配额确已占用。

## 二、被拦 / 剔除（原计划 5 颗 → 实际 5 颗，替换 2 颗）

| alpha_id | 拦截层 | 原因 |
|---|---|---|
| `WjegEmQO`（原第 2） | `submit_verdict` | `ROBUSTNESS_REJECT`：decay_ratio 0.22 < 0.30（2023 sharpe 0.43 vs full 1.94） |
| `QPK26lQX`（原第 1） | 提交节点 prod_gate | **self = 0.9984**，命中自家 ACTIVE `3qVa2Lze` → 同族重犯 |
| `j289xaxO` | 预判剔除 | 与 `QPK26lQX` 互相关 0.9908（同族） |
| `omWVZ7lm` | 预判剔除 | 与 `N1VnJjXg` 逐位相同 |
| `RR6NOlma` / `LLZ6wZO2` | 纪律剔除 | margin .014 / .0238 < 0.03 |

## 三、★ 本批最重要的发现（已固化到 MEMORY / 自动化 / 技能）

**台账 `prod` 会陈旧，提交节点的 `both`-max 才是权威判定。**

- `QPK26lQX` 台账 prod **0.5385**（看似余量 .16、报告原列第 1 位），提交节点实测 **0.9985** 直接拦截。
- 拆开 `check_correlation` 看：`production.max = 0.5385`（旧缓存），**`self.max = 0.9984`** —— 节点报的 "prod_max" 实为 `type="both"` 的 **max(prod, self)**。
- 真因：`3qVa2Lze` 是**我们自己 2026-10-05 提交的 ACTIVE alpha**（GBR/model53/同波 `gb_rank_opt_20261005`，表达式与 `QPK26lQX` **仅差 backfill 窗口 500 vs 250**）⇒ 典型「同腿近亲，self 冲 0.99+」。
- ⇒ **报告里的 prod 余量必须标注「台账快照值」，排序前必自查候选是否命中自家近期同波同族。**

**通道事实**：SUPER 不得走 `workflow_submit_alpha`（回 `super_requires_super_build`），必须 `tools/super_build.py submit`（内置 prod-gate）；该工具受全局锁拦，用户授权时以 `WQB_ALLOW_ALPHA_SUBMIT=1` 前缀放行。

## 四、留痕

- 本批记录：`results/submit_batch_20261006-1240.json`
- 台账：`ledger_kv` 中 `submit_<id>` 5 条（`submitted=True / final_status=ACTIVE`）
