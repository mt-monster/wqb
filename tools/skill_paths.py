# -*- coding: utf-8 -*-
"""tools/ 下 CLI 查找 skill 脚本目录的唯一入口（2026-09-27 R12）。

顺序与 AGENTS.md §6 第 2 条、`wqb.workflow._common._skill_roots()` 一致：显式环境变量（WQ_*_DIR）>
WQ_SKILLS_DIR > Claude 安装位 > ~/.claude/skills > ~/.codex/skills > 历史 Agent 位
（qoder-cn / cursor / workbuddy）> 仓库自带 Claude/skills（兜底，clone 即可用）。

此前 wave_gate / probe_batch_mode / pre_backtest_filter 各抄一份只含 WQ_*_DIR 与三个历史位的
候选表：~/.claude、~/.codex 与仓库自身都不在其中。MCP 节点经 .mcp.json 设了 WQ_*_DIR 不受影响，
CLI 直跑、测试与未设 env 的宿主却找不到 verifier / toolkit（审计 N12；仓库
test_inspect_mode_failclosed_p1p1 两条、test_probe_batch_mode_b_distribution_mode 一条常红即此因）。
"""
from __future__ import annotations

import os
import sys
from typing import List, Optional

_REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def skill_roots() -> List[str]:
    """全部 skill 根目录候选（有序）。src/ 可导入时直接复用 `_skill_roots()`，否则按同序兜底。"""
    src = os.path.join(_REPO_ROOT, "src")
    if os.path.isdir(src) and src not in sys.path:
        sys.path.insert(0, src)
    try:
        from wqb.workflow._common import _skill_roots
        return list(_skill_roots())
    except Exception:
        home = os.path.expanduser("~")
        # 同序兜底（须与 _common._skill_roots() 一致）：.cline / .agents = Cline
        # Desktop/CLI 两个全局位（2026-10-03 补，取自 Cline dist/lib.mjs 的 yYt()）。
        roots = [os.path.join(home, h, "skills")
                 for h in (".claude", ".codex", ".cline", ".agents",
                           ".qoder-cn", ".cursor", ".workbuddy")]
        roots.append(os.path.join(_REPO_ROOT, "Claude", "skills"))
        return roots


def skill_script_dirs(skill: str, env_var: Optional[str] = None) -> List[str]:
    r"""某 skill 的 scripts/ 目录候选（有序、去重、分隔符归一）；env_var（如 WQ_TOOLKIT_DIR）给出时排最前。

    2026-09-28：`_skill_roots()` 的部分候选用 `/` 拼 home（Windows 上出混合分隔符，
    如 `C:\Users\x/.claude/skills\...`），字符串相等性比较（含 test_skill_script_dirs_follow_skill_roots）
    与命令展示都受害；此处统一 `normpath`。
    """
    cands = [os.environ.get(env_var)] if env_var else []   # env 显式值原样保留（不归一）
    cands += [os.path.normpath(os.path.join(root, skill, "scripts")) for root in skill_roots()]
    out: List[str] = []
    for c in cands:
        if c and c not in out:
            out.append(c)
    return out
