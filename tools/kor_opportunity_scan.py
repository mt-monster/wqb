#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""kor_opportunity_scan.py — KOR 机会空间穷举扫描（S-PRE 用，2026-09-28）。

解决的问题：S-PRE 原先只看 S0 评分 top-N 选白名单，且死路检查是 **region-scoped**
（漏跨区负先验）且**大小写敏感**（`shortinterest3` 命不中 `KOR-SHORTINTEREST3-DEAD`）
→ 系统性高估机会空间、白烧回测。

本工具对全区数据集做四道过滤，输出**真实可打集合**：
  ① 类别未点亮（KOR/D1 实测 lit = ANALYST/MODEL/OTHER/PV，按 SOP 硬规则 0 排除作主数据集）
  ② 非区域红榜族（chart_patterns / news_sentiment / ai_ml / credit_risk / glb_emotion）
  ③ **跨区**死路检查（不限 region，大小写不敏感，同时查 entry_id 与 payload）
  ④ 字段数 ≥5（dataset_health.field_count_hard_min）

用法: python tools/kor_opportunity_scan.py [--region KOR] [--min-fields 5] [--json out.json]
"""
from __future__ import annotations

import argparse
import json
# 2026-09-28：构造级死路标记 —— 死路 rule/reason 含这些字样时，死的是「构造方式」
# 而非数据集本身（实证 shortinterest38 被 wave96 bare-skeleton 死路误杀，
# 论坛换构造后 Sharpe 2.43 全闸通过）。此类条目降为约束，不封锁数据集。
CONSTRUCTION_SCOPED_MARKERS = ("skeleton", "bare", "骨架", "构造",
                               "multi-field combos", "with multi-field",
                               "event-gating", "event-")

import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "src"))
from wqb.db_conn import connect as db_connect  # noqa: E402

# KOR/D1 实测已点亮类别（platform pyramid-multipliers，2026-09-28 实测）
LIT_CATEGORIES = {"ANALYST": 6, "MODEL": 4, "OTHER": 6, "PV": 3}
# 区域红榜族 → 对应类别应排除
RED_FAMILIES = ("chart_patterns", "news_sentiment", "ai_ml", "credit_risk", "glb_emotion")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--region", default="KOR")
    ap.add_argument("--min-fields", type=int, default=5)
    ap.add_argument("--json", default=None)
    a = ap.parse_args()

    conn = db_connect(readonly=True)
    rid = conn.execute("SELECT id FROM regions WHERE name=?", (a.region,)).fetchone()
    if not rid:
        print(f"[ERR] 未知区域 {a.region}")
        return 1
    rid = rid[0]

    rows = conn.execute(
        """SELECT d.name, d.category, d.field_count, d.coverage, d.alpha_count
           FROM datasets d WHERE d.region_id=? AND COALESCE(d.field_count,0)>=?
           ORDER BY d.category, COALESCE(d.alpha_count,0) DESC""",
        (rid, a.min_fields),
    ).fetchall()

    # 全部 dead_end 条目（跨区、大小写不敏感）
    dead = conn.execute(
        "SELECT region, entry_id, COALESCE(payload,'') FROM registry_empirical WHERE layer='dead_end'"
    ).fetchall()
    dead_blob = [(r[0], r[1], (r[1] + " " + r[2]).lower()) for r in dead]


    def xdead(name: str):
        """返回 (blocking, scoped) 两组死路命中（跨区、大小写不敏感）。

        2026-09-28 修正（第三类假阴性）：死路条目的 `rule` 若**只禁特定构造**
        （含 skeleton/bare/骨架/构造/multi-field 等字样），它是**构造级死路**——
        换构造仍可挖，不应封锁整个数据集。
        实证：`shortinterest38` 被 `KOR-WAVE96-UNLIT-BARE-SIGNAL-DEAD`（只禁
        bare rank/vec_avg 骨架）子串误杀；论坛 2026-09 换「比值→自身基线→峰值→
        sector」构造后 Sharpe 2.43 全闸通过并提交（KOR_InvFlowRev_sec_0.5704）。
        数据集级死路（rule 未限定构造，如 "do not re-mine shortinterest3"）才封锁。
        """
        key = name.lower()
        blocking, scoped = [], []
        for d in dead_blob:
            if key not in d[2]:
                continue
            raw = d[2].split(" ", 1)[1] if " " in d[2] else ""
            try:
                payload = json.loads(raw) if raw.lstrip().startswith("{") else {}
            except Exception:
                payload = {}
            blob = (str(payload.get("rule", "")) + " " +
                    str(payload.get("reason", ""))).lower()
            if any(m in blob for m in CONSTRUCTION_SCOPED_MARKERS):
                scoped.append(d)
            else:
                blocking.append(d)
        return blocking, scoped

    keep, blocked = [], []
    for name, cat, fc, cov, ac in rows:
        cat_u = (cat or "").upper()
        rec = {"dataset": name, "category": cat, "fields": fc,
               "coverage": round(cov, 4) if cov is not None else None,
               "platform_alphas": ac}
        # ① 已点亮类别 → 不得作主数据集
        if cat_u in LIT_CATEGORIES:
            rec["block_reason"] = f"已点亮类别 {cat_u}（SOP 硬规则 0：仅可作辅助腿）"
            blocked.append(rec)
            continue
        # ② 红榜族（NEWS/SENTIMENT 在 KOR 属 news_sentiment 红榜；chart_patterns → PV 子类）
        if cat_u in ("NEWS", "SENTIMENT"):
            rec["block_reason"] = "KOR 红榜族 news_sentiment"
            blocked.append(rec)
            continue
        # ③ 跨区死路（只认数据集级；构造级死路降为约束随行记录）
        blocking_hits, scoped_hits = xdead(name)
        if blocking_hits:
            regs = sorted({h[0] for h in blocking_hits})
            rec["block_reason"] = f"死路命中（{len(regs)} 区：{','.join(regs[:4])}）: " + \
                                  "; ".join(h[1] for h in blocking_hits[:3])
            rec["dead_regions"] = regs
            blocked.append(rec)
            continue
        if scoped_hits:
            regs = sorted({h[0] for h in scoped_hits})
            rec["construction_constraints"] = (
                f"构造级死路（{len(regs)} 区：{','.join(regs[:4])}）: "
                + "; ".join(h[1] for h in scoped_hits[:3])
                + " —— 数据集可用，但须避开该死路限定的构造方式")
            rec["construction_constraint_regions"] = regs
        keep.append(rec)

    conn.close()

    print(f"\n=== {a.region} 机会空间扫描（字段≥{a.min_fields}）===")
    print(f"候选数据集 {len(rows)} -> 通过四道过滤 {len(keep)} / 被排除 {len(blocked)}")
    print(f"（已点亮类别 {sorted(LIT_CATEGORIES)}；红榜族 {RED_FAMILIES}）\n")

    print("--- ★ 真实可打集合（未点亮 ∧ 非红榜 ∧ 无跨区死路 ∧ 字段足）---")
    print(f"{'dataset':<30} {'category':<13} {'fields':>6} {'cov':>7} {'platAlphas':>10}")
    for r in sorted(keep, key=lambda x: (-(x["platform_alphas"] or 0))):
        print(f"{r['dataset']:<30} {r['category']:<13} {r['fields']:>6} "
              f"{str(r['coverage']):>7} {str(r['platform_alphas']):>10}")
    if not keep:
        print("  （空 —— 该区在现有规则下已无可打数据集）")

    print("\n--- 被排除明细（前 25）---")
    for r in blocked[:25]:
        print(f"  ✗ {r['dataset']:<26} {r['block_reason'][:96]}")

    if a.json:
        Path(a.json).write_text(json.dumps(
            {"region": a.region, "min_fields": a.min_fields,
             "playable": keep, "blocked": blocked,
             "lit_categories": LIT_CATEGORIES, "red_families": list(RED_FAMILIES),
             "generated_at": __import__("datetime").datetime.now().isoformat(timespec="seconds")},
            ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"\n[写出] {a.json}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
