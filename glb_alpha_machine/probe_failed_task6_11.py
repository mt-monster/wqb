# -*- coding: utf-8 -*-
"""Re-probe the 16 failed sims (task 6 idx40-47 + task 11 idx80-87) to capture
the REAL API child error messages (the pipeline never persisted them)."""
import os, sys, time, json, pickle
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from glb_machine_lib import login, generate_sim_data

BASE = "https://api.worldquantbrain.com"
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "cache", "probe_failed_6_11.json")
REGION, UNI, NEUT = "GLB", "TOP3000", "SUBINDUSTRY"

fo = pickle.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "cache", "stage1_first_order.pkl"), "rb"))
task6 = fo[40:48]
task11 = fo[80:88]
batches = [("task6_idx40-47", task6), ("task11_idx80-87", task11)]

s = login()
all_res = []
for tag, alpha_list in batches:
    sim_data_list = generate_sim_data(alpha_list, REGION, UNI, NEUT)
    print(f"\n=== {tag}: POST 8 sims ===", flush=True)
    progress_url = None
    for attempt in range(15):
        try:
            resp = s.post(f"{BASE}/simulations", json=sim_data_list, timeout=60)
            if resp.status_code == 201:
                progress_url = resp.headers.get("Location")
                break
            elif resp.status_code == 429:
                w = min(40*(attempt+1), 300); print(f"  429 wait {w}s", flush=True); time.sleep(w); s = login()
            else:
                print(f"  HTTP {resp.status_code}: {resp.text[:200]}", flush=True); time.sleep(30); s = login()
        except Exception as e:
            print(f"  post err {type(e).__name__}: {e}", flush=True); time.sleep(30); s = login()
    if not progress_url:
        print(f"  {tag}: GIVE UP (no progress_url after retries)", flush=True)
        all_res.append({"tag": tag, "outcome": "GIVE_UP", "children": []})
        continue
    # poll
    waited = 0; child_results = None
    while waited < 900:
        try:
            sim = s.get(progress_url, timeout=30)
            ra = sim.headers.get("Retry-After", 0)
            if ra == 0:
                d = sim.json(); st = d.get("status")
                if st == "COMPLETE":
                    child_results = d.get("children", []); break
                elif st in ("ERROR", "DONE"):
                    det = {}
                    for cid in d.get("children", []):
                        if isinstance(cid, dict):
                            det[cid.get("id","")] = cid
                        elif isinstance(cid, str):
                            try: det[cid] = s.get(f"{BASE}/simulations/{cid}", timeout=15).json()
                            except Exception: det[cid] = {"status":"UNKNOWN"}
                    child_results = det; break
                else:
                    time.sleep(5)
            else:
                time.sleep(float(ra))
        except Exception as e:
            print(f"  poll err {type(e).__name__}", flush=True); time.sleep(30); s = login()
        waited += 5
    # summarize children
    rec = {"tag": tag, "waited": waited}
    if child_results is None:
        rec["outcome"] = "POLL_TIMEOUT"; rec["children"] = []
    elif isinstance(child_results, list):
        rec["outcome"] = "COMPLETE"; rec["children"] = [{"id": c, "status": "COMPLETE"} for c in child_results]
    else:
        kids = []
        for cid, val in child_results.items():
            if isinstance(val, dict):
                kids.append({"id": cid, "status": val.get("status"), "message": val.get("message")})
            else:
                kids.append({"id": cid, "status": "COMPLETE"})
        n_err = sum(1 for k in kids if k.get("status") != "COMPLETE")
        rec["outcome"] = "ERROR" if n_err else "COMPLETE"
        rec["children"] = kids
    print(f"  {tag} -> {rec['outcome']}", flush=True)
    for k in rec.get("children", []):
        print(f"    {k.get('id')}: {k.get('status')} {('- '+str(k.get('message'))[:150]) if k.get('message') else ''}", flush=True)
    all_res.append(rec)
    time.sleep(25)

json.dump(all_res, open(OUT, "w"), ensure_ascii=False, indent=1)
print(f"\nsaved {OUT}")
for r in all_res:
    print(r["tag"], "->", r["outcome"], "| errors:", sum(1 for c in r.get("children",[]) if c.get("status")!="COMPLETE"))
