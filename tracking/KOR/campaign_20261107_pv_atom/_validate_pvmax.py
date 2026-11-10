import sys,json; sys.path.insert(0,'src')
from wqb.expression.op_arity import check_expressions
d=json.load(open(sys.argv[1],encoding='utf-8'))
for name in ['MAX','ONG']:
    print('====',name)
    res=check_expressions(d[name])
    print(json.dumps(res,ensure_ascii=False)[:1500])
