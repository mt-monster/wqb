# -*- coding: utf-8 -*-
"""discover_datasets.py - 数据集发现（灌 datasets 表）。

针对 datasets 表为空的区域（ASI/GLB/HKG/DEU），用 GET /data-sets 分页拉平台数据集，
插入本地 datasets 表，使后续 validate_fields_batch.py --backfill 能按 dataset.id= 拉字段。

用法：
  python tools/discover_datasets.py --region HKG --universe TOP800 --delay 1
  python tools/discover_datasets.py --region GLB --universe MINVOL10M --delay 1 --dry-run
"""
import sys as _sys, os as _os
_sys.path.insert(0, str(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '..', 'src')))
from wqb.db_conn import connect as db_connect  # 规范工厂（2026-09-20 L1 收口）
from wqb.store import CampaignStore  # 数据集行写入走库层单一 API（2026-10-01）
import argparse
import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "lib"))
from api_client import Api, load_creds

DB = "data/wqb.db"
PAGE = 50


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

    conn = db_connect(args.db)
    conn.execute("PRAGMA foreign_keys=ON")
    cur = conn.cursor()
    store = CampaignStore(args.db)
    rid = cur.execute("SELECT id FROM regions WHERE name=?", (args.region,)).fetchone()
    if not rid:
        print(f"区域 {args.region} 不在 regions 表")
        store.close()
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
        # 2026-10-01：改为走库层单一写入 API（原为手写 INSERT，字段清单与
        # upsert_dataset_meta 重复且缺 delay/tier）。仍保持「只插不更」语义：
        # 已存在的行在上面已 continue，不会覆盖。
        if not args.dry_run:
            store.upsert_dataset_meta(args.region, dict(d, delay=args.delay))
        n_ins += 1
        fc = d.get("fieldCount") or 0
        cat_raw = d.get("category")
        cat = cat_raw.get("id") if isinstance(cat_raw, dict) else (cat_raw or d.get("type"))
        print(f"  {'DRY' if args.dry_run else 'INS'} {name:30s} fields={fc:>5} cat={cat}")

    print(f"\n插入={n_ins}  跳过(已存在)={n_skip}")
    store.close()
    conn.close()


if __name__ == "__main__":
    main()
