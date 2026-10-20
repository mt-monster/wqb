#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""把仓库 Claude/skills/ 同步到 Agent 实际加载的全部 skill 安装位。

背景（2026-09-06 审计）：仓库副本与 `~/.claude/skills` 已漂移约两周 ——
`brain-make-some-gem` 仓库侧 last_verified=2026-09-05，安装位停在 2026-08-22；
`wq-brain-ra-pipeline` 仓库侧已修正 `check_expr_against_inspect` 的落点路径
并补了整链执行小节，安装位仍是旧文。于是 Agent 读的是旧 SOP，而回归测试
读的是新文，两边都"自洽"，问题只在运行时显形。

根因曾是 `install_now.py` 的 `if target_path.exists(): skip` —— 已装的 skill
永不更新，加上它的源目录 `~/mnt/skills` 在本机根本不存在，等于完全失效。

2026-09-10 审计补强：此前本脚本**只同步单个目标**（`resolve_install_root()` 取
首个命中），于是 `~/.codex/skills` / `~/.workbuddy/skills` 等不在同步链上的宿主
反复分叉——09-08 修过一次，09-10 又复发（ra-pipeline 落后 67 行）。现改为**多目标
同步**：自动枚举全部受维护的安装位，逐个同步 + 逐个校验。

    python tools/sync_skills.py --check     # 只报告漂移，任一目标有漂移则 exit 1（CI/单测用）
    python tools/sync_skills.py --dry-run   # 打印将要执行的动作，不写盘
    python tools/sync_skills.py             # 同步全部安装位（已关闭项除外）
    python tools/sync_skills.py --target ~/.codex/skills --target ~/.workbuddy/skills
    python tools/sync_skills.py --prune-orphans            # 只列出安装位孤儿（仓库没有的顶层条目）
    python tools/sync_skills.py --prune-orphans --apply    # 归档孤儿到 attic/sync_orphans_<date>/

方向是单向的：**仓库是源，安装位是派生物**。安装位的本地修改会被覆盖，
要改 skill 请改仓库副本再同步。

2026-10-20 用户裁定不再维护 `~/.cursor/skills`：登记在 `DISABLED_INSTALL_ROOTS`，
自动枚举与 `--target` 都会拒绝。只清空目录内容不够 —— 下一次同步会回填。

