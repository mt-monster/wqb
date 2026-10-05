#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""把单发 fanout 的 checkpoint 回填 ``alphas`` 表（补真相源漏记）。

放在 ``tracking/EUR/scripts/`` 而非 ``tools/``：2026-10-04 实测 ``tools/`` 下的同名
脚本被外部清理进程**反复删除**两次（见记忆 §47.4），而 tracking 目录不受影响。

用法::

    python tracking/EUR/scripts/backfill_alphas_from_ckpt.py --tag wave299_decay2 --dataset analyst_factor_signals
    python tracking/EUR/scripts/backfill_alphas_from_ckpt.py --tag wave299_decay2 --dry-run

幂等：以 ``alpha_id`` 为键，已存在则只补 NULL 字段，不覆盖已有非空值。
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "src"))

from wqb.db_conn import connect  # noqa: E402


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--tag", required=True)
    ap.add_argument("--region", default="EUR")
    ap.add_argument("--dataset", default="risk70")
    ap.add_argument("--results-dir", default="tracking/EUR/results")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    ck = Path(ROOT) / args.results_dir / f"{args.tag}_checkpoint.json"
    if not ck.is_file():
        print(f"[x] 找不到 checkpoint: {ck}")
        return 1
    rows = [r for r in json.load(open(ck, encoding="utf-8")).get("results", [])
            if r.get("id") and r.get("id") != "DROPPED"]
    if not rows:
        print(f"[x] {args.tag} 无有效结果")
        return 1

    conn = connect(str(Path(ROOT) / "data" / "wqb.db"), timeout=60.0)
    rid = conn.execute("SELECT id FROM regions WHERE name=?", (args.region,)).fetchone()
    rid = rid[0] if rid else None
    did = conn.execute("SELECT id FROM datasets WHERE name=? AND region_id=?",
                       (args.dataset, rid)).fetchone()
    did = did[0] if did else None

    ins = upd = 0
    for r in rows:
        aid = r["id"]
        margin = (r.get("margin_bp") or 0) / 10000.0 if r.get("margin_bp") else None
        exists = conn.execute("SELECT 1 FROM alphas WHERE alpha_id=?", (aid,)).fetchone()
        if args.dry_run:
            print(f"  [dry] {aid} S={r.get('sharpe')} F={r.get('fitness')} "
                  f"{'已存在' if exists else '新增'}")
            continue
        if exists:
            conn.execute(
                """UPDATE alphas SET
                     expression=COALESCE(expression, ?),
                     sharpe=COALESCE(sharpe, ?), fitness=COALESCE(fitness, ?),
                     two_year_sharpe=COALESCE(two_year_sharpe, ?),
                     margin=COALESCE(margin, ?), turnover=COALESCE(turnover, ?),
                     sub_universe_sharpe=COALESCE(sub_universe_sharpe, ?),
                     platform_status=COALESCE(platform_status, 'UNSUBMITTED'),
                     stage=COALESCE(stage, 'IS')
                   WHERE alpha_id=?""",
                (r["code"], r.get("sharpe"), r.get("fitness"), r.get("two_year_sharpe"),
                 margin, r.get("turnover_pct"), r.get("sub_universe_sharpe"), aid),
            )
            upd += 1
        else:
            conn.execute(
                """INSERT INTO alphas
                     (alpha_id, expression, region_id, dataset_id, universe, delay,
                      neutralization, sharpe, fitness, margin, turnover,
                      two_year_sharpe, platform_status, stage, alpha_type,
                      sub_universe_sharpe)
                   VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                (aid, r["code"], rid, did, "TOPCS1600", 1, "SUBINDUSTRY",
                 r.get("sharpe"), r.get("fitness"), margin, r.get("turnover_pct"),
                 r.get("two_year_sharpe"), "UNSUBMITTED", "IS", "REGULAR",
                 r.get("sub_universe_sharpe")),
            )
            ins += 1
    if not args.dry_run:
        conn.commit()
    print(f"[ok] {args.tag}: 新增 {ins} / 补字段 {upd} / 共 {len(rows)} 条"
          f"{'（dry-run 未写库）' if args.dry_run else ''}")
    conn.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
