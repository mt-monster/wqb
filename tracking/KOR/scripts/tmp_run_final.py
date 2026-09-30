# -*- coding: utf-8 -*-
"""FINAL —— 最后一组压 prod 尝试（P02ROJrw=0.7084，目标<0.7）。
唯一未试旋钮：分组轴换成数据自带 subindustry 字段 / 外层套 rank / 极短 ts_mean。
"""
import asyncio, json, sys, os, time
REPO = r"D:\coding\traeCN_project\wqb"
sys.path.insert(0, os.path.join(REPO, "world-quant-brain-mcp"))
R = "divide(vec_avg(shrt38_stk_invactsell_amt), add(vec_avg(shrt38_stk_invactbuy_amt), 0.0001))"
SPECS = [
  ("Z1_field_axis", "SUBINDUSTRY", 4, 0.08, [
     ("z1_shrt38_subind", f"group_rank({R}, shrt38_subindustry)"),
     ("z2_shrt38_sector", f"group_rank({R}, shrt38_sector)"),
  ]),
  ("Z2_outer_rank", "SUBINDUSTRY", 4, 0.08, [
     ("z3_rank_group", f"rank(group_rank({R}, subindustry))"),
     ("z4_tsmean3",    f"group_rank(ts_mean({R}, 3), subindustry)"),
  ]),
  ("Z3_combo", "SUBINDUSTRY", 4, 0.05, [
     ("z5_tsmean2_t05", f"group_rank(ts_mean({R}, 2), subindustry)"),
     ("z6_pow05",       f"group_rank(signed_power({R}, 0.5), subindustry)"),
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
        pid = r.get("multisimulation_id") or (r.get("location") or "").rstrip("/").split("/")[-1]
        print(f"{gname} pid={pid} n={len(items)}")
        out["batches"].append({"group":gname,"nu":nu,"decay":dec,"trunc":trunc,"progress_id":pid,"ids":[it[0] for it in items]})
        await asyncio.sleep(1)
    with open(os.path.join(REPO,"tracking/KOR/candidates/wave_FINAL_submitted.json"),"w",encoding="utf-8") as f:
        json.dump(out,f,ensure_ascii=False,indent=1)
asyncio.run(main())
