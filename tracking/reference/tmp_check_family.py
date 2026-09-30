# -*- coding: utf-8 -*-
"""检查 IND ds=1358 族内候选的全部 FAIL/WARNING checks。"""
import sys, os, asyncio
REPO = r"D:\coding\traeCN_project\wqb"
sys.path.insert(0, os.path.join(REPO, "world-quant-brain-mcp"))
from brain_api import brain_client

IDS = ["O0NwW6oR", "P02ro8Op", "9qjPxmre", "WjbwO0Gk", "A1NJVm3e",
       "vRrnAY5r", "d5b8Wodj", "WjbwlYXo", "xA3wvlnJ", "d5b8a90w"]


async def go():
    await brain_client.ensure_authenticated()
    for aid in IDS:
        r = await brain_client._request("GET", f"https://api.worldquantbrain.com/alphas/{aid}")
        if r.status_code != 200:
            print(f"{aid}: HTTP {r.status_code}")
            continue
        d = r.json()
        isd = d.get("is") or {}
        bad = []
        for c in isd.get("checks", []):
            if c.get("result") in ("FAIL", "WARNING"):
                bad.append(f"{c.get('name')}={c.get('result')}({c.get('value')}/{c.get('limit')})")
        to = None
        for c in isd.get("checks", []):
            if c.get("name") == "LOW_TURNOVER":
                to = c.get("value")
        tag = " | ".join(bad) if bad else "ALL PASS"
        print(f"{aid}  TO={to}  ->  {tag}")


asyncio.run(go())
