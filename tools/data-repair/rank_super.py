#!/usr/bin/env python
"""列出全部 ACTIVE SUPER 的指标，按 investability Sharpe 排名，用于「每 scope 只纳入 top N」决策。

★ 2026-10-21 重构（两处口径修正，务必保持）：
  ① **不再按 prod<0.70 过滤**。用户 2026-10-21 定：prod 相关性只影响「能否提交进账户」，
     不影响「能否配 Osmosis 点数」（官方《Osmosis Allocation Guide》全文无 prod；
     论坛两套分配方案均无 prod 筛选；分配的真实硬门槛是 `COMPENSATED_ALPHA`）。
     旧版写死 `prod<0.70`，导致它报的 TOP10 与分配器实际选择不一致（88vKp8Va/wpjrMnz5
     被它当作入榜，实际分配器选的是 A1NQ57NW/rKOPg9gd）。
  ② **排名口径改为「每 scope topN」**，与 `osmosis_allocate.py --super-top-n N` 一致。
     旧的「全局 top10」会让小池 scope 被大池 scope 挤空（IND 的 11 颗 inv 集中在
     2.15~3.98 窄带，全局门槛线 3.12 正切在带子中间 ⇒ IND 只剩 2 颗）。
"""
from __future__ import annotations

import asyncio
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "world-quant-brain-mcp"))

ALLOC = {"IND", "KOR", "GBR", "GLB", "DEU"}   # 可分配区
EXCL = {"USA", "MEA", "EUR", "ASI", "CHN", "TWN", "HKG", "JPN", "AMR"}
TOP_N = 4                                     # 与 --super-top-n 保持一致
SUPER_MAX_PTS = 10_000                        # 与 --super-max-pts 保持一致


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
sup = []
for x in pool:
    if x.get("type") != "SUPER" or x.get("status") != "ACTIVE":
        continue
    st = x.get("settings") or {}
    isd = x.get("is") or {}
    prod = isd.get("prodCorrelation")
    if prod is None:
        prod = x.get("prod")
    sup.append({
        "id": x["id"], "reg": st.get("region"), "delay": st.get("delay"),
        "is": isd.get("sharpe") or 0.0,
        # ⚠ investability 在 is 子对象里；顶层 x["investabilityConstrained"] 恒为 None
        "inv": (isd.get("investabilityConstrained") or {}).get("sharpe"),
        "prod": prod, "pts": x.get("osmosisPoints") or 0,
        "ds": (x.get("dateSubmitted") or "")[:10],
    })

cand = [s for s in sup if s["reg"] in ALLOC and s["inv"] is not None]
cand.sort(key=lambda s: -s["inv"])

print(f"\n可分配区 ACTIVE SUPER 共 {len([s for s in sup if s['reg'] in ALLOC])} 颗，"
      f"其中 inv 可得的 {len(cand)} 颗（**不看 prod**，仅作参考列示）\n")

# ── 全局视角（仅供对比，不是分配口径）──
print(f"{'#':<4}{'id':<12}{'区':<6}{'inv':>7}{'IS':>7}{'prod':>8}{'当前pts':>10}{'提交':<12}")
print("=" * 68)
for i, s in enumerate(cand, 1):
    print(f"{i:<4}{s['id']:<12}{s['reg']:<6}{s['inv']:>7.3f}{s['is']:>7.2f}"
          f"{(s['prod'] if s['prod'] is not None else -1):>8.4f}{s['pts']:>10,}  {s['ds']}")

# ── ★ 真实分配口径：每 scope topN ──
print(f"\n\n{'=' * 72}")
print(f"★ 真实分配口径：每 scope 取 inv 前 {TOP_N} 颗（升序排列，x = 会被清零）")
print("=" * 72)
keep_all = []
for reg in sorted(ALLOC, key=lambda r: -max([s["inv"] for s in cand if s["reg"] == r] or [0])):
    grp = sorted([s for s in cand if s["reg"] == reg], key=lambda s: -s["inv"])
    if not grp:
        print(f"\n[{reg}] 无 inv 可得的 SUPER")
        continue
    kept = grp[:TOP_N]
    keep_all.extend(kept)
    kept_ids = {s["id"] for s in kept}
    print(f"\n[{reg}] {len(grp)} -> {len(kept)} 颗")
    for s in grp:
        tag = "  " if s["id"] in kept_ids else "x "
        print(f"  {tag}{s['id']:<12}inv={s['inv']:>6.3f}  IS={s['is']:>5.2f}  "
              f"prod={(s['prod'] if s['prod'] is not None else -1):.4f}  pts={s['pts']:>7,}")

print(f"\n\n合计保留 {len(keep_all)} 颗。单 scope 内 SA 预算约 "
      f"{100 * 0.22:.0f}k，若某 scope SA 颗数 < 3，单颗会逼近/触及上限 "
      f"{SUPER_MAX_PTS:,} —— 分配器已按该上限封顶，超额回流 RA。")

print("\n--- 排除区 SUPER（不参与排名，会被清零）---")
for s in sup:
    if s["reg"] in EXCL:
        print(f"    {s['id']:<12}{s['reg']:<6}inv={(s['inv'] if s['inv'] is not None else -1):.3f}"
              f"  IS={s['is']:.2f}  prod={s['prod']}  pts={s['pts']:,}")
