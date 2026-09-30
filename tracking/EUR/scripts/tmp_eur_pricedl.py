"""EUR price_signal_dl probe（同 KOR 表达式跨区域复用）。"""
import asyncio, json, sys, os
REPO = r"D:\coding\traeCN_project\wqb"
sys.path.insert(0, os.path.join(REPO, "world-quant-brain-mcp"))
T="normalized_trend_indicator_%d"; V="normalized_volume_indicator_%d"
C = [
    ("T_trend_sum", f"hump(group_rank(ts_decay_linear(add(add({T%0},{T%1}),{T%2}), 250), subindustry), hump=0.0025)"),
    ("T_trend_sum_ind", f"hump(group_rank(ts_decay_linear(add(add({T%0},{T%1}),{T%2}), 250), industry), hump=0.0025)"),
    ("T_tr0_decay", f"hump(group_rank(ts_decay_linear({T%0}, 250), subindustry), hump=0.0025)"),
    ("T_tr0_rank", f"hump(group_rank(ts_rank({T%0}, 250), subindustry), hump=0.0025)"),
    ("T_tr_delta", f"hump(group_rank(ts_delta({T%3}, 20), subindustry), hump=0.0025)"),
    ("T_tv_ratio", f"hump(group_rank(ts_decay_linear(divide({T%0}, add({V%0},0.0001)), 250), subindustry), hump=0.0025)"),
    ("T_vol_rev", f"hump(group_rank(ts_decay_linear(multiply(-1,{V%0}), 250), subindustry), hump=0.0025)"),
    ("T_trendsum_d10", f"hump(group_rank(ts_decay_linear(add(add({T%0},{T%1}),{T%2}), 10), subindustry), hump=0.0025)"),
]
async def main():
    from brain_api import brain_client
    from tools_sim import create_multi_simulation
    await brain_client.ensure_authenticated()
    r = await create_multi_simulation([c[1] for c in C], region="EUR", universe="TOPCS1600", delay=1,
        decay=30, neutralization="SUBINDUSTRY", truncation=0.02, nan_handling="ON", test_period="P0Y0M")
    if isinstance(r, dict) and r.get("error"):
        print("ERR", json.dumps(r, ensure_ascii=False)[:250]); return
    pid = r.get("multisimulation_id") or (r.get("location") or "").rstrip("/").split("/")[-1]
    print("pid", pid)
    for i in range(20):
        await asyncio.sleep(20)
        rr = await brain_client._request("GET", f"https://api.worldquantbrain.com/simulations/{pid}")
        d = rr.json()
        print(f"  [{i*20}s] {d.get('status')} children={len(d.get('children') or [])}", flush=True)
        if d.get("status") in ("COMPLETE","ERROR"):
            for j, ch in enumerate(d.get("children") or []):
                r2 = await brain_client._request("GET", f"https://api.worldquantbrain.com/simulations/{ch}")
                dd = r2.json(); aid = dd.get("alpha")
                if aid:
                    r3 = await brain_client._request("GET", f"https://api.worldquantbrain.com/alphas/{aid}")
                    a=r3.json(); is_=a.get("is") or {}
                    print(f"    {C[j][0]}: {aid} S={is_.get('sharpe')} F={is_.get('fitness')} T={is_.get('turnover')}")
                else:
                    print(f"    {C[j][0]}: {dd.get('status')} {str(dd.get('message'))[:80]}")
            break
asyncio.run(main())
