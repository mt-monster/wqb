#!/usr/bin/env python3
"""Final: retrieve optimization results."""
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
    "opt_b1": {"id": "1l2Sc85Ky5es9upJg8VHeoZ", "label": "model30_star_eps_asi_decay20"},
    "opt_b2": {"id": "2leJMb87U59LbOOHeoU4rbE", "label": "model110_mdl110_score_opt_decay4"},
}

EXPRESSIONS_B1 = [
    "group_rank(ts_rank(ts_decay_linear(ts_backfill(winsorize(star_eps_surprise_prediction_fy1, std=5), 60), 5), 30), group_cartesian_product(country, bucket(rank(cap), range='0, 1, 0.1')))",
    "group_rank(ts_rank(ts_backfill(winsorize(star_eps_surprise_prediction_fy1, std=5), 60), 30), group_cartesian_product(country, bucket(rank(cap), range='0, 1, 0.1')))",
    "ts_zscore(group_rank(ts_mean(star_eps_surprise_prediction_fy1, 20), country), 40)",
    "ts_zscore(group_rank(ts_mean(star_eps_surprise_prediction_fy1, 20), group_cartesian_product(country, bucket(rank(cap), range='0, 1, 0.1'))), 40)",
    "group_rank(ts_rank(ts_backfill(winsorize(star_eps_surprise_prediction_fy1, std=5), 60), 60), group_cartesian_product(country, bucket(rank(cap), range='0, 1, 0.1')))",
    "group_rank(ts_backfill(winsorize(star_eps_surprise_prediction_fy1, std=5), 60), group_cartesian_product(country, bucket(rank(cap), range='0, 1, 0.1')))",
    "ts_zscore(group_rank(ts_mean(star_eps_surprise_prediction_fy1, 20), subindustry), 40)",
    "ts_zscore(group_rank(ts_rank(ts_backfill(winsorize(star_eps_surprise_prediction_fy1, std=5), 60), 30), country), 40)",
]
EXPRESSIONS_B2 = [
    "group_rank(ts_rank(ts_backfill(winsorize(mdl110_score,std=5),60),40),group_cartesian_product(country,bucket(rank(cap),range='0,1,0.1')))",
    "group_rank(ts_rank(ts_backfill(winsorize(mdl110_score,std=5),60),30),group_cartesian_product(country,bucket(rank(cap),range='0,1,0.1')))",
    "group_rank(ts_rank(ts_backfill(winsorize(mdl110_score,std=5),60),50),group_cartesian_product(country,bucket(rank(cap),range='0,1,0.1')))",
    "group_rank(ts_backfill(winsorize(mdl110_score,std=5),60),group_cartesian_product(country,bucket(rank(cap),range='0,1,0.1')))",
    "group_rank(ts_rank(ts_decay_linear(ts_backfill(winsorize(mdl110_score,std=5),60),5),40),group_cartesian_product(country,bucket(rank(cap),range='0,1,0.1')))",
    "group_rank(ts_rank(ts_backfill(winsorize(mdl110_score,std=5),60),60),group_cartesian_product(country,bucket(rank(cap),range='0,1,0.1')))",
    "group_rank(ts_decay_linear(ts_backfill(winsorize(mdl110_score,std=5),60),5),group_cartesian_product(country,bucket(rank(cap),range='0,1,0.1')))",
    "group_rank(signed_power(subtract(ts_rank(ts_backfill(winsorize(mdl110_score,std=5),60),40),0.5),5),group_cartesian_product(country,bucket(rank(cap),range='0,1,0.1')))",
]

def extract_metrics(details, expr_idx):
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
        try: val_f = float(val)
        except: continue
        if "IS_LADDER" in name or "LONG_TERM" in name:
            two_yr = val_f
        elif "2Y" in name and two_yr is None:
            two_yr = val_f
        if "ASI_JPN" in name or "JAPAN" in name:
            asi_jpn = val_f
        if "SUB_UNIVERSE" in name:
            sub_u = val_f
        if "ROBUST_UNIVERSE" in name and rn_sh is None:
            rn_sh = val_f

    is_sh = float(is_data.get("sharpe",0) or 0)
    is_fit = float(is_data.get("fitness",0) or 0)
    is_tvr = float(is_data.get("turnover",0) or 0)
    is_margin = float(is_data.get("margin",0) or 0)

    return {
        "expr_idx": expr_idx,
        "alpha_id": details.get("id",""),
        "expr": details.get("regular",{}).get("code","") or details.get("expression",""),
        "sharpe": round(is_sh, 3),
        "fitness": round(is_fit, 3),
        "turnover": round(is_tvr, 4),
        "margin_bp": round(is_margin*10000, 2),
        "returns": round(float(is_data.get("returns",0) or 0), 4),
        "two_year": round(two_yr,3) if two_yr else None,
        "asi_jpn": round(asi_jpn,3) if asi_jpn else None,
        "subU": round(sub_u,3) if sub_u else None,
        "rn_sh": round(rn_sh,3) if rn_sh else None,
        "failed_checks": failed,
        "warn_checks": warn,
    }

