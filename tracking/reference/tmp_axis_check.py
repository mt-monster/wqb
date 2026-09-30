# -*- coding: utf-8 -*-
"""快速验证 EUR 分组轴合法性（单条 POST）。"""
import asyncio, sys, os
REPO = r"D:\coding\traeCN_project\wqb"
sys.path.insert(0, os.path.join(REPO, "world-quant-brain-mcp"))
RW="avg_similarity_rising_wedge_pattern_120"
VB="avg_similarity_v_reversal_bottom"
DIFF=f"subtract(ts_zscore({RW}, 60), ts_zscore({VB}, 60))"
async def main():
    from brain_api import brain_client
    await brain_client.ensure_authenticated()
    for ax in ("market","sector","industry","subindustry","exchange","country"):
        expr = f"group_zscore({DIFF}, {ax})"
        payload={"type":"REGULAR","settings":{"instrumentType":"EQUITY","region":"EUR","universe":"TOP2500",
            "delay":1,"decay":12,"neutralization":"SUBINDUSTRY","truncation":0.02,"pasteurization":"ON",
            "nanHandling":"ON","unitHandling":"VERIFY","language":"FASTEXPR","visualization":False,"testPeriod":"P0Y0M"},
            "regular":expr}
        r=await brain_client._request("POST","https://api.worldquantbrain.com/simulations",json=payload)
        print(f"{ax:12s} {r.status_code} {r.text[:120]}", flush=True)
        await asyncio.sleep(2)
asyncio.run(main())
