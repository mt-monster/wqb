"""零成本核实：KOR 当月已提交 alpha 分类统计（纯PPA/PPA+REG/REGULAR）"""
import asyncio, json, sys, os
from datetime import datetime
REPO = r"D:\coding\traeCN_project\wqb"
sys.path.insert(0, os.path.join(REPO, "world-quant-brain-mcp"))

async def main():
    from brain_api import brain_client
    await brain_client.ensure_authenticated()
    now = datetime.now()
    # ET 当月范围（近似用本地月，足够判定）
    start = f"{now.year}-{now.month:02d}-01"
    if now.month == 12:
        end = f"{now.year+1}-01-01"
    else:
        end = f"{now.year}-{now.month+1:02d}-01"
    print(f"查询区间: {start} ~ {end}")

    all_alphas = []
    offset = 0
    while True:
        url = (f"https://api.worldquantbrain.com/users/self/alphas?limit=100&offset={offset}"
               f"&status!=UNSUBMITTED%1FIS_FAIL"
               f"&dateSubmitted%3E={start}T00:00:00-04:00"
               f"&dateSubmitted%3C{end}T00:00:00-04:00")
        r = await brain_client._request("GET", url)
        if r.status_code != 200:
            print(f"HTTP {r.status_code}: {r.text[:200]}")
            break
        j = r.json()
        res = j.get("results", [])
        all_alphas.extend(res)
        if len(all_alphas) >= j.get("count", 0) or not res:
            break
        offset += 100
    print(f"本月已提交总数: {len(all_alphas)}")

    from collections import defaultdict
    stat = defaultdict(lambda: {"pure_ppa": 0, "ppa_reg": 0, "regular": 0, "atom": 0, "other": 0})
    for a in all_alphas:
        region = a.get("settings", {}).get("region", "?")
        cls_ids = [c.get("id", "") for c in a.get("classifications", [])]
        has_pp = any("POWER_POOL" in c for c in cls_ids)
        has_reg = any("REGULAR" in c for c in cls_ids)
        has_atom = any("SINGLE_DATA_SET" in c for c in cls_ids)
        s = stat[region]
        if has_pp and not has_reg and not has_atom:
            s["pure_ppa"] += 1
        elif has_pp and has_reg:
            s["ppa_reg"] += 1
        elif has_pp and has_atom:
            s["atom"] += 1
        elif has_reg:
            s["regular"] += 1
        else:
            s["other"] += 1
    print("\n=== 分区域统计 ===")
    for region, s in sorted(stat.items()):
        print(f"{region}: 纯PPA={s['pure_ppa']}  PPA+REG={s['ppa_reg']}  PPA+ATOM={s['atom']}  REGULAR={s['regular']}  other={s['other']}")

    print("\n=== KOR 明细 ===")
    for a in all_alphas:
        if a.get("settings", {}).get("region") != "KOR":
            continue
        cls_ids = [c.get("id", "") for c in a.get("classifications", [])]
        print(f"{a.get('id')} | {a.get('name','')[:40]} | {a.get('status')} | {cls_ids}")

asyncio.run(main())
