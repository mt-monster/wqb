# -*- coding: utf-8 -*-
"""SI16 —— S2 净买压「取反」验证（SI14 发现 S=-2.05，取反即 +2.05）。

经济含义：违规净买入额占比高 = 非理性/散户净买入集中 → 未来跑输（反向指标）。
取反后应得强正 Sharpe。同时试不同的负号位置与分组轴。
"""
import asyncio, json, sys, os, time
REPO = r"D:\coding\traeCN_project\wqb"
sys.path.insert(0, os.path.join(REPO, "world-quant-brain-mcp"))

NETA = "shrt38_stk_invactnet_buy_amt"
SEL = "shrt38_stk_invactsell_amt"
BUY = "shrt38_stk_invactbuy_amt"
NU = "SLOW_AND_FAST"

# 用 group_rank 后取负，或直接对信号取负再 rank —— 两种写法都试
SPECS = [
    ("R1_negrank", NU, 30, 0.02, [
        ("r1_a", f"hump(multiply(-1, group_rank(ts_decay_linear(divide(vec_sum({NETA}), add(vec_sum({SEL}), vec_sum({BUY}))), 500), industry)), hump=0.0025)"),
        ("r1_b", f"hump(multiply(-1, group_rank(ts_decay_linear(divide(vec_sum({NETA}), add(vec_sum({SEL}), vec_sum({BUY}))), 500), subindustry)), hump=0.0025)"),
    ]),
    ("R2_negrank750", NU, 30, 0.02, [
        ("r2_a", f"hump(multiply(-1, group_rank(ts_decay_linear(divide(vec_sum({NETA}), add(vec_sum({SEL}), vec_sum({BUY}))), 750), industry)), hump=0.0025)"),
        ("r2_b", f"hump(multiply(-1, group_rank(ts_decay_linear(divide(vec_sum({NETA}), add(vec_sum({SEL}), vec_sum({BUY}))), 250), subindustry)), hump=0.0025)"),
    ]),
    # 直接 rank 后 1-x 的等价写法，与 multiply(-1) 对照（部分场景 rank 域更稳）
    ("R3_oneMinus", NU, 30, 0.02, [
        ("r3_a", f"hump(subtract(1, group_rank(ts_decay_linear(divide(vec_sum({NETA}), add(vec_sum({SEL}), vec_sum({BUY}))), 500), industry)), hump=0.0025)"),
        ("r3_b", f"hump(subtract(0.5, group_rank(ts_decay_linear(divide(vec_sum({NETA}), add(vec_sum({SEL}), vec_sum({BUY}))), 500), subindustry)), hump=0.0025)"),
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
    p = os.path.join(REPO, "tracking/KOR/candidates/wave_SI16_submitted.json")
    with open(p, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print("SAVED", p)

asyncio.run(main())
