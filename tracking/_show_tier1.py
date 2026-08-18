import json, sys
path = sys.argv[1]
region = sys.argv[2]
d = json.load(open(path, encoding='utf-8'))
t1 = [r for r in d['ranking'] if r.get('tier') == 'tier1']
print(f"{region} tier1 count: {len(t1)} (total {d.get('total')})")
for r in t1[:30]:
    pm = r.get('pyramidMultiplier', '?')
    print(f"  {r['id']:42s} cov={r['coverage']:.2f} ac={r['alphaCount']:5d} fc={r['fieldCount']:5d} pm={pm} vs={r.get('valueScore','?')}")
