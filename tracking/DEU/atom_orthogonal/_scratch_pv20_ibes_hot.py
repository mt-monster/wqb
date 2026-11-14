
import csv, re
fp = r"D:\coding\traeCN_project\wqb\tracking\DEU\atom_orthogonal\pv20_fields.csv"
rows=[]
with open(fp, encoding="utf-8", errors="replace") as f:
    for r in csv.DictReader(f):
        if r.get("id"): rows.append(r)
ib=[r for r in rows if re.match(r'pv20_[a-z]+_indicator_\d+_feature\d+$', r["id"])]
def n(x):
    try: return int(float(x))
    except: return 0
ib.sort(key=lambda r: -n(r["ac"]))
print("pv20 IBES 字段 hot TOP 15 (id | uc | ac):")
for r in ib[:15]:
    print("  %-40s uc=%3d ac=%4d | %s" % (r["id"], n(r["uc"]), n(r["ac"]), (r.get("desc") or "")[:70]))
print("\nIBES 字段中 ac>0 的个数:", sum(1 for r in ib if n(r["ac"])>0), "/", len(ib))
print("各 metric 的最高 ac:")
import collections
best=collections.defaultdict(lambda:(0,""))
for r in ib:
    m=re.match(r'pv20_([a-z]+)_indicator',r["id"]).group(1)
    if n(r["ac"])>best[m][0]: best[m]=(n(r["ac"]), r["id"])
for k,(a,i) in sorted(best.items(), key=lambda x:-x[1][0]):
    print("  %-5s ac=%4d  %s" % (k,a,i))
