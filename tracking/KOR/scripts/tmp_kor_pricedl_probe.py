# -*- coding: utf-8 -*-
"""KOR price_signal_dl probe（28 MATRIX 趋势/量指标，cov 0.95-0.99，零竞争）。

设置：KOR/TOP600/D1/SLOW_AND_FAST/decay30/trunc0.02（KOR 已验证配方）
结构：趋势指标反转 / 量价背离 / 趋势-量比值
"""
import asyncio, json, sys, os
REPO = r"D:\coding\traeCN_project\wqb"
sys.path.insert(0, os.path.join(REPO, "world-quant-brain-mcp"))

T = "normalized_trend_indicator_%d"
V = "normalized_volume_indicator_%d"

C = [
    # 多趋势指标平均（趋势共振）
    ("t1_trend_avg_rev", "hump(group_rank(ts_decay_linear(multiply(-1, add(add(" + T % 0 + f", {T % 1}), {T % 2})), 250), subindustry), hump=0.0025)"),
    # 趋势-量比值（背离）
    ("t2_trend_vol_ratio", f"hump(group_rank(ts_decay_linear(divide({T % 0}, add({V % 0}, 0.0001)), 250), subindustry), hump=0.0025)"),
    # 趋势指标变化率（动量）
    ("t3_trend_delta", f"hump(group_rank(ts_delta({T % 3}, 20), subindustry), hump=0.0025)"),
    # 趋势指标时序排名
    ("t4_trend_rank", f"hump(group_rank(ts_rank({T % 0}, 250), industry), hump=0.0025)"),
    # 量指标反转
    ("t5_vol_rev", f"hump(group_rank(ts_decay_linear(multiply(-1, {V % 0}), 250), subindustry), hump=0.0025)"),
    # 原始趋势 vs 归一化趋势（比值 = 波动率代理）
    ("t6_raw_norm_ratio", f"hump(group_rank(ts_decay_linear(divide(raw_trend_indicator_0, add({T % 0}, 0.0001)), 250), subindustry), hump=0.0025)"),
    # 趋势分散度（多指标 std）
    ("t7_trend_std", f"hump(group_rank(ts_decay_linear(multiply(-1, ts_std_dev({T % 0}, 60)), 20), subindustry), hump=0.0025)"),
    # 量价协同（trend × volume 同号）
    ("t8_tv_sync", f"hump(group_rank(ts_decay_linear(multiply({T % 0}, {V % 0}), 250), industry), hump=0.0025)"),
]


async def main():
    from brain_api import brain_client
    from tools_sim import create_multi_simulation
    await brain_client.ensure_authenticated()
    r = await create_multi_simulation([c[1] for c in C], region="KOR", universe="TOP600", delay=1,
        decay=30, neutralization="SLOW_AND_FAST", truncation=0.02, nan_handling="ON", test_period="P0Y0M")
    if isinstance(r, dict) and r.get("error"):
        print("ERR", json.dumps(r, ensure_ascii=False)[:300]); return
    pid = r.get("multisimulation_id") or (r.get("location") or "").rstrip("/").split("/")[-1]
    print("pid", pid)
    for i in range(20):
        await asyncio.sleep(20)
        rr = await brain_client._request("GET", f"https://api.worldquantbrain.com/simulations/{pid}")
        d = rr.json()
        print(f"  [{i*20}s] {d.get('status')} children={len(d.get('children') or [])}", flush=True)
        if d.get("status") in ("COMPLETE", "ERROR"):
            for j, ch in enumerate(d.get("children") or []):
                r2 = await brain_client._request("GET", f"https://api.worldquantbrain.com/simulations/{ch}")
                dd = r2.json(); aid = dd.get("alpha")
                if aid:
                    r3 = await brain_client._request("GET", f"https://api.worldquantbrain.com/alphas/{aid}")
                    a = r3.json(); is_ = a.get("is") or {}
                    print(f"    {C[j][0]}: {aid} S={is_.get('sharpe')} F={is_.get('fitness')} T={is_.get('turnover')}")
                else:
                    print(f"    {C[j][0]}: {dd.get('status')} {str(dd.get('message'))[:90]}")
            break
asyncio.run(main())
