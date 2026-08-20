import json, sys
with open('D:/coding/traeCN_project/wqb/tracking/GBR/reference/gbr_dataset_ranking.json', encoding='utf-8') as f:
    d = json.load(f)
r = d['ranking']
print('=== TIER1 whitelist ===')
for x in r:
    if x.get('tier') == 'tier1':
        print(f"{x['id']:30s} score={x['score']:.4f} cov={x['coverage']:.4f} fields={x['fieldCount']:5d} alphas={x['alphaCount']:6d} cat={x['category']:12s} pyr={x['pyramidMultiplier']}")
print()
print('=== TIER2 backup (top 20) ===')
count = 0
for x in r:
    if x.get('tier') == 'tier2' and count < 20:
        print(f"{x['id']:30s} score={x['score']:.4f} cov={x['coverage']:.4f} fields={x['fieldCount']:5d} alphas={x['alphaCount']:6d} cat={x['category']:12s} pyr={x['pyramidMultiplier']}")
        count += 1
print()
print(f"Total: {d['total']}, dead_excluded: {d['dead_excluded']}")
