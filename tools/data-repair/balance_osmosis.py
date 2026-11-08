#!/usr/bin/env python
"""Osmosis 收尾平衡：把每个 scope 的实际点数和精确对齐到 100,000。

背景（2026-10-21 实证，经历两轮修正）：

① 初版认知「平台 osmosisPoints 最小值是 1、不能设 0」→ 分配器把计划外 alpha
   清零时只能写 1，平 scope 点数和 = 100,000 + 计划外颗数（实测 IND/KOR 各 +12、
   GBR +3、GLB +2、DEU +1）。本脚本就是为了从各 scope 最大项扣回这些差额。

② ★ 后续修正：`0` 确实被 400 拒，但 **`null` 可以真正清零**。
   - PATCH {"osmosisPoints": 0}    -> HTTP 400 "greater than or equal to 1"
   - PATCH {"osmosisPoints": null} -> HTTP 200，回读 osmosisPoints=None
   `osmosis_core.py::zero_others` 已改为优先发 null ⇒ 正常情况下**不再产生残留**，
   本脚本退化为「复核/兜底」角色（校验每 scope 是否精确 100,000，差则从最大项扣补）。

用法：
  python tools/data-repair/balance_osmosis.py            # 预览
  python tools/data-repair/balance_osmosis.py --apply    # 写入
"""
from __future__ import annotations

import argparse
import asyncio
import json
import os
import sqlite3
import sys
from collections import defaultdict

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "world-quant-brain-mcp"))

TARGET = 100_000
# 兜底：读不到 plan 时用（2026-11-05 起 plan 含 6 个 scope，含 USA）
SCOPES_FALLBACK = {("IND", 1), ("KOR", 1), ("GBR", 1), ("GLB", 1), ("DEU", 1),
                   ("USA", 1)}
_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
DEFAULT_PLAN = os.path.join(_ROOT, "results", "osmosis_plan.json")


def plan_scopes(path: str | None = None) -> set:
    """从 plan 文件推导「应保持 100k」的 scope 集合。

    ★ 2026-11-05 修正：原实现硬编码 5 个 scope，USA 加入后会被判为「非计划 scope，不动」，
    导致 USA 的 100k 不再被校验（漏检）。改为以 plan 为准，scope 集合变化自动跟随。
    """
    try:
        plan = json.load(open(path or DEFAULT_PLAN, encoding="utf-8"))
        got = {(r["region"], r.get("delay") or 1) for r in plan if r.get("region")}
        return got or SCOPES_FALLBACK
    except Exception:
        return SCOPES_FALLBACK


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


def verify_plan(pool: list, path: str) -> int:
    """逐颗比对方案点数与平台侧 osmosisPoints（只读，不改写）。

    用于分配落库后的独立复核：确认 plan 里每一颗的实际点数确实写进去了，
    而不只是各 scope 总额恰好等于 100,000（总额对≠逐颗对）。
    """
    with open(path, encoding="utf-8") as f:
        plan = json.load(f)
    if isinstance(plan, dict):
        plan = plan.get("plan") or plan.get("items") or [
            {"alpha_id": k, "points": v} for k, v in plan.items()
            if not str(k).startswith("_")
        ]
    actual = {x["id"]: (x.get("osmosisPoints") or 0) for x in pool}
    ok, diff, miss = 0, [], []
    for e in plan:
        aid = str(e.get("alpha_id") or e.get("id") or "")
        exp = e.get("points")
        if not aid or exp is None:
            continue
        act = actual.get(aid)
        if act is None:
            miss.append((aid, exp))
        elif int(act) != int(exp):
            diff.append((aid, exp, act))
        else:
            ok += 1
    print(f"\n[verify-plan] {path}")
    print(f"  方案 {len(plan)} 颗 | 一致 {ok} | 不一致 {len(diff)} | 不在 OS 池 {len(miss)}")
    for aid, exp, act in diff[:60]:
        print(f"    x {aid}  方案 {exp:,}  实际 {act:,}  差 {act - exp:+,}")
    for aid, exp in miss[:60]:
        print(f"    ? {aid}  方案 {exp:,}  平台无此 alpha")
    if not diff and not miss:
        print("  OK 全部一致")
    return 0 if not diff and not miss else 1


async def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--no-purge", action="store_true")
    ap.add_argument("--verify-plan", default=None, metavar="PATH",
                    help="核验分配方案是否已在平台侧生效：逐颗比对 osmosisPoints 与方案值，"
                         "只打印不一致项与汇总（只读，不改写）")
    ap.add_argument("--ids", default=None, metavar="ID[,ID...]",
                    help="只打印指定 alpha_id 的平台侧 osmosisPoints（逗号分隔，只读）")
    a = ap.parse_args()

    if not a.no_purge:
        print(f"[cache] purged {purge()} 条")

    keep = plan_scopes(a.verify_plan)
    print(f"[scopes] 以 plan 为准：{sorted(f'{r}D{d}' for r, d in keep)}")

    pool = await fetch()

    if a.verify_plan:
        return verify_plan(pool, a.verify_plan)
    if a.ids:
        idx = {x["id"]: (x.get("osmosisPoints") or 0) for x in pool}
        print()
        for aid in [i.strip() for i in a.ids.split(",") if i.strip()]:
            print(f"  {aid}  {idx.get(aid, '（不在 OS 池）')}")
        return 0

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
        if k not in keep:
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
