# -*- coding: utf-8 -*-
"""查 alpha prod / self 相关性。用法: python tools/tmp_corr.py <alpha_id> [prod|self]"""
import asyncio, os, sys, json
REPO = r"D:\coding\traeCN_project\wqb"
sys.path.insert(0, os.path.join(REPO, "world-quant-brain-mcp"))

async def main():
    aid = sys.argv[1]
    kind = sys.argv[2] if len(sys.argv) > 2 else "prod"
    from brain_api import brain_client
    await brain_client.ensure_authenticated()
    url = f"https://api.worldquantbrain.com/alphas/{aid}/correlations/{kind}"
    for attempt in range(6):
        r = await brain_client._request("GET", url)
        if r.status_code == 200:
            t = r.text.strip()
            if not t:
                print(f"[{aid}] {kind}: empty body (computing), retry {attempt+1}")
                await asyncio.sleep(8); continue
            d = r.json()
            print(f"[{aid}] {kind}:")
            print(json.dumps(d, ensure_ascii=False, indent=1)[:1500])
            return
        else:
            print(f"HTTP {r.status_code}: {r.text[:200]}")
            return
    print("gave up")

asyncio.run(main())
