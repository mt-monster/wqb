#!/usr/bin/env python
"""Osmosis 分配快照（写 wqb.db::osmosis_alloc_history + osmosis_scope_snapshot，按周跑）。

## 为什么需要这个脚本（2026-11-10）

`osmosis_rank_snapshot.py` 只存账户级 `dailyOsmosisRank` 一行。但官方机制是：
**每天的 rank = 各已分配 scope「当日 PnL 横截面排名」的算术平均**，且用的是
**锁后第 8 天起生效一周**的那一版分配。⇒ 想解释「rank 今天为什么掉」，
必须能重建「那天生效的是哪一版分配、每个 scope 里放了哪些颗、各多少点」。

本地此前只有 `results/osmosis_plan.json`（覆盖式 canonical 快照，129 颗），
写一次就被下一次覆盖，**没有时序**；`alphas` 表也没有 `osmosis_points` 列。
本脚本把平台侧真实分配（`osmosisPoints`）按日/周落进 DB，形成 vintage 序列。

## 平台实测（2026-11-10，全部只读）

- `osmosisPoints` 在 `GET /users/self/alphas` 的每条记录上（分页 limit=100）。
- `is.sharpe` / `is.prodCorrelation` / `is.selfCorrelation` 同一条记录内可得。
- **per-scope rank 无端点**：`region` / `delay` / `scope` / `stage=osmosis_scope`
  参数全被 `/consultant/boards/leader` 忽略，恒返回同一账户行。
- **per-alpha OS 日 PnL 无端点**：`/alphas/{id}/recordsets/pnl` 只到 IS 期末
  2023-12-29，`startDate` / `os` / `is` / `version=2.0` 参数全部无效。
  ⇒ combo 级 PnL 无法自建，`osmosis_scope_snapshot` 里的 scope 质量只能是
  **点数加权代理**（`wavg_*`），不是真实 combo 表现。这一层限制不可绕过，
  已在 `LEGACY` 注明，别再用「加个参数试试」重走一遍。

## 落库

`osmosis_alloc_history`（一行 = 某日某颗的点数）
  snapshot_date / alpha_id / scope / region / delay / universe / alpha_type /
  status / points / is_sharpe / prod_corr

`osmosis_scope_snapshot`（一行 = 某日某 scope 的聚合）
  snapshot_date / scope / n_alphas / total_points / top1_share / hhi /
  wavg_is_sharpe / wavg_prod / n_with_metrics

两个表都以 snapshot_date 为第一主键 ⇒ 同日重跑先删当日再写，天然幂等。

## 用法

  PYTHONPATH=world-quant-brain-mcp python tools/data-repair/osmosis_alloc_snapshot.py
  PYTHONPATH=world-quant-brain-mcp python tools/data-repair/osmosis_alloc_snapshot.py --dry-run
"""
from __future__ import annotations

import argparse
import asyncio
import json
import os
import sys
from datetime import datetime, timedelta, timezone

_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, os.path.join(_ROOT, "world-quant-brain-mcp"))
sys.path.insert(0, _ROOT)
sys.path.insert(0, os.path.join(_ROOT, "src"))

DB = os.path.join(_ROOT, "data", "wqb.db")
CST = timezone(timedelta(hours=8))

PAGE = 100
STATUSES = ("ACTIVE", "DECOMMISSIONED")
EXPECTED_SCOPE_TOTAL = 100_000
MIN_SCOPE_ALPHAS = 10

ALLOC_COLS = [
    ("snapshot_date", "TEXT NOT NULL"),
    ("alpha_id", "TEXT NOT NULL"),
    ("scope", "TEXT NOT NULL"),
    ("region", "TEXT"),
    ("delay", "INTEGER"),
    ("universe", "TEXT"),
    ("alpha_type", "TEXT"),
    ("status", "TEXT"),
    ("points", "INTEGER"),
    ("is_sharpe", "REAL"),
    ("prod_corr", "REAL"),
]
ALLOC_PK = "PRIMARY KEY (snapshot_date, alpha_id)"

SCOPE_COLS = [
    ("snapshot_date", "TEXT NOT NULL"),
    ("scope", "TEXT NOT NULL"),
    ("n_alphas", "INTEGER"),
    ("total_points", "INTEGER"),
    ("top1_share", "REAL"),
    ("hhi", "REAL"),
    ("wavg_is_sharpe", "REAL"),
    ("wavg_prod", "REAL"),
    ("n_with_metrics", "INTEGER"),
]
SCOPE_PK = "PRIMARY KEY (snapshot_date, scope)"


def ensure_tables(con) -> None:
    for name, cols, pk in (
        ("osmosis_alloc_history", ALLOC_COLS, ALLOC_PK),
        ("osmosis_scope_snapshot", SCOPE_COLS, SCOPE_PK),
    ):
        body = ",\n  ".join([f"{n} {t}" for n, t in cols] + [pk])
        con.execute(f"CREATE TABLE IF NOT EXISTS {name} (\n  {body}\n)")


