# -*- coding: utf-8 -*-
"""清理 src/ 和 tools/ 目录的 27 个未使用 import（保守小步）。

安全约束：
- 只处理用户确认的 src/ + tools/ 共 19 个文件、27 个未用 import
- 用 AST 精确重建 import 行，保留原有缩进/格式
- 按行号从大到小处理（删除行不影响前面的行号定位）
- 每步 ast.parse 验证 + 删除后未用 import 数校验
- 动手前 .bak_imp 备份
"""
import ast
import os

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# (相对路径, 行号, 类型, 参数)
#   类型 "line"  -> 删除整行
#   类型 "names" -> 从该行的 import 中删除指定名字
OPS = [
    ("src/wqb/expression/diversity_enhancer.py", 13, "names", ["Counter"]),
    ("src/wqb/expression/diversity_enhancer.py", 14, "names", ["Set"]),
    ("src/wqb/expression/diversity_enhancer.py", 16, "line", None),

    ("src/wqb/expression/validator.py", 15, "names", ["Optional"]),
    ("src/wqb/expression/validator.py", 17, "names", ["SHAPE_CLASSES"]),

    ("src/wqb/memory/idea_store.py", 18, "names", ["Union"]),

    ("src/wqb/store/campaign.py", 15, "names", ["Iterable"]),

    ("src/wqb/workflow/executor.py", 12, "names", ["Callable"]),
    ("src/wqb/workflow/executor.py", 14, "names", ["WorkflowRegistry"]),

    ("src/wqb/workflow/mcp_check.py", 9, "names", ["Optional"]),

    ("src/wqb/workflow/nodes/batch_track.py", 7, "line", None),
    ("src/wqb/workflow/nodes/batch_track.py", 13, "names", ["List"]),

    ("src/wqb/workflow/nodes/feature_engineering.py", 8, "line", None),
    ("src/wqb/workflow/nodes/feature_engineering.py", 13, "names", ["List"]),

    ("src/wqb/workflow/nodes/judge.py", 7, "line", None),
    ("src/wqb/workflow/nodes/judge.py", 10, "line", None),

    ("src/wqb/workflow/nodes/submit_alpha.py", 8, "line", None),

    ("src/wqb/workflow/registry.py", 9, "line", None),
    ("src/wqb/workflow/registry.py", 10, "line", None),

    ("tools/archive_json_to_attic.py", 16, "line", None),
    ("tools/convert_alpha_list_to_exprs.py", 23, "line", None),
    ("tools/gbr_pre_submit_check.py", 12, "names", ["List"]),
    ("tools/migrate_phase2.py", 16, "line", None),
    ("tools/submit_batch.py", 34, "line", None),
    ("tools/submit_verdict.py", 22, "line", None),
    ("tools/super_build.py", 31, "line", None),
    ("tools/test_gbr_batch_isolation.py", 12, "names", ["Optional"]),
]


def rebuild_import_line(line, drop_names):
    """用 AST 重建 import 行，移除 drop_names 中的名字。
    保留原有缩进与行尾注释。"""
    stripped = line.lstrip()
    indent = line[: len(line) - len(stripped)]
    # 分离行尾注释（import 行通常无注释，但保守处理）
    code_part = stripped
    comment = ""
    if "#" in code_part and not code_part.strip().startswith("#"):
        idx = code_part.index("#")
        # 简单判断：# 前是空白且其后不构成字符串（import 行基本不会有字符串常量）
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
        if a.asname:
            kept.append(f"{a.name} as {a.asname}")
        else:
            kept.append(a.name)

    if not kept:
        # 全部名字都被删除 -> 标记删除整行
        return ""

    if isinstance(node, ast.Import):
        new_code = "import " + ", ".join(kept)
    else:
        dots = "." * (node.level or 0)
        module = (dots + node.module) if node.module else dots
        new_code = f"from {module} import " + ", ".join(kept)

    return indent + new_code + (("  " + comment) if comment else "")


def main():
    # 按文件分组，行号从大到小
    by_file = {}
    for rel, line, kind, param in OPS:
        by_file.setdefault(rel, []).append((line, kind, param))

    done, failed, skipped = [], [], []

    for rel in sorted(by_file):
        path = os.path.join(ROOT, rel)
        if not os.path.exists(path):
            failed.append((rel, "文件不存在"))
            continue

        with open(path, encoding="utf-8", newline="") as f:
            original = f.read()

        with open(path + ".bak_imp", "w", encoding="utf-8", newline="") as f:
            f.write(original)

        lines = original.split("\n")

        # 行号从大到小，避免删除导致偏移
        ops = sorted(by_file[rel], key=lambda x: -x[0])
        removed_count = 0
        modified_count = 0

        for lineno, kind, param in ops:
            idx = lineno - 1
            if idx >= len(lines):
                failed.append((rel, f"行号 {lineno} 越界"))
                continue

            target_line = lines[idx]

            if kind == "line":
                # 校验该行确实是 import 语句（防误删）
                s = target_line.strip()
                if not (s.startswith("import ") or s.startswith("from ")):
                    failed.append((rel, f"L{lineno} 不是 import 行: {s[:50]}"))
                    continue
                del lines[idx]
                removed_count += 1
            else:  # names
                new_line = rebuild_import_line(target_line, param)
                if new_line is None:
                    failed.append((rel, f"L{lineno} 无法解析: {target_line.strip()[:50]}"))
                    continue
                if new_line == "":
                    # 所有名字都被删 -> 删整行
                    del lines[idx]
                    removed_count += 1
                else:
                    lines[idx] = new_line
                    modified_count += 1

        new_content = "\n".join(lines)

        # 语法校验
        try:
            ast.parse(new_content)
        except SyntaxError as e:
            failed.append((rel, f"修改后语法错误 line {e.lineno}: {e.msg}"))
            os.remove(path + ".bak_imp")
            continue

        with open(path, "w", encoding="utf-8", newline="") as f:
            f.write(new_content)

        done.append((rel, removed_count, modified_count))

    print(f"处理成功: {len(done)} 个文件")
    for rel, rm, mod in done:
        print(f"  OK  {rel}  (删整行 {rm}, 改行内 {mod})")

    if failed:
        print(f"\n失败: {len(failed)}")
        for rel, why in failed:
            print(f"  XX  {rel}: {why}")

    print(f"\n备份: 各文件同目录 *.bak_imp")


if __name__ == "__main__":
    main()
