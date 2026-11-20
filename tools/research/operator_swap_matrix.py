#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""operator_swap_matrix.py — 同类别算子全替换矩阵生成器（按需工具，用户 2026-11-20 裁定）。

来源规则
--------
用户 2026-11-20：「在回测的 alpha 表达式上，每加一个新的算子，就要把同类型的算子
都要替换一遍回测，看是否对指标值有改善」。裁定为**按需工具**（非默认硬闸），
替换范围 = **同 category 全替 + no-op 去重**。

做什么
------
输入一条基线表达式 + 要替换的算子名，从平台算子 catalog（MCP `get_operators`
刷出的 ``docs/reference/operators_catalog.json``）取该算子的 category，
把同 category 里**参数形状兼容**的算子逐一换入，其他部分逐字冻结，
生成可直接喂 ``create_multi_simulation`` 的表达式列表。

no-op 去重（docs/experience/02_signal_patterns.md §17）
------------------------------------------------------
1. **rank 壳内聚合互换**：`rank(ts_sum(F,d))` / `rank(ts_mean(F,d))` /
   `rank(ts_av_diff(F,d))` 逐位相同 —— 若替换算子位于 rank/group_rank 壳内且
   候选是 ts_sum/ts_mean/ts_av_diff 同窗口，跳过。
2. **恒等包装**：`rank(rank(x))`、`winsorize(rank(x))`、`group_neutralize(group_neutralize(...))` 不生成。
3. **arity 不兼容**：只换单参数白名单算子；ts_corr(x,y,d)、group_rank(x,group) 这类
   多参算子不做单参替换（group 类第二参是分组轴，保留原参数不改）。
4. **scope 过滤**：只取 scope 含 REGULAR 的算子。

用法
----
::

    # 1) 先确保 catalog 是最新的（Agent 调 get_operators 存 raw，再刷）
    python tools/refresh_operator_catalog.py raw_get_operators.json

    # 2) 生成替换矩阵
    python tools/operator_swap_matrix.py \
        --expr "group_rank(ts_zscore(ts_backfill(F,60),250),industry)" \
        --op ts_zscore --out logs/_tmp_swap.json

    # 3) 看某算子的可替换候选（不生成）
    python tools/operator_swap_matrix.py --list ts_zscore

输出 JSON 形态::

    {"baseline": "...", "op": "ts_zscore", "category": "Time Series",
     "replacements": [{"op": "ts_rank", "expression": "...", "note": ""}, ...],
     "skipped": [{"op": "...", "reason": "no-op: rank壳内聚合互换"}]}

注意
----
- 不直接派发回测（用户硬约束：派发只用 MCP create_multi_simulation）。
- 不判断哪个算子"更好"——只生成候选；好坏由回测指标 Δ 表回答。
- 替换后的表达式必须过 ``mcp__wq-brain-http__preflight_expressions`` 才发。
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CATALOG = os.path.join(ROOT, "docs", "reference", "operators_catalog.json")

# rank 壳内的聚合互换是 no-op（§17.1）
NOOP_AGG_OPS = {"ts_sum", "ts_mean", "ts_av_diff"}

# 单输入算子白名单（从平台 103 算子清单人工核对）
# 按「调用形态」分组——替换必须保持调用形状，否则 arity/命名参数不兼容。
# 窗口类：op(x, d)  —— 第二位置参数是窗口，可直接换入保留原 d
WINDOW_1D = {
    "ts_zscore", "ts_rank", "ts_quantile", "ts_mean", "ts_sum", "ts_delta",
    "ts_std_dev", "ts_av_diff", "ts_scale", "ts_ir", "ts_kurtosis", "ts_arg_max",
    "ts_arg_min", "ts_max_diff", "ts_returns", "ts_product", "ts_decay_linear",
}
# 无窗类：op(x) —— 只吃一个参数，与窗口类不可互换（替换时会多一个位置参数）
NO_WINDOW = {"days_from_last_change", "ts_step", "reverse", "abs", "sign", "log",
             "sqrt", "inverse", "pasteurize", "densify", "winsorize", "zscore",
             "normalize", "quantile", "rank"}
