# -*- coding: utf-8 -*-
"""把实测经验写入 `KB/template_kb` 的 measured 层（2026-11-15 P4）。

**不碰人工维护的 `templates[]`**：新增两个子键
- `measured_validated[]`：本区实测出现过 win 的 skeleton / family；
- `measured_failed[]`：本区统计判死的 skeleton / family（advisory，不是硬禁）。

`assemble_priors` 以**低于人工层**的优先级读取它们（source=`template_kb_measured`），
这样 `template_kb` 不再是有读无写的 orphan，同时不会用统计覆盖人工验证过的模板。
"""
from __future__ import annotations

import datetime
from typing import Any, Dict, List

MAX_MEASURED = 200


def _entry(kind: str, name: str, region: str, g: Dict[str, Any], wave: str) -> Dict[str, Any]:
    return {
        "kind": kind,
        "name": name,
        "region": region.upper(),
        "n": g.get("n"),
        "n_win": g.get("n_win"),
        "n_near": g.get("n_near"),
        "max_sharpe": g.get("max_sharpe"),
        "dominant_wall": g.get("dominant_wall"),
        "dominant_wall_share": g.get("dominant_wall_share"),
        "wave": wave,
        "evidence_attempt_ids": g.get("examples") or [],
        "updated_at": datetime.datetime.now().isoformat(timespec="seconds"),
    }


def _upsert(items: List[Dict[str, Any]], entry: Dict[str, Any]) -> List[Dict[str, Any]]:
    key = (entry.get("kind"), entry.get("region"), entry.get("name"))
    out = [x for x in items
           if (x.get("kind"), x.get("region"), x.get("name")) != key]
    out.insert(0, entry)
    return out[:MAX_MEASURED]


def publish_templates(store: Any, region: str, lesson: Dict[str, Any]) -> Dict[str, Any]:
    """写 measured_validated / measured_failed；保留 templates[] 与其它键。"""
    region = region.upper()
    wave = str(lesson.get("wave") or "")
    kb = store.get_ledger("KB", "template_kb") or {}
    if not isinstance(kb, dict):
        kb = {}
    validated = list(kb.get("measured_validated") or [])
    failed = list(kb.get("measured_failed") or [])

    for kind, key in (("skeleton", "by_skeleton"), ("family", "by_family")):
        for g in (lesson.get(key) or []):
            if not isinstance(g, dict):
                continue
            name = g.get(kind)
            if not name or name == "_unknown":
                continue
            entry = _entry(kind, str(name), region, g, wave)
            if (g.get("n_win") or 0) > 0:
                validated = _upsert(validated, entry)
            if g.get("dead"):
                failed = _upsert(failed, entry)

    kb["measured_validated"] = validated
    kb["measured_failed"] = failed
    kb["measured_updated_at"] = datetime.datetime.now().isoformat(timespec="seconds")
    kb["measured_source"] = "wqb.knowledge.templates.publish_templates"
    store.upsert_ledger("KB", "template_kb", kb)
    return {"validated": len(validated), "failed": len(failed), "region": region}
