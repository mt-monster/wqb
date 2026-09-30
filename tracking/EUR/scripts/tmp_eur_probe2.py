# -*- coding: utf-8 -*-
"""EUR Other 塔 v2：提 turnover + 换结构（Mode B）。
首轮：8 条全正但弱（S 0.16-0.30），turnover 仅 0.05 → 信号过慢。
v2 变更：decay 30→4/10；加 ts_delta/ts_zscore/ts_rank 时序；情绪变化率。
"""
import asyncio, json, sys, os
REPO = r"D:\coding\traeCN_project\wqb"
sys.path.insert(0, os.path.join(REPO, "world-quant-brain-mcp"))

C = [
    # 情绪变化（delta）—— 提 turnover
    ("v1_pos_neg_delta", "hump(group_rank(ts_delta(divide(vec_avg(headline_vader_positive_polarity), add(vec_avg(headline_vader_negative_polarity),0.0001)), 20), subindustry), hump=0.0025)"),
    ("v2_vader_delta", "hump(group_rank(ts_delta(vec_avg(headline_sentiment_vader_score), 20), subindustry), hump=0.0025)"),
    # 短窗 decay
    ("v3_pos_neg_d10", "hump(group_rank(ts_decay_linear(divide(vec_avg(headline_vader_positive_polarity), add(vec_avg(headline_vader_negative_polarity),0.0001)), 10), subindustry), hump=0.0025)"),
    ("v4_vader_d10", "hump(group_rank(ts_decay_linear(vec_avg(headline_sentiment_vader_score), 10), industry), hump=0.0025)"),
    # ts_rank 时序排名
    ("v5_vader_rank60", "hump(group_rank(ts_rank(vec_avg(headline_sentiment_vader_score), 60), subindustry), hump=0.0025)"),
    ("v6_pos_neg_rank60", "hump(group_rank(ts_rank(divide(vec_avg(headline_vader_positive_polarity), add(vec_avg(headline_vader_negative_polarity),0.0001)), 60), subindustry), hump=0.0025)"),
    # 可读性（复杂度）delta
    ("v7_readab_delta", "hump(group_rank(ts_delta(vec_avg(headline_flesch_readability_score), 20), subindustry), hump=0.0025)"),
    # 句子情绪均值 delta
    ("v8_sentavg_delta", "hump(group_rank(ts_delta(vec_avg(headline_sentence_sentiment_average), 20), industry), hump=0.0025)"),
]


async def main():
    from brain_api import brain_client
    from tools_sim import create_multi_simulation
    await brain_client.ensure_authenticated()
    r = await create_multi_simulation([c[1] for c in C], region="EUR", universe="TOPCS1600", delay=1,
        decay=4, neutralization="SUBINDUSTRY", truncation=0.02, nan_handling="ON", test_period="P0Y0M")
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
                dd = r2.json()
                aid = dd.get("alpha")
                if aid:
                    r3 = await brain_client._request("GET", f"https://api.worldquantbrain.com/alphas/{aid}")
                    a = r3.json(); is_ = a.get("is") or {}
                    print(f"    {C[j][0]}: {aid} S={is_.get('sharpe')} F={is_.get('fitness')} T={is_.get('turnover')}")
                else:
                    print(f"    {C[j][0]}: {dd.get('status')} {str(dd.get('message'))[:90]}")
            break
asyncio.run(main())
