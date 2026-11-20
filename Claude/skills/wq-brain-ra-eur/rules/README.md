# EUR 区域独有规则（rules/）

> **定位**：只放**EUR 特有**的规则与纪律；九步通用正文在 `../../wq-brain-ra-pipeline/SKILL.md`，不在此重复。
> **as_of**：2026-11-12 ｜ 手写区，SKILL.md 生成块重渲不会覆盖它。
> **分工**：SKILL.md 只留入口与摘要（目标 ≤250 行）；细则在 `rules/` 与 `../references/`。

| 文件 | 内容 |
|---|---|
| （待填）`six-step-eur-override.md` | 六步纵深骨架的 EUR 覆盖项 + 改控制纪律（从 SKILL.md 手写区下沉） |
| [`gate-and-submit-discipline.md`](gate-and-submit-discipline.md) | **本区闸门纪律**（2026-11-12 建）：SUB 比率闸 0.519×S / self 先于 prod / prod 熔断累加 / 带符号最大值 / checks.warning / 篮子互相关与组腿配额 |
| [`settings-axis-strategy.md`](settings-axis-strategy.md) | **本区设置轴纪律**（2026-11-19 建 / 11-20 升级三段式）：**档位净化**（risk_neutralized_sharpe 判标准档/风险线）→ **历史分布+跨宇宙探测并行**（宇宙轴摆幅 0.63–0.86 ≫ 中性化轴 0.17–0.31）→ **近闸定向扫参**（A/B/C 三分支）→ 全设置仅两种情形；F=S·√(ret/0.125) 可行域否决 |
| [`dispatch-discipline.md`](dispatch-discipline.md) | **本区派发纪律**（2026-11-20 建，与设置轴正交）：批次两种失败形态（**A 编译期连坐**＝父 ERROR＋其余 CANCELLED，**整批丢槽位** / **B 运行期逐条**＝单条 WARNING）→ **派发分层小批**（新算子/新字段/新组合 ⇒ 1~2 条先探；「同类别全替换」批必须逐层小批）→ 本地三闸 → 收批必核子任务状态；平台口径坑（children 是相对路径、单条无 children、n=1 发裸 dict） |

## 填充纪律

1. 只写**本区独有**的（别的区通用的回 `../wq-brain-ra-pipeline/`）；跨区普适规律沉淀到 `docs/experience/`。
2. 实证数字必须带 `as_of` + alpha id / 波号；判死结论写清「结构性 / 可修复」。
3. 门槛数字不抄字面量——引用 `PLATFORM_CHECK_LINES` / `GATES_*` 常量名（`tools/skill_lint` const-literal 闸）。
