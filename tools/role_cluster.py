# -*- coding: utf-8 -*-
"""职责聚类 + 跨文件重复逻辑检测（只读）。

职责聚类：按函数名的语义后缀/前缀分组计数 —— 组的数量 = 该文件承担的关注点数。
  一个健康模块通常落在 1–2 个组；组数越多，职责越杂。

重复检测：把每个函数体归一化后取 token 指纹（结构指纹），跨文件比对，
  输出重复/近似重复的簇。用于识别「同一段逻辑被抄到 N 个 skill 副本」。
"""
from __future__ import annotations

import ast
import hashlib
import os
import re
import sys
from collections import defaultdict
from typing import Dict, List, Tuple

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKIP_DIRS = {".git", "__pycache__", ".venv", "venv", "node_modules",
             ".pytest_cache", ".mypy_cache", "site-packages"}

#: 职责组 → 触发关键词（按优先级从特殊到通用匹配）
ROLE_RULES: List[Tuple[str, Tuple[str, ...]]] = [
    ("门禁/准入判定", ("gate", "guard", "check_fail", "preflight", "verdict", "admit", "qualif")),
    ("体检/覆盖检查", ("coverage", "inspect", "prescreen", "health", "audit", "scan_fields")),
    ("结果解析/摘要", ("extract", "parse", "summary", "summarize", "tail", "digest")),
    ("引用/路径解析", ("resolve", "locate", "find_", "locator")),
    ("台账读写/持久化", ("upsert", "persist", "save", "load", "write_", "read_", "store", "ledger", "ckpt")),
    ("进程/子进程执行", ("popen", "subprocess", "run_child", "wait_and_collect", "spawn", "exec")),
    ("提交/配额", ("submit", "quota", "shipment")),
    ("回测批处理", ("batch", "multisim", "sim_")),
    ("评审/评级", ("review", "score", "judge", "rank", "grade")),
    ("选波/表达式生成", ("wave", "expression", "expr", "build_", "generate", "template")),
    ("CLI/参数解析", ("cmd_", "main", "argv", "cli", "argparse")),
    ("相关性/风控", ("corr", "prod_", "self_corr", "risk")),
]


def role_of(name: str) -> str:
    n = name.lower()
    for role, keys in ROLE_RULES:
        for k in keys:
            if k in n:
                return role
    return "其他/胶水"


def iter_py(root: str):
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for fn in filenames:
            if fn.endswith(".py"):
                yield os.path.join(dirpath, fn)


def analyze_roles(path: str) -> Dict[str, object]:
    try:
        src = open(path, encoding="utf-8", errors="replace").read()
        tree = ast.parse(src)
    except Exception:
        return {}
    names: List[str] = []

    def walk(body):
        for n in body:
            if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)):
                names.append(n.name)
            elif isinstance(n, ast.ClassDef):
                names.append(n.name)
                walk(n.body)
    walk(tree.body)

    groups = defaultdict(list)
    for n in names:
        groups[role_of(n)].append(n)
    return {
        "path": os.path.relpath(path, ROOT).replace("\\", "/"),
        "n_units": len(names),
        "n_roles": len(groups),
        "roles": {k: len(v) for k, v in sorted(groups.items(), key=lambda x: -len(x[1]))},
        "detail": {k: v for k, v in groups.items()},
    }


# ---------------------------------------------------------------- 重复检测
def norm_body(fn_src: str) -> str:
    """去掉注释/空行/多余空白，保留结构。"""
    fn_src = re.sub(r"#.*", "", fn_src)
    lines = [ln.strip() for ln in fn_src.splitlines() if ln.strip()]
    return " ".join(lines)


def dup_fingerprints(min_lines: int = 30):
    """对每个 >= min_lines 的函数取整体指纹（含归一化体），跨文件聚类。"""
    clusters: Dict[str, List[str]] = defaultdict(list)
    for p in iter_py(ROOT):
        try:
            src = open(p, encoding="utf-8", errors="replace").read()
            tree = ast.parse(src)
        except Exception:
            continue
        lines = src.splitlines()
        for n in ast.walk(tree):
            if not isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)):
                continue
            seg = (n.end_lineno or n.lineno) - n.lineno + 1
            if seg < min_lines:
                continue
            body = "\n".join(lines[n.lineno - 1:(n.end_lineno or n.lineno)])
            fp = hashlib.md5(norm_body(body).encode("utf-8")).hexdigest()
            rel = os.path.relpath(p, ROOT).replace("\\", "/")
            clusters[fp].append(f"{rel}::{n.name}({seg}L)")
    return {k: v for k, v in clusters.items() if len(v) > 1}


def main() -> int:
    targets = sys.argv[1:] or [
        "src/wqb/workflow/nodes/campaign.py",
        "Claude/skills/wq-brain-campaign-toolkit/scripts/pipeline.py",
        "Claude/skills/wq-brain-campaign-toolkit/scripts/gate.py",
        "src/wqb/workflow/nodes/gem.py",
        "tools/campaign_intel.py",
        "Claude/skills/wq-brain-campaign-toolkit/scripts/build_wave.py",
        "wqb_db_mcp.py",
    ]
    print("=" * 96)
    print("职责聚类")
    print("=" * 96)
    for t in targets:
        p = os.path.join(ROOT, t)
        if not os.path.isfile(p):
            print(f"[skip] {t}")
            continue
        r = analyze_roles(p)
        print(f'\n{r["path"]}')
        print(f'  单元数 {r["n_units"]}   职责组数 {r["n_roles"]}')
        for k, v in r["roles"].items():
            print(f'    {k:<18}{v:>3}')

    print()
    print("=" * 96)
    print("跨文件重复函数簇（>=30 行且指纹相同）")
    print("=" * 96)
    dups = dup_fingerprints()
    print(f"重复簇数：{len(dups)}")
    shown = sorted(dups.values(), key=lambda v: -len(v))[:18]
    for members in shown:
        print(f'\n  [{len(members)} 份]')
        for m in members[:6]:
            print(f"     {m}")
        if len(members) > 6:
            print(f"     ... 另 {len(members)-6} 份")
    return 0


if __name__ == "__main__":
    sys.exit(main())
