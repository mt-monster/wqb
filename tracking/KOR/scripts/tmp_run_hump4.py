# -*- coding: utf-8 -*-
"""HUMP4 —— hump 细网格扫（0.0025~0.0045），找 prod<0.7 且 S≥1.58 的甜点。
已知：hump=0.002 → prod 0.7031/S 2.13；hump=0.005 → prod 0.3688/S 1.12。
"""
import asyncio, json, sys, os, time
REPO = r"D:\coding\traeCN_project\wqb"
sys.path.insert(0, os.path.join(REPO, "world-quant-brain-mcp"))
R = "divide(vec_avg(shrt38_stk_invactsell_amt), add(vec_avg(shrt38_stk_invactbuy_amt), 0.0001))"
SPECS = [
  ("U1", "SUBINDUSTRY", 4, 0.08, [
     ("u1_hump0025", f"hump(group_rank({R}, subindustry), hump=0.0025)"),
     ("u2_hump003",  f"hump(group_rank({R}, subindustry), hump=0.003)"),
  ]),
  ("U2", "SUBINDUSTRY", 4, 0.08, [
     ("u3_hump0035", f"hump(group_rank({R}, subindustry), hump=0.0035)"),
     ("u4_hump004",  f"hump(group_rank({R}, subindustry), hump=0.004)"),
  ]),
]
async def main():
    from brain_api import brain_client
    from tools_sim import create_multi_simulation
    await brain_client.ensure_authenticated()
    out={"submitted_at": time.strftime("%Y-%m-%d %H:%M:%S"), "batches": []}
    for gname, nu, dec, trunc, items in SPECS:
        r = await create_multi_simulation([it[1] for it in items], region="KOR", universe="TOP600", delay=1,
                decay=dec, neutralization=nu, truncation=trunc, nan_handling="ON", test_period="P0Y0M")
        if isinstance(r, dict) and r.get("error"):
            print(f"{gname} GATE: {json.dumps(r.get('failed_expressions',{}),ensure_ascii=False)[:200]}"); continue
        pid = r.get("multisimulation_id") or (r.get("location") or "").rstrip("/").split("/")[-1]
        print(f"{gname} pid={pid}")
        out["batches"].append({"group":gname,"nu":nu,"decay":dec,"trunc":trunc,"progress_id":pid,"ids":[it[0] for it in items]})
        await asyncio.sleep(1)
    with open(os.path.join(REPO,"tracking/KOR/candidates/wave_HUMP4_submitted.json"),"w",encoding="utf-8") as f:
        json.dump(out,f,ensure_ascii=False,indent=1)
asyncio.run(main())
