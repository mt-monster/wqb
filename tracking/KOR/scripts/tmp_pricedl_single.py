"""逐条单提交，精确定位 price_signal_dl probe 中哪条表达式导致 FAIL。"""
import asyncio, json, sys, os
REPO = r"D:\coding\traeCN_project\wqb"
sys.path.insert(0, os.path.join(REPO, "world-quant-brain-mcp"))

T = "normalized_trend_indicator_%d"
V = "normalized_volume_indicator_%d"

C = [
    ("t1_trend_avg_rev", "hump(group_rank(ts_decay_linear(multiply(-1, add(add(" + T % 0 + f", {T % 1}), {T % 2})), 250), subindustry), hump=0.0025)"),
    ("t2_trend_vol_ratio", f"hump(group_rank(ts_decay_linear(divide({T % 0}, add({V % 0}, 0.0001)), 250), subindustry), hump=0.0025)"),
    ("t3_trend_delta", f"hump(group_rank(ts_delta({T % 3}, 20), subindustry), hump=0.0025)"),
    ("t4_trend_rank", f"hump(group_rank(ts_rank({T % 0}, 250), industry), hump=0.0025)"),
    ("t5_vol_rev", f"hump(group_rank(ts_decay_linear(multiply(-1, {V % 0}), 250), subindustry), hump=0.0025)"),
    ("t6_raw_norm_ratio", f"hump(group_rank(ts_decay_linear(divide(raw_trend_indicator_0, add({T % 0}, 0.0001)), 250), subindustry), hump=0.0025)"),
    ("t7_trend_std", f"hump(group_rank(ts_decay_linear(multiply(-1, ts_std_dev({T % 0}, 60)), 20), subindustry), hump=0.0025)"),
    ("t8_tv_sync", f"hump(group_rank(ts_decay_linear(multiply({T % 0}, {V % 0}), 250), industry), hump=0.0025)"),
]


async def one(bc, e):
    payload = {"type": "REGULAR", "settings": {
        "instrumentType": "EQUITY", "region": "KOR", "universe": "TOP600", "delay": 1,
        "decay": 30, "neutralization": "SLOW_AND_FAST", "truncation": 0.02, "nanHandling": "ON",
        "pasteurization": "ON", "unitHandling": "VERIFY", "language": "FASTEXPR", "testPeriod": "P0Y0M",
        "maxTrade": "OFF", "visualization": False}, "regular": e}
    r = await bc._request("POST", "https://api.worldquantbrain.com/simulations", json=payload)
    loc = r.headers.get("Location") or ""
    return r.status_code, r.text.strip()[:150], loc.rstrip("/").split("/")[-1]


async def main():
    from brain_api import brain_client
    await brain_client.ensure_authenticated()
    pids = []
    for name, e in C:
        code, txt, pid = await one(brain_client, e)
        print(f"{name:20s} {code} {txt}")
        pids.append((name, pid))
        await asyncio.sleep(3)
    print("\n=== poll ===")
    await asyncio.sleep(60)
    for name, pid in pids:
        if not pid:
            continue
        r = await brain_client._request("GET", f"https://api.worldquantbrain.com/simulations/{pid}")
        d = r.json()
        aid = d.get("alpha")
        msg = d.get("message")
        line = f"{name:20s} status={d.get('status')} alpha={aid}"
        if aid:
            r2 = await brain_client._request("GET", f"https://api.worldquantbrain.com/alphas/{aid}")
            is_ = (r2.json().get("is") or {})
            line += f" S={is_.get('sharpe')} F={is_.get('fitness')} T={is_.get('turnover')}"
        if msg:
            line += f" msg={str(msg)[:90]}"
        print(line)


asyncio.run(main())
