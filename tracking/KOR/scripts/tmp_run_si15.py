# -*- coding: utf-8 -*-
"""SI15 —— 已验证配方（dl + industry/subindustry）的窗口网格细分。

已知：RS=invactsell/invactbuy, dl500+industry → 0.6958；dl500+subindustry → 0.5753；dl750+industry → 0.6918。
本波填网格：dl{400,600,900} × {industry, subindustry} + 不同 hump，找 prod 更低/IS 更强的点。
"""
import asyncio, json, sys, os, time
REPO = r"D:\coding\traeCN_project\wqb"
sys.path.insert(0, os.path.join(REPO, "world-quant-brain-mcp"))

SELL = "shrt38_stk_invactsell_amt"
BUY = "shrt38_stk_invactbuy_amt"
RS = f"divide(vec_sum({SELL}), vec_sum({BUY}))"
NU = "SLOW_AND_FAST"

SPECS = [
    ("G1_dl400", NU, 30, 0.02, [
        ("g1_a", f"hump(group_rank(ts_decay_linear({RS}, 400), industry), hump=0.0025)"),
        ("g1_b", f"hump(group_rank(ts_decay_linear({RS}, 400), subindustry), hump=0.0025)"),
    ]),
    ("G2_dl600", NU, 30, 0.02, [
        ("g2_a", f"hump(group_rank(ts_decay_linear({RS}, 600), industry), hump=0.0025)"),
        ("g2_b", f"hump(group_rank(ts_decay_linear({RS}, 600), subindustry), hump=0.0025)"),
    ]),
    ("G3_dl900", NU, 30, 0.02, [
        ("g3_a", f"hump(group_rank(ts_decay_linear({RS}, 900), industry), hump=0.0025)"),
        ("g3_b", f"hump(group_rank(ts_decay_linear({RS}, 900), subindustry), hump=0.0025)"),
    ]),
    ("G4_humpvar", NU, 30, 0.02, [
        ("g4_a", f"hump(group_rank(ts_decay_linear({RS}, 500), subindustry), hump=0.003)"),
        ("g4_b", f"hump(group_rank(ts_decay_linear({RS}, 500), subindustry), hump=0.002)"),
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
    p = os.path.join(REPO, "tracking/KOR/candidates/wave_SI15_submitted.json")
    with open(p, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print("SAVED", p)

asyncio.run(main())
