#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""preflight.py — 发批前三闸（括号平衡 → 元数/算子存在性 → 元数兜底）。

用法::  python tracking/KOR/scripts/preflight.py <exprs.txt>
退出码 0=全过；3=有不过（不得发批，否则整批连坐 CANCELLED）。
"""
from __future__ import annotations
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "src"))

def main() -> int:
    if len(sys.argv) < 2:
        print(__doc__); return 2
    exprs = [l.strip() for l in open(sys.argv[1], encoding="utf-8") if l.strip()]
    bad = 0
    for i, e in enumerate(exprs, 1):
        bal = e.count("(") - e.count(")")
        if bal:
            print(f"[preflight] {i}: 括号不平衡 {bal:+d}"); bad += 1
    if bad:
        print(f"[preflight] ABORT: {bad} 条括号不平衡"); return 3
    print(f"[preflight] 括号平衡 OK（{len(exprs)} 条）")
    try:
        from wqb.expression import op_arity as oa
        oa.ensure_safe_for_dispatch(exprs)
        print("[preflight] 元数/算子存在性闸 OK（ensure_safe_for_dispatch）")
    except Exception as ex:
        print(f"[preflight] ABORT: 元数/算子闸失败 -> {type(ex).__name__}: {str(ex)[:400]}")
        return 3
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