⚠ 单向同步**不会传播删除**：仓库里删掉一个 skill，安装位的副本会原地留下，
被 `prune_orphans` 分成 protected / user-native / 可归档三类。其中 user-native 的
判据是「仓库全部历史零提交」，而「建了又删、从未提交」的 skill 也零提交 ⇒ 会被误判成
宿主原生而永久跳过。这类**已裁定退役**的 skill 必须显式登记进 `RETIRED_SKILLS`
（登记即优先于 native 判定，归档到 attic 并写下裁定依据）。删仓库 skill 时同批登记。
"""
from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path
from typing import List, Optional, Tuple


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
REPO_ROOT = find_repo_root(__file__)
SOURCE = REPO_ROOT / "Claude" / "skills"

#: 明确不再维护的安装位 → 关闭原因。只影响**同步面**，不改
#: `wqb.workflow._common._skill_roots()` 的运行时解析顺序（目录不存在时自然跳过）。
#: 2026-10-20 用户裁定：不需要 Cursor 下的 skill 副本。只清空目录内容不够 ——
#: 实测清空 6 分钟后被一次 `sync_skills.py` 回填 51 项；必须在同步源头关掉。
DISABLED_INSTALL_ROOTS = {
    Path(os.path.expanduser("~/.cursor/skills")).resolve(): "用户 2026-10-20 指定不再维护 Cursor 安装位",
}

#: 不参与同步的产物/缓存（与 .gitignore 的 Claude/skills 规则同口径）
IGNORE_DIRS = {"__pycache__", "outputs", "output_report", "processed_templates", ".git"}
IGNORE_SUFFIXES = (".pyc", ".pyo", ".log")     # `.log`：运行时日志（vendored ace_lib 一 import 就在 CWD 建 ace.log），.gitignore 同口径
IGNORE_NAMES = {"parsetab.py", "parser.out"}


def _is_secret_file(name: str) -> bool:
    """密钥/凭据类本地文件（`.env`、`.arxiv_llm.env`、`.env.local` …）：只留在源位，不复制到安装位。

    `*.env.example` / `*.example` / `config.example.json` 是模板，照常同步。skills 审查 X-15：skill 目录内的 key 文件不得被同步扩散。
    `config.json` 同样按凭据文件处理（`.gitignore` 把 `**/config.json` 归在「Secrets / Credentials」下；GEM 的
    `headless_runner/config.json` 与 feature-implementation 的 `config.json` 里放 BRAIN 账号 / LLM 密钥）——它只留在
    用户自建的那一处：安装位里已有的不会被覆盖或删除，源位里若有则不会被复制到其它安装位。
    """
    if name.endswith(".example") or name == "config.example.json":
        return False
    return name == ".env" or name.endswith(".env") or name.startswith(".env.") or name == "config.json"


def _is_ignored(rel: Path) -> bool:
    if any(part in IGNORE_DIRS for part in rel.parts):
        return True
    if rel.name in IGNORE_NAMES or rel.suffix in IGNORE_SUFFIXES:
        return True
    if ".bak_" in rel.name:
        return True
    if _is_secret_file(rel.name):
        return True
    return False


def _candidate_roots() -> List[Path]:
    """复用 workflow 的解析顺序（`wqb.workflow._common._skill_roots()`）。"""
    sys.path.insert(0, str(REPO_ROOT / "src"))
    try:
        from wqb.workflow._common import _skill_roots
        raw = _skill_roots()
    except Exception:
        # 兜底顺序必须与 wqb.workflow._common._skill_roots() 同序（见该文件注释）：
        # .cline / .agents 是 Cline Desktop/CLI 的两个全局安装位（2026-10-03 补，
        # 取自 Cline dist/lib.mjs 的 yYt() 搜索链，不是猜的）。
        raw = (
            os.environ.get("WQ_SKILLS_DIR") or "",
            os.path.expanduser("~/.claude/skills"),
            os.path.expanduser("~/.codex/skills"),
            os.path.expanduser("~/.cline/skills"),
            os.path.expanduser("~/.agents/skills"),
            os.path.expanduser("~/.trae-cn/skills"),
            os.path.expanduser("~/.qoder-cn/skills"),
            os.path.expanduser("~/.cursor/skills"),
            os.path.expanduser("~/.workbuddy/skills"),
        )
    return [Path(r) for r in raw if r]


def _is_repo_related(candidate: Path) -> bool:
    """安装位解析结果与仓库存在「相同 / 祖先 / 子孙」三种危险关系之一。

    命中即危险：同步会把 `Claude/skills/<name>/` 逐个铺成 `<安装位>/<name>/`，
    于是**仓库内长出整棵技能树**（`wq-brain-ra-usa/SKILL.md`、`alpha-expression-verifier/` …）。

    实测复发三次，前两次（2026-10-14）是 `WQ_SKILLS_DIR` 被指到**仓库根**；
    第三次（2026-10-17 22:50）是安装位被指到**仓库内的某个子目录**，长出
    `<repo>/wq-brain-ra-usa/`（466 件、48 个子目录、与 `Claude/skills` 同源的完整副本）。
    ⇒ 只判「相同 / 祖先」拦不住第三种，必须把**子孙**一并纳入。
    见 AGENTS.md §8.13 命名规范第 6 条。

    为什么连子孙也要拦：安装位落在仓库内任意深处，都会把技能树铺进工作树，
    污染 `git status`、被后来者误当「在用的技能源」，且因未追踪而对取 git 面的守卫失明。
    """
    try:
        resolved = candidate.resolve()
    except OSError:
        return False
    repo = REPO_ROOT.resolve()
    if resolved == repo:
        return True            # 相同：铺成仓库根顶层杂物
    if repo.is_relative_to(resolved):
        return True            # 祖先：仓库是安装位的子目录
    if resolved.is_relative_to(repo):
        return True            # 子孙：安装位在仓库内
    return False


def _is_repo_root_or_ancestor(candidate: Path) -> bool:
    """向后兼容别名 —— 语义已扩展为 `_is_repo_related`（含子孙判定）。"""
    return _is_repo_related(candidate)


def _disabled_reason(candidate: Path) -> Optional[str]:
    """安装位是否被显式关闭（同步面）。关闭项仍可被运行时解析，但不再写入。

    `--target ~/.cursor/skills` 这种波浪号写法也要拦住 —— 不展开会变成字面量
    `~` 目录，既匹配不到登记项，又可能真在 CWD 下建出一个 `~` 目录。
    """
    try:
        resolved = candidate.expanduser().resolve()
    except OSError:
        return None
    return DISABLED_INSTALL_ROOTS.get(resolved)


def resolve_install_roots() -> List[Path]:
    """全部已存在的 skill 安装位（按解析顺序，去重，排除仓库源自身与已关闭项）。

    与 `wqb.workflow._common._skill_roots()` 同源，避免"同步到一个没人读的
    目录"。2026-09-10 起返回**列表**（多目标），不再只取首个命中。
    `DISABLED_INSTALL_ROOTS` 中的安装位不参与同步（用户显式裁定不再维护）。
    """
    source_resolved = SOURCE.resolve()
    seen, ordered, blocked, aliased, disabled = set(), [], [], [], []
    for candidate in _candidate_roots():
        try:
            resolved = candidate.resolve()
        except OSError:
            continue
        if resolved == source_resolved:
            continue
        reason = DISABLED_INSTALL_ROOTS.get(resolved)
        if reason:
            if candidate.is_dir():
                disabled.append(f"{candidate}（{reason}）")
            continue
        if resolved in seen:
            # 不是"少同步了一个"，是**同一个物理目录的另一个入口**：Windows 目录
            # junction 的 `is_symlink()` 恒 False、但 `resolve()` 会跟过去。
            # 实测 2026-10-15：`~/.qoder-cn/skills` → `~/.claude/skills`，故宿主数 7、
            # 物理目标 6。静默去重会让人以为漏了一个安装位而去"修"一个非缺陷。
            aliased.append(f"{candidate} -> {resolved}")
            continue
        if _is_repo_related(candidate):
            blocked.append(candidate)
            continue
        if candidate.is_dir():
            seen.add(resolved)
            ordered.append(candidate)
    if blocked:
        # 静默丢弃会让人以为"同步成功了 8 个目标"，其实少了一个 —— 顶屏说清楚。
        print(f"[sync_skills] ⚠ 已拒绝 {len(blocked)} 个安装位（与仓库相同/祖先/子孙三种关系之一，"
              f"同步会在工作树里长出整棵技能树）：{[str(b) for b in blocked]}", file=sys.stderr)
    if aliased:
        print(f"[sync_skills] 去重 {len(aliased)} 个安装位入口（junction / 同物理目录，"
              f"已由前序目标覆盖）：{aliased}", file=sys.stderr)
    if disabled:
        print(f"[sync_skills] 跳过 {len(disabled)} 个已关闭的安装位（不同步）：{disabled}",
              file=sys.stderr)
    return ordered


def resolve_install_root() -> Optional[Path]:
    """兼容旧调用：返回首个安装位（多目标请用 `resolve_install_roots()`）。"""
    roots = resolve_install_roots()
    return roots[0] if roots else None


#: 孤儿清理白名单：这些顶层条目不参与 prune。
#: 判据：① 非 WQ 全局技能（由 WorkBuddy / 其他项目独立维护，本仓库无源）
#:       ② 2026-09-10 审计 P2-1 已裁决"不处置"的废弃 skill。
#: 以 "." 开头的条目（WorkBuddy 迁移标记等）由代码统一放行，无需在此登记。
PROTECTED_ORPHANS = {
    "code-optimization", "dead-code-cleanup", "gold-analysis", "jin10-news",
    "brain-enhance-template",  # 已废止，裁决保留原位（P2-1）
    # 2026-10-08 新增：宿主原生 skill（仓库全部历史里从未出现过，见 `_never_in_repo_history`）。
    # 它们不是「本仓改名前的遗留」，归档等于把宿主上正在用的 skill 摘掉。
    "wq-batch-dispatch-safety", "wq-operator-playbook-by-gate",
    "wq-post-rank-clip-break-prod-wall", "wq-prod-lever-self-lock-guard",
    "wq-wave-preflight-dispatch", "wq-window-valley-break-prod-wall",
    "wqb-test-failure-triage",
}


def _never_in_repo_history(name: str) -> bool:
    """该顶层条目在**仓库全部历史**里都没出现过 ⇒ 宿主原生 skill，不是本仓遗留。

    2026-10-08 实证：安装位 `~/.workbuddy/skills` 下 7 个条目在
    `git log --all -- Claude/skills/<name>` 里**零提交** —— 它们由用户级会话直接创建、
    与仓库无源流关系。把它们当「孤儿」归档（`--apply` 是**移动**）＝ 宿主当场失去
    在用 skill，代价远大于留着占位；而「本仓改名前的旧目录」必然有历史，仍会被清理。

    ⚠ 已知失效方向（2026-10-15 实证）：「在同一个未提交的工作区状态里建了又删」的
    skill 同样是零提交 ⇒ 会被本函数误判成宿主原生而永久跳过清理。这类条目必须显式
    登记进 `RETIRED_SKILLS`，否则裁定退役只在仓库侧生效、安装位上留着已作废的副本。
    """
    try:
        rel = SOURCE.relative_to(REPO_ROOT)
    except ValueError:
        return False
    r = subprocess.run(["git", "log", "--all", "--oneline", "-1", "--",
                        f"{rel.as_posix()}/{name}"],
                       cwd=str(REPO_ROOT), capture_output=True, text=True)
    # 查不动（非 git 仓库 / git 缺失）时按「可能有历史」处理 —— 保守，不扩大清理面。
    return r.returncode == 0 and not (r.stdout or "").strip()


#: 已裁定**退役**的 skill 名 → 裁定依据（谁裁的 / 何时 / 由谁承接）。
#: 为什么需要这张表：见 `_never_in_repo_history` 的 ⚠ —— 零提交既可能是「宿主原生」，
#: 也可能是「本仓建了又删、从未提交」。前者绝不能清（摘掉在用 skill），后者必须清
#: （留着就是同一套方法论以两个 skill 名并存，Agent 按名字调到已作废的那份）。
#: 两种形态在 git 里**不可区分**，所以由本表提供人工反证：登记即「有裁定、该归档」，
#: 优先于 native 判定；归档仍是**移动**到 `attic/sync_orphans_<date>/<host>/`，可回滚。
#: 纪律：删一个仓库 skill 时若它可能已被同步到安装位，**同批登记到这里**。
RETIRED_SKILLS = {
    "wq-brain-gatebreak-kor": (
        "2026-10-15 22:20 用户裁定：KOR「字段体检 → 归因 → 破闸」工作流改由区域 skill "
        "wq-brain-ra-kor（src/wqb/profiles/render.py 的 KOR 特化分支生成）承载。仓库侧副本"
        "当天已删；其比 ra-kor 更丰富的片段已合并进 ra-kor 的 SKILL.md 与 "
        "references/_kor-gatebreak-evidence.md（单腿 S0.89、离线包 1126/1333 退化、pow≥0.9 "
        "跳变）。裁定记录：.workbuddy/memory/2026-10-15.md。"
    ),
}


def prune_orphans(target: Path, apply: bool = False) -> List[str]:
    """列出（并可选归档）安装位里"仓库根本没有的顶层条目"。

    只增不删是安全默认（历史产物不该被静默清掉），但长期会堆积改名前的旧
    skill 目录与一次性脚本 —— 2026-09-11 审计手工清了 21 项，说明缺口真实存在。
    故提供显式入口：默认**只打印**，`--apply` 才移入
    `<repo>/attic/sync_orphans_<YYYYMMDD>/<host>/`（移动而非删除，可回滚）。

    判据是"顶层条目在仓库完全不存在"，而非"子文件有差异"：后者
    （如 `brain-forum-browse/data/agent_profile.json`、GEM 的 `data/*_idea_*.json`）
    是运行时产物，属正常，**不得**当孤儿清理。
    """
    if not target.is_dir():
        return []
    src_top = {p.name for p in SOURCE.iterdir()}
    candidates = [
        entry.name for entry in sorted(target.iterdir(), key=lambda p: p.name)
        if entry.name not in src_top
        and not entry.name.startswith(".")
        and "migration" not in entry.name.lower()   # WorkBuddy 迁移标记（_bm_skillid_migration.json 等）
    ]
    # 四层筛，每层都在报告里留名：静默吞掉的条目会让「扫描 0 项」看起来像机制失效。
    protected = [n for n in candidates if n in PROTECTED_ORPHANS]
    rest = [n for n in candidates if n not in PROTECTED_ORPHANS]
    # 已裁定退役（零提交但确有裁定）：必须清，否则安装位留着已作废的副本。
    retired = [n for n in rest if n in RETIRED_SKILLS]
    # 宿主原生 skill（仓库历史里从未出现）：归档＝从宿主摘掉在用 skill，永不自动清理。
    native = [n for n in rest if n not in RETIRED_SKILLS and _never_in_repo_history(n)]
    orphans = [n for n in rest if n not in native]
    if protected:
        print(f"    [protected] {len(protected)} 项在白名单（非本仓 skill / 已裁决保留原位）："
              f"{', '.join(protected)}")
    if retired:
        print(f"    [retired] {len(retired)} 项已裁定退役（仓库侧已删、安装位是作废副本，"
              f"零提交故 native 判据抓不到）：{', '.join(retired)}")
    if native:
        print(f"    [user-native] {len(native)} 项在仓库历史中从未出现（宿主原生 skill，"
              f"归档＝摘掉在用 skill，故跳过）：{', '.join(native)}")
    if not orphans or not apply:
        return orphans

    import datetime
    host = target.resolve().parent.name or "target"
    stamp = datetime.date.today().strftime("%Y%m%d")
    dest_root = REPO_ROOT / "attic" / f"sync_orphans_{stamp}" / host
    links: List[str] = []
    for name in orphans:
        src = target / name
        # 悬空链接：symlink 与 Windows directory junction 都会「lexists 但 exists==False」。
        # 二者内容都不在本机（目标已删），跨盘 shutil.move 必失败（跟随悬空 reparse point）。
        # 故只记录 target 再摘除链接本身；symlink 用 unlink，junction 用 rmdir。
        if os.path.lexists(src) and not os.path.exists(src):
            try:
                tgt = os.readlink(src)
            except OSError:
                tgt = "<unresolvable>"
            links.append(f"{name}\t-> {tgt}")
            try:
                os.unlink(src)
            except OSError:
                try:
                    os.rmdir(src)
                except OSError as e:
                    print(f"    [warn] 无法移除悬空链接 {name}: {e}")
            continue
        dest = dest_root / name
        if dest.exists():
            continue
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(src), str(dest))
    if links:
        dest_root.mkdir(parents=True, exist_ok=True)
        with open(dest_root / "dangling_symlinks.txt", "w", encoding="utf-8", newline="") as f:
            f.write("# 已删除的悬空符号链接（内容不在本机，仅留 target 备查）\n")
            f.write("\n".join(links) + "\n")
    # 归档目录自带裁定依据：否则半年后看到 attic 里一个 skill 目录，无从判断是
    # 「改名前的旧目录」还是「被裁定退役、已由别人承接」——两者处置完全不同。
    archived_retired = [n for n in orphans if n in RETIRED_SKILLS]
    if archived_retired:
        dest_root.mkdir(parents=True, exist_ok=True)
        with open(dest_root / "retired_skills.txt", "w", encoding="utf-8", newline="") as f:
            f.write("# 本次归档中属于「已裁定退役」的条目（登记于 sync_skills.RETIRED_SKILLS）\n")
            f.write("# 退役 ≠ 作废内容：其增量片段应已合并进承接方，归档只为让安装位不再\n")
            f.write("# 以两个 skill 名并存同一套方法论。\n\n")
            for n in archived_retired:
                f.write(f"## {n}\n{RETIRED_SKILLS[n]}\n\n")
    return orphans


def _read_normalized(path: Path) -> Optional[bytes]:
    """读文件并归一化换行符。

    仓库侧是 CRLF、安装位是 LF（或反之）是常态，逐字节比较会把 33 个 skill
    全报成漂移 —— 首次实测 27 个"漂移"里只有 5 个是真的。
    """
    try:
        return path.read_bytes().replace(b"\r\n", b"\n")
    except OSError:
        return None


def diff_tree(source: Path, target: Path) -> Tuple[List[Path], List[Path], List[Path]]:
    """返回 (仅源有, 内容不同, 仅目标有) 的相对路径列表。"""
    src_files = {
        p.relative_to(source)
        for p in source.rglob("*")
        if p.is_file() and not _is_ignored(p.relative_to(source))
    }
    dst_files = {
        p.relative_to(target)
        for p in target.rglob("*")
        if p.is_file() and not _is_ignored(p.relative_to(target))
    }

    only_source = sorted(src_files - dst_files)
    only_target = sorted(dst_files - src_files)
    changed = sorted(
        rel for rel in (src_files & dst_files)
        if _read_normalized(source / rel) != _read_normalized(target / rel)
    )
    return only_source, changed, only_target


#: 运行时产物判据（安装位有、仓库没有，但**属正常**，不参与孤儿清理也不该刷屏）
# 2026-09-25 目标 C：裸 "data" 段豁免过宽——任何含 data 的路径段都被吞，会掩盖真孤儿。
# 收窄为「带上下文的已知产物位置」：仅当 data 段出现在已知产物目录下才豁免。
RUNTIME_PARTS = {"outputs", "output_report", "logs", "__pycache__"}
RUNTIME_SUFFIXES = (".log", ".csv", ".pyc", ".pyo")
RUNTIME_NAMES = {"agent_profile.json", "loop_state.json", "parsetab.py"}

#: 已知产物位置（相邻两段路径模式）：GEM 数据产物 / FE 报告位 / GEM 备用产物位。
#: 目标 A 迁移后 GEM 新产物落仓库 data/gem_runs（不在安装位），安装位只剩历史残留，
#: 仍豁免但会被识别为已知模式；其他 skill 下出现的 data/ 段不再被误吞。
RUNTIME_PATH_PATTERNS = (
    ("brain-feature-implementation", "data"),
    ("headless_runner", "outputs"),
    ("brain-data-feature-engineering", "output_report"),
)


def _is_runtime_artifact(rel: Path) -> bool:
    parts = rel.parts
    if any(part in RUNTIME_PARTS for part in parts):
        return True
    # 带上下文的已知产物位置：相邻两段匹配已知模式
    for i in range(len(parts) - 1):
        if (parts[i], parts[i + 1]) in RUNTIME_PATH_PATTERNS:
            return True
    if rel.suffix in RUNTIME_SUFFIXES:
        return True
    if ".bak_" in rel.name or rel.name in RUNTIME_NAMES:
        return True
    return False


def sync(source: Path, target: Path, dry_run: bool) -> int:
    only_source, changed, only_target = diff_tree(source, target)
    actions = 0

    for rel in only_source + changed:
        verb = "ADD " if rel in only_source else "UPD "
        print(f"  {verb} {rel.as_posix()}")
        actions += 1
        if dry_run:
            continue
        dst = target / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source / rel, dst)

    # 安装位多出来的文件只报告不删除：可能是本地产物（outputs 已在忽略表里，
    # 但历史遗留的其他文件不该被本工具静默清掉）。按顶层条目去重，避免刷屏。
    # 2026-09-11：把"运行时产物"（GEM 的 data/*_idea_*.json、ace.log 等）与
    # "真孤儿"（改名前的旧 skill 目录、一次性脚本）**分开报**，否则前者会把
    # 后者淹掉，读者以为一切正常。
    runtime = {rel for rel in only_target if _is_runtime_artifact(rel)}
    real_orphans = [rel for rel in only_target if rel not in runtime]
    for top in sorted({(rel.parts[0] if rel.parts else rel.as_posix()) for rel in real_orphans}):
        print(f"  ONLY-AT-INSTALL {top}（未删除，如确认是废弃 skill/产物请手工清理）")
    if runtime:
        print(f"  [runtime] {len(runtime)} 个运行时产物（正常，不计入孤儿）")

    return actions


def _check_one(target: Path) -> int:
    only_source, changed, _only_target = diff_tree(SOURCE, target)
    for rel in only_source:
        print(f"  MISSING  {rel.as_posix()}")
    for rel in changed:
        print(f"  STALE    {rel.as_posix()}")
    return len(only_source) + len(changed)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--check", action="store_true",
                    help="只检查漂移，任一目标有漂移则 exit 1（不写盘）")
    ap.add_argument("--dry-run", action="store_true",
                    help="打印将要执行的动作，不写盘")
    ap.add_argument("--target", action="append", default=None,
                    help="显式指定安装位（可重复；默认自动枚举全部已存在安装位）")
    ap.add_argument("--prune-orphans", action="store_true",
                    help="列出安装位里仓库不存在的顶层条目（旧 skill 目录 / 一次性脚本）；"
                         "默认只打印，配 --apply 才归档（移动，非删除）")
    ap.add_argument("--apply", action="store_true",
                    help="配合 --prune-orphans：实际执行归档（默认 dry-run）")
    a = ap.parse_args()

    if not SOURCE.is_dir():
        print(f"[sync_skills] 源目录不存在：{SOURCE}", file=sys.stderr)
        return 2

    if a.target:
        # 先展开 `~`：PowerShell 不会替原生命令展开，字面量 `~` 会被当成仓库内
        # 相对路径（误报「与仓库相关」）或真的在 CWD 下建目录。
        targets = [Path(t).expanduser() for t in a.target]
        # 显式 --target 同样硬拦：把仓库根/仓库内子目录交给 --target 与设错 WQ_SKILLS_DIR
        # 是同一个事故，而且手滑一次就把 51 个技能目录铺进根层或仓库内
        # （2026-10-14 / 2026-10-17 两次复发实测形态，第三次是仓库内子目录）。
        hit = [str(t) for t in targets if _is_repo_related(t)]
        if hit:
            print(f"[sync_skills] 拒绝执行：--target 里有与仓库相关的路径 {hit}；"
                  f"技能源就是 {SOURCE}，往仓库根或仓库内同步等于在工作树里复制整棵树（S17 会判红）",
                  file=sys.stderr)
            return 2
        disabled_hit = []
        for t in targets:
            reason = _disabled_reason(t)
            if reason:
                disabled_hit.append(f"{t}（{reason}）")
        if disabled_hit:
            print(f"[sync_skills] 拒绝执行：--target 里有已关闭的安装位 {disabled_hit}；"
                  f"若确需恢复，先删除 DISABLED_INSTALL_ROOTS 中的登记", file=sys.stderr)
            return 2
    else:
        targets = resolve_install_roots()
    if not targets:
        print("[sync_skills] 未找到 skill 安装位；用 --target 指定或设 WQ_SKILLS_DIR",
              file=sys.stderr)
        return 2

    print(f"[sync_skills] 源   : {SOURCE}")
    print(f"[sync_skills] 目标 : {len(targets)} 个安装位")

    if a.check:
        total_drift, drifted = 0, []
        for t in targets:
            n = _check_one(t)
            print(f"  [{'OK' if n == 0 else f'漂移 {n}'}] {t}")
            total_drift += n
            if n:
                drifted.append(t)
        if total_drift:
            print(f"[sync_skills] 共 {total_drift} 个文件漂移，涉及 {len(drifted)} 个安装位；"
                  f"跑 `python tools/sync_skills.py` 同步", file=sys.stderr)
            return 1
        print("[sync_skills] 全部受维护安装位与仓库一致")
        return 0

    total = 0
    for t in targets:
        print(f"\n[sync_skills] -> {t}")
        total += sync(SOURCE, t, dry_run=a.dry_run)
    verb = "将同步" if a.dry_run else "已同步"
    print(f"\n[sync_skills] {verb} {total} 个文件（{len(targets)} 个安装位）")

    # 同步成功后跑 S17 自检：同步曾把技能树铺进仓库根/仓库内子目录
    # （2026-10-14 / 2026-10-17 两次复发，守卫加了子孙判定但**执行缺口**
    # 仍存在——没人跑 audit_structure ⇒ 问题滞留一天才被发现）。
    # 这里加一个轻量自检：只看仓库根有没有非白名单目录，不跑全套审计。
    if not a.dry_run:
        s17_offenders = []
        for p in sorted(REPO_ROOT.iterdir()):
            if not p.is_dir():
                continue
            if p.name in {"__pycache__", ".venv", ".venvs", "node_modules", ".cache"}:
                continue
            if p.name.startswith("."):
                continue
            # S17_TOP_DIR_ALLOWLIST（内联避免循环 import）
            if p.name in {"src", "tools", "tests", "world-quant-brain-mcp", "Claude",
                          "tracking", "research-data", "extensions", "data",
                          "docs", "reports", "output_report", "attic",
                          "cache", "logs", "results"}:
                continue
            s17_offenders.append(p.name)
        if s17_offenders:
            print(f"[sync_skills] ⚠ S17 自检发现 {len(s17_offenders)} 个未声明顶层目录："
                  f"{s17_offenders}（同步可能把技能树铺进了仓库；见 attic/sync_strays_*）",
                  file=sys.stderr)

    if a.prune_orphans:
        print("\n[sync_skills] 孤儿扫描（安装位有、仓库没有的**顶层条目**；"
              "子文件差异与 . 开头条目不算）")
        total_orphans = 0
        for t in targets:
            names = prune_orphans(t, apply=a.apply)
            total_orphans += len(names)
            flag = "" if names else "  (无)"
            print(f"  {t}{flag}")
            for n in names:
                print(f"    - {n}")
        if total_orphans and not a.apply:
            print(f"\n[sync_skills] 待归档 {total_orphans} 项 —— 加 --apply 执行"
                  f"（移入 attic/sync_orphans_<date>/<host>/，可回滚）")
        else:
            print(f"\n[sync_skills] {'已归档' if a.apply else '无需清理'} {total_orphans} 项")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
