# -*- coding: utf-8 -*-
"""RATIO-C 重发（改正单条提交的 PID 捕获：用 location 字段）。"""
import asyncio, json, sys, os, time
REPO = r"D:\coding\traeCN_project\wqb"
sys.path.insert(0, os.path.join(REPO, "world-quant-brain-mcp"))
BASE = "divide(vec_avg(shrt38_stk_invactsell_amt), add(vec_avg(shrt38_stk_invactbuy_amt), 0.0001))"
VARIANTS = [
  ("c1_rk63_stat",   f"group_rank(ts_rank({BASE}, 63), market)", "STATISTICAL", 4),
  ("c2_rk126_stat",  f"group_rank(ts_rank({BASE}, 126), market)", "STATISTICAL", 4),
  ("c3_rk252_stat",  f"group_rank(ts_rank({BASE}, 252), market)", "STATISTICAL", 4),
  ("c7_base_d10",    f"group_rank({BASE}, market)", "STATISTICAL", 10),
  ("c8_base_d20",    f"group_rank({BASE}, market)", "STATISTICAL", 20),
  ("c11_base_d6",    f"group_rank({BASE}, market)", "STATISTICAL", 6),
  ("c12_rk126_sub",  f"group_rank(ts_rank({BASE}, 126), market)", "SUBINDUSTRY", 4),
  ("c13_rk63_sub",   f"group_rank(ts_rank({BASE}, 63), market)", "SUBINDUSTRY", 4),
  ("c14_basesector", f"group_rank({BASE}, sector)", "STATISTICAL", 4),
  ("c15_base_exch",  f"group_rank({BASE}, exchange)", "STATISTICAL", 4),
]
async def main():
    from brain_api import brain_client
    from tools_sim import create_multi_simulation
    await brain_client.ensure_authenticated()
    out={"submitted_at": time.strftime("%Y-%m-%d %H:%M:%S"), "batches": []}
    for v in VARIANTS:
        r = await create_multi_simulation([v[1]], region="KOR", universe="TOP600", delay=1,
                decay=v[3], neutralization=v[2], truncation=0.08, nan_handling="ON", test_period="P0Y0M")
        print(f"{v[0]} resp={json.dumps(r,ensure_ascii=False)[:160]}")
        out["batches"].append({"id":v[0],"nu":v[2],"decay":v[3],"resp":r})
        await asyncio.sleep(0.6)
    with open(os.path.join(REPO,"tracking/KOR/candidates/wave_RATIOC_submitted.json"),"w",encoding="utf-8") as f:
        json.dump(out,f,ensure_ascii=False,indent=1)
asyncio.run(main())
