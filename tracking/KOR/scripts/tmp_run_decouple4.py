# -*- coding: utf-8 -*-
"""DECOUPLE4 —— 最后一推（压 prod<0.7）。P02ROJrw=0.7084。
旋钮：trunc极低 / group_zscore / 极短平滑消CW / 内层ts_rank短窗。
"""
import asyncio, json, sys, os, time
REPO = r"D:\coding\traeCN_project\wqb"
sys.path.insert(0, os.path.join(REPO, "world-quant-brain-mcp"))
R = "divide(vec_avg(shrt38_stk_invactsell_amt), add(vec_avg(shrt38_stk_invactbuy_amt), 0.0001))"
# (group_name, nu, decay, trunc, [(id, expr), ...])  —— 每表达式必须全局唯一
SPECS = [
  ("K1_subd_trunc01", "SUBINDUSTRY", 4, 0.01, [
     ("k1_subind_t01", f"group_rank({R}, subindustry)"),
     ("k2_zscore_subind", f"group_zscore({R}, subindustry)"),
  ]),
  ("K2_subd_tsdl3", "SUBINDUSTRY", 4, 0.08, [
     ("k3_tsdl3_subind", f"group_rank(ts_decay_linear({R}, 3), subindustry)"),
     ("k4_tr5_subind",   f"group_rank(ts_rank({R}, 5), subindustry)"),
  ]),
  ("K3_subd_trunc02", "SUBINDUSTRY", 4, 0.02, [
     ("k5_subind_t02", f"group_rank({R}, subindustry)"),
     ("k6_zscore_sub_t02", f"group_zscore({R}, subindustry)"),
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
        print(f"{gname} pid={pid} n={len(items)} trunc={trunc}")
        out["batches"].append({"group":gname,"nu":nu,"decay":dec,"trunc":trunc,"progress_id":pid,"ids":[it[0] for it in items]})
        await asyncio.sleep(1)
    with open(os.path.join(REPO,"tracking/KOR/candidates/wave_DECOUPLE4_submitted.json"),"w",encoding="utf-8") as f:
        json.dump(out,f,ensure_ascii=False,indent=1)
asyncio.run(main())
