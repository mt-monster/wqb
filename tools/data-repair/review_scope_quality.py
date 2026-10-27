#!/usr/bin/env python
"""只看每 scope 内部质量分布：investability 覆盖率、quality 长尾、集中度。

用途：判断「该 scope 是否该全分，还是只分 top-K」。
"""
from __future__ import annotations

import asyncio
import os
import sys
from collections import defaultdict

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "world-quant-brain-mcp"))
import osmosis_allocate as OA  # noqa: E402

EXCL = {"USA", "MEA"}


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
    OA.PROD_POLICY = "exclude"
    OA.PROD_MAX = 0.70
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
        reg = st.get("region")
        if reg in EXCL:
            continue
        by[(reg, st.get("delay"))].append({
            "id": x.get("id"), "inv": inv, "sharpe": isd.get("sharpe"),
            "to": isd.get("turnover"), "prod": prod,
            "pts": x.get("osmosisPoints") or 0,
        })

    print(f"\n{'scope':<9}{'n':>4}{'inv覆盖':>8}{'prod剔除':>9}{'有效n':>7}"
          f"{'top10占比':>10}{'尾部(后1/3)占比':>16}{'负q':>6}")
    print("=" * 78)
    for k in sorted(by, key=lambda k: -len(by[k])):
        al = by[k]
        n = len(al)
        inv_n = sum(1 for x in al if x["inv"] is not None)
        bad = sum(1 for x in al if x["prod"] is not None and x["prod"] >= 0.70)
        eff = [x for x in al if not (x["prod"] is not None and x["prod"] >= 0.70)]
        qs = sorted((OA.quality({
            "investability_sharpe": x["inv"], "sharpe": x["sharpe"],
            "turnover": x["to"], "prod": x["prod"], "os_sharpe": None,
        }) for x in eff), reverse=True)
        tot = sum(qs) or 1.0
        top10 = sum(qs[:10]) / tot if len(qs) >= 10 else 1.0
        tail_n = len(qs) // 3
        tail = sum(qs[-tail_n:]) / tot if tail_n else 0.0
        neg = sum(1 for q in qs if q <= 0)
        print(f"{k[0]}D{k[1]:<7}{n:>4}{inv_n:>8}{bad:>9}{len(eff):>7}"
              f"{top10*100:>9.1f}%{tail*100:>15.1f}%{neg:>6}")

    # 每个 scope 的 top10 明细（优先展示哪些区域由环境变量决定，不写死在比较式里 ——
    # `wqb.profiles.audit.region_literal_branches` 对 `not in ("EUR",)` 这类字面量报新增；
    # 区域差异属数据层。缺省仍是 EUR，要换：`WQB_DETAIL_REGIONS=GBR,USA`。）
    _DETAIL_REGIONS = tuple(os.environ.get("WQB_DETAIL_REGIONS", "EUR").split(","))
    for k in sorted(by, key=lambda k: -len(by[k])):
        if k[0] not in _DETAIL_REGIONS:
            continue
        print(f"\n=== {k[0]}D{k[1]} 明细（按 quality 降序）===")
        eff = [x for x in by[k] if not (x["prod"] is not None and x["prod"] >= 0.70)]
        eff.sort(key=lambda x: -OA.quality({
            "investability_sharpe": x["inv"], "sharpe": x["sharpe"],
            "turnover": x["to"], "prod": x["prod"], "os_sharpe": None}))
        for i, x in enumerate(eff, 1):
            q = OA.quality({"investability_sharpe": x["inv"], "sharpe": x["sharpe"],
                            "turnover": x["to"], "prod": x["prod"], "os_sharpe": None})
            inv = f"{x['inv']:.3f}" if x["inv"] is not None else "  -  "
            pr = f"{x['prod']:.4f}" if x["prod"] is not None else "  -  "
            print(f"  {i:>2}. {x['id']}  inv={inv}  IS={x['sharpe']}  TO={x['to']}  "
                  f"prod={pr}  q={q:.3f}  当前pts={x['pts']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
