# -*- coding: utf-8 -*-
"""KOR 各塔点亮状态盘点（2026-09-29）。

权威源：GET /users/self/activities/pyramid-alphas  （按 region/delay/category 返回 alphaCount）
点亮定义：同一塔名下 ACTIVE>=3。
本脚本只打印 KOR 段落 + 全量 category 计数，便于识别"未点亮塔"。
"""
import asyncio, json, sys, os
REPO = r"D:\coding\traeCN_project\wqb"
sys.path.insert(0, os.path.join(REPO, "world-quant-brain-mcp"))


async def main():
    from brain_api import brain_client
    await brain_client.ensure_authenticated()
    r = await brain_client._request(
        "GET", "https://api.worldquantbrain.com/users/self/activities/pyramid-alphas"
    )
    print("status:", r.status_code)
    d = r.json()
    # 结构探测
    if isinstance(d, dict):
        print("top keys:", list(d.keys())[:20])
        rows = d.get("pyramids") or d.get("items") or d.get("results") or []
    else:
        rows = d
    print("total rows:", len(rows))
    print("\n=== KOR ===")
    kor = [x for x in rows if str(x.get("region", "")).upper() == "KOR"]
    for x in sorted(kor, key=lambda z: (str(z.get("delay")), str((z.get("category") or {}).get("name") if isinstance(z.get("category"), dict) else z.get("category")))):
        cat = x.get("category")
        cname = cat.get("name") if isinstance(cat, dict) else cat
        cid = cat.get("id") if isinstance(cat, dict) else None
        print(f"  delay={x.get('delay')} cat={cname}({cid}) count={x.get('alphaCount')}")
    print(f"  KOR rows: {len(kor)}")
    print("\n=== ALL region/delay/cat (count>0) ===")
    for x in sorted(rows, key=lambda z: (str(z.get("region")), str(z.get("delay")), -int(z.get("alphaCount") or 0))):
        c = int(x.get("alphaCount") or 0)
        if c == 0:
            continue
        cat = x.get("category")
        cname = cat.get("name") if isinstance(cat, dict) else cat
        print(f"  {x.get('region')}/D{x.get('delay')}/{cname} = {c}")


asyncio.run(main())
