"""Batch syntax validation for generated alpha expressions (KOR pattern_scores campaign)."""
import json
import sys

sys.path.insert(0, r"D:\coding\traeCN_project\wqb\.cursor\skills\alpha-expression-verifier\scripts")
from validator import ExpressionValidator

SRC = r"D:\coding\traeCN_project\wqb\.cursor\skills\brain-makeSomeGem\scripts\trailSomeAlphas\skills\brain-feature-implementation\data\pattern_scores_KOR_delay1\final_expressions.json"
OUT = r"D:\coding\traeCN_project\wqb\tracking\KOR\candidates\kor_pattern_scores_valid_exprs.json"

exprs = json.load(open(SRC, encoding="utf-8"))
validator = ExpressionValidator()
valid, invalid = [], []
for e in exprs:
    try:
        r = validator.check_expression(e)
        if r.get("valid"):
            valid.append(e)
        else:
            invalid.append({"expr": e, "errors": r.get("errors")})
    except Exception as exc:
        invalid.append({"expr": e, "errors": [str(exc)]})

json.dump(valid, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(f"total={len(exprs)} valid={len(valid)} invalid={len(invalid)}")
for item in invalid[:10]:
    print("INVALID:", item["expr"], "->", item["errors"])
