"""统计「骨架结构」对 fitness 效率(eff = F/S = sqrt(R/TO)) 的影响。

要检验两个候选解释：
  H1 层位置：group_rank 在 ts_* 外层 vs 内层
  H2 稳定层：是否含长窗口稳定化（ts_backfill / ts_zscore / ts_rank）

起源：sentiment21 消融批（USA D1，2026-10-29）单项受控实测显示同样字段、
同样 sharpe 下
  group_rank(ts_decay_linear(x,W), g)   → eff 0.14，TO 102.7%
  ts_decay_linear(group_rank(x,g), W)   → eff 0.48，TO   8.2%
但全库观察统计对 H1 只有 1.06x（无区分度）⇒ H1 不足以解释。
`zqrgna91`（S2.67/F1.66）的成功骨架内部多一层 ts_zscore(ts_backfill(x,252),252)，
故检验 H2。

注意：本脚本是**观察性**统计（样本经自选择、跨数据集混杂），证据强度低于
受控实验。结论只用于「是否值得再做受控实验」，不单独作为规约依据。

用法：
    python tools/fields/skeleton_position_stats.py
    python tools/fields/skeleton_position_stats.py --region USA --min-sharpe 1.0
"""
from __future__ import annotations

import argparse
import os
import sqlite3
import statistics
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(os.path.dirname(_HERE))
if os.path.join(_ROOT, "src") not in sys.path:
    sys.path.insert(0, os.path.join(_ROOT, "src"))

from wqb.db_conn import connect as db_connect  # noqa: E402

OUTER_PATTERNS = (
    "group_rank(ts_decay_linear(",
    "group_rank(ts_mean(",
    "group_rank(ts_sum(",
)
INNER_PATTERNS = (
    "ts_decay_linear(group_rank(",
    "ts_mean(group_rank(",
    "ts_sum(group_rank(",
)
STABLE_TOKENS = ("ts_zscore(", "ts_backfill(", "ts_rank(")


def classify(expr: str) -> str:
    e = (expr or "").replace(" ", "")
    if any(p.replace(" ", "") in e for p in OUTER_PATTERNS):
        return "OUTER"
    if any(p.replace(" ", "") in e for p in INNER_PATTERNS):
        return "INNER"
    return "OTHER"


def is_stabilized(expr: str) -> bool:
    e = (expr or "").replace(" ", "")
    return any(tok in e for tok in STABLE_TOKENS)


def fmt(name: str, grp: list[dict], min_n: int) -> str:
    if len(grp) < min_n:
        return f"{name:<22} {len(grp):>6}  样本不足（<{min_n}）"
    eff = [r["fitness"] / r["sharpe"] for r in grp if r["sharpe"]]
    to = [r["turnover"] for r in grp if r["turnover"] is not None]
    good = sum(1 for e in eff if e >= 0.4)
    med_eff = statistics.median(eff)
    return (
        f"{name:<22} {len(grp):>6} "
        f"{statistics.median(r['sharpe'] for r in grp):>7.2f} "
        f"{statistics.median(r['fitness'] for r in grp):>7.2f} "
        f"{med_eff:>9.3f} "
        f"{(statistics.median(to) * 100 if to else float('nan')):>8.1f}% "
        f"{good / len(eff) * 100:>10.1f}%"
    )


HEADER = (
    f"{'分组':<22} {'n':>6} {'medS':>7} {'medF':>7} {'med_eff':>9} "
    f"{'medTO':>9} {'eff>=.4':>11}"
)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--region", default=None, help="区域名过滤，如 USA；省略=全部")
    ap.add_argument("--min-sharpe", type=float, default=0.8)
    ap.add_argument("--min-n", type=int, default=15)
    args = ap.parse_args()

    # 只读连接走统一工厂（mode=ro 且跳过 WAL PRAGMA，不改库文件字节）。
    con = db_connect(readonly=True, row_factory=sqlite3.Row)
    cols = {r[1] for r in con.execute("PRAGMA table_info(alphas)")}
    expr_col = "expr" if "expr" in cols else "expression"
    if expr_col not in cols:
        print("alphas 表无 expr/expression 列，列名：", sorted(cols))
        return 2

    sql = (
        f"SELECT {expr_col} AS expr, sharpe, fitness, turnover "
        "FROM alphas WHERE sharpe IS NOT NULL AND fitness IS NOT NULL "
        "AND sharpe >= ?"
    )
    params: list[object] = [args.min_sharpe]
    if args.region:
        sql += " AND region_id IN (SELECT id FROM regions WHERE name = ?)"
        params.append(args.region)
    rows = [dict(r) for r in con.execute(sql, params)]
    con.close()

    print(f"\n总样本(sharpe>={args.min_sharpe}"
          f"{', region=' + args.region if args.region else ''}) = {len(rows)}")
    print("\n[H1] 层位置")
    print(HEADER)
    print("-" * 76)
    buckets = {"OUTER": [], "INNER": [], "OTHER": []}
    for r in rows:
        buckets[classify(r["expr"])].append(r)
    for k in ("OUTER", "INNER"):
        print(fmt(k, buckets[k], args.min_n))

    print("\n[H2] 稳定层（含 ts_zscore/ts_backfill/ts_rank 任一）")
    print(HEADER)
    print("-" * 76)
    for label, want in (("STABILIZED", True), ("RAW", False)):
        grp = [r for r in rows if is_stabilized(r["expr"]) is want]
        print(fmt(label, grp, args.min_n))

    print("\n[H2 交叉] 稳定层 × 层位置")
    print(HEADER)
    print("-" * 76)
    for label, want in (("STABILIZED", True), ("RAW", False)):
        for pos in ("OUTER", "INNER"):
            grp = [r for r in rows
                   if is_stabilized(r["expr"]) is want and classify(r["expr"]) == pos]
            print(fmt(f"{label}/{pos}", grp, args.min_n))

    print("\n判读：eff 中位数差 >=1.5x 才算有区分度的候选解释；")
    print("      观察性统计受自选择与跨数据集混杂，不能替代受控实验。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
