#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""补拉缺表达式的候选 -> 合并回 merged 文件并重聚类。"""
import asyncio
import json
import re
import sys
from pathlib import Path
from collections import defaultdict

WQ_ROOT = Path(r"D:\coding\traeCN_project\wqb")
sys.path.insert(0, str(WQ_ROOT / "world-quant-brain-mcp"))

RD = WQ_ROOT / "research-data"
MERGED = RD / "submittable_merged_20260901.json"

reps = json.load(open(MERGED, encoding="utf-8"))
need = [r for r in reps if not r["expr"]]
print(f"[INFO] 需补拉表达式: {len(need)}")


async def main():
    from brain_api import BrainApiClient
    brain = BrainApiClient()
    await brain.ensure_authenticated()

    sem = asyncio.Semaphore(3)
    got = {}

    async def one(r):
        for attempt in range(3):
            try:
                async with sem:
                    d = await brain._request(
                        "GET", f"{brain.base_url}/alphas/{r['id']}")
                    j = d.json()
                raw = j.get("regular")
                code = raw.get("code") if isinstance(raw, dict) else raw
                if code:
                    got[r["id"]] = code
                    print(f"  [OK] {r['id']:<10} {str(code)[:68]}")
                else:
                    print(f"  [--] {r['id']:<10} 无 code status={j.get('status')}")
                return
            except Exception as e:
                if attempt == 2:
                    print(f"  [ERR] {r['id']:<10} {type(e).__name__}: {str(e)[:70]}")
                else:
                    await asyncio.sleep(3)

    await asyncio.gather(*[one(r) for r in need])

    for r in reps:
        if r["id"] in got:
            r["expr"] = got[r["id"]]
            r["_expr_fetched"] = True

    FIELD_RE = re.compile(r"\b([a-z][a-z0-9]*_[a-z0-9_]+)")

    def sig(expr):
        if not expr:
            return None
        skeleton = re.sub(r"\d+(?:\.\d+)?", "#", expr)
        skeleton = re.sub(r"\s+", "", skeleton)
        return skeleton + "||" + ",".join(sorted(set(FIELD_RE.findall(expr))))

    fams = defaultdict(list)
    nofam = []
    for r in reps:
        s = sig(r["expr"])
        (fams[s].append(r) if s else nofam.append(r))

    out = []
    for s, members in fams.items():
        members.sort(key=lambda x: (-(x["fitness"] or 0), -(x["sharpe"] or 0)))
        best = members[0]
        best["fam_size"] = len(members)
        best["fam_members"] = [m["id"] for m in members[1:]]
        out.append(best)
    for r in nofam:
        r.setdefault("fam_size", 1)
        r["fam_members"] = []
        out.append(r)
    out.sort(key=lambda x: (-(x["fitness"] or 0), -(x["sharpe"] or 0)))

    json.dump(out, open(MERGED, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print()
    print(f"[INFO] 补拉成功 {len(got)}/{len(need)}；重聚类后 {len(out)} 族 "
          f"(仍缺表达式 {len(nofam)})")
    print()
    print("=== 重聚类后各族代表（前 40） ===")
    print(f"{'#':>3} {'id':<10} {'reg':<4} {'shrp':>5} {'fit':>5} {'to':>6} {'族':>3}  字段")
    for i, r in enumerate(out[:40], 1):
        fields = sorted(set(FIELD_RE.findall(r["expr"])))
        fstr = (",".join(fields) or "?")[:44]
        print(f"{i:>3} {r['id']:<10} {str(r['region']):<4} {r['sharpe']:>5.2f} {r['fitness']:>5.2f} "
              f"{r['turnover']:>6.4f} {r['fam_size']:>3}  {fstr}")


if __name__ == "__main__":
    asyncio.run(main())
