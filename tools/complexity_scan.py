# -*- coding: utf-8 -*-
"""全项目 Python 文件复杂度 / 职责度量（只读、零副作用）。

输出 JSON + 终端 Top-N，用于「哪些文件该拆」的排序依据。

度量项：
  loc        总行数
  sloc       非空非注释行
  n_func     顶层函数数
  n_class    顶层类数
  max_func   最长函数（行数 / 圈复杂度）
  max_class  最长类（行数 / 方法数 / 公开方法数）
  max_cc     全文件最高圈复杂度
  hot_cc     圈复杂度 >= 10 的函数个数（McCabe 经验阈值）
  long_func  行数 > 80 的函数个数
  god_class  方法数 >= 15 或行数 > 400 的类
  imports    顶层 import 语句数（依赖面宽度，职责混杂的侧面证据）
"""
from __future__ import annotations

import ast
import json
import os
import sys
from typing import Any, Dict, List

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SKIP_DIRS = {
    ".git", "__pycache__", ".venv", "venv", "node_modules",
    ".pytest_cache", ".mypy_cache", "site-packages",
}
#: 第三方 /  vendored / 归档：不参与「该拆」排序，但仍统计
VENDOR_HINTS = ("world-quant-brain-mcp/.venv", "site-packages", "attic/", "cache/backup")


def iter_py(root: str):
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for fn in filenames:
            if fn.endswith(".py"):
                yield os.path.join(dirpath, fn)


# ---------------------------------------------------------------- 圈复杂度
_CC_NODES = (
    ast.If, ast.For, ast.AsyncFor, ast.While, ast.ExceptHandler,
    ast.With, ast.AsyncWith, ast.Assert, ast.IfExp,
    ast.comprehension,
)


def _cc(node: ast.AST) -> int:
    """McCabe 圈复杂度（简化版）：决策点 + 1。"""
    score = 1
    for child in ast.walk(node):
        if isinstance(child, _CC_NODES):
            score += 1
        elif isinstance(child, ast.BoolOp):
            score += len(child.values) - 1
        elif isinstance(child, ast.Try):
            score += len(child.handlers)
        elif isinstance(child, ast.Match):
            score += len(child.cases)
    return score


def _seg(node: ast.AST) -> int:
    return (node.end_lineno or node.lineno) - node.lineno + 1


def analyze(path: str) -> Dict[str, Any]:
    try:
        src = open(path, encoding="utf-8", errors="replace").read()
        tree = ast.parse(src, filename=path)
    except (SyntaxError, ValueError, UnicodeDecodeError) as e:
        return {"path": path, "error": f"{type(e).__name__}: {e}"}

    lines = src.splitlines()
    loc = len(lines)
    sloc = sum(1 for ln in lines if ln.strip() and not ln.strip().startswith("#"))

    funcs: List[Dict[str, Any]] = []
    classes: List[Dict[str, Any]] = []
    n_imports = 0

    def walk_body(body, prefix=""):
        nonlocal n_imports
        for node in body:
            if isinstance(node, (ast.Import, ast.ImportFrom)):
                n_imports += 1
            elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                funcs.append({
                    "name": prefix + node.name,
                    "lines": _seg(node),
                    "cc": _cc(node),
                    "args": len(node.args.args) + len(node.args.kwonlyargs),
                    "lineno": node.lineno,
                })
            elif isinstance(node, ast.ClassDef):
                methods = [n for n in node.body
                           if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))]
                pub = [m for m in methods if not m.name.startswith("_")]
                m_cc = max((_cc(m) for m in methods), default=1)
                classes.append({
                    "name": prefix + node.name,
                    "lines": _seg(node),
                    "n_methods": len(methods),
                    "n_public": len(pub),
                    "max_method_lines": max((_seg(m) for m in methods), default=0),
                    "max_method_cc": m_cc,
                    "lineno": node.lineno,
                })
                walk_body(node.body, prefix=prefix + node.name + ".")

    walk_body(tree.body)

    return {
        "path": path,
        "loc": loc,
        "sloc": sloc,
        "n_func": len([f for f in funcs if "." not in f["name"]]),
        "n_class": len([c for c in classes if "." not in c["name"]]),
        "n_imports": n_imports,
        "max_func_lines": max((f["lines"] for f in funcs), default=0),
        "max_func": max((f["name"] for f in funcs), key=lambda n: 0) if funcs else "",
        "top_func": max(funcs, key=lambda f: f["lines"])["name"] if funcs else "",
        "worst_cc_func": max(funcs, key=lambda f: f["cc"])["name"] if funcs else "",
        "max_cc": max((f["cc"] for f in funcs), default=1),
        "class_max_cc": max((c["max_method_cc"] for c in classes), default=1),
        "max_class_lines": max((c["lines"] for c in classes), default=0),
        "top_class": max(classes, key=lambda c: c["lines"])["name"] if classes else "",
        "max_methods": max((c["n_methods"] for c in classes), default=0),
        "max_public_methods": max((c["n_public"] for c in classes), default=0),
        "hot_cc": sum(1 for f in funcs if f["cc"] >= 10),
        "long_func": sum(1 for f in funcs if f["lines"] > 80),
        "very_long_func": sum(1 for f in funcs if f["lines"] > 150),
        "god_class": sum(1 for c in classes if c["n_methods"] >= 15 or c["lines"] > 400),
        "total_units": len(funcs) + len(classes),
    }


def main() -> int:
    out = []
    for p in iter_py(ROOT):
        rel = os.path.relpath(p, ROOT).replace("\\", "/")
        r = analyze(p)
        if "error" in r:
            continue
        r["path"] = rel
        out.append(r)

    out.sort(key=lambda r: -r["loc"])
    json.dump(out, open(os.path.join(ROOT, "output_report", "py_complexity_scan.json"),
                        "w", encoding="utf-8"), ensure_ascii=False, indent=1)

    print(f"扫描文件数：{len(out)}")
    print()
    hdr = f'{"文件":<62}{"LOC":>6}{"函数":>5}{"类":>4}{"最长函数":>9}{"最高CC":>7}{"热CC":>5}{"长函数":>6}{"最长类":>7}{"方法":>5}'
    print(hdr)
    print("-" * len(hdr))
    for r in out[:30]:
        print(f'{r["path"][:61]:<62}{r["loc"]:>6}{r["n_func"]:>5}{r["n_class"]:>4}'
              f'{r["max_func_lines"]:>9}{max(r["max_cc"], r["class_max_cc"]):>7}'
              f'{r["hot_cc"]:>5}{r["long_func"]:>6}{r["max_class_lines"]:>7}{r["max_methods"]:>5}')
    return 0


if __name__ == "__main__":
    sys.exit(main())
