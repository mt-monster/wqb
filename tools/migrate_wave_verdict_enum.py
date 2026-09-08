# -*- coding: utf-8 -*-
"""数据库迁移：wave_results.verdict 归一到三态枚举（2026-09-08）。

背景
----
`_lib/wave_results.upsert` 从 2026-09-01 起硬约束 verdict ∈ {PASS, FAIL, PARTIAL}
（机械判定 `WHERE verdict='FAIL'` 需要严格枚举），描述性结论一律放 key_findings。
但该约束落地前已有历史行写入了描述性 verdict（如 "0/8 过硬闸, 新高 0.02"、
"GATE_FAIL"），这些行对 `WHERE verdict IN (...)` 是隐形的。

本迁移把它们归一到三态，并把原文原样搬进 key_findings 首条，不丢信息。

映射规则（按序匹配，全部确定性，不猜）
------------------------------------
1. 已是 PASS/FAIL/PARTIAL 或空 → 跳过（空 verdict 由 upsert 的 status=closed 闸管）
2. GREEN:* → PASS  /  YELLOW:* → PARTIAL  /  RED:* → FAIL
   （auto_upsert_from_review 修复前会生成这三种前缀）
3. "<n>/<m> 过硬闸" → n>0 ? PASS : FAIL
4. 含 GATE_FAIL / FAIL / 全灭 → FAIL
5. 其余 → 不动，只报告，留人工判定（宁可漏改不可错改）

幂等：已归一的行第 1 条即跳过；key_findings 里已有同一条 "原 verdict（迁移前）"
不重复追加。

用法：
    python tools/migrate_wave_verdict_enum.py            # 默认 data/wqb.db
    python tools/migrate_wave_verdict_enum.py --dry-run  # 只打印不写
    python tools/migrate_wave_verdict_enum.py --db path/to.db
"""
import argparse
import json
import re
import sqlite3

VERDICT_OK = ("PASS", "FAIL", "PARTIAL")
NOTE_PREFIX = "原 verdict（迁移前）: "
_HARD_GATE_RE = re.compile(r"(\d+)\s*/\s*(\d+)\s*过硬闸")


def classify(verdict):
    """描述性 verdict -> (枚举值, 命中的规则名)；无法确定返回 (None, 原因)。"""
    v = (verdict or "").strip()
    if not v:
        return None, "空 verdict（跳过，由 status=closed 闸管）"
    if v in VERDICT_OK:
        return None, "已是枚举值"
    up = v.upper()
    if up.startswith("GREEN"):
        return "PASS", "GREEN 前缀"
    if up.startswith("YELLOW"):
        return "PARTIAL", "YELLOW 前缀"
    if up.startswith("RED"):
        return "FAIL", "RED 前缀"
    m = _HARD_GATE_RE.search(v)
    if m:
        n_pass = int(m.group(1))
        return ("PASS" if n_pass > 0 else "FAIL"), f"过硬闸计数 {m.group(1)}/{m.group(2)}"
    if "GATE_FAIL" in up or "FAIL" in up or "全灭" in v:
        return "FAIL", "FAIL/全灭 关键词"
    return None, "无匹配规则（需人工判定）"


def migrate(conn, dry_run=False):
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    placeholders = ",".join("?" * len(VERDICT_OK))
    rows = cur.execute(
        "SELECT id, region, wave_number, verdict, key_findings FROM wave_results "
        f"WHERE verdict IS NOT NULL AND TRIM(verdict) <> '' "
        f"AND TRIM(verdict) NOT IN ({placeholders}) ORDER BY id",
        VERDICT_OK,
    ).fetchall()

    actions = []
    changed = manual = 0
    for r in rows:
        tag = f"{r['region']}/wave{r['wave_number']} (id={r['id']})"
        new_verdict, rule = classify(r["verdict"])
        if new_verdict is None:
            manual += 1
            actions.append(f"[MANUAL] {tag} verdict={r['verdict']!r} -> {rule}")
            continue

        try:
            findings = json.loads(r["key_findings"] or "[]")
        except (TypeError, ValueError):
            findings = []
        if not isinstance(findings, list):
            findings = [findings]
        note = NOTE_PREFIX + r["verdict"]
        if note not in findings:
            findings.insert(0, note)

        if dry_run:
            actions.append(f"[DRY] {tag} {r['verdict']!r} -> {new_verdict}"
                           f"（{rule}；原文入 key_findings 首条）")
        else:
            cur.execute(
                "UPDATE wave_results SET verdict=?, key_findings=? WHERE id=?",
                (new_verdict, json.dumps(findings, ensure_ascii=False), r["id"]),
            )
            actions.append(f"[OK] {tag} {r['verdict']!r} -> {new_verdict}"
                           f"（{rule}；原文入 key_findings 首条）")
        changed += 1

    if not dry_run:
        conn.commit()

    actions.append(f"\n非枚举 verdict 行 {len(rows)} 条："
                   f"已归一 {changed}，待人工 {manual}")
    dist = cur.execute(
        "SELECT COALESCE(verdict, '<NULL>') v, COUNT(*) n FROM wave_results "
        "GROUP BY verdict ORDER BY n DESC"
    ).fetchall()
    actions.append("迁移后 verdict 分布：" +
                   ", ".join(f"{d['v']}={d['n']}" for d in dist))
    return actions


def main():
    ap = argparse.ArgumentParser(description="wave_results.verdict 三态归一迁移")
    ap.add_argument("--db", default="data/wqb.db")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    conn = sqlite3.connect(args.db)
    for a in migrate(conn, dry_run=args.dry_run):
        print(a)
    conn.close()
    print(f"\n{'[DRY-RUN] 未执行任何更改' if args.dry_run else '迁移完成'}: {args.db}")


if __name__ == "__main__":
    main()
