# GBR 区域独有规则（rules/）

> **定位**：只放**GBR 特有**的规则与纪律；九步通用正文在 `../../wq-brain-ra-pipeline/SKILL.md`，不在此重复。
> **as_of**：2026-10-18 ｜ 手写区，SKILL.md 生成块重渲不会覆盖它。
> **分工**：SKILL.md 只留入口与摘要（目标 ≤250 行，当前 315 行）；细则在 `rules/` 与 `../references/`。

| 文件 | 内容 |
|---|---|
| `six-step-gbr-override.md` | 六步纵深骨架的 GBR 覆盖项 + 改控制纪律（从 SKILL.md 手写区下沉） |
| **[`gate-and-submit-discipline.md`](gate-and-submit-discipline.md)** | **提交前五道闸的执行顺序与细则（as_of 2026-10-31）**：① 台账排除 ② RA+塔位 ③ 近十年 ④ self-corr ⑤ 互相关+配额；含 `LOW_ROBUST_UNIVERSE_SHARPE` 的分区下发差异、self-corr 判据分层、prod 收割 SQL、塔位杠杆（集内市场量 ⇒ 单塔）、本区已知数据面边界表 |

## 填充纪律

1. 只写**本区独有**的（别的区通用的回 `../wq-brain-ra-pipeline/`）；跨区普适规律沉淀到 `docs/experience/`。
2. 实证数字必须带 `as_of` + alpha id / 波号；判死结论写清「结构性 / 可修复」。
3. 门槛数字不抄字面量——引用 `PLATFORM_CHECK_LINES` / `GATES_*` 常量名（`tools/skill_lint` const-literal 闸）。
