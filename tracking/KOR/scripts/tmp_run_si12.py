# -*- coding: utf-8 -*-
"""SI12 —— 结构差异化补池（为明日 REGULAR 名额准备第 5 颗）。

池内已有结构：
  A) ts_mean(ts_zscore(vec_sum比值,1260),5)  [omLjG1M5 ACTIVE]
  B) hump(group_rank(vec_sum比值))           [KPNo2lgl ACTIVE]
  C) hump(group_rank(vec_avg比值))           [x3 同族待提]

本波目标 = 换「数学结构」而非换分组轴：
  N1 ts_decay_linear(长窗)  —— 时序衰减平滑，与 A 的 zscore 不同源
  N2 ts_rank(短窗)          —— 秩变换，分布无关
  N3 ratio 取「净额差」而非比值 —— subtract 结构，经济含义=净卖空额
  N4 ts_delta 比值          —— 变化率
全部 SLOW_AND_FAST + trunc0.02 + hump 压 prod。
"""
import asyncio, json, sys, os, time
REPO = r"D:\coding\traeCN_project\wqb"
sys.path.insert(0, os.path.join(REPO, "world-quant-brain-mcp"))

SELL = "shrt38_stk_invactsell_amt"
BUY = "shrt38_stk_invactbuy_amt"
NU = "SLOW_AND_FAST"

SPECS = [
    ("N1_decaylin", NU, 30, 0.02, [
        ("n1_a", f"hump(group_rank(ts_decay_linear(divide(vec_sum({SELL}), vec_sum({BUY})), 250), sector), hump=0.0025)"),
        ("n1_b", f"hump(group_rank(ts_decay_linear(divide(vec_sum({SELL}), vec_sum({BUY})), 500), industry), hump=0.0025)"),
    ]),
    ("N2_tsrank", NU, 30, 0.02, [
        ("n2_a", f"hump(group_rank(ts_rank(divide(vec_sum({SELL}), vec_sum({BUY})), 250), sector), hump=0.003)"),
        ("n2_b", f"hump(group_rank(ts_rank(divide(vec_sum({SELL}), vec_sum({BUY})), 500), industry), hump=0.003)"),
    ]),
    ("N3_netsub", NU, 30, 0.02, [
        ("n3_a", f"hump(group_rank(divide(subtract(vec_sum({SELL}), vec_sum({BUY})), add(vec_sum({SELL}), vec_sum({BUY}))), sector), hump=0.0025)"),
        ("n3_b", f"hump(group_rank(divide(subtract(vec_sum({SELL}), vec_sum({BUY})), add(vec_sum({SELL}), vec_sum({BUY}))), industry), hump=0.003)"),
    ]),
    ("N4_delta", NU, 30, 0.02, [
        ("n4_a", f"hump(group_rank(ts_delta(divide(vec_sum({SELL}), vec_sum({BUY})), 60), sector), hump=0.003)"),
        ("n4_b", f"hump(group_rank(ts_delta(divide(vec_sum({SELL}), vec_sum({BUY})), 120), industry), hump=0.003)"),
    ]),
]

async def main():
    from brain_api import brain_client
    from tools_sim import create_multi_simulation
    await brain_client.ensure_authenticated()
    out = {"submitted_at": time.strftime("%Y-%m-%d %H:%M:%S"), "batches": []}
    for gname, nu, dec, trunc, items in SPECS:
        r = await create_multi_simulation([it[1] for it in items], region="KOR", universe="TOP600", delay=1,
                decay=dec, neutralization=nu, truncation=trunc, nan_handling="ON", test_period="P0Y0M")
        if isinstance(r, dict) and r.get("error"):
            print(f"{gname} ERR: {json.dumps(r,ensure_ascii=False)[:200]}"); continue
        pid = r.get("multisimulation_id") or (r.get("location") or "").rstrip("/").split("/")[-1]
        print(f"{gname} pid={pid}")
        out["batches"].append({"group": gname, "nu": nu, "decay": dec, "trunc": trunc,
                               "progress_id": pid, "ids": [it[0] for it in items]})
        await asyncio.sleep(1)
    p = os.path.join(REPO, "tracking/KOR/candidates/wave_SI12_submitted.json")
    with open(p, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print("SAVED", p)

asyncio.run(main())
