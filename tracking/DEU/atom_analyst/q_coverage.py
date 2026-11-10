import sqlite3, json
con = sqlite3.connect('data/wqb.db')
con.row_factory = sqlite3.Row
q = '''
SELECT b.alpha_id, b.sharpe, b.fitness, b.turnover, b.two_year_sharpe, b.sub_universe_sharpe,
       b.long_count, b.short_count, b.ra_failed_checks, b.wave, b.code
FROM backtest_results b
WHERE b.region = 'DEU' AND b.dataset = 'analyst47'
ORDER BY b.sharpe DESC
'''
rows = [dict(x) for x in con.execute(q).fetchall()]
print(json.dumps(rows, ensure_ascii=False))
