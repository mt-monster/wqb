# -*- coding: utf-8 -*-
"""全量 OS REGULAR alpha 盘点：分页拉全 → 按区域/状态/提交月份聚合。

用途：流水线「已交付」段的事实基线，避免只看最近 100 条得出偏差结论。
"""
import asyncio
import collections
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _pyenv  # noqa: E402

MCP_DIR = str(_pyenv.mcp_dir())
sys.path.insert(0, MCP_DIR)
os.chdir(MCP_DIR)

from brain_api import BrainApiClient  # noqa: E402


async def main():
    c = BrainApiClient()
    await c.ensure_authenticated()
    rows, offset = [], 0
    while offset <= 400:
        r = c.session.get(f"{c.base_url}/users/self/alphas",
                          params={"stage": "OS", "type": "REGULAR",
                                  "limit": 100, "offset": offset})
        if r.status_code != 200:
            print("ERR", offset, r.status_code, r.text[:200])
            break
        j = r.json()
        got = j.get("results", [])
        rows.extend(got)
        if len(got) < 100:
            break
        offset += 100

    out = []
    for a in rows:
        s = a.get("settings", {}) or {}
        out.append({
            "id": a.get("id"),
            "region": s.get("region"),
            "status": a.get("status"),
            "universe": s.get("universe"),
            "delay": s.get("delay"),
            "neutralization": s.get("neutralization"),
            "dateSubmitted": a.get("dateSubmitted"),
            "sharpe": (a.get("is") or {}).get("sharpe"),
            "fitness": (a.get("is") or {}).get("fitness"),
            "turnover": (a.get("is") or {}).get("turnover"),
            "code": (a.get("regular") or {}).get("code"),
        })
    json.dump(out, open(os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "..",
        "tracking", "EUR", "runs", "os_inventory.json"), "w"), indent=1)

    print("TOTAL OS REGULAR:", len(out))
    print("\n--- region x status ---")
    for k, v in sorted(collections.Counter((r["region"], r["status"]) for r in out).items(),
                       key=lambda x: -x[1]):
        print(k, v)

    print("\n--- ACTIVE by region ---")
    act = collections.Counter(r["region"] for r in out if r["status"] == "ACTIVE")
    for k, v in sorted(act.items(), key=lambda x: -x[1]):
        print(k, v)
    print("ACTIVE total:", sum(act.values()))

    print("\n--- ACTIVE by submit month ---")
    for k, v in sorted(collections.Counter(
            (r["dateSubmitted"] or "")[:7] for r in out if r["status"] == "ACTIVE").items()):
        print(k, v)


asyncio.run(main())
