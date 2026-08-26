import sqlite3

conn = sqlite3.connect('data/wqb.db')
cursor = conn.cursor()

# 检查表结构
cursor.execute("PRAGMA table_info(backtest_results)")
columns = cursor.fetchall()
print("backtest_results 表结构:")
for col in columns:
    print(f"  {col}")

print("\n" + "="*80 + "\n")

# 检查 wave 6 的数据
cursor.execute("SELECT COUNT(*) FROM backtest_results WHERE region='USA' AND wave='6'")
count = cursor.fetchone()[0]
print(f"Wave 6 记录数: {count}")

# 检查所有 wave 的数据
cursor.execute("SELECT wave, COUNT(*) FROM backtest_results WHERE region='USA' GROUP BY wave ORDER BY wave")
waves = cursor.fetchall()
print("\n所有 wave 的记录数:")
for wave, count in waves:
    print(f"  wave={wave}: {count} 条")

conn.close()
