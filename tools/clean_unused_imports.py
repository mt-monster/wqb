# -*- coding: utf-8 -*-
"""清理未使用 import（报告驱动 / 直接扫描，安全优先）。

收编自 tracking/_scratch/_clean_unused_imports.py（2026-08-28）。固化第 3 次
全项目清理经验，落实 dead-code-cleanup skill 红线（尤其 SHAPE_CLASSES 重导出
误删教训：单文件 AST 无法识别 re-export，必须跨文件校验）。

安全约束:
  - **默认 --dry-run（只列出将删除的 import，不动手）；--apply 才实际写**
  - 跨文件 re-export 校验：若某 import 的名字被其他文件 `from <本模块> import 名字`
    引用（即本文件在重导出公开 API），则跳过，绝不删
  - 动手前 .bak_imp 备份；按行号从大到小删除避免偏移；写回后 ast.parse 验证

用法:
  # 直接扫描某路径，列出将删除项（dry-run）
  python tools/clean_unused_imports.py --path tools/
  python tools/clean_unused_imports.py --path src/wqb/expression/validator.py

  # 用 scan_deadcode 的 JSON 报告驱动
  python tools/clean_unused_imports.py --report logs/_deadcode_report.json

  # 实际执行（带备份 + 跨文件校验 + ast 校验）
  python tools/clean_unused_imports.py --path src/wqb/ --apply

退出码: 0=完成；1=dry-run 且有可删项（便于 CI 检测未清理残留）
"""
import argparse
import ast
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKIP_DIRS = {
    ".git", "attic", ".venv", "__pycache__", "node_modules",
    ".pytest_tmp", ".pytest_cache", "research-data", "extensions",
    "logs", "data", "tracking/_scratch",
}


def iter_py_files(root, only_path=None):
    if only_path:
        abs_only = os.path.abspath(only_path)
        if os.path.isfile(abs_only):
            yield abs_only  # 生成器函数：必须 yield 而非 return 列表
            return
        for dirpath, dirnames, filenames in os.walk(abs_only):
            dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS
                           and not d.startswith(".")]
            for fn in filenames:
                if fn.endswith(".py"):
                    yield os.path.join(dirpath, fn)
        return
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS
                       and not d.startswith(".")]
        # 按相对路径跳过一次性脚本区（gitignored，不审计）
        rel_dir = os.path.relpath(dirpath, root).replace("\\", "/")
        if rel_dir == "tracking/_scratch" or rel_dir.startswith("tracking/_scratch/"):
            dirnames[:] = []
            continue
        for fn in filenames:
            if fn.endswith(".py"):
                yield os.path.join(dirpath, fn)


def detect_unused_imports(path):
    """返回未使用 import 列表 [(name, module, line)]（module 为 None 表示相对导入）。"""
    try:
        src = open(path, encoding="utf-8").read()
    except Exception:
        return []
    try:
        tree = ast.parse(src)
    except SyntaxError:
        return []

    imported, alias_map = {}, {}
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for a in node.names:
                local = a.asname or a.name.split(".")[0]
                imported[local] = (node.lineno, None)
                alias_map[local] = a.name
        elif isinstance(node, ast.ImportFrom):
            if node.module == "__future__":
                continue
            for a in node.names:
                if a.name in ("annotations", "TYPE_CHECKING"):
                    continue
                local = a.asname or a.name
                imported[local] = (node.lineno, node.module)
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

    out = []
    for name, (lineno, module) in imported.items():
        if name not in used and name != "_":
            out.append((name, module, lineno))
    return out


def build_import_index(root):
    """跨文件 import 索引：module(点分) -> {name: set(rel_file)}。

    用于 re-export 校验：若本文件 F 的模块名 `tools.validator` 出现在索引中
    且带有候选 name，说明别的文件 `from tools.validator import name`（重导出），
    则该 import 不可删。
    """
    index = {}
    for path in iter_py_files(root):
        rel = os.path.relpath(path, root).replace("\\", "/")
        canon = rel[:-3].replace("/", ".")
        try:
            src = open(path, encoding="utf-8").read()
            tree = ast.parse(src)
        except Exception:
            continue
        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom) and node.module:
                for a in node.names:
                    local = a.asname or a.name
                    index.setdefault(node.module, {}).setdefault(local, set()).add(rel)
    return index


def is_reexported(rel, name, index):
    """rel 文件的模块是否被其他文件 import 了 name（即 rel 在重导出 name）。"""
    canon = rel[:-3].replace("/", ".")
    consumers = index.get(canon, {}).get(name, set())
    return any(c != rel for c in consumers)


def rebuild_import_line(line, drop_names):
    """用 AST 重建 import 行，移除 drop_names（保留缩进/注释）。返回 '' 表示整行删除。"""
    stripped = line.lstrip()
    indent = line[: len(line) - len(stripped)]
    code_part = stripped
    comment = ""
    if "#" in code_part and not code_part.strip().startswith("#"):
        idx = code_part.index("#")
        comment = code_part[idx:]
        code_part = code_part[:idx].rstrip()
    try:
        tree = ast.parse(code_part)
    except SyntaxError:
        return None
    if not tree.body or not isinstance(tree.body[0], (ast.Import, ast.ImportFrom)):
        return None
    node = tree.body[0]
    kept = []
    for a in node.names:
        local = a.asname or a.name.split(".")[0]
        if local in drop_names:
            continue
        kept.append(f"{a.name} as {a.asname}" if a.asname else a.name)
    if not kept:
        return ""
    if isinstance(node, ast.Import):
        new_code = "import " + ", ".join(kept)
    else:
        dots = "." * (node.level or 0)
        module = (dots + node.module) if node.module else dots
        new_code = f"from {module} import " + ", ".join(kept)
    return indent + new_code + (("  " + comment) if comment else "")


