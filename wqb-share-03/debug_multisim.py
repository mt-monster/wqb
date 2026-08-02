#!/usr/bin/env python3
"""Debug: inspect raw multisim response structure."""
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

from main import BrainApiClient

async def main():
    bc = BrainApiClient()
    await bc.ensure_authenticated()
    print("[AUTH] OK")

    for sim_id in ["1l2Sc85Ky5es9upJg8VHeoZ", "2leJMb87U59LbOOHeoU4rbE"]:
        resp = await bc._request('GET', f"{bc.base_url}/simulations/{sim_id}")
        data = resp.json() if hasattr(resp, 'json') else resp
        print(f"\n=== {sim_id} ===")
        print(f"Type: {type(data)}")
        if isinstance(data, dict):
            print(f"Status: {data.get('status','?')}")
            # Print full keys
            print(f"Top keys: {list(data.keys())}")
            # Check children
            children = data.get("children", "N/A")
            if isinstance(children, dict):
                print(f"Children type: {type(children)}")
                for k, v in children.items():
                    if isinstance(v, list):
                        print(f"  children.{k}: list of {len(v)} items")
                        if v:
                            print(f"    first: {json.dumps(v[0], ensure_ascii=False)[:200]}")
                    elif isinstance(v, dict):
                        print(f"  children.{k}: dict with keys {list(v.keys())[:5]}")
                    else:
                        print(f"  children.{k}: {type(v).__name__} = {str(v)[:100]}")
            else:
                print(f"Children: {type(children).__name__} = {str(children)[:200]}")
            # Check other fields
            for field in ["simulations", "alphaIds", "results", "alpha_ids", "items", "entries"]:
                val = data.get(field)
                if val is not None:
                    print(f"'{field}': {type(val).__name__} = {str(val)[:200]}")

if __name__ == "__main__":
    asyncio.run(main())
