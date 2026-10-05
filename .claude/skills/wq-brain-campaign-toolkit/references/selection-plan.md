# 机制与对照驱动的选波

> 本页只讲**选波**（怎么把 GEM 产物选成一波）。波后怎么读结果、研究线索、纠错复验见 [`post-wave-reading.md`](post-wave-reading.md)。

## 两种模式

- **普通探索**：`--size N` 是容量上限。允许因历史去重、字段 / 族配额而少选；`wave_meta` 记录差额与原因。不得据此声称已覆盖全部机会。
- **已评审实验**：`--selection-contract-key KEY` 从同区域 ledger 读取下方清单。条数由 `required` 推导，容量不得小于它。保持现有配额、去重及后续门禁；冲突时报告缺失项，**不自动放宽或凑数**。

没有固定的 8 条或 12 条上限。先选经济机制，再为关键变化 / 残差等变换配水平基线或反证对照。相同字段换窗口通常属于参数敏感性，不能冒充多个独立机制。首次探针有限不代表全集搜索完成。

`--expected-count N`（固定机制批）数量不符时返回 `selection-count` 与排除原因，不写本波表达式或 `wave_meta`；`--source-wave` 显式指定 GEM 来源，重建时不再优先读残缺目标波。选中项若已回测、`dropped` 或 `superseded`，返回 `selection-state` 并回滚选集事务；落库后验证每个 picked 的状态与 `alpha_id`。**该检查只保证「本次 picked」，不会自动清理旧的 `selected` / `gated`。** `--size` 在 CLI 与 workflow S2 中都只表示容量，不会自动补 `expected-count`。预定机制 / 对照实验优先 `--selection-contract-key`：按 DB 清单推导数量，并核验 `source_id`、原式、`dataset` / `region` / `delay` / `source_wave` 及状态——同条数错表达式也会失败。`wave_meta.selection_audit` 记录来源项的选中 / 延后及原因；**未选不等于机制失败**。

**「受保护状态」**（`build_wave` 拒绝覆盖）：目标波里已有 `alpha_id`（已回测），或状态为 `superseded` / `dropped` 的行；另外，「计划外」的 `selected` / `gated` / 已回测行会阻断，防下游多发。

## DB 清单

由 `mcp__wqb-db__upsert_ledger_key(region=…, key=…, value=…)` 保存，约定键名 `selection_w<W>`（`<W>` = 目标波号；`--selection-contract-key` 接受任意键名）；来源必须是实际 GEM 产物，不能自己造表达式绕过 S2。

```json
{
  "region": "EUR", "dataset": "fundamental17", "delay": 1,
  "wave": "251", "source_wave": "s2_fundamental17_d1",
  "required": [
    {"source_id": 123, "expression": "<DB 原式逐字复制>",
     "mechanism": "receivables_efficiency", "role": "hypothesis",
     "rationale": "检验应收周转改善"},
    {"source_id": 124, "expression": "<配对基线 DB 原式>",
     "mechanism": "receivables_efficiency", "role": "control",
     "rationale": "保持预处理和分组一致，检验水平是否解释变化信号"}
  ]
}
```

ID 仅为格式示例。`required` 内 ID、原式和机制 / 角色对不得重复；同一机制如需两个不同对照，应明确命名各自问题。清单 `region` / `dataset` / `delay` / `wave` 必须与本次一致。

调用既有 `workflow_campaign(stage="S2", …)` 的 `extra_args` 传：`--selection-contract-key KEY --size N --enhance-diversity never --auto-coverage never`（两者缺省本就是 `never`，显式写出是为了让命令自证）。清单推导 `source_wave` 和 `expected_count`；显式传入冲突值会失败。旧 `--expected-count` 是兼容的数量检查，不具备身份覆盖保证。

## 失败及审计

源 ID 缺失、来源不符、表达式变化、已回测或受保护状态均阻断；不会自动恢复 `superseded` / `dropped`。字段 / 族配额或历史去重挡住清单项时，返回机制、原式和原因，不落目标波选集。先审查去重是否已有可复用证据，再决定修改计划、容量或分波；不要机械放大配额。目标波已有计划外 `selected` / `gated` / 已回测行时阻断，防下游多发；通常使用新波，只有无回测且已核实的旧选集才可显式整理。

`wave_meta` 记录模式、清单快照、容量、计划数、选中数、`source_id` / 原式 / 源状态以及选中或延后原因。单独源池中未选项原样保留；同目标波落选待选项仍按既有规则归档 `superseded`，保留原式和状态变更记录。`superseded` 不代表实证 `dead_end`；恢复须明确理由及 ID。
