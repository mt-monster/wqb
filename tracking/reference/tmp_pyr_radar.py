# -*- coding: utf-8 -*-
"""全区域塔灯盘点：点亮(lit>=3) / 差1(2) / 差2(1) / 空(0)。权威源 pyramid-alphas。"""
import asyncio, json, sys, os
REPO = r"D:\coding\traeCN_project\wqb"
sys.path.insert(0, os.path.join(REPO, "world-quant-brain-mcp"))

CANON = ["analyst", "fundamental", "model", "other", "pv", "shortinterest", "earnings",
         "imbalance", "insiders", "institutions", "macro", "news", "sentiment", "risk",
         "socialmedia"]


async def main():
    from brain_api import brain_client
    await brain_client.ensure_authenticated()
    r = await brain_client._request("GET", "https://api.worldquantbrain.com/users/self/activities/pyramid-alphas")
    rows = r.json()
    if isinstance(rows, dict):
        rows = rows.get("pyramids") or rows.get("items") or rows.get("results") or []
    by = {}
    for x in rows:
        reg = str(x.get("region", "")).upper()
        cat = x.get("category")
        cid = (cat.get("id") if isinstance(cat, dict) else cat) or ""
        cid = str(cid).lower().replace(" ", "").replace("-", "")
        cnt = int(x.get("alphaCount") or 0)
        by[(reg, cid)] = cnt
    regs = sorted({k[0] for k in by})
    print("区域雷达（lit=已亮 / +1=差1 / +2=差2）：\n")
    for reg in regs:
        lit = [c for c in CANON if by.get((reg, c)) is not None and by[(reg, c)] >= 3]
        need1 = [c for c in CANON if by.get((reg, c), 0) == 2]
        need2 = [c for c in CANON if by.get((reg, c), 0) == 1]
        print(f"{reg}:")
        print(f"   LIT  ({len(lit)}): {', '.join(lit) if lit else '-'}")
        print(f"   +1   ({len(need1)}): {', '.join(need1) if need1 else '-'}")
        print(f"   +2   ({len(need2)}): {', '.join(need2) if need2 else '-'}")
    print("\n=== 全局'差1颗即亮'优先目标 ===")
    for reg in regs:
        for c in CANON:
            if by.get((reg, c), -1) == 2:
                print(f"  {reg}/D1/{c}  (2 -> 3)")


asyncio.run(main())