# 命名参类：op(x, name=const) —— 第二参不是位置窗口，不可直接套 d
NAMED_2ND = {"hump", "ts_target_tvr_decay", "ts_target_tvr_hump"}
SINGLE_INPUT_TIME_SERIES = WINDOW_1D | {"days_from_last_change", "ts_step"} | NAMED_2ND
SINGLE_INPUT_CROSS_SECTIONAL = {
    "rank", "zscore", "winsorize", "normalize", "quantile", "scale", "vector_neut",
}
SINGLE_INPUT_GROUP = {
    "group_rank", "group_zscore", "group_neutralize", "group_scale", "group_mean",
    "group_std_dev", "group_sum", "group_count", "group_backfill",
}
SINGLE_INPUT_TRANSFORMATIONAL = {"tail", "trade_when", "bucket"}
SINGLE_INPUT_ARITHMETIC = {
    "sign", "abs", "log", "sqrt", "inverse", "reverse", "pasteurize", "densify",
}
SINGLE_INPUT_VECTOR = {
    "vec_avg", "vec_sum", "vec_max", "vec_min", "vec_stddev", "vec_range", "vec_count",
}
CATEGORY_SINGLE_INPUT = {
    "Time Series": SINGLE_INPUT_TIME_SERIES,
    "Cross Sectional": SINGLE_INPUT_CROSS_SECTIONAL,
    "Group": SINGLE_INPUT_GROUP,
    "Transformational": SINGLE_INPUT_TRANSFORMATIONAL,
    "Arithmetic": SINGLE_INPUT_ARITHMETIC,
    "Vector": SINGLE_INPUT_VECTOR,
}
IDENTITY_PATTERNS = (
    re.compile(r"rank\(\s*rank\("),
    re.compile(r"winsorize\(\s*rank\("),
    re.compile(r"group_neutralize\(\s*group_neutralize\("),
)
# 等价实现族：与 ts_rank/ts_zscore 同属「时序相对化」，替换保机制（§51 实测四者相关≈1）
EQUIV_TIME = {"ts_rank", "ts_zscore", "ts_quantile", "ts_av_diff"}
# 语义变更族：合法替换但换了信号机制（分布变换/聚合/事件时点），Δ读数要按「新机制」解释，
# 不能当「实现优化」——这类替换往往是真正的破闸杠杆（§12 GBR news50 的 ts_decay_linear）。
SEMANTIC_CHANGE_NOTE = "语义变更族：替换后信号机制改变（非等价实现），Δ读数按新机制解释"


def _load_catalog():
    with open(CATALOG, encoding="utf-8") as f:
        data = json.load(f)
    ops = data.get("results", data.get("operators", data)) if isinstance(data, dict) else data
    return {op["name"]: op for op in ops}


def _category(cat, op):
    return cat.get(op, {}).get("category", "unknown")


def _regular_scope(cat, op):
    return "REGULAR" in (cat.get(op, {}).get("scope") or [])


def _arity(cat, op):
    """从平台 catalog 的 definition 提取位置参数个数（忽略带默认值的参）。

    definition 形如 ``group_rank(x, group)`` / ``group_backfill(x, group, d, std = 4.0)`` /
    ``group_mean(x, weight, group)``。返参：必填位置参数个数。
    - 带 ``=`` 的参数（如 ``std = 4.0``）是可选参，不计入 arity；
    - 取不到 definition 时回 None（调用方按「不校验」处理，保持旧行为）。
    """
    definition = (cat.get(op, {}).get("definition") or "").strip()
    m = re.search(r"\((.*)\)", definition)
    if not m:
        return None
    inner = m.group(1).strip()
    if not inner:
        return 0
    required = [p for p in inner.split(",") if "=" not in p]
    return len(required)


def _in_rank_shell(expr, op_start):
    prefix = expr[:op_start]
    m = list(re.finditer(r"([a-zA-Z_][a-zA-Z0-9_]*)\(", prefix))
    return bool(m) and m[-1].group(1) in ("rank", "group_rank")


def _op_occurrences(expr, op):
    """返回该算子名在表达式中的所有出现位置（按左到右）。"""
    return [m.start() for m in re.finditer(r"\b" + re.escape(op) + r"\s*\(", expr)]


def _replace_op(expr, op, repl, nth=None):
    """替换算子名。

    nth=None（默认）：替换**全部**出现（保持历史行为）。
    nth=N（1-based）：只替换第 N 处出现 —— **逐层替换必须用它**，
    否则同名算子的多层（如 `group_rank(x, group_rank(y))`）会被一起改掉，
    生成的矩阵不再是「单层对照」。
    """
    pat = re.compile(r"\b" + re.escape(op) + r"\s*\(")
    if nth is None:
        return pat.sub(repl + "(", expr)
    if nth < 1:
        raise ValueError("nth 必须 ≥ 1（1-based）")
    count = 0
    out = []
    pos = 0
    for m in pat.finditer(expr):
        count += 1
        out.append(expr[pos:m.start()])
        out.append(repl + "(" if count == nth else m.group(0))
        pos = m.end()
    out.append(expr[pos:])
    return "".join(out)


