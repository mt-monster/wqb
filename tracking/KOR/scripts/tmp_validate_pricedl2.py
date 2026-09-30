"""用平台 validate 端点校验 price_signal_dl 表达式。"""
import asyncio, json, sys, os
REPO = r"D:\coding\traeCN_project\wqb"
sys.path.insert(0, os.path.join(REPO, "world-quant-brain-mcp"))


async def main():
    from brain_api import brain_client
    await brain_client.ensure_authenticated()
    exprs = [
        "normalized_trend_indicator_0",
        "ts_rank(normalized_trend_indicator_0, 250)",
        "normalized_volume_indicator_0",
        "raw_trend_indicator_0",
    ]
    url = "https://api.worldquantbrain.com/simulations"
    for e in exprs:
        payload = {
            "type": "REGULAR",
            "settings": {"instrumentType": "EQUITY", "region": "KOR", "universe": "TOP600", "delay": 1,
                         "decay": 30, "neutralization": "SLOW_AND_FAST", "truncation": 0.02,
                         "nanHandling": "ON", "pasteurization": "ON", "unitHandling": "VERIFY",
                         "language": "FASTEXPR", "testPeriod": "P0Y0M", "maxTrade": "OFF",
                         "visualization": False},
            "regular": e,
        }
        r = await brain_client._request("POST", url, json=payload)
        print(f"{e[:50]:52s} -> {r.status_code} {r.text.strip()[:200]}")
        if r.status_code in (200, 201):
            print("   loc:", r.headers.get("Location") or "")
        await asyncio.sleep(2)


asyncio.run(main())
