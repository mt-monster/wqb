import sqlite3

conn = sqlite3.connect('data/wqb.db')
cursor = conn.cursor()

cursor.execute("SELECT key FROM ledger_kv WHERE region='USA' AND key LIKE '%ckpt%' OR key LIKE '%w3%'")
results = cursor.fetchall()

print('所有包含 ckpt 或 w3 的 ledger keys:')
for row in results:
    print(f'  {row[0]}')

conn.close()
