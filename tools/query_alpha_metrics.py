# -*- coding: utf-8 -*-
"""query_alpha_metrics.py — 本地库直查 alpha 全指标（免打平台 API）。

动机（2026-09-18，设计文档 §2.2 改动#7）：候选筛选（prod≤0.7 / self≤0.7）
此前需要逐条打平台 `check_correlation`，既消耗配额又占单并发队列。
本工具直接读 `data/wqb.db`，把筛选/复盘收敛为零成本 SQL。

用法示例：
  # 看整体填充率（评估落库覆盖率）
  python tools/query_alpha_metrics.py --coverage

  # 找 KOR 区域 prod≤0.7 且 self≤0.7 的候选
  python tools/query_alpha_metrics.py --region KOR --max-prod 0.7 --max-self 0.7

  # 只要平台权威值（排除本地抽测）
  python tools/query_alpha_metrics.py --source platform_sync --limit 30

  # 按 sharpe 门槛筛（默认只列未提交 UNSUBMITTED）
  python tools/query_alpha_metrics.py --region USA --min-sharpe 1.58 --status any

  # 导出 CSV
  python tools/query_alpha_metrics.py --region KOR --csv out/kor_candidates.csv
"""
from __future__ import annotations

import argparse
import csv
import os
import sqlite3
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_DB = os.path.join(REPO, "data", "wqb.db")

# 参与填充率统计的指标列
_METRIC_COLS = (
    "sharpe", "fitness", "turnover", "margin", "two_year_sharpe",
    "is_ladder_sharpe", "prod_correlation", "self_correlation",
    "sub_universe_sharpe", "returns", "drawdown", "long_count",
    "short_count", "concentrated_weight", "cluster_test",
)


def _conn(db):
    c = sqlite3.connect(db, timeout=30.0)
    c.row_factory = sqlite3.Row
    c.execute("PRAGMA journal_mode=WAL")
    return c


def cmd_coverage(conn) -> int:
    """输出各指标填充率（含来源分布）。"""
    cols = {r[1] for r in conn.execute("PRAGMA table_info(alphas)")}
    total = conn.execute("SELECT COUNT(*) FROM alphas").fetchone()[0]
    print(f"alphas 总行数 = {total}\n")
    print(f"{'指标':<26}{'有值':>8}{'填充率':>10}")
    print("-" * 46)
    for c in _METRIC_COLS:
        if c not in cols:
            print(f"{c:<26}{'—':>8}{'缺列':>10}")
            continue
        n = conn.execute(
            f"SELECT COUNT(*) FROM alphas WHERE {c} IS NOT NULL").fetchone()[0]
        pct = (n / total * 100) if total else 0.0
        print(f"{c:<26}{n:>8}{pct:>9.1f}%")

    if "prod_corr_source" in cols:
        print("\n来源分布（prod_corr_source）：")
        for r in conn.execute(
            "SELECT COALESCE(prod_corr_source,'(未标记)') AS s, COUNT(*) AS n "
            "FROM alphas WHERE prod_correlation IS NOT NULL OR self_correlation IS NOT NULL "
            "GROUP BY s ORDER BY n DESC"
        ):
            print(f"  {r['s']:<16}{r['n']:>8}")
    return 0


def build_query(a) -> tuple[str, list]:
    cols = {r[1] for r in conn_placeholder[0].execute("PRAGMA table_info(alphas)")}
    sql = [
        "SELECT a.alpha_id, r.name AS region, a.sharpe, a.fitness, a.turnover,",
        "       a.two_year_sharpe, a.prod_correlation, a.self_correlation,",
        "       a.prod_corr_source, a.corr_checked_at, a.status, a.date_submitted",
        "FROM alphas a LEFT JOIN regions r ON a.region_id = r.id WHERE 1=1",
    ]
    p: list = []
    if a.region:
        sql.append("AND r.name = ?")
        p.append(a.region)
    if a.status and a.status != "any":
        sql.append("AND a.status = ?")
        p.append(a.status)
    if a.min_sharpe is not None:
        sql.append("AND a.sharpe IS NOT NULL AND a.sharpe >= ?")
        p.append(a.min_sharpe)
    if a.max_prod is not None:
        sql.append("AND a.prod_correlation IS NOT NULL AND a.prod_correlation <= ?")
        p.append(a.max_prod)
    if a.max_self is not None:
        sql.append("AND a.self_correlation IS NOT NULL AND a.self_correlation <= ?")
        p.append(a.max_self)
    if a.source:
        sql.append("AND a.prod_corr_source = ?")
        p.append(a.source)
    if a.has_prod:
        sql.append("AND a.prod_correlation IS NOT NULL")
    sql.append("ORDER BY (a.prod_correlation IS NULL), a.prod_correlation ASC, a.sharpe DESC")
    sql.append("LIMIT ?")
    p.append(a.limit)
    return " ".join(sql), p


