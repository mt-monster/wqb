#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""harvest_batch.py — 收割 multi-sim，输出 IS 关键闸（含 investability 保留率与 limit）。

用法::  python tracking/KOR/scripts/harvest_batch.py <multisim_id> [label1 label2 ...]
"""
from __future__ import annotations
import asyncio, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "world-quant-brain-mcp"))

async def main() -> int:
    if len(sys.argv) < 2:
        print(__doc__); return 2
    mid, labels = sys.argv[1], sys.argv[2:]
    from brain_api import brain_client as brain
    await brain.ensure_authenticated()
    r = await brain._request("GET", brain.base_url + f"/simulations/{mid}")
    j = r.json() or {}
    ch = j.get("children") or ([j] if j.get("alpha") else [])
    if not ch:
        print(f"[harvest] {mid}: parent={j.get('status')} children=0（排队中或 ID 有误）"); return 1
    print(f"{'label':14s} {'alpha':10s} {'S':>6s} {'F':>6s} {'2Y':>6s} {'TO':>7s} {'INV':>6s} {'lmt':>6s} {'保留率':>6s}  RA_FAIL")
    for i, c in enumerate(ch):
        lab = labels[i] if i < len(labels) else f"c{i}"
        if isinstance(c, str):
            c = (await brain._request("GET", brain.base_url + f"/simulations/{c}")).json()
        aid = c.get("alpha")
        if not aid:
            print(f"{lab:14s} {c.get('status','')[:10]:10s} {(c.get('error') or '')[:40]}"); continue
        jj = (await brain._request("GET", brain.base_url + f"/alphas/{aid}")).json() or {}
        m, ra = jj.get("is") or {}, jj.get("ra") or {}
        inv = m.get("investability_sharpe")
        lmt = next((x.get("limit") for x in (m.get("checks") or [])
                    if x.get("name") == "LOW_INVESTABILITY_CONSTRAINED_SHARPE"), None)
        keep = f"{inv / m['sharpe'] * 100:.0f}%" if (m.get("sharpe") and inv) else "-"
        raf = ",".join(ra.get("ra_failed_checks") or []) or "ok"
        print(f"{lab:14s} {aid:10s} {m.get('sharpe')!s:>6s} {m.get('fitness')!s:>6s} "
              f"{m.get('two_year_sharpe')!s:>6s} {m.get('turnover')!s:>7s} "
              f"{inv!s:>6s} {lmt!s:>6s} {keep:>6s}  {raf}")
    return 0

if __name__ == "__main__":
    raise SystemExit(asyncio.run(main()))
