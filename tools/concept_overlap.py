# -*- coding: utf-8 -*-
"""concept_overlap.py — 概念重叠检查（skills 审查 EX-01 / EX-10）。

`brain-explain-alphas` 与 Mode B 一直声称「换概念前先查与既有 book 的概念重叠」，但从未有过对应的程序。
本工具把目标表达式与本区 book（`alphas` 表里的 ACTIVE alpha）逐条比对两个维度，给出重叠清单与建议：

  · 信号族 = 表达式引用的**字段集合**（`tools/campaign_intel.py::_pf_family`，prod-first 探针的分组单位）
  · 骨架指纹 = 表达式里**前 2 个算子调用名**（`tools/wave_gate.py::_pf_family`，闸 PF 的判据）

两个定义与全库同源（直接 import，不另写一份），所以这里判「重叠」的口径与闸 PF / prod-first 一致。

等级（**启发式提示，不是平台判定，不能用来否决或放行**；真实相关性只有 `check_self_correlation` /
`check_correlation` 给得出）：
  HIGH    字段集合完全相同，或「同骨架且字段 Jaccard ≥ 0.5」
  MEDIUM  字段 Jaccard ≥ 0.5（骨架不同），或「同骨架且至少共享 1 个字段」
  LOW     只共享部分字段（Jaccard < 0.5，骨架不同）
阈值 0.5 的理由：字段数按 2–3 个的典型表达式算，「共享一半以上字段」是能被一句话概括为「同一个信号」的下限
（2 个字段共享 1 个 = 0.33 → LOW；3 个共享 2 个 = 0.67 → MEDIUM）；`--jaccard` 可调，未做样本外标定。

只读：book 取自 `alphas` 表（或 `--book-json` 给的列表），不写库、不发任何平台请求。

用法:
  $WQ_PY tools/concept_overlap.py --region KOR --alpha-id <ID>
  $WQ_PY tools/concept_overlap.py --region KOR --expr "rank(ts_zscore(<字段>, 66))"
  $WQ_PY tools/concept_overlap.py --region KOR --expr "..." --book-json book.json   # book = [{alpha_id, expression}, ...]

退出码: 0=检查完成（结论看 JSON 的 verdict），2=参数 / 输入错误。
运行环境: MCP venv（$WQ_PY）。
"""
import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _pyenv  # noqa: E402  跨平台解释器/路径解析（tools/_pyenv.py）

_REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if os.path.join(_REPO, "src") not in sys.path:
    sys.path.insert(0, os.path.join(_REPO, "src"))

JACCARD_HIGH = 0.5

_ADVICE = {
    "HIGH": "概念高度重叠：换概念（不同字段集 + 不同骨架）；同字段换骨架只算 1 次结构性尝试（见 RA 决策表 D0-P）。",
    "MEDIUM": "概念部分重叠：可继续，但优先换骨架 / 换字段；提交前必须实测 SELF / PROD 相关性。",
    "LOW": "只共享少量字段：概念基本不同；仍须实测相关性。",
    "CLEAR": "与本区 book 无字段重叠（仍须实测相关性）。",
}


def _families(expr: str):
    from campaign_intel import _pf_family as field_family
    from wave_gate import _pf_family as skeleton_fp
    fam = field_family(expr)
    fields = set() if fam == "?" else set(fam.split("+"))
    return fields, skeleton_fp(expr)


