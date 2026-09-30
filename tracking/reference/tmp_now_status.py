# -*- coding: utf-8 -*-
"""当前平台侧真值：REGULAR/SUPER 配额 + 各区域 pyramid 点亮计数。"""
import asyncio, json, os, sys
REPO = r"D:\coding\traeCN_project\wqb"
sys.path.insert(0, os.path.join(REPO, "world-quant-brain-mcp"))


async def main():
    from brain_api import brain_client
    await brain_client.ensure_authenticated()

    # 配额
    r = await brain_client._request("GET", "https://api.worldquantbrain.com/users/self")
    prof = r.json()
    print("[PROFILE]", json.dumps({k: prof.get(k) for k in ("id", "email")}, ensure_ascii=False))

    # pyramid-alphas
    for region in ("KOR", "DEU", "EUR", "ASI", "IND", "GBR", "JPN", "CHN", "USA", "GLB", "HKG", "MEA", "AMR", "TWN"):
        try:
            rr = await brain_client._request("GET",
                f"https://api.worldquantbrain.com/users/self/activities/pyramid-alphas?region={region}")
            if rr.status_code != 200:
                continue
            d = rr.json()
        except Exception as e:
            print(region, "ERR", e); continue
        items = d if isinstance(d, list) else d.get("pyramidAlphas", d.get("items", []))
        if not items:
            continue
        print(f"\n=== {region} ===")
        for it in items:
            cnt = it.get("alphaCount", 0)
            lit = "LIT" if cnt >= 3 else ("~1" if cnt else "0")
            print(f"  {it.get('delay')}/{it.get('category')}: {cnt}  {lit}")


asyncio.run(main())
