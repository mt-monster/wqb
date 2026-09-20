# -*- coding: utf-8 -*-
"""migrate_campaign_state.py - 把 9 个区域的 <prefix>_d1_campaign_state.json 迁入 ledger_kv 表。

每个 JSON 文件的顶层 kv 平铺到 ledger_kv（region, key, value）。
幂等：UNIQUE(region, key) + INSERT OR REPLACE。

用法：
  python tools/migrate_campaign_state.py --dry-run
  python tools/migrate_campaign_state.py
"""
import argparse
import json
import sqlite3
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DB = ROOT / "data" / "wqb.db"

# 区域目录名 -> region 名（IND 目录里是 kor 文件，特殊处理）
REGION_FILES = {
    "ASI": ["asi_d1_campaign_state.json"],
    "EUR": ["eur_d1_campaign_state.json"],
    "GBR": ["gbr_d1_campaign_state.json"],
    "HKG": ["hkg_d1_campaign_state.json"],
    "IND": ["kor_d1_campaign_state.json"],  # IND 目录里是 kor 前缀（历史遗留）
    "KOR": ["kor_d1_campaign_state.json"],
    "MEA": ["mea_d1_campaign_state.json"],
    "USA": ["usa_d1_campaign_state.json"],
}

# KOR/results 下还有一个（重复，跳过）
SKIP = ["tracking/KOR/results/kor_d1_campaign_state.json"]


def load_json(p):
    with open(p, "r", encoding="utf-8-sig") as f:
        return json.load(f)


def ensure_table(conn):
    conn.execute("""
        CREATE TABLE IF NOT EXISTS ledger_kv (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            region VARCHAR(50) NOT NULL,
            key VARCHAR(200) NOT NULL,
            value JSON NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(region, key)
        )
    """)
    conn.execute("CREATE INDEX IF NOT EXISTS idx_ledger_kv_region ON ledger_kv(region)")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    conn = sqlite3.connect(DB)
    ensure_table(conn)

    total = 0
    for region, files in REGION_FILES.items():
        for fname in files:
            fp = ROOT / "tracking" / region / fname
            if not fp.exists():
                print(f"[SKIP] {fp} not found")
                continue
            try:
                data = load_json(fp)
            except Exception as e:
                print(f"[SKIP] {fp} parse error: {e}")
                continue
            if not isinstance(data, dict):
                print(f"[SKIP] {fp} top-level is {type(data).__name__}")
                continue

            n = 0
            for k, v in data.items():
                if not args.dry_run:
                    conn.execute("""
                        INSERT OR REPLACE INTO ledger_kv (region, key, value, updated_at)
                        VALUES (?, ?, ?, datetime('now'))
                    """, (region, k, json.dumps(v, ensure_ascii=False)))
                n += 1
            print(f"[{region}] {fname}: {n} keys")
            total += n

    if not args.dry_run:
        conn.commit()

    # 验证
    c = conn.cursor()
    c.execute("SELECT region, COUNT(*) FROM ledger_kv GROUP BY region ORDER BY region")
    print("\n=== ledger_kv by region ===")
    for r in c.fetchall():
        print(f"  {r[0]:6s} {r[1]} keys")

    conn.close()
    print(f"\n[{'DRY-RUN' if args.dry_run else 'OK'}] total={total} keys migrated")
    return 0


if __name__ == "__main__":
    sys.exit(main())