def compare(target_expr: str, book, jaccard_high: float = JACCARD_HIGH, exclude_alpha_id=None):
    """纯函数：目标表达式 vs book（[{alpha_id, expression, ...}]）→ 结果 dict。"""
    t_fields, t_skel = _families(target_expr)
    overlaps = []
    for row in book:
        if exclude_alpha_id and row.get("alpha_id") == exclude_alpha_id:
            continue
        b_fields, b_skel = _families(row.get("expression") or "")
        shared = t_fields & b_fields
        if not shared:
            continue
        union = t_fields | b_fields
        jac = len(shared) / len(union) if union else 0.0
        same_skel = t_skel != "?" and t_skel == b_skel
        if t_fields == b_fields or (same_skel and jac >= jaccard_high):
            level = "HIGH"
        elif jac >= jaccard_high or same_skel:
            level = "MEDIUM"
        else:
            level = "LOW"
        overlaps.append({
            "alpha_id": row.get("alpha_id"), "level": level, "jaccard": round(jac, 3),
            "same_skeleton": same_skel, "shared_fields": sorted(shared), "skeleton": b_skel,
            "prod_correlation": row.get("prod_correlation"),
        })
    rank = {"HIGH": 0, "MEDIUM": 1, "LOW": 2}
    overlaps.sort(key=lambda o: (rank[o["level"]], -o["jaccard"]))
    verdict = overlaps[0]["level"] if overlaps else "CLEAR"
    return {
        "target": {"fields": sorted(t_fields), "skeleton": t_skel},
        "book_size": len(book), "verdict": verdict, "advice": _ADVICE[verdict],
        "jaccard_high": jaccard_high, "overlaps": overlaps,
    }


def load_book_from_db(region: str, statuses=("ACTIVE",), db_path=None):
    """本区 book：`alphas` 表里 status 在 statuses 内的行（只读连接）。库不可读 → 抛 RuntimeError。"""
    from wqb.db_conn import connect
    from wqb.store._common import default_db_path
    marks = ",".join("?" for _ in statuses)
    sql = ("SELECT a.alpha_id, a.expression, a.status, a.prod_correlation FROM alphas a "
           "JOIN regions r ON a.region_id = r.id "
           f"WHERE r.name = ? AND a.status IN ({marks}) AND a.expression IS NOT NULL")
    try:
        conn = connect(db_path or default_db_path(), readonly=True)
        try:
            cur = conn.execute(sql, (region.upper(), *statuses))
            return [dict(zip(("alpha_id", "expression", "status", "prod_correlation"), r)) for r in cur.fetchall()]
        finally:
            conn.close()
    except Exception as e:  # noqa: BLE001
        raise RuntimeError(f"读不到本区 book（alphas 表）：{e}") from e


def _lookup_expression(alpha_id: str, db_path=None):
    from wqb.db_conn import connect
    from wqb.store._common import default_db_path
    try:
        conn = connect(db_path or default_db_path(), readonly=True)
        try:
            row = conn.execute("SELECT expression FROM alphas WHERE alpha_id = ?", (alpha_id,)).fetchone()
        finally:
            conn.close()
    except Exception:  # noqa: BLE001
        row = None
    return row[0] if row and row[0] else None


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="概念重叠检查：目标表达式 vs 本区 ACTIVE book（只读、启发式）")
    ap.add_argument("--region", required=True)
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--alpha-id", help="目标 alpha（须已在 alphas 表；否则改用 --expr）")
    g.add_argument("--expr", help="目标表达式（尚未入库的想法）")
    ap.add_argument("--book-json", help="book 改用文件：[{alpha_id, expression, ...}]（如 get_user_alphas 的 ACTIVE 导出）")
    ap.add_argument("--status", action="append", help="book 的状态过滤（可重复；缺省 ACTIVE）")
    ap.add_argument("--jaccard", type=float, default=JACCARD_HIGH, help=f"字段 Jaccard 阈值（缺省 {JACCARD_HIGH}）")
    a = ap.parse_args(argv)

    expr = a.expr or _lookup_expression(a.alpha_id)
    if not expr:
        print(f"找不到 alpha {a.alpha_id} 的表达式（不在 alphas 表）：请改用 --expr", file=sys.stderr)
        return 2
    if a.book_json:
        with open(a.book_json, encoding="utf-8") as f:
            book = json.load(f)
        if not isinstance(book, list):
            print("--book-json 必须是 [{alpha_id, expression}, ...] 列表", file=sys.stderr)
            return 2
    else:
        try:
            book = load_book_from_db(a.region, tuple(a.status or ("ACTIVE",)))
        except RuntimeError as e:
            print(str(e), file=sys.stderr)
            return 2
    out = compare(expr, book, jaccard_high=a.jaccard, exclude_alpha_id=a.alpha_id)
    out["region"] = a.region.upper()
    out["target"]["alpha_id"] = a.alpha_id
    print(json.dumps(out, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    _pyenv.reexec_under_venv()
    sys.exit(main())
