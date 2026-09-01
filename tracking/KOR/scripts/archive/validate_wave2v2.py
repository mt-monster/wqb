"""wave2v2 语法校验"""
import sys, json
sys.path.insert(0, r"D:\coding\traeCN_project\wqb\.cursor\skills\alpha-expression-verifier\scripts")
from validator import ExpressionValidator

v = ExpressionValidator()
exprs = json.load(open(r"D:\coding\traeCN_project\wqb\tracking\KOR\candidates\kor_wave2v2_exprs.json", encoding="utf-8"))
bad = []
for e in exprs:
    r = v.check_expression(e)
    ok = r.get("valid") if isinstance(r, dict) else bool(r)
    if not ok:
        bad.append((e, r))
print(f"total={len(exprs)} invalid={len(bad)}")
for e, r in bad:
    print("BAD:", e, r)
