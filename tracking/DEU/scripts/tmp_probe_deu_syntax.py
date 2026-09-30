"""验证 DEU SI3 VECTOR 字段的正确时序算子用法（快速单模拟探测）。"""
import asyncio, json, sys, os
REPO = r"D:\coding\traeCN_project\wqb"
sys.path.insert(0, os.path.join(REPO, "world-quant-brain-mcp"))

CANDIDATES = [
    ("A_vecavg_plain", "ts_rank(vec_avg(shrt3_bar), 250)"),
    ("B_vecavg_backfill", "ts_delta(ts_backfill(vec_avg(shrt3_bar), 20), 20)"),
    ("C_vecsum_ratio", "ts_rank(divide(vec_sum(loaned_market_value_usd), add(vec_sum(loaned_share_count), 0.0001)), 250)"),
    ("D_bar_direct_rank", "ts_rank(shrt3_bar, 250)"),
]

async def main():
    from brain_api import brain_client
    from tools_sim import create_multi_simulation
    await brain_client.ensure_authenticated()
    r = await create_multi_simulation([c[1] for c in CANDIDATES], region="DEU", universe="TOP500", delay=1,
        decay=30, neutralization="SLOW_AND_FAST", truncation=0.02, nan_handling="ON", test_period="P0Y0M")
    pid = r.get("multisimulation_id") or (r.get("location") or "").rstrip("/").split("/")[-1]
    print("pid", pid)
    for i in range(12):
        await asyncio.sleep(20)
        rr = await brain_client._request("GET", f"https://api.worldquantbrain.com/simulations/{pid}")
        d = rr.json()
        print(f"  [{i*20}s] {d.get('status')} children={len(d.get('children') or [])}")
        if d.get("status") in ("COMPLETE", "ERROR"):
            for j, ch in enumerate(d.get("children") or []):
                r2 = await brain_client._request("GET", f"https://api.worldquantbrain.com/simulations/{ch}")
                dd = r2.json()
                aid = dd.get("alpha")
                if aid:
                    r3 = await brain_client._request("GET", f"https://api.worldquantbrain.com/alphas/{aid}")
                    is_ = (r3.json().get("is") or {})
                    print(f"    {CANDIDATES[j][0]}: {aid} S={is_.get('sharpe')} F={is_.get('fitness')} T={is_.get('turnover')}")
                else:
                    print(f"    {CANDIDATES[j][0]}: ERR {str(dd.get('error'))[:100]}")
            break
asyncio.run(main())
