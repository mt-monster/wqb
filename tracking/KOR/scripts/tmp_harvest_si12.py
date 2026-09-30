# -*- coding: utf-8 -*-
"""收割 SI12 multi-sim 结果。"""
import asyncio, json, sys, os
REPO = r"D:\coding\traeCN_project\wqb"
sys.path.insert(0, os.path.join(REPO, "world-quant-brain-mcp"))
PIDS = json.load(open(os.path.join(REPO,"tracking/KOR/candidates/wave_SI12_submitted.json"),encoding="utf-8"))["batches"]

async def main():
    from brain_api import brain_client
    await brain_client.ensure_authenticated()
    for b in PIDS:
        pid = b["progress_id"]
        for attempt in range(60):
            r = await brain_client._request("GET", f"https://api.worldquantbrain.com/simulations/{pid}")
            try:
                d = r.json()
            except Exception:
                await asyncio.sleep(15); continue
            if d.get("status") == "COMPLETE" or d.get("children"):
                ch = d.get("children") or []
                print(f"--- {b['group']} COMPLETE children={len(ch)}")
                for c in ch:
                    aid = (c.get("location") or "").rstrip("/").split("/")[-1]
                    if not aid or aid == "simulations": 
                        print("    raw child:", json.dumps(c)[:200]); continue
                    rr = await brain_client._request("GET", f"https://api.worldquantbrain.com/alphas/{aid}")
                    dd = rr.json()
                    is_ = dd.get("is") or {}
                    chk = {x.get("name"): x.get("result") for x in is_.get("checks",[])}
                    print(f"    {aid} S={is_.get('sharpe')} F={is_.get('fitness')} TO={is_.get('turnover')} FAILs={[k for k,v in chk.items() if v=='FAIL']}")
                break
            prog = d.get("progress")
            if attempt % 4 == 0:
                print(f"    {b['group']} progress={prog}")
            await asyncio.sleep(20)
        else:
            print(f"--- {b['group']} TIMEOUT")
asyncio.run(main())
