"""Pull the actual vwap FIELD distribution (not PnL) and generate histogram.

Strategy:
1. List available recordsets for the vwap raw-alpha.
2. Try common field-level recordsets (data, expression, raw, etc.).
3. If none exist, fall back: extract signal values from a raw simulation by
   creating a second alpha whose expression = field name itself, then use
   recordsets/data or the simulation output positions.
"""
import asyncio
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(PROJ, "world-quant-brain-mcp"))

OUT_DIR = os.path.join(PROJ, "results", "sa_20261023_vwap_hist")
os.makedirs(OUT_DIR, exist_ok=True)

ALPHA_ID = "zqr0wOEX"


async def main():
    from brain_api import BrainApiClient

    c = BrainApiClient()
    await c.ensure_authenticated()

    # 1. list all recordsets
    print("=== Available recordsets ===")
    try:
        rsets = await c.get_record_sets(ALPHA_ID)
        print(json.dumps(rsets, indent=2)[:3000])
        with open(os.path.join(OUT_DIR, f"{ALPHA_ID}_recordsets_list.json"), "w", encoding="utf-8") as f:
            json.dump(rsets, f, indent=2)
    except Exception as e:
        print(f"list err: {e}")
        return

    # 2. fetch each recordset, save
    if isinstance(rsets, dict):
        records = rsets.get("results") or rsets.get("records") or []
    elif isinstance(rsets, list):
        records = rsets
    else:
        records = []

    print(f"\n=== Fetching {len(records)} recordsets ===")
    for r in records:
        name = r.get("name") or r.get("recordSetKey") or r.get("id")
        if not name:
            continue
        print(f"\n--- recordset: {name} ---")
        print(json.dumps(r, indent=2)[:500])
        try:
            data = await c.get_record_set_data(ALPHA_ID, name)
            with open(os.path.join(OUT_DIR, f"{ALPHA_ID}_{name}.json"), "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, default=str)
            if isinstance(data, dict):
                rec = data.get("records") or []
                print(f"  records: {len(rec)}, sample: {rec[:1]}")
            else:
                print(f"  data type: {type(data).__name__}")
        except Exception as e:
            print(f"  fetch err: {e}")


if __name__ == "__main__":
    asyncio.run(main())
