# -*- coding: utf-8 -*-
"""harvest_expr.py — 按「simulation id」收割多维仿真批次，并**打印表达式**（供人工反解参数）。

为什么要这个（而不是 tools/harvest_multisim.py）：
  - `harvest_multisim.py` 按 alpha_id 关联 expressions 表，**不打印表达式原文**；
    而平台返回的 children 顺序与 expressions 表行序**不一致**（2026-10-05 实测），
    只按顺序对应会把参数张冠李戴 —— 曾据此误判甜点。
  - 本脚本恒打印每条结果的 `expression` 原文 + 指标，让调用方**按表达式本身**核对参数，
    不依赖任何顺序假设。

用法：
  python tracking/GBR/scripts/harvest_expr.py <sim_id> [<sim_id> ...]
  python tracking/GBR/scripts/harvest_expr.py <sim_id> --persist <wave_name> [--dataset <ds>]

指标块：`/alphas/{id}` 的 IS 指标在 **`is`** 键下（不在 `metrics`）。
"""
from __future__ import annotations

import argparse
import asyncio
import os
import re
import sqlite3
import sys
import time

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.insert(0, os.path.join(ROOT, "world-quant-brain-mcp"))

from brain_api import brain_client  # noqa: E402

# 参数反解：从表达式里抽 bf / win / tvr / axis / 字段名，便于人工核对
# ⚠ win 不能用 `ts_delta\([^,]+,(\d+)\)` —— 嵌套写法 `ts_delta(ts_backfill(f,500),11)` 里
#    `[^,]+` 会在内层逗号处断开，把 backfill 的 500 误当 win（2026-10-05 实测踩到）。
#    改用「紧邻 lambda_min 之前的那个数」定位 win。
ANNOT = [
    (re.compile(r"ts_backfill\(\s*([a-z0-9_]+)\s*,\s*(\d+)\s*\)"), lambda m: f"fld={m.group(1)}"),
    (re.compile(r",\s*(\d+)\s*\)+\s*,\s*lambda_min"), lambda m: f"win={m.group(1)}"),
    (re.compile(r"target_tvr=([0-9.]+)"), lambda m: f"tvr={m.group(1)}"),
    (re.compile(r"lambda_min=([0-9.]+)"), lambda m: f"lmin={m.group(1)}"),
    (re.compile(r"\),\s*(industry|sector|subindustry|market)\s*\)\s*$"), lambda m: f"axis={m.group(1)}"),
]


def annotate(code: str) -> str:
    tags = []
    for rx, fn in ANNOT:
        for m in rx.finditer(code or ""):
            tags.append(fn(m))
    # 主字段名：取最长的 1–2 个非算子 token（配对表达式会显示两个字段）
    OPS = {"group_rank", "ts_target_tvr_decay", "rank", "ts_delta", "ts_backfill", "subtract",
           "divide", "add", "abs", "multiply", "ts_mean", "ts_zscore", "industry", "sector",
           "subindustry", "market", "lambda_min", "lambda_max", "target_tvr", "signed_power"}
    toks = [t for t in re.findall(r"[a-z][a-z0-9_]{5,}", code or "") if t not in OPS]
    uniq = sorted(set(toks), key=lambda t: -len(t))
    if uniq:
        tags.insert(0, "field=" + "+".join(uniq[:2]))
    return " ".join(tags)


