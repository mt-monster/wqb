#!/usr/bin/env python3
"""Retrieve previous optimization results using the MCP server's own BrainApiClient."""
import sys, os, json, time, asyncio
from pathlib import Path
from datetime import datetime

# Point to MCP module
MCP_DIR = Path(__file__).parent.parent / "world-quant-brain-mcp"
sys.path.insert(0, str(MCP_DIR))
os.chdir(str(MCP_DIR))  # .env loading depends on cwd

TRACKING_DIR = Path(__file__).parent.parent / "wqb-share-03" / "tracking"

# Load .env
env_path = MCP_DIR / ".env"
if env_path.exists():
    for line in env_path.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith('#') or '=' not in line: continue
        k, v = line.split('=', 1)
        os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))

# Setup proxy env vars (MCP server handles this internally)
os.environ.setdefault("REQUESTS_CA_BUNDLE", "")
os.environ.setdefault("CURL_CA_BUNDLE", "")

from main import BrainApiClient

MULTISIMS = {
    "opt_b1": {"id": "1l2Sc85Ky5es9upJg8VHeoZ", "label": "model30_star_eps_asi_decay20"},
    "opt_b2": {"id": "2leJMb87U59LbOOHeoU4rbE", "label": "model110_mdl110_score_opt_decay4"},
}

async def extract_metrics_from_child(bc, child_id):
    """Get alpha details from a child simulation ID."""
    try:
        # Get child simulation
        resp = await bc._request('GET', f"{bc.base_url}/simulations/{child_id}")
        data = resp.json() if isinstance(resp, dict) else resp.json() if hasattr(resp, 'json') else resp

        if isinstance(data, str):
            data = json.loads(data)

        if isinstance(data, dict):
            # Look for alpha ID
            alpha_id = data.get("alpha", "")
            if not alpha_id:
                # Try to find from links
                links = data.get("_links", {}).get("alpha", {})
                alpha_id = links.get("href", "") if isinstance(links, dict) else ""
                if alpha_id:
                    alpha_id = alpha_id.rsplit("/", 1)[-1] if "/" in alpha_id else alpha_id

            if alpha_id:
                # Fetch alpha details
                alpha_data_resp = await bc._request('GET', f"{bc.base_url}/alphas/{alpha_id}")
                if alpha_data_resp and hasattr(alpha_data_resp, 'json'):
                    alpha_data = alpha_data_resp.json()
                    if alpha_data:
                        return extract_metrics(alpha_data)
    except Exception as e:
        print(f"    Error for child {child_id}: {e}")
    return None

def extract_metrics(details):
    if not details: return None
    is_data = details.get("is", {})
    checks = details.get("checks", [])

    failed = [c.get("name","") for c in checks if c.get("result")=="FAIL"]
    warn = [c.get("name","") for c in checks if c.get("result") in ("WARNING","WARN")]

    two_yr, asi_jpn, sub_u, rn_sh = None, None, None, None
    for c in checks:
        name = c.get("name","")
        val = c.get("value")
        if val is None: continue
        if "IS_LADDER" in name or "LONG_TERM" in name or "LADDER" in name:
            two_yr = float(val)
        elif "2Y" in name and two_yr is None:
            two_yr = float(val)
        if "ASI_JPN" in name or "JAPAN" in name or "JPN" in name:
            asi_jpn = float(val)
        if "SUB_UNIVERSE" in name or "subUniverse" in name:
            sub_u = float(val)
        if "ROBUST" in name:
            rn_sh = float(val)

    return {
        "alpha_id": details.get("id",""),
        "expr": details.get("regular",{}).get("code",""),
        "sharpe": round(float(is_data.get("sharpe",0) or 0), 3),
        "fitness": round(float(is_data.get("fitness",0) or 0), 3),
        "turnover": round(float(is_data.get("turnover",0) or 0), 4),
        "margin_bp": round(float(is_data.get("margin",0) or 0)*10000, 2),
        "returns": round(float(is_data.get("returns",0) or 0), 4),
        "two_year": round(two_yr, 3) if two_yr else None,
        "asi_jpn": round(asi_jpn, 3) if asi_jpn else None,
        "subU": round(sub_u, 3) if sub_u else None,
        "rn_sh": round(rn_sh, 3) if rn_sh else None,
        "failed_checks": failed,
        "warn_checks": warn,
    }

async def main():
    bc = BrainApiClient()

    # Authenticate
    await bc.ensure_authenticated()
    print("[AUTH] OK")

    for batch_name, info in MULTISIMS.items():
        print(f"\n{'='*50}")
        print(f"  {batch_name}: {info['label']}")
        print(f"  Multisim: {info['id']}")
        print(f"{'='*50}")

        # Get multisim
        try:
            resp = await bc._request('GET', f"{bc.base_url}/simulations/{info['id']}")
            multisim = resp.json() if hasattr(resp, 'json') else resp
        except Exception as e:
            print(f"  [ERR] {e}")
            continue

        children = multisim.get("children", {})
        if isinstance(children, dict):
            sims = children.get("simulations", [])
        else:
            sims = []

        print(f"  {len(sims)} child simulations")

        results = []
        for i, child_id in enumerate(sims):
            print(f"  [{i+1}/{len(sims)}] {child_id}...")
            m = await extract_metrics_from_child(bc, child_id)
            if m:
                results.append(m)
                failed_str = ",".join(m["failed_checks"]) if m["failed_checks"] else "none"
                print(f"    sh={m['sharpe']}, fit={m['fitness']}, 2Y={m['two_year']}, asi_jpn={m['asi_jpn']}, subU={m['subU']}, rn_sh={m['rn_sh']}, margin={m['margin_bp']}bp, tvr={m['turnover']}, failed=[{failed_str}]")
            await asyncio.sleep(0.5)

        # Save
        output = {
            "batch": batch_name,
            "label": info["label"],
            "multisim_id": info["id"],
            "timestamp": datetime.now().isoformat(),
            "alphas": results,
        }
        out_file = TRACKING_DIR / f"result_{batch_name}.json"
        with open(out_file, "w", encoding="utf-8") as f:
            json.dump(output, f, indent=2, ensure_ascii=False)
        print(f"  Saved to {out_file}")

        if results:
            best = max(results, key=lambda r: r.get("sharpe", 0))
            print(f"  BEST: {best['alpha_id']} sh={best['sharpe']}")
            passing = [r for r in results
                       if r.get("sharpe",0) > 1.58
                       and r.get("fitness",0) > 1.0
                       and 0.05 <= r.get("turnover",0) <= 0.30
                       and r.get("margin_bp",0) > 5
                       and len(r.get("failed_checks",[])) == 0]
            if passing:
                print(f"  ✅ {len(passing)} PASSING: {[p['alpha_id'] for p in passing]}")
            else:
                print(f"  ❌ No full pass")

    print("\n[DONE]")

if __name__ == "__main__":
    asyncio.run(main())
