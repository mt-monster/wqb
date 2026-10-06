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

#: 预期长期存在未跟踪文件的路径前缀（外部数据包 / 浏览器扩展源 / skill 安装位镜像）。
#: **与 `docs/governance/untracked_allowlist.md` §1 逐条对齐**（2026-10-06 治理评审 P1-8）：
#: 那个常量曾在 `= ()` 处声明后从未被使用，文档却自述「执行者 = 本脚本」，
#: 于是「文档写了但流程不认」——同一件事两处各说一套。现在两边真接上了，
#: 对齐由 `tests/unit/07_docs_skills/test_untracked_allowlist.py` 机械守护。
#: 口径：本处是**代码可执行投影**（单一事实源），文档是给人看的说明；改一处必须改两处。
EXPECTED_UNTRACKED_PREFIXES = (
    "logs/", "cache/", "results/", "data/", "attic/",
    "research-data/", "extensions/", "selfcorr_quick_out/",
    "outputs/", ".claude/", ".codex/", ".cline/", ".agents/",
)

#: 抢救点 / 事故快照里「main 没有」的源码归档位置说明（读数只供裁决，不自行判定）
ADJUDICATION_DOC = "docs/governance/snapshot_adjudication.md"

#: 参算「源码类」的顶层目录（跳运期产物目录后还要这一层，否则 `logs/*.json` 会被当成资产）
CODE_ROOTS = ("src", "tools", "tests", "world-quant-brain-mcp", "Claude", "docs", "tracking", "reports", "output_report")


def _git(*args: str) -> tuple[int, str]:
    try:
        r = subprocess.run(["git", *args], cwd=REPO_ROOT, capture_output=True,
                           text=True, encoding="utf-8", errors="replace", timeout=120)
    except (OSError, subprocess.SubprocessError):
        return 2, ""
    return r.returncode, r.stdout


def _in_runtime_dir(rel: str) -> bool:
    return any(part in RUNTIME_DIRS for part in rel.replace("\\", "/").split("/"))


def _in_allowlisted_prefix(rel: str) -> bool:
    """是否落在文档 §1「允许长期未跟踪」的路径下（白名单命中）。"""
    p = rel.replace("\\", "/")
    return any(p.startswith(x) for x in EXPECTED_UNTRACKED_PREFIXES)


def _snapshot_refs() -> list:
    """参算「抢救点独有文件」的 ref 集：`preserve/*` + `backup/*` tag，外加滞留下的 `wip/*` 分支。

    ⚠ annotated tag 必须用 `<tag>^{commit}` / `ls-tree <tag>` 解引用后比 —— `git rev-parse <tag>`
    返回的是 **tag 对象**的 sha，不是 commit sha（本日实测差点因此误判「tag 与分支不同指一个 commit」）。
    `wip/*` 仍入集（2026-10-06 防御保留）：两条 `wip/DANGER-*` 已降为 tag-only 并删除，
    但「会话新造一条长期 wip 分支并在其上存未入库内容」是本仓反复出现过的形状，只扫 tag
    会让这种新快照永远不进台账（`branch_policy.md` §1 现约定此集应为空，由 `danger_branches` 读数盯）。
    """
    refs: list[str] = []
    rc, out = _git("tag", "-l", "preserve/*", "backup/*")
    if rc == 0:
        refs += [t.strip() for t in out.splitlines() if t.strip()]
    rc, out = _git("branch", "--format=%(refname:short)")
    if rc == 0:
        refs += [b for b in out.splitlines() if b.startswith("wip/")]
    return refs


def snapshot_unique_sources(main_ref: str = "main") -> list:
    """只存在于各抢救点 / 事故快照、而 `main` 里没有的**源码类**路径（去重排序）。

    为什么需要这一类读数（2026-10-06 治理评审 P2-7）：S1–S14 与本工具的先行指标都只看
    **工作区与 main**，看不见「对象库里有、主干上没有」的那批件。实测抢救点
    `4910e65` 与 `05b64a6` 合计独有 90+ 个 src/tools/tests 文件（含 `src/wqb/semantic_ledger.py`、
    `tests/unit/09_core/test_paths.py`），其中绝大部分无人裁决 —— 不读数就是「无台账、无裁决、无闸」。

    口径：每个 ref 都取**两条腿** —— 受跟踪树（`ls-tree -r <ref>`）与未跟踪父提交
    （`<ref>^3`，stash 式快照才有）。只取受跟踪部分会漏掉关键依赖（本仓已踩过）。
    行尾归一不参与比较（只比路径集）。
    """
    rc, out = _git("ls-tree", "-r", "--name-only", main_ref)
    if rc != 0:
        return []
    in_main = set(out.splitlines())

    found = set()
    for ref in _snapshot_refs():
        for suffix in ("", "^3"):  # 未跟踪父提交不存在时 git 报错，忽略即可
            rc, out = _git("ls-tree", "-r", "--name-only", f"{ref}{suffix}")
            if rc != 0:
                continue
            for p in out.splitlines():
                if not p or p in in_main:
                    continue
                ext = os.path.splitext(p)[1].lower()
                if ext not in SOURCE_EXTS or _in_runtime_dir(p):
                    continue
                if p.split("/", 1)[0] not in CODE_ROOTS:
                    continue
                found.add(p)
    return sorted(found)


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

    # 白名单命中（未跟踪且落在文档 §1 的路径里）：设计内，不算欠债。
    # 它们已被 `--exclude-standard`（gitignore）与 RUNTIME_DIRS 两道隔掉，
    # 这里只作**可观测性**：让读数能回答「为何不卡我」。文档↔代码一致性由守护测试管。
    allowed_hits = sorted(p for p in untracked if _in_allowlisted_prefix(p))

    # 抢救点独有源码（对象库里有、主干上没有）——必须有人逐件三态裁决，
    # 否则就是一批「没人知道为什么留着」的债（裁决表见 ADJUDICATION_DOC）。
    snap = snapshot_unique_sources()

    return {
        "ok": True,
        "untracked_source": sorted(src),
        "untracked_source_count": len(src),
        "untracked_other_count": len(other),
        "allowed_untracked_count": len(allowed_hits),
        "allowed_untracked_prefixes": list(EXPECTED_UNTRACKED_PREFIXES),
        "ignored_source_count": len(ignored_src),
        "ignored_source_sample": sorted(ignored_src)[:15],
        "ahead": ahead,
        "behind": behind,
        "preserve_tags": len(preserve),
        "danger_branches": danger,
        "snapshot_unique_source_count": len(snap),
        "snapshot_unique_sources": snap,
        "adjudication_doc": ADJUDICATION_DOC,
    }


