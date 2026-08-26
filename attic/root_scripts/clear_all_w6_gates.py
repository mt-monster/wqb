import sqlite3
import os

db_path = 'data/wqb.db'
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# 清除 wave 6 相关的 checkpoint
cursor.execute("DELETE FROM ledger_kv WHERE key LIKE 'ckpt_w6%'")
cursor.execute("DELETE FROM ledger_kv WHERE key LIKE '%wave%6%'")
cursor.execute("DELETE FROM ledger_kv WHERE key LIKE 's2_compliance_w6'")

# 清除 expressions 表中 wave 6 的记录
cursor.execute("DELETE FROM expressions WHERE region='USA' AND wave='6'")

# 清除 backtest_results 表中 wave 6 的记录
cursor.execute("DELETE FROM backtest_results WHERE region='USA' AND wave='6'")

conn.commit()
conn.close()

print("Wave 6 checkpoint 和旧数据已清除")
