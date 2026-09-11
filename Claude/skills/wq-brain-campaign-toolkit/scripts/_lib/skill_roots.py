# -*- coding: utf-8 -*-
"""技能库根目录解析（纯标准库，镜像 `src/wqb/workflow/_common._skill_roots()` 的顺序）。

为什么需要它：2026-09-11 审计发现 4 处脚本各自维护一份"技能根搜索链"，且都漏了
主安装位 `~/.claude/skills` 与仓库自带副本 → 会静默解析到**旧拷贝**（与"GBR 跑满
180 条零达标""ra-pipeline 落后 67 行"同源）。四处收敛到本模块，顺序只此一份。

顺序（高 → 低）：
    1. $WQ_SKILLS_DIR（冒号/os.pathsep 分隔，可多值）
    2. ~/.claude/skills          （主安装位 = Claude Code / 本工作区 Agent 实际加载位）
    3. ~/.codex/skills           （Codex 安装位）
    4. ~/.trae-cn/skills         ┐
    5. ~/.qoder-cn/skills        │ 历史 Agent 安装位（独立物理拷贝，可能已落后）
    6. ~/.cursor/skills          │
    7. ~/.workbuddy/skills       ┘
    8. <repo>/Claude/skills      （仓库自带，最后兜底 → clone 即可用）

`tests/unit/test_docs_consistency.py` 守护：本模块与
`brain-make-some-gem/scripts/trailSomeAlphas/skill_roots.py` 的宿主顺序必须与
`_common._skill_roots()` 一致。
"""
from __future__ import annotations

import os

#: 安装位宿主目录名（相对 $HOME），顺序即优先级
HOST_DIRS = (".claude", ".codex", ".trae-cn", ".qoder-cn", ".cursor", ".workbuddy")

#: 本文件位于 <skills_root>/wq-brain-campaign-toolkit/scripts/_lib/ → 上溯 3 层即 <skills_root>
REPO_SKILLS_ROOT = os.path.normpath(
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..")
)


def skill_roots() -> list:
    """返回技能库根目录候选（按优先级，去重，保留首次出现顺序）。"""
    home = os.path.expanduser("~")
    roots = []
    env = os.environ.get("WQ_SKILLS_DIR")
    if env:
        roots.extend(p for p in env.split(os.pathsep) if p)
    roots.extend(os.path.join(home, h, "skills") for h in HOST_DIRS)
    roots.append(REPO_SKILLS_ROOT)
    seen, ordered = set(), []
    for r in roots:
        key = os.path.normcase(os.path.normpath(r))
        if key not in seen:
            seen.add(key)
            ordered.append(r)
    return ordered


def find_under_skill(skill_name: str, *parts: str) -> str:
    """在首个命中的技能根下拼出 `<root>/<skill_name>/<parts...>`；都不存在返回空串。"""
    for root in skill_roots():
        candidate = os.path.join(root, skill_name, *parts)
        if os.path.exists(candidate):
            return candidate
    return ""


def candidate_paths_under_skill(skill_name: str, *parts: str) -> list:
    """返回全部候选路径（不判存在），供调用方自行 os.path.isfile 探测。"""
    return [os.path.join(root, skill_name, *parts) for root in skill_roots()]
