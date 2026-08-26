import sqlite3
import json

conn = sqlite3.connect('data/wqb.db')
cursor = conn.cursor()

# 查询 wave 6 的 checkpoint
cursor.execute("SELECT key, value FROM ledger_kv WHERE region='USA' AND key LIKE '%w6%'")
results = cursor.fetchall()

print(f"找到 {len(results)} 条 wave 6 相关的 ledger 记录:")
for key, value in results:
    print(f"\n键: {key}")
    try:
        data = json.loads(value)
        print(f"值: {json.dumps(data, indent=2, ensure_ascii=False)[:500]}...")
    except:
        print(f"值: {value[:200]}...")

conn.close()
