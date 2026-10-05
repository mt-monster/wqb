# -*- coding: utf-8 -*-
"""wqb.semantic_ledger — ``s1_semantic_*`` 语义台账的解析与 L3.5 判定唯一口径。

为什么单独成模块（2026-10-05）：判定「台账是否含 L3.5 结构族」这件事有两个消费点，
必须同源，否则一处按「键存在」判、另一处按「族非空」判就会分叉——
  1. ``src/wqb/workflow/nodes/campaign.py`` 的 S1 收尾（补做触发条件）；
  2. ``tools/field_semantic_classify.py --all``（跳过已有完整台账的选择口径）。

★ 关键口径：判定用「**键存在**」而非「族非空」。
原生集（``fundamental*`` / ``pv*`` / ``news*``）字段名不带角色/期限/方向后缀，``families``
为空是**正确结果**；若按「族为空」判待补做，会导致每次 S1 都重跑、永不幂等。
只有旧版（families 功能之前生成的）台账才真正**不含** ``families`` / ``family_stats`` 键。
"""
from __future__ import annotations

import json
from typing import Optional, Union

#: L3.5 结构层的标志键：新版 ``field_semantic_classify`` 会同时写这两个键。
_L35_KEYS = ("families", "family_stats")


def parse_ledger(value: Union[str, bytes, bytearray, dict, None]) -> Optional[dict]:
    """把台账 ``value`` 列解析成 dict。

    - dict 原样返回；
    - str / bytes → JSON 解析，失败或非 dict 结果返回 ``None``；
    - None / 空串 → ``None``。

    调用方据 ``None`` 判「台账不可用」，与「台账在但缺 L3.5」是两种不同状态。
    """
    if value is None:
        return None
    if isinstance(value, dict):
        return value
    if isinstance(value, (bytes, bytearray)):
        try:
            value = value.decode("utf-8")
        except UnicodeDecodeError:
            return None
    if not isinstance(value, str):
        return None
    value = value.strip()
    if not value:
        return None
    try:
        parsed = json.loads(value)
    except (ValueError, TypeError):
        return None
    return parsed if isinstance(parsed, dict) else None


def ledger_has_l35(value: Union[str, bytes, bytearray, dict, None]) -> bool:
    """台账是否含 L3.5 结构族（``families`` / ``family_stats`` 任一键存在）。

    判定基于**键存在**，不看族是否为空 —— 见模块 docstring 的幂等性说明。
    解析失败或台账为空一律 ``False``（视为待补做）。
    """
    sem = parse_ledger(value)
    if not isinstance(sem, dict):
        return False
    return any(k in sem for k in _L35_KEYS)


def family_count(value: Union[str, bytes, bytearray, dict, None]) -> int:
    """台账里的族数量（``families`` 为 dict 时取其长度，否则 0）。纯便捷函数。"""
    sem = parse_ledger(value)
    if not isinstance(sem, dict):
        return 0
    fams = sem.get("families")
    return len(fams) if isinstance(fams, dict) else 0
