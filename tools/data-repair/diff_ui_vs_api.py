#!/usr/bin/env python
"""对比平台 UI（Genius Status 页）点数与 API 拉取点数，定位口径差异。

UI 截图（2026-10-21 15:52）显示：
  KOR/D1 126,148 (32颗) | IND/D1 111,359 (43颗) | GLB 100,001 (11) | EUR 12 (12)
  DEU 99,999 (10) | GBR 100,000 (18)

而 API（stage=OS, ACTIVE+REGULAR 过滤）显示每 scope 恰 ~100k。
本脚本：拉 stage=OS 全量（不过滤 type/status），按 scope 统计 pts 总和与颗数，
逐颗列出 pts>1 的明细，找出 UI 多出来的点数/颗数来自哪。
"""
from __future__ import annotations

import asyncio
import os
import sys
from collections import defaultdict

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "world-quant-brain-mcp"))


async def go() -> list:
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


pool = asyncio.run(go())
print(f"stage=OS 全量 {len(pool)} 颗\n")

by: dict = defaultdict(list)
for x in pool:
    st = x.get("settings") or {}
    pts = x.get("osmosisPoints") or 0
    by[(st.get("region"), st.get("delay"))].append({
        "id": x.get("id"), "pts": pts,
        "status": x.get("status"), "type": x.get("type"),
        "ds": (x.get("dateSubmitted") or "")[:10],
        "classi": [c.get("id") for c in (x.get("classifications") or []) if isinstance(c, dict)],
    })

UI = {("IND", 1): (111359, 43), ("KOR", 1): (126148, 32), ("GLB", 1): (100001, 11),
      ("EUR", 1): (12, 12), ("DEU", 1): (99999, 10), ("GBR", 1): (100000, 18)}

print(f"{'scope':<9}{'API颗':>6}{'API pts>1':>10}{'API点数和':>11}   UI点数/颗数       差")
print("=" * 74)
for k in sorted(by, key=lambda k: -sum(x["pts"] for x in by[k])):
    al = by[k]
    n_all = len(al)
    gt1 = sum(1 for x in al if x["pts"] > 1)
    tot = sum(x["pts"] for x in al)
    ui = UI.get(k)
    ui_s = f"{ui[0]:,}/{ui[1]}" if ui else "-"
    diff = f"{tot - ui[0]:+,} 点, {n_all - ui[1]:+d} 颗" if ui else ""
    print(f"{k[0]}D{k[1]:<7}{n_all:>6}{gt1:>10}{tot:>11,}   {ui_s:<18}{diff}")

print("\n=== IND / KOR 逐颗明细（只看 pts>1 的）===")
for k in [("IND", 1), ("KOR", 1)]:
    al = sorted(by[k], key=lambda x: -x["pts"])
    print(f"\n--- {k[0]}D{k[1]} ---")
    for x in al:
        if x["pts"] <= 1:
            continue
        print(f"  {x['id']:<11} pts={x['pts']:>7,}  {x['status']:<10} {x['type']:<10} "
              f"sub={x['ds']}  {','.join(x['classi'])[:40]}")

# 非 ACTIVE 但 pts>0 的（残留嫌疑）
print("\n=== 非 ACTIVE 或 非 REGULAR 但仍有 pts>0 的（残留嫌疑）===")
cnt = 0
for k, al in by.items():
    for x in al:
        if (x["status"] != "ACTIVE" or x["type"] != "REGULAR") and x["pts"] > 0:
            print(f"  {k[0]}D{k[1]}  {x['id']:<11} pts={x['pts']:>7,}  "
                  f"{x['status']} / {x['type']}  sub={x['ds']}")
            cnt += 1
print(f"共 {cnt} 颗")
