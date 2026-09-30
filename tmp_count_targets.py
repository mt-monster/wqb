# -*- coding: utf-8 -*-
"""临时统计：is 段可补列的填充率。"""
import sqlite3

con = sqlite3.connect("file:data/wqb.db?mode=ro", uri=True)
cur = con.cursor()
for t in ("backtest_results", "alphas"):
    cols = {r[1] for r in cur.execute(f'PRAGMA table_info("{t}")')}
    total = cur.execute(f'SELECT COUNT(*) FROM "{t}"').fetchone()[0]
    print(f"=== {t} (总 {total}) ===")
    for c in ("long_count", "short_count", "pnl", "book_size",
              "sharpe", "fitness", "turnover", "sub_universe_sharpe"):
        if c not in cols:
            print(f"  {c:22}缺列")
            continue
        n = cur.execute(f'SELECT COUNT(*) FROM "{t}" WHERE {c} IS NOT NULL').fetchone()[0]
        print(f"  {c:22}{n:>7}  {n/total*100:5.1f}%")
    print()
