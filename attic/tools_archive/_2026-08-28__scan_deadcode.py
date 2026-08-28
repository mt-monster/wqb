# -*- coding: utf-8 -*-
"""扫描项目源码中的未使用 import 与死代码（只读，不修改任何文件）。
用法: python tracking/_scratch/_scan_deadcode.py
输出: tracking/_scratch/_deadcode_report.json
"""
import ast
import os
import json
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SKIP_DIRS = {".git", "attic", ".venv", "__pycache__", "node_modules",
             ".pytest_tmp", ".pytest_cache", "research-data", "extensions",
             "logs", "data", "tracking/_scratch"}

# 这些 import 即使"看起来未用"也是必要的（副作用/注册/类型注解）
KEEP_MODULES = {
    "__future__",  # from __future__ import annotations
}
KEEP_NAMES = {
    "annotations",  # from __future__ import annotations
    "TYPE_CHECKING",
}


def iter_py_files(root):
    """遍历项目内所有 .py 文件（跳过归档/第三方/运行时目录）。"""
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS
                       and not d.startswith(".")]
        # 相对路径判断，用于跳过嵌套的 tracking/_scratch
        rel = os.path.relpath(dirpath, root).replace("\\", "/")
        if rel.startswith("tracking/_scratch"):
            dirnames[:] = []
            continue
        for fn in filenames:
            if fn.endswith(".py"):
                yield os.path.join(dirpath, fn)


def analyze_file(path):
    """返回 (未使用import列表, 顶层未引用函数/类列表, 语法错误)"""
    try:
        src = open(path, encoding="utf-8").read()
    except Exception as e:
        return None, None, f"读取失败: {e}"

    try:
        tree = ast.parse(src)
    except SyntaxError as e:
        return None, None, f"语法错误 line {e.lineno}: {e.msg}"

    # ---------- 1) 收集所有 import 的名字 ----------
    imported = {}   # name -> lineno
    alias_map = {}  # asname -> 原始模块路径（用于 from x import y as z）
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for a in node.names:
                local = a.asname or a.name.split(".")[0]
                imported[local] = node.lineno
                alias_map[local] = a.name
        elif isinstance(node, ast.ImportFrom):
            if node.module in KEEP_MODULES:
                continue
            for a in node.names:
                if a.name in KEEP_NAMES:
                    continue
                local = a.asname or a.name
                imported[local] = node.lineno
                alias_map[local] = f"{node.module}.{a.name}" if node.module else a.name

    # ---------- 2) 收集所有"被使用"的名字 ----------
    used = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Name):
            used.add(node.id)
        elif isinstance(node, ast.Attribute):
            # a.b.c -> 记录最左端 a
            n = node
            while isinstance(n, ast.Attribute):
                n = n.value
            if isinstance(n, ast.Name):
                used.add(n.id)

    # 字符串注解 / __all__ / docstring 里出现的也视为使用（保守）
    for node in ast.walk(tree):
        if isinstance(node, ast.Constant) and isinstance(node.value, str):
            for name in imported:
                if name in node.value:
                    used.add(name)

    # 类型注解（即便用字符串形式也在上面覆盖了）
    unused_imports = []
    for name, lineno in imported.items():
        if name not in used and name != "_":
            unused_imports.append({
                "name": name,
                "module": alias_map.get(name, ""),
                "line": lineno,
            })

    # ---------- 3) 顶层函数/类是否被内部引用 ----------
    top_defs = []
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            top_defs.append(("def", node.name, node.lineno))
        elif isinstance(node, ast.ClassDef):
            top_defs.append(("class", node.name, node.lineno))

    # 统计每个名字在全文件（除 def 行本身）出现的次数
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
    from collections import Counter
    name_count = Counter(all_names)

    # 文件内文本出现次数（含字符串/docstring，更保守）
    dead_defs = []
    for kind, name, lineno in top_defs:
        # 被引用次数 = 全文本出现次数
        occurrences = src.count(name)
        if kind == "def":
            # def foo 本身算 1 次；若只出现 1 次则未被引用
            is_dead = name_count.get(name, 0) <= 0 and occurrences <= 1
        else:
            is_dead = name_count.get(name, 0) <= 0 and occurrences <= 1
        # 排除 dunder / 常见入口 / 被 __all__ 导出
        if is_dead and not name.startswith("__"):
            # 检查是否在 __all__ 中
            in_all = False
            for node in tree.body:
                if isinstance(node, ast.Assign):
                    for t in node.targets:
                        if isinstance(t, ast.Name) and t.id == "__all__":
                            if isinstance(node.value, (ast.List, ast.Tuple)):
                                for el in node.value.elts:
                                    if isinstance(el, ast.Constant) and el.value == name:
                                        in_all = True
            if not in_all:
                dead_defs.append({"kind": kind, "name": name, "line": lineno})

    return unused_imports, dead_defs, None


def main():
    files = list(iter_py_files(ROOT))
    report = {
        "root": ROOT,
        "scanned_files": len(files),
        "files_with_unused_imports": [],
        "files_with_dead_defs": [],
        "syntax_errors": [],
        "total_unused_imports": 0,
        "total_dead_defs": 0,
    }

    for path in files:
        rel = os.path.relpath(path, ROOT).replace("\\", "/")
        unused, dead, err = analyze_file(path)
        if err:
            report["syntax_errors"].append({"file": rel, "error": err})
            continue
        if unused:
            report["files_with_unused_imports"].append({"file": rel, "items": unused})
            report["total_unused_imports"] += len(unused)
        if dead:
            report["files_with_dead_defs"].append({"file": rel, "items": dead})
            report["total_dead_defs"] += len(dead)

    out = os.path.join(ROOT, "tracking", "_scratch", "_deadcode_report.json")
    with open(out, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)

    print(f"扫描文件数: {report['scanned_files']}")
    print(f"未使用 import 总数: {report['total_unused_imports']}")
    print(f"疑似死定义总数: {report['total_dead_defs']}")
    print(f"语法错误文件数: {len(report['syntax_errors'])}")
    print(f"\n报告已写入: {out}")

    # 打印 Top 20
    print("\n=== 未使用 import 最多的文件 (Top 20) ===")
    rows = sorted(report["files_with_unused_imports"],
                  key=lambda x: -len(x["items"]))[:20]
    for r in rows:
        names = ", ".join(i["name"] for i in r["items"][:8])
        print(f"  {r['file']}: {len(r['items'])} 个 -> {names}")

    if report["syntax_errors"]:
        print("\n=== 语法错误文件 ===")
        for e in report["syntax_errors"][:10]:
            print(f"  {e['file']}: {e['error']}")


if __name__ == "__main__":
    main()
