import json, collections, re, sys
raw = open(sys.argv[1], encoding="utf-8-sig").read()
d = json.loads(raw[raw.find("{"):])
res = d.get("results") or []
# suffix families
suf = collections.Counter()
for f in res:
    fid = f.get("id") or ""
    m = re.match(r"^(anl44_\d+_)?(.+)$", fid)
    rest = m.group(2) if m else fid
    parts = rest.split("_")
    suf[parts[-1]] += 1
print("suffix_top=", suf.most_common(25))
print("--- MATRIX fields ---")
for f in res:
    if f.get("type") == "MATRIX":
        print(f.get("id"), "|cov", round(f.get("coverage") or 0,3), "|aC", f.get("alphaCount"), "|uC", f.get("userCount"), "|", (f.get("description") or "")[:80])
