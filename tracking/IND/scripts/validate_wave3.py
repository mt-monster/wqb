"""wave3 语法校验 (ml_factor_proj)"""
import sys, json
sys.path.insert(0, r"D:\coding\traeCN_project\wqb\.cursor\skills\alpha-expression-verifier\scripts")
from validator import ExpressionValidator

v = ExpressionValidator()
plan = json.load(open(r"D:\coding\traeCN_project\wqb\tracking\KOR\candidates\kor_wave3_plan.json", encoding="utf-8"))
exprs = plan["batch1_exprs"] + plan["batch2_exprs"] + plan["batch3_exprs"]
bad = []
for e in exprs:
    r = v.check_expression(e)
    ok = r.get("valid") if isinstance(r, dict) else bool(r)
    if not ok:
        bad.append((e, r))
print(f"total={len(exprs)} invalid={len(bad)}")
for e, r in bad:
    print("BAD:", e, r)
