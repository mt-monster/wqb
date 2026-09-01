# -*- coding: utf-8 -*-
"""对比 USA 四座塔的计入明细：MODEL(亮)/OTHER(亮) vs FUNDAMENTAL(未亮)/PV(未亮)，
找 UI 点亮与 API pyramids 计数差异的区分规律。"""
import asyncio
import sys
from pathlib import Path

WQ_ROOT = Path(r"D:\coding\traeCN_project\wqb")
sys.path.insert(0, str(WQ_ROOT / "world-quant-brain-mcp"))
TARGETS = ("USA/D1/MODEL", "USA/D1/OTHER", "USA/D1/FUNDAMENTAL", "USA/D1/PV")


def expr_of(a):
    code = a.get("regular")
    return (code.get("code") if isinstance(code, dict) else str(code)) or ""


async def main():
    from brain_api import BrainApiClient
    brain = BrainApiClient()
    await brain.ensure_authenticated()

    out, off = [], 0
    while True:
        r = await brain._request(
            "GET", f"{brain.base_url}/users/self/alphas",
            params={"status": "ACTIVE", "limit": 100, "offset": off})
        arr = r.json().get("results") or []
        out.extend(arr)
        if len(arr) < 100 or off > 5000:
            break
        off += 100

    for t in TARGETS:
        rows = []
        for a in out:
            pys = [p.get("name") for p in (a.get("pyramids") or []) if p.get("name")]
            if t in pys:
                eff = (a.get("pyramidThemes") or {}).get("effective")
                rows.append((str(a.get("dateSubmitted"))[:10], a.get("id"),
                             str(a.get("name"))[:24], len(pys), eff,
                             expr_of(a)[:70]))
        rows.sort(reverse=True)
        print(f"\n===== {t}（计入 {len(rows)} 颗，按提交时间倒序）=====")
        for sub, aid, nm, nt, eff, ex in rows:
            print(f"  {sub}  {aid:10s} {nm:24s} 挂塔={nt} eff={eff}")
            print(f"      {ex}")

    # 顺带试平台金字塔端点
    for ep in ("/users/self/pyramids", "/users/self/pyramid-themes",
               "/users/self/activities/pyramids"):
        try:
            r = await brain._request("GET", f"{brain.base_url}{ep}")
            print(f"\n[{ep}] HTTP {r.status_code}: {r.text[:200]}")
        except Exception as e:
            print(f"\n[{ep}] ERR {str(e)[:80]}")


if __name__ == "__main__":
    asyncio.run(main())
