# -*- coding: utf-8 -*-
"""死代码扫描（只读，绝不修改任何文件）。

收编自 tracking/_scratch/_scan_deadcode.py (v1) 与 _scan_deadcode_v2.py (v2)，
固化第 3 次全项目清理（2026-08-28）经验。遵循 AGENTS.md §6 工具化纪律。

能力:
  - 未使用 import 检测（保守：字符串/docstring 内出现也算使用）
  - 死定义检测（排除注册式装饰器 @mcp.tool()/@app.route()/@fixture 等反射调用）
  - 排除归档 / 第三方 / 运行时目录

用法:
  # 扫描整个项目，输出 JSON 报告
  python tools/scan_deadcode.py --out logs/_deadcode_report.json

  # 只扫描单个文件
  python tools/scan_deadcode.py --path src/wqb/expression/validator.py

  # 只扫描某个子目录
  python tools/scan_deadcode.py --path tools/ --out logs/_t.json

退出码: 0（只读工具，不做删除；删除请配合 tools/clean_unused_imports.py）
"""
import argparse
import ast
import json
import os
import sys
from collections import Counter

# 项目根 = tools/ 的上一级
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 全量扫描时跳过的目录（归档/第三方/运行时）
SKIP_DIRS = {
    ".git", "attic", ".venv", "__pycache__", "node_modules",
    ".pytest_tmp", ".pytest_cache", "research-data", "extensions",
    "logs", "data",
}

# 视为"注册式"的装饰器（被框架反射调用，文件内无直接引用 = 正常，非死代码）
REGISTRY_DECORATORS = {
    "tool", "resource", "prompt",                        # FastMCP
    "app", "mcp", "route", "fixture",                    # 命名空间/路由
    "property", "staticmethod", "classmethod",
}


def is_test_file(rel):
    """测试文件：pytest 反射式收集 test_* 函数，内部无直接引用 = 正常，非死代码。
    默认扫描排除（--include-tests 可纳入）。"""
    base = os.path.basename(rel)
    return ("/tests/" in rel) or base.startswith("test_") or base == "conftest.py"


def iter_py_files(root, only_path=None, include_tests=False):
    """遍历 .py 文件。only_path 为单文件则只返回它；为目录则只扫该目录。"""
    if only_path:
        abs_only = os.path.abspath(only_path)
        if os.path.isfile(abs_only):
            # 注意：本函数是生成器（下文有 yield），必须 yield 而非 return 列表
            yield abs_only
            return
        # 目录模式：仍跳过嵌套的归档/运行时目录，但保留目标目录本身
        for dirpath, dirnames, filenames in os.walk(abs_only):
            dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS
                           and not d.startswith(".")]
            for fn in filenames:
                if fn.endswith(".py"):
                    p = os.path.join(dirpath, fn)
                    rel = os.path.relpath(p, root).replace("\\", "/")
                    if not include_tests and is_test_file(rel):
                        continue
                    yield p
        return

    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS
                       and not d.startswith(".")]
        # 相对路径判断，跳过嵌套的 tracking/_scratch（一次性脚本不审计）
        rel = os.path.relpath(dirpath, root).replace("\\", "/")
        if rel.startswith("tracking/_scratch"):
            dirnames[:] = []
            continue
        for fn in filenames:
            if fn.endswith(".py"):
                p = os.path.join(dirpath, fn)
                prel = os.path.relpath(p, root).replace("\\", "/")
                if not include_tests and is_test_file(prel):
                    continue
                yield p


def decorator_names(node):
    """提取节点装饰器的点分名字列表。"""
    out = []
    for d in node.decorator_list:
        if isinstance(d, ast.Name):
            out.append(d.id)
        elif isinstance(d, ast.Attribute):
            parts = []
            n = d
            while isinstance(n, ast.Attribute):
                parts.append(n.attr)
                n = n.value
            if isinstance(n, ast.Name):
                parts.append(n.id)
            out.append(".".join(reversed(parts)))
        elif isinstance(d, ast.Call):
            f = d.func
            if isinstance(f, ast.Attribute):
                parts = []
                n = f
                while isinstance(n, ast.Attribute):
                    parts.append(n.attr)
                    n = n.value
                if isinstance(n, ast.Name):
                    parts.append(n.id)
                out.append(".".join(reversed(parts)))
            elif isinstance(f, ast.Name):
                out.append(f.id)
    return out


def is_registry(node):
    """是否被注册式装饰器修饰（反射调用，非死代码）。"""
    for n in decorator_names(node):
        last = n.split(".")[-1]
        if last in REGISTRY_DECORATORS or n in REGISTRY_DECORATORS:
            return True
    return False


