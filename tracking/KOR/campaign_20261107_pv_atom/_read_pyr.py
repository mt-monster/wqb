import json,sys
raw=open(sys.argv[1],encoding="utf-8-sig").read(); d=json.loads(raw[raw.find("{"):])
pyr=d.get("pyramids") or {}
kor=pyr.get("KOR") or {}
print("KOR keys:",list(kor.keys()))
for delay,cats in kor.items():
    print("== KOR",delay)
    for c,n in sorted(cats.items(), key=lambda x:-x[1]):
        lit="LIT" if n>=3 else "unlit"
        print(f"  {c:15} {n}  {lit}")
