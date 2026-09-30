# -*- coding: utf-8 -*-
"""SI17 —— 深挖 subindustry 轴 + 探索更细分组/混合结构。

SI15 结论：subindustry 轴 prod 0.56-0.58（最优），industry 0.69。
本波：
  H1 更细分组（如果 KOR 支持更细）+ subindustry 轴上换窗口
  H2 vec_avg 版本 + subindustry（族A 与族C 交叉）
  H3 subtract 净额差版本 + subindustry（曾 prod 0.87 在 sector，试换轴）
  H4 winsorize/ts_backfill 预处理 + subindustry
"""
import asyncio, json, sys, os, time
REPO = r"D:\coding\traeCN_project\wqb"
sys.path.insert(0, os.path.join(REPO, "world-quant-brain-mcp"))

SELL = "shrt38_stk_invactsell_amt"
BUY = "shrt38_stk_invactbuy_amt"
RS = f"divide(vec_sum({SELL}), vec_sum({BUY}))"
RA = f"divide(vec_avg({SELL}), add(vec_avg({BUY}), 0.0001))"
NET = f"divide(subtract(vec_sum({SELL}), vec_sum({BUY})), add(vec_sum({SELL}), vec_sum({BUY})))"
NU = "SLOW_AND_FAST"

SPECS = [
    ("H1_sub_win", NU, 30, 0.02, [
        ("h1_a", f"hump(group_rank(ts_decay_linear({RS}, 300), subindustry), hump=0.0025)"),
        ("h1_b", f"hump(group_rank(ts_decay_linear({RS}, 1260), subindustry), hump=0.0025)"),
    ]),
    ("H2_avg_sub", NU, 30, 0.02, [
        ("h2_a", f"hump(group_rank(ts_decay_linear({RA}, 500), subindustry), hump=0.0025)"),
        ("h2_b", f"hump(group_rank(ts_decay_linear({RA}, 500), industry), hump=0.0025)"),
    ]),
    ("H3_net_sub", NU, 30, 0.02, [
        ("h3_a", f"hump(group_rank(ts_decay_linear({NET}, 500), subindustry), hump=0.0025)"),
        ("h3_b", f"hump(group_rank(ts_decay_linear({NET}, 500), industry), hump=0.0025)"),
    ]),
    ("H4_preproc", NU, 30, 0.02, [
        ("h4_a", f"hump(group_rank(winsorize(ts_backfill(ts_decay_linear({RS}, 500), 20), std=4), subindustry), hump=0.0025)"),
        ("h4_b", f"hump(group_rank(ts_decay_linear({RS}, 500), subindustry), hump=0.002)"),
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
            print(f"{gname} ERR: {json.dumps(r,ensure_ascii=False)[:250]}"); continue
        pid = r.get("multisimulation_id") or (r.get("location") or "").rstrip("/").split("/")[-1]
        print(f"{gname} pid={pid}")
        out["batches"].append({"group": gname, "nu": nu, "decay": dec, "trunc": trunc,
                               "progress_id": pid, "ids": [it[0] for it in items]})
        await asyncio.sleep(1)
    p = os.path.join(REPO, "tracking/KOR/candidates/wave_SI17_submitted.json")
    with open(p, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print("SAVED", p)

asyncio.run(main())