async def get_child_alpha_id(bc, child_id):
    """Get the actual alpha ID from a child simulation ID."""
    resp = await bc._request('GET', f"{bc.base_url}/simulations/{child_id}")
    data = resp.json() if hasattr(resp, 'json') else resp
    if isinstance(data, dict):
        alpha_id = data.get("alpha", "")
        if not alpha_id:
            links = data.get("_links", {})
            for key in links:
                href = links[key].get("href","") if isinstance(links[key], dict) else str(links[key])
                if "/alphas/" in href:
                    alpha_id = href.rsplit("/",1)[-1]
                    break
        return alpha_id or child_id  # fallback
    return child_id

async def main():
    bc = BrainApiClient()
    await bc.ensure_authenticated()
    print("[AUTH] OK")

    all_batches = {
        "opt_b1": (MULTISIMS["opt_b1"], EXPRESSIONS_B1),
        "opt_b2": (MULTISIMS["opt_b2"], EXPRESSIONS_B2),
    }

    for batch_name, (info, expressions) in all_batches.items():
        print(f"\n{'='*60}")
        print(f"  {batch_name}: {info['label']}")
        print(f"{'='*60}")

        resp = await bc._request('GET', f"{bc.base_url}/simulations/{info['id']}")
        data = resp.json() if hasattr(resp, 'json') else resp
        status = data.get("status", "?")
        children = data.get("children", [])
        print(f"  Status: {status}, {len(children)} child sims")

        results = []
        for i, child_id in enumerate(children):
            expr_label = f"expr{i+1}"
            print(f"  [{i+1}/{len(children)}] {child_id}...")

            # Get the alpha ID from child sim
            alpha_id = await get_child_alpha_id(bc, child_id)
            if not alpha_id or alpha_id == child_id:
                # Try directly accessing alpha
                alpha_id = child_id

            # Fetch alpha details
            aresp = await bc._request('GET', f"{bc.base_url}/alphas/{alpha_id}")
            if aresp.status_code == 200:
                adata = aresp.json() if hasattr(aresp, 'json') else aresp
                m = extract_metrics(adata, i+1)
                if m and m["sharpe"] != 0:
                    m["expr"] = expressions[i] if i < len(expressions) else ""
                    results.append(m)
                    failed_str = ",".join(m["failed_checks"][:3]) if m["failed_checks"] else "none"
                    print(f"    sh={m['sharpe']}, fit={m['fitness']}, 2Y={m['two_year']}, asi_jpn={m['asi_jpn']}, subU={m['subU']}, rn_sh={m['rn_sh']}, margin={m['margin_bp']}bp, tvr={m['turnover']}, failed=[{failed_str}]")
                else:
                    print(f"    No metrics (m={m})")
            else:
                print(f"    Alpha HTTP {aresp.status_code}")
            await asyncio.sleep(0.3)

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

        if results:
            best = max(results, key=lambda r: r.get("sharpe", 0))
            print(f"\n  BEST: {best['alpha_id']} sh={best['sharpe']} fit={best['fitness']} 2Y={best['two_year']} asi_jpn={best['asi_jpn']}")
            passing = [r for r in results
                       if r.get("sharpe",0) > 1.58
                       and r.get("fitness",0) > 1.0
                       and 0.05 <= r.get("turnover",0) <= 0.30
                       and r.get("margin_bp",0) > 5
                       and len(r.get("failed_checks",[])) == 0]
            if passing:
                print(f"  ✅ {len(passing)} FULLY PASSING!")
            near = [r for r in results
                    if r.get("sharpe",0) > 1.58
                    and len(r.get("failed_checks",[])) <= 2]
            if near:
                print(f"  🟡 {len(near)} near-miss (sh>1.58, ≤2 failures)")

    print("\n[DONE]")

if __name__ == "__main__":
    asyncio.run(main())
