# -*- coding: utf-8 -*-
"""SI7 —— PENDING 窗口验证：跑新腿后立即提交（趁 MATCHES_THEMES 处于 PENDING）。

假说：新 alpha 提交时 D1 PP 主题为 PENDING（平台未判定）→ 放行；
      旧 alpha 提交时已被判 WARNING → PURE_POWER_POOL_THEME FAIL。
"""
import asyncio, json, sys, os, time
REPO = r"D:\coding\traeCN_project\wqb"
sys.path.insert(0, os.path.join(REPO, "world-quant-brain-mcp"))

RA = "divide(vec_avg(shrt38_stk_invactsell_amt), add(vec_avg(shrt38_stk_invactbuy_amt), 0.0001))"

SPECS = [
  ("P1", "SUBINDUSTRY", 4, 0.08, [
     ("p1", f"hump(group_rank({RA}, sector), hump=0.003)"),
     ("p2", f"hump(group_rank({RA}, industry), hump=0.003)"),
  ]),
  ("P2", "SUBINDUSTRY", 4, 0.08, [
     ("p3", f"hump(group_rank({RA}, market), hump=0.003)"),
     ("p4", f"group_rank(ts_rank({RA}, 252), sector)"),
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
            print(f"{gname} GATE-REJECT"); continue
        pid = r.get("multisimulation_id") or (r.get("location") or "").rstrip("/").split("/")[-1]
        print(f"{gname} pid={pid}")
        out["batches"].append({"group":gname,"nu":nu,"decay":dec,"trunc":trunc,"progress_id":pid,"ids":[it[0] for it in items]})
        await asyncio.sleep(1)
    with open(os.path.join(REPO,"tracking/KOR/candidates/wave_SI7_submitted.json"),"w",encoding="utf-8") as f:
        json.dump(out,f,ensure_ascii=False,indent=1)
    print("SAVED")
asyncio.run(main())
