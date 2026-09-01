"""Batch syntax validation for generated alpha expressions (KOR pattern_scores campaign).

已迁移到数据库：从 ideas.db 读取表达式，而非 JSON 文件.
"""
import json
import sys
from pathlib import Path

# 添加 src 到路径
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / "src"))

from wqb.memory.idea_store import IdeaStore

sys.path.insert(0, r"D:\coding\traeCN_project\wqb\.cursor\skills\alpha-expression-verifier\scripts")
from validator import ExpressionValidator

# 从数据库读取表达式
store = IdeaStore()
idea_id = "pattern_scores_KOR_1_idea"  # 根据实际 idea id 调整
idea = store.get_idea(idea_id)
if idea is None:
    # 回退到 JSON 文件（兼容旧流程）
    SRC = r"D:\coding\traeCN_project\wqb\.cursor\skills\brain-makeSomeGem\scripts\trailSomeAlphas\skills\brain-feature-implementation\data\pattern_scores_KOR_delay1\final_expressions.json"
    exprs = json.load(open(SRC, encoding="utf-8"))
    print(f"[WARN] 数据库中未找到 idea '{idea_id}'，回退到 JSON 文件: {SRC}")
else:
    exprs = idea.get("expression_list", [])
    print(f"[OK] 从数据库加载 idea '{idea_id}': {len(exprs)} 个表达式")

store.close()

OUT = r"D:\coding\traeCN_project\wqb\tracking\KOR\candidates\kor_pattern_scores_valid_exprs.json"

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
