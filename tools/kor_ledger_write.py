#!/usr/bin/env python
"""KOR 台账写入（wqb-db MCP 未连接时的降级写库）。

用法: python tools/kor_ledger_write.py <key> <json_file>
按 ledger_kv(region,key) 唯一键 upsert。
"""
import json, sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from wqb.db_conn import connect as db_connect  # 规范工厂（禁裸 sqlite3.connect）

REGION = "KOR"


def upsert(key, value_obj):
    c = db_connect()
    try:
        now = datetime.now().isoformat(timespec="seconds")
        v = json.dumps(value_obj, ensure_ascii=False)
        cur = c.execute("SELECT id FROM ledger_kv WHERE region=? AND key=?", (REGION, key))
        row = cur.fetchone()
        if row:
            c.execute("UPDATE ledger_kv SET value=?, updated_at=? WHERE id=?", (v, now, row[0]))
            act = "UPDATE"
        else:
            c.execute("INSERT INTO ledger_kv(region,key,value,created_at,updated_at) VALUES(?,?,?,?,?)",
                      (REGION, key, v, now, now))
            act = "INSERT"
        c.commit()
        print(f"[{act}] ledger_kv KOR/{key} ({len(v)} chars)")
    finally:
        c.close()


if __name__ == "__main__":
    key = sys.argv[1]
    path = sys.argv[2]
    with open(path, encoding="utf-8") as f:
        obj = json.load(f)
    upsert(key, obj)
