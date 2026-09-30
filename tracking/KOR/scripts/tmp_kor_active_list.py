# -*- coding: utf-8 -*-
"""列出 KOR 全部 ACTIVE alpha 及其 pyramids 塔归属（判断点亮进度）。"""
import asyncio, json, sys, os
REPO = r"D:\coding\traeCN_project\wqb"
sys.path.insert(0, os.path.join(REPO, "world-quant-brain-mcp"))

async def main():
    from brain_api import brain_client
    await brain_client.ensure_authenticated()
    # 拉取 KOR ACTIVE alpha
    url = ("https://api.worldquantbrain.com/users/self/alphas?limit=100&offset=0"
           "&status=ACTIVE&order=-dateCreated")
    rows = []
    while True:
        r = await brain_client._request("GET", url)
        if r.status_code != 200:
            print("ERR", r.status_code, r.text[:200]); break
        d = r.json()
        rs = d.get("results") or []
        rows.extend(rs)
        nxt = d.get("next")
        if not nxt or not rs:
            break
        url = nxt if nxt.startswith("http") else "https://api.worldquantbrain.com" + nxt
    kor = [x for x in rows if (x.get("settings") or {}).get("region") == "KOR"]
    print(f"total ACTIVE={len(rows)} KOR={len(kor)}")
    for x in kor:
        aids = x.get("id")
        pyr = x.get("pyramids") or []
        names = [p.get("name") for p in pyr] if isinstance(pyr, list) else pyr
        print(f"  {aids}  {names}")

asyncio.run(main())
