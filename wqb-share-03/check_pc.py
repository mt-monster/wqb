#!/usr/bin/env python3
"""Check if PC checks are now available for the alpha candidates."""
import sys, os, json, asyncio, time
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

# Alpha IDs to check (best from each batch + all from opt_b2)
ALPHA_IDS = {
    "b1_best_2": "gJ9nPVlM",   # model30 sh=1.49
    "b1_best_1": "O0xlAK2b",   # model30 sh=1.22
    "b1_best_w60": "np8LvwXE", # model30 sh=1.32
    "b2_best_raw": "3BkUUgdox5k9cyAzneiTfTi",  # sh=2.74
    "b2_raw_decay": "4kHvCjftj4UE8KE1bKleaSww", # sh=2.55
    "b2_w50": "3qe80Y8O",       # sh=2.40
    "b2_w60": "3DF2oLrC55z9dS1bay2K6fS",       # sh=2.49
    "b2_w40_decay": "2xSzLOf1z4sP9N2E23MxbCb", # sh=2.03
}

async def main():
    bc = BrainApiClient()
    await bc.ensure_authenticated()
    print("[AUTH] OK\n")

    for label, alpha_id in ALPHA_IDS.items():
        resp = await bc._request('GET', f"{bc.base_url}/alphas/{alpha_id}")
        data = resp.json()

        checks = data.get("checks", [])
        is_data = data.get("is", {})
        stage = data.get("stage", "?")

        print(f"\n--- {label}: {alpha_id} (stage={stage}) ---")
        print(f"  IS: sh={is_data.get('sharpe','?')}, fit={is_data.get('fitness','?')}, tvr={is_data.get('turnover','?')}, margin={is_data.get('margin','?')}")
        print(f"  Checks: {len(checks)} items")

        if checks:
            for c in checks:
                name = c.get("name", "?")
                result = c.get("result", "?")
                value = c.get("value", "?")
                print(f"    {name}: {result} = {value}")
        else:
            print(f"  ⚠ No checks yet — PC stage may not have run")

        await asyncio.sleep(0.3)

if __name__ == "__main__":
    asyncio.run(main())
