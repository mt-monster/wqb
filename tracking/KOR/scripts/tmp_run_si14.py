# -*- coding: utf-8 -*-
"""SI14 —— 跨「信号概念」扩池（Mode B：换信号概念，非换分组轴）。

池内已有概念：
  C1 违规卖空比 vec_sum/v… : invactsell/invactbuy  [KPNo2lgl, omLjG1M5]
  C2 违规卖空比 vec_avg    : 同上变体             [mLmGQEq9 等]
  C3 违规卖空比 + dl500/750 + industry/subindustry [JjNAkqbn, A1Np5AXd, QPbxpJ8K]

本波 = 换「信号概念」（用同一数据类型的不同字段）：
  S1 真卖空强度   : short_sell_amt 相对总额占比 / 其变化
  S2 净买压反转   : invactnet_buy_amt 取负（净买入高 → 未来跌）
  S3 量价背离     : sell_qty/buy_qty 与 amt 比值的差
  S4 卖空权重     : amt_wgt（成交额权重，已归一化）水平/趋势
全部 SLOW_AND_FAST + trunc0.02 + hump，分组轴取已验证的 industry/subindustry。
"""
import asyncio, json, sys, os, time
REPO = r"D:\coding\traeCN_project\wqb"
sys.path.insert(0, os.path.join(REPO, "world-quant-brain-mcp"))

NU = "SLOW_AND_FAST"

# 概念腿定义（每组 2 条：不同分组轴）
SPECS = [
    # S1 真卖空强度
    ("S1_realshort", NU, 30, 0.02, [
        ("s1_a", "hump(group_rank(ts_decay_linear(divide(vec_sum(shrt38_stk_short_sellshort_sell_amt), add(vec_sum(shrt38_stk_invactsell_amt), vec_sum(shrt38_stk_invactbuy_amt))), 500), industry), hump=0.0025)"),
        ("s1_b", "hump(group_rank(ts_decay_linear(vec_sum(shrt38_stk_short_sellshort_sell_qty), 500), subindustry), hump=0.0025)"),
    ]),
    # S2 净买压反转
    ("S2_netbuy", NU, 30, 0.02, [
        ("s2_a", "hump(group_rank(ts_decay_linear(divide(vec_sum(shrt38_stk_invactnet_buy_amt), add(vec_sum(shrt38_stk_invactsell_amt), vec_sum(shrt38_stk_invactbuy_amt))), 500), industry), hump=0.0025)"),
        ("s2_b", "hump(group_rank(ts_decay_linear(divide(vec_sum(shrt38_stk_invactnet_buy_qty), add(vec_sum(shrt38_stk_invactsell_qty), vec_sum(shrt38_stk_invactbuy_qty))), 500), subindustry), hump=0.0025)"),
    ]),
    # S3 量价背离（qty 比值 - amt 比值）
    ("S3_qtyamt", NU, 30, 0.02, [
        ("s3_a", "hump(group_rank(ts_decay_linear(subtract(divide(vec_sum(shrt38_stk_invactsell_qty), vec_sum(shrt38_stk_invactbuy_qty)), divide(vec_sum(shrt38_stk_invactsell_amt), vec_sum(shrt38_stk_invactbuy_amt))), 500), industry), hump=0.0025)"),
        ("s3_b", "hump(group_rank(ts_decay_linear(subtract(divide(vec_sum(shrt38_stk_invactsell_qty), vec_sum(shrt38_stk_invactbuy_qty)), divide(vec_sum(shrt38_stk_invactsell_amt), vec_sum(shrt38_stk_invactbuy_amt))), 750), subindustry), hump=0.0025)"),
    ]),
    # S4 卖空成交额权重（已归一化）
    ("S4_amt_wgt", NU, 30, 0.02, [
        ("s4_a", "hump(group_rank(ts_decay_linear(vec_avg(shrt38_stk_short_sellshort_sell_amt_wgt), 500), industry), hump=0.0025)"),
        ("s4_b", "hump(group_rank(ts_decay_linear(vec_avg(shrt38_amt_wgt), 500), subindustry), hump=0.0025)"),
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
    p = os.path.join(REPO, "tracking/KOR/candidates/wave_SI14_submitted.json")
    with open(p, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print("SAVED", p)

asyncio.run(main())
