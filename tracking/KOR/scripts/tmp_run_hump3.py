# -*- coding: utf-8 -*-
"""HUMP3 —— 修正 hump 命名参数语法（hump=<val>）。"""
import asyncio, json, sys, os, time
REPO = r"D:\coding\traeCN_project\wqb"
sys.path.insert(0, os.path.join(REPO, "world-quant-brain-mcp"))
R = "divide(vec_avg(shrt38_stk_invactsell_amt), add(vec_avg(shrt38_stk_invactbuy_amt), 0.0001))"
SPECS = [
  ("H1_hump", "SUBINDUSTRY", 4, 0.08, [
     ("h1_hump001",  f"hump(group_rank({R}, subindustry), hump=0.001)"),
     ("h2_hump005",  f"hump(group_rank({R}, subindustry), hump=0.005)"),
  ]),
  ("H2_hump2", "SUBINDUSTRY", 4, 0.08, [
     ("h3_hump01",   f"hump(group_rank({R}, subindustry), hump=0.01)"),
     ("h4_hump002",  f"hump(group_rank({R}, subindustry), hump=0.002)"),
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
            print(f"{gname} GATE-REJECT: {json.dumps(r.get('failed_expressions',{}),ensure_ascii=False)[:200]}")
            continue
        pid = r.get("multisimulation_id") or (r.get("location") or "").rstrip("/").split("/")[-1]
        print(f"{gname} pid={pid} n={len(items)}")
        out["batches"].append({"group":gname,"nu":nu,"decay":dec,"trunc":trunc,"progress_id":pid,"ids":[it[0] for it in items]})
        await asyncio.sleep(1)
    with open(os.path.join(REPO,"tracking/KOR/candidates/wave_HUMP3_submitted.json"),"w",encoding="utf-8") as f:
        json.dump(out,f,ensure_ascii=False,indent=1)
asyncio.run(main())
