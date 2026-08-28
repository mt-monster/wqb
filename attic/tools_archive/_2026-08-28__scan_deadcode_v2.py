# -*- coding: utf-8 -*-
"""死代码扫描 v2：排除装饰器注册（MCP @mcp.tool() 等）导致的误报。
只读扫描，不修改任何文件。
"""
import ast
import os
import json
from collections import Counter

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SKIP_DIRS = {".git", "attic", ".venv", "__pycache__", "node_modules",
             ".pytest_tmp", ".pytest_cache", "research-data", "extensions",
             "logs", "data"}

# 视为"注册式"的装饰器（被框架反射调用，文件内无直接引用 = 正常）
REGISTRY_DECORATORS = {
    "tool", "resource", "prompt",           # FastMCP
    "app.tool", "mcp.tool", "app.route",    # 带命名空间的
    "fixture", "property", "staticmethod", "classmethod",
}


def iter_py_files(root):
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS
                       and not d.startswith(".")]
        rel = os.path.relpath(dirpath, root).replace("\\", "/")
        if rel.startswith("tracking/_scratch"):
            dirnames[:] = []
            continue
        for fn in filenames:
            if fn.endswith(".py"):
                yield os.path.join(dirpath, fn)


def decorator_names(node):
    """提取节点装饰器的点分名字列表"""
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
            # @mcp.tool() 形式
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
    """是否被注册式装饰器修饰"""
    names = decorator_names(node)
    for n in names:
        # 取最后一段匹配（mcp.tool -> tool）
        last = n.split(".")[-1]
        if last in REGISTRY_DECORATORS or n in REGISTRY_DECORATORS:
            return True
    return False


def analyze(path):
    try:
        src = open(path, encoding="utf-8").read()
    except Exception as e:
        return None, None, f"读取失败: {e}"
    try:
        tree = ast.parse(src)
    except SyntaxError as e:
        return None, None, f"语法错误 line {e.lineno}: {e.msg}"

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

    # 收集 __all__ 导出
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
            registry.append({"kind": kind, "name": name, "line": node.lineno,
                             "decorators": decorator_names(node)})
            continue
        occurrences = src.count(name)
        if name_count.get(name, 0) <= 0 and occurrences <= 1:
            dead.append({"kind": kind, "name": name, "line": node.lineno})

    return unused_imports, {"dead": dead, "registry": registry}, None


def main():
    files = list(iter_py_files(ROOT))
    report = {"root": ROOT, "scanned_files": len(files),
              "unused_imports": [], "dead_defs": [], "registry_defs": [],
              "syntax_errors": [], "totals": {}}

    for path in files:
        rel = os.path.relpath(path, ROOT).replace("\\", "/")
        unused, defs, err = analyze(path)
        if err:
            report["syntax_errors"].append({"file": rel, "error": err})
            continue
        if unused:
            report["unused_imports"].append({"file": rel, "items": unused})
        if defs["dead"]:
            report["dead_defs"].append({"file": rel, "items": defs["dead"]})
        if defs["registry"]:
            report["registry_defs"].append({"file": rel, "items": defs["registry"]})

    report["totals"] = {
        "unused_imports": sum(len(r["items"]) for r in report["unused_imports"]),
        "true_dead_defs": sum(len(r["items"]) for r in report["dead_defs"]),
        "registry_defs_excluded": sum(len(r["items"]) for r in report["registry_defs"]),
        "syntax_errors": len(report["syntax_errors"]),
        "files_with_unused": len(report["unused_imports"]),
        "files_with_dead": len(report["dead_defs"]),
    }

    out = os.path.join(ROOT, "tracking", "_scratch", "_deadcode_report_v2.json")
    with open(out, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)

    t = report["totals"]
    print(f"扫描文件数: {report['scanned_files']}")
    print(f"未使用 import: {t['unused_imports']} 个（分布在 {t['files_with_unused']} 个文件）")
    print(f"真·死定义（排除注册式）: {t['true_dead_defs']} 个（分布在 {t['files_with_dead']} 个文件）")
    print(f"注册式定义（已排除，非死代码）: {t['registry_defs_excluded']} 个")
    print(f"语法错误文件: {t['syntax_errors']} 个")
    print(f"\n报告: {out}")

    if report["dead_defs"]:
        print("\n=== 真·死定义 Top 15 文件 ===")
        rows = sorted(report["dead_defs"], key=lambda x: -len(x["items"]))[:15]
        for r in rows:
            names = ", ".join(f"{i['name']}" for i in r["items"][:6])
            print(f"  {r['file']}: {len(r['items'])} 个 -> {names}")


if __name__ == "__main__":
    main()
