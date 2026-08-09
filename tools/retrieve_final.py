#!/usr/bin/env python3
"""Final proper retrieval with PC check data."""
import sys, os, json, asyncio
from pathlib import Path
from datetime import datetime

MCP_DIR = Path(__file__).parent.parent / "world-quant-brain-mcp"
sys.path.insert(0, str(MCP_DIR))
os.chdir(str(MCP_DIR))

env_path = MCP_DIR / ".env"
for line in env_path.read_text().splitlines():
    line = line.strip()
    if not line or line.startswith('#') or '=' not in line: continue
    k, v = line.split('=', 1)
    os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))

TRACKING_DIR = Path(__file__).parent.parent / "wqb-share-03" / "tracking"

from main import BrainApiClient

MULTISIMS = {
    "opt_b1": ("1l2Sc85Ky5es9upJg8VHeoZ", [
        "forum_core_ts_decay", "forum_core_no_decay", "proven_country", "proven_cap_decile",
        "forum_w60", "raw_cap_decile", "proven_subindustry", "forum_ts_zscore_outer"
    ]),
    "opt_b2": ("2leJMb87U59LbOOHeoU4rbE", [
        "w40", "w30", "w50", "raw", "w40_ts_decay_linear5",
        "w60", "raw_ts_decay_linear5", "w40_signed_power"
    ]),
}

def extract_alpha_metrics(alpha_data):
    """Extract all metrics from alpha details including checks."""
    checks = alpha_data.get("checks", [])
    is_data = alpha_data.get("is", {})
    os_data = alpha_data.get("os") or {}

    failed = [c.get("name","") for c in checks if c.get("result")=="FAIL"]
    warn = [c.get("name","") for c in checks if c.get("result") in ("WARNING","WARN")]
    passed = [c.get("name","") for c in checks if c.get("result")=="PASS"]

    two_yr, asi_jpn, sub_u, rn_sh = None, None, None, None
    for c in checks:
        name = c.get("name","")
        val = c.get("value")
        if val is None: continue
        try: val_f = float(val)
        except: continue
        if "IS_LADDER" in name or "LADDER" in name:
            two_yr = val_f
        elif ("2Y" in name or "2_YEAR" in name) and two_yr is None:
            two_yr = val_f
        if "ASI_JPN" in name or "JAPAN" in name or ("JPN" in name and "ASI" in name):
            asi_jpn = val_f
        if "SUB_UNIVERSE" in name:
            sub_u = val_f
        if "ROBUST" in name and rn_sh is None:
            rn_sh = val_f

    return {
        "stage": alpha_data.get("stage","?"),
        "alpha_id": alpha_data.get("id",""),
        "sharpe": round(float(is_data.get("sharpe",0) or 0), 3),
        "fitness": round(float(is_data.get("fitness",0) or 0), 3),
        "turnover": round(float(is_data.get("turnover",0) or 0), 4),
        "margin_bp": round(float(is_data.get("margin",0) or 0)*10000, 2),
        "returns": round(float(is_data.get("returns",0) or 0), 4),
        "os_sharpe": round(float(os_data.get("sharpe",0) or 0), 3),
        "two_year": round(two_yr,3) if two_yr else None,
        "asi_jpn": round(asi_jpn,3) if asi_jpn else None,
        "subU": round(sub_u,3) if sub_u else None,
        "rn_sh": round(rn_sh,3) if rn_sh else None,
        "failed_checks": failed,
        "warn_checks": warn,
        "passed_checks": passed,
    }

async def main():
    bc = BrainApiClient()
    await bc.ensure_authenticated()
    print("[AUTH] OK\n")

    for batch_name, (sim_id, labels) in MULTISIMS.items():
        print(f"{'='*60}")
        print(f"  {batch_name}: {sim_id}")
        print(f"{'='*60}")

        resp = await bc._request('GET', f"{bc.base_url}/simulations/{sim_id}")
        data = resp.json()
        children = data.get("children", [])
        print(f"  {len(children)} children, status={data.get('status','?')}")

        results = []
        for i, child_id in enumerate(children):
            label = labels[i] if i < len(labels) else f"expr{i+1}"
            print(f"  [{i+1}] {child_id} -> ", end="", flush=True)

            # Get child sim → find alpha ID
            cresp = await bc._request('GET', f"{bc.base_url}/simulations/{child_id}")
            cdata = cresp.json()
            alpha_id = cdata.get("alpha", "")

            if not alpha_id:
                print("NO ALPHA")
                continue

            print(f"{alpha_id}...", end="", flush=True)

            # Fetch alpha details
            aresp = await bc._request('GET', f"{bc.base_url}/alphas/{alpha_id}")
            adata = aresp.json()
            m = extract_alpha_metrics(adata)
            m["expr_idx"] = i+1
            m["variant"] = label
            m["child_id"] = child_id
            results.append(m)

            checks_str = f"{len(m['passed_checks'])}P/{len(m['failed_checks'])}F" if m['passed_checks'] else "0 checks"
            print(f" stage={m['stage']} sh={m['sharpe']} fit={m['fitness']} 2Y={m['two_year']} asi_jpn={m['asi_jpn']} subU={m['subU']} rn_sh={m['rn_sh']} check={checks_str}")
            await asyncio.sleep(0.3)

        # Save
        out_file = TRACKING_DIR / f"result_{batch_name}.json"
        output = {"batch": batch_name, "multisim_id": sim_id,
                  "timestamp": datetime.now().isoformat(), "alphas": results}
        with open(out_file, "w", encoding="utf-8") as f:
            json.dump(output, f, indent=2, ensure_ascii=False)

        # Quick summary
        if results:
            best_sh = max(results, key=lambda r: r["sharpe"])
            print(f"\n  BEST: {best_sh['alpha_id']} ({best_sh['variant']}) sh={best_sh['sharpe']}")
            passing = [r for r in results
                       if r["sharpe"] > 1.58 and r.get("fitness",0) > 1.0
                       and 0.05 <= r.get("turnover",0) <= 0.30
                       and r.get("margin_bp",0) > 5
                       and len(r.get("failed_checks",[])) == 0]
            print(f"  PASS: {len(passing)}/{len(results)}")
            if passing:
                for p in passing:
                    print(f"    ✅ {p['alpha_id']} ({p['variant']})")

        print(f"  Saved: {out_file}\n")

    print("[DONE]")

if __name__ == "__main__":
    asyncio.run(main())
