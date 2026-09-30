"""扫描各区域：未亮/半亮塔 + 该区域可用数据集（cov>=0.5, alphaCount<=60, fields>=5）。"""
import asyncio, json, sys, os
REPO = r"D:\coding\traeCN_project\wqb"
sys.path.insert(0, os.path.join(REPO, "world-quant-brain-mcp"))

# 目标：未亮或刚亮的塔（缺口<=2）
TARGETS = {
 "EUR": [("other", 2), ("news", 0), ("risk", 0)],
 "GBR": [("pv", 1)],
 "ASI": [("pv", 2), ("sentiment", 2), ("model", 1), ("other", 1), ("risk", 1)],
 "HKG": [],  # 全亮
}

async def main():
    from brain_api import brain_client
    await brain_client.ensure_authenticated()
    for region, cats in TARGETS.items():
        if not cats:
            continue
        uni = {"EUR":"TOP2500","GBR":"TOP3500","ASI":"MINVOL1M"}.get(region,"TOP1000")
        print(f"\n=== {region} (universe={uni}) ===")
        off, rows = 0, []
        while True:
            url=(f"https://api.worldquantbrain.com/data-sets?instrumentType=EQUITY&region={region}"
                 f"&delay=1&universe={uni}&limit=50&offset={off}")
            r = await brain_client._request("GET", url)
            if r.status_code != 200:
                print("  ERR", r.status_code, r.text[:150]); break
            d = r.json(); rs = d.get("results") or []
            rows.extend(rs)
            if not rs or off+50 >= (d.get("count") or 0): break
            off += 50
        for catid, gap in cats:
            cands=[x for x in rows if (x.get("category") or {}).get("id")==catid]
            cands=[x for x in cands if (x.get("coverage") or 0)>=0.5 and (x.get("alphaCount") or 0)<=60 and (x.get("fieldCount") or 0)>=5]
            cands.sort(key=lambda x: x.get("alphaCount") or 0)
            print(f"  [{catid}] 缺口{gap} 合格数据集 {len(cands)}:")
            for x in cands[:6]:
                print(f"     {x.get('id'):24s} f={x.get('fieldCount'):3d} a={x.get('alphaCount'):4d} cov={(x.get('coverage') or 0):.2f} {x.get('name')[:36]}")
asyncio.run(main())
