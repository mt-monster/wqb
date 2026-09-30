# -*- coding: utf-8 -*-
"""SI13 —— 压 RRbOoMNg 族 prod（0.7682 → <0.7）+ 求更多差异化新腿。

已证：hump 越大 prod 越低（0.001→0.711, 0.0025→0.6675, 0.003→0.5701）。
本波：对 decay_linear 结构加 hump 阶梯 + 换更长归一化窗，找 prod<0.7 且 F≥1.0。
"""
import asyncio, json, sys, os, time
REPO = r"D:\coding\traeCN_project\wqb"
sys.path.insert(0, os.path.join(REPO, "world-quant-brain-mcp"))

SELL = "shrt38_stk_invactsell_amt"
BUY = "shrt38_stk_invactbuy_amt"
RS = f"divide(vec_sum({SELL}), vec_sum({BUY}))"
NU = "SLOW_AND_FAST"

SPECS = [
    # P1: decay_linear 结构 + hump 阶梯（RRbOoMNg 是 250/sector，无 hump → prod 0.7682）
    ("P1_dl_hump", NU, 30, 0.02, [
        ("p1_a", f"hump(group_rank(ts_decay_linear({RS}, 250), sector), hump=0.003)"),
        ("p1_b", f"hump(group_rank(ts_decay_linear({RS}, 250), sector), hump=0.004)"),
    ]),
    # P2: 更长衰减窗（解耦更强）+ hump
    ("P2_dl_long", NU, 30, 0.02, [
        ("p2_a", f"hump(group_rank(ts_decay_linear({RS}, 750), industry), hump=0.003)"),
        ("p2_b", f"hump(group_rank(ts_decay_linear({RS}, 1000), sector), hump=0.003)"),
    ]),
    # P3: JjNAkqbn（prod 0.6958）的结构再分化 —— 换轴 + 换窗
    ("P3_dl_axes", NU, 30, 0.02, [
        ("p3_a", f"hump(group_rank(ts_decay_linear({RS}, 500), subindustry), hump=0.0025)"),
        ("p3_b", f"hump(group_rank(ts_decay_linear({RS}, 630), sector), hump=0.0025)"),
    ]),
    # P4: ts_mean 长窗平滑（与 decay_linear 不同的时序加权）
    ("P4_tsmean", NU, 30, 0.02, [
        ("p4_a", f"hump(group_rank(ts_mean(ts_zscore({RS}, 1000), 5), industry), hump=0.003)"),
        ("p4_b", f"hump(group_rank(ts_mean(ts_rank({RS}, 1000), 5), sector), hump=0.003)"),
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
    p = os.path.join(REPO, "tracking/KOR/candidates/wave_SI13_submitted.json")
    with open(p, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print("SAVED", p)

asyncio.run(main())
