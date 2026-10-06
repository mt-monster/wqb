# -*- coding: utf-8 -*-
"""全量扫描项目内 Python 文件：行数 / 函数类规模 / 圈复杂度 / 职责数量。

输出 JSON + 控制台摘要，供「体量过大 / 职责混杂」分析。只读，不改任何文件。
"""
from __future__ import annotations

import ast
import json
import os
import sys

EXCLUDE_DIRS = {"__pycache__", ".venv", "venv", ".git", "node_modules", "attic",
                "site-packages", ".pytest_cache", "world-quant-brain-mcp/.venv"}


def _excluded(path: str) -> bool:
    parts = set(path.replace("\\", "/").split("/"))
    if "world-quant-brain-mcp" in parts and ".venv" in parts:
        return True
    return bool(parts & EXCLUDE_DIRS) or "/.venv/" in path.replace("\\", "/")


def cyclomatic_complexity(node: ast.AST) -> int:
    """简易圈复杂度：decision points + 1。"""
    cc = 1
    for child in ast.walk(node):
        if isinstance(child, (ast.If, ast.For, ast.AsyncFor, ast.While,
                              ast.ExceptHandler, ast.With, ast.Assert)):
            cc += 1
        elif isinstance(child, ast.BoolOp):
            cc += len(child.values) - 1
        elif isinstance(child, ast.IfExp):
            cc += 1
        elif isinstance(child, ast.comprehension):
            cc += len(child.ifs) + 1
        elif isinstance(child, (ast.And, ast.Or)):
            cc += 1
    return cc


def analyze_file(path: str):
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as f:
            src = f.read()
    except Exception as e:
        return {"path": path, "error": str(e)}
    lines = src.splitlines()
    n_lines = len(lines)
    try:
        tree = ast.parse(src, filename=path)
    except SyntaxError as e:
        return {"path": path, "lines": n_lines, "error": f"SyntaxError: {e}"}

    funcs = []   # (name, lines, cc, is_method, class_name)
    classes = []  # (name, lines, n_methods)
    imports = set()

    def span(nd):
        start = getattr(nd, "lineno", 0)
        end = getattr(nd, "end_lineno", start)
        return max(1, end - start + 1)

    for nd in ast.walk(tree):
        if isinstance(nd, (ast.Import, ast.ImportFrom)):
            if isinstance(nd, ast.ImportFrom) and nd.module:
                imports.add(nd.module.split(".")[0])
            else:
                for a in nd.names:
                    imports.add(a.name.split(".")[0])
        elif isinstance(nd, ast.ClassDef):
            methods = [c for c in nd.body if isinstance(c, (ast.FunctionDef, ast.AsyncFunctionDef))]
            classes.append({
                "name": nd.name, "lines": span(nd), "n_methods": len(methods),
            })
        elif isinstance(nd, (ast.FunctionDef, ast.AsyncFunctionDef)):
            funcs.append({
                "name": nd.name, "lines": span(nd), "cc": cyclomatic_complexity(nd),
                "async": isinstance(nd, ast.AsyncFunctionDef),
            })

    # 模块级圈复杂度（顶层语句）
    top_cc = 0
    top_level = [n for n in tree.body if not isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef))]
    for n in top_level:
        top_cc += cyclomatic_complexity(n) - 1

    funcs.sort(key=lambda x: -x["lines"])
    classes.sort(key=lambda x: -x["lines"])
    max_cc = max([f["cc"] for f in funcs], default=0)
    biggest = funcs[0] if funcs else None

    return {
        "path": path,
        "lines": n_lines,
        "n_funcs": len(funcs),
        "n_classes": len(classes),
        "n_imports": len(imports),
        "max_func": biggest,
        "max_class": classes[0] if classes else None,
        "max_cc": max_cc,
        "top_funcs": funcs[:5],
        "top_classes": classes[:3],
        "top_level_cc": top_cc,
        # 启发式「职责数量」：顶层函数 + 类 + 模块级逻辑复杂度簇
        "responsibility_score": len(classes) + len([f for f in funcs]) + top_cc // 3,
    }


def main():
    root = sys.argv[1] if len(sys.argv) > 1 else "."
    out_json = sys.argv[2] if len(sys.argv) > 2 else "logs/file_audit.json"
    files = []
    for dirpath, dirnames, filenames in os.walk(root):
        # 原地剪枝
        dirnames[:] = [d for d in dirnames if d not in EXCLUDE_DIRS and not d.endswith(".egg-info")]
        for fn in filenames:
            if fn.endswith(".py"):
                p = os.path.join(dirpath, fn)
                if not _excluded(p):
                    files.append(p)
    rows = []
    for p in files:
        rows.append(analyze_file(p))
    rows = [r for r in rows if "error" not in r or "lines" in r]
    rows.sort(key=lambda r: -(r.get("lines", 0)))

    os.makedirs(os.path.dirname(out_json), exist_ok=True)
    with open(out_json, "w", encoding="utf-8") as f:
        json.dump(rows, f, ensure_ascii=False, indent=2)

    print(f"scanned {len(rows)} files -> {out_json}")
    print("\n=== Top 25 by lines ===")
    print(f"{'lines':>6} {'func':>4} {'cls':>4} {'maxF':>5} {'maxCC':>5}  path")
    for r in rows[:25]:
        mf = r["max_func"]["lines"] if r.get("max_func") else 0
        print(f"{r['lines']:>6} {r['n_funcs']:>4} {r['n_classes']:>4} {mf:>5} {r['max_cc']:>5}  {r['path']}")

    print("\n=== Top 15 by max single function lines ===")
    bymf = sorted(rows, key=lambda r: -(r["max_func"]["lines"] if r.get("max_func") else 0))
    for r in bymf[:15]:
        mf = r.get("max_func")
        if not mf:
            continue
        print(f"{mf['lines']:>5} (cc {mf['cc']:>3}) {mf['name']:<40}  {r['path']}")

    print("\n=== Top 15 by max cyclomatic complexity ===")
    bycc = sorted(rows, key=lambda r: -r["max_cc"])
    for r in bycc[:15]:
        mf = r.get("max_func") or {}
        print(f"cc {r['max_cc']:>4}  {mf.get('name',''):<40} {r['path']}")


if __name__ == "__main__":
    main()
