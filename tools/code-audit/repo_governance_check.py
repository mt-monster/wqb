#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""repo_governance_check.py — 仓库治理的**唯一先行指标**：未跟踪的「源码类」文件数。

为什么需要它
------------
2026-10-06 治理复盘的核心结论：本仓库反复发生的资产损失都不是「提交丢了」，
而是**一批源码只以工作区未跟踪文件的形式存在**，于是任何一次 `git clean -fd`
或等价清理都会静默抹掉它们。已实证的事故：

- `tools/` 下 17 个被 AGENTS.md / tools/README.md / MEMORY 引用的工具从未入库
  → 清理后 `tools/*.py` 与 S11 基线 159 条对不上磁盘，`refs_scan.py`
  （迁移配方第 1 步的工具）也一并消失；
- `docs/experience/02_signal_patterns.md` 的 §10–§16 与
  `methodology_rules.json` 的 7 条规则（双轨同源的一体两面）同时缺失。

这两类损失的共同前兆是同一个数字：**未跟踪的源码类文件数 > 0**。
按「能自动发现的先行指标只留一个」的原则，本工具就盯这一个数，其余作辅助读数。

为什么不并入 audit_structure.py
------------------------------
两者的问题域不同：S1–S13 查的是**已入库内容的形状**（结构契约、路径、漂移），
全部只读 `git ls-files` 的世界。本工具查的是**尚未入库的东西**——即"下一次
清理会带走什么"。混在一起会让 S 系列的「只减不增」棘轮语义被搅浑。

判据
----
「源码类」扩展名 = .py .sh .ps1 .js .ts .sql .md .json .yaml .yml .toml .ini .cfg
运行期目录（logs/ cache/ results/ data/ attic/ selfcorr_quick_out/ __pycache__/ 等）
与 `git check-ignore` 判定为忽略的路径一律不计——那些是设计内产物，不是待入库资产。

用法
----
    python tools/code-audit/repo_governance_check.py            # 人类可读
    python tools/code-audit/repo_governance_check.py --json     # 机读
    python tools/code-audit/repo_governance_check.py --quiet    # 只给退出码

退出码：0 = 无未跟踪源码；1 = 存在未跟踪源码（"下次清理会带走 N 个文件"）；
        2 = 无法判定（不在 git 仓库 / git 不可用）。
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path


def _bootstrap_src() -> None:
    """把 `src/` 放上 sys.path：向上探测双标记，**与文件层数无关**
    （AGENTS.md §8 禁止新增 `parents[N]` / `dirname(dirname())` 这类层数硬编码）。
    """
    for parent in Path(__file__).resolve().parents:
        if (parent / "pyproject.toml").exists() and (parent / "src" / "wqb").is_dir():
            src = str(parent / "src")
            if src not in sys.path:
                sys.path.insert(0, src)
            return
    raise RuntimeError("仓库根未找到（向上未见 pyproject.toml + src/wqb 双标记）")


_bootstrap_src()

from wqb.paths import find_repo_root  # noqa: E402

#: 仓库根：层数无关解析（本文件可安全在 tools/ 主题间搬家）
REPO_ROOT = str(find_repo_root(__file__))

SOURCE_EXTS = {
    ".py", ".sh", ".ps1", ".js", ".mjs", ".ts", ".tsx", ".sql",
    ".md", ".json", ".yaml", ".yml", ".toml", ".ini", ".cfg",
}

#: 运行期 / 归档：其中的未跟踪文件是设计内产物，不计入先行指标
RUNTIME_DIRS = {
    "logs", "cache", "results", "data", "attic", "selfcorr_quick_out",
    "__pycache__", ".pytest_cache", ".venv", "node_modules", "research-data",
    "extensions", "outputs",
}

#: 预期长期存在未跟踪文件的路径前缀（外部数据包 / 浏览器扩展源，整目录 gitignore）
EXPECTED_UNTRACKED_PREFIXES = ()


def _git(*args: str) -> tuple[int, str]:
    try:
        r = subprocess.run(["git", *args], cwd=REPO_ROOT, capture_output=True,
                           text=True, encoding="utf-8", errors="replace", timeout=120)
    except (OSError, subprocess.SubprocessError):
        return 2, ""
    return r.returncode, r.stdout


def _in_runtime_dir(rel: str) -> bool:
    return any(part in RUNTIME_DIRS for part in rel.replace("\\", "/").split("/"))


