# probe-sop retired 2026-10-20

**归档日期**：2026-10-20
**归档原因**：EUR 区策略反转——由 `probe-only` 改为 `full-coverage`（数据集必须做尽）。原探针 SOP 与「全量覆盖」语义直接冲突，不再适用；归档保留历史留档。

## 原文件

- `_probe-sop.md`（原 `Claude/skills/wq-brain-ra-eur/references/_probe-sop.md`）——2026-10-13 定稿的探针派发 SOP，8-10 槽位的稀疏派发规则、双结构保底、EUR 失败模式预筛等。

## 现行替代

- **新 SOP**：`Claude/skills/wq-brain-ra-eur/SKILL.md` 「全量覆盖操作纪律」段。
- **三道闸**：`tools/full_coverage_gate.py`
  - 闸 1：字段全量覆盖（`coverage ≥ 1.0`）
  - 闸 2：模板族全量（`min_families ≥ 3`）
  - 闸 3：边界算子穷举（`tracking/EUR/reference/boundary_ops_eur.json`）
- **边界算子清单**：`Claude/skills/wq-brain-ra-eur/references/_boundary-ops-eur.md`

## 恢复条件

本归档**不是删除**。以下任一条件成立时可恢复到 `Claude/skills/wq-brain-ra-eur/references/`：

1. EUR 全量覆盖闸证明「数据集必须做尽」在 EUR 区成本过高、平台不支持；
2. 用户明确撤回 2026-10-20 全量覆盖决议；
3. 新策略连续 3 波次 |S|<0.5 且三闸全过——即证明做尽后仍无信号，此时需回到探针式做粗筛再择重跑。

## 相关文件变更

- `Claude/skills/wq-brain-ra-eur/SKILL.md`：入场状态改 `full-coverage`；「探针派发 SOP」段整体替换为「全量覆盖操作纪律」；六步骨架 ②③⑤⑥ 补齐 EUR 覆盖。
- `tracking/EUR/reference/methodology_rules.json`：新增 3 条 `gate_override` 规则（`eur_full_field_coverage_v1` / `eur_template_family_full_sweep_v1` / `eur_boundary_ops_exhaust_v1`）。
- `tools/full_coverage_gate.py`：新建，三道闸前置门禁脚本。
- `Claude/skills/wq-brain-ra-eur/references/_boundary-ops-eur.md`：新建，边界算子人可读清单。
- `tracking/EUR/reference/boundary_ops_eur.json`：新建，边界算子机器可读配置。
