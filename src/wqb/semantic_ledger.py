# -*- coding: utf-8 -*-
"""`s1_semantic_<ds>` 台账「是否含 L3.5 族能力」的**唯一判定口径**。

## 为什么需要单一事实源

判定「这个语义台账要不要补做」时，有两个容易混淆的语义：

- **族非空**（`families` 里有东西）—— 表示这个数据集**产出了**结构族；
- **含 L3.5**（台账由带族能力的版本生成）—— 表示这个数据集**已经被 L3.5 处理过**。

二者不等价：原生集（`fundamental*` / `pv*` / `news*`）字段名不带角色后缀，
`build_families()` 会**正确地**返回空族。若用「族非空」当补做条件，这些集永远达不到
"完整"状态 ⇒ `--all` 永不幂等、S1 每次都重跑（2026-10-01 实测把
`test_batch_writes_ledger_and_is_idempotent` 跑红）。

故补做条件一律用 **含 L3.5**（`family_stats` 或 `families` 键存在），
「族非空」只作展示/提示用。

消费方（必须都从这里取，禁各写一份正则或 `bool(sem.get(...))`）：
  - `tools/field_semantic_classify.py::run_all`（`--all` 跳过判断）
  - `src/wqb/workflow/nodes/campaign.py::_semantic_coverage_check`（S1 自动补做）
"""
from __future__ import annotations

import json
from typing import Any

#: 台账键前缀
LEDGER_KEY_PREFIX = "s1_semantic_"


def parse_ledger(value: Any):
    """解析 ledger_kv.value → dict；不可解析返回 None（不抛）。"""
    if value is None:
        return None
    try:
        sem = json.loads(value) if isinstance(value, (str, bytes)) else value
    except (ValueError, TypeError):
        return None
    return sem if isinstance(sem, dict) else None


def ledger_has_l35(value: Any) -> bool:
    """台账是否由**含 L3.5 族能力**的版本生成（决定要不要补做）。

    判据 = `family_stats` 或 `families` 键存在（新版 `classify_dataset()` 两者必写，
    即使族为空也会写 `family_stats: {"n_families": 0, ...}`）。
    """
    sem = parse_ledger(value)
    if sem is None:
        return False
    return ("family_stats" in sem) or ("families" in sem)


def ledger_family_count(value: Any) -> int:
    """台账里结构族的个数（展示用；0 表示"该集无族"，不等于"需要补做"）。"""
    sem = parse_ledger(value)
    if sem is None:
        return 0
    fams = sem.get("families")
    return len(fams) if isinstance(fams, dict) else 0
