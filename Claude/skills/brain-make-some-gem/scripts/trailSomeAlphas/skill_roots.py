# -*- coding: utf-8 -*-
"""技能库根目录解析（纯标准库）。与 toolkit `scripts/_lib/skill_roots.py` **同序**。

2026-09-11 审计：`run_pipeline.py` / `skeletons.py` 原先各自内联搜索链，且都漏了
`~/.claude/skills`（主安装位）与仓库自带副本 → 会静默读到旧拷贝。收敛到本模块。

顺序见 `wq-brain-campaign-toolkit/scripts/_lib/skill_roots.py` 模块头（两份必须一致，
由 `tests/unit/test_docs_consistency.py::test_skill_roots_mirrors_agree_with_common` 守护）。
"""
from __future__ import annotations

import os

#: 安装位宿主目录名（相对 $HOME），顺序即优先级
HOST_DIRS = (".claude", ".codex", ".trae-cn", ".qoder-cn", ".cursor", ".workbuddy")

#: 本文件位于 <skills_root>/brain-make-some-gem/scripts/trailSomeAlphas/ → 上溯 3 层即 <skills_root>
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


def candidate_paths_under_skill(skill_name: str, *parts: str) -> list:
    """返回全部候选路径（不判存在），供调用方自行 os.path.isfile 探测。"""
    return [os.path.join(root, skill_name, *parts) for root in skill_roots()]
