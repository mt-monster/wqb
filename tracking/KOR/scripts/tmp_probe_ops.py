"""逐条提交，定位哪条表达式 FAIL。"""
import asyncio, json, sys, os
REPO = r"D:\coding\traeCN_project\wqb"
sys.path.insert(0, os.path.join(REPO, "world-quant-brain-mcp"))
T="normalized_trend_indicator_%d"; V="normalized_volume_indicator_%d"
EXPRS = [
    ("e_std", f"ts_std_dev({T % 0}, 60)"),
    ("e_hump", f"hump(group_rank(ts_decay_linear({T % 0}, 250), subindustry), hump=0.0025)"),
    ("e_add3", f"add(add({T % 0}, {T % 1}), {T % 2})"),
    ("e_div", f"divide({T % 0}, add({V % 0}, 0.0001))"),
    ("e_mul", f"multiply({T % 0}, {V % 0})"),
    ("e_rank_ind", f"group_rank(ts_rank({T % 0}, 250), industry)"),
]
async def one(bc, e):
    payload = {"type":"REGULAR","settings":{"instrumentType":"EQUITY","region":"KOR","universe":"TOP600",
      "delay":1,"decay":30,"neutralization":"SLOW_AND_FAST","truncation":0.02,"nanHandling":"ON",
      "pasteurization":"ON","unitHandling":"VERIFY","language":"FASTEXPR","testPeriod":"P0Y0M",
      "maxTrade":"OFF","visualization":False},"regular": e}
    r = await bc._request("POST","https://api.worldquantbrain.com/simulations", json=payload)
    return r.status_code, r.text.strip()[:120]
async def main():
    from brain_api import brain_client
    await brain_client.ensure_authenticated()
    for name, e in EXPRS:
        code, txt = await one(brain_client, e)
        print(f"{name:14s} {code} {txt}")
        await asyncio.sleep(2)
asyncio.run(main())
