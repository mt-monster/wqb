"""打印指定波次全部结果（不排序截断）。"""
import json
import sys

for t in sys.argv[1:]:
    d = json.load(open(f"tracking/EUR/results/{t}_checkpoint.json", encoding="utf-8"))
    rs = d["results"]
    print(f"=== {t} n={len(rs)} ran_at={d.get('ran_at')}")
    for r in rs:
        fails = (r.get("failed_checks") or r.get("error") or "")[:40]
        print(f"  {str(r.get('id')):12} S={r.get('sharpe')} F={r.get('fitness')} "
              f"TO={r.get('turnover_pct')} FAIL={fails} | {r.get('note')}")
