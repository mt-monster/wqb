# -*- coding: utf-8 -*-
"""EUR Other 塔挖掘 probe（news_sentiment_nlp，23 VECTOR 情绪/可读性字段，cov 0.913，零竞争）。

目标：点亮 EUR/D1/OTHER 塔（现 2 颗，缺口 1... 实为 cat=other 计 2）。
设置：EUR / TOPCS1600 / D1 / SUBINDUSTRY / decay 30 / trunc 0.02（对齐 KOR 成功配方）

probe 策略（先小样本定方向）：
  情绪极性（正面-负面）比值 / 可读性 / 主观性 → 各 1-2 条，看方向
"""
import asyncio, json, sys, os
REPO = r"D:\coding\traeCN_project\wqb"
sys.path.insert(0, os.path.join(REPO, "world-quant-brain-mcp"))

C = [
    # 情绪极性：正面 vs 负面（比值/差）
    ("e1_pos_neg_ratio", "hump(group_rank(ts_decay_linear(divide(vec_avg(headline_vader_positive_polarity), add(vec_avg(headline_vader_negative_polarity),0.0001)), 250), subindustry), hump=0.0025)"),
    ("e2_pos_neg_diff", "hump(group_rank(ts_decay_linear(subtract(vec_avg(headline_vader_positive_polarity), vec_avg(headline_vader_negative_polarity)), 250), subindustry), hump=0.0025)"),
    # VADER 综合情绪
    ("e3_vader", "hump(group_rank(ts_decay_linear(vec_avg(headline_sentiment_vader_score), 250), subindustry), hump=0.0025)"),
    ("e4_textblob", "hump(group_rank(ts_decay_linear(vec_avg(headline_textblob_sentiment_score), 250), subindustry), hump=0.0025)"),
    # 句子情绪均值（另一极性定义）
    ("e5_sent_avg", "hump(group_rank(ts_decay_linear(vec_avg(headline_sentence_sentiment_average), 250), industry), hump=0.0025)"),
    # 主观性
    ("e6_subjectivity", "hump(group_rank(ts_decay_linear(vec_avg(headline_subjectivity_score), 250), subindustry), hump=0.0025)"),
    # 情绪方差（分歧度）
    ("e7_sent_var", "hump(group_rank(ts_decay_linear(vec_avg(headline_sentence_sentiment_variance), 250), subindustry), hump=0.0025)"),
    # 可读性（复杂度）
    ("e8_readability", "hump(group_rank(ts_decay_linear(vec_avg(headline_flesch_readability_score), 250), subindustry), hump=0.0025)"),
]


async def main():
    from brain_api import brain_client
    from tools_sim import create_multi_simulation
    await brain_client.ensure_authenticated()
    r = await create_multi_simulation([c[1] for c in C], region="EUR", universe="TOPCS1600", delay=1,
        decay=30, neutralization="SUBINDUSTRY", truncation=0.02, nan_handling="ON", test_period="P0Y0M")
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
                    print(f"    {C[j][0]}: {aid} S={is_.get('sharpe')} F={is_.get('fitness')} T={is_.get('turnover')} pyr={a.get('pyramids')}")
                else:
                    print(f"    {C[j][0]}: {dd.get('status')} {str(dd.get('message'))[:90]}")
            break
asyncio.run(main())
