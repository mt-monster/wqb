# -*- coding: utf-8 -*-
"""SI8 —— 复制 omLjG1M5 的成功 settings（SLOW_AND_FAST / decay30 / trunc0.02）。

omLjG1M5 ACTIVE | nu=SLOW_AND_FAST decay=30 trunc=0.02
  expr: group_rank(ts_mean(ts_zscore(divide(vec_sum(sell), vec_sum(buy)), 1260), 5), sector)
本波：同 settings 下换参数/表达式，产出同族第 2、3 颗。
"""
import asyncio, json, sys, os, time
REPO = r"D:\coding\traeCN_project\wqb"
sys.path.insert(0, os.path.join(REPO, "world-quant-brain-mcp"))

RS = "divide(vec_sum(shrt38_stk_invactsell_amt), vec_sum(shrt38_stk_invactbuy_amt))"
RA = "divide(vec_avg(shrt38_stk_invactsell_amt), add(vec_avg(shrt38_stk_invactbuy_amt), 0.0001))"

NU = "SLOW_AND_FAST"
DEC = 30
TRUNC = 0.02

SPECS = [
  ("M1_omlj_clone", NU, DEC, TRUNC, [
     ("m1_a", f"group_rank(ts_mean(ts_zscore({RS}, 1260), 5), sector)"),          # 完全克隆
     ("m1_b", f"group_rank(ts_mean(ts_zscore({RS}, 1008), 5), sector)"),          # 窗 1260→1008
  ]),
  ("M2_wins", NU, DEC, TRUNC, [
     ("m2_a", f"group_rank(ts_mean(ts_zscore({RS}, 1260), 10), sector)"),         # 内层 5→10
     ("m2_b", f"group_rank(ts_mean(ts_zscore({RS}, 1260), 3), industry)"),        # 轴 sector→industry
  ]),
  ("M3_avg", NU, DEC, TRUNC, [
     ("m3_a", f"group_rank(ts_mean(ts_zscore({RA}, 1260), 5), sector)"),          # 换 vec_sum→vec_avg
     ("m3_b", f"group_rank(ts_mean(ts_zscore({RA}, 1500), 5), sector)"),          # 窗 1500
  ]),
  ("M4_dec", NU, 20, TRUNC, [
     ("m4_a", f"group_rank(ts_mean(ts_zscore({RS}, 1260), 5), sector)"),          # decay 30→20
     ("m4_b", f"group_rank(ts_mean(ts_zscore({RS}, 1260), 5), industry)"),        # decay 20 + industry
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
        print(f"{gname} nu={nu} decay={dec} trunc={trunc} pid={pid}")
        out["batches"].append({"group":gname,"nu":nu,"decay":dec,"trunc":trunc,"progress_id":pid,"ids":[it[0] for it in items]})
        await asyncio.sleep(1)
    with open(os.path.join(REPO,"tracking/KOR/candidates/wave_SI8_submitted.json"),"w",encoding="utf-8") as f:
        json.dump(out,f,ensure_ascii=False,indent=1)
    print("SAVED wave_SI8_submitted.json")
asyncio.run(main())
