# -*- coding: utf-8 -*-
"""paths — 仓库根与工作区路径的规范解析（2026-10-04 P2-1 新增）。

为什么要有这个模块
------------------
`tools/` 与 skill 脚本里长期存在**五种**互相不兼容的仓库根推导写法（实测同一主题目录内就有）：

    _REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))   # 层数硬编码
    REPO_ROOT = Path(__file__).resolve().parents[1]                        # 层数硬编码
    REPO = Path(__file__).resolve().parent.parent                          # 层数硬编码
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
    Path(__file__).resolve().parents[2]                                    # 更深一层

前三类**对文件所在层数敏感**：脚本从 `tools/x.py` 移到 `tools/<主题>/x.py`，层数 +1，
常量静默变成错误目录 —— DB 路径、报告输出、attic 归档全部指错，而单测未必覆盖到那条分支。
2026-10-04 的结构治理因此**不做批量下沉**（见 `tools/THEMES.json` 的 `_why_not_moved`），
但新代码一律走本模块的**向上探测**写法：与所在层数无关，移动文件不再需要改路径。

约定
----
- 仓库根标记 = 同时存在 `pyproject.toml` 与 `src/wqb/`（后者避免命中同名子项目）。
- 解析优先级：`WQB_ROOT` 环境变量 > 从起点向上探测 > 调用方 cwd 兜底。
  （`WQB_ROOT` 语义与 `docs/env_registry.json` 登记一致：各脚本仓库根覆盖。）
"""
from __future__ import annotations

import os
from pathlib import Path
from typing import Optional

_ROOT_MARKERS = ("pyproject.toml", "src/wqb")


def find_repo_root(start: Optional[str] = None) -> Path:
    """向上探测仓库根。

    Args:
        start: 起点文件或目录；缺省用本模块位置（`src/wqb/paths.py`）。
               脚本里写 ``find_repo_root(__file__)`` 即可与自身层数解耦。

    Raises:
        RuntimeError: 找不到根标记（不在本工作区内运行）。
    """
    env = os.environ.get("WQB_ROOT")
    if env:
        p = Path(env).resolve()
        if _has_markers(p):
            return p
        # 环境变量指错时不静默采信，继续向上探测（避免错误根污染后续路径）

    here = Path(start or __file__).resolve()
    base = here if here.is_dir() else here.parent
    for parent in (base, *base.parents):
        if _has_markers(parent):
            return parent
    raise RuntimeError(
        f"仓库根未找到（从 {base} 向上未出现 {list(_ROOT_MARKERS)}）；"
        f"可用 WQB_ROOT 显式指定"
    )


def _has_markers(p: Path) -> bool:
    return p.is_dir() and all((p / m).exists() for m in _ROOT_MARKERS)


def repo_relative(*parts: str) -> Path:
    """仓库根下的路径，如 ``repo_relative("data", "wqb.db")``。"""
    out = find_repo_root()
    for p in parts:
        out = out / p
    return out


def repo_root() -> Path:
    """本工作区仓库根（等价于 ``find_repo_root()``，命名对齐既有脚本的 ``REPO_ROOT``）。"""
    return find_repo_root()
