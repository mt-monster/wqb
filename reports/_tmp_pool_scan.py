import sqlite3, collections

con = sqlite3.connect(r"D:/coding/traeCN_project/wqb/data/wqb.db")
con.row_factory = sqlite3.Row
cur = con.cursor()

rows = list(cur.execute("""
    SELECT a.alpha_id, a.region_id, a.universe, a.delay, a.dataset_id, a.neutralization,
           a.sharpe, a.fitness, a.two_year_sharpe, a.sub_universe_sharpe,
           a.prod_correlation, a.self_correlation, a.turnover, a.status, a.expression
    FROM alphas a
    WHERE a.stage = 'IS'
      AND a.prod_correlation IS NOT NULL AND a.prod_correlation < 0.7
      AND (a.status IS NULL OR a.status NOT IN ('ACTIVE','SUPERSEDED'))
      AND a.sharpe >= 1.58 AND a.fitness >= 1.0
      AND (a.two_year_sharpe IS NULL OR a.two_year_sharpe >= 1.58)
      AND (a.self_correlation IS NULL OR a.self_correlation < 0.7)
    ORDER BY a.region_id, a.sharpe DESC
"""))
print("全闸 + prod<0.7 + self<0.7 的未提交候选:", len(rows))
by = collections.Counter(r["region_id"] for r in rows)
print("按 region_id 分布:", dict(by))
print("=" * 112)
for r in rows:
    print("%-11s rid=%-3s %-11s S=%-5s F=%-5s 2Y=%-5s SUB=%-5s prod=%-7s self=%-8s | %s" % (
        r["alpha_id"], r["region_id"], str(r["universe"])[:11], r["sharpe"], r["fitness"],
        r["two_year_sharpe"], r["sub_universe_sharpe"], r["prod_correlation"], r["self_correlation"],
        str(r["expression"])[:64]))
con.close()
