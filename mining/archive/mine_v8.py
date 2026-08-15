import json, sys, os, time
import os
sys.path.insert(0, os.environ.get("WQ_ACE_LIB", r"C:/Users/MENGTAO/.workbuddy/skills/brain-simAlphasinBatch-and-track/scripts"))
import ace_lib

cfg = json.load(open(r'C:/Users/MENGTAO/.workbuddy/skills/brain-simAlphasinBatch-and-track/configs/config.json'))
for k, v in cfg.items():
    os.environ[str(k).upper()] = str(v); os.environ[str(k)] = str(v)
SESSION = ace_lib.start_session()
API = ace_lib.brain_api_url

# T_B template (from 6JMmdrG, ra_failed:false, sharpe 1.64) -- proven for mdl177 time-series fields
TPL = "piece_1 = group_mean(ts_std_dev({F},20),1, subindustry) - ts_std_dev({F},20);ts_mean(piece_1,60);"
SETTINGS = {
    "instrumentType": "EQUITY", "region": "USA", "universe": "TOP3000", "delay": 1,
    "decay": 5, "neutralization": "MARKET", "truncation": 0.08, "pasteurization": "ON",
    "unitHandling": "VERIFY", "nanHandling": "ON", "maxTrade": "OFF", "maxPosition": "OFF",
    "language": "FASTEXPR", "visualization": False,
    "startDate": "2018-01-20", "endDate": "2023-01-20",
}

# 8 new mdl177 fields across value/growth/quality/earnings families (NOT in book)
FIELDS = [
    "mdl177_2_5yearrelativevaluefactor_rel5ycfp",
    "mdl177_2_deepvaluefactor_acqmul",
    "mdl177_2_earningmomentumfactor400_lagegp",
    "mdl177_2_earningsqualityfactor_chgsgasale",
    "mdl177_2_garpanalystmodel_qgp_relpegy",
    "mdl177_2_deepvaluefactor_curep",
    "mdl177_2_earningsqualityfactor_uar",
    "mdl177_2_5yearrelativevaluefactor_rel5yep",
]

alphas = []
for f in FIELDS:
    alphas.append({"type": "REGULAR", "regular": TPL.format(F=f), "settings": dict(SETTINGS)})

print(f"Submitting {len(alphas)} mdl177 T_B sims...", flush=True)
resp = SESSION.post(API + "/simulations", json=alphas)
print("submit status:", resp.status_code, flush=True)
if resp.status_code // 100 != 2:
    print("FAIL:", resp.text[:400]); sys.exit(1)

loc = resp.headers.get("Location")
children = []
for _ in range(40):
    pdata = SESSION.get(loc).json()
    children = pdata.get("children") or pdata.get("child_ids") or []
    if children or pdata.get("status") in ("ERROR","FAIL","FAILED","CANCELLED"):
        break
    time.sleep(5)
print("children:", len(children), flush=True)
if not children:
    print("NO CHILDREN:", json.dumps(pdata)[:400]); sys.exit(1)

PER = 600
results = {}
for cid in children:
    t0 = time.time(); done = False
    while time.time() - t0 < PER:
        try:
            r = SESSION.get(f"{API}/simulations/{cid}")
            if r.status_code == 200:
                d = r.json(); st = d.get("status")
                if st in ("COMPLETED","COMPLETE"):
                    aid = d.get("alpha")
                    if aid:
                        det = ace_lib.get_simulation_result_json(SESSION, aid)
                        m = det.get("metrics", {}); ra = det.get("ra", {})
                        checks = det.get("checks", {})
                        cval = None
                        for c in checks.get("warning", []) + checks.get("fail", []):
                            if "CLUSTER" in c.get("name",""): cval = c.get("value")
                        results[cid] = {"status":"COMPLETED","alpha_id":aid,
                            "sharpe":m.get("sharpe"),"fitness":m.get("fitness"),
                            "two_year_sharpe":m.get("two_year_sharpe"),
                            "ra_failed":ra.get("ra_failed"),"ppa_failed":ra.get("ppa_failed"),
                            "cluster_value":cval}
                    else:
                        results[cid] = {"status":"COMPLETED_NO_ALPHA"}
                    done = True; break
                elif st in ("ERROR","FAIL","FAILED"):
                    err = str(d.get("errors") or d.get("error") or d.get("message") or "")[:160]
                    results[cid] = {"status":"ERROR","error":err}; done = True; break
                elif st == "CANCELLED":
                    results[cid] = {"status":"CANCELLED"}; done = True; break
        except Exception as e:
            print("poll exc", e, flush=True)
        time.sleep(5)
    if not done:
        results[cid] = {"status":"TIMEOUT"}

print("\n===== RESULTS =====", flush=True)
for i, cid in enumerate(children):
    f = FIELDS[i] if i < len(FIELDS) else "?"
    r = results.get(cid, {})
    if r.get("status") == "COMPLETED":
        flag = "PASS" if not r["ra_failed"] else "FAIL_RA"
        print(f"[{flag}] {f:50s} id={r['alpha_id']} s={r['sharpe']} f={r['fitness']} 2y={r['two_year_sharpe']} ra_failed={r['ra_failed']} cluster={r['cluster_value']}")
    else:
        print(f"[{r.get('status')}] {f:50s} {r.get('error','')}")
print("===== DONE =====", flush=True)
passed = [FIELDS[i] for i,cid in enumerate(children) if results.get(cid,{}).get("ra_failed") is False]
print(f"PASSED ra_failed:false count = {len(passed)} -> {passed}")
