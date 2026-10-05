#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""scan_backup_ra.py — 备选 RA 补扫：把「全闸但未入队」的候选自动补进 submit_ready。

★ 为什么需要它（2026-10-05 实测教训）
  `tools/submit_inventory.py` 的盘点**只读 `submit_ready` 表**
  （`SELECT * FROM submit_ready WHERE status IN (...)`）。
  于是任何「存在于 `alphas` 表、但从未入队」的达标候选，对每日盘点完全隐形。
  典型受害者：`WjegEmQO`（EUR，S1.94/F1.38/2Y1.59/sub1.96，会话内实测
  prod 0.5012 / self 0.1616 全过）——它在 `alphas` 里躺着，但 `submit_ready` 无行，
  所以连续多轮盘点都扫不到它。

★ 两条硬口径（与本工作区铁律一致）
  1) **prod 为 NULL 但业绩已明确记录的对象必须纳入**。
     会话里实测过的 prod/self 常常没回写 `alphas`（`WjegEmQO` 就是
     prod_correlation=None 的裸行）。若按「prod 必填」过滤，这批真候选会被静默丢弃。
     ⇒ 口径写成 `(prod IS NULL OR prod < --max-prod)`，
       且要求 `(sharpe, fitness) IS NOT NULL` 作为「业绩已明确记录」的判据。
  2) **同族只留一条**（同族铁律）：默认按 `(region, skeleton)` 只保留优先级最高的
     `--max-per-skeleton` 条，避免一次性把 144 条 ASI 同族变体冲进队列。

默认 dry-run（只看不写）；加 `--apply` 才落库。离线零配额，不碰平台。

用法:
  python tools/scan_backup_ra.py --region EUR                 # dry-run 列出
  python tools/scan_backup_ra.py --region EUR --apply         # 入队
  python tools/scan_backup_ra.py --all-regions --dry-run      # 全库体检
