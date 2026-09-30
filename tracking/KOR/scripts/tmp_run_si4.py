# -*- coding: utf-8 -*-
"""SI4 —— 模仿 omLjG1M5(ACTIVE) 的成功结构，叠 hump 降 prod。

omLjG1M5 成功结构: group_rank(ts_mean(ts_zscore(divide(vec_sum(sell), vec_sum(buy)), 1260), 5), sector)
目标：命中 D1 Power Pool Oct'26 且拿到 POWER_POOL_ELIGIBLE + REGULAR:REGULAR 双分类。
"""
import asyncio, json, sys, os, time
REPO = r"D:\coding\traeCN_project\wqb"
sys.path.insert(0, os.path.join(REPO, "world-quant-brain-mcp"))

RS = "divide(vec_sum(shrt38_stk_invactsell_amt), vec_sum(shrt38_stk_invactbuy_amt))"
RA = "divide(vec_avg(shrt38_stk_invactsell_amt), add(vec_avg(shrt38_stk_invactbuy_amt), 0.0001))"

SPECS = [
  # 组1: omLjG1M5 精确结构 + hump 外套（降 prod）
  ("G1_omlj_hump", "SUBINDUSTRY", 4, 0.08, "G1", [
     ("g1_a", f"hump(group_rank(ts_mean(ts_zscore({RS}, 1260), 5), sector), hump=0.002)"),
     ("g1_b", f"hump(group_rank(ts_mean(ts_zscore({RS}, 1260), 5), sector), hump=0.003)"),
  ]),
  # 组2: omLjG1M5 精确结构（无 hump）→ 基线，验证分类是否出现
  ("G2_omlj_base", "SUBINDUSTRY", 4, 0.08, "G2", [
     ("g2_a", f"group_rank(ts_mean(ts_zscore({RS}, 1260), 5), sector)"),
     ("g2_b", f"hump(group_rank(ts_mean(ts_zscore({RA}, 1260), 5), sector), hump=0.004)"),
  ]),
  # 组3: 我们的腿 + ts_zscore 长窗平滑（补上缺失的"平滑"要素）
  ("G3_smooth", "SUBINDUSTRY", 4, 0.08, "G3", [
     ("g3_a", f"hump(group_rank(ts_zscore({RA}, 1260), subindustry), hump=0.003)"),
     ("g3_b", f"group_rank(ts_zscore({RA}, 1260), subindustry)"),
  ]),
  # 组4: hump 在外层 + sector 轴（换轴看主题匹配）
  ("G4_sector", "SUBINDUSTRY", 4, 0.08, "G4", [
     ("g4_a", f"hump(group_rank({RA}, sector), hump=0.003)"),
     ("g4_b", f"hump(group_rank({RA}, industry), hump=0.003)"),
  ]),
]

async def main():
    from brain_api import brain_client
    from tools_sim import create_multi_simulation
    await brain_client.ensure_authenticated()
    out={"submitted_at": time.strftime("%Y-%m-%d %H:%M:%S"), "batches": []}
    for gname, nu, dec, trunc, tag, items in SPECS:
        r = await create_multi_simulation([it[1] for it in items], region="KOR", universe="TOP600", delay=1,
                decay=dec, neutralization=nu, truncation=trunc, nan_handling="ON", test_period="P0Y0M")
        if isinstance(r, dict) and r.get("error"):
            print(f"{gname} GATE-REJECT: {json.dumps(r.get('failed_expressions',{}),ensure_ascii=False)[:300]}")
            continue
        pid = r.get("multisimulation_id") or (r.get("location") or "").rstrip("/").split("/")[-1]
        print(f"{gname} pid={pid} n={len(items)}")
        out["batches"].append({"group":gname,"nu":nu,"decay":dec,"trunc":trunc,"progress_id":pid,"ids":[it[0] for it in items]})
        await asyncio.sleep(1)
    with open(os.path.join(REPO,"tracking/KOR/candidates/wave_SI4_submitted.json"),"w",encoding="utf-8") as f:
        json.dump(out,f,ensure_ascii=False,indent=1)
    print("SAVED wave_SI4_submitted.json")
asyncio.run(main())
