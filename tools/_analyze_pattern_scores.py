import json
from collections import Counter

d = json.load(open('D:/coding/traeCN_project/wqb/tracking/GBR/reference/gbr_pattern_scores_fields.json', encoding='utf-8'))
fields = d['fields']
print(f'Total fields: {len(fields)}')

# Categorize by pattern type
patterns = Counter()
for f in fields:
    fid = f['id']
    # Extract pattern name
    for pat in ['asc_triangle', 'desc_triangle', 'sym_triangle', 'rising_wedge', 'falling_wedge',
                'breakaway_gap', 'common_gap', 'v_reversal', 'v_continuation', 'head_shoulders',
                'double_top', 'double_bottom', 'triple_top', 'triple_bottom', 'flag', 'pennant',
                'cup_handle', 'rounding', 'rectangle', 'diamond', 'wedge', 'gap', 'triangle',
                'support_flat', 'resistance_flat']:
        if pat in fid:
            patterns[pat] += 1
            break
    else:
        patterns['other'] += 1

print('\n=== Pattern categories ===')
for k, v in patterns.most_common():
    print(f'  {k}: {v}')

# Extract stat types
stats = Counter()
for f in fields:
    fid = f['id']
    if 'mean_simscore' in fid: stats['mean'] += 1
    elif 'min_simscore' in fid: stats['min'] += 1
    elif 'max_simscore' in fid: stats['max'] += 1
    elif 'std_simscore' in fid: stats['std'] += 1
    elif 'dynamic_simscore' in fid: stats['dynamic'] += 1
    elif 'adaptive_similarity' in fid: stats['adaptive'] += 1
    else: stats['other_stat'] += 1

print('\n=== Stat types ===')
for k, v in stats.most_common():
    print(f'  {k}: {v}')

# Lookback windows
lookbacks = Counter()
for f in fields:
    fid = f['id']
    if 'lookback120' in fid or '_120' in fid: lookbacks['120'] += 1
    elif 'lookback60' in fid or '_60' in fid: lookbacks['60'] += 1
    else: lookbacks['none'] += 1

print('\n=== Lookback windows ===')
for k, v in lookbacks.most_common():
    print(f'  {k}: {v}')

# List all unique field IDs grouped by pattern
print('\n=== Sample fields by pattern ===')
seen_patterns = set()
for f in fields:
    fid = f['id']
    for pat in ['asc_triangle', 'desc_triangle', 'sym_triangle', 'rising_wedge', 'falling_wedge',
                'breakaway_gap', 'common_gap', 'v_reversal', 'v_continuation']:
        if pat in fid and pat not in seen_patterns:
            print(f'\n  [{pat}]')
            # Print all fields with this pattern
            for f2 in fields:
                if pat in f2['id']:
                    print(f"    {f2['id']}  cov={f2['coverage']:.4f}")
            seen_patterns.add(pat)
            break
