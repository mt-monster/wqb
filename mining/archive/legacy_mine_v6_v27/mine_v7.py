import json, sys, os, time
import os
sys.path.insert(0, os.environ.get("WQ_ACE_LIB", r"C:/Users/MENGTAO/.workbuddy/skills/brain-simAlphasinBatch-and-track/scripts"))
import ace_lib

cfg = json.load(open(r'C:/Users/MENGTAO/.workbuddy/skills/brain-simAlphasinBatch-and-track/configs/config.json'))
for k, v in cfg.items():
    os.environ[str(k).upper()] = str(v); os.environ[str(k)] = str(v)
SESSION = ace_lib.start_session()
API = ace_lib.brain_api_url

F = "historic_earnings_surprise_score"  # proven strong field (xAdL5vmN used no-suffix)

# 4 variants clearly different from xAdL5vmN's exact T_A (vec_avg+subindustry+SLOW_AND_FAST+decay6)
BASE = {
    "instrumentType": "EQUITY", "region": "USA", "universe": "TOP3000", "delay": 1,
    "truncation": 0.08, "pasteurization": "ON", "unitHandling": "VERIFY", "nanHandling": "ON",
    "maxTrade": "ON", "maxPosition": "OFF", "language": "FASTEXPR", "visualization": False,
    "startDate": "2014-01-01", "endDate": "2023-12-31",
}

def mk(name, regular, neut, decay, d1, d2):
    s = dict(BASE); s["neutralization"] = neut; s["decay"] = decay
    return {"name": name, "type": "REGULAR", "regular": regular, "settings": s}

cands = [
    mk("V1_zscore_industry_d90",
       f"ts_decay_linear(signed_power(subtract(group_rank(ts_zscore(ts_backfill({F},252),252), industry), 0.5), 5), 90)",
       "SLOW_AND_FAST", 6, None, None),
    mk("V2_tsmean_subind_d90",
       f"ts_decay_linear(signed_power(subtract(group_rank(ts_mean({F},20), subindustry), 0.5), 5), 90)",
       "SLOW_AND_FAST", 6, None, None),
    mk("V3_rank_backfill",
       f"rank(ts_backfill({F}, 252))",
       "SLOW_AND_FAST", 6, None, None),
    mk("V4_stddev_industry",
       f"group_rank(ts_std_dev({F}, 30), industry)",
       "SLOW_AND_FAST", 6, None, None),
    mk("V5_decaysigned_marketslow_d60",
       f"ts_decay_linear(signed_power(subtract(group_rank(vec_avg({F}), subindustry), 0.5), 5), 60)",
       "MARKET", 5, None, None),
]

alphas = [{"type": c["type"], "regular": c["regular"], "settings": c["settings"]} for c in cands]
print(f"Submitting {len(alphas)} variant sims...", flush=True)
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

PER = 540
results = {}
for cid in children:
    t0 = time.time(); st = None
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
                        # extract CLUSTER_TEST value
                        cval = None
                        for c in checks.get("warning", []) + checks.get("fail", []):
                            if "CLUSTER" in c.get("name",""):
                                cval = c.get("value")
                        results[cid] = {"status":"COMPLETED","alpha_id":aid,
                            "sharpe":m.get("sharpe"),"fitness":m.get("fitness"),
                            "two_year_sharpe":m.get("two_year_sharpe"),
                            "ra_failed":ra.get("ra_failed"),"ppa_failed":ra.get("ppa_failed"),
                            "cluster_value":cval}
                    else:
                        results[cid] = {"status":"COMPLETED_NO_ALPHA"}
                    break
                elif st in ("ERROR","FAIL","FAILED"):
                    err = str(d.get("errors") or d.get("error") or d.get("message") or "")[:160]
                    results[cid] = {"status":"ERROR","error":err}; break
                elif st == "CANCELLED":
                    results[cid] = {"status":"CANCELLED"}; break
        except Exception as e:
            print("poll exc", e, flush=True)
        time.sleep(5)
    else:
        results[cid] = {"status":"TIMEOUT"}

print("\n===== RESULTS =====", flush=True)
for i, cid in enumerate(children):
    c = cands[i] if i < len(cands) else {}
    r = results.get(cid, {})
    if r.get("status") == "COMPLETED":
        print(f"[{c.get('name')}] id={r['alpha_id']} s={r['sharpe']} f={r['fitness']} 2y={r['two_year_sharpe']} ra_failed={r['ra_failed']} cluster={r['cluster_value']}")
    else:
        print(f"[{c.get('name')}] {r.get('status')} {r.get('error','')}")
print("===== DONE =====", flush=True)