def collect() -> dict:
    rc, out = _git("rev-parse", "--is-inside-work-tree")
    if rc != 0 or out.strip() != "true":
        return {"ok": False, "error": "不在 git 工作区里"}

    # 未跟踪 + 未被忽略：`--exclude-standard` 让 gitignore 自行过滤，避免重复造规则。
    # 再叠一层 RUNTIME_DIRS 兜底，用于「目录本身被 gitignore、但里面某项被手工 add」
    # 这类 gitignore 表达不了的情形。
    rc, out = _git("ls-files", "--others", "--exclude-standard", "-z")
    if rc != 0:
        return {"ok": False, "error": "git ls-files 失败"}
    untracked = [p for p in out.split("\0") if p]

    src, other = [], []
    for rel in untracked:
        ext = os.path.splitext(rel)[1].lower()
        if ext in SOURCE_EXTS and not _in_runtime_dir(rel):
            src.append(rel)
        else:
            other.append(rel)

    # 被忽略的源码类文件：不是"待入库资产"（设计内排除），但数量值得读一眼——
    # 整目录忽略（如旧的 DEU/reports/）曾把结论永久挡在库外，是本指标的历史成因。
    rc, out = _git("ls-files", "--others", "--ignored", "--exclude-standard", "-z")
    ignored_src = []
    if rc == 0:
        for rel in out.split("\0"):
            if rel and os.path.splitext(rel)[1].lower() in SOURCE_EXTS \
                    and not _in_runtime_dir(rel):
                ignored_src.append(rel)

    ahead, behind = {}, {}
    for remote in ("origin", "gitcode"):
        rc, _ = _git("rev-parse", "--verify", "-q", f"{remote}/main")
        if rc != 0:
            continue
        rc, out = _git("rev-list", "--left-right", "--count", f"{remote}/main...main")
        if rc == 0 and out.strip():
            b, a = out.split()
            behind[remote], ahead[remote] = int(b), int(a)

    rc, out = _git("tag", "-l", "preserve/*")
    preserve = [t for t in out.splitlines() if t.strip()]
    rc, out = _git("branch", "--format=%(refname:short)")
    danger = [b for b in out.splitlines() if b.startswith("wip/DANGER-")]

    return {
        "ok": True,
        "untracked_source": sorted(src),
        "untracked_source_count": len(src),
        "untracked_other_count": len(other),
        "ignored_source_count": len(ignored_src),
        "ignored_source_sample": sorted(ignored_src)[:15],
        "ahead": ahead,
        "behind": behind,
        "preserve_tags": len(preserve),
        "danger_branches": danger,
    }


def render(d: dict) -> str:
    if not d.get("ok"):
        return f"[repo_governance] 无法判定：{d.get('error')}"
    n = d["untracked_source_count"]
    lines = []
    lines.append("=" * 72)
    lines.append("★ 唯一先行指标：未跟踪的源码类文件 = %d" % n)
    lines.append("=" * 72)
    if n:
        lines.append("  含义：下次 `git clean -fd`（或任何等价清理）会带走这 %d 个文件。" % n)
        lines.append("  处置：判断该入库还是该 gitignore —— 不要放着不管。")
        for p in d["untracked_source"]:
            lines.append(f"    - {p}")
    else:
        lines.append("  含义：工作区里没有「只存在于磁盘」的源码 —— 清理不会再造成资产损失。")
    lines.append("")
    lines.append("--- 辅助读数 ---")
    lines.append(f"  未跟踪的非源码文件（运行产物等）：{d['untracked_other_count']}")
    lines.append(f"  被 gitignore 排除的源码类文件数：{d['ignored_source_count']}")
    if d["ignored_source_count"]:
        lines.append("    ⚠ 其中若有「结论/报告类」，说明它们被整目录规则挡住、永远落不了库：")
        for p in d["ignored_source_sample"]:
            lines.append(f"      · {p}")
    for r in sorted(set(d["ahead"]) | set(d["behind"])):
        lines.append(f"  相对 {r}/main：本地 main 领先 {d['ahead'].get(r, '?')} / "
                     f"落后 {d['behind'].get(r, '?')}（领先未推送，落后未拉取 → `git push {r} main`）")
    lines.append(f"  抢救点保留（preserve/* tag）：{d['preserve_tags']} 个")
    lines.append(f"  仍存在的 wip/DANGER-* 分支：{d['danger_branches'] or '无'}")
    return "\n".join(lines)


def main() -> int:
    ap = argparse.ArgumentParser(description="仓库治理先行指标：未跟踪源码类文件数")
    ap.add_argument("--json", action="store_true", help="输出机读 JSON")
    ap.add_argument("--quiet", action="store_true", help="不打印，只用退出码")
    ap.add_argument("--warn", action="store_true",
                    help="只打一行摘要且**恒 exit 0**（给 pre-commit 当告警用：未跟踪文件是"
                         "情境性的——本机常态有多条并行会话，拿它卡提交只会逼人 --no-verify）")
    args = ap.parse_args()

    d = collect()
    if args.warn:
        if not d.get("ok"):
            print("[governance] 无法判定（不在 git 仓库 / git 不可用）", file=sys.stderr)
            return 0
        n = d["untracked_source_count"]
        if n:
            print(f"[governance] WARN: 未跟踪源码类文件 = {n} 个 —— 下次 `git clean -fd` 会"
                  f"**永久**带走它们（从未进 git，救不回）。清单："
                  f"python tools/code-audit/repo_governance_check.py")
        else:
            print("[governance] OK: 无未跟踪源码类文件")
        return 0
    if not args.quiet:
        print(json.dumps(d, ensure_ascii=False, indent=1) if args.json else render(d))
    if not d.get("ok"):
        return 2
    return 1 if d["untracked_source_count"] else 0


if __name__ == "__main__":
    sys.exit(main())
