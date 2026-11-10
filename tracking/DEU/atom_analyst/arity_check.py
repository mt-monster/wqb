import json, sys
sys.path.insert(0, "src")
from wqb.expression.op_arity import ensure_safe_for_dispatch
exprs = json.load(open("tracking/DEU/atom_analyst/wave2_exprs.json", encoding="utf-8"))
res = {"C": ensure_safe_for_dispatch(exprs["C"]), "D": ensure_safe_for_dispatch(exprs["D"])}
print(json.dumps(res, ensure_ascii=False, default=str))
