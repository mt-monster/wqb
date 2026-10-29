#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""算子压缩：给出「一次只改一个点」的消融候选 + 「全部无损改写」合并候选。

用法：
    python compress.py --expr "<表达式>"                 # 列出消融候选
    python compress.py --expr "..." --out cands.txt      # 写出候选（每行一个，可直接喂 submit_batch）
    python compress.py --expr "..." --lossless-only      # 只列无损改写
    python compress.py --expr "..." --apply-lossless     # 输出「全部无损改写合并」后的表达式
    python compress.py --file exprs.txt --json

纪律（见 references/op-compression.md）：先无损、再有损；有损必须逐个消融并回测，一次只改一个点。
本脚本只**生成候选表达式**，不做仿真、不提交。
"""
from __future__ import annotations

import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from wqexpr import ParseError, find_rewrites, op_count, parse  # noqa: E402


def canonical(expr: str) -> str:
    return parse(expr).to_str()


def apply_rewrite(expr: str, where: str, after: str) -> str:
    """在规范化表达式上替换子表达式（全部出现处）。"""
    return canonical(expr).replace(where, after)


def apply_all_lossless(expr: str, max_rounds: int = 8) -> str:
    cur = canonical(expr)
    for _ in range(max_rounds):
        node = parse(cur)
        rules = [r for r in find_rewrites(node) if r["lossless"]]
        if not rules:
            break
        # 取省算子最多的先改
        r = max(rules, key=lambda x: x["op_saved"])
        nxt = cur.replace(r["where"], r["after"])
        if nxt == cur:
            break
        cur = nxt
    return cur


def build_variants(expr: str, lossless_only: bool) -> list[dict]:
    canon = canonical(expr)
    node = parse(canon)
    base_ops = op_count(canon)
    out: list[dict] = []
    for r in find_rewrites(node):
        if lossless_only and not r["lossless"]:
            continue
        new_expr = canon.replace(r["where"], r["after"])
        if new_expr == canon:
            continue
        out.append(
            {
                "rule": r["rule"],
                "lossless": r["lossless"],
                "op_before": base_ops,
                "op_after": op_count(new_expr),
                "op_saved": r["op_saved"],
                "expr": new_expr,
                "note": r["note"],
            }
        )
    out.sort(key=lambda d: (not d["lossless"], -d["op_saved"], d["expr"]))
    return out


def main() -> None:
    ap = argparse.ArgumentParser(description="WQ alpha 算子压缩候选生成（只读）")
    src = ap.add_mutually_exclusive_group(required=True)
    src.add_argument("--expr")
    src.add_argument("--file")
    ap.add_argument("--out", help="把候选表达式写到文件（每行一个）")
    ap.add_argument("--lossless-only", action="store_true", help="只列无损改写")
    ap.add_argument("--apply-lossless", action="store_true",
                    help="直接输出「全部无损改写合并」后的表达式")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    exprs = [args.expr] if args.expr else [
        ln.strip() for ln in open(args.file, encoding="utf-8")
        if ln.strip() and not ln.startswith("#")
    ]

    results, out_lines = [], []
    for e in exprs:
        try:
            canon = canonical(e)
        except ParseError as exc:
            print(f"[compress] 跳过无法解析的表达式: {exc}", file=sys.stderr)
            continue

        if args.apply_lossless:
            merged = apply_all_lossless(e)
            print(merged)
            out_lines.append(merged)
            results.append({"expr": e, "merged_lossless": merged,
                            "op_before": op_count(canon), "op_after": op_count(merged)})
            continue

        vs = build_variants(e, args.lossless_only)
        results.append({"expr": canon, "op_count": op_count(canon), "variants": vs})
        out_lines += [v["expr"] for v in vs]

        if not args.json:
            print("=" * 72)
            print(f"原始（{op_count(canon)} 算子）: {canon[:200]}")
            if not vs:
                print("  （无可自动改写点，请人工逐算子消融）")
            for v in vs:
                tag = "无损" if v["lossless"] else "有损(需重测)"
                print(f"  [{v['rule']}] {tag}  {v['op_before']}→{v['op_after']} 算子  (-{v['op_saved']})")
                print(f"     {v['expr'][:200]}")
                if v["note"]:
                    print(f"     说明: {v['note']}")

    if args.out and out_lines:
        with open(args.out, "w", encoding="utf-8") as fh:
            fh.write("\n".join(out_lines) + "\n")
        print(f"\n[compress] 已写出 {len(out_lines)} 条候选 -> {args.out}")

    if args.json:
        print(json.dumps(results if len(results) > 1 else results[0], ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