conn_placeholder: list = []


def cmd_query(a) -> int:
    conn = conn_placeholder[0]
    sql, params = build_query(a)
    rows = conn.execute(sql, params).fetchall()
    if not rows:
        print("无匹配记录。")
        return 0
    hdr = ["alpha_id", "region", "sharpe", "fitness", "turnover", "2Y",
           "prod", "self", "source", "checked_at", "status", "submitted"]
    print("  ".join(f"{h:<10}" for h in hdr[:8]) + "  " + "  ".join(hdr[8:]))
    print("-" * 130)
    for r in rows:
        print("  ".join([
            f"{(r['alpha_id'] or ''):<10}",
            f"{(r['region'] or ''):<10}",
            f"{(r['sharpe'] if r['sharpe'] is not None else '-'):<10}",
            f"{(r['fitness'] if r['fitness'] is not None else '-'):<10}",
            f"{(r['turnover'] if r['turnover'] is not None else '-'):<10}",
            f"{(r['two_year_sharpe'] if r['two_year_sharpe'] is not None else '-'):<10}",
            f"{(r['prod_correlation'] if r['prod_correlation'] is not None else '-'):<10}",
            f"{(r['self_correlation'] if r['self_correlation'] is not None else '-'):<10}",
            f"{(r['prod_corr_source'] or '-'):<16}",
            f"{(r['corr_checked_at'] or '-'):<20}",
            f"{(r['status'] or '-'):<12}",
            f"{(r['date_submitted'] or '-'):<20}",
        ]))
    print(f"\n共 {len(rows)} 条")
    if a.csv:
        with open(a.csv, "w", newline="", encoding="utf-8-sig") as f:
            w = csv.writer(f)
            w.writerow(hdr)
            for r in rows:
                w.writerow([r[k] for k in (
                    "alpha_id", "region", "sharpe", "fitness", "turnover",
                    "two_year_sharpe", "prod_correlation", "self_correlation",
                    "prod_corr_source", "corr_checked_at", "status", "date_submitted")])
        print(f"[csv] 已写出 {a.csv}")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description="本地 alpha 指标查询（免打平台）")
    ap.add_argument("--db", default=DEFAULT_DB)
    ap.add_argument("--coverage", action="store_true", help="只输出填充率统计")
    ap.add_argument("--region", help="区域（KOR/USA/EUR/IND/GBR/...）")
    ap.add_argument("--status", default="UNSUBMITTED",
                    help="本地状态过滤，'any' 不过滤（默认 UNSUBMITTED）")
    ap.add_argument("--min-sharpe", type=float, help="sharpe 下界（如 1.58）")
    ap.add_argument("--max-prod", type=float, help="prod_correlation 上界（如 0.7）")
    ap.add_argument("--max-self", type=float, help="self_correlation 上界（如 0.7）")
    ap.add_argument("--source", help="prod_corr_source 过滤")
    ap.add_argument("--has-prod", action="store_true", help="只要已测过 prod 的")
    ap.add_argument("--limit", type=int, default=50)
    ap.add_argument("--csv", help="导出 CSV 路径")
    a = ap.parse_args()

    if not os.path.exists(a.db):
        print(f"[error] 数据库不存在: {a.db}")
        return 1
    conn = _conn(a.db)
    conn_placeholder.append(conn)
    try:
        if a.coverage:
            return cmd_coverage(conn)
        return cmd_query(a)
    finally:
        conn.close()


if __name__ == "__main__":
    sys.exit(main())
