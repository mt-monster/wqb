# -*- coding: utf-8 -*-
"""backfill_longcount.py — 从平台补回 is 段持仓广度指标（longCount/shortCount/pnl/bookSize）。

背景（2026-09-29 实测）：
  `backtest_results.long_count` 只填了 830/9010（9.2%），`pnl`/`book_size` 只有 0.8%。
  原因是**采集层从来没取过 `is.longCount`** —— payload_json 里已展平的行只有
  sharpe/fitness/turnover_pct/margin_bp 等，没有多空持仓数。
  平台 `GET /alphas/{id}` 的 `is` 段实测含 `longCount`/`shortCount`/`pnl`/`bookSize`
  （probe：pwR8rdMg → is.longCount=1579 / shortCount=1482，与本地已有值一致）。

用途（补完能做什么）：
  1. VECTOR 字段「伪白空间」判据（cov 0.85 但实测 longCount 11-16，MEA f72 实证）；
  2. CONCENTRATED_WEIGHT 风险前瞻（实测：longCount<50 档 CW 命中率 38.5%，≥1000 档仅 2.1%）；
  3. 多空失衡诊断（L/S 悬殊 → 需 signed_power / 双 rank 对称化）；
  4. Sharpe 可信度门槛（3 只股票跑出的 Sharpe 不是因子）。

设计（遵循用户级回测脚本纪律）：
  * **断点续跑**：checkpoint 落 `results/backfill_longcount_checkpoint.json`，原子写；
    重跑自动跳过已完成的 alpha_id。 `LC_FRESH=1` 或 `--fresh` 强制全量。
  * **只把拿到确定结果的算完成**：HTTP 200（无论有没有 is 段）算完成；
    429/5xx/网络异常算未完成，下轮重试。
  * **幂等**：写库用 COALESCE，不覆盖已有非空值。

用法：
  python tools/backfill_longcount.py --limit 30              # 小样本 probe
  python tools/backfill_longcount.py --region KOR            # 只补某区
  python tools/backfill_longcount.py                         # 全量（后台跑）
  python tools/backfill_longcount.py --dry-run               # 只拉不写库
  python tools/backfill_longcount.py --fresh                 # 忽略 checkpoint
  python tools/backfill_longcount.py --status ACTIVE,UNSUBMITTED   # 只补候选池
"""
from __future__ import annotations

import argparse
import json
import os
import sqlite3
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime

_HERE = os.path.dirname(os.path.abspath(__file__))
_REPO = os.path.dirname(_HERE)
sys.path.insert(0, os.path.join(_HERE, "lib"))
sys.path.insert(0, os.path.join(_REPO, "src"))

from api_client import Api, load_creds  # noqa: E402

DB = os.path.join(_REPO, "data", "wqb.db")
CKPT = os.path.join(_REPO, "results", "backfill_longcount_checkpoint.json")

# 每线程独立 Api（requests.Session 非严格线程安全）
_local = threading.local()


def _api():
    a = getattr(_local, "api", None)
    if a is None:
        e, pw = load_creds()
        a = Api()
        a.login(e, pw)
        _local.api = a
    return a


# ---------------- checkpoint ----------------

def load_ckpt(path):
    if not os.path.exists(path):
        return {"meta": {}, "results": {}}
    try:
        with open(path, encoding="utf-8") as f:
            d = json.load(f)
        if not isinstance(d.get("results"), dict):
            return {"meta": {}, "results": {}}
        return d
    except Exception as e:
        print(f"[warn] checkpoint 损坏({e})，按空处理", file=sys.stderr)
        return {"meta": {}, "results": {}}


def save_ckpt(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False)
    os.replace(tmp, path)


# ---------------- 目标集 ----------------

def fetch_targets(region=None, status=None, limit=None):
    """需要补的 alpha_id（去重）。"""
    where = ["alpha_id IS NOT NULL", "alpha_id<>''",
             "(long_count IS NULL OR short_count IS NULL)"]
    args = []
    if region:
        where.append("region=?")
        args.append(region)
    if status:
        # 按 alphas.platform_status 过滤（候选池优先）
        where.append("""alpha_id IN (SELECT alpha_id FROM alphas
                        WHERE platform_status IN (%s))""" %
                     ",".join("?" * len(status)))
        args.extend(status)
    sql = ("SELECT DISTINCT alpha_id FROM backtest_results WHERE "
           + " AND ".join(where) + " ORDER BY id DESC")
    if limit:
        sql += f" LIMIT {int(limit)}"
    con = sqlite3.connect("file:%s?mode=ro" % DB.replace("\\", "/"), uri=True)
    try:
        return [r[0] for r in con.execute(sql, args)]
    finally:
        con.close()


# ---------------- 拉取 ----------------

def fetch_one(aid):
    """返回 dict；ok=True 表示确定结果（可入 checkpoint）。"""
    try:
        d = json.load(_api().get(f"/alphas/{aid}"))
    except Exception as e:
        msg = str(e)[:160]
        # 429 / 5xx / 网络 → 未完成，下轮重试
        return {"ok": False, "error": msg}
    isv = d.get("is") or {}
    return {
        "ok": True,
        "lc": isv.get("longCount"),
        "sc": isv.get("shortCount"),
        "pnl": isv.get("pnl"),
        "bs": isv.get("bookSize"),
        "has_is": bool(isv),
    }


# ---------------- 写库 ----------------

