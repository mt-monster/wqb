import sqlite3

conn = sqlite3.connect('data/wqb.db')
cursor = conn.cursor()

cursor.execute("DELETE FROM ledger_kv WHERE region='USA' AND key='ckpt_w4'")
conn.commit()
print(f'已删除 checkpoint，影响行数: {cursor.rowcount}')

conn.close()
