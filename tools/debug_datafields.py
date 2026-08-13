#!/usr/bin/env python3
"""Debug: inspect raw datafields response structure."""
import sys, os, json, asyncio
from pathlib import Path

MCP_DIR = Path(__file__).parent.parent / "world-quant-brain-mcp"
sys.path.insert(0, str(MCP_DIR))
os.chdir(str(MCP_DIR))

env_path = MCP_DIR / ".env"
for line in env_path.read_text().splitlines():
    line = line.strip()
    if not line or line.startswith('#') or '=' not in line: continue
    k, v = line.split('=', 1)
    os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))

from brain_api import BrainApiClient

async def main():
    bc = BrainApiClient()
    await bc.ensure_authenticated()
    print("[AUTH] OK\n")

    for ds_id in ["model110", "model243", "other36"]:
        resp = await bc._request(
            'GET',
            f"{bc.base_url}/data-fields"
            f"?dataset.id={ds_id}"
            f"&region=ASI&universe=MINVOL1M&delay=1"
        )
        data = resp.json()
        print(f"\n=== {ds_id} ===")
        print(f"Type: {type(data).__name__}")
        if isinstance(data, dict):
            print(f"Keys: {list(data.keys())}")
            count = data.get("count", data.get("total", "?"))
            print(f"Count: {count}")
            results = data.get("results", [])
            print(f"Type of results: {type(results).__name__}, len={len(results)}")
            if results:
                print(f"First item type: {type(results[0]).__name__}")
                print(f"First item: {json.dumps(results[0], indent=2, ensure_ascii=False)[:500]}")
        elif isinstance(data, list):
            print(f"List len={len(data)}")
            if data:
                print(f"First item: {json.dumps(data[0], indent=2, ensure_ascii=False)[:500]}")

if __name__ == "__main__":
    asyncio.run(main())
