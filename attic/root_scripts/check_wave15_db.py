import sqlite3

conn = sqlite3.connect('data/wqb.db')
cursor = conn.cursor()

# 查询 backtest_results 表的结构
cursor.execute("PRAGMA table_info(backtest_results)")
columns = cursor.fetchall()
print('backtest_results 表结构:')
for col in columns:
    print(f'  {col}')

# 查询 Wave 15 的所有记录
cursor.execute("""
    SELECT *
    FROM backtest_results
    WHERE region='USA' AND wave='15'
""")

results = cursor.fetchall()
print(f'\nWave 15 的所有记录（共 {len(results)} 条）:')
for row in results:
    print(f'  {row}')

# 查询最近的回测记录
cursor.execute("""
    SELECT alpha_id, wave, sharpe, fitness, created_at
    FROM backtest_results
    WHERE region='USA'
    ORDER BY created_at DESC
    LIMIT 10
""")

results = cursor.fetchall()
print(f'\n最近的 10 条回测记录:')
for row in results:
    print(f'  {row}')

conn.close()
