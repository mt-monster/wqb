# -*- coding: utf-8 -*-
"""DECOUPLE3 —— 沿 P02ROJrw(prod 0.7084) 的 subindustry 轴继续压 prod。
变量：更细/更粗 group 轴 × decay 微调 × 截断。目标 prod<0.7 且四闸全过。
"""
import asyncio, json, sys, os, time
REPO = r"D:\coding\traeCN_project\wqb"
sys.path.insert(0, os.path.join(REPO, "world-quant-brain-mcp"))
R = "divide(vec_avg(shrt38_stk_invactsell_amt), add(vec_avg(shrt38_stk_invactbuy_amt), 0.0001))"
GROUPS = [
  ("M1_subind_d4", "SUBINDUSTRY", 4, [
     ("m1_subind_d4_t05", f"group_rank({R}, subindustry)"),  # trunc 0.05 via settings
     ("m2_sector_axis",   f"group_rank({R}, sector)"),
  ]),
  ("M2_subind_d6", "SUBINDUSTRY", 6, [
     ("m3_subind_d6",     f"group_rank({R}, subindustry)"),
     ("m4_industry_axis", f"group_rank({R}, industry)"),
  ]),
  ("M3_subind_d4t02", "SUBINDUSTRY", 4, [
     ("m5_subind_d4t02",  f"group_rank({R}, subindustry)"),
     ("m6_subind_decay3", f"group_rank({R}, subindustry)"),
  ]),
]
async def main():
    from brain_api import brain_client
    from tools_sim import create_multi_simulation
    await brain_client.ensure_authenticated()
    out={"submitted_at": time.strftime("%Y-%m-%d %H:%M:%S"), "batches": []}
    specs = [
      ("M1_subind_d4", "SUBINDUSTRY", 4, 0.05, [("m1_subind_d4_t05",f"group_rank({R}, subindustry)"),("m2_sector_axis",f"group_rank({R}, sector)")]),
      ("M2_subind_d6", "SUBINDUSTRY", 6, 0.08, [("m3_subind_d6",f"group_rank({R}, subindustry)"),("m4_industry_axis",f"group_rank({R}, industry)")]),
      ("M3_subind_d4t02", "SUBINDUSTRY", 4, 0.02, [("m5_subind_d4t02",f"group_rank({R}, subindustry)"),("m6_subind_decay3",f"group_rank({R}, subindustry)")]),
    ]
    for gname, nu, dec, trunc, items in specs:
        r = await create_multi_simulation([it[1] for it in items], region="KOR", universe="TOP600", delay=1,
                decay=dec, neutralization=nu, truncation=trunc, nan_handling="ON", test_period="P0Y0M")
        pid = r.get("multisimulation_id") or (r.get("location") or "").rstrip("/").split("/")[-1]
        print(f"{gname} pid={pid} n={len(items)} trunc={trunc}")
        out["batches"].append({"group":gname,"nu":nu,"decay":dec,"trunc":trunc,"progress_id":pid,"ids":[it[0] for it in items]})
        await asyncio.sleep(1)
    with open(os.path.join(REPO,"tracking/KOR/candidates/wave_DECOUPLE3_submitted.json"),"w",encoding="utf-8") as f:
        json.dump(out,f,ensure_ascii=False,indent=1)
asyncio.run(main())
