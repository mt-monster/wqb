
import csv, json, os, re, glob, collections

BASE = r"D:\coding\traeCN_project\wqb\tracking\DEU\atom_orthogonal"
ROOT = r"D:\coding\traeCN_project\wqb\tracking\DEU"
BT = chr(96)

EXPR_HINT = re.compile(r'[A-Za-z_][A-Za-z0-9_]*\s*\(')
exprs = []

def walk_json(obj, depth=0):
    if depth > 12: return
    if isinstance(obj, dict):
        for v in obj.values(): walk_json(v, depth+1)
    elif isinstance(obj, list):
        for v in obj: walk_json(v, depth+1)
    elif isinstance(obj, str):
        if len(obj) < 4000 and EXPR_HINT.search(obj) and (')' in obj):
            exprs.append(obj)

njson = nmd = 0
for dirpath, _, fns in os.walk(ROOT):
    for fn in fns:
        low = fn.lower()
        fp = os.path.join(dirpath, fn)
        try:
            sz = os.path.getsize(fp)
        except OSError:
            continue
        if sz > 8_000_000: continue
        if low.endswith(".json"):
            try: txt = open(fp, encoding="utf-8", errors="replace").read()
            except OSError: continue
            njson += 1
            try: walk_json(json.loads(txt))
            except Exception:
                for m in re.findall(r'"([^"\\]{8,3800})"', txt):
                    if EXPR_HINT.search(m) and (')' in m): exprs.append(m)
        elif low.endswith(".md"):
            nmd += 1
            try:
                for line in open(fp, encoding="utf-8", errors="replace"):
                    s = line.strip().strip(BT)
                    if len(s) < 4000 and EXPR_HINT.search(s) and (')' in s) and not s.startswith('#'):
                        exprs.append(s)
            except OSError: pass

used = set(re.findall(r"[A-Za-z_][A-Za-z0-9_]*", "\n".join(exprs)))

ds_meta = {}
with open(os.path.join(BASE, "deu_datasets_20261108_full.csv"), encoding="utf-8", errors="replace") as f:
    for row in csv.DictReader(f): ds_meta[row["id"]] = row

fields = {}
for fp in glob.glob(os.path.join(BASE,"*_fields.csv")) + glob.glob(os.path.join(BASE,"*","fields","*_fields.csv")):
    ds = os.path.basename(fp)[:-len("_fields.csv")]
    rws = []
    with open(fp, encoding="utf-8", errors="replace") as f:
        for row in csv.DictReader(f):
            if row.get("id"): rws.append(row)
    if rws: fields[ds] = rws

LIT = {"ANALYST","MODEL","SHORTINTEREST"}
def num(x,d=0.0):
    try: return float(x)
    except: return d

rows = []
for ds, fl in fields.items():
    tower = (ds_meta.get(ds,{}).get("cat") or "?").upper()
    usedf = [f for f in fl if f["id"] in used]
    un = [f for f in fl if f["id"] not in used]
    rows.append({"ds":ds,"tower":tower,"lit":tower in LIT,"n":len(fl),
                 "used":len(usedf),"untested":len(un),
                 "cov":num(ds_meta.get(ds,{}).get("cov")),
                 "sumac":sum(num(f.get("ac")) for f in un),
                 "maxac":max([num(f.get("ac")) for f in un], default=0),
                 "used_ids":[f["id"] for f in usedf]})
rows.sort(key=lambda r: (-r["untested"], -r["sumac"]))
json.dump(rows, open(os.path.join(BASE,"_recheck_expr_only.json"),"w",encoding="utf-8"), ensure_ascii=False, indent=1)

tot = sum(r["n"] for r in rows); totu = sum(r["untested"] for r in rows)
print(json.dumps({"expr_strings":len(exprs),"json_files":njson,"md_files":nmd,
                  "expr_tokens":len(used),"fields_total":tot,"untested_total":totu,
                  "pct":round(100*totu/tot,1)}, ensure_ascii=False))

print("\n=== unlit towers: untested field TOP 20 ===")
print("dataset                     tower        n   used untest   cov  sumac")
for r in [x for x in rows if not x["lit"]][:20]:
    print('%-28s%-12s%6d%6d%7d%6.2f%7.0f' % (r["ds"], r["tower"], r["n"], r["used"], r["untested"], r["cov"], r["sumac"]))

for r in rows:
    if r["ds"]=="pv20":
        print("\npv20 really-tested fields (%d):" % r["used"])
        for x in r["used_ids"]: print("   ", x)
