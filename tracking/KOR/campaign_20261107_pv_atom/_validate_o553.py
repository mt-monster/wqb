import sys,json; sys.path.insert(0,'src')
from wqb.expression.op_arity import check_expressions
E=json.load(open(sys.argv[1],encoding='utf-8'))
res=check_expressions(E)
print("ok",res.get("ok"),"passed",res.get("passed"),"/",res.get("total"))
for it in res.get("items",[]):
    if not it.get("valid"): print("INVALID",it.get("errors"))
# verify fields exist
raw=open(sys.argv[2],encoding='utf-8-sig').read(); d=json.loads(raw[raw.find('{'):])
ids={f.get('id') for f in (d.get('results') or [])}
import re
for e in E:
    for t in re.findall(r'oth553_[a-z0-9_]+', e):
        if t not in ids: print("MISSING FIELD",t)
