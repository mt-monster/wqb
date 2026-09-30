# -*- coding: utf-8 -*-
"""SI9 —— SLOW_AND_FAST 下换信号概念（拉开与 omLjG1M5 的 prod）。

已证：SLOW_AND_FAST + decay20~30 + trunc0.02 → PURE_POWER_POOL_THEME 消失 ✓
问题：同族腿 prod 0.92+（omLjG1M5 兄弟）→ 必须换字段/换概念。
"""
import asyncio, json, sys, os, time
REPO = r"D:\coding\traeCN_project\wqb"
sys.path.insert(0, os.path.join(REPO, "world-quant-brain-mcp"))

SELL = "shrt38_stk_invactsell_amt"
BUY = "shrt38_stk_invactbuy_amt"
RS = f"divide(vec_sum({SELL}), vec_sum({BUY}))"
RA = f"divide(vec_avg({SELL}), add(vec_avg({BUY}), 0.0001))"

NU = "SLOW_AND_FAST"

SPECS = [
  # A. 换信号：买卖差（而非比）
  ("T1_diff", NU, 20, 0.02, [
     ("t1_a", f"group_rank(ts_mean(ts_zscore(subtract(vec_sum({SELL}), vec_sum({BUY})), 1260), 5), sector)"),
     ("t1_b", f"group_rank(ts_mean(ts_zscore(subtract(vec_avg({SELL}), vec_avg({BUY})), 1260), 5), sector)"),
  ]),
  # B. 换信号：卖空占比（归一化到总量）
  ("T2_share", NU, 20, 0.02, [
     ("t2_a", f"group_rank(ts_mean(ts_zscore(divide(vec_sum({SELL}), add(vec_sum({SELL}), vec_sum({BUY}))), 1260), 5), sector)"),
     ("t2_b", f"group_rank(ts_mean(ts_zscore(divide(vec_avg({SELL}), add(vec_avg({SELL}), vec_avg({BUY}))), 1260), 5), industry)"),
  ]),
  # C. 换结构：ts_delta / ts_rank 替代 zscore
  ("T3_alt", NU, 30, 0.02, [
     ("t3_a", f"group_rank(ts_mean(ts_rank({RS}, 1260), 5), sector)"),
     ("t3_b", f"group_rank(ts_delta(ts_zscore({RS}, 504), 10), sector)"),
  ]),
  # D. 换轴+换窗
  ("T4_mix", NU, 20, 0.02, [
     ("t4_a", f"group_rank(ts_mean(ts_zscore({RS}, 750), 5), industry)"),
     ("t4_b", f"group_rank(ts_mean(ts_zscore({RA}, 900), 5), subindustry)"),
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
        print(f"{gname} nu={nu} decay={dec} pid={pid}")
        out["batches"].append({"group":gname,"nu":nu,"decay":dec,"trunc":trunc,"progress_id":pid,"ids":[it[0] for it in items]})
        await asyncio.sleep(1)
    with open(os.path.join(REPO,"tracking/KOR/candidates/wave_SI9_submitted.json"),"w",encoding="utf-8") as f:
        json.dump(out,f,ensure_ascii=False,indent=1)
    print("SAVED wave_SI9_submitted.json")
asyncio.run(main())
