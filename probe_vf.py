#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""探查本账号在 WQ BRAIN 平台的 'vf'（因子质量评分）取值位置。

策略：登录后分别拉取 /users/self（profile）、/users/self/statistics（猜测端点）、
以及一颗样本 alpha 的详情，全文检索 'vf'（不区分大小写），并打印顶层字段便于人工定位。
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


def find_keys(obj, needle, path=""):
    """递归查找含 needle（小写）的 key 或字符串值，返回命中路径列表。"""
    hits = []
    n = needle.lower()
    if isinstance(obj, dict):
        for k, v in obj.items():
            kk = str(k).lower()
            if n in kk:
                hits.append((path + "/" + str(k), v if not isinstance(v, (dict, list)) else f"<{type(v).__name__}>"))
            hits.extend(find_keys(v, needle, path + "/" + str(k)))
    elif isinstance(obj, list):
        for i, v in enumerate(obj[:200]):
            hits.extend(find_keys(v, needle, path + f"[{i}]"))
    else:
        s = str(obj)
        if n in s.lower():
            hits.append((path, (s[:80] + "…") if len(s) > 80 else s))
    return hits


async def probe(brain, method, url, label):
    print(f"\n### {label}: GET {url}")
    try:
        resp = await brain._request(method, url)
        if resp.status_code >= 400:
            print(f"  HTTP {resp.status_code} -> { (resp.text or '')[:200] }")
            return None
        data = resp.json()
        print(f"  HTTP {resp.status_code}, top-level type={type(data).__name__}")
        if isinstance(data, dict):
            print(f"  keys: {list(data.keys())[:40]}")
        hits = find_keys(data, "vf")
        if hits:
            print(f"  >>> vf 命中 {len(hits)} 处:")
            for p, v in hits[:20]:
                print(f"      {p} = {v}")
        else:
            print("  >>> 未找到 'vf' 字段")
        return data
    except Exception as e:
        print(f"  ERROR: {str(e)[:200]}")
        return None


async def main():
    brain = BrainApiClient()
    await brain.ensure_authenticated()

    await probe(brain, "GET", f"{brain.base_url}/users/self", "用户 profile")
    await probe(brain, "GET", f"{brain.base_url}/users/self/statistics", "用户 statistics(猜测)")
    # 样本 alpha：刚 ACTIVE 的 MEA SA
    await probe(brain, "GET", f"{brain.base_url}/alphas/3qlYKAaO", "样本 alpha 3qlYKAaO 详情")


if __name__ == "__main__":
    asyncio.run(main())
