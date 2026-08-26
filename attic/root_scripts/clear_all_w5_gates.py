import sqlite3

conn = sqlite3.connect('data/wqb.db')
cursor = conn.cursor()

# 查询所有 wave 5 相关的 keys（包括 gate）
cursor.execute("SELECT key FROM ledger_kv WHERE region='USA' AND (key LIKE '%w5%' OR key LIKE '%wave5%' OR key LIKE 'gate_w5%')")
keys = cursor.fetchall()

print('所有 wave 5 相关的 keys:')
for key in keys:
    print(f'  {key[0]}')
    cursor.execute("DELETE FROM ledger_kv WHERE region='USA' AND key=?", (key[0],))
    print(f'    已删除: {cursor.rowcount} 行')

conn.commit()
conn.close()