def analyze(path):
    """返回 (unused_imports, dead_defs, registry_defs, err)。

    unused_imports: [{name, module, line}]
    dead_defs:      [{kind, name, line}]   (排除注册式 + __all__ 导出)
    registry_defs:  [{kind, name, line, decorators}]
    """
    try:
        src = open(path, encoding="utf-8").read()
    except Exception as e:
        return None, None, None, f"读取失败: {e}"

    try:
        tree = ast.parse(src)
    except SyntaxError as e:
        return None, None, None, f"语法错误 line {e.lineno}: {e.msg}"

    # ---- 未使用 import ----
    imported, alias_map = {}, {}
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for a in node.names:
                local = a.asname or a.name.split(".")[0]
                imported[local] = node.lineno
                alias_map[local] = a.name
        elif isinstance(node, ast.ImportFrom):
            if node.module == "__future__":
                continue
            for a in node.names:
                if a.name in ("annotations", "TYPE_CHECKING"):
                    continue
                local = a.asname or a.name
                imported[local] = node.lineno
                alias_map[local] = f"{node.module}.{a.name}" if node.module else a.name

    used = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Name):
            used.add(node.id)
        elif isinstance(node, ast.Attribute):
            n = node
            while isinstance(n, ast.Attribute):
                n = n.value
            if isinstance(n, ast.Name):
                used.add(n.id)
    # 字符串 / docstring 内出现的名字也保守视为使用
    for node in ast.walk(tree):
        if isinstance(node, ast.Constant) and isinstance(node.value, str):
            for name in imported:
                if name in node.value:
                    used.add(name)

    unused_imports = [
        {"name": n, "module": alias_map.get(n, ""), "line": ln}
        for n, ln in imported.items() if n not in used and n != "_"
    ]

    # ---- 死定义（排除注册式装饰器 + __all__ 导出）----
    all_names = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Name):
            all_names.append(node.id)
        elif isinstance(node, ast.Attribute):
            n = node
            while isinstance(n, ast.Attribute):
                n = n.value
            if isinstance(n, ast.Name):
                all_names.append(n.id)
    name_count = Counter(all_names)

    exported = set()
    for node in tree.body:
        if isinstance(node, ast.Assign):
            for t in node.targets:
                if isinstance(t, ast.Name) and t.id == "__all__":
                    if isinstance(node.value, (ast.List, ast.Tuple)):
                        for el in node.value.elts:
                            if isinstance(el, ast.Constant):
                                exported.add(el.value)

    dead, registry = [], []
    for node in tree.body:
        if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            continue
        kind = "class" if isinstance(node, ast.ClassDef) else "def"
        name = node.name
        if name.startswith("__") or name in exported:
            continue
        if is_registry(node):
            registry.append({
                "kind": kind, "name": name, "line": node.lineno,
                "decorators": decorator_names(node),
            })
            continue
        occurrences = src.count(name)
        if name_count.get(name, 0) <= 0 and occurrences <= 1:
            dead.append({"kind": kind, "name": name, "line": node.lineno})

    return unused_imports, dead, registry, None


def main():
    ap = argparse.ArgumentParser(description="死代码只读扫描（未用 import + 死定义）")
    ap.add_argument("--root", default=ROOT, help="项目根（默认 tools/ 上级）")
    ap.add_argument("--path", default=None,
                    help="只扫描单文件或子目录（默认全项目）")
    ap.add_argument("--out", default=None,
                    help="报告 JSON 输出路径（默认不写文件，仅打印摘要）")
    ap.add_argument("--include-tests", action="store_true",
                    help="纳入 tests/ 与 test_*.py（默认排除：pytest 反射收集会产生误报）")
    args = ap.parse_args()

    files = list(iter_py_files(args.root, args.path, args.include_tests))
    report = {
        "root": os.path.abspath(args.root),
        "scanned_path": os.path.abspath(args.path) if args.path else "(whole project)",
        "scanned_files": len(files),
        "unused_imports": [], "dead_defs": [], "registry_defs": [],
        "syntax_errors": [], "totals": {},
    }

    for path in files:
        rel = os.path.relpath(path, args.root).replace("\\", "/")
        unused, dead, registry, err = analyze(path)
        if err:
            report["syntax_errors"].append({"file": rel, "error": err})
            continue
        if unused:
            report["unused_imports"].append({"file": rel, "items": unused})
        if dead:
            report["dead_defs"].append({"file": rel, "items": dead})
        if registry:
            report["registry_defs"].append({"file": rel, "items": registry})

    t = report["totals"] = {
        "unused_imports": sum(len(r["items"]) for r in report["unused_imports"]),
        "true_dead_defs": sum(len(r["items"]) for r in report["dead_defs"]),
        "registry_defs_excluded": sum(len(r["items"]) for r in report["registry_defs"]),
        "syntax_errors": len(report["syntax_errors"]),
        "files_with_unused": len(report["unused_imports"]),
        "files_with_dead": len(report["dead_defs"]),
    }

    if args.out:
        os.makedirs(os.path.dirname(os.path.abspath(args.out)), exist_ok=True)
        with open(args.out, "w", encoding="utf-8") as f:
            json.dump(report, f, ensure_ascii=False, indent=2)

    print(f"扫描文件数: {report['scanned_files']}")
    print(f"未使用 import: {t['unused_imports']} 个（分布在 {t['files_with_unused']} 个文件）")
    print(f"真·死定义（排除注册式）: {t['true_dead_defs']} 个（分布在 {t['files_with_dead']} 个文件）")
    print(f"注册式定义（已排除，非死代码）: {t['registry_defs_excluded']} 个")
    print(f"语法错误文件: {t['syntax_errors']} 个")
    if args.out:
        print(f"\n报告: {os.path.abspath(args.out)}")

    if report["dead_defs"]:
        print("\n=== 真·死定义 Top 15 ===")
        for r in sorted(report["dead_defs"], key=lambda x: -len(x["items"]))[:15]:
            names = ", ".join(i["name"] for i in r["items"][:6])
            print(f"  {r['file']}: {len(r['items'])} 个 -> {names}")

    if report["syntax_errors"]:
        print("\n=== 语法错误 ===")
        for e in report["syntax_errors"][:10]:
            print(f"  {e['file']}: {e['error']}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
