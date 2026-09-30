# -*- coding: utf-8 -*-
"""SI10 —— ts_delta 结构（3qXK50vZ prod 0.3921）的 F 优化。

3qXK50vZ: group_rank(ts_delta(ts_zscore(RS,504),10), sector) SLOW_AND_FAST decay30
  → prod 0.3921 ✅✅ 但 F 0.78 FAIL
目标：保 prod<0.7，把 F 提到 ≥1.0。
"""
import asyncio, json, sys, os, time
REPO = r"D:\coding\traeCN_project\wqb"
sys.path.insert(0, os.path.join(REPO, "world-quant-brain-mcp"))

RS = "divide(vec_sum(shrt38_stk_invactsell_amt), vec_sum(shrt38_stk_invactbuy_amt))"
RA = "divide(vec_avg(shrt38_stk_invactsell_amt), add(vec_avg(shrt38_stk_invactbuy_amt), 0.0001))"

NU = "SLOW_AND_FAST"

SPECS = [
  # 1. ts_delta 骨架：加外层 ts_mean 平滑（提 F）
  ("D1_smooth", NU, 30, 0.02, [
     ("d1_a", f"group_rank(ts_mean(ts_delta(ts_zscore({RS}, 504), 10), 5), sector)"),
     ("d1_b", f"group_rank(ts_mean(ts_delta(ts_zscore({RS}, 504), 10), 20), sector)"),
  ]),
  # 2. ts_delta 窗变体
  ("D2_win", NU, 30, 0.02, [
     ("d2_a", f"group_rank(ts_delta(ts_zscore({RS}, 1260), 10), sector)"),
     ("d2_b", f"group_rank(ts_delta(ts_zscore({RS}, 504), 5), sector)"),
  ]),
  # 3. ts_delta + signed_power（压尾提 F）
  ("D3_pow", NU, 30, 0.02, [
     ("d3_a", f"group_rank(signed_power(ts_delta(ts_zscore({RS}, 504), 10), 0.5), sector)"),
     ("d3_b", f"group_rank(ts_delta(ts_zscore({RA}, 504), 10), sector)"),
  ]),
  # 4. 换轴版本
  ("D4_axis", NU, 30, 0.02, [
     ("d4_a", f"group_rank(ts_delta(ts_zscore({RS}, 504), 10), industry)"),
     ("d4_b", f"group_rank(ts_delta(ts_zscore({RS}, 504), 10), subindustry)"),
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
    with open(os.path.join(REPO,"tracking/KOR/candidates/wave_SI10_submitted.json"),"w",encoding="utf-8") as f:
        json.dump(out,f,ensure_ascii=False,indent=1)
    print("SAVED wave_SI10_submitted.json")
asyncio.run(main())
