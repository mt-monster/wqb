#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""算子审计：统计 alpha 表达式的算子调用点数、逐算子计数、可压缩改写点。

用法：
    python op_count.py --expr "winsorize(group_rank(...), std=4)"
    python op_count.py --file exprs.txt                 # 每行一个表达式
    python op_count.py --alpha-id zqbVMkv1              # 从平台取 code（需 brain_api 可导入）
    python op_count.py --expr "..." --json              # 机器可读

只读、零副作用；不提交任何东西。
"""
from __future__ import annotations

import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from wqexpr import ParseError, compress_report, op_count  # noqa: E402


def fetch_code(alpha_id: str) -> str:
    """从平台取 alpha 的真实表达式（合规只看 get_alpha_details().code）。"""
    candidates = [
        os.path.join(os.getcwd(), "world-quant-brain-mcp"),
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "..",
                     "coding", "traeCN_project", "wqb", "world-quant-brain-mcp"),
    ]
    for p in candidates:
        if os.path.isdir(p):
            sys.path.insert(0, os.path.abspath(p))
            break
    try:
        import asyncio

        from brain_api import BrainApiClient  # type: ignore
    except Exception as exc:  # pragma: no cover
        raise SystemExit(
            f"[op_count] 无法导入 brain_api（{exc}）。请改用 --expr / --file。"
        ) from exc

    async def _run() -> str:
        b = BrainApiClient()
        await b.ensure_authenticated()
        a = (await b._request("GET", "/alphas/" + alpha_id)).json()
        return ((a.get("regular") or {}).get("code") or "")

    return asyncio.run(_run())


def report_one(expr: str, as_json: bool) -> dict:
    try:
        rep = compress_report(expr)
    except ParseError as exc:
        rep = {"expr": expr, "error": str(exc), "op_count": op_count(expr),
               "per_op": {}, "fields": [], "rewrites": []}
    if as_json:
        return rep
    print("=" * 72)
    print(f"表达式: {rep['expr'][:200]}")
    if rep.get("error"):
        print(f"  ⚠ 解析失败: {rep['error']}（算子计数仍按正则给出）")
    print(f"  算子调用点数: {rep['op_count']}")
    if rep["per_op"]:
        print("  逐算子计数: " + ", ".join(f"{k}×{v}" for k, v in rep["per_op"].items()))
    if rep["fields"]:
        print("  字段/轴: " + ", ".join(rep["fields"][:12]))
    if rep["rewrites"]:
        print("  ── 可压缩改写点（无损优先）──")
        for r in rep["rewrites"]:
            tag = "无损" if r["lossless"] else "有损(需重测)"
            print(f"    [{r['rule']}] {tag}  省 {r['op_saved']} 算子")
            print(f"        before: {r['where'][:110]}")
            print(f"        after : {r['after'][:110]}")
            if r["note"]:
                print(f"        说明  : {r['note']}")
    else:
        print("  ── 未发现自动可压缩点（仍需人工逐算子消融）──")
    return rep


def main() -> None:
    ap = argparse.ArgumentParser(description="WQ alpha 算子审计（只读）")
    src = ap.add_mutually_exclusive_group(required=True)
    src.add_argument("--expr", help="表达式字符串")
    src.add_argument("--file", help="每行一个表达式的文件")
    src.add_argument("--alpha-id", help="平台 alpha id（自动取 code）")
    ap.add_argument("--json", action="store_true", help="输出 JSON")
    args = ap.parse_args()

    exprs: list[str] = []
    if args.expr:
        exprs = [args.expr]
    elif args.file:
        with open(args.file, encoding="utf-8") as fh:
            exprs = [ln.strip() for ln in fh if ln.strip() and not ln.startswith("#")]
    else:
        code = fetch_code(args.alpha_id)
        if not code:
            raise SystemExit(f"[op_count] alpha {args.alpha_id} 没有 code")
        exprs = [code]

    reps = [report_one(e, args.json) for e in exprs]
    if args.json:
        print(json.dumps(reps if len(reps) > 1 else reps[0], ensure_ascii=False, indent=1))
    else:
        total = sum(r["op_count"] for r in reps)
        print("-" * 72)
        print(f"合计 {len(reps)} 条表达式，算子调用点总数 {total}")


if __name__ == "__main__":
    main()
