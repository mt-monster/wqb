# -*- coding: utf-8 -*-
"""DECOUPLE2 —— 裸比值 × 更细分组轴 × 极浅decay，目标把 prod 从 0.749 压到 0.7 下。
合规：单信号（比值）+ 分组轴变化。
注意：同表达式跨批会去重 → 每条表达式必须唯一。
"""
import asyncio, json, sys, os, time
REPO = r"D:\coding\traeCN_project\wqb"
sys.path.insert(0, os.path.join(REPO, "world-quant-brain-mcp"))
SELL = "vec_avg(shrt38_stk_invactsell_amt)"
BUY  = "vec_avg(shrt38_stk_invactbuy_amt)"
GROUPS = [
  ("N1_sub_d0", "SUBINDUSTRY", 0, [
     ("n1_base_sub_d0",  f"group_rank(divide({SELL}, add({BUY}, 0.0001)), market)"),
     ("n2_rk22_sub_d0",  f"group_rank(ts_rank(divide({SELL}, add({BUY}, 0.0001)), 22), market)"),
  ]),
  ("N2_sector_d4", "SECTOR", 4, [
     ("n3_base_sector_d4", f"group_rank(divide({SELL}, add({BUY}, 0.0001)), market)"),
     ("n4_base_subind_d4", f"group_rank(divide({SELL}, add({BUY}, 0.0001)), subindustry)"),
  ]),
  ("N3_sub_d2", "SUBINDUSTRY", 2, [
     ("n5_base_sub_d2",  f"group_rank(divide({SELL}, add({BUY}, 0.0001)), market)"),
     ("n6_rk63_sub_d2",  f"group_rank(ts_rank(divide({SELL}, add({BUY}, 0.0001)), 63), market)"),
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
    with open(os.path.join(REPO,"tracking/KOR/candidates/wave_DECOUPLE2_submitted.json"),"w",encoding="utf-8") as f:
        json.dump(out,f,ensure_ascii=False,indent=1)
asyncio.run(main())
