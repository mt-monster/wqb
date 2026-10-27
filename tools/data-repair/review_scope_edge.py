#!/usr/bin/env python
"""估每 scope 的「预期 rank 代理」= 权重加权平均 investability Sharpe。

官方：Daily Osmosis Rank = 各已分配 scope 的 rank 取**算术平均**（不是按点数加权），
且 "Performance is not proportional to number of scopes"。
⇒ 加一个 scope 是否加分，取决于该 scope 的预期 rank 是否好于现有 scope 的平均。

代理指标（越接近真实越好）：
  wavg_inv  = Σ(pts × inv)/Σpts          —— 组合后的约束后 Sharpe 代理（未计相关性）
  wavg_is   = Σ(pts × IS)/Σpts
  n_eff     = 有效颗数（prod<0.7）
  med_prod  = prod 中位数（越低越独特）
"""
from __future__ import annotations

import asyncio
import os
import statistics
import sys
from collections import defaultdict

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "world-quant-brain-mcp"))

EXCL_DEFAULT = {"USA", "MEA"}


async def fetch_pool() -> list:
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


def main() -> int:
    pool = asyncio.run(fetch_pool())
    act = [x for x in pool if x.get("status") == "ACTIVE" and x.get("type") == "REGULAR"]

    by: dict = defaultdict(list)
    for x in act:
        st = x.get("settings") or {}
        isd = x.get("is") or {}
        prod = isd.get("prodCorrelation")
        if prod is None:
            prod = x.get("prod")
        inv = (isd.get("investabilityConstrained") or {}).get("sharpe")
        by[(st.get("region"), st.get("delay"))].append({
            "id": x.get("id"), "inv": inv, "sharpe": isd.get("sharpe") or 0.0,
            "to": isd.get("turnover") or 0.0, "prod": prod,
            "pts": x.get("osmosisPoints") or 0,
            "ds": (x.get("dateSubmitted") or "")[:10],
        })

    print(f"\n{'scope':<9}{'ACTIVE':>7}{'已分配':>7}{'有效':>6}{'wavg_inv':>10}"
          f"{'wavg_IS':>9}{'med_prod':>10}{'prod缺失':>9}{'≥10颗':>7}")
    print("=" * 76)
    rows = []
    for k in sorted(by, key=lambda k: -len(by[k])):
        al = by[k]
        got = [x for x in al if x["pts"] > 1]
        eff = [x for x in al if not (x["prod"] is not None and x["prod"] >= 0.70)]
        base = got or eff
        if not base:
            continue
        # ★ 2026-10-21 修正：未分配的 scope 里每颗 pts=0，旧式 `sum(pts) or 1.0`
        # 会让分子分母同时归零 ⇒ wavg_inv 恒为 0.000，无法评估候选区。
        # 现改为：已分配用实际点数，未分配按**等权 1**计（等价于该区等权组合的质量）。
        def w(x: dict) -> float:
            return x["pts"] if x["pts"] > 1 else 1.0

        tot = sum(w(x) for x in base) or 1.0
        wavg_inv = sum(w(x) * (x["inv"] if x["inv"] is not None else x["sharpe"] * 0.65)
                       for x in base) / tot
        wavg_is = sum(w(x) * x["sharpe"] for x in base) / tot
        pr = [x["prod"] for x in base if x["prod"] is not None]
        med = statistics.median(pr) if pr else None
        miss = sum(1 for x in base if x["prod"] is None)
        flag = "YES" if len(al) >= 10 else f"差{10 - len(al)}"
        print(f"{k[0]}D{k[1]:<7}{len(al):>7}{len(got):>7}{len(eff):>6}{wavg_inv:>10.3f}"
              f"{wavg_is:>9.3f}{(f'{med:.3f}' if med is not None else '  -  '):>10}"
              f"{miss:>9}{flag:>7}")
        rows.append((k, len(al), len(got), wavg_inv, wavg_is, med, flag))

    cur = [r for r in rows if r[2] >= 10]
    if cur:
        avg = sum(r[3] for r in cur) / len(cur)
        print("-" * 76)
        print(f"当前已启用 {len(cur)} 个 scope 的平均 wavg_inv = {avg:.3f}")
        for r in rows:
            if r[2] >= 10:
                continue
            if r[1] >= 10:
                d = r[3] - avg
                print(f"  候选 {r[0][0]}D{r[0][1]}：wavg_inv={r[3]:.3f} vs 现有均值 {avg:.3f} "
                      f"→ 差 {d:+.3f} {'（加入会拉高平均 ✔）' if d > 0 else '（加入会拉低平均 ✘）'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
