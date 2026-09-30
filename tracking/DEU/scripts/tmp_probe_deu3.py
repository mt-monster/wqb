"""DEU SI3 定点探测：divide(vec_sum(A),vec_sum(B)) 结构 + 高覆盖字段。"""
import asyncio, json, sys, os
REPO = r"D:\coding\traeCN_project\wqb"
sys.path.insert(0, os.path.join(REPO, "world-quant-brain-mcp"))

# 高覆盖字段（p5_d1 后缀 cov 0.783，_main cov 0.687，裸字段 cov 0.668）
C = [
    ("p1_mv_share_p5", "hump(group_rank(ts_decay_linear(divide(vec_sum(loaned_market_value_usd_p5_d1), add(vec_sum(loaned_share_count_p5_d1),0.0001)), 500), subindustry), hump=0.0025)"),
    ("p2_rate_max_mean_p5", "hump(group_rank(ts_decay_linear(divide(vec_sum(max_loan_rate_p5_d1), add(vec_sum(mean_loan_rate_p5_d1),0.0001)), 500), subindustry), hump=0.0025)"),
    ("p3_cnt_rate_main", "hump(group_rank(ts_decay_linear(divide(vec_sum(transaction_count_main), add(vec_sum(mean_loan_rate_main),0.0001)), 500), industry), hump=0.0025)"),
    ("p4_borrow_bar", "hump(group_rank(ts_decay_linear(vec_avg(shrt3_bar), 250), subindustry), hump=0.0025)"),
    ("p5_loaned_share_lvl", "hump(group_rank(ts_decay_linear(vec_avg(loaned_share_count_p5_d1), 500), subindustry), hump=0.0025)"),
    ("p6_rate_vol_lvl", "hump(group_rank(ts_decay_linear(vec_avg(loan_rate_volatility_p5_d1), 500), industry), hump=0.0025)"),
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
