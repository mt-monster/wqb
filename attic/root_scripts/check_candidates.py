import sqlite3
import json

conn = sqlite3.connect('data/wqb.db')
cursor = conn.cursor()

# 查询 Wave 1 的候选表达式（Sharpe >= 1.0）
cursor.execute('''
    SELECT code, sharpe, fitness, returns, turnover, margin, 
           two_year_sharpe, sub_universe_sharpe, ra_failed_count, ra_failed_checks,
           ppa_failed_count, ppa_failed_checks, alpha_id
    FROM backtest_results
    WHERE region='USA' AND wave='1' AND sharpe >= 1.0
    ORDER BY sharpe DESC
''')

results = cursor.fetchall()
print(f'Wave 1 候选表达式（Sharpe >= 1.0，共 {len(results)} 条）:')
print('=' * 120)

for i, row in enumerate(results, 1):
    (code, sharpe, fitness, returns, turnover, margin, 
     two_year_sharpe, sub_universe_sharpe, ra_failed_count, ra_failed_checks,
     ppa_failed_count, ppa_failed_checks, alpha_id) = row
    
    print(f'\n{i}. Alpha ID: {alpha_id}')
    print(f'   Expression: {code}')
    print(f'   Sharpe: {sharpe:.3f} | Fitness: {fitness:.3f} | Turnover: {turnover:.2f} | Margin: {margin:.6f}')
    print(f'   2Y Sharpe: {two_year_sharpe if two_year_sharpe else "N/A"} | Sub Universe Sharpe: {sub_universe_sharpe if sub_universe_sharpe else "N/A"}')
    print(f'   RA Failed: {ra_failed_count} | PPA Failed: {ppa_failed_count}')
    
    if ra_failed_checks:
        ra_checks = json.loads(ra_failed_checks) if isinstance(ra_failed_checks, str) else ra_failed_checks
        print(f'   RA Failed Checks: {ra_checks}')
    
    if ppa_failed_checks:
        ppa_checks = json.loads(ppa_failed_checks) if isinstance(ppa_failed_checks, str) else ppa_failed_checks
        print(f'   PPA Failed Checks: {ppa_checks}')

conn.close()
