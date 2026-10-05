"""稳健提取 multisim 子 alpha 指标：认证 429 自动退避重试，单次认证会话内完成。

用法: python tracking/IND/scripts/_harvest.py <mid> [<mid> ...]
输出: 排序表 + 表达式清单，并落 logs/_harvest_<mid>.json 与 logs/_harvest_latest.json

注意：logs/_harvest.py 曾被外部清理进程删除，权威副本放 tracking/ 下（不受清理影响）。
"""
import asyncio
import json
import sys
import time

sys.path.insert(0, "world-quant-brain-mcp")
from brain_api import brain_client as brain  # noqa: E402

TERMINAL = ("COMPLETE", "ERROR", "CANCELLED", "WARNING")


async def auth(max_try=8):
    for i in range(max_try):
        try:
            await brain.ensure_authenticated()
            return True
        except Exception as e:
            w = 180 if "429" in str(e) else 30
            print(f"[auth] try {i+1} failed: {str(e)[:80]} -> sleep {w}s", flush=True)
            time.sleep(w)
    return False


async def req(method, url, tries=6):
    """带退避重试的 _request —— 平台偶发 10054/429 断连不再整批崩溃。"""
    for i in range(tries):
        try:
            return await brain._request(method, url)
        except Exception as e:
            print(f"[req] {method} {url} try {i+1} failed: {str(e)[:90]}", flush=True)
            await asyncio.sleep(min(20 * (i + 1), 120))
    return None


async def poll(mid, max_min=40):
    for _ in range(max_min * 3):
        r = await req("GET", f"{brain.base_url}/simulations/{mid}")
        try:
            d = r.json() if r is not None else {}
        except Exception:
            d = {}
        if d.get("status") in TERMINAL:
            return d
        await asyncio.sleep(20)
    return {}


async def one(mid):
    rows = []
    d = await poll(mid)
    if not d:
        print(f"=== {mid} === TIMEOUT / empty", flush=True)
        return rows
    for cid in d.get("children") or []:
        rc = await req("GET", f"{brain.base_url}/simulations/{cid}")
        if rc is None:
            rows.append({"mid": mid, "cid": cid, "aid": None, "status": "REQ_FAIL"})
            continue
        cd = rc.json()
        aid = cd.get("alpha")
        if not aid:
            rows.append({"mid": mid, "cid": cid, "aid": None, "status": cd.get("status"),
                         "err": (cd.get("message") or "")[:160]})
            continue
        ra = await req("GET", f"{brain.base_url}/alphas/{aid}")
        ad = ra.json() if ra is not None else {}
        isd = ad.get("is") or {}
        checks = isd.get("checks") or []
        fails = [c.get("name") for c in checks if c.get("result") == "FAIL"]
        warns = [c.get("name") for c in checks if c.get("result") == "WARNING"]
        rows.append({
            "mid": mid, "cid": cid, "aid": aid, "status": cd.get("status"),
            "code": (ad.get("regular") or {}).get("code"),
            "S": isd.get("sharpe"), "F": isd.get("fitness"),
            "ret": isd.get("returns"), "TO": isd.get("turnover"),
            "DD": isd.get("drawdown"), "margin": isd.get("margin"),
            "L": isd.get("longCount"), "Sh": isd.get("shortCount"),
            "fails": fails, "warns": warns,
        })
    rows.sort(key=lambda r: (len(r.get("fails") or []), -(r.get("S") or -9)))
    return rows


async def main():
    if not await auth():
        print("AUTH FAIL")
        return
    all_rows = []
    for mid in sys.argv[1:]:
        print(f"\n=== {mid} ===", flush=True)
        rows = await one(mid)
        all_rows.extend(rows)
        print(f"{'alpha_id':<10} {'S':<6} {'F':<6} {'ret':<7} {'TO':<7} {'DD':<7} L/Sh  FAIL / WARN")
        for r in rows:
            if not r.get("aid"):
                print(f"  {r.get('cid')} ERR {r.get('status')} {r.get('err')}")
                continue
            print(f"{r['aid']:<10} {r['S']:<6} {r['F']:<6} {r['ret']:<7} {r['TO']:<7} "
                  f"{r['DD']:<7} {r['L']}/{r['Sh']}  {r['fails']} | {r['warns']}")
        print()
        for i, r in enumerate([x for x in rows if x.get("aid")], 1):
            print(f" {i}. [{r['aid']}] S={r['S']} F={r['F']} TO={r['TO']}")
            print(f"    {r['code']}")
        with open(f"logs/_harvest_{mid}.json", "w", encoding="utf-8") as f:
            json.dump(rows, f, ensure_ascii=False, indent=1)
    with open("logs/_harvest_latest.json", "w", encoding="utf-8") as f:
        json.dump(all_rows, f, ensure_ascii=False, indent=1)
    print("\nsaved -> logs/_harvest_latest.json", flush=True)


asyncio.run(main())
