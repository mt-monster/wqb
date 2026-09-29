# SA 情景卡（从零到一）

> 主 SOP 见 [`../SKILL.md`](../SKILL.md)；参数与证据见 [`levers-and-evidence.md`](levers-and-evidence.md)。旧版缺这三张「从零到一」情景（skills 审查 SP-19），只有零散案例。命令以 `python tools/super_build.py --help` 与各子命令 `--help` 为准。
> 前置共同点：**用户已明确要组 SA**；提交前另需**用户明确确认**（不可逆）。

## 情景 SA-01　KOR / IND 从 0 到 SA

- **前置状态**：区域 R 是 KOR 或 IND；不知道本区 ACTIVE REGULAR 够不够 10 颗。
- **步骤**
  1. `python tools/sa_probe.py --region KOR` → 预期 `verdict: GO / BLOCKED`、`eligible`、`need`。
     - `BLOCKED`（例：`eligible 7 → need 3`）→ 把「区域 / 缺口 3 颗 /（PROD 已饱和时）需 prod < 0.55 的新血」交 `wq-brain-ra-pipeline`，**结束本卡**。
  2. `GO` → 选中性化：KOR / IND 已知最优 STATISTICAL（levers §1），仍须各扫一遍；`python tools/super_build.py select --region KOR --neutralization STATISTICAL --decay 5 --selection-limit 10 --self-gate 0.55`。
  3. `python tools/super_build.py status --alpha-id <ID>` → 无 `ERROR`、无 `FAIL`。
  4. `python tools/super_build.py probe --alpha-id <ID>` → `PASS` 则请用户确认；`BLOCKED` 按下面分支。
  5. 用户确认后 `python tools/super_build.py submit --alpha-id <ID>`（默认带 prod 闸）→ `status` 核验 `ACTIVE`。
- **分支**：SELF 高 → decay 拉到 200–300 再试（KOR 曲线，levers §3；同时盯 turnover ≥ 0.02）；PROD 高 → 先做 levers §3 的「prod < 0.6 硬门」零成本探针，成分池 prod 分布本身高就是**饱和**，停止调参、回 RA 挖新血；`ERROR: At least 10 component alphas` → 情景 SA-02。
- **产物与落点**：SUPER alpha（平台侧）；S6 由 `wq-backtest-monitor` §14 回写台账。
- **完成定义与失败分支**：`status == ACTIVE`；被 403 拒绝零成本，按 FAIL 名回上面分支。
- **反例**：不要凭「本区应该够了」的印象跳过 `sa_probe`；不要把 USA 的 SUBINDUSTRY 当 KOR / IND 的缺省；不要在 PROD 已饱和（KOR 0.78）时继续扫 decay。

## 情景 SA-02　组件恰好 10 颗（放宽 gate 的路径与代价）

- **前置状态**：`sa_probe` 的 `eligible` 恰好 10（GLB 2026-09-24：0 颗 SUPER，池子未被消耗）。
- **步骤**：`select` 用缺省 `--self-gate 0.55` → 秒级 `status: ERROR / At least 10 component alphas` → 依次放宽：`--self-gate 0.65` → `0.70` → `0.85`（每档一次 select，秒级回错，成本极低）；仍不足再试 `--turnover-max 0.6`（池内成分 turnover 上限 0.5495 时）、`--prod-ceiling 1.0`。
- **分支**：0.70 即成（GLB A1NQ57NW）→ 走 SA-01 第 3 步起；放宽到 0.85 仍不足 → 回 RA 补缺口。
- **代价**：gate 越宽，被纳入的成分与 book 越相关 → SELF 更难过；放宽只解决「组件够不够」，不解决「SELF / PROD 过不过」。
- **完成定义**：SUPER simulation 无 `ERROR`。
- **反例**：不要靠加大 `--selection-limit` 凑数（超过有效池后无效）；不要一步跳到最宽的 gate（越宽越易近克隆）。

## 情景 SA-03　近克隆被拒（同构淘汰法）

- **前置状态**：本区已有 ≥ 1 颗 ACTIVE SUPER（KOR 已有 3 颗）；`probe` 的 SELF ≈ 0.9+，且 top 命中某颗已 ACTIVE 的 SA。
- **步骤**
  1. 枚举存量 SA 的 `(neutralization, decay)` 组合（`get_alpha_details` 读各 SA 的 settings）。
  2. 新变体**刻意错开**：不用任何已存在的组合（例：存量有 STATISTICAL/dec5、dec30 → 新变体用 SUBINDUSTRY/dec10）。
  3. 逐个 `select` → `status` → `probe`，`PASS` 者请用户确认后再 `submit`。**不要**用 `submit` 当「试探」：第一个通过的就是真提交，未必最优。
  4. 被淘汰的变体：打 `RETIRE_<YYYYMMDD>` 标签并 hidden（规范见 `docs/alpha_properties_spec.md`），撞了谁写进描述；不用 RED。
- **分支**：所有错开的组合仍近克隆 → 池子被消耗（KOR 13 颗大多被 3 颗 SA 用过）→ 新血 REGULAR 才是出路（回 RA），不再磨 decay。
- **完成定义**：某变体 `probe = PASS` 且用户确认后 `ACTIVE`。
- **反例**：不要重提与存量同 `(neutralization, decay)` 的变体（KOR 案例 4：STATISTICAL/dec5 → SELF 0.9729）；不要按 value 预判 PASS / FAIL（分界 0.86–0.89 不稳定）。

## 情景 SA-04　PROD 饱和：什么时候停

- **前置状态**：`probe` 的 PROD ≥ 0.7，且 levers §3 的「prod < 0.6 硬门」探针报 `At least 10 component alphas`（合格低 prod 成分不足 10 颗）。
- **步骤**：**停止调参**（decay / 评分 / 中性化都动不了成分池的 prod 地板：USA 0.85–0.91、KOR 0.78）→ 输出缺口清单（区域、需要 N 颗 prod < 0.55 的新 REGULAR）交 `wq-brain-ra-pipeline` → 新血 ACTIVE 后回 SA-01 第 2 步，用「宽篮 + 低 decay（3–10）」这套已过 SELF 的配置直接重提。
- **完成定义**：已交接给 RA，且不再消耗仿真槽在同一个池上调参。
- **反例**：不要用 `--allow-prod-above-07` 绕过这条线：那是用户显式豁免才有的开关，不是「PROD 饱和」的解法。
