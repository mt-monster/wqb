import sqlite3

con = sqlite3.connect(r"D:/coding/traeCN_project/wqb/data/wqb.db")
con.row_factory = sqlite3.Row
cur = con.cursor()

RID = 7  # GBR (universe TOP700)

rows = list(cur.execute("""
    SELECT alpha_id, region_id, universe, delay, neutralization, dataset_id,
           sharpe, fitness, two_year_sharpe, sub_universe_sharpe,
           prod_correlation, self_correlation, turnover, status, alpha_type,
           expression
    FROM alphas
    WHERE region_id = ? AND stage = 'IS'
      AND prod_correlation IS NOT NULL AND prod_correlation < 0.7
      AND (status IS NULL OR status NOT IN ('ACTIVE','SUPERSEDED'))
    ORDER BY sharpe DESC
""", (RID,)))
print("GBR (region_id=7) prod<0.7 未提交候选:", len(rows))
print("=" * 118)
hdr = "%-11s %-6s %-14s %6s %6s %6s %6s %7s %8s %8s %-11s"
print(hdr % ("alpha_id", "ds", "neut", "S", "F", "2Y", "SUB", "prod", "self", "TO", "status"))
for r in rows:
    print(hdr % (r["alpha_id"], r["dataset_id"], str(r["neutralization"])[:14],
                 r["sharpe"], r["fitness"], r["two_year_sharpe"], r["sub_universe_sharpe"],
                 r["prod_correlation"], r["self_correlation"], r["turnover"], str(r["status"])[:11]))
print("=" * 118)
for r in rows:
    print(r["alpha_id"], "|", r["alpha_type"], "| delay", r["delay"], "| prod", r["prod_correlation"],
          "| self", r["self_correlation"], "|", str(r["expression"])[:135])
con.close()