def flush(rows, dry_run=False):
    """rows: {aid: {"lc":..,"sc":..,"pnl":..,"bs":..}} → 写两张表。"""
    if not rows or dry_run:
        return 0, 0
    ts = datetime.now().isoformat(timespec="seconds")
    con = sqlite3.connect(DB, timeout=30)
    con.execute("PRAGMA journal_mode=WAL")
    cur = con.cursor()
    nb = na = 0
    try:
        for aid, v in rows.items():
            cur.execute(
                """UPDATE backtest_results SET
                     long_count  = COALESCE(?, long_count),
                     short_count = COALESCE(?, short_count),
                     pnl         = COALESCE(?, pnl),
                     book_size   = COALESCE(?, book_size)
                   WHERE alpha_id=?""",
                (v.get("lc"), v.get("sc"), v.get("pnl"), v.get("bs"), aid))
            nb += cur.rowcount
            cur.execute(
                """UPDATE alphas SET
                     long_count  = COALESCE(?, long_count),
                     short_count = COALESCE(?, short_count),
                     updated_at  = ?
                   WHERE alpha_id=?""",
                (v.get("lc"), v.get("sc"), ts, aid))
            na += cur.rowcount
        con.commit()
    finally:
        con.close()
    return nb, na


def report():
    con = sqlite3.connect("file:%s?mode=ro" % DB.replace("\\", "/"), uri=True)
    try:
        tot = con.execute("SELECT COUNT(*) FROM backtest_results").fetchone()[0]
        got = con.execute(
            "SELECT COUNT(*) FROM backtest_results WHERE long_count IS NOT NULL").fetchone()[0]
        atot = con.execute("SELECT COUNT(*) FROM alphas").fetchone()[0]
        agot = con.execute(
            "SELECT COUNT(*) FROM alphas WHERE long_count IS NOT NULL").fetchone()[0]
        return tot, got, atot, agot
    finally:
        con.close()


# ---------------- main ----------------

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--region")
    ap.add_argument("--status", help="按 alphas.platform_status 过滤，逗号分隔")
    ap.add_argument("--limit", type=int)
    ap.add_argument("--concurrency", type=int, default=4)
    ap.add_argument("--cool", type=float, default=0.15, help="每任务后冷却秒")
    ap.add_argument("--flush-every", type=int, default=50)
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--fresh", action="store_true",
                    help="忽略 checkpoint（LC_FRESH=1 同效）")
    a = ap.parse_args()

    fresh = a.fresh or os.environ.get("LC_FRESH") == "1"
    ck = {"meta": {}, "results": {}} if fresh else load_ckpt(CKPT)
    done = ck.setdefault("results", {})
    carried = len(done)

    targets = fetch_targets(a.region, a.status.split(",") if a.status else None, a.limit)
    todo = [t for t in targets if t not in done]
    print(f"本轮缺失目标 {len(targets)} 个 | checkpoint 已尝试 {carried}（跳过）| 待拉 {len(todo)}"
          f"{'  [FRESH]' if fresh else ''}{'  [DRY-RUN]' if a.dry_run else ''}")
    print("  注：目标集按 DB 缺失动态重算，补上的会自动移出；checkpoint 主要拦"
          "「无 is 段/已判跳过」的重复拉取。--limit 是本轮上限，滚动作业。")

    if not todo:
        print("无需拉取。")
        t, g, at, ag = report()
        print(f"现状: backtest_results {g}/{t} | alphas {ag}/{at}")
        return 0

    started = time.time() - carried * 0.6  # ETA 修正：把已搬运的进度折算进去
    got = skipped = failed = 0
    pending = {}
    lock = threading.Lock()

    def work(aid):
        nonlocal got, skipped, failed
        r = fetch_one(aid)
        if a.cool:
            time.sleep(a.cool)
        return aid, r

    with ThreadPoolExecutor(max_workers=a.concurrency) as ex:
        futs = {ex.submit(work, aid): aid for aid in todo}
        for i, fu in enumerate(as_completed(futs), 1):
            aid, r = fu.result()
            with lock:
                if r.get("ok"):
                    if r.get("has_is"):
                        got += 1
                        pending[aid] = {k: r.get(k) for k in ("lc", "sc", "pnl", "bs")}
                    else:
                        skipped += 1  # alpha 无 is 段（已删/未回测完）→ 不再重试
                    done[aid] = {"at": datetime.now().isoformat(timespec="seconds"),
                                 "lc": r.get("lc"), "sc": r.get("sc")}
                else:
                    failed += 1  # 不入 checkpoint，下轮重试
            if i % a.flush_every == 0 or i == len(todo):
                with lock:
                    batch, pending = pending, {}
                nb, na = flush(batch, a.dry_run)
                ck["meta"] = {"updated_at": datetime.now().isoformat(timespec="seconds"),
                              "region": a.region, "concurrency": a.concurrency}
                save_ckpt(CKPT, ck)
                el = time.time() - started
                eta = el / i * (len(todo) - i) if i else 0
                print(f"  {i}/{len(todo)} 有值={got} 无is={skipped} 失败={failed} "
                      f"写库(br={nb},al={na}) ETA={eta/60:.1f}min", flush=True)

    with lock:
        if pending:
            flush(pending, a.dry_run)
    ck["meta"] = {"updated_at": datetime.now().isoformat(timespec="seconds"),
                  "region": a.region, "concurrency": a.concurrency}
    save_ckpt(CKPT, ck)

    print(f"\n完成: 有值={got} 无is跳过={skipped} 失败(可重跑)={failed}")
    t, g, at, ag = report()
    print(f"现状: backtest_results {g}/{t} ({g/t*100:.1f}%) | alphas {ag}/{at} ({ag/at*100:.1f}%)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
