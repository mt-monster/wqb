"""Fetch PnL for alpha zqr0wOEX (vwap raw) and generate histogram."""
import asyncio
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.dirname(HERE)
MCP = os.path.join(PROJ, "world-quant-brain-mcp")
sys.path.insert(0, MCP)

OUT_DIR = os.path.join(PROJ, "results", "sa_20261023_vwap_hist")
os.makedirs(OUT_DIR, exist_ok=True)

ALPHA_ID = "zqr0wOEX"


async def main():
    from brain_api import BrainApiClient

    c = BrainApiClient()
    await c.ensure_authenticated()

    # Try get_alpha_pnl first
    try:
        pnl = await c.get_alpha_pnl(ALPHA_ID)
        print("get_alpha_pnl OK")
    except Exception as e:
        print(f"get_alpha_pnl err: {e}")
        # fallback: REST /alphas/{id}/pnl
        d, err = await c._get_json(f"{c.base_url}/alphas/{ALPHA_ID}/pnl")
        if err:
            print(f"REST err: {err}")
            return
        pnl = d

    out = os.path.join(OUT_DIR, f"{ALPHA_ID}_pnl.json")
    with open(out, "w", encoding="utf-8") as f:
        json.dump(pnl, f, indent=2)
    print(f"Wrote {out}")
    if isinstance(pnl, dict):
        print("keys:", list(pnl.keys())[:20])
        for k, v in pnl.items():
            if isinstance(v, list):
                print(f"  {k}: list len={len(v)}, sample={v[:1]}")
    elif isinstance(pnl, list):
        print(f"list len={len(pnl)}, sample={pnl[:1]}")


if __name__ == "__main__":
    asyncio.run(main())
