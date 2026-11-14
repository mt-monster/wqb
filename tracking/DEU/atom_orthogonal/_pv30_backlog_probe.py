import sqlite3, json, io
c = sqlite3.connect("file:data/wqb.db?mode=ro", uri=True)
rows = c.execute("select id, status, expression from expressions where region=? and dataset=? and status in ('gem','gated') order by id", ("DEU","pv30")).fetchall()
lines = ["# pv30 积压清单（s2_pv30_d1，33 条从未回测）", "", "生成：2026-11-11 只读查询 expressions 表；可直接整批派发（字段已预检存在）。", ""]
for r in rows:
    lines.append("- [%s/%s] `%s`" % (r[0], r[1], r[2]))
open("tracking/DEU/atom_orthogonal/pv30_backlog_33_expressions.md", "w", encoding="utf-8").write("\n".join(lines))
print("written", len(rows))