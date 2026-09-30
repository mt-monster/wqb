# -*- coding: utf-8 -*-
"""扫描各区域的"强信号源"数据集：VECTOR/event 类（行为/资金流/持仓），
参照 KOR shrt38 成功模式。输出候选数据集清单（region/category/dataset）。
"""
import asyncio, json, sys, os
REPO = r"D:\coding\traeCN_project\wqb"
sys.path.insert(0, os.path.join(REPO, "world-quant-brain-mcp"))

REGIONS = ["USA", "EUR", "ASI", "DEU", "GBR", "HKG", "IND", "JPN", "CHN", "GLB", "MEA", "AMR", "KOR"]
# 关注类别关键词（强信号源）
KEYS = ["shortinterest", "insider", "institution", "imbalance", "sentiment", "news",
        "option", "analyst", "socialmedia", "other", "risk", "earnings", "model", "pv"]

async def main():
    from brain_api import brain_client
    await brain_client.ensure_authenticated()
    out = {}
    for reg in REGIONS:
        try:
            r = await brain_client._request(
                "GET",
                f"https://api.worldquantbrain.com/data-sets?instrumentType=EQUITY&region={reg}&delay=1&limit=50&offset=0")
            if r.status_code != 200:
                print(f"{reg}: HTTP {r.status_code}")
                continue
            d = r.json()
            sets = d.get("results") or []
            # 分页
            off = 50
            while d.get("next") and off < 400:
                r2 = await brain_client._request(
                    "GET",
                    f"https://api.worldquantbrain.com/data-sets?instrumentType=EQUITY&region={reg}&delay=1&limit=50&offset={off}")
                if r2.status_code != 200: break
                d = r2.json()
                sets += d.get("results") or []
                off += 50
            rows = []
            for s in sets:
                cat = ((s.get("category") or {}).get("name")) or "?"
                aid = s.get("id")
                nm = s.get("name") or ""
                ac = s.get("alphaCount") or 0
                fc = s.get("fieldCount") or 0
                if any(k in cat.lower() or k in nm.lower() for k in KEYS):
                    rows.append({"id": aid, "name": nm, "category": cat,
                                 "alphaCount": ac, "fieldCount": fc,
                                 "users": s.get("userCount")})
            rows.sort(key=lambda x: (-x["alphaCount"]))
            out[reg] = rows
            print(f"\n=== {reg} ({len(rows)} 强信号候选数据集) ===")
            for x in rows[:25]:
                print(f"  {x['id']:16s} cat={x['category']:15s} aC={x['alphaCount']:5d} fC={x['fieldCount']:4d} {x['name'][:48]}")
        except Exception as e:
            print(f"{reg}: EXC {e}")
    with open(os.path.join(REPO, "tracking/reference/strong_ds_scan.json"), "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print("\nSAVED strong_ds_scan.json")

asyncio.run(main())
