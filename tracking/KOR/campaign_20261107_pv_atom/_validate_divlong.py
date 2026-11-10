import sys,json; sys.path.insert(0,'src')
from wqb.expression.op_arity import check_expressions
E=json.load(open(sys.argv[1],encoding='utf-8'))
res=check_expressions(E)
print("ok",res.get("ok"),"passed",res.get("passed"),"/",res.get("total"))
for it in res.get("items",[]):
    if not it.get("valid"): print("INVALID",it.get("errors"))
