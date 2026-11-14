
import csv, re, collections, json, os
fp = r"D:\coding\traeCN_project\wqb\tracking\DEU\atom_orthogonal\pv20_fields.csv"
rows=[]
with open(fp, encoding="utf-8", errors="replace") as f:
    for r in csv.DictReader(f):
        if r.get("id"): rows.append(r)
print("pv20 total", len(rows))
ind = collections.Counter()
for r in rows:
    m = re.match(r'pv20_([a-z]+)_indicator_(\d+)_feature(\d+)$', r["id"])
    if m: ind[m.group(1)] += 1
print("indicator families:", dict(ind))
# 每个 metric 的 (indicator 编号集, feature 编号集)
by = collections.defaultdict(lambda: {"ind":set(),"feat":set()})
for r in rows:
    m = re.match(r'pv20_([a-z]+)_indicator_(\d+)_feature(\d+)$', r["id"])
    if m:
        by[m.group(1)]["ind"].add(int(m.group(2)))
        by[m.group(1)]["feat"].add(int(m.group(3)))
for k,v in sorted(by.items()):
    print(f'  {k:5s} indicators={sorted(v["ind"])} features={min(v["feat"])}..{max(v["feat"])} n={len(v["ind"])*len(v["feat"])}')
other=[r["id"] for r in rows if not re.match(r'pv20_[a-z]+_indicator_\d+_feature\d+$', r["id"])]
print("\n非 indicator 结构字段数:", len(other))
print("样例:", other[:40])
# 描述样例
print("\n描述样例（同一 metric 不同 feature）:")
cnt=0
for r in rows:
    if r["id"].startswith("pv20_ebi_indicator_1_feature"):
        print("  ", r["id"], "|", (r.get("desc") or "")[:150]); cnt+=1
        if cnt>=6: break
