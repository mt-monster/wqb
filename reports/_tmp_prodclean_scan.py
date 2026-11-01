import sqlite3

con = sqlite3.connect(r"D:/coding/traeCN_project/wqb/data/wqb.db")
con.row_factory = sqlite3.Row
cur = con.cursor()

print("=== region_id 分布（alphas 表无 region 列，用 region_id 近似 + universe 佐证）===")
for r in cur.execute("""
    SELECT region_id, universe, stage, COUNT(*) n,
           SUM(CASE WHEN prod_correlation IS NOT NULL AND prod_correlation < 0.7 THEN 1 ELSE 0 END) prod_ok
    FROM alphas
    WHERE stage = 'IS' AND (status IS NULL OR status != 'ACTIVE')
    GROUP BY region_id, universe, stage
    ORDER BY n DESC
"""):
    print(dict(r))

print()
print("=== stage=IS 且 prod<0.7 已实测的候选（全区域，按 region_id 分）===")
rows = list(cur.execute("""
    SELECT alpha_id, region_id, universe, delay, neutralization, dataset_id,
           sharpe, fitness, two_year_sharpe, sub_universe_sharpe,
           prod_correlation, self_correlation, turnover, status, alpha_type,
           substr(expression,1,110) expr
    FROM alphas
    WHERE stage = 'IS'
      AND prod_correlation IS NOT NULL AND prod_correlation < 0.7
      AND (status IS NULL OR status NOT IN ('ACTIVE','SUPERSEDED'))
    ORDER BY region_id, prod_correlation ASC
"""))
print("count:", len(rows))
hdr = "%-11s %-4s %-11s %-13s %-5s %6s %6s %6s %6s %7s %7s %s"
print(hdr % ("alpha_id", "rid", "universe", "neut", "delay", "S", "F", "2Y", "SUB", "prod", "self", "status"))
for r in rows:
    print(hdr % (r["alpha_id"], r["region_id"], str(r["universe"])[:11], str(r["neutralization"])[:13],
                 r["delay"], r["sharpe"], r["fitness"], r["two_year_sharpe"], r["sub_universe_sharpe"],
                 r["prod_correlation"], r["self_correlation"], str(r["status"])[:12]))
print()
for r in rows:
    print(r["alpha_id"], "| ds", r["dataset_id"], "|", str(r["expr"]))
con.close()