退出码: 0=正常  2=参数错误  3=DB 不可用
"""
import argparse
import os
import sqlite3
import sys
from collections import defaultdict
from typing import Any, Dict, List, Optional

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "src"))

from wqb.store import submit_queue as sq  # noqa: E402

# 全闸口径默认值（源自 tracking/EUR/GOAL_20_ACCUMULATION.md 实测确立的口径）
DEF_MIN_SHARPE = 1.58
DEF_MIN_FITNESS = 1.0
DEF_MIN_2Y = 1.58
DEF_MIN_SUB = 1.0
DEF_MAX_PROD = 0.7


def _connect(db: Optional[str] = None) -> sqlite3.Connection:
    con = sq.connect(db) if db else sq.connect()
    con.row_factory = sqlite3.Row
    return con


def scan(con: sqlite3.Connection,
         region: Optional[str] = None,
         min_sharpe: float = DEF_MIN_SHARPE,
         min_fitness: float = DEF_MIN_FITNESS,
         min_2y: float = DEF_MIN_2Y,
         min_sub: float = DEF_MIN_SUB,
         max_prod: float = DEF_MAX_PROD,
         exclude_known_skeleton: bool = True) -> List[Dict[str, Any]]:
    """返回「全闸 + 未入队」的候选行（未去重）。"""
    q = """
        SELECT a.alpha_id,
               r.name                    AS region,
               a.universe, a.delay, a.neutralization, a.expression,
               a.sharpe, a.fitness, a.turnover,
               a.two_year_sharpe         AS two_year,
               a.sub_universe_sharpe     AS sub_universe,
               a.cluster_test,
               a.prod_correlation        AS prod,
               a.self_correlation        AS self_corr,
               (SELECT b.ra_failed_checks FROM backtest_results b
                 WHERE b.alpha_id = a.alpha_id ORDER BY b.id DESC LIMIT 1) AS ra_failed_checks
          FROM alphas a
          LEFT JOIN regions r ON a.region_id = r.id
         WHERE a.alpha_id IS NOT NULL AND a.alpha_id <> ''
           AND COALESCE(a.soft_deleted, 0) = 0
           AND COALESCE(a.disposition, '') <> 'DEAD'
           AND a.status IN ('UNSUBMITTED', 'COMPLETE')
           AND COALESCE(a.platform_status, '') NOT IN ('ACTIVE', 'DECOMMISSIONED')
           AND a.date_submitted IS NULL
           AND a.sharpe  IS NOT NULL            -- ★「业绩已明确记录」判据
           AND a.fitness IS NOT NULL
           AND a.sharpe   >= ?
           AND a.fitness  >= ?
           AND a.two_year_sharpe      >= ?
           AND a.sub_universe_sharpe  >= ?
           AND (a.prod_correlation IS NULL OR a.prod_correlation < ?)
    """
    ps: List[Any] = [min_sharpe, min_fitness, min_2y, min_sub, max_prod]
    if region:
        q += " AND r.name = ?"
        ps.append(region)
    rows = [dict(r) for r in con.execute(q, ps).fetchall()]

    # 已在 submit_ready 的（任意状态）不再重复入队
    have = {(x[0], x[1]) for x in
            con.execute("SELECT alpha_id, region FROM submit_ready").fetchall()}
    rows = [r for r in rows
            if r.get("region") and (r["alpha_id"], r["region"]) not in have]

    # ★ 已知骨架跳过：队列里已有同骨架兄弟的，不再新增（避免同族重复行）。
    #   例：EUR 的 `omWVZ7lm` 与队列里已 READY 的 `N1VnJjXg` 骨架完全相同。
    if exclude_known_skeleton:
        known: set = set()
        for x in con.execute("SELECT region, skeleton, expr FROM submit_ready").fetchall():
            sig = x["skeleton"] or sq._sig(x["expr"])
            if sig:
                known.add((x["region"], sig))
        kept = []
        for r in rows:
            sig = sq._sig(r.get("expression")) or ""
            if (r["region"], sig) in known:
                continue
            kept.append(r)
        rows = kept
    return rows


def _prio(r: Dict[str, Any]) -> tuple:
    """同族内优先级（升序更优）。

    ★ 同族铁律：只提 prod 最低那颗；prod 未测的退化为「IS sharpe 最高」优先
    （`WjegEmQO` 就落在这一档——DB 里 prod 为 NULL，但它是该族 IS 最优）。
    """
    p = r.get("prod")
    if p is not None:
        return (0, float(p), -(r.get("sharpe") or 0))
    return (1, 0.0, -(r.get("sharpe") or 0))


def dedup(rows: List[Dict[str, Any]], max_per_skeleton: int = 1) -> List[Dict[str, Any]]:
    """按 (region, skeleton) 分组，每组只留优先级最高的 N 条。"""
    if max_per_skeleton <= 0:
        for r in rows:
            r["skeleton"] = sq._sig(r.get("expression"))
        return sorted(rows, key=_prio)
    groups: Dict[Any, List[Dict[str, Any]]] = defaultdict(list)
    for r in rows:
        sig = sq._sig(r.get("expression")) or ""
        r["skeleton"] = sig
        groups[(r["region"], sig)].append(r)
    out: List[Dict[str, Any]] = []
    for key, g in groups.items():
        g.sort(key=_prio)
        out.extend(g[:max_per_skeleton])
    return sorted(out, key=_prio)


def main() -> int:
    ap = argparse.ArgumentParser(
        description="备选 RA 补扫：全闸但未入队的候选补进 submit_ready（默认 dry-run）")
    ap.add_argument("--region", help="只扫该区域（如 EUR）；缺省扫全库")
    ap.add_argument("--all-regions", action="store_true",
                    help="显式声明扫全库（与 --region 互斥，仅作可读性提示）")
    ap.add_argument("--min-sharpe", type=float, default=DEF_MIN_SHARPE)
    ap.add_argument("--min-fitness", type=float, default=DEF_MIN_FITNESS)
    ap.add_argument("--min-2y", type=float, default=DEF_MIN_2Y)
    ap.add_argument("--min-sub", type=float, default=DEF_MIN_SUB)
    ap.add_argument("--max-prod", type=float, default=DEF_MAX_PROD)
    ap.add_argument("--max-per-skeleton", type=int, default=1,
                    help="每个 (region,骨架) 保留条数（默认 1，同族铁律；0=不去重）")
    ap.add_argument("--apply", action="store_true", help="真正写入 submit_ready（默认 dry-run）")
    ap.add_argument("--dry-run", action="store_true", help="只看不写（默认行为）")
    ap.add_argument("--include-known-skeleton", action="store_true",
                    help="连队列里已有同骨架的兄弟也一起入队（默认跳过，避免同族重复行）")
    ap.add_argument("--note", default="backup-ra-scan", help="入队 note 标记")
    ap.add_argument("--db", help="指定 sqlite 路径（默认走 wqb 默认库）")
    a = ap.parse_args()

    try:
        con = _connect(a.db)
    except Exception as e:  # noqa: BLE001
        print(f"[ERROR] 打不开 DB: {e}", file=sys.stderr)
        return 3

    raw = scan(con, region=a.region, min_sharpe=a.min_sharpe, min_fitness=a.min_fitness,
               min_2y=a.min_2y, min_sub=a.min_sub, max_prod=a.max_prod,
               exclude_known_skeleton=not a.include_known_skeleton)
    picked = dedup(raw, max_per_skeleton=a.max_per_skeleton)

    scope = a.region or "全库"
    print(f"=== 备选 RA 补扫（{scope}）===")
    print(f"命中全闸且未入队：{len(raw)} 条 | 骨架去重后入选：{len(picked)} 条")
    if not picked:
        print("  （空）")
        return 0

    by_region: Dict[str, int] = defaultdict(int)
    for r in picked:
        by_region[str(r["region"])] += 1
    print("按区分布：" + ", ".join(f"{k}={v}" for k, v in sorted(by_region.items())))
    print()
    print(f"{'alpha_id':13}{'reg':5}{'S':>6}{'F':>6}{'2Y':>7}{'sub':>7}{'TO':>8}{'prod':>9}  skeleton")
    print("-" * 96)
    for r in picked:
        print(f"{r['alpha_id']:13}{str(r['region']):5}"
              f"{r.get('sharpe') or 0:>6}{r.get('fitness') or 0:>6}"
              f"{r.get('two_year') or 0:>7}{r.get('sub_universe') or 0:>7}"
              f"{r.get('turnover') or 0:>8}{str(r.get('prod')):>9}  "
              f"{(r.get('skeleton') or '')[:28]}")

    if not a.apply:
        print("\n[dry-run] 未写入。确认无误后加 --apply 入队。")
        return 0

    sq.ensure_table(con)
    n = 0
    for r in picked:
        rec = {
            "alpha_id": r["alpha_id"], "region": r["region"],
            "universe": r.get("universe"), "delay": r.get("delay"),
            "decay": None, "neutralization": r.get("neutralization"),
            "expr": r.get("expression"),
            "skeleton": r.get("skeleton") or None,
            "sharpe": r.get("sharpe"), "fitness": r.get("fitness"),
            "turnover": r.get("turnover"), "two_year": r.get("two_year"),
            "sub_universe": r.get("sub_universe"), "cluster_test": r.get("cluster_test"),
            "prod": r.get("prod"), "self": r.get("self_corr"),
            "ra_failed_checks": r.get("ra_failed_checks"),
            "verified_by": "IS_only",
        }
        try:
            gate = sq.enqueue(con, rec, note=a.note)
        except Exception as e:  # noqa: BLE001
            print(f"  {r['alpha_id']}: 入队失败 {str(e)[:120]}")
            continue
        n += 1
        print(f"  {r['alpha_id']} [{r['region']}] → {gate}")
    con.commit()
    print(f"\n[apply] 已入队 {n} 条（note={a.note}）。")
    print("提示：入队后跑 `python tools/submit_inventory.py --no-csv` 即可看到它们；"
          "prod 为 NULL 的行会由盘点脚本实测回源补齐。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