async def fetch_allocated(client) -> list[dict]:
    """拉全部 ACTIVE/DECOMMISSIONED，只留有 osmosisPoints 的。"""
    out: list[dict] = []
    seen: set[str] = set()
    for status in STATUSES:
        offset = 0
        while True:
            r = await client._request(
                "GET", client.base_url + "/users/self/alphas",
                params={"limit": PAGE, "offset": offset, "status": status},
            )
            r.raise_for_status()
            body = r.json() or {}
            rows = body.get("results") or []
            if not rows:
                break
            for x in rows:
                pts = x.get("osmosisPoints") or 0
                if pts <= 0 or x["id"] in seen:
                    continue
                seen.add(x["id"])
                st = x.get("settings") or {}
                isb = x.get("is") or {}
                out.append({
                    "alpha_id": x["id"],
                    "region": st.get("region"),
                    "delay": st.get("delay"),
                    "universe": st.get("universe"),
                    "alpha_type": x.get("type"),
                    "status": x.get("status") or status,
                    "points": int(pts),
                    "is_sharpe": isb.get("sharpe"),
                    "prod_corr": isb.get("prodCorrelation"),
                })
            offset += PAGE
            total = body.get("count") or 0
            if offset >= total:
                break
            await asyncio.sleep(0.5)
    out.sort(key=lambda d: (d["region"] or "", d["delay"] or 0, -d["points"]))
    return out


def build_scope_rows(snapshot_date: str, rows: list[dict]) -> list[dict]:
    by: dict[str, list[dict]] = {}
    for d in rows:
        scope = f"{d['region']}-D{d['delay']}"
        d["scope"] = scope
        by.setdefault(scope, []).append(d)

    out = []
    for scope, items in sorted(by.items()):
        pts = [i["points"] for i in items]
        total = sum(pts)
        top1 = max(pts) / total if total else None
        hhi = sum((p / total) ** 2 for p in pts) if total else None
        with_m = [i for i in items if i["is_sharpe"] is not None]
        wsum = sum(i["points"] for i in with_m)
        wavg_is = (sum(i["is_sharpe"] * i["points"] for i in with_m) / wsum) if wsum else None
        prods = [(i["prod_corr"], i["points"]) for i in items if i["prod_corr"] is not None]
        psum = sum(w for _, w in prods)
        wavg_prod = (sum(v * w for v, w in prods) / psum) if psum else None
        out.append({
            "snapshot_date": snapshot_date,
            "scope": scope,
            "n_alphas": len(items),
            "total_points": total,
            "top1_share": round(top1, 4) if top1 is not None else None,
            "hhi": round(hhi, 4) if hhi is not None else None,
            "wavg_is_sharpe": round(wavg_is, 4) if wavg_is is not None else None,
            "wavg_prod": round(wavg_prod, 4) if wavg_prod is not None else None,
            "n_with_metrics": len(with_m),
        })
    return out


def write(con, snapshot_date: str, rows: list[dict], scope_rows: list[dict]) -> None:
    con.execute("DELETE FROM osmosis_alloc_history WHERE snapshot_date=?", (snapshot_date,))
    con.execute("DELETE FROM osmosis_scope_snapshot WHERE snapshot_date=?", (snapshot_date,))
    con.executemany(
        "INSERT INTO osmosis_alloc_history (snapshot_date, alpha_id, scope, region, delay, "
        "universe, alpha_type, status, points, is_sharpe, prod_corr) "
        "VALUES (?,?,?,?,?,?,?,?,?,?,?)",
        [(snapshot_date, d["alpha_id"], d["scope"], d["region"], d["delay"], d["universe"],
          d["alpha_type"], d["status"], d["points"], d["is_sharpe"], d["prod_corr"])
         for d in rows],
    )
    con.executemany(
        "INSERT INTO osmosis_scope_snapshot (snapshot_date, scope, n_alphas, total_points, "
        "top1_share, hhi, wavg_is_sharpe, wavg_prod, n_with_metrics) "
        "VALUES (?,?,?,?,?,?,?,?,?)",
        [(s["snapshot_date"], s["scope"], s["n_alphas"], s["total_points"], s["top1_share"],
          s["hhi"], s["wavg_is_sharpe"], s["wavg_prod"], s["n_with_metrics"])
         for s in scope_rows],
    )
    con.commit()


async def main() -> int:
    ap = argparse.ArgumentParser(description="Osmosis 分配快照（只读平台，只写本地 DB）")
    ap.add_argument("--dry-run", action="store_true", help="只打印，不写库")
    args = ap.parse_args()

    from brain_api import brain_client
    from wqb.db_conn import connect

    snapshot_date = datetime.now(CST).strftime("%Y-%m-%d")

    await brain_client.ensure_authenticated()
    rows = await fetch_allocated(brain_client)
    if not rows:
        print("[error] 未取到任何带 osmosisPoints 的 alpha（平台分配为空或接口异常）",
              file=sys.stderr)
        return 1

    scope_rows = build_scope_rows(snapshot_date, rows)

    if not args.dry_run:
        con = connect(DB, readonly=False)
        try:
            ensure_tables(con)
            write(con, snapshot_date, rows, scope_rows)
        finally:
            con.close()

    tag = "[dry] " if args.dry_run else ""
    print(f"[ok] {tag}{snapshot_date} alphas={len(rows)} scopes={len(scope_rows)} "
          f"points_sum={sum(r['points'] for r in rows)} -> "
          f"wqb.db::osmosis_alloc_history + osmosis_scope_snapshot")
    for s in scope_rows:
        flag = ""
        if s["total_points"] != EXPECTED_SCOPE_TOTAL:
            flag = f"  [!] 点数≠{EXPECTED_SCOPE_TOTAL}"
        if s["n_alphas"] < MIN_SCOPE_ALPHAS:
            flag += f"  [!] 颗数<{MIN_SCOPE_ALPHAS}"
        print(f"  {s['scope']:<10} n={s['n_alphas']:<3} pts={s['total_points']:<7} "
              f"top1={s['top1_share']} hhi={s['hhi']} "
              f"wavgIS={s['wavg_is_sharpe']} wavgProd={s['wavg_prod']}{flag}")
    return 0


if __name__ == "__main__":
    raise SystemExit(asyncio.run(main()))
