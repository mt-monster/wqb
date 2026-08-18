import json, sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

d = json.load(open(r'D:\coding\traeCN_project\wqb\tracking\GBR\reference\gbr_dataset_ranking.json', encoding='utf-8'))
rk = d['ranking']
rows = [r for r in rk if not r.get('hard_excluded')]
rows.sort(key=lambda r: -r.get('score', 0))
n = len(rows)
print(f'non-hard-excluded rows: {n}')
for i, r in enumerate(rows):
    pct = (i + 1) / n
    print(f"rank={i+1:>2} pct={pct:.2f} {r['id']:34s} cov={r['coverage']:.2f} fc={r['fieldCount']:>4} ac={r['alphaCount']:>5} py={r['pyramidMultiplier']:>5} vs={r['valueScore']:>3} score={r['score']:.3f} tier={r.get('tier',''):8s} note={r.get('tier_note','')}")
