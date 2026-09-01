#!/usr/bin/env python
# -*- coding: utf-8 -*-
import asyncio, json, sys
from pathlib import Path

WQ_ROOT = Path(r"D:\coding\traeCN_project\wqb")
sys.path.insert(0, str(WQ_ROOT / "world-quant-brain-mcp"))


async def main():
    from brain_api import BrainApiClient
    brain = BrainApiClient()
    await brain.ensure_authenticated()

    aid = "1Yw3d69R"
    for url in [f"{brain.base_url}/alphas/{aid}",
                f"{brain.base_url}/alphas/{aid}/recordsets"]:
        try:
            r = await brain._request("GET", url, params={"limit": 1})
            print("=" * 70)
            print("URL:", url, "status:", r.status_code)
            j = r.json()
            print("top keys:", list(j.keys()))
            print(json.dumps(j, ensure_ascii=False)[:1500])
        except Exception as e:
            print(f"ERR {url}: {type(e).__name__} {str(e)[:120]}")


if __name__ == "__main__":
    asyncio.run(main())
