# -*- coding: utf-8 -*-
"""BOM 损坏修复（剥离 U+FEFF）。安全优先。

收编自 tracking/_scratch/_fix_bom.py（2026-08-28）。背景：部分 run_wave*.py
首行 `import os` 被插到 shebang 之前，导致本属 shebang 行首的 BOM 卡在第 2 行
中间，Python 无法解析（ast.parse 抛 SyntaxError）。

安全约束（遵循项目纪律）:
  - 只用 Python open(encoding='utf-8', newline='')，绝不用 PowerShell Get/Set-Content
    （GBK 会破坏 CJK 且不可逆）
  - newline='' 保留原始换行符（CRLF），不做隐式转换
  - 动手前 .bak_bom 备份
  - 逐文件校验：修复前后 CJK 字符数必须一致（防 mojibake）+ 修复后必须 ast.parse 通过
  - **默认 --dry-run（只列出含 BOM 的文件，不动手）；--apply 才实际修复**

用法:
  python tools/fix_bom.py --dry-run                 # 列出含 BOM 的 .py 文件
  python tools/fix_bom.py --apply                   # 全项目修复（带备份+校验）
  python tools/fix_bom.py --path <file> --apply     # 只修单个文件
  python tools/fix_bom.py --path <dir>  --apply     # 修某目录下所有 .py

退出码: 0=列出/修复完成；1=存在 BOM 但处于 dry-run（便于串进 CI 检测）
"""
import argparse
import ast
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKIP_DIRS = {
    ".git", "attic", ".venv", "__pycache__", "node_modules",
    ".pytest_tmp", ".pytest_cache", "research-data", "extensions",
    "logs", "data", "tracking/_scratch",
}
BOM = "\ufeff"


def cjk_count(s):
    return sum(1 for ch in s if "\u4e00" <= ch <= "\u9fff")


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


def main():
    ap = argparse.ArgumentParser(description="BOM(U+FEFF) 剥离修复")
    ap.add_argument("--root", default=ROOT, help="项目根（默认 tools/ 上级）")
    ap.add_argument("--path", default=None, help="单文件或子目录（默认全项目）")
    ap.add_argument("--dry-run", action="store_true",
                    help="只列出含 BOM 的文件，不修改（默认行为）")
    ap.add_argument("--apply", dest="apply", action="store_true",
                    help="实际修复（带备份 + CJK/ast 校验）")
    args = ap.parse_args()

    # 默认 dry-run
    dry_run = not args.apply

    found = []
    for path in iter_py_files(args.root, args.path):
        with open(path, encoding="utf-8", newline="") as f:
            before = f.read()
        if BOM not in before:
            continue
        rel = os.path.relpath(path, args.root).replace("\\", "/")
        found.append((path, rel, before.count(BOM)))

    if not found:
        print("未发现含 BOM 的文件。")
        return 0

    print(f"发现 {len(found)} 个含 BOM 的文件：")
    for path, rel, n in found:
        print(f"  {'DRY ' if dry_run else 'FIX '} {rel}  (BOM x{n})")

    if dry_run:
        print("\n(dry-run) 未做任何修改。加 --apply 才实际修复（带 *.bak_bom 备份）。")
        return 1

    fixed, failed = [], []
    for path, rel, n in found:
        before = open(path, encoding="utf-8", newline="").read()
        cjk_before = cjk_count(before)
        bak = path + ".bak_bom"
        with open(bak, "w", encoding="utf-8", newline="") as f:
            f.write(before)

        after = before.replace(BOM, "")
        if cjk_count(after) != cjk_before:
            failed.append((rel, f"CJK 数量变化 {cjk_before}->{cjk_count(after)}，已回滚"))
            os.remove(bak)
            continue
        try:
            ast.parse(after)
        except SyntaxError as e:
            failed.append((rel, f"修复后仍语法错误 L{e.lineno}: {e.msg}"))
            os.remove(bak)
            continue
        with open(path, "w", encoding="utf-8", newline="") as f:
            f.write(after)
        fixed.append((rel, n, cjk_before))

    print(f"\n修复成功: {len(fixed)} 个")
    for rel, n, cjk in fixed:
        print(f"  OK  {rel}  (移除 {n} 个 BOM, CJK {cjk} 字符完好)")
    if failed:
        print(f"\n失败: {len(failed)} 个")
        for rel, why in failed:
            print(f"  XX  {rel}: {why}")
    print("\n备份位置: 各文件同目录 *.bak_bom")
    return 0


if __name__ == "__main__":
    sys.exit(main())
