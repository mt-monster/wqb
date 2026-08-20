import json
from collections import Counter

d = json.load(open(r'D:\coding\traeCN_project\wqb\tracking\GBR\reference\gbr_dataset_ranking.json', encoding='utf-8'))
rk = d['ranking']
print('tier dist:', Counter(r['tier'] for r in rk))
print('hard_excluded:', Counter(r.get('hard_excluded') for r in rk))
print()
t1 = [r for r in rk if r.get('tier') == 'tier1']
t1.sort(key=lambda r: -r.get('score', 0))
print('== tier1 (all, sorted by score) ==')
for r in t1:
    print(f"{r['id']:34s} cov={r['coverage']:.2f} fc={r['fieldCount']:>4} ac={r['alphaCount']:>5} py={r['pyramidMultiplier']:>5} vs={r['valueScore']:>3} score={r['score']:.3f} note={r.get('tier_note','')} dead={r.get('dead','')}")
print()
# datasets with ac>100 but strong signal (high score / not excluded)
print('== ac>100 datasets NOT hard_excluded, sorted by score ==')
hi = [r for r in rk if r.get('alphaCount', 0) > 100 and not r.get('hard_excluded')]
hi.sort(key=lambda r: -r.get('score', 0))
for r in hi[:30]:
    print(f"{r['id']:34s} cov={r['coverage']:.2f} fc={r['fieldCount']:>4} ac={r['alphaCount']:>5} py={r['pyramidMultiplier']:>5} vs={r['valueScore']:>3} score={r['score']:.3f} tier={r.get('tier','')} note={r.get('tier_note','')} dead={r.get('dead','')}")
