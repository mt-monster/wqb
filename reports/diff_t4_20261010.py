import json

base = json.load(open('output_report/deu_field_baseline_20261010.json'))
plat = json.load(open('output_report/deu_t4_platform_20261010.json'))['datasets']

print(f"{'dataset':<22}{'status':<26}{'local':>7}{'plat':>7}  rename/new  removed/full")
print("-"*95)
total_rename=0
total_full_removed=0
full_checked=0
for name, p in plat.items():
    b = base.get(name)
    if b is None:
        print(f"{name:<22}{p['status']:<26}{0:>7}{p['count']:>7}  (not in local baseline!)")
        continue
    local = set(b['fields'])
    plats = set(p['names'])
    status = p['status']
    if status == 'FULL':
        full_checked += 1
        removed = local - plats      # local name absent on platform -> renamed/removed
        new = plats - local          # platform name absent locally -> new field
        total_full_removed += len(removed)
        total_rename += len(new)
        flag = f"{len(new):>5}      {len(removed):>5}"
        print(f"{name:<22}{status:<26}{len(local):>7}{p['count']:>7}  {flag}")
    elif status.startswith('TRUNCATED'):
        new = plats - local          # rename/new within the 100-sample
        total_rename += len(new)
        print(f"{name:<22}{status:<26}{len(local):>7}{p['count']:>7}  new_in_sample={len(new):<5} (truncated; removed N/A)")
    else:  # EMPTY or SEARCH_AMBIGUOUS_ZERO
        print(f"{name:<22}{status:<26}{len(local):>7}{p['count']:>7}  platform returned 0")

print("-"*95)
print(f"FULL datasets definitively checked: {full_checked}")
print(f"Total rename/new fields detected   : {total_rename}")
print(f"Total removed fields (FULL only)   : {total_full_removed}")
