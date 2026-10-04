"""读 EUR 波次 checkpoint 并排序打印。用法: python tools/tmp_wave_ckpt.py wave275_risk62 [wave276_risk70 ...]"""
import json
import os
import sys

for t in sys.argv[1:]:
    p = f"tracking/EUR/results/{t}_checkpoint.json"
    print("===", t)
    if not os.path.exists(p):
        print("  MISSING")
        continue
    d = json.load(open(p, encoding="utf-8"))
    rs = d["results"]
    print(f"  ran_at={d.get('ran_at')}  n={len(rs)}")
    for r in sorted(rs, key=lambda x: -(x.get("sharpe") or -99)):
        fails = (r.get("failed_checks") or r.get("error") or "")[:40]
        print(f"   {str(r.get('id')):12} S={r.get('sharpe')} F={r.get('fitness')} "
              f"TO={r.get('turnover_pct')} 2Y={r.get('two_year_sharpe')} "
              f"FAIL={fails} | {r.get('note')}")
