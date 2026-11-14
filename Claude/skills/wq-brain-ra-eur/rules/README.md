# EUR 区域独有规则（rules/）

> **定位**：只放**EUR 特有**的规则与纪律；九步通用正文在 `../../wq-brain-ra-pipeline/SKILL.md`，不在此重复。
> **as_of**：2026-11-12 ｜ 手写区，SKILL.md 生成块重渲不会覆盖它。
> **分工**：SKILL.md 只留入口与摘要（目标 ≤250 行）；细则在 `rules/` 与 `../references/`。

| 文件 | 内容 |
|---|---|
| （待填）`six-step-eur-override.md` | 六步纵深骨架的 EUR 覆盖项 + 改控制纪律（从 SKILL.md 手写区下沉） |
| [`gate-and-submit-discipline.md`](gate-and-submit-discipline.md) | **本区闸门纪律**（2026-11-12 建）：SUB 比率闸 0.519×S / self 先于 prod / prod 熔断累加 / 带符号最大值 / checks.warning / 篮子互相关与组腿配额 |

## 填充纪律

1. 只写**本区独有**的（别的区通用的回 `../wq-brain-ra-pipeline/`）；跨区普适规律沉淀到 `docs/experience/`。
2. 实证数字必须带 `as_of` + alpha id / 波号；判死结论写清「结构性 / 可修复」。
3. 门槛数字不抄字面量——引用 `PLATFORM_CHECK_LINES` / `GATES_*` 常量名（`tools/skill_lint` const-literal 闸）。
