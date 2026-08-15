import json, sys, os, time, sys
import os
sys.path.insert(0, os.environ.get("WQ_ACE_LIB", r"C:/Users/MENGTAO/.workbuddy/skills/brain-simAlphasinBatch-and-track/scripts"))
import ace_lib

# ---- auth ----
cfg = json.load(open(r'C:/Users/MENGTAO/.workbuddy/skills/brain-simAlphasinBatch-and-track/configs/config.json'))
for k, v in cfg.items():
    os.environ[str(k).upper()] = str(v)
    os.environ[str(k)] = str(v)

SESSION = ace_lib.start_session()
API = ace_lib.brain_api_url

# ---- T_B template (exact from 6JMmdrG, ra_failed:false, sharpe 1.64) ----
TPL = "piece_1 = group_mean(ts_std_dev({F},20),1, subindustry) - ts_std_dev({F},20);ts_mean(piece_1,60);"
SETTINGS = {
    "instrumentType": "EQUITY", "region": "USA", "universe": "TOP3000", "delay": 1,
    "decay": 5, "neutralization": "MARKET", "truncation": 0.08, "pasteurization": "ON",
    "unitHandling": "VERIFY", "nanHandling": "ON", "maxTrade": "OFF", "maxPosition": "OFF",
    "language": "FASTEXPR", "visualization": False,
    "startDate": "2018-01-20", "endDate": "2023-01-20",
}

# Probe earnings surprise score variants (unknown whether _2.._5 / higher exist; _1,_6 unknown, _7 & no-suffix known)
CANDIDATES = [
    "historic_earnings_surprise_score_2",
    "historic_earnings_surprise_score_3",
    "historic_earnings_surprise_score_4",
    "historic_earnings_surprise_score_5",
    "historic_earnings_surprise_score_8",
    "historic_earnings_surprise_score_9",
    "historic_earnings_surprise_score_10",
    "historic_earnings_surprise_score_0",
]

alphas = []
for f in CANDIDATES:
    alphas.append({"type": "REGULAR", "regular": TPL.format(F=f), "settings": dict(SETTINGS)})

print(f"Submitting {len(alphas)} candidate sims...", flush=True)
resp = SESSION.post(API + "/simulations", json=alphas)
print("submit status:", resp.status_code, flush=True)
if resp.status_code // 100 != 2:
    print("SUBMIT FAILED:", resp.text[:500]); sys.exit(1)

loc = resp.headers.get("Location")
print("parent loc:", loc, flush=True)
# poll parent until children spawn
children = []
for _ in range(40):
    pdata = SESSION.get(loc).json()
    children = pdata.get("children") or pdata.get("child_ids") or []
    pst = pdata.get("status")
    if children or pst in ("ERROR", "FAIL", "FAILED", "CANCELLED", "COMPLETED", "COMPLETE"):
        break
    time.sleep(5)
print("parent status:", pdata.get("status"), "children:", len(children), flush=True)
if not children:
    print("NO CHILDREN. parent dump:", json.dumps(pdata)[:600]); sys.exit(1)

PER_CHILD_TIMEOUT = 540
results = {}
for cid in children:
    t0 = time.time()
    while time.time() - t0 < PER_CHILD_TIMEOUT:
        try:
            r = SESSION.get(f"{API}/simulations/{cid}")
            if r.status_code == 200:
                d = r.json()
                st = d.get("status")
                if st in ("COMPLETED", "COMPLETE"):
                    aid = d.get("alpha")
                    if aid:
                        det = ace_lib.get_simulation_result_json(SESSION, aid)
                        m = det.get("metrics", {})
                        ra = det.get("ra", {})
                        results[cid] = {
                            "status": "COMPLETED", "alpha_id": aid,
                            "sharpe": m.get("sharpe"), "fitness": m.get("fitness"),
                            "two_year_sharpe": m.get("two_year_sharpe"),
                            "ra_failed": ra.get("ra_failed"), "ppa_failed": ra.get("ppa_failed"),
                        }
                    else:
                        results[cid] = {"status": "COMPLETED_NO_ALPHA"}
                    break
                elif st in ("ERROR", "FAIL", "FAILED"):
                    err = ""
                    try:
                        err = d.get("errors") or d.get("error") or d.get("message") or ""
                        if isinstance(err, list): err = json.dumps(err)
                    except Exception: pass
                    results[cid] = {"status": "ERROR", "error": str(err)[:160]}
                    break
                elif st == "CANCELLED":
                    results[cid] = {"status": "CANCELLED"}
                    break
        except Exception as e:
            print(f"  poll {cid} exc: {e}", flush=True)
        time.sleep(5)
    else:
        results[cid] = {"status": "TIMEOUT"}

# map child -> candidate field
print("\n===== RESULTS =====", flush=True)
for i, cid in enumerate(children):
    f = CANDIDATES[i] if i < len(CANDIDATES) else "?"
    r = results.get(cid, {})
    if r.get("status") == "COMPLETED":
        print(f"[OK] {f:45s} id={r['alpha_id']} s={r['sharpe']} f={r['fitness']} 2y={r['two_year_sharpe']} ra_failed={r['ra_failed']}")
    elif r.get("status") == "ERROR":
        print(f"[ERR] {f:45s} {r['error']}")
    else:
        print(f"[{r.get('status')}] {f:45s}")
print("===== DONE =====", flush=True)
