# -*- coding: utf-8 -*-
"""migrate_phase2.py - Phase 2 迁移：registry 实证层 + wave 结果台账 + 跨区教训入 SQLite。

数据源（Phase 1 拆分后的结构）：
  - research-data/registry/index.json        -> cross_region_lessons 表
  - research-data/registry/<REGION>.json     -> registry_empirical 表（dead_ends/wins/orphans/campaigns）
  - tracking/<REGION>/results/wave*_results.json -> wave_results 表
  - tracking/<REGION>/results/_archive/waves_*.json -> wave_results 表（archived=1）

幂等：UNIQUE 约束 + INSERT OR REPLACE，可重复跑。
用法：
  python tools/migrate_phase2.py --dry-run   # 只统计不写库
  python tools/migrate_phase2.py             # 实跑
"""
import argparse
import glob
import json
import re
import sqlite3
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DB = ROOT / "data" / "wqb.db"
SCHEMA = ROOT / "database" / "schema_phase2.sql"
REGISTRY_DIR = ROOT / "research-data" / "registry"

CLOSED_MARKERS = ("FINAL VERDICT", "REJECTED", "SUBMITTED", "EXHAUSTED", "DEAD")


def load_json(p):
    # utf-8-sig 兼容 BOM
    with open(p, "r", encoding="utf-8-sig") as f:
        return json.load(f)


def wave_num_from_name(name):
    m = re.search(r"wave(\d+)", name)
    return int(m.group(1)) if m else -1


def is_closed_wave(data):
    if isinstance(data, list):
        text = json.dumps(data, ensure_ascii=False)
        return any(m in text for m in CLOSED_MARKERS)
    if not isinstance(data, dict):
        return False
    findings = data.get("key_findings", [])
    blob = " ".join(str(x) for x in findings) if isinstance(findings, list) else str(findings)
    text = f"{blob} {data.get('verdict', '')} {data.get('status', '')}"
    return any(m in text for m in CLOSED_MARKERS)


def init_schema(conn):
    with open(SCHEMA, "r", encoding="utf-8") as f:
        conn.executescript(f.read())


def migrate_cross_region_lessons(conn, dry_run):
    idx = REGISTRY_DIR / "index.json"
    if not idx.exists():
        print("[SKIP] index.json not found")
        return 0
    data = load_json(idx)
    lessons = data.get("cross_region_lessons", [])
    n = 0
    for les in lessons:
        row = (
            les.get("id"), les.get("family"), les.get("finding"), les.get("rule"),
        )
        if not dry_run:
            conn.execute("""
                INSERT OR REPLACE INTO cross_region_lessons (lesson_id, family, finding, rule, updated_at)
                VALUES (?, ?, ?, ?, datetime('now'))
            """, row)
        n += 1
    return n


def migrate_registry_empirical(conn, dry_run):
    n = 0
    for fp in sorted(REGISTRY_DIR.glob("*.json")):
        if fp.name == "index.json":
            continue
        region = fp.stem
        data = load_json(fp)
        emp = data.get("empirical", {})

        # dead_ends
        for de in emp.get("dead_ends", []):
            row = (region, "dead_end", de.get("id"), de.get("family"),
                   json.dumps(de, ensure_ascii=False), de.get("dead_at"))
            if not dry_run:
                conn.execute("""
                    INSERT OR REPLACE INTO registry_empirical (region, layer, entry_id, family, payload, dead_at, updated_at)
                    VALUES (?, ?, ?, ?, ?, ?, datetime('now'))
                """, row)
            n += 1

        # wins
        for w in emp.get("wins", []):
            row = (region, "win", w.get("id"), w.get("what"),
                   json.dumps(w, ensure_ascii=False), w.get("date"))
            if not dry_run:
                conn.execute("""
                    INSERT OR REPLACE INTO registry_empirical (region, layer, entry_id, family, payload, dead_at, updated_at)
                    VALUES (?, ?, ?, ?, ?, ?, datetime('now'))
                """, row)
            n += 1

        # orphans（list of str 或 list of dict）
        for o in emp.get("orphans", []):
            oid = o.get("id") if isinstance(o, dict) else str(o)
            row = (region, "orphan", oid, None,
                   json.dumps(o, ensure_ascii=False) if isinstance(o, dict) else json.dumps({"id": oid}),
                   None)
            if not dry_run:
                conn.execute("""
                    INSERT OR REPLACE INTO registry_empirical (region, layer, entry_id, family, payload, dead_at, updated_at)
                    VALUES (?, ?, ?, ?, ?, ?, datetime('now'))
                """, row)
            n += 1

        # campaigns（list of dict 或 dict of dict）
        camps = emp.get("campaigns", [])
        if isinstance(camps, dict):
            camps = [{"dataset": k, **v} if isinstance(v, dict) else {"dataset": k, "note": str(v)}
                     for k, v in camps.items()]
        for c in camps:
            cid = c.get("dataset") or c.get("id")
            row = (region, "campaign", cid, c.get("dataset"),
                   json.dumps(c, ensure_ascii=False), None)
            if not dry_run:
                conn.execute("""
                    INSERT OR REPLACE INTO registry_empirical (region, layer, entry_id, family, payload, dead_at, updated_at)
                    VALUES (?, ?, ?, ?, ?, ?, datetime('now'))
                """, row)
            n += 1
    return n


