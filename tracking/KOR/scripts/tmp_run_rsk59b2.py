# -*- coding: utf-8 -*-
"""RSK59B 补测 s4/s5（借券费率取反 IND/SUB），另加两条利用 nu 提 2Y 的姊妹。"""
import asyncio, json, sys, os, time
REPO = r"D:\coding\traeCN_project\wqb"
sys.path.insert(0, os.path.join(REPO, "world-quant-brain-mcp"))
GROUPS = [
  ("R4_ind", "INDUSTRY", 4, [
     ("s4_lastrate_ind", "group_rank(multiply(-1, vec_avg(rsk59_last_rate)), market)"),
     ("s4b_avg_ind",     "group_rank(multiply(-1, divide(add(vec_avg(rsk59_offer_rate), vec_avg(rsk59_last_rate)), 2)), market)"),
  ]),
  ("R5_sub", "SUBINDUSTRY", 4, [
     ("s5_lastrate_sub", "group_rank(multiply(-1, vec_avg(rsk59_last_rate)), market)"),
     ("s5b_avg_sub",     "group_rank(multiply(-1, divide(add(vec_avg(rsk59_offer_rate), vec_avg(rsk59_last_rate)), 2)), market)"),
  ]),
]
async def main():
    from brain_api import brain_client
    from tools_sim import create_multi_simulation
    await brain_client.ensure_authenticated()
    out={"submitted_at": time.strftime("%Y-%m-%d %H:%M:%S"), "batches": []}
    for gname, nu, dec, items in GROUPS:
        r = await create_multi_simulation([it[1] for it in items], region="KOR", universe="TOP600", delay=1,
                decay=dec, neutralization=nu, truncation=0.08, nan_handling="ON", test_period="P0Y0M")
        pid = r.get("multisimulation_id") or (r.get("location") or "").rstrip("/").split("/")[-1]
        print(f"{gname} pid={pid} n={len(items)}")
        out["batches"].append({"group":gname,"nu":nu,"decay":dec,"progress_id":pid,"ids":[it[0] for it in items]})
        await asyncio.sleep(1)
    with open(os.path.join(REPO,"tracking/KOR/candidates/wave_RSK59B2_submitted.json"),"w",encoding="utf-8") as f:
        json.dump(out,f,ensure_ascii=False,indent=1)
asyncio.run(main())
