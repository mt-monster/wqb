# -*- coding: utf-8 -*-
"""KB 社区模板库读取/过滤/导出工具（P1-5：让 59KB 社区模板回流生成端）。

数据源（权威）：data/wqb.db ledger_kv 中 region='KB' 的两个键：
  - community_tpl_kb ：论坛模板候选库（templates / ghost_operator_advisory /
    placeholder_conventions / categories）
  - template_kb      ：validated / failed 两层（蒸馏晋升终点）

用途：
  1. 列出/检索社区模板（按 category、ghost 过滤）；
  2. 导出为 GEM ideas 可消费的 JSON（--emit-ideas），经
     `run.py --ideas-file <导出文件>` 注入 brain-make-some-gem；
  3. 任何模板入批前用 ghost_operator_advisory 做算子替换/拦截。

退出码：0=成功；1=失败（DB/键缺失等）。只读工具，绝不写库。
"""
from __future__ import annotations

import argparse
import json
import os
import sqlite3
import sys


def _load_kb(db_path: str) -> dict:
    if not os.path.exists(db_path):
        print(f"[kb_templates] DB 不存在：{db_path}", file=sys.stderr)
        sys.exit(1)
    conn = sqlite3.connect(db_path)
    try:
        row = conn.execute(
            "SELECT value FROM ledger_kv WHERE region='KB' AND key='community_tpl_kb'"
        ).fetchone()
        if not row:
            print("[kb_templates] ledger 缺 KB/community_tpl_kb 键", file=sys.stderr)
            sys.exit(1)
        return json.loads(row[0])
    finally:
        conn.close()


def _ghost_names(kb: dict) -> list:
    adv = kb.get("ghost_operator_advisory", {}) or {}
    return sorted((adv.get("ghost_to_equivalent") or {}).keys())


def _expr_uses_ghost(expr: str, ghosts: list) -> list:
    return [g for g in ghosts if f"{g}(" in expr or f"{g} " in expr]


def main() -> int:
    ap = argparse.ArgumentParser(description="KB 社区模板库读取/过滤/导出（只读）")
    ap.add_argument("--db", default=os.path.join(".", "data", "wqb.db"))
    ap.add_argument("--category", default=None, help="按 category 过滤")
    ap.add_argument("--search", default=None, help="按 id/描述关键词过滤")
    ap.add_argument("--with-ghost", action="store_true",
                    help="保留含幽灵算子的模板（默认剔除并在报告中单列）")
    ap.add_argument("--limit", type=int, default=20)
    ap.add_argument("--emit-ideas", default=None,
                    help="导出为 GEM ideas JSON 到指定路径（配合 run.py --ideas-file）")
    ap.add_argument("--json", action="store_true", help="输出完整 JSON")
    a = ap.parse_args()

    kb = _load_kb(a.db)
    templates = kb.get("templates", []) or []
    if isinstance(templates, dict):
        templates = [{"id": k, **(v if isinstance(v, dict) else {"tpl": v})}
                     for k, v in templates.items()]
    ghosts = _ghost_names(kb)

    picked, ghost_blocked = [], []
    for t in templates:
        if not isinstance(t, dict):
            continue
        exprs = json.dumps(t, ensure_ascii=False)
        used = _expr_uses_ghost(exprs, ghosts)
        if used and not a.with_ghost:
            ghost_blocked.append((t.get("id") or t.get("tpl_id") or "?", used))
            continue
        if a.category and a.category not in json.dumps(t.get("category", ""), ensure_ascii=False):
            continue
        if a.search:
            hay = json.dumps(t, ensure_ascii=False)
            if a.search.lower() not in hay.lower():
                continue
        picked.append(t)
        if len(picked) >= a.limit:
            break

    summary = {
        "kb_updated_at": kb.get("updated_at"),
        "total_templates": len(templates),
        "ghost_ops": ghosts,
        "picked": len(picked),
        "ghost_blocked_sample": ghost_blocked[:5],
        "ghost_blocked_total": len(ghost_blocked),
    }

    if a.emit_ideas:
        ideas = {
            "dataset_id": "KB_COMMUNITY_TPL",
            "region": "",
            "delay": 1,
            "source": "kb_templates.py",
            "kb_updated_at": kb.get("updated_at"),
            "ideas": [
                {
                    "idea_name": t.get("id") or t.get("tpl_id") or f"tpl_{i}",
                    "concept": t.get("description") or t.get("category") or "",
                    "template": t.get("template") or t.get("expression") or "",
                    "placeholders": t.get("placeholders") or [],
                    "category": t.get("category"),
                    "note": "来自 KB/community_tpl_kb；入批前按 ghost_operator_advisory 替换",
                }
                for i, t in enumerate(picked)
            ],
        }
        with open(a.emit_ideas, "w", encoding="utf-8", newline="") as f:
            json.dump(ideas, f, ensure_ascii=False, indent=1)
        summary["emitted"] = a.emit_ideas

    if a.json:
        print(json.dumps({"summary": summary, "templates": picked},
                         ensure_ascii=False, indent=1))
    else:
        print(json.dumps(summary, ensure_ascii=False, indent=1))
        for t in picked:
            tid = t.get("id") or t.get("tpl_id") or "?"
            print(f"  - {tid}: {str(t.get('description') or t.get('category'))[:80]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
