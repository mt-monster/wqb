# -*- coding: utf-8 -*-
"""高置信度死代码侦察（只读，不删任何东西）。

算法（高效）：先把全仓文本一次性 token 化成全局 Counter，再对每个私有函数名查引用数。
引用数 = 全局词频 - 定义次数（定义行本身含 1 次）。<=0 → 候选死代码。

仅作候选清单；同名多定义、getattr 动态调用、__init__ re-export、框架钩子都可能误报，
删除前必须人工复核。
"""
from __future__ import annotations

import ast
import os
import re
import sys
from collections import Counter, defaultdict

SCAN_CODE_ROOTS = ["src/wqb", "tools"]
EXCLUDE_DIR = {"__pycache__", ".venv", "venv", ".git", "node_modules", "site-packages", "attic", "cache"}
TEXT_EXT = {".py", ".md", ".json", ".txt", ".yaml", ".yml", ".toml"}
DUNDER = re.compile(r"^__.*__$")
TOKEN = re.compile(r"[A-Za-z_][A-Za-z0-9_]*")


def iter_files(root):
    for dp, dn, fn in os.walk(root):
        dn[:] = [d for d in dn if d not in EXCLUDE_DIR]
        for f in fn:
            yield os.path.join(dp, f)


def collect_defs():
    defs = []
    for root in SCAN_CODE_ROOTS:
        if not os.path.isdir(root):
            continue
        for p in iter_files(root):
            if not p.endswith(".py"):
                continue
            try:
                tree = ast.parse(open(p, encoding="utf-8", errors="replace").read())
            except SyntaxError:
                continue
            for node in ast.walk(tree):
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    nm = node.name
                    if nm.startswith("_") and not DUNDER.match(nm):
                        defs.append((nm, p.replace("\\", "/"), node.lineno))
    return defs


def build_counter():
    cnt = Counter()
    for p in iter_files("."):
        if os.path.splitext(p)[1].lower() in TEXT_EXT:
            try:
                text = open(p, encoding="utf-8", errors="replace").read()
            except OSError:
                continue
            cnt.update(TOKEN.findall(text))
    return cnt


def main():
    defs = collect_defs()
    print(f"私有函数定义 {len(defs)} 个", file=sys.stderr)
    by_name = defaultdict(list)
    for nm, f, ln in defs:
        by_name[nm].append((f, ln))

    cnt = build_counter()
    print(f"全仓 token 化完成，唯一标识符 {len(cnt)} 个", file=sys.stderr)

    zero_unique, zero_multi = [], []
    for nm, locs in sorted(by_name.items()):
        n_defs = len(locs)
        n_ref = cnt.get(nm, 0) - n_defs
        if n_ref <= 0:
            (zero_unique if n_defs == 1 else zero_multi).append((nm, locs))

    print(f"\n=== 高置信度死代码候选（唯一定义 + 零引用）：{len(zero_unique)} 个 ===")
    for nm, locs in zero_unique:
        f, ln = locs[0]
        print(f"  {nm}   @ {f}:{ln}")
    print(f"\n=== 同名多定义（零引用但需人工区分哪个副本死）：{len(zero_multi)} 个 ===")
    for nm, locs in zero_multi:
        loc_s = "; ".join(f"{f}:{ln}" for f, ln in locs)
        print(f"  {nm}   @ {loc_s}")


if __name__ == "__main__":
    main()
