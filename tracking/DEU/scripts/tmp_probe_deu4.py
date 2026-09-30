"""DEU SI3 第四轮：取反 + 换轴（信号方向修正）。"""
import asyncio, json, sys, os
REPO = r"D:\coding\traeCN_project\wqb"
sys.path.insert(0, os.path.join(REPO, "world-quant-brain-mcp"))

C = [
    ("n1_mv_share_inv", "hump(group_rank(ts_decay_linear(multiply(-1, divide(vec_sum(loaned_market_value_usd_p5_d1), add(vec_sum(loaned_share_count_p5_d1),0.0001))), 500), subindustry), hump=0.0025)"),
    ("n2_bar_inv", "hump(group_rank(ts_decay_linear(multiply(-1, vec_avg(shrt3_bar)), 250), industry), hump=0.0025)"),
    ("n3_ratevol_inv", "hump(group_rank(ts_decay_linear(multiply(-1, vec_avg(loan_rate_volatility_p5_d1)), 500), subindustry), hump=0.0025)"),
    ("n4_mv_share_ind", "hump(group_rank(ts_decay_linear(multiply(-1, divide(vec_sum(loaned_market_value_usd_p5_d1), add(vec_sum(loaned_share_count_p5_d1),0.0001))), 500), industry), hump=0.0025)"),
    ("n5_rate_max_mean_inv", "hump(group_rank(ts_decay_linear(multiply(-1, divide(vec_sum(max_loan_rate_p5_d1), add(vec_sum(mean_loan_rate_p5_d1),0.0001))), 500), subindustry), hump=0.0025)"),
    ("n6_bar_inv_long", "hump(group_rank(ts_decay_linear(multiply(-1, vec_avg(shrt3_bar)), 500), subindustry), hump=0.0025)"),
]

async def main():
    from brain_api import brain_client
    from tools_sim import create_multi_simulation
    await brain_client.ensure_authenticated()
    r = await create_multi_simulation([c[1] for c in C], region="DEU", universe="TOP500", delay=1,
        decay=30, neutralization="SLOW_AND_FAST", truncation=0.02, nan_handling="ON", test_period="P0Y0M")
    pid = r.get("multisimulation_id") or (r.get("location") or "").rstrip("/").split("/")[-1]
    print("pid", pid)
    for i in range(15):
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
                    print(f"    {C[j][0]}: {aid} S={is_.get('sharpe')} F={is_.get('fitness')} T={is_.get('turnover')}")
                else:
                    print(f"    {C[j][0]}: {dd.get('status')} {str(dd.get('message'))[:90]}")
            break
asyncio.run(main())