def _noop_reason(expr, op, repl, nth=None, cat=None):
    if repl == op:
        return "same as baseline"
    # 平台 definition 的必填参数个数必须一致（2026-11-20 实测：group_mean(x,weight,group)
    # 与 group_backfill(x,group,d,std=4) 都需 ≥3 参，当 2 参 group 算子替换会生成
    # 不可派发表达式，被 toolkit 静态门禁拒绝）——这是 arity 白名单之外的硬校验。
    if cat is not None:
        arity_op, arity_repl = _arity(cat, op), _arity(cat, repl)
        if arity_op is not None and arity_repl is not None and arity_op != arity_repl:
            return f"arity: {op} 需 {arity_op} 参，{repl} 需 {arity_repl} 参（平台 definition）"
    # 调用形状必须一致：窗口类 ↔ 无窗类 ↔ 命名参类 不可直接互换
    if op in WINDOW_1D and repl not in WINDOW_1D:
        return f"arity: {op} 是窗口类 op(x,d)，{repl} 不接受位置窗口参数"
    if op in NO_WINDOW and repl not in NO_WINDOW:
        return f"arity: {op} 是无窗类 op(x)，{repl} 需要额外参数"
    if op in NAMED_2ND and repl not in NAMED_2ND:
        return f"arity: {op} 第二参是命名参数，{repl} 不适用"
    if op in NOOP_AGG_OPS and repl in NOOP_AGG_OPS:
        m = re.search(r"\b" + re.escape(op) + r"\s*\(", expr)
        if m and _in_rank_shell(expr, m.start()):
            return "no-op: rank壳内聚合互换（§17.1）"
    if any(p.search(expr) for p in IDENTITY_PATTERNS):
        return "identity pattern already present"
    return None


def build_matrix(expr, op, cat, nth=None):
    category = _category(cat, op)
    if category == "unknown":
        raise SystemExit(f"算子 {op} 不在平台 catalog（{CATALOG}）；先跑 refresh_operator_catalog.py")
    family = CATEGORY_SINGLE_INPUT.get(category, set())
    if op not in family:
        raise SystemExit(f"算子 {op}（{category}）不在本工具的单参数白名单；多参算子需人工处理")
    n_occ = len(_op_occurrences(expr, op))
    if nth is not None and nth > n_occ:
        raise SystemExit(f"算子 {op} 在表达式中只出现 {n_occ} 次，--nth {nth} 越界")
    candidates = sorted(x for x in family if _regular_scope(cat, x))
    replacements, skipped = [], []
    for repl in candidates:
        reason = _noop_reason(expr, op, repl, nth, cat)
        if reason:
            skipped.append({"op": repl, "reason": reason})
            continue
        note = ""
        if op in EQUIV_TIME and repl in EQUIV_TIME:
            note = "等价实现族：时序相对化，相关≈1（§51），Δ主要来自数值路径"
        elif repl not in cat:
            note = "算子不在 catalog（仅白名单）"
        else:
            note = SEMANTIC_CHANGE_NOTE
        replacements.append({
            "op": repl,
            "expression": _replace_op(expr, op, repl, nth),
            "note": note,
        })
    return {
        "baseline": expr,
        "op": op,
        "category": category,
        "nth": nth,
        "n_occurrences": n_occ,
        "n_replacements": len(replacements),
        "n_skipped_noop": len(skipped),
        "replacements": replacements,
        "skipped": skipped,
        "note": ("替换后必须过 preflight_expressions 才可用 create_multi_simulation 派发"
                 + ("" if nth else "；表达式中该算子出现多次时用 --nth N 只换第 N 处（逐层替换）")),
    }


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--expr", help="基线表达式")
    ap.add_argument("--op", help="要替换的算子名（如 ts_zscore）")
    ap.add_argument("--out", help="输出 JSON 路径（缺省打到 stdout）")
    ap.add_argument("--list", metavar="OP", help="只列出该算子的 category 与可替换候选")
    ap.add_argument("--nth", type=int, default=None,
                    help="只替换同名算子的第 N 处出现（1-based）——逐层替换必须用它，"
                         "否则同名多层会被一起替换，矩阵不再是单层对照")
    args = ap.parse_args(argv)

    cat = _load_catalog()
    if args.list:
        op = args.list
        category = _category(cat, op)
        family = CATEGORY_SINGLE_INPUT.get(category, set())
        print(f"{op}: category={category}")
        print("可替换候选（REGULAR scope）:")
        for x in sorted(y for y in family if _regular_scope(cat, y)):
            print(f"  {x}" + ("  [baseline]" if x == op else ""))
        return 0
    if not args.expr or not args.op:
        ap.error("需要 --expr 和 --op（或用 --list）")
    result = build_matrix(args.expr, args.op, cat, args.nth)
    if result["n_occurrences"] > 1 and args.nth is None:
        print(f"[warn] 算子 {args.op} 在表达式中出现 {result['n_occurrences']} 次，"
              f"本次替换了全部出现；逐层对照请加 --nth N。", file=sys.stderr)
    text = json.dumps(result, ensure_ascii=False, indent=2)
    if args.out:
        with open(args.out, "w", encoding="utf-8") as f:
            f.write(text + "\n")
        print(f"[operator-swap] {result['n_replacements']} replacements / "
              f"{result['n_skipped_noop']} no-op skipped -> {args.out}")
    else:
        print(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
