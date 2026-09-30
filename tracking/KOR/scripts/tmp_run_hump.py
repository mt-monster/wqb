# -*- coding: utf-8 -*-
"""HUMP/MM 波 —— 论坛实测降 prod 杠杆（hump 平滑 / mm 结构 / trade_when）。
基线 P02ROJrw prod 0.7084（group_rank(R, subindustry)）。
合规：单信号结构化（hump 是平滑算子、mm 是字段几何、trade_when 是事件门控）。
"""
import asyncio, json, sys, os, time
REPO = r"D:\coding\traeCN_project\wqb"
sys.path.insert(0, os.path.join(REPO, "world-quant-brain-mcp"))
R = "divide(vec_avg(shrt38_stk_invactsell_amt), add(vec_avg(shrt38_stk_invactbuy_amt), 0.0001))"
SPECS = [
  # H1: hump 外套（论坛实测量级最强 0.855→0.32）
  ("H1_hump", "SUBINDUSTRY", 4, 0.08, [
     ("h1_hump001",  f"hump(group_rank({R}, subindustry), 0.001)"),
     ("h2_hump005",  f"hump(group_rank({R}, subindustry), 0.005)"),
  ]),
  ("H2_hump2", "SUBINDUSTRY", 4, 0.08, [
     ("h3_hump01",   f"hump(group_rank({R}, subindustry), 0.01)"),
     ("h4_hump002",  f"hump(group_rank({R}, subindustry), 0.002)"),
  ]),
  # M1: mm 结构（滚动极值差 − 滚动均值差），作用在卖/买比上
  ("M1_mm", "SUBINDUSTRY", 4, 0.08, [
     ("m1_mm110",    f"group_rank(subtract(ts_max_diff({R},110), ts_av_diff({R},110)), subindustry)"),
     ("m2_mm250",    f"group_rank(subtract(ts_max_diff({R},250), ts_av_diff({R},250)), subindustry)"),
  ]),
  # T1: trade_when 事件门控（分层）
  ("T1_tw", "SUBINDUSTRY", 4, 0.08, [
     ("t1_tw_vol",   f"trade_when(volume > ts_mean(volume, 20), group_rank({R}, subindustry), -1)"),
     ("t2_tw_abs",   f"trade_when(ts_rank(vec_avg(shrt38_stk_invactbuy_amt), 252) > 0.3, group_rank({R}, subindustry), -1)"),
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
    with open(os.path.join(REPO,"tracking/KOR/candidates/wave_HUMP_submitted.json"),"w",encoding="utf-8") as f:
        json.dump(out,f,ensure_ascii=False,indent=1)
asyncio.run(main())
