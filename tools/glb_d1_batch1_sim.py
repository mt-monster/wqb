#!/usr/bin/env python3
"""GLB D1 batch simulation via BrainApiClient (bypasses MCP create_multi_simulation bug)."""
import sys, os, json, asyncio, time
from pathlib import Path

MCP_DIR = Path(__file__).parent.parent / "world-quant-brain-mcp"
sys.path.insert(0, str(MCP_DIR))
os.chdir(str(MCP_DIR))

# Load .env
env_path = MCP_DIR / ".env"
if env_path.exists():
    for line in env_path.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith('#') or '=' not in line: continue
        k, v = line.split('=', 1)
        os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))

from main import brain_client as bc

TRACKING_DIR = Path(__file__).parent.parent / "wqb-share-03" / "tracking"
TRACKING_DIR.mkdir(parents=True, exist_ok=True)

# ── Round 1: news73 + news48 + fnd44 white-space datasets, COUNTRY neutralization ──
BATCH_1 = [
    ("nws73_neg_20", "ts_rank(nws73_globalsent_negativescore, 20)"),
    ("nws73_findown_60", "ts_rank(nws73_globalsent_findownscore, 60)"),
    ("nws73_certainty_20", "ts_rank(nws73_globalsent_certaintyscore, 20)"),
    ("nws48_nip_20", "ts_rank(nws48_nip, 20)"),
    ("nws48_ens_60", "ts_rank(nws48_ens, 60)"),
    ("nws48_relevance_20", "ts_rank(nws48_relevance, 20)"),
    ("nws48_gens_20", "ts_rank(nws48_g_ens, 20)"),
    ("nws73_neg_rankchg_20", "ts_delta(rank(nws73_globalsent_negativescore), 20)"),
    ("fnd44_mscore_20", "ts_rank(fnd44_mscore, 20)"),
    ("fnd44_yoon_60", "ts_rank(fnd44_yoon_wc_accruals, 60)"),
]

SETTINGS = {
    "region": "GLB",
    "delay": 1,
    "universe": "TOP3000",
    "decay": 4,
    "truncation": 0.08,
    "neutralization": "COUNTRY",
    "test_period": "P0Y0M",
    "language": "FASTEXPR",
    "unit_handling": "VERIFY",
    "nan_handling": "OFF",
}

async def main():
    await bc.ensure_authenticated()
    print("[AUTH] OK\n")

    batch_num = 1
    results = []
    out_file = TRACKING_DIR / f"glb_d1_batch{batch_num:02d}.json"

    for idx, (label, expr) in enumerate(BATCH_1, 1):
        print(f"[{idx:2d}] {label}: {expr}", flush=True)
        last_err = None
        for attempt in range(4):
            try:
                payload = {
                    "type": "REGULAR",
                    "settings": {
                        "instrumentType": "EQUITY",
                        "region": "GLB",
                        "universe": "TOP3000",
                        "delay": 1,
                        "decay": 4.0,
                        "truncation": 0.08,
                        "neutralization": "COUNTRY",
                        "pasteurization": "ON",
                        "unitHandling": "VERIFY",
                        "nanHandling": "OFF",
                        "language": "FASTEXPR",
                        "testPeriod": "P0Y0M",
                        "visualization": False,
                    },
                    "regular": expr
                }
                resp = await bc._request("POST", f"{bc.base_url}/simulations", json=payload)
                data = resp.json()
                sim_id = data.get("id", "") or data.get("location", "")
                alpha_id = data.get("alpha", "") or data.get("alphaId", "")
                print(f"     → attempt={attempt} sim_id={sim_id} alpha={alpha_id} status={resp.status_code}", flush=True)
                results.append({
                    "label": label, "expression": expr,
                    "sim_id": sim_id, "alpha_id": alpha_id,
                    "status": "SUBMITTED", "error": None
                })
                break
            except Exception as e:
                last_err = str(e)
                print(f"     → attempt={attempt} ERROR: {e}", flush=True)
                await asyncio.sleep(10 + attempt * 20)
        else:
            results.append({
                "label": label, "expression": expr,
                "sim_id": None, "alpha_id": None,
                "status": "ERROR", "error": last_err
            })
        await asyncio.sleep(15)  # Rate limit safety

    output = {
        "batch": batch_num, "region": "GLB", "delay": 1,
        "universe": "TOP3000", "neutralization": "COUNTRY",
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "results": results
    }
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    print(f"\n[SAVED] {out_file}")

    # Print summary
    submitted = [r for r in results if r["status"] == "SUBMITTED"]
    errors = [r for r in results if r["status"] == "ERROR"]
    print(f"[SUMMARY] Submitted: {len(submitted)}, Errors: {len(errors)}")
    if submitted:
        sim_ids = [r["sim_id"] for r in submitted]
        print(f"[POLL] Simulation IDs: {sim_ids}")

if __name__ == "__main__":
    asyncio.run(main())