#!/usr/bin/env python3
"""Quick debug: inspect a child sim's response to find alpha ID."""
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
    print("[AUTH] OK\n")

    # Get a child sim - take the first from opt_b2
    child_id = "38cPTlQU4qKbpSDmt9DRNV"  # b2 #3: sh=2.4
    resp = await bc._request('GET', f"{bc.base_url}/simulations/{child_id}")
    data = resp.json()
    print(f"Child sim response type: {type(data)}")
    print(f"Top keys: {list(data.keys())}")
    print(f"Status: {data.get('status','?')}")

    # Look for alpha field
    alpha_id = data.get("alpha", "")
    print(f"\nalpha field: '{alpha_id}'")

    # Check links
    links = data.get("_links", {})
    for k, v in links.items():
        print(f"  _links.{k}: {v}")

    # Check settings for alpha reference
    settings = data.get("settings", {})
    print(f"\nsettings keys: {list(settings.keys())}")

    # Try full response preview
    print(f"\nFull response (first 1000 chars):")
    print(json.dumps(data, indent=2, ensure_ascii=False)[:1000])

    # If we found an alpha, fetch it
    if alpha_id:
        print(f"\n--- Fetching alpha {alpha_id} ---")
        aresp = await bc._request('GET', f"{bc.base_url}/alphas/{alpha_id}")
        adata = aresp.json()
        print(f"Alpha response type: {type(adata)}")
        print(f"Alpha top keys: {list(adata.keys())}")
        checks = adata.get("checks", [])
        print(f"Checks: {len(checks)} items")
        for c in checks[:5]:
            print(f"  {c.get('name','?')}: {c.get('result','?')} = {c.get('value','?')}")
        is_data = adata.get("is", {})
        print(f"IS sharpe: {is_data.get('sharpe','?')}")
        print(f"IS fitness: {is_data.get('fitness','?')}")

if __name__ == "__main__":
    asyncio.run(main())
