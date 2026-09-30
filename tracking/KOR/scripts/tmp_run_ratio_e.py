# -*- coding: utf-8 -*-
"""RATIO-E decay 深阶梯 —— E5pjkN0P(decay20) 五闸全过唯一腿，探 decay 30/40/60 + truncation 影响。"""
import asyncio, json, sys, os, time
REPO = r"D:\coding\traeCN_project\wqb"
sys.path.insert(0, os.path.join(REPO, "world-quant-brain-mcp"))
B="divide(vec_avg(shrt38_stk_invactsell_amt), add(vec_avg(shrt38_stk_invactbuy_amt), 0.0001))"
E = f"group_rank({B}, market)"
GROUPS = [
  ("E_d30", "STATISTICAL", 30, 0.08, [("e1_d30", E), ("e1b_d30b", E)]),   # 占位第2条（重复不计，仅为满足≥2）
  ("E_d40", "STATISTICAL", 40, 0.08, [("e2_d40", E), ("e2b_d40b", E)]),
  ("E_d60", "STATISTICAL", 60, 0.08, [("e3_d60", E), ("e3b_d60b", E)]),
  ("E_d20t02", "STATISTICAL", 20, 0.02, [("e4_d20t02", E), ("e4b", E)]),
]
async def main():
    from brain_api import brain_client
    from tools_sim import create_multi_simulation
    await brain_client.ensure_authenticated()
    out={"submitted_at": time.strftime("%Y-%m-%d %H:%M:%S"), "batches": []}
    for gname, nu, dec, trunc, items in GROUPS:
        r = await create_multi_simulation([it[1] for it in items], region="KOR", universe="TOP600", delay=1,
                decay=dec, neutralization=nu, truncation=trunc, nan_handling="ON", test_period="P0Y0M")
        pid = r.get("multisimulation_id") or (r.get("location") or "").rstrip("/").split("/")[-1]
        print(f"{gname} pid={pid} decay={dec} trunc={trunc}")
        out["batches"].append({"group":gname,"nu":nu,"decay":dec,"trunc":trunc,"progress_id":pid,
                               "ids":[it[0] for it in items]})
        await asyncio.sleep(1)
    with open(os.path.join(REPO,"tracking/KOR/candidates/wave_RATIOE_submitted.json"),"w",encoding="utf-8") as f:
        json.dump(out,f,ensure_ascii=False,indent=1)
asyncio.run(main())
