import sqlite3

conn = sqlite3.connect('data/wqb.db')
cursor = conn.cursor()

# 清除 wave 7 相关的 checkpoint
cursor.execute("DELETE FROM ledger_kv WHERE key LIKE 'ckpt_w7%'")
cursor.execute("DELETE FROM ledger_kv WHERE key LIKE '%wave%7%'")
cursor.execute("DELETE FROM ledger_kv WHERE key LIKE 's2_compliance_w7'")

# 清除 expressions 表中 wave 7 的记录
cursor.execute("DELETE FROM expressions WHERE region='USA' AND wave='7'")

# 清除 backtest_results 表中 wave 7 的记录
cursor.execute("DELETE FROM backtest_results WHERE region='USA' AND wave='7'")

conn.commit()
conn.close()

print("Wave 7 checkpoint 和旧数据已清除")
