"""全量 OS 实盘数据扫描（只读，带断点续跑）。

平台把 OS 字段从 os.sharpe 迁到 os.osISSharpeRatio（OS/IS Sharpe 比值），
且只在 get_alpha_details 返回真值（user_alphas 列表里恒为 null）。
本脚本对全部 ACTIVE REGULAR alpha 逐颗 get_alpha_details，抽取：
  region / IS_sharpe / investability_sharpe / prod / osISSharpeRatio
并换算 OS_sharpe = IS_sharpe × osISSharpeRatio。
结果落 results/os_scan.json（断点续跑）。
用法: python tools/data-repair/os_scan_all.py [--fresh]
"""
import os
import sys
import json
import asyncio
import time

HERE = os.path.dirname(os.path.abspath(__file__))
WQB = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.join(WQB, "world-quant-brain-mcp"))
from brain_api import BrainApiClient

OUT = os.path.join(WQB, "results", "os_scan.json")


async def fetch_pool(b):
    rows, off = [], 0
    for _ in range(200):
        r = await b.get_user_alphas(stage="OS", limit=100, offset=off)
        pl = r["result"] if isinstance(r, dict) and isinstance(r.get("result"), dict) else r
        res = pl.get("results", []) or []
        if not res:
            break
        rows.extend(res)
        if not pl.get("next"):
            break
        off += 100
    return rows


async def main(fresh):
    b = BrainApiClient()
    await b.ensure_authenticated()

    pool = await fetch_pool(b)
    regs = [a for a in pool if a.get("type") == "REGULAR" and a.get("status") == "ACTIVE"]
    # 平台列表基础指标（IS/inv/prod），osISSharpeRatio 需逐颗 details
    base = {}
    for a in regs:
        st = a.get("settings") or {}
        isd = a.get("is") or {}
        prod = isd.get("prodCorrelation")
        if prod is None:
            prod = a.get("prod")
        base[a["id"]] = {
            "region": st.get("region"), "delay": st.get("delay"),
            "is_sharpe": isd.get("sharpe"),
            "inv_sharpe": (isd.get("investabilityConstrained") or {}).get("sharpe"),
            "prod": prod,
        }
    print(f"[pool] {len(pool)} total, {len(regs)} ACTIVE REGULAR")

    ck = {}
    if os.path.exists(OUT) and not fresh:
        ck = json.load(open(OUT, encoding="utf-8"))
        print(f"[resume] 已有 {len(ck)} 颗缓存")

    todo = [aid for aid in base if aid not in ck]
    print(f"[scan] 待扫 {len(todo)} 颗")

    def save():
        tmp = OUT + ".tmp"
        json.dump(ck, open(tmp, "w", encoding="utf-8"), ensure_ascii=False)
        os.replace(tmp, OUT)

    t0 = time.time()
    for i, aid in enumerate(todo, 1):
        try:
            a = await b.get_alpha_details(aid)
            isd = a.get("is") or {}
            osd = a.get("os") or {}
            ratio = osd.get("osISSharpeRatio")
            rec = dict(base[aid])
            rec["os_ratio"] = ratio
            is_sh = rec.get("is_sharpe")
            rec["os_sharpe"] = round(is_sh * ratio, 4) if (is_sh and ratio is not None) else None
            rec["date_submitted"] = a.get("dateSubmitted")
            ck[aid] = rec
        except Exception as e:  # noqa: BLE001
            print(f"  [err] {aid}: {repr(e)[:120]}")
            ck[aid] = dict(base[aid]); ck[aid]["os_ratio"] = None; ck[aid]["os_sharpe"] = None
        if i % 10 == 0 or i == len(todo):
            save()
            el = time.time() - t0
            print(f"  [{i}/{len(todo)}] elapsed={el:.0f}s rate={i/max(el,1):.1f}/s")
        await asyncio.sleep(0.4)  # 轻度限速
    save()

    # 汇总
    from collections import defaultdict
    byreg = defaultdict(list)
    for aid, r in ck.items():
        byreg[r["region"]].append(r)
    print("\n=== OS 覆盖（fresh osISSharpeRatio） ===")
    print(f"{'reg':>5} {'n':>4} {'有OS':>5} {'正OS':>5} {'负OS':>5} {'avgOS':>7} {'avgIS':>7}")
    for reg in sorted(byreg, key=lambda x: -len(byreg[x])):
        al = byreg[reg]
        withos = [r for r in al if r.get("os_ratio") is not None]
        pos = [r for r in withos if (r.get("os_sharpe") or 0) > 0]
        neg = [r for r in withos if (r.get("os_sharpe") or 0) <= 0]
        avg_os = (sum(r["os_sharpe"] for r in withos) / len(withos)) if withos else None
        isv = [r["is_sharpe"] for r in al if r.get("is_sharpe") is not None]
        avg_is = (sum(isv) / len(isv)) if isv else None
        print(f"{reg:>5} {len(al):>4} {len(withos):>5} {len(pos):>5} {len(neg):>5} "
              f"{(round(avg_os,3) if avg_os is not None else '-'):>7} "
              f"{(round(avg_is,3) if avg_is is not None else '-'):>7}")
    print(f"\n[done] -> {OUT}")


if __name__ == "__main__":
    asyncio.run(main("--fresh" in sys.argv))
