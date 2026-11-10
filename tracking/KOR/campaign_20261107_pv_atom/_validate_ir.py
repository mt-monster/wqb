import sys,json,re; sys.path.insert(0,'src')
from wqb.expression.op_arity import check_expressions
E=json.load(open(sys.argv[1],encoding='utf-8'))
res=check_expressions(E)
print("ok",res.get("ok"),"passed",res.get("passed"),"/",res.get("total"))
for it,e in zip(res.get("items",[]),E):
    nops=len(re.findall(r"[a-z_]+\(", e))
    print("valid",it.get("valid"),"ops~",nops,"|",e[:80], "| errs",it.get("errors"))