async def run(sim_ids, wave="", region="GBR", dataset=""):
    await brain_client.ensure_authenticated()
    rows = []
    for sim in sim_ids:
        r = await brain_client._request("GET", f"/simulations/{sim}")
        j = r.json()
        children = j.get("children") or []
        print(f"[{sim}] status={j.get('status')} children={len(children)}")
        for c in children:
            cr = await brain_client._request("GET", f"/simulations/{c}")
            cj = cr.json()
            aid = cj.get("alpha")
            if not aid:
                msg = (cj.get("message") or "")[:90]
                if msg:
                    print("   x ERROR:", msg)
                continue
            ar = await brain_client._request("GET", f"/alphas/{aid}")
            aj = ar.json()
            m = aj.get("is") or {}
            code = (aj.get("regular") or {}).get("code") or ""
            row = {
                "alpha_id": aid, "code": code,
                "sharpe": m.get("sharpe"), "fitness": m.get("fitness"),
                "margin": m.get("margin"), "turnover": m.get("turnover"),
                "two_year": m.get("twoYearSharpe"), "sub": m.get("subUniverseSharpe"),
                "drawdown": m.get("drawdown"),
            }
            rows.append(row)
            gap = None
            if row["fitness"] is not None:
                gap = (1.0 - row["fitness"]) * 1000  # bp 口径的相对提示
            mark = " *** F>=1.0" if (row["fitness"] or 0) >= 1.0 else ""
            print(f"   + {aid} [{annotate(code)}] S={row['sharpe']} F={row['fitness']} "
                  f"m={(row['margin'] or 0) * 1e4:.2f}bp TO={row['turnover']} "
                  f"2Y={row['two_year']} gap={gap if gap is None else f'{gap:+.2f}bp'}{mark}")
            time.sleep(1.0)  # 平台限流：连发 GET /alphas/{id} 会 rate limit

    if wave and rows:
        db = sqlite3.connect(os.path.join(ROOT, "data", "wqb.db"))
        cur = db.cursor()
        rid = cur.execute("SELECT id FROM regions WHERE name=?", (region,)).fetchone()
        if not rid:
            print(f"[harvest_expr] 区域 {region!r} 不在 regions 表，拒绝入库")
            return rows
        rid = rid[0]
        ds_name = dataset
        if not ds_name:
            cands = set()
            for r in rows:
                for f in re.findall(r"[a-z][a-z0-9_]{4,}", r.get("code") or ""):
                    h = cur.execute(
                        "SELECT d.name FROM fields fl JOIN datasets d ON d.id=fl.dataset_id"
                        " WHERE d.region_id=? AND fl.field_name=? LIMIT 1", (rid, f)).fetchone()
                    if h:
                        cands.add(h[0])
            ds_name = sorted(cands)[0] if len(cands) == 1 else ("+".join(sorted(cands)) if cands else "unknown")
        cur.execute("INSERT OR IGNORE INTO waves (region_id, wave_number, dataset_id,"
                    " expression_count, status, created_at, updated_at)"
                    " VALUES (?,?,?,?,'completed',datetime('now'),datetime('now'))",
                    (rid, wave, ds_name, len(rows)))
        cur.execute("SELECT id FROM waves WHERE region_id=? AND wave_number=?", (rid, wave))
        wid = cur.fetchone()[0]
        n = 0
        for r in rows:
            ex = cur.execute("SELECT alpha_id FROM alphas WHERE alpha_id=?", (r["alpha_id"],)).fetchone()
            vals = (r["code"], r["sharpe"], r["fitness"], r["margin"], r["turnover"],
                    r["two_year"], r["sub"], r["drawdown"], r["alpha_id"])
            if ex:
                cur.execute("UPDATE alphas SET expression=?,sharpe=?,fitness=?,margin=?,turnover=?,"
                            " two_year_sharpe=?,sub_universe_sharpe=?,drawdown=?,"
                            " updated_at=datetime('now') WHERE alpha_id=?", vals)
            else:
                cur.execute("INSERT INTO alphas (alpha_id,expression,region_id,dataset_id,universe,"
                            " delay,neutralization,sharpe,fitness,margin,turnover,two_year_sharpe,"
                            " sub_universe_sharpe,drawdown,status,created_at,updated_at)"
                            " VALUES (?,?,?,?,'TOP700',1,'STATISTICAL',?,?,?,?,?,?,?,"
                            " 'UNSUBMITTED',datetime('now'),datetime('now'))",
                            (r["alpha_id"], r["code"], rid, ds_name) + vals[1:-1])
            n += 1
        db.commit()
        db.close()
        print(f"[DB] persisted wave={wave} rows={n} dataset={ds_name}")
    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("sim_ids", nargs="+")
    ap.add_argument("--persist", default="")
    ap.add_argument("--region", default="GBR")
    ap.add_argument("--dataset", default="")
    a = ap.parse_args()
    asyncio.run(run(a.sim_ids, a.persist, a.region, a.dataset))


if __name__ == "__main__":
    main()
