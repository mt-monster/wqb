# -*- coding: utf-8 -*-
"""定位 leM88RN5 的 self-correlation 冲突对象（top 记录）。"""
import asyncio
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "src"))
sys.path.insert(0, "/d/coding/traeCN_project/wqb/world-quant-brain-mcp")

from wqb.workflow._common import get_brain_client

TARGET = "leM88RN5"


async def main():
    client = get_brain_client()
    res = await client.get_self_correlation(TARGET, correlation_type="self")
    print(f"[SC] max={res.get('max')} pool_size={res.get('pool_size')} "
          f"local={res.get('local_calculation')}")
    recs = res.get("records", [])
    print(f"[SC] top {len(recs)} conflicting alphas:")
    for r in recs:
        print(f"  {r['id']}: {r['correlation']:.4f}")


if __name__ == "__main__":
    asyncio.run(main())