def snapshot_unique_records(main_ref: str = "main") -> list:
    """同 `snapshot_unique_sources()`，但返回带 blob 的记录（裁决台账需要内容比较）。

    每条：`{"path", "blob", "refs"}`。blob = 该件在快照里的 blob id；
    同名件在 main 的哪个路径上由调用方自查（路径重组 vs 内容分叉得靠 blob 相等才能区分）。
    ⚠ 只同算法才能比：本仓是 sha1 仓库，快照与 main 的 blob 同一口径；
    **不要拿 blob id 去和文件层的 SHA-256 哈希互比**（本仓曾因此误判出「三条血统」）。
    """
    rc, out = _git("ls-tree", "-r", "--name-only", main_ref)
    if rc != 0:
        return []
    in_main = set(out.splitlines())

    found: dict[str, dict] = {}
    for ref in _snapshot_refs():
        for suffix in ("", "^3"):
            rc, out = _git("ls-tree", "-r", f"{ref}{suffix}")
            if rc != 0:
                continue
            for line in out.splitlines():
                # 形式：`<mode> <type> <sha>\t<path>`
                meta, _, path = line.partition("\t")
                parts = meta.split()
                if not path or len(parts) < 3 or parts[1] != "blob":
                    continue
                if path in in_main:
                    continue
                ext = os.path.splitext(path)[1].lower()
                if ext not in SOURCE_EXTS or _in_runtime_dir(path):
                    continue
                if path.split("/", 1)[0] not in CODE_ROOTS:
                    continue
                rec = found.setdefault(path, {"path": path, "blob": parts[2], "refs": []})
                tag = f"{ref}{suffix}"
                if tag not in rec["refs"]:
                    rec["refs"].append(tag)
    return [found[k] for k in sorted(found)]


def main_blob_index(main_ref: str = "main") -> dict:
    """`{文件名: [(路径, blob), …]}` —— 给「同名件是否只是搬了目录」提供查表。"""
    rc, out = _git("ls-tree", "-r", main_ref)
    idx: dict[str, list] = {}
    if rc != 0:
        return idx
    for line in out.splitlines():
        meta, _, path = line.partition("\t")
        parts = meta.split()
        if not path or len(parts) < 3 or parts[1] != "blob":
            continue
        idx.setdefault(os.path.basename(path), []).append((path, parts[2]))
    return idx


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
    lines.append(f"  未跟踪的非源码文件（运行产物等）：{d['untracked_other_count']}"
                 f"（其中落在文档 §1 白名单路径下、属设计内的：{d.get('allowed_untracked_count', 0)}）")
    lines.append(f"  被 gitignore 排除的源码类文件数：{d['ignored_source_count']}")
    if d["ignored_source_count"]:
        lines.append("    ⚠ 其中若有「结论/报告类」，说明它们被整目录规则挡住、永远落不了库：")
        for p in d["ignored_source_sample"]:
            lines.append(f"      · {p}")
    for r in sorted(set(d["ahead"]) | set(d["behind"])):
        lines.append(f"  相对 {r}/main：本地 main 领先 {d['ahead'].get(r, '?')} / "
                     f"落后 {d['behind'].get(r, '?')}（领先未推送，落后未拉取 → `git push {r} main`）")
    lines.append(f"  抢救点保留（preserve/* tag）：{d['preserve_tags']} 个")
    # 2026-10-06：两条 `wip/DANGER-*` 已降为 tag-only（对象由同名 tag 持有），
    # 所以这一栏**预期为空**。非空 = 有人又造了长期 wip 分支（违反 branch_policy §1），
    # 而不是「一切正常」——因此它不是状态汇报，是欠债读数。
    danger = d["danger_branches"]
    lines.append(f"  长期滞留的 wip/DANGER-* 分支（应为空，§1 约定当日清）："
                 f"{danger if danger else '无'}")
    n_snap = d.get("snapshot_unique_source_count", 0)
    lines.append(f"  ★ 抢救点独有源码（对象库里有、main 没有）：{n_snap} 个")
    if n_snap:
        doc = d.get("adjudication_doc", "")
        lines.append(f"    含义：这批件只活在本地 tag 上。未逐件裁决前，它们既是「可取回的资产」")
        lines.append(f"          也是「将来会被遗忘的债」（全量清单：--json 取 snapshot_unique_sources）。")
        lines.append(f"    处置：在 {doc} 里逐件标「恢复 / 有意放弃 / 运行产物」三态之一。")
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
