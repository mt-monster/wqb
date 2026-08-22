#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""扩展探查：定位本账号 'vf'（Value Factors 价值因子）的取值来源。

vf 是顾问级账户指标（越接近 1 越好），与 OS 表现和季度津贴直接相关。
候选来源：base-payment / other-payment / pyramid-multipliers / pyramid-alphas /
user_activities，以及 research/consultant/payments 猜测端点。全文检索 vf / valueFactor / value。
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

NEEDLES = ["vf", "valuefactor", "value factor", "value_fraction", "valuefraction", "v.f."]


def find_keys(obj, needles, path=""):
    hits = []
    for n in needles:
        nl = n.lower()
        def rec(o, p):
            if isinstance(o, dict):
                for k, v in o.items():
                    kk = str(k).lower()
                    if nl in kk:
                        hits.append((n, p + "/" + str(k), v if not isinstance(v, (dict, list)) else f"<{type(v).__name__}>"))
                    rec(v, p + "/" + str(k))
            elif isinstance(o, list):
                for i, v in enumerate(o[:300]):
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
            print(f"  keys: {list(data.keys())[:40]}")
        hits = find_keys(data, NEEDLES)
        if hits:
            print(f"  >>> 命中 {len(hits)} 处:")
            for n, p, v in hits[:25]:
                print(f"      [{n}] {p} = {v}")
        else:
            print("  >>> 未命中 vf/valueFactor")
        return data
    except Exception as e:
        print(f"  ERROR: {str(e)[:200]}")
        return None


async def mixin_call(brain, coro, label):
    print(f"\n### {label} (mixin)")
    try:
        data = await coro
        print(f"  type={type(data).__name__}")
        if isinstance(data, dict):
            print(f"  keys: {list(data.keys())[:40]}")
        hits = find_keys(data, NEEDLES)
        if hits:
            print(f"  >>> 命中 {len(hits)} 处:")
            for n, p, v in hits[:25]:
                print(f"      [{n}] {p} = {v}")
        else:
            print("  >>> 未命中 vf/valueFactor")
        return data
    except Exception as e:
        print(f"  ERROR: {str(e)[:200]}")
        return None


async def main():
    brain = BrainApiClient()
    await brain.ensure_authenticated()
    base = brain.base_url

    await raw(brain, f"{base}/users/self/activities/base-payment", "base-payment")
    await raw(brain, f"{base}/users/self/activities/other-payment", "other-payment")
    await raw(brain, f"{base}/users/self/research", "research(猜测)")
    await raw(brain, f"{base}/users/self/consultant", "consultant(猜测)")
    await raw(brain, f"{base}/users/self/payments", "payments(猜测)")
    await mixin_call(brain, brain.get_pyramid_multipliers(), "get_pyramid_multipliers")
    await mixin_call(brain, brain.get_pyramid_alphas(), "get_pyramid_alphas")
    await mixin_call(brain, brain.get_user_activities("self"), "get_user_activities")


if __name__ == "__main__":
    asyncio.run(main())
