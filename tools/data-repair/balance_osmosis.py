#!/usr/bin/env python
"""Osmosis 收尾平衡：把每个 scope 的实际点数和精确对齐到 100,000。

背景（2026-10-21 实证，经历两轮修正）：

① 初版认知「平台 osmosisPoints 最小值是 1、不能设 0」→ 分配器把计划外 alpha
   清零时只能写 1，平 scope 点数和 = 100,000 + 计划外颗数（实测 IND/KOR 各 +12、
   GBR +3、GLB +2、DEU +1）。本脚本就是为了从各 scope 最大项扣回这些差额。

② ★ 后续修正：`0` 确实被 400 拒，但 **`null` 可以真正清零**。
   - PATCH {"osmosisPoints": 0}    -> HTTP 400 "greater than or equal to 1"
   - PATCH {"osmosisPoints": null} -> HTTP 200，回读 osmosisPoints=None
   `osmosis_allocate.py::zero_others` 已改为优先发 null ⇒ 正常情况下**不再产生残留**，
   本脚本退化为「复核/兜底」角色（校验每 scope 是否精确 100,000，差则从最大项扣补）。

用法：
  python tools/data-repair/balance_osmosis.py            # 预览
  python tools/data-repair/balance_osmosis.py --apply    # 写入
"""
from __future__ import annotations

import argparse
import asyncio
import os
import sqlite3
import sys
from collections import defaultdict

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "world-quant-brain-mcp"))

TARGET = 100_000
SCOPES_KEEP = {("IND", 1), ("KOR", 1), ("GBR", 1), ("GLB", 1), ("DEU", 1)}


def purge() -> int:
    from wqb.db_conn import connect
    con = connect(readonly=False)
    n = con.execute("DELETE FROM api_cache WHERE cache_key LIKE 'user_alphas%'").rowcount
    con.commit()
    con.close()
    return n


async def fetch() -> list:
    from brain_api import brain_client
    rows: list = []
    off = 0
    for _ in range(200):
        r = await brain_client.get_user_alphas(stage="OS", limit=100, offset=off)
        pl = r["result"] if isinstance(r, dict) and isinstance(r.get("result"), dict) else r
        res = pl.get("results", []) or []
        if not res:
            break
        rows.extend(res)
        if not pl.get("next"):
            break
        off += 100
    return rows


async def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--no-purge", action="store_true")
    a = ap.parse_args()

    if not a.no_purge:
        print(f"[cache] purged {purge()} 条")

    pool = await fetch()
    by: dict = defaultdict(list)
    for x in pool:
        st = x.get("settings") or {}
        k = (st.get("region"), st.get("delay"))
        by[k].append({"id": x["id"], "pts": x.get("osmosisPoints") or 0,
                      "type": x.get("type"), "status": x.get("status")})

    print(f"\n{'scope':<9}{'颗数':>6}{'实际合计':>10}{'目标':>9}{'差额':>8}")
    print("=" * 44)
    fixes = []
    for k in sorted(by, key=lambda k: -(sum(x["pts"] for x in by[k]))):
        al = [x for x in by[k] if x["pts"] > 0]
        tot = sum(x["pts"] for x in al)
        if k not in SCOPES_KEEP:
            if tot > 0:
                print(f"{k[0]}D{k[1]:<7}{len(al):>6}{tot:>10,}{'—':>9}{'（非计划scope，不动）':>8}")
            continue
        diff = tot - TARGET
        print(f"{k[0]}D{k[1]:<7}{len(al):>6}{tot:>10,}{TARGET:>9,}{diff:>+8,}")
        if diff != 0:
            top = max(al, key=lambda x: x["pts"])
            newp = top["pts"] - diff
            if newp < 1:
                print(f"    !! 最大项 {top['id']} 仅 {top['pts']} 点，扣 {diff} 会到 {newp}<1，跳过")
                continue
            fixes.append((k, top["id"], top["pts"], newp, diff))

    if not fixes:
        print("\n所有计划内 scope 已精确对齐 100,000 ✓")
        return 0

    print("\n待修正：")
    for k, aid, old, new, diff in fixes:
        print(f"  {k[0]}D{k[1]}  {aid}  {old:,} -> {new:,}  (差额 {diff:+,})")

    if not a.apply:
        print("\n[dry-run] 加 --apply 写入")
        return 0

    from brain_api import brain_client
    await brain_client.ensure_authenticated()
    base = brain_client.base_url
    for k, aid, old, new, diff in fixes:
        r = await brain_client._request("PATCH", f"{base}/alphas/{aid}",
                                        json={"osmosisPoints": int(new)})
        ok = r.status_code < 400
        print(f"  PATCH {aid} -> {new:,}  {'OK' if ok else 'FAIL ' + (getattr(r, 'text', '') or '')[:120]}")

    # 复核
    print("\n[复核]")
    purge()
    pool2 = await fetch()
    by2: dict = defaultdict(int)
    for x in pool2:
        st = x.get("settings") or {}
        k = (st.get("region"), st.get("delay"))
        if k in SCOPES_KEEP:
            by2[k] += x.get("osmosisPoints") or 0
    for k in sorted(by2, key=lambda k: -by2[k]):
        flag = "✓" if by2[k] == TARGET else f"✗ 差 {by2[k] - TARGET:+,}"
        print(f"  {k[0]}D{k[1]}  {by2[k]:>9,} / {TARGET:,}  {flag}")
    return 0


if __name__ == "__main__":
    raise SystemExit(asyncio.run(main()))
