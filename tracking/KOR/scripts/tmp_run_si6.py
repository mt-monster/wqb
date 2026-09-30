# -*- coding: utf-8 -*-
"""SI6 —— 对照组：验证 PP 通道触发条件。

假说：POWER_POOL_ELIGIBLE 由「数据集命中 PP 主题」触发；换 nu / 跨数据集可绕开。
对照组设计：
  A. 同表达式（xA3LVkzl）+ 换 nu（STATISTICAL/SECTOR/INDUSTRY/MARKET）
  B. 跨数据集（shrt38 + oth466 基本面/量价）→ 强制非 SINGLE_DATA_SET
  C. ts_delta/ts_rank 长窗替换 hump（不同算子几何）
"""
import asyncio, json, sys, os, time
REPO = r"D:\coding\traeCN_project\wqb"
sys.path.insert(0, os.path.join(REPO, "world-quant-brain-mcp"))

RA = "divide(vec_avg(shrt38_stk_invactsell_amt), add(vec_avg(shrt38_stk_invactbuy_amt), 0.0001))"

SPECS = [
  # A. 同表达式换 nu（分别提交）
  ("A1_nuSTAT", "STATISTICAL", 4, 0.08, [
     ("a1", f"hump(group_rank({RA}, sector), hump=0.003)"),
     ("a2", f"hump(group_rank({RA}, industry), hump=0.003)"),
  ]),
  ("A2_nuSECTOR", "SECTOR", 4, 0.08, [
     ("a3", f"hump(group_rank({RA}, subindustry), hump=0.003)"),
     ("a4", f"hump(group_rank({RA}, sector), hump=0.003)"),
  ]),
  ("A3_nuMARKET", "MARKET", 4, 0.08, [
     ("a5", f"hump(group_rank({RA}, sector), hump=0.003)"),
     ("a6", f"hump(group_rank({RA}, industry), hump=0.003)"),
  ]),
  # B. 跨数据集（非 SINGLE_DATA_SET）→ 用量价+SI 组合
  ("B1_cross", "SUBINDUSTRY", 4, 0.08, [
     ("b1", f"hump(group_rank(add(rank({RA}), rank(divide(close, ts_mean(close, 60)))), sector), hump=0.003)"),
     ("b2", f"hump(group_rank(divide({RA}, add(ts_std_dev(returns, 60), 0.001)), industry), hump=0.003)"),
  ]),
  # C. 非 hump 降 prod（ts_rank 长窗）
  ("C1_tsrank", "SUBINDUSTRY", 4, 0.08, [
     ("c1", f"group_rank(ts_rank({RA}, 252), sector)"),
     ("c2", f"group_rank(ts_rank({RA}, 504), industry)"),
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
            print(f"{gname} GATE-REJECT: {json.dumps(r.get('failed_expressions',{}),ensure_ascii=False)[:250]}")
            continue
        pid = r.get("multisimulation_id") or (r.get("location") or "").rstrip("/").split("/")[-1]
        print(f"{gname} nu={nu} pid={pid} n={len(items)}")
        out["batches"].append({"group":gname,"nu":nu,"decay":dec,"trunc":trunc,"progress_id":pid,"ids":[it[0] for it in items]})
        await asyncio.sleep(1)
    with open(os.path.join(REPO,"tracking/KOR/candidates/wave_SI6_submitted.json"),"w",encoding="utf-8") as f:
        json.dump(out,f,ensure_ascii=False,indent=1)
    print("SAVED wave_SI6_submitted.json")
asyncio.run(main())
