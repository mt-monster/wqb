"""定位 wqb 工作区（src/wqb）并打开 CampaignStore——本 skill 内所有脚本共用这一份。

此前 build_alpha_list.py / resolve_settings.py 各拷了一段「WQB_ROOT → WQ_PROJECT_ROOT → 作者本机盘符」，
仓库不在该盘符时静默退化（skills 审查 X-14）。现在：显式环境变量 > 仓库内上溯 src/wqb，没有作者盘符兜底。
"""
from __future__ import annotations

import os
import sys
from pathlib import Path


def workspace_roots() -> list[str]:
    roots: list[str] = []
    for name in ("WQB_WORKSPACE", "WQB_ROOT", "WQ_PROJECT_ROOT"):
        v = os.environ.get(name)
        if v and v not in roots:
            roots.append(v)
    here = Path(__file__).resolve()
    for parent in here.parents:                       # 仓库内的 skill：上溯到含 src/wqb 的目录
        if (parent / "src" / "wqb").is_dir():
            if str(parent) not in roots:
                roots.append(str(parent))
            break
    return roots


def open_store():
    """返回 CampaignStore（WQB_DB_PATH 优先，便于隔离）；找不到工作区返回 None。"""
    for root in workspace_roots():
        src = os.path.join(root, "src")
        if os.path.isdir(os.path.join(src, "wqb")):
            if src not in sys.path:
                sys.path.insert(0, src)
            from wqb.store import CampaignStore
            db = os.environ.get("WQB_DB_PATH") or os.path.join(root, "data", "wqb.db")
            return CampaignStore(db)
    return None
