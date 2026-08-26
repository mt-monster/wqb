import sqlite3

conn = sqlite3.connect('data/wqb.db')
cursor = conn.cursor()

# 清除 wave 14 checkpoint
cursor.execute("DELETE FROM ledger_kv WHERE region='USA' AND key='ckpt_w14'")
conn.commit()

print('[OK] 已清除 wave 14 checkpoint')

conn.close()
