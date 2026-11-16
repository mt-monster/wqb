# -*- coding: utf-8 -*-
"""候选选择的经验层辅助（纯函数，2026-11-15 P2）。

`build_wave` 用本模块把“跨波实测死骨架”**稳定地排到尾部**，绝不删除：
- 删除是不可逆的，会静默缩小探索面（2026-11-09 coverage 闸教训）；
- 重排可逆，且会写进 `wave_meta.selection_audit[].reason`，事后可审计。
"""
from __future__ import annotations

from typing import Any, Dict, Iterable, Optional, Sequence, Set, Tuple

from wqb.expression.skeleton import structural_signature


def dead_skeletons(skeleton_stats: Optional[Iterable[Dict[str, Any]]], *, min_n: int = 5) -> Set[str]:
    """从 region_kb.skeleton_stats 提取“统计死路”骨架签名。"""
    out: Set[str] = set()
    for g in skeleton_stats or []:
        if not isinstance(g, dict):
            continue
        if not g.get("dead"):
            continue
        if int(g.get("n") or 0) < int(min_n):
            continue
        sk = g.get("skeleton")
        if sk and sk != "_unknown":
            out.add(str(sk))
    return out


def deprioritize_dead_skeletons(
    picked: Sequence[str],
    skeleton_stats: Optional[Iterable[Dict[str, Any]]],
    *,
    min_n: int = 5,
) -> Tuple[list, Set[str]]:
    """稳定重排：存活表达式保持原顺序，死骨架整体移到尾部。

    返回 `(新列表, 被降权的表达式集合)`；两者长度恒等于输入。
    """
    dead = dead_skeletons(skeleton_stats, min_n=min_n)
    if not dead:
        return list(picked), set()
    keep, tail = [], []
    for e in picked:
        (tail if structural_signature(e) in dead else keep).append(e)
    if not tail:
        return list(picked), set()
    return keep + tail, set(tail)
