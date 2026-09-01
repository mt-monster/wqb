# -*- coding: utf-8 -*-
"""discover_datasets.py - 数据集发现（灌 datasets 表）。

针对 datasets 表为空的区域（ASI/GLB/HKG/DEU），用 GET /data-sets 分页拉平台数据集，
插入本地 datasets 表，使后续 validate_fields_batch.py --backfill 能按 dataset.id= 拉字段。

用法：
  python tools/discover_datasets.py --region HKG --universe TOP800 --delay 1
  python tools/discover_datasets.py --region GLB --universe MINVOL10M --delay 1 --dry-run
"""
import argparse
import json
import os
import sqlite3
import sys
from datetime import datetime

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "lib"))
from api_client import Api, load_creds

DB = "data/wqb.db"
PAGE = 50


def _now():
    return datetime.now().isoformat(timespec="seconds")


def fetch_all_datasets(api, region, universe, delay):
    base = ("/data-sets?instrumentType=EQUITY&region={region}"
            "&delay={delay}&universe={universe}&limit={pg}").format(
                region=region, delay=delay, universe=universe, pg=PAGE)
    out, offset = [], 0
    while True:
        j = json.load(api.get(f"{base}&offset={offset}"))
        results = j.get("results", [])
        out.extend(results)
        offset += len(results)
        if not results or offset >= j.get("count", 0):
            return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--region", required=True)
    ap.add_argument("--universe", required=True)
    ap.add_argument("--delay", type=int, default=1)
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--db", default=DB)
    ap.add_argument("--sleep", type=float, default=1.0)
    args = ap.parse_args()

    conn = sqlite3.connect(args.db)
    cur = conn.cursor()
    rid = cur.execute("SELECT id FROM regions WHERE name=?", (args.region,)).fetchone()
    if not rid:
        print(f"区域 {args.region} 不在 regions 表")
        return
    rid = rid[0]

    api = Api()
    e, p = load_creds()
    api.login(e, p)
    print("[AUTH] OK")

    raw = fetch_all_datasets(api, args.region, args.universe, args.delay)
    print(f"区域={args.region} universe={args.universe} delay={args.delay}  平台数据集={len(raw)}\n")

    n_ins = n_skip = 0
    for d in raw:
        name = d.get("id")
        if not name:
            continue
        exists = cur.execute(
            "SELECT id FROM datasets WHERE name=? AND region_id=?", (name, rid)).fetchone()
        if exists:
            n_skip += 1
            continue
        # category 是嵌套 dict {id,name}, 取 id
        cat_raw = d.get("category")
        cat = cat_raw.get("id") if isinstance(cat_raw, dict) else (cat_raw or d.get("type"))
        if not args.dry_run:
            cur.execute(
                """INSERT INTO datasets
                   (name, region_id, category, field_count, coverage, alpha_count,
                    value_score, pyramid_multiplier, created_at, updated_at)
                   VALUES (?,?,?,?,?,?,?,?,?,?)""",
                (name, rid, cat,
                 d.get("fieldCount"), d.get("coverage"), d.get("alphaCount"),
                 d.get("valueScore"), d.get("pyramidMultiplier"),
                 _now(), _now()))
        n_ins += 1
        fc = d.get("fieldCount") or 0
        print(f"  {'DRY' if args.dry_run else 'INS'} {name:30s} fields={fc:>5} cat={cat}")

    if not args.dry_run:
        conn.commit()
    print(f"\n插入={n_ins}  跳过(已存在)={n_skip}")
    conn.close()


if __name__ == "__main__":
    main()
