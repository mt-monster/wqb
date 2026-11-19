# -*- coding: utf-8 -*-
"""_lib.dead_sets — 判死集合读取的薄壳（2026-11-19 新增）。

**判据本体只有一份**：``src/wqb/dead_datasets.py``（见该模块 docstring：
ledger 判死记录有四种键形态，后缀匹配会漏拦/误拦）。

本薄壳只做两件事：
1. 能导入 ``wqb`` 时**委托**规范实现（仓库内 / 装了仓库 skill 的场景）；
2. 不能导入时**降级**：只认规范形态 ``<ds>_dead``，并**显式打印 WARN** 说明
   「聚合键 / 族级镜像 / 带日期后缀」的判死记录未纳入检查——
   降级方向是「少拦 + 明说」，不是「复制一份可能漂移的解析」。

与 ``_lib/db.py`` 同一模式（连接工厂同口径、判据本体只有一份）。
"""
from __future__ import annotations

import json

DEGRADED = False

try:  # pragma: no cover — 取决于运行环境是否装了仓库 skill
    from wqb.dead_datasets import dead_levels as _dead_levels
    DEGRADED = False
except Exception:  # noqa: BLE001 — 仓库外安装（wqb 不可导入）
    _dead_levels = None
    DEGRADED = True


def read_dead_rows(conn, region: str) -> list[tuple[str, str]]:
    """读某区全部**判死语义**的 ledger 行（不限键形态）。"""
    cur = conn.cursor()
    cur.execute(
        "SELECT key, value FROM ledger_kv WHERE region=? AND ("
        " key LIKE '%_dead' OR key LIKE 'dead_%' OR key LIKE '%_dead_%'"
        " OR key LIKE '%_dead_end' OR key LIKE 'dead_end_%')",
        (region,),
    )
    return cur.fetchall()


def dead_reasons(rows) -> dict[str, str]:
    """``{dataset: 一行判死证据}``——给硬闸命中时当场出示（误判当场可辨）。

    与 :func:`dead_levels` 同源（同一份 rows）。降级模式下只给规范形态 ``<ds>_dead`` 的原始
    reason 文本；不复制解析逻辑，只做「取值」。
    """
    out: dict[str, str] = {}
    for key, value in rows:
        try:
            payload = json.loads(value) if isinstance(value, str) else value
        except (json.JSONDecodeError, TypeError):
            payload = None
        if not isinstance(payload, dict):
            continue
        ds = payload.get("dataset") if isinstance(payload.get("dataset"), str) else None
        if not ds and key.endswith("_dead"):
            ds = key[:-5]
        if not ds:
            continue
        reason = str(payload.get("reason") or payload.get("evidence")
                     or payload.get("conclusion") or "")[:180]
        extra = []
        if payload.get("dead_at"):
            extra.append(str(payload["dead_at"]))
        if payload.get("evidence"):
            extra.append(str(payload["evidence"])[:80])
        if payload.get("source"):
            extra.append(str(payload["source"])[:60])
        line = reason
        if extra:
            line = (line + " 〔" + " | ".join(extra) + "〕").strip()
        out.setdefault(ds, line)
    return out


def dead_levels(rows) -> dict[str, list[str]]:
    """返回 ``{"dataset": [...], "conditional": [...], "family": [...]}``。

    降级模式（仓库外安装）只返回规范形态 ``<ds>_dead`` 的数据集级集合，
    并由调用方打印 WARN——**不复制**规范实现的解析逻辑。
    """
    if not DEGRADED:
        return _dead_levels(rows)
    out: dict[str, list[str]] = {"dataset": [], "conditional": [], "family": []}
    for key, value in rows:
        if not key.endswith("_dead"):
            continue
        try:
            payload = json.loads(value) if isinstance(value, str) else value
        except (json.JSONDecodeError, TypeError):
            payload = None
        if isinstance(payload, dict) and payload.get("family") not in (None, "", key[:-5]):
            out["family"].append(key[:-5])       # 族级 ⇒ 不硬拦
            continue
        out["dataset"].append(key[:-5])
    return {k: sorted(set(v)) for k, v in out.items()}
