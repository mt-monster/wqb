#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""对合并后的候选逐颗查 type/表达式 -> 只保留 REGULAR -> 完整重聚类。

背景：扫描把 SUPER alpha 混了进来。SUPER 的 sharpe/fitness 是合成指标，
远高于单 alpha（4.3/5.02 这种），不能当 REGULAR 提交候选。
"""
import asyncio
import json
import re
import sys
from pathlib import Path
from collections import defaultdict, Counter

WQ_ROOT = Path(r"D:\coding\traeCN_project\wqb")
sys.path.insert(0, str(WQ_ROOT / "world-quant-brain-mcp"))

RD = WQ_ROOT / "research-data"
MERGED = RD / "submittable_merged_20260901.json"
OUT = RD / "submittable_regular_20260901.json"

rows = json.load(open(MERGED, encoding="utf-8"))
print(f"[INFO] 待核查: {len(rows)}")


async def main():
    from brain_api import BrainApiClient
    brain = BrainApiClient()
    await brain.ensure_authenticated()

    sem = asyncio.Semaphore(3)

    async def one(r):
        for attempt in range(3):
            try:
                async with sem:
                    resp = await brain._request(
                        "GET", f"{brain.base_url}/alphas/{r['id']}")
                j = resp.json()
                r["type"] = j.get("type")
                raw = j.get("regular")
                code = raw.get("code") if isinstance(raw, dict) else raw
                r["expr"] = code or ""
                st = j.get("settings") or {}
                r["sel_limit"] = st.get("selectionLimit")
                r["decay"] = st.get("decay")
                r["trunc"] = st.get("truncation")
                r["universe"] = st.get("universe") or r.get("universe")
                r["neut"] = st.get("neutralization") or r.get("neut")
                r["delay"] = st.get("delay") or r.get("delay")
                r["startDate"] = st.get("startDate")
                r["endDate"] = st.get("endDate")
                return
            except Exception as e:
                if attempt == 2:
                    r["type"] = "ERR"
                    r["_err"] = f"{type(e).__name__}: {str(e)[:80]}"
                else:
                    await asyncio.sleep(3)

    await asyncio.gather(*[one(r) for r in rows])

    print("\n[INFO] type 分布:", dict(Counter(r.get("type") for r in rows)))

    regular = [r for r in rows if r.get("type") == "REGULAR"]
    super_al = [r for r in rows if r.get("type") == "SUPER"]
    other = [r for r in rows if r.get("type") not in ("REGULAR", "SUPER")]

    print(f"[INFO] REGULAR={len(regular)}  SUPER={len(super_al)}  OTHER={len(other)}")

    if super_al:
        print("\n=== 被剔除的 SUPER alpha（合成指标，不可当 REGULAR 提交） ===")
        for r in sorted(super_al, key=lambda x: -(x["fitness"] or 0)):
            print(f"  {r['id']:<10} {str(r['region']):<4} shrp={r['sharpe']:>5.2f} "
                  f"fit={r['fitness']:>5.2f} selLimit={r.get('sel_limit')}")
    if other:
        print("\n=== 异常项 ===")
        for r in other:
            print(f"  {r['id']:<10} {r.get('type')} {r.get('_err','')}")

    # REGULAR 重聚类
    FIELD_RE = re.compile(r"\b([a-z][a-z0-9]*_[a-z0-9_]+)")

    def sig(expr):
        if not expr:
            return None
        sk = re.sub(r"\d+(?:\.\d+)?", "#", expr)
        sk = re.sub(r"\s+", "", sk)
        return sk + "||" + ",".join(sorted(set(FIELD_RE.findall(expr))))

    fams = defaultdict(list)
    nofam = []
    for r in regular:
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
        r["fam_size"] = 1
        r["fam_members"] = []
        out.append(r)
    out.sort(key=lambda x: (-(x["fitness"] or 0), -(x["sharpe"] or 0)))

    json.dump({"regular": out, "super": super_al, "other": other},
              open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=2)

    print(f"\n[INFO] REGULAR 重聚类: {len(out)} 族 / {len(regular)} 颗 "
          f"(缺表达式 {len(nofam)})")
    print("\n=== REGULAR 各族代表（按 fitness 降序） ===")
    print(f"{'#':>3} {'id':<10} {'reg':<4} {'shrp':>5} {'fit':>5} {'to':>6} {'族':>3}  字段")
    for i, r in enumerate(out, 1):
        fields = sorted(set(FIELD_RE.findall(r["expr"])))
        fstr = (",".join(fields) or "?")[:44]
        print(f"{i:>3} {r['id']:<10} {str(r['region']):<4} {r['sharpe']:>5.2f} {r['fitness']:>5.2f} "
              f"{r['turnover']:>6.4f} {r['fam_size']:>3}  {fstr}")
    print(f"\n[saved] {OUT}")


if __name__ == "__main__":
    asyncio.run(main())
