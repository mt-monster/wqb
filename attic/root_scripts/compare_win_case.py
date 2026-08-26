import sqlite3

conn = sqlite3.connect('data/wqb.db')
cursor = conn.cursor()

# 查询成功案例的回测结果
cursor.execute("""
    SELECT code, sharpe, fitness, turnover, alpha_id
    FROM backtest_results
    WHERE alpha_id='GrlGJnPJ'
""")
win_result = cursor.fetchone()

# 查询我们的 Top 3 候选表达式
cursor.execute("""
    SELECT code, sharpe, fitness, turnover, alpha_id
    FROM backtest_results
    WHERE region='USA' AND wave='9'
    ORDER BY sharpe DESC
    LIMIT 3
""")
our_results = cursor.fetchall()

print('成功案例 vs 我们的候选表达式:\n')
print(f'{"Alpha ID":<15} {"Sharpe":<10} {"Fitness":<10} {"Turnover":<10} {"Expression":<80}')
print('-' * 150)

if win_result:
    code, sharpe, fitness, turnover, alpha_id = win_result
    code_str = code[:77] + '...' if len(code) > 80 else code
    print(f'{alpha_id:<15} {sharpe:<10.3f} {fitness:<10.3f} {turnover:<10.3f} {code_str:<80}')

print()
for row in our_results:
    code, sharpe, fitness, turnover, alpha_id = row
    code_str = code[:77] + '...' if len(code) > 80 else code
    print(f'{alpha_id:<15} {sharpe:<10.3f} {fitness:<10.3f} {turnover:<10.3f} {code_str:<80}')

conn.close()