def extract_candidates(data):
    """从 wave JSON 提取候选 alpha 摘要（各子批次的 list 项）。"""
    cands = []
    if not isinstance(data, dict):
        return cands
    for k, v in data.items():
        if isinstance(v, list):
            for item in v:
                if isinstance(item, dict) and "id" in item and ("sharpe" in item or "variant" in item):
                    cands.append({
                        "batch": k,
                        "id": item.get("id"),
                        "variant": item.get("variant"),
                        "sharpe": item.get("sharpe"),
                        "fit": item.get("fit"),
                        "tvr": item.get("tvr"),
                        "fail": item.get("fail"),
                        "note": item.get("note"),
                    })
    return cands


def migrate_wave_results(conn, region, dry_run):
    n = 0
    results_dir = ROOT / "tracking" / region / "results"
    if not results_dir.exists():
        return 0

    # 活跃文件
    for fp in sorted(results_dir.glob("wave*_results.json")):
        wn = wave_num_from_name(fp.name)
        if wn < 0:
            continue
        try:
            data = load_json(fp)
        except Exception as e:
            print(f"[SKIP] {fp.name} parse error: {e}")
            continue
        if not isinstance(data, dict):
            print(f"[SKIP] {fp.name} top-level is {type(data).__name__}, not dict")
            continue
        row = (
            region, wn,
            data.get("focus") or data.get("theme"),
            data.get("context"),
            json.dumps(data.get("key_findings", []), ensure_ascii=False),
            json.dumps(extract_candidates(data), ensure_ascii=False),
            json.dumps(data.get("batches", []), ensure_ascii=False),
            data.get("verdict"),
            "closed" if is_closed_wave(data) else "open",
            str(fp.relative_to(ROOT)),
            0,
        )
        if not dry_run:
            conn.execute("""
                INSERT OR REPLACE INTO wave_results
                (region, wave_number, focus, context, key_findings, candidates, batches, verdict, status, source_file, archived, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, datetime('now'))
            """, row)
        n += 1

    # 归档文件
    for fp in sorted((results_dir / "_archive").glob("waves_*.json")):
        try:
            arch = load_json(fp)
        except Exception as e:
            print(f"[SKIP] {fp.name} parse error: {e}")
            continue
        for wkey, data in arch.get("waves", {}).items():
            wn = wave_num_from_name(wkey)
            if wn < 0:
                continue
            if not isinstance(data, dict):
                print(f"[SKIP] {fp.name}:{wkey} top-level is {type(data).__name__}, not dict")
                continue
            row = (
                region, wn,
                data.get("focus") or data.get("theme"),
                data.get("context"),
                json.dumps(data.get("key_findings", []), ensure_ascii=False),
                json.dumps(extract_candidates(data), ensure_ascii=False),
                json.dumps(data.get("batches", []), ensure_ascii=False),
                data.get("verdict"),
                "closed",
                str(fp.relative_to(ROOT)),
                1,
            )
            if not dry_run:
                conn.execute("""
                    INSERT OR REPLACE INTO wave_results
                    (region, wave_number, focus, context, key_findings, candidates, batches, verdict, status, source_file, archived, updated_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, datetime('now'))
                """, row)
            n += 1
    return n


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--regions", default="MEA,USA,KOR,ASI,EUR,GBR,HKG,IND,GLB,DEU")
    args = ap.parse_args()

    if not DB.exists():
        print(f"[ERROR] db not found: {DB}")
        return 1

    conn = sqlite3.connect(DB)
    init_schema(conn)

    n_lessons = migrate_cross_region_lessons(conn, args.dry_run)
    n_emp = migrate_registry_empirical(conn, args.dry_run)
    n_waves = 0
    for region in args.regions.split(","):
        n_waves += migrate_wave_results(conn, region.strip(), args.dry_run)

    if not args.dry_run:
        conn.commit()

    # 验证
    c = conn.cursor()
    for t in ("cross_region_lessons", "registry_empirical", "wave_results"):
        c.execute(f'SELECT COUNT(*) FROM "{t}"')
        print(f"[db] {t}: {c.fetchone()[0]} rows")

    conn.close()
    print(f"[{'DRY-RUN' if args.dry_run else 'OK'}] lessons={n_lessons} empirical={n_emp} waves={n_waves}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
