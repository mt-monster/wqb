#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""把 ``get_operators`` 的实时输出刷进 docs/reference/operators_catalog.json。

``wqb.expression.op_arity`` 的签名表是从这份 catalog 的 ``definition`` 串推导
的（``name = <字面量>`` 即命名参数）。平台加算子或改签名后，闸门要跟着更新，
否则新算子一律"未知放行"，等于没闸。

用法::

    # 1) 让 Agent 调 mcp__wq-brain-http__get_operators，把结果存成 JSON
    # 2) 刷进 catalog（原样输出 / {"results": [...]} / 裸 list 都吃）
    python tools/refresh_operator_catalog.py raw_get_operators.json

    # 只看会变什么，不写盘
    python tools/refresh_operator_catalog.py raw.json --dry-run

写盘后建议跑一遍回归，确认新签名没把历史合法写法误杀::

    python -m pytest tests/unit/test_op_arity.py -q
"""
from __future__ import annotations

import argparse
import datetime
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DST = os.path.join(ROOT, "docs", "reference", "operators_catalog.json")


def _entries(payload):
    """兼容 MCP 原样输出 / {"results": [...]} / 裸 list 三种形态。"""
    if isinstance(payload, dict):
        for key in ("result", "results", "operators"):
            if key in payload:
                return _entries(payload[key])
        return []
    if isinstance(payload, list):
        return [it for it in payload if isinstance(it, dict) and "name" in it]
    return []


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="刷新算子 catalog 快照")
    ap.add_argument("source", help="get_operators 输出的 JSON 文件（'-' 读 stdin）")
    ap.add_argument("--out", default=DST, help=f"输出路径（默认 {DST}）")
    ap.add_argument("--dry-run", action="store_true", help="只报告差异，不写盘")
    a = ap.parse_args(argv)

    raw = sys.stdin.read() if a.source == "-" else open(
        a.source, encoding="utf-8").read()
    entries = _entries(json.loads(raw))
    if not entries:
        print("[fail] 源里没解析出算子条目")
        return 1

    old = {}
    if os.path.isfile(a.out):
        with open(a.out, encoding="utf-8") as f:
            old = {o["name"]: o.get("definition", "")
                   for o in _entries(json.load(f))}
    new = {o["name"]: o.get("definition", "") for o in entries}

    added = sorted(set(new) - set(old))
    removed = sorted(set(old) - set(new))
    changed = sorted(n for n in set(new) & set(old) if new[n] != old[n])
    print(f"[diff] 算子 {len(old)} -> {len(new)}；"
          f"新增 {len(added)} 删除 {len(removed)} 签名变更 {len(changed)}")
    for n in added:
        print(f"  + {n}: {new[n]}")
    for n in removed:
        print(f"  - {n}: {old[n]}")
    for n in changed:
        print(f"  ~ {n}: {old[n]!r} -> {new[n]!r}")

    if a.dry_run:
        print("[dry-run] 未写盘")
        return 0

    payload = {
        "_source": "mcp__wq-brain-http__get_operators (live BRAIN platform)",
        "_fetched_at": datetime.date.today().isoformat(),
        "_note": "刷新方式：python tools/refresh_operator_catalog.py <get_operators 输出.json>",
        "count": len(entries),
        "results": entries,
    }
    os.makedirs(os.path.dirname(os.path.abspath(a.out)), exist_ok=True)
    with open(a.out, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, ensure_ascii=False)
    print(f"[done] 写入 {a.out}（{len(entries)} 个算子）；"
          f"请跑 python -m pytest tests/unit/test_op_arity.py -q 确认无误杀")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
