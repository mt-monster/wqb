# -*- coding: utf-8 -*-
"""为 SI12 通过腿写三段式 PP description（≥100 字符）。"""
import asyncio, json, sys, os
REPO = r"D:\coding\traeCN_project\wqb"
sys.path.insert(0, os.path.join(REPO, "world-quant-brain-mcp"))

TARGETS = {
 "E5pjMalL": ("KOR SI Net Imbalance Net-Sell share",
   "Idea: rank KOR stocks by their net invalid-short-selling imbalance, defined as the difference between invalid sell and buy amounts scaled by their sum. Persistently high net invalid-sell share indicates a stock whose short-selling activity is dominated by sells that fail delivery or violate rules, a proxy for speculative bearish pressure that tends to revert over daily horizons. Rationale for data used: the KOR shortinterest dataset (shrt38) reports mandated daily invalid short-sale amount components per stock; taking their sum over the reporting window denoises single-day noise while preserving the cross-sectional ordering of net sell pressure. Rationale for operators used: vec_sum aggregates the multi-period amount vectors into a scalar per stock; divide normalizes by total activity so the signal is scale-free and comparable across market caps; hump smooths the position path to suppress high-frequency turnover and reduce correlation with crowded short-interest factors; group_rank within sector removes industry-level common factors so the residual captures purely idiosyncratic invalid-sell pressure."),
 "RRbOoMNg": ("KOR SI Ratio Decay-Linear 250d",
   "Idea: rank KOR stocks by a decay-weighted average of their invalid short-sell to invalid short-buy ratio, emphasizing recent weeks. A rising invalid sell/buy ratio signals deteriorating delivery discipline on the short side, which historically precedes negative returns over daily rebalancing horizons. Rationale for data used: the shrt38 shortinterest dataset provides regulated daily invalid short-sale amounts; the sell/buy ratio is a self-normalizing measure of directional short pressure that is robust to firm size and aggregate market activity. Rationale for operators used: vec_sum condenses the intraday amount vectors into per-stock daily totals; divide forms the scale-free ratio; ts_decay_linear applies a linear weighting over 250 trading days so that recent observations dominate while old observations still anchor the level; hump constrains position changes to reduce turnover and lower correlation with existing short-interest alphas; group_rank within sector neutralizes industry effects."),
 "JjNAkqbn": ("KOR SI Ratio Decay-Linear 500d Industry",
   "Idea: rank KOR stocks by a two-year decay-weighted average of the invalid short-sell to short-buy ratio, neutralized within industry. The long decay window captures the structural level of short-side delivery failure rather than transient spikes, providing a slow-moving signal with high Sharpe and low turnover. Rationale for data used: the shrt38 shortinterest dataset offers regulatory daily invalid short-sale amounts; the sell/buy ratio is dimensionless and hence comparable across all listed KOR equities. Rationale for operators used: vec_sum reduces the amount vectors to daily scalars; divide builds the dimensionless pressure ratio; ts_decay_linear with a 500-day window yields a smooth structural estimate; hump caps period-over-period position changes to control turnover and decorrelate from fast short-interest signals; group_rank within industry removes sector-level common variation."),
 "e7bYP29g": ("KOR SI Net Imbalance Industry",
   "Idea: rank KOR stocks by net invalid-short-selling imbalance normalized by total invalid short activity, neutralized within industry. Stocks with a persistently positive net invalid-sell share reflect speculative bearish positioning that mean-reverts at daily frequency. Rationale for data used: the shrt38 shortinterest dataset reports mandated invalid short-sale amounts; summing across the vector collapses reporting granularity into a single robust daily measure, while the normalization by total activity makes the signal size-independent. Rationale for operators used: vec_sum aggregates the multi-period vectors; subtract isolates the net sell direction, and divide by the sum produces a bounded imbalance in [-1,1]; hump smooths trading to cut turnover and reduce overlap with existing short-interest alphas; group_rank within industry neutralizes common industry factors."),
}

async def main():
    from brain_api import brain_client
    await brain_client.ensure_authenticated()
    for aid,(nm,desc) in TARGETS.items():
        # 写 name + description
        payload = {"name": nm, "regular": {"description": desc}}
        r = await brain_client._request("PATCH", f"https://api.worldquantbrain.com/alphas/{aid}", json=payload)
        print(f"{aid} PATCH {r.status_code} desc_len={len(desc)}")
        # 回读
        rr = await brain_client._request("GET", f"https://api.worldquantbrain.com/alphas/{aid}")
        d = rr.json()
        got = (d.get("regular") or {}).get("description") or ""
        print(f"   readback: name={d.get('name')!r} desc_len={len(got)}")
        await asyncio.sleep(1)
asyncio.run(main())
