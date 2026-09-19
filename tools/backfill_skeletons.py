# -*- coding: utf-8 -*-
"""backfill_skeletons.py — 为存量表达式回填骨架签名（幂等，dry-run 默认）。

背景（2026-09-17 实测）：`expressions.skeleton` 全库 0 行——唯一写入方是
`gem_wave` 节点，而它不在实际生成链路中（实际链路 = GEM runner → AI 调
MCP `upsert_expressions`，该工具此前也不写骨架）。写入侧已修
（`_expressions.py::_expr_skeleton` 自动计算），存量需一次性回填。

口径：字段→F、数字→N、算子按「后紧跟 (」识别（`wqb.expression.skeleton.structural_signature`）。
只填空值，不覆盖已有（幂等；重跑零变化）。

用法：
  python tools/backfill_skeletons.py                # 预览
  python tools/backfill_skeletons.py --apply        # 写库
  python tools/backfill_skeletons.py --stats        # 顺带打印骨架复用率
"""
import argparse
import collections
import os
import sqlite3
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "src"))


def main():
    ap = argparse.ArgumentParser(description="存量表达式骨架签名回填（幂等，dry-run 默认）")
    ap.add_argument("--db", default=os.path.join(REPO, "data", "wqb.db"))
    ap.add_argument("--apply", action="store_true", help="实际写库（缺省只预览）")
    ap.add_argument("--stats", action="store_true", help="打印骨架复用率统计")
    a = ap.parse_args()

    from wqb.expression.skeleton import structural_signature

    conn = sqlite3.connect(a.db)
    rows = conn.execute(
        "SELECT id, expression FROM expressions WHERE skeleton IS NULL "
        "AND expression IS NOT NULL AND expression<>''").fetchall()
    print(f"待回填（skeleton IS NULL）= {len(rows)}")

    filled = {}
    for rid, expr in rows:
        sig = structural_signature(expr)
        if sig:
            filled[rid] = sig
    print(f"  可计算 = {len(filled)}  跳过（计算失败/空）= {len(rows) - len(filled)}")
    for rid, sig in list(filled.items())[:5]:
        print(f"   {rid}: {sig[:80]}")

    if a.stats and filled:
        # 直接按签名计数（skeleton_distribution 吃的是表达式列表，这里已是指纹）
        c0 = collections.Counter(filled.values())
        print(f"  存量骨架复用：唯一={len(c0)} 复用率={len(filled)/len(c0):.1f}")

    if not a.apply:
        print("\n[dry-run] 未写库。确认后加 --apply。")
        return
    conn.execute("BEGIN")
    conn.executemany("UPDATE expressions SET skeleton=? WHERE id=? AND skeleton IS NULL",
                     [(sig, rid) for rid, sig in filled.items()])
    conn.commit()
    n = conn.execute("SELECT COUNT(skeleton) FROM expressions").fetchone()[0]
    print(f"\n[apply] 已回填 {len(filled)} 行 → expressions.skeleton（全库非空现为 {n}）")

    if a.stats:
        allsigs = [r[0] for r in conn.execute(
            "SELECT skeleton FROM expressions WHERE skeleton IS NOT NULL")]
        c = collections.Counter(allsigs)
        tot = len(allsigs)
        print(f"\n全库骨架复用率 = {tot}/{len(c)} = {tot/len(c):.1f}")
        print("Top5 簇：")
        for s, n2 in c.most_common(5):
            print(f"  {n2:>5} ({n2/tot*100:4.1f}%)  {s[:88]}")


if __name__ == "__main__":
    main()
