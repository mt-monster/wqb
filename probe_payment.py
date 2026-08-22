#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""探查本账号 payment（顾问津贴）金额与发放时间。

试探多个候选端点，全文检索 payment / amount / date / payout / stipend /
quarter / next / estimate 等关键词。
"""
from __future__ import annotations

import asyncio
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
MCP = ROOT / "world-quant-brain-mcp"
sys.path.insert(0, str(MCP))
from brain_api import BrainApiClient  # noqa: E402

NEEDLES = [
    "payment", "amount", "payout", "stipend", "quarter", "next", "estimate",
    "date", "paid", "salary", "bonus", "reward", "compensation", "invoice",
    "weight", "valuefactor", "os", "rank",
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


async def raw(brain, url, label):
    print(f"\n### {label}: GET {url}")
    try:
        resp = await brain._request("GET", url)
        if resp.status_code >= 400:
            print(f"  HTTP {resp.status_code} -> {(resp.text or '')[:160]}")
            return None
        data = resp.json()
        print(f"  HTTP {resp.status_code}, type={type(data).__name__}")
        if isinstance(data, dict):
            print(f"  keys: {list(data.keys())}")
        hits = find_keys(data, NEEDLES)
        if hits:
            print(f"  >>> 命中 {len(hits)} 处:")
            for n, p, v in hits[:40]:
                print(f"      [{n}] {p} = {v}")
        else:
            print("  >>> 未命中关键词")
        return data
    except Exception as e:
        print(f"  ERROR: {str(e)[:200]}")
        return None


async def main():
    brain = BrainApiClient()
    await brain.ensure_authenticated()
    base = brain.base_url

    # 已知 consultant 端点（含 vf），完整 dump 看是否带 payment 字段
    await raw(brain, f"{base}/users/self/consultant", "consultant(full)")
    # 各 payment 候选端点
    await raw(brain, f"{base}/users/self/payment", "payment")
    await raw(brain, f"{base}/users/self/payments", "payments")
    await raw(brain, f"{base}/users/self/consultant/payment", "consultant/payment")
    await raw(brain, f"{base}/consultant/payments", "consultant/payments")
    await raw(brain, f"{base}/users/self/payment/estimate", "payment/estimate")
    await raw(brain, f"{base}/users/self/payment/summary", "payment/summary")
    await raw(brain, f"{base}/users/self/consultant/payments", "consultant/payments")


if __name__ == "__main__":
    asyncio.run(main())
