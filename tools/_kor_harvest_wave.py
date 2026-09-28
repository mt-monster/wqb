#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""_kor_harvest_wave.py — 用 MCP 已验证的 harvest_multisim_alphas 批量收批并落库。

背景（2026-09-28）：本轮 KOR/s2_fundamental17_d1 波用 tools/harvest_multisim.py 收批时
21 个 multisim 里 20 个报 HTTP 404，而同一 ID 走 MCP harvest_multisim_alphas 正常返回 8 条
—— 证明是 CLI 侧路径/鉴权问题，不是平台问题。为避免逐条 MCP 调用把大 payload 灌进
Agent 上下文，这里直接复用 MCP 的同一实现函数收批，产出只打印紧凑汇总。

用法: python tools/_kor_harvest_wave.py --ids-file cache/_kor_msids.txt --region KOR --wave <wave>
运行环境: MCP venv
"""
from __future__ import annotations

import argparse
import asyncio
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "world-quant-brain-mcp"))
sys.path.insert(0, str(REPO / "src"))


async def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ids-file", required=True)
    ap.add_argument("--region", required=True)
    ap.add_argument("--wave", required=True)
    ap.add_argument("--dataset", default=None)
    a = ap.parse_args()

    from tools_sim import harvest_multisim_alphas  # MCP 同源实现
    from wqb.store import CampaignStore

    ids = [l.strip() for l in Path(a.ids_file).read_text().splitlines() if l.strip()]
    all_rows, ok, fail = [], 0, []
    for i, mid in enumerate(ids, 1):
        try:
            res = await harvest_multisim_alphas(f"/simulations/{mid}")
        except Exception as e:
            fail.append((mid, f"exc: {e}"))
            continue
        alphas = res.get("alphas") or []
        if not alphas:
            fail.append((mid, f"0 alphas/{res.get('error') or 'no children'}"))
            continue
        ok += 1
        for al in alphas:
            m = al.get("metrics") or {}
            ra = al.get("ra") or {}
            all_rows.append({
                "id": al.get("alpha_id") or al.get("id"),
                "code": al.get("code") or al.get("expression"),
                "status": al.get("status"),
                "sharpe": m.get("sharpe"),
                "fitness": m.get("fitness"),
                "turnover": m.get("turnover"),
                "returns": m.get("returns"),
                "drawdown": m.get("drawdown"),
                "margin": m.get("margin"),
                "two_year_sharpe": m.get("two_year_sharpe"),
                "sub_universe_sharpe": m.get("sub_universe_sharpe"),
                "long_count": m.get("longCount"),
                "short_count": m.get("shortCount"),
                "pnl": m.get("pnl"),
                "book_size": m.get("bookSize"),
                "ra_failed_checks": ra.get("ra_failed_checks"),
            })
        print(f"[{i}/{len(ids)}] {mid}: {len(alphas)} alphas OK", flush=True)

    # 落库
    store = CampaignStore(str(REPO / "data" / "wqb.db"))
    try:
        n = store.upsert_backtest_rows(a.region, a.wave, all_rows, dataset=a.dataset)
    finally:
        store.close()

    sh = [r["sharpe"] for r in all_rows if isinstance(r.get("sharpe"), (int, float))]
    fit = [r["fitness"] for r in all_rows if isinstance(r.get("fitness"), (int, float))]
    print("\n=== 汇总 ===")
    print(f"multisim 成功 {ok}/{len(ids)}；失败 {len(fail)}")
    for mid, why in fail[:8]:
        print(f"  ✗ {mid}: {why}")
    print(f"alpha 行 {len(all_rows)} 条，落库 {n} 行")
    if sh:
        top = sorted(all_rows, key=lambda r: -abs(r["sharpe"] or 0))[:8]
        print(f"max|sharpe|={max(abs(x) for x in sh):.3f}  max|fitness|={max(abs(x) for x in fit):.3f}" if fit else "")
        print("Top8 by |sharpe|:")
        for r in top:
            print(f"  {r['id']}  S={r['sharpe']:.2f} F={r['fitness']:.2f} 2Y={r['two_year_sharpe']} "
                  f"to={r['turnover']:.3f}  {str(r['code'])[:78]}")
    import statistics
    if sh:
        print(f"\n|S|>=1.58 的条数: {sum(1 for x in sh if abs(x) >= 1.58)}")
        print(f"|S|>=0.5 的条数 : {sum(1 for x in sh if abs(x) >= 0.5)}")


if __name__ == "__main__":
    asyncio.run(main())
