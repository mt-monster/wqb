# -*- coding: utf-8 -*-
"""SI5 —— sector/industry 轴扩展（SI4 证实这两轴可过提交层）。"""
import asyncio, json, sys, os, time
REPO = r"D:\coding\traeCN_project\wqb"
sys.path.insert(0, os.path.join(REPO, "world-quant-brain-mcp"))

RA = "divide(vec_avg(shrt38_stk_invactsell_amt), add(vec_avg(shrt38_stk_invactbuy_amt), 0.0001))"
RS = "divide(vec_sum(shrt38_stk_invactsell_amt), vec_sum(shrt38_stk_invactbuy_amt))"

SPECS = [
  ("S1_sec", "SUBINDUSTRY", 4, 0.08, [
     ("s1_a", f"hump(group_rank({RA}, sector), hump=0.0025)"),
     ("s1_b", f"hump(group_rank({RA}, sector), hump=0.0035)"),
  ]),
  ("S2_ind", "SUBINDUSTRY", 4, 0.08, [
     ("s2_a", f"hump(group_rank({RA}, industry), hump=0.0025)"),
     ("s2_b", f"hump(group_rank({RA}, industry), hump=0.004)"),
  ]),
  ("S3_secsum", "SUBINDUSTRY", 4, 0.08, [
     ("s3_a", f"hump(group_rank({RS}, sector), hump=0.003)"),
     ("s3_b", f"hump(group_rank({RS}, industry), hump=0.003)"),
  ]),
  ("S4_market", "SUBINDUSTRY", 4, 0.08, [
     ("s4_a", f"hump(group_rank({RA}, market), hump=0.003)"),
     ("s4_b", f"hump(group_rank(ts_mean({RA},5), sector), hump=0.003)"),
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
            print(f"{gname} GATE-REJECT: {json.dumps(r.get('failed_expressions',{}),ensure_ascii=False)[:250]}")
            continue
        pid = r.get("multisimulation_id") or (r.get("location") or "").rstrip("/").split("/")[-1]
        print(f"{gname} pid={pid} n={len(items)}")
        out["batches"].append({"group":gname,"nu":nu,"decay":dec,"trunc":trunc,"progress_id":pid,"ids":[it[0] for it in items]})
        await asyncio.sleep(1)
    with open(os.path.join(REPO,"tracking/KOR/candidates/wave_SI5_submitted.json"),"w",encoding="utf-8") as f:
        json.dump(out,f,ensure_ascii=False,indent=1)
    print("SAVED wave_SI5_submitted.json")
asyncio.run(main())
