#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""轮询取 prod 相关性并落 ``alpha_corr_cache``（tools/ 下同名脚本被外部清理删除两次，
故放 tracking/EUR/scripts/ 保命，见记忆 §47.4/§51）。

平台 `/correlations/prod` 是**单账号单并发**异步计算：首次 GET 触发服务端计算，
未算完返回空体（json 解析失败）。本脚本耐心轮询，默认每颗最多 8 分钟、间隔 20s。

用法::

    python tracking/EUR/scripts/fetch_prod.py pw5VPeoX XgJYWLg1
    python tracking/EUR/scripts/fetch_prod.py --file ids.txt --max-wait 480
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "Claude" / "skills" / "wq-brain-campaign-toolkit" / "scripts"))

from _lib.api import Api  # noqa: E402
from _lib.common import load_credentials  # noqa: E402
from wqb.db_conn import connect  # noqa: E402


def bucket_n(records, lo=0.7, hi=0.8):
    for row in records or []:
        if isinstance(row, (list, tuple)) and len(row) >= 3:
            try:
                if abs(float(row[0]) - lo) < 1e-9 and abs(float(row[1]) - hi) < 1e-9:
                    return int(row[2])
            except (TypeError, ValueError):
                continue
    return None


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("alpha_ids", nargs="*")
    ap.add_argument("--file")
    ap.add_argument("--max-wait", type=int, default=480)
    ap.add_argument("--interval", type=int, default=20)
    ap.add_argument("--refresh", action="store_true")
    ap.add_argument("--no-persist", action="store_true")
    args = ap.parse_args()

    ids = list(args.alpha_ids)
    if args.file:
        ids += [l.strip() for l in open(args.file, encoding="utf-8") if l.strip()]
    if not ids:
        print("[x] 需要 alpha_ids 或 --file")
        return 1

    conn = connect(str(ROOT / "data" / "wqb.db"), timeout=60.0)
    api = Api()
    api.login(*load_credentials())

    print(f"{'alpha_id':12s} {'prod':>8s} {'n[.7,.8)':>9s}  判定")
    for aid in ids:
        if not args.refresh:
            row = conn.execute(
                "SELECT prod_correlation FROM alpha_corr_cache WHERE alpha_id=?", (aid,)
            ).fetchone()
            if row and row[0] is not None:
                print(f"{aid:12s} {row[0]:>8.4f} {'-':>9s}  (缓存命中)")
                continue
        got = None
        t0 = time.time()
        tries = 0
        while time.time() - t0 < args.max_wait:
            tries += 1
            try:
                d = json.load(api.get(f"/alphas/{aid}/correlations/prod"))
            except Exception:
                time.sleep(args.interval)
                continue
            if d and d.get("max") is not None:
                got = d
                break
            time.sleep(args.interval)
        if not got:
            print(f"{aid:12s} {'-':>8s} {'-':>9s}  超时（{tries} 次尝试）")
            continue
        mx = got.get("max")
        n70 = bucket_n(got.get("records"))
        verdict = "PASS(<0.7)" if mx < 0.7 else "FAIL"
        if n70:
            verdict += f" / DEAD(单钉子 n={n70})"
        print(f"{aid:12s} {mx:>8.4f} {str(n70):>9s}  {verdict}")
        if not args.no_persist:
            now = time.strftime("%Y-%m-%dT%H:%M:%S")
            ex = conn.execute("SELECT 1 FROM alpha_corr_cache WHERE alpha_id=?", (aid,)).fetchone()
            if ex:
                conn.execute(
                    "UPDATE alpha_corr_cache SET prod_correlation=?, prod_records=?, "
                    "source='platform', checked_at=?, updated_at=? WHERE alpha_id=?",
                    (mx, json.dumps(got.get("records")), now, now, aid),
                )
            else:
                conn.execute(
                    "INSERT INTO alpha_corr_cache (alpha_id, prod_correlation, prod_records, "
                    "source, checked_at, created_at, updated_at) VALUES (?,?,?,?,?,?,?)",
                    (aid, mx, json.dumps(got.get("records")), "platform", now, now, now),
                )
            conn.commit()
    conn.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
