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
                # module="" 表示普通 import 语句；None 保留给相对导入（level>0）
                imported[local] = (node.lineno, "")
                alias_map[local] = a.name
        elif isinstance(node, ast.ImportFrom):
            if node.module == "__future__":
                continue
            if node.level > 0:
                # 相对导入 from . import x：保守起见整体不参与清理
                for a in node.names:
                    local = a.asname or a.name
                    imported[local] = (node.lineno, None)
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


def module_keys(rel):
    """返回文件可能对应的所有模块名（全路径 + 各级后缀）。

    必须做**后缀全展开**而非只取 canon/base：
      - src/ 布局下 src/wqb/expression/validator.py 的实际模块名是
        `wqb.expression.validator`（src 是源根，不是包的一部分），只按仓库根算
        canon 会得到 `src.wqb.expression.validator`，与消费者 `from wqb.expression
        .validator import ...` 的 module 对不上 → re-export 校验失效。
        曾因此把 validator.py 的 SHAPE_CLASSES 误判为可删（2026-09-01 复现）。
      - 裸文件名覆盖"以包目录为 cwd 运行"的隐式导入（world-quant-brain-mcp 内部
        `from mcp_core import ...`）。
    后缀匹配偏保守（宁可不删也不错删），与原 base 匹配同向。
    """
    canon = rel[:-3].replace("\\", "/").replace("/", ".")
    parts = canon.split(".")
    return [".".join(parts[i:]) for i in range(len(parts))]


def is_reexported(rel, name, index):
    """rel 文件的模块是否被其他文件 import 了 name（即 rel 在重导出 name）。"""
    for key in module_keys(rel):
        consumers = index.get(key, {}).get(name, set())
        if any(c != rel for c in consumers):
            return True
    return False


# 结构性保护文件：这些文件的 import 即使静态分析"未使用"也不可删。
#   - 门面重导出：对外 API 通过它暴露（brain_api.py）
#   - 副作用注册：import 只为触发 MCP 工具注册（main.py 的 tools_*）
#   - 整文件粘贴型：第三方/生成代码，改动需人工（labs_data_analysis_agent.py）
DEFAULT_PROTECTED = {
    "world-quant-brain-mcp/brain_api.py",
    "world-quant-brain-mcp/main.py",
    "world-quant-brain-mcp/labs_data_analysis_agent.py",
}


def rebuild_import_stmt(node, drop_names):
    """用 AST 重建 import 语句（支持多行括号形式），移除 drop_names。
    返回新语句字符串；返回 "" 表示全部名字被删（整语句删除）。"""
    kept = []
    for a in node.names:
        local = a.asname or a.name.split(".")[0]
        if local in drop_names:
            continue
        kept.append(f"{a.name} as {a.asname}" if a.asname else a.name)
    if not kept:
        return ""
    if isinstance(node, ast.Import):
        return "import " + ", ".join(kept)
    dots = "." * (node.level or 0)
    module = (dots + node.module) if node.module else dots
    return f"from {module} import " + ", ".join(kept)


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
    ap.add_argument("--exclude", action="append", default=[],
                    help="排除的文件相对路径（精确匹配，可重复）。用于门面重导出/副作用导入/整文件粘贴等不可清理文件")
    args = ap.parse_args()

    if args.report and args.path:
        print("错误：--report 与 --path 二选一", file=sys.stderr)
        return 2

    dry_run = not args.apply
    candidates = collect_candidates(args.report, args.path, args.include_tests)
    excludes = set(args.exclude) | DEFAULT_PROTECTED
    protected_hit = sorted(DEFAULT_PROTECTED & {rel for rel, _ in candidates})
    candidates = [(rel, items) for rel, items in candidates if rel not in excludes]
    if protected_hit:
        print(f"[保护] 结构性保护文件已跳过（不可清理）: {', '.join(protected_hit)}")
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

    # ---- 实际删除（语句级：支持多行括号 import）----
    done, failed = [], []
    for rel in sorted(by_file):
        path = os.path.join(args.root, rel)
        with open(path, encoding="utf-8", newline="") as f:
            original = f.read()
        with open(path + ".bak_imp", "w", encoding="utf-8", newline="") as f:
            f.write(original)

        # 按语句起始行聚合待删名字
        stmt_drops = {}
        for name, lineno in by_file[rel]:
            stmt_drops.setdefault(lineno, set()).add(name)

        try:
            tree = ast.parse(original)
        except SyntaxError as e:
            failed.append((rel, f"解析失败 L{e.lineno}: {e.msg}"))
            continue

        lines = original.split("\n")
        # 找到覆盖待删行的 import 语句节点，按起始行从大到小处理（避免偏移）
        stmts = [n for n in ast.walk(tree)
                 if isinstance(n, (ast.Import, ast.ImportFrom))
                 and n.lineno in stmt_drops
                 and not (isinstance(n, ast.ImportFrom) and n.level > 0)]
        removed = modified = 0
        unresolved = set(stmt_drops)
        for node in sorted(stmts, key=lambda n: -n.lineno):
            drops = stmt_drops[node.lineno]
            start = node.lineno - 1
            end = node.end_lineno  # 切片右开：覆盖到语句最后一行
            if end > len(lines):
                failed.append((rel, f"L{node.lineno}-{end} 越界"))
                continue
            indent = re.match(r"[ \t]*", lines[start]).group(0)
            new_stmt = rebuild_import_stmt(node, drops)
            if new_stmt == "":
                del lines[start:end]
                removed += 1
            else:
                lines[start:end] = [indent + new_stmt]
                modified += 1
            unresolved.discard(node.lineno)

        if unresolved:
            failed.append((rel, f"未定位到语句: {sorted(unresolved)}"))
            os.remove(path + ".bak_imp")
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
