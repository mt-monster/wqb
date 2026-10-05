# repair 情景卡

> 主文见 [`../SKILL.md`](../SKILL.md)；模板见 [`repair-recipes.md`](repair-recipes.md)。**动手改表达式的是 `wq-brain-alpha-optimization-v1`**——下面的卡回答「该往哪个方向修、怎么验收」，产出的变体仍要走它的校验层（verifier → `ghost-audit` → `wave_gate --batch-type repair`）。
> 线一律读 `wqb.config`（`GATES_INTERNAL` = 内部严线；`PLATFORM_CHECK_LINES` = 平台线）；下面出现的数值只是**演算例**（Fitness 公式的代入），不是新线。

## 卡 RE-1　降换手：Sharpe 过了、Fitness 因换手 32% 不过

- **症状**：Sharpe 1.7、Returns 6%、Turnover 32% → `Fitness = 1.7 × sqrt(0.06 / 0.32)` ≈ **0.74**，`LOW_FITNESS` FAIL（Sharpe 检查是过的；平台 `HIGH_TURNOVER` 线更宽，32% 不会触发它）。
- **根因**：换手偏高，Fitness 公式的分母 `max(Turnover, 0.125)` 变大。
- **动作**：对信号包一层平滑：`ts_decay_linear(<信号>, 5)` 或 `ts_mean(<信号>, 5)`（窗口取白名单 5 / 22）；或 `hump(<信号>, hump=0.01)`（命名参数）。目标：在 Sharpe、Returns 不变的假设下，换手压到 ≲ **17%** 时 Fitness ≥ 1.0（20% → ≈ 0.93；12.5% → ≈ 1.18）。
- **预期**：换手下降，但平滑同时会改变 Sharpe 与 Returns——**幅度没有库内实测，以重测为准**，把「前 → 后」的 Sharpe / Returns / Turnover / Fitness 写进本轮日志。
- **验收**：重测后 `LOW_FITNESS` 为 `PASS`，且 `Failed RA == 0`。
- **失败分支**：Fitness 仍不足（Sharpe 被平滑压低）→ 换窗口（5 ↔ 22）再试 1 次；仍不行 → 回 optimization-v1 Mode B 换想法（先想法后参数）。
- **反例**：换手已低于 12.5% 还继续压（分母被 floor，Fitness 不再涨）。

## 卡 RE-2　覆盖不足：cr < 0.4

- **症状**：字段体检 `CoverageRatio` < 0.4（长 / 短持仓过少），或 `CONCENTRATED_WEIGHT` 显示 `WARNING`。
- **动作**：`ts_backfill(<字段>, 66)`（低频字段）或 `group_backfill`；VECTOR 字段先经 `vec_avg` 等聚合再回填。
- **预期**：覆盖率上升，集中度风险下降。
- **验收**：重跑体检硬门（`wave_gate --batch-type repair` 内含；函数级 `tools/webdata_quality.py::check_expr_against_inspect` 返回 `ok=True`），且 `CONCENTRATED_WEIGHT` 为 `PASS`。
- **失败分支**：回填后 `WARNING` 仍在 → 这是表达式结构问题（瞬时离散计数），改为**时间平滑**（how-to-pass §4），**不要换中性化**。
- **反例**：把非缺失的字段也强行回填 66 天（会把陈旧值当新值）。

## 卡 RE-3　降相关：prod 0.78

- **症状**：某族首探 `check_correlation` 读数 0.78。
- **判据（不是另一套学说，就是 D0-P）**：≥ 0.75 → 家族记 `dead_end`：先 `forum_recon`（`found=true` 不得直接判死）→ `seal_dead_end`；下一步 = **换机制 / 换白名单不同的数据集**。
- **唯一例外**：候选已 `eligible`（资格判定表：主闸或旁路）**且**有 salvage 辅助腿 → 交 `wq-brain-alpha-optimization-v1` 的「组合腿救援」（形态库 F2 正交化优先；禁加权混合）。
- **对照**：读数 0.72（踩线带）→ 只允许 1 次结构性尝试（删腿 / 换广度轴，或 `group_neutralize(同信号, sector)`）；0.60–0.70 → 不扩变体、当天进步 8。
- **验收**：有终验读数（`refresh=True`）；落入哪一行按 D0-P 执行，已写入本轮日志。
- **反例**：磨 decay / 中性化 / 窗口；用 `POST /submit` 探测（通过即真提交）；「先跑 5 个探针再决定」（家族首探 = 1 条）。
