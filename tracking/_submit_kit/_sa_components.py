# -*- coding: utf-8 -*-
"""读取 SUPER alpha 的实际组件列表（record sets）。

用法: python _sa_components.py <super_alpha_id>
"""
import asyncio
import json
import sys
from pathlib import Path

WQ_ROOT = Path(r"D:\coding\traeCN_project\wqb")
sys.path.insert(0, str(WQ_ROOT / "world-quant-brain-mcp"))


async def main(aid):
    from brain_api import BrainApiClient
    brain = BrainApiClient()
    await brain.ensure_authenticated()

    print(f"=== SA {aid} record sets ===")
    rs = await brain.get_record_sets(aid)
    print(json.dumps(rs, ensure_ascii=False)[:1500])

    sets = (rs or {}).get("results") or rs.get("recordSets") or []
    if isinstance(rs, dict) and isinstance(rs.get("results"), list):
        sets = rs["results"]
    names = []
    for s in sets if isinstance(sets, list) else []:
        n = s.get("name") or s.get("id")
        if n:
            names.append(n)
    print(f"\nrecord set names: {names}")

    for n in names:
        try:
            data = await brain.get_record_set_data(aid, n)
            items = data if isinstance(data, list) else (data.get("records") or data.get("results") or [])
            print(f"\n--- {n}: {len(items)} records ---")
            for it in items[:40]:
                print("   ", json.dumps(it, ensure_ascii=False)[:220])
        except Exception as e:
            print(f"  [{n}] ERROR {e}")


if __name__ == "__main__":
    asyncio.run(main(sys.argv[1]))
