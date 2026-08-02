#!/usr/bin/env python3
"""Fix: retrieve results from completed multisims and extract metrics."""
import sys, os, json, time, requests, base64
from pathlib import Path
from datetime import datetime

MCP_DIR = Path(__file__).parent.parent / "world-quant-brain-mcp"
TRACKING_DIR = Path(__file__).parent.parent / "wqb-share-03" / "tracking"

# Load creds
env_path = MCP_DIR / ".env"
for line in env_path.read_text().splitlines():
    line = line.strip()
    if not line or line.startswith('#') or '=' not in line: continue
    k, v = line.split('=', 1)
    os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))

BASE_URL = "https://api.worldquantbrain.com"
EMAIL = os.environ.get("CREDENTIALS_EMAIL", "")
PASSWORD = os.environ.get("CREDENTIALS_PASSWORD", "")

session = requests.Session()

# Auth
credentials = f"{EMAIL}:{PASSWORD}"
encoded = base64.b64encode(credentials.encode()).decode()
resp = session.post(f"{BASE_URL}/authentication", headers={"Authorization": f"Basic {encoded}"}, timeout=30)
print(f"[AUTH] {resp.status_code}")

# Completed multisims (from P68gSB output)
MULTISIMS = {
    "opt_b1": {"id": "1l2Sc85Ky5es9upJg8VHeoZ", "label": "model30_star_eps_asi_decay20"},
    "opt_b2": {"id": "2leJMb87U59LbOOHeoU4rbE", "label": "model110_mdl110_score_opt_decay4"},
}

def get_multisim_result(sim_id):
    """Get multisim and extract children alpha IDs."""
    resp = session.get(f"{BASE_URL}/simulations/{sim_id}", timeout=30)
    if resp.status_code != 200:
        print(f"[ERR] sim {sim_id}: HTTP {resp.status_code}")
        return None

    data = resp.json()
    if isinstance(data, list):
        # Multisim response: list of child sims
        print(f"[OK] sim {sim_id}: {len(data)} children (list)")
        alpha_ids = []
        for child in data:
            if isinstance(child, dict):
                cid = child.get("id", child.get("alpha", ""))
                # Try to extract alpha ID from child
                if "alpha" in child:
                    aid = child.get("alpha", "")
                    if aid: alpha_ids.append(aid)
                elif "regular" in child:
                    aid = child.get("regular", {}).get("alpha", "")
                    if aid: alpha_ids.append(aid)
        return alpha_ids
    elif isinstance(data, dict):
        status = data.get("status", "?")
        print(f"[OK] sim {sim_id}: status={status}")
        children = data.get("children", {})
        if isinstance(children, dict):
            sims = children.get("simulations", [])
        elif isinstance(children, list):
            sims = children
        else:
            sims = []
        alpha_ids = []
        for ch in sims:
            if isinstance(ch, str):
                alpha_ids.append(ch)
            elif isinstance(ch, dict):
                aid = ch.get("id", ch.get("alpha", ""))
                if aid: alpha_ids.append(aid)
        return alpha_ids
    return None

def get_alpha_details(alpha_id):
    """Fetch alpha details from API."""
    resp = session.get(f"{BASE_URL}/alphas/{alpha_id}", timeout=30)
    if resp.status_code == 200:
        return resp.json()
    return None

def extract_metrics(details):
    if not details: return None
    is_data = details.get("is", {})
    checks = details.get("checks", [])
    failed = [c.get("name","") for c in checks if c.get("result")=="FAIL"]
    warn = [c.get("name","") for c in checks if c.get("result") in ("WARNING","WARN")]

    # Find 2Y / IS_LADDER from checks
    two_yr = None
    for c in checks:
        name = c.get("name","")
        if "IS_LADDER" in name or "LONG_TERM" in name or "LADDER" in name:
            two_yr = c.get("value")
        elif "2Y" in name:
            two_yr = c.get("value")

    # Find ASI_JPN from checks
    asi_jpn = None
    for c in checks:
        if "ASI_JPN" in c.get("name","") or "JAPAN" in c.get("name","") or "JPN" in c.get("name",""):
            asi_jpn = c.get("value")

    sub_u = None
    for c in checks:
        if "SUB_UNIVERSE" in c.get("name","") or "subUniverse" in c.get("name",""):
            sub_u = c.get("value")

    rn_sh = None
    for c in checks:
        if "ROBUST" in c.get("name","") or "ROBUST_UNIVERSE" in c.get("name",""):
            rn_sh = c.get("value")

    # PPA checks
    ppa_checks = details.get("powerPerformance", details.get("ppa", {}))

    return {
        "alpha_id": details.get("id",""),
        "expr": details.get("regular",{}).get("code",""),
        "sharpe": round(is_data.get("sharpe",0) or 0, 3),
        "fitness": round(is_data.get("fitness",0) or 0, 3),
        "turnover": round(is_data.get("turnover",0) or 0, 4),
        "margin_bp": round((is_data.get("margin",0) or 0)*10000, 2),
        "returns": round(is_data.get("returns",0) or 0, 4),
        "longCount": is_data.get("longCount",0),
        "two_year": round(two_yr, 3) if two_yr else None,
        "asi_jpn": round(asi_jpn, 3) if asi_jpn else None,
        "subU": round(sub_u, 3) if sub_u else None,
        "rn_sh": round(rn_sh, 3) if rn_sh else None,
        "failed_checks": failed,
        "warn_checks": warn,
    }

for batch_name, info in MULTISIMS.items():
    print(f"\n{'='*50}")
    print(f"  {batch_name}: {info['label']}")
    print(f"  Multisim: {info['id']}")
    print(f"{'='*50}")

    alpha_ids = get_multisim_result(info["id"])
    if not alpha_ids:
        print("  [FAIL] Could not get alpha IDs")
        continue

    print(f"  Got {len(alpha_ids)} alpha IDs: {alpha_ids}")

    results = []
    for i, aid in enumerate(alpha_ids):
        print(f"  [{i+1}/{len(alpha_ids)}] Fetching {aid}...")
        details = get_alpha_details(aid)
        if details:
            m = extract_metrics(details)
            if m:
                results.append(m)
                failed_str = ",".join(m["failed_checks"]) if m["failed_checks"] else "none"
                print(f"    sh={m['sharpe']} fit={m['fitness']} 2Y={m['two_year']} asi_jpn={m['asi_jpn']} subU={m['subU']} rn_sh={m['rn_sh']} margin={m['margin_bp']}bp tvr={m['turnover']} failed=[{failed_str}]")
        time.sleep(0.5)

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

    # Summary
    if results:
        best = max(results, key=lambda r: r.get("sharpe", 0))
        passing = [r for r in results
                   if r.get("sharpe",0) > 1.58
                   and r.get("fitness",0) > 1.0
                   and 0.05 <= r.get("turnover",0) <= 0.30
                   and r.get("margin_bp",0) > 5
                   and len(r.get("failed_checks",[])) == 0]
        print(f"\n  BEST: {best['alpha_id']} sh={best['sharpe']}")
        if passing:
            print(f"  ✅ {len(passing)} PASSING: {[p['alpha_id'] for p in passing]}")
        else:
            print(f"  ❌ No full pass candidates (best sh={best['sharpe']})")
        for r in sorted(results, key=lambda r: r.get("sharpe",0), reverse=True)[:5]:
            print(f"  TOP5: {r['alpha_id']} sh={r['sharpe']} fit={r['fitness']} 2Y={r['two_year']} asi_jpn={r['asi_jpn']}")

    print(f"  Saved: {out_file}")

print("\n[DONE]")