def is_test_file(rel):
    """测试文件默认排除（与 scan_deadcode.py 口径一致；--include-tests 纳入）。"""
    base = os.path.basename(rel)
    return ("/tests/" in rel) or base.startswith("test_") or base == "conftest.py"


def collect_candidates(report_path, scan_path, include_tests=False):
    """返回 [(rel, [(name, module, line)])]。"""
    if report_path:
        with open(report_path, encoding="utf-8") as f:
            rep = json.load(f)
        cands = []
        for entry in rep.get("unused_imports", []):
            if not include_tests and is_test_file(entry["file"]):
                continue
            cands.append((entry["file"], [(it["name"], it["module"] or None, it["line"])
                                          for it in entry["items"]]))
        return cands
    # 直接扫描
    root = ROOT
    files = iter_py_files(root, scan_path) if scan_path else iter_py_files(root)
    cands = []
    for path in files:
        rel = os.path.relpath(path, root).replace("\\", "/")
        if not include_tests and is_test_file(rel):
            continue
        ui = detect_unused_imports(path)
        if ui:
            cands.append((rel, ui))
    return cands


def main():
    ap = argparse.ArgumentParser(description="清理未使用 import（安全，dry-run 默认）")
    ap.add_argument("--root", default=ROOT, help="项目根（默认 tools/ 上级）")
    ap.add_argument("--path", default=None, help="扫描单文件/子目录（与 --report 二选一）")
    ap.add_argument("--report", default=None, help="scan_deadcode 输出的 JSON 报告")
    ap.add_argument("--apply", dest="apply", action="store_true",
                    help="实际删除（带备份 + 跨文件校验 + ast 校验）；默认 dry-run")
    ap.add_argument("--include-tests", action="store_true",
                    help="纳入 tests/ 与 test_*.py（默认排除）")
    args = ap.parse_args()

    if args.report and args.path:
        print("错误：--report 与 --path 二选一", file=sys.stderr)
        return 2

    dry_run = not args.apply
    candidates = collect_candidates(args.report, args.path, args.include_tests)
    index = build_import_index(args.root)

    plan = []          # (rel, name, module, line, skip_reason)
    skippable = 0
    for rel, items in candidates:
        for name, module, line in items:
            if module is None:
                plan.append((rel, name, module, line, "相对导入(保守跳过)"))
                skippable += 1
            elif is_reexported(rel, name, index):
                plan.append((rel, name, module, line, "被其他文件重导出(跳过)"))
                skippable += 1
            else:
                plan.append((rel, name, module, line, ""))

    removable = [p for p in plan if not p[4]]

    print(f"候选未用 import: {len(plan)} 个（其中 {skippable} 个安全跳过，{len(removable)} 个可删）")
    if skippable:
        print("\n=== 安全跳过（不删）===")
        for rel, name, module, line, reason in plan:
            if reason:
                print(f"  SKIP {rel}:{line}  {name}  ({reason})")

    if not removable:
        print("\n无需删除（或已全部被安全跳过）。")
        return 0

    print("\n=== 将删除 ===" if dry_run else "\n=== 删除中 ===")
    by_file = {}
    for rel, name, module, line, _ in removable:
        by_file.setdefault(rel, []).append((name, line))

    if dry_run:
        for rel in sorted(by_file):
            names = ", ".join(n for n, _ in by_file[rel])
            print(f"  DRY  {rel}: {names}")
        print("\n(dry-run) 未做任何修改。加 --apply 才实际删除（带 *.bak_imp 备份）。")
        return 1

    # ---- 实际删除 ----
    done, failed = [], []
    for rel in sorted(by_file):
        path = os.path.join(args.root, rel)
        with open(path, encoding="utf-8", newline="") as f:
            original = f.read()
        with open(path + ".bak_imp", "w", encoding="utf-8", newline="") as f:
            f.write(original)
        lines = original.split("\n")
        # 行号从大到小
        ops = sorted(by_file[rel], key=lambda x: -x[1])
        removed = modified = 0
        for name, lineno in ops:
            idx = lineno - 1
            if idx >= len(lines):
                failed.append((rel, f"行号 {lineno} 越界"))
                continue
            target = lines[idx]
            s = target.strip()
            if s.startswith("import ") or s.startswith("from "):
                new_line = rebuild_import_line(target, {name})
                if new_line is None:
                    failed.append((rel, f"L{lineno} 无法解析"))
                    continue
                if new_line == "":
                    del lines[idx]
                    removed += 1
                else:
                    lines[idx] = new_line
                    modified += 1
            else:
                failed.append((rel, f"L{lineno} 非 import 行"))
                continue
        new_content = "\n".join(lines)
        try:
            ast.parse(new_content)
        except SyntaxError as e:
            failed.append((rel, f"修改后语法错误 L{e.lineno}: {e.msg}"))
            os.remove(path + ".bak_imp")
            continue
        with open(path, "w", encoding="utf-8", newline="") as f:
            f.write(new_content)
        done.append((rel, removed, modified))

    print(f"\n处理成功: {len(done)} 个文件")
    for rel, rm, mod in done:
        print(f"  OK  {rel}  (删整行 {rm}, 改行内 {mod})")
    if failed:
        print(f"\n失败: {len(failed)}")
        for rel, why in failed:
            print(f"  XX  {rel}: {why}")
    print("\n备份: 各文件同目录 *.bak_imp")
    return 0


if __name__ == "__main__":
    sys.exit(main())
