# -*- coding: utf-8 -*-
"""workflow 共享工具：路径解析、数据集类别推断、Python 解释器定位。

单一事实源，替代各节点里重复的 skill 目录探测、硬编码绝对路径、
以及 gem/feature_engineering 各自复制的 `_infer_category`。

约定（与 tools/wave_gate.py 的 WQ_TOOLKIT_DIR/WQ_VALIDATOR_DIR 模式对齐）：
  - env 优先，默认值全部基于 os.path.expanduser("~")
  - 权威套 ~/.qoder-cn/skills，~/.cursor/skills 为 Cursor 联接安装位，
    ~/.workbuddy/skills 仅作跨 Agent 回退
"""
from __future__ import annotations

import os
import sqlite3
from pathlib import Path
from typing import Optional

# src/wqb/workflow/_common.py -> repo root
REPO_ROOT = Path(__file__).resolve().parents[3]

_SKILL_ROOTS = (
    os.path.expanduser("~/.qoder-cn/skills"),
    os.path.expanduser("~/.cursor/skills"),
    os.path.expanduser("~/.workbuddy/skills"),
)

# 平台 dataset category 前缀兜底表（与 src/wqb/config.py PLATFORM_CATEGORIES 同口径；
# 仅当 data/wqb.db 快照无记录时使用。短 key 放长 key 之后，避免子串误截断）。
_PREFIX_CATEGORY = [
    ("analyst", "analyst"),
    ("model", "model"),
    ("news", "news"),
    ("fundamental", "fundamental"),
    ("pv", "pv"),
    ("option", "option"),
    ("risk", "risk"),
    ("shortinterest", "shortinterest"),
    ("institutions", "institutions"),
    ("imbalance", "imbalance"),
    ("macro", "macro"),
    ("earnings", "earnings"),
    ("equity", "equity"),
    ("sentiment", "sentiment"),
    ("insiders", "insiders"),
    ("insider", "insiders"),
]

#: data/wqb.db（datasets 表为平台 get_datasets 快照，见 tools/ingest_dataset_assets.py）
_DB_PATH = REPO_ROOT / "data" / "wqb.db"


def _platform_category(dataset_id: str) -> Optional[str]:
    """以平台 category 为准：优先查 datasets 快照（category 非空的最新一条）。

    快照缺记录（如 model50 在 IND 仅存 category=NULL 行）时返回 None，
    由调用方回退前缀推断。
    """
    try:
        conn = sqlite3.connect(_DB_PATH)
        try:
            row = conn.execute(
                "SELECT category FROM datasets WHERE name=? "
                "AND category IS NOT NULL AND category != '' "
                "ORDER BY id DESC LIMIT 1",
                (dataset_id,),
            ).fetchone()
            return str(row[0]) if row else None
        finally:
            conn.close()
    except Exception:
        return None


def infer_data_category(dataset_id: str) -> str:
    """推断数据集类别：平台 category 优先（data/wqb.db 快照），无记录时前缀兜底。

    分类口径一律以平台 category 为准（2026-09-01 统一）——如 model50 内容为
    下行风险评估打分（International Scorings Data），但平台分类为 model，
    不按内容语义归入 risk。
    """
    platform = _platform_category(dataset_id)
    if platform:
        return platform
    lower = dataset_id.lower()
    for key, value in _PREFIX_CATEGORY:
        if key in lower:
            return value
    return "other"


def resolve_skill_dir(skill_name: str) -> Optional[str]:
    """定位 skill 根目录（如 brain-makeSomeGem）。返回绝对路径或 None。"""
    for root in _SKILL_ROOTS:
        candidate = os.path.join(root, skill_name)
        if os.path.isdir(candidate):
            return candidate
    return None


def resolve_toolkit_dir() -> Optional[str]:
    """定位 wq-brain-campaign-toolkit/scripts（含 WQ_TOOLKIT_DIR 覆盖）。"""
    env = os.environ.get("WQ_TOOLKIT_DIR")
    if env and os.path.isdir(env):
        return env
    for root in _SKILL_ROOTS:
        candidate = os.path.join(root, "wq-brain-campaign-toolkit", "scripts")
        if os.path.isdir(candidate):
            return candidate
    return None


def resolve_tools_dir() -> str:
    """定位仓库 tools/ 目录（基于 REPO_ROOT 推导，不依赖 cwd、不硬编码盘符）。"""
    return str(REPO_ROOT / "tools")


def resolve_campaign_dir(region: str) -> Optional[str]:
    """解析区域战役目录 tracking/<region>。

    优先级：WQB_CAMPAIGN_DIR 环境变量 > WQB_WORKSPACE_ROOT > 仓库 tracking/<region>。
    """
    env = os.environ.get("WQB_CAMPAIGN_DIR")
    if env and os.path.exists(env):
        return os.path.abspath(env)

    workspace_root = os.environ.get("WQB_WORKSPACE_ROOT")
    if workspace_root:
        candidate = os.path.join(workspace_root, "tracking", region)
        if os.path.exists(candidate):
            return os.path.abspath(candidate)

    candidate = REPO_ROOT / "tracking" / region
    if candidate.is_dir():
        return str(candidate)
    return None


def wq_py() -> str:
    """返回 MCP venv 的 python 解释器路径。

    优先 WQ_PY 环境变量；回退到 world-quant-brain-mcp/.venv/Scripts/python.exe；
    最后回退 "python"。
    """
    env = os.environ.get("WQ_PY")
    if env and os.path.isfile(env):
        return env
    for rel in (
        os.path.join("world-quant-brain-mcp", ".venv", "Scripts", "python.exe"),
        os.path.join("world-quant-brain-mcp", ".venv", "bin", "python"),
    ):
        candidate = REPO_ROOT / rel
        if candidate.is_file():
            return str(candidate)
    return "python"
