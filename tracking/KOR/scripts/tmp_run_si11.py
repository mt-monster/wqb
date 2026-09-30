# -*- coding: utf-8 -*-
"""SI11 —— 决定性：把已验证 prod<0.7 且 F≥1.0 的 hump 腿，改用 SLOW_AND_FAST 设置。

xA3LVkzl: hump(group_rank(RA, sector), hump=0.003)  SUBINDUSTRY decay4 → prod 0.6207 S2.03 F1.17 ✓指标
88j0VQ6W: hump(group_rank(RA, industry), hump=0.003) SUBINDUSTRY decay4 → prod 0.6044 S1.95 F1.09 ✓指标
问题：SUBINDUSTRY → PURE_POWER_POOL_THEME FAIL
本波：同表达式，换 SLOW_AND_FAST + decay30/20 + trunc0.02
"""
import asyncio, json, sys, os, time
REPO = r"D:\coding\traeCN_project\wqb"
sys.path.insert(0, os.path.join(REPO, "world-quant-brain-mcp"))

RA = "divide(vec_avg(shrt38_stk_invactsell_amt), add(vec_avg(shrt38_stk_invactbuy_amt), 0.0001))"
RS = "divide(vec_sum(shrt38_stk_invactsell_amt), vec_sum(shrt38_stk_invactbuy_amt))"
NU = "SLOW_AND_FAST"

SPECS = [
  ("K1_hump_slow", NU, 30, 0.02, [
     ("k1_a", f"hump(group_rank({RA}, sector), hump=0.003)"),
     ("k1_b", f"hump(group_rank({RA}, industry), hump=0.003)"),
  ]),
  ("K2_hump_sub", NU, 30, 0.02, [
     ("k2_a", f"hump(group_rank({RA}, subindustry), hump=0.003)"),
     ("k2_b", f"hump(group_rank({RS}, sector), hump=0.003)"),
  ]),
  ("K3_dec20", NU, 20, 0.02, [
     ("k3_a", f"hump(group_rank({RA}, sector), hump=0.0025)"),
     ("k3_b", f"hump(group_rank({RA}, industry), hump=0.0025)"),
  ]),
  ("K4_plain", NU, 30, 0.02, [
     ("k4_a", f"group_rank({RA}, sector)"),
     ("k4_b", f"group_rank({RA}, industry)"),
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
            print(f"{gname} ERR: {json.dumps(r,ensure_ascii=False)[:200]}"); continue
        pid = r.get("multisimulation_id") or (r.get("location") or "").rstrip("/").split("/")[-1]
        print(f"{gname} pid={pid}")
        out["batches"].append({"group":gname,"nu":nu,"decay":dec,"trunc":trunc,"progress_id":pid,"ids":[it[0] for it in items]})
        await asyncio.sleep(1)
    with open(os.path.join(REPO,"tracking/KOR/candidates/wave_SI11_submitted.json"),"w",encoding="utf-8") as f:
        json.dump(out,f,ensure_ascii=False,indent=1)
    print("SAVED wave_SI11_submitted.json")
asyncio.run(main())
