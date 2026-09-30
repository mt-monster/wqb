# -*- coding: utf-8 -*-
import asyncio, json, sys, os
REPO = r"D:\coding\traeCN_project\wqb"
sys.path.insert(0, os.path.join(REPO, "world-quant-brain-mcp"))
WAVE = sys.argv[1] if len(sys.argv)>1 else "wave_SI12_submitted.json"
BATCHES = json.load(open(os.path.join(REPO,"tracking/KOR/candidates",WAVE),encoding="utf-8"))["batches"]

def sid_of(c):
    if isinstance(c, str): return c.rstrip("/").split("/")[-1]
    if isinstance(c, dict): return (c.get("location") or c.get("id") or "").rstrip("/").split("/")[-1]
    return ""

async def main():
    from brain_api import brain_client
    await brain_client.ensure_authenticated()
    results=[]
    for b in BATCHES:
        pid = b["progress_id"]
        for attempt in range(80):
            r = await brain_client._request("GET", f"https://api.worldquantbrain.com/simulations/{pid}")
            try: d = r.json()
            except Exception:
                await asyncio.sleep(15); continue
            ch = d.get("children")
            if d.get("status")=="COMPLETE" or ch:
                ch = ch or []
                print(f"=== {b['group']} children={len(ch)}")
                for c in ch:
                    sid = sid_of(c)
                    if not sid: continue
                    # 从 simulation 取 alpha
                    sr = await brain_client._request("GET", f"https://api.worldquantbrain.com/simulations/{sid}")
                    try: sd = sr.json()
                    except Exception: print("   sim parse fail", sid); continue
                    aid = ((sd.get("alpha") or "").rstrip("/").split("/")[-1]) or sd.get("alphaId") or ""
                    if not aid:
                        print(f"   sim {sid} keys={list(sd.keys())[:12]}"); continue
                    rr = await brain_client._request("GET", f"https://api.worldquantbrain.com/alphas/{aid}")
                    dd = rr.json()
                    is_ = dd.get("is") or {}
                    chk = {x.get("name"): x.get("result") for x in is_.get("checks",[])}
                    print(f"   {aid} S={is_.get('sharpe')} F={is_.get('fitness')} TO={is_.get('turnover')} FAILs={[k for k,v in chk.items() if v=='FAIL']}")
                    print(f"       {(dd.get('regular') or {}).get('code','')[:160]}")
                    results.append({"group":b["group"],"id":aid,"sharpe":is_.get("sharpe"),"fitness":is_.get("fitness"),
                                    "turnover":is_.get("turnover"),"fails":[k for k,v in chk.items() if v=='FAIL'],
                                    "expr":(dd.get('regular') or {}).get('code','')})
                break
            if attempt % 4==0: print(f"   {b['group']} progress={d.get('progress')}")
            await asyncio.sleep(20)
        else: print(f"=== {b['group']} TIMEOUT")
    with open(os.path.join(REPO,"tracking/KOR/candidates",WAVE.replace("_submitted","_results")),"w",encoding="utf-8") as f:
        json.dump(results,f,ensure_ascii=False,indent=1)
    print("SAVED results")
asyncio.run(main())
