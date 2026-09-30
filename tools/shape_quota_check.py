#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""shape_quota_check —— 模板形状配额检查（反模板同质化，2026-09-28 落地）。

背景：wave84/85 实测连续两波候选同质化（19 条选中仅 ~9 个算子形状、trade_when
占比 62%），而平台已验证算子 103 个、KB 模板库 141 条零调用。GEM 的 ideas 渲染
模式只会复制手写示例形状，契约波又强制关闭两个形状发生器（--enhance-diversity
never / --auto-coverage never）——形状配额必须机械检查，不能靠自觉。

判据（ra-pipeline 步 4「模板形状配额与形状源」）：
  1. shape family 数 ≥ --min-families（默认 3）
  2. trade_when 类条件式占比 ≤ --max-trade-when（默认 0.4）
两项任一不过 → 退出码 1。仅统计/报告，不改表达式。

用法：
  python tools/shape_quota_check.py --region USA --wave s2_analyst7_d1   # 从 DB 读选中候选
  python tools/shape_quota_check.py --exprs-file candidates.txt          # 每行一条
  python tools/shape_quota_check.py --exprs-file c.txt --min-families 4  # 收紧
"""
from __future__ import annotations

import argparse
import re
import sqlite3
import sys
from collections import Counter
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]

# 形状族判定（按优先级首个命中归属；谓词基于骨架签名算子）
SHAPE_RULES = [
    ("conditional_trade_when", lambda e: "trade_when(" in e),
    ("regime_if_else", lambda e: "if_else(" in e),
    ("timing_argextremum", lambda e: "ts_arg_max(" in e or "ts_arg_min(" in e),
    ("recency_days_from_last_change", lambda e: "days_from_last_change(" in e),
    ("resonance_ts_corr", lambda e: "ts_corr(" in e or "covariance(" in e),
    ("interaction_multiply", lambda e: "multiply(" in e),
    ("spread_rank_diff", lambda e: "subtract(rank(" in e.replace(" ", "")),
    ("ratio_geometry", lambda e: "divide(" in e),
    ("convex_signed_power", lambda e: "signed_power(" in e or "power(" in e),
    ("truncation_winsorize", lambda e: "winsorize(" in e),
    ("state_zscore", lambda e: "zscore(" in e),
    ("trend_ts_delta_mean", lambda e: "ts_delta(" in e or "ts_mean(" in e),
    ("group_geometry", lambda e: "group_" in e),
    ("bare_rank", lambda e: "rank(" in e),
]

OP_RE = re.compile(r"([a-z_][a-z0-9_]*)\s*\(")


def classify(expr: str) -> str:
    e = (expr or "").strip()
    for name, pred in SHAPE_RULES:
        try:
            if pred(e):
                return name
        except Exception:
            continue
    return "other"


def load_exprs(args) -> list:
    if args.exprs_file:
        return [
            ln.strip()
            for ln in Path(args.exprs_file).read_text(encoding="utf-8").splitlines()
            if ln.strip() and not ln.strip().startswith("#")
        ]
    if args.region and args.wave:
        db = args.db or str(REPO / "data" / "wqb.db")
        conn = sqlite3.connect(f"file:{db}?mode=ro", uri=True)
        conn.execute("PRAGMA busy_timeout=30000")  # 2026-09-28：合规守卫要求（防 database is locked）
        try:
            rows = conn.execute(
                """SELECT e.expression FROM expressions e
                   JOIN waves w ON e.wave_id=w.id
                   WHERE e.region=? AND w.wave_number=? AND e.status IN ('selected','gated','gem')
                   ORDER BY e.id""",
                (args.region, str(args.wave)),
            ).fetchall()
        finally:
            conn.close()
        return [r[0] for r in rows if r and r[0]]
    return []


def main() -> int:
    ap = argparse.ArgumentParser(description="模板形状配额检查（shape family ≥N、trade_when 占比 ≤M）")
    ap.add_argument("--exprs-file", default=None, help="每行一条表达式的文件")
    ap.add_argument("--region", default=None)
    ap.add_argument("--wave", default=None)
    ap.add_argument("--db", default=None, help="DB 路径（缺省 <repo>/data/wqb.db）")
    ap.add_argument("--min-families", type=int, default=3)
    ap.add_argument("--max-trade-when", type=float, default=0.4)
    args = ap.parse_args()

    exprs = load_exprs(args)
    if not exprs:
        print("[shape_quota] 无表达式可查（给 --exprs-file 或 --region/--wave）", file=sys.stderr)
        return 2

    fams = Counter(classify(e) for e in exprs)
    n = len(exprs)
    tw = fams.get("conditional_trade_when", 0)
    tw_share = tw / n if n else 0.0
    ops = Counter(op for e in exprs for op in OP_RE.findall(e or ""))

    print(f"[shape_quota] n={n} shape_families={len(fams)} trade_when={tw} ({tw_share:.0%})")
    for name, cnt in fams.most_common():
        print(f"    {cnt:4d}  {name}")
    print(f"[shape_quota] 算子调用面：{len(ops)} 种 -> "
          + ", ".join(f"{k}:{v}" for k, v in ops.most_common(12)))

    ok = True
    if len(fams) < args.min_families:
        print(f"[shape_quota] FAIL: shape family {len(fams)} < {args.min_families}"
              f"——回步 4 补骨架（查 KB/community_tpl_kb，优先 external_template_sources）")
        ok = False
    if tw_share > args.max_trade_when:
        print(f"[shape_quota] FAIL: trade_when 占比 {tw_share:.0%} > {args.max_trade_when:.0%}"
              f"——事件条件化换 if_else 状态机/ts_arg_max 时点/days_from_last_change 新鲜度等形状")
        ok = False
    if ok:
        print("[shape_quota] PASS")
        return 0
    return 1


if __name__ == "__main__":
    sys.exit(main())
