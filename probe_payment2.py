#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""最终确认：检查 get_user_activities / pyramid 三个 mixin 方法是否含 payment 字段。"""
from __future__ import annotations

import asyncio
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
MCP = ROOT / "world-quant-brain-mcp"
sys.path.insert(0, str(MCP))
from brain_api import BrainApiClient  # noqa: E402

NEEDLES = [
    "payment", "amount", "payout", "stipend", "quarter", "next", "estimate",
    "paid", "date", "salary", "bonus", "reward", "compensation", "invoice",
    "weight", "valuefactor", "value", "total",
]


def find_keys(obj, needles, path=""):
    hits = []
    for n in needles:
        nl = n.lower()
        def rec(o, p):
            if isinstance(o, dict):
                for k, v in o.items():
                    kk = str(k).lower()
                    if nl in kk:
                        hits.append((n, p + "/" + str(k),
                                     v if not isinstance(v, (dict, list)) else f"<{type(v).__name__}>"))
                    rec(v, p + "/" + str(k))
            elif isinstance(o, list):
                for i, v in enumerate(o[:50]):
                    rec(v, p + f"[{i}]")
            else:
                s = str(o).lower()
                if nl in s:
                    sv = str(o)
                    hits.append((n, p, (sv[:80] + "…") if len(sv) > 80 else sv))
        rec(obj, path)
    return hits


async def main():
    brain = BrainApiClient()
    await brain.ensure_authenticated()

    for coro, label in [
        (brain.get_user_activities("self"), "get_user_activities"),
        (brain.get_pyramid_multipliers(), "get_pyramid_multipliers"),
        (brain.get_pyramid_alphas(), "get_pyramid_alphas"),
    ]:
        print(f"\n### {label}")
        try:
            data = await coro
            print(f"  type={type(data).__name__}")
            if isinstance(data, dict):
                print(f"  keys: {list(data.keys())}")
            hits = find_keys(data, NEEDLES)
            if hits:
                print(f"  >>> 命中 {len(hits)} 处:")
                for n, p, v in hits[:40]:
                    print(f"      [{n}] {p} = {v}")
            else:
                print("  >>> 未命中 payment/amount/date 等关键词")
        except Exception as e:
            print(f"  ERROR: {str(e)[:200]}")


if __name__ == "__main__":
    asyncio.run(main())
