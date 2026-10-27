#!/usr/bin/env python
"""核查 USA「OS 优质子集」（OS>=0.85）的 inv / prod 是否满足分配条件。

背景：USA 整区 41 颗 ACTIVE REGULAR 中仅 23 颗有 OS 实测数据，整区 IS 2.043 → OS 0.530
（衰减 74%）。但 OS 排序后前 10 颗（OS>=0.85）OS 均值 1.277、衰减仅 20%，
需核实这批是否满足 --drop-inv-below 1.0 与 prod<0.70 两道闸、以及是否够 10 颗门槛。
"""
from __future__ import annotations

import asyncio
import os
import sqlite3          # 仅用于 sqlite3.Row（连接本身一律走 db_connect）
import sys

_ROOT = os.path.join(os.path.dirname(__file__), "..", "..")
sys.path.insert(0, os.path.join(_ROOT, "src"))
sys.path.insert(0, os.path.join(_ROOT, "world-quant-brain-mcp"))

from wqb.db_conn import connect as db_connect  # noqa: E402

TARGET = ["WL5qXEG", "EzZbK6G", "WZdxPRk", "VdKw8Jw", "KmP73gj",
          "pGPqPXb", "AzRmNQw", "dK5ExGg", "5Glv3nn", "lAXaGXx"]

# 区域走环境变量，不写死在比较式里（区域差异属数据层，见 AGENTS.md §8.13；
# `wqb.profiles.audit.region_literal_branches` 会对 `== "USA"` 这类字面量分支报新增）。
# 缺省仍是 USA（本脚本的原始命题），要查别的区：`WQB_REGION=GBR python tools/...`。
TARGET_REGION = os.environ.get("WQB_REGION", "USA")


async def main() -> int:
    # OS 值从 DB 取（平台已清空 os 段）
    con = db_connect(os.path.join(_ROOT, "data", "wqb.db"), readonly=True)
    con.row_factory = sqlite3.Row
    db = {r["alpha_id"]: dict(r) for r in con.execute(
        "SELECT alpha_id, sharpe, os_sharpe FROM alphas WHERE os_sharpe IS NOT NULL"
    ).fetchall()}
    con.close()

    from brain_api import brain_client
    await brain_client.ensure_authenticated()
    rows: list = []
    off = 0
    for _ in range(50):
        r = await brain_client.get_user_alphas(stage="OS", limit=100, offset=off)
        pl = r["result"] if isinstance(r, dict) and isinstance(r.get("result"), dict) else r
        res = pl.get("results", []) or []
        if not res:
            break
        rows += res
        if not pl.get("next"):
            break
        off += 100

    usa = {x["id"]: x for x in rows if (x.get("settings") or {}).get("region") == TARGET_REGION}

    print(f"{'alpha':<10}{'平台id':<12}{'inv':>7}{'IS':>7}{'OS':>7}{'prod':>9}{'判定':<10}")
    print("-" * 66)
    passed, failed = [], []
    for t in TARGET:
        m = [v for k, v in usa.items() if k.startswith(t)]
        if not m:
            print(f"{t:<10}(未在平台找到)")
            continue
        x = m[0]
        isd = x.get("is") or {}
        inv = (isd.get("investabilityConstrained") or {}).get("sharpe")
        prod = isd.get("prodCorrelation")
        if prod is None:
            prod = x.get("prod")
        osv = db.get(x["id"], {}).get("os_sharpe")
        isv = isd.get("sharpe") or 0.0

        ok_inv = inv is not None and inv >= 1.0
        ok_prod = prod is not None and prod < 0.70
        if ok_inv and ok_prod:
            verdict = "✔ 可用"
            passed.append((t, inv, prod, osv))
        elif not ok_inv:
            verdict = "inv<1.0"
            failed.append((t, "inv", inv))
        else:
            verdict = "prod>=0.70"
            failed.append((t, "prod", prod))

        inv_s = f"{inv:.3f}" if inv is not None else "None"
        prod_s = f"{prod:.4f}" if prod is not None else "None"
        os_s = f"{osv:.2f}" if osv is not None else "-"
        print(f"{t:<10}{x['id']:<12}{inv_s:>7}{isv:>7.2f}{os_s:>7}{prod_s:>9}{verdict:<10}")

    print()
    print(f"通过双闸: {len(passed)} 颗  |  被剔: {len(failed)} 颗")
    if passed:
        avg_inv = sum(p[1] for p in passed) / len(passed)
        avg_os = sum(p[3] for p in passed if p[3] is not None) / max(1, len([p for p in passed if p[3] is not None]))
        print(f"  → 平均 inv {avg_inv:.3f} | 平均 OS {avg_os:.3f}")
        print(f"  → 10 颗门槛: {'满足 ✔' if len(passed) >= 10 else f'不足，差 {10 - len(passed)} 颗 ✘'}")
    for f_ in failed:
        print(f"  剔除 {f_[0]}: {f_[1]}={f_[2]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(asyncio.run(main()))
