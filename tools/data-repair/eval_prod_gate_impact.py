#!/usr/bin/env python
"""评估「prod>=0.70 剔除」在 Osmosis 分配中造成的损失。

## 背景（2026-10-21 查证结论）

- **官方 Osmosis 指南全文没有一处提到 prod correlation**。官方列的排除标准里，
  唯一涉及相关性的是第 9 条 "evaluate **intra-set correlations**"，指的是
  **你自己池内的互相关（self correlation）**，不是与平台产品池的 prod correlation。
- prod correlation 在官方文档里只出现在**提交前测试 CorrAll** 与**诊断视图**。
- Osmosis 分配的**唯一硬门槛是 `COMPENSATED_ALPHA`**：超每日 4 个提交限额的 alpha
  是「未计费」的，PATCH 会报 `Cannot update Osmosis points for non-compensated alpha`
  （来源：论坛 ZH87224《什么是 Non-Compensated Alpha》）。
- ⇒ **prod 只影响「能否提交」，不影响「能否分配点数」**。

本脚本量化：若改用正确口径（只按 compensated + inv 筛，不看 prod），
每个 scope 会多出多少可用 alpha、它们的 inv 分布如何。

用法：
  python tools/data-repair/eval_prod_gate_impact.py
"""
from __future__ import annotations

import asyncio
import os
import sys
from collections import defaultdict

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "world-quant-brain-mcp"))

KEEP_SCOPES = {"IND", "KOR", "GBR", "GLB", "DEU"}


async def main() -> int:
    from brain_api import brain_client
    await brain_client.ensure_authenticated()
    rows: list = []
    off = 0
    for _ in range(200):
        r = await brain_client.get_user_alphas(stage="OS", limit=100, offset=off)
        pl = r["result"] if isinstance(r, dict) and isinstance(r.get("result"), dict) else r
        res = pl.get("results", []) or []
        if not res:
            break
        rows += res
        if not pl.get("next"):
            break
        off += 100

    by: dict = defaultdict(lambda: {"prod_hi": [], "ok": [], "noncomp": 0})
    for x in rows:
        if x.get("status") != "ACTIVE":
            continue
        st = x.get("settings") or {}
        reg = st.get("region")
        if reg not in KEEP_SCOPES:
            continue
        isd = x.get("is") or {}
        prod = isd.get("prodCorrelation")
        if prod is None:
            prod = x.get("prod")
        osd = x.get("os") or {}
        checks = {c.get("name"): c.get("result") for c in (osd.get("checks") or []) if isinstance(c, dict)}
        noncomp = checks.get("COMPENSATED_ALPHA") == "WARNING"
        inv = (isd.get("investabilityConstrained") or {}).get("sharpe")

        rec = {"id": x["id"], "type": x.get("type"), "prod": prod,
               "inv": inv, "is": isd.get("sharpe"), "noncomp": noncomp}
        if noncomp:
            by[reg]["noncomp"] += 1
            continue
        if prod is not None and prod >= 0.70:
            by[reg]["prod_hi"].append(rec)
        else:
            by[reg]["ok"].append(rec)

    print("\n=== 若放开 prod 闸（只用 COMPENSATED_ALPHA + inv 筛），各 scope 多出的可用 alpha ===")
    print(f"{'scope':<6}{'当前可用':>9}{'prod>=0.7被剔':>14}{'其中inv>=1.0':>13}"
          f"{'被剔inv均值':>13}{'non-comp':>10}")
    print("=" * 70)
    total_gain = 0
    detail = []
    for reg in sorted(by):
        b = by[reg]
        oh = b["prod_hi"]
        usab = [a for a in oh if a["inv"] is not None and a["inv"] >= 1.0]
        invs = [a["inv"] for a in oh if a["inv"] is not None]
        avg = sum(invs) / len(invs) if invs else None
        total_gain += len(usab)
        print(f"{reg:<6}{len(b['ok']):>9}{len(oh):>14}{len(usab):>13}"
              f"{(f'{avg:.3f}' if avg is not None else '-'):>13}{b['noncomp']:>10}")
        for a in usab:
            detail.append((reg, a))

    print()
    if detail:
        print(f"★ 共 {total_gain} 颗 prod>=0.70 但 inv>=1.0、可正常分配点数的 alpha：")
        for reg, a in sorted(detail, key=lambda t: -(t[1]["inv"] or 0)):
            print(f"   {reg:<5}{a['id']:<10}{str(a['type']):<8}"
                  f"inv={a['inv']:.3f}  IS={a['is']:.2f}  prod={a['prod']:.4f}")
        print()
        print("⚠ 但这批 prod 高 = 与平台已上线产品高度同质；Osmosis 里它们的 PnL 仍计入你的组合，")
        print("   官方未禁止。真正的分散度风险应看 **self correlation（池内互相关）**，不是 prod。")
    else:
        print("当前没有 prod>=0.70 且 inv>=1.0 的 alpha —— 剔除无损失。")
    return 0


if __name__ == "__main__":
    raise SystemExit(asyncio.run(main()))
