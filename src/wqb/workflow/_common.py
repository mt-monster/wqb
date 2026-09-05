# -*- coding: utf-8 -*-
"""workflow 共享工具：路径解析、数据集类别推断、Python 解释器定位。

单一事实源，替代各节点里重复的 skill 目录探测、硬编码绝对路径、
以及 gem/feature_engineering 各自复制的 `_infer_category`。

约定（与 tools/wave_gate.py 的 WQ_TOOLKIT_DIR/WQ_VALIDATOR_DIR 模式对齐）：
  - env 优先（WQ_SKILLS_DIR / WQ_TOOLKIT_DIR），其余基于 os.path.expanduser("~")
  - 候选顺序见 _skill_roots()：Claude 安装位 > 历史 Agent 安装位（qoder-cn /
    cursor / workbuddy）> 仓库自带 Claude/skills（兜底，保证 clone 即可用）
"""
from __future__ import annotations

import logging
import os
import sqlite3
from pathlib import Path
from typing import Any, Dict, Optional

# src/wqb/workflow/_common.py -> repo root
REPO_ROOT = Path(__file__).resolve().parents[3]

def _skill_roots() -> tuple:
    """技能根目录候选表（按优先级）。

    2026-09-05 修复：此前只认 ~/.qoder-cn / ~/.cursor / ~/.workbuddy 三处，
    而仓库自带 Claude/skills/ 且 install_claude_skills.ps1 / install_now.py
    装到 %APPDATA%\\Claude\\skills 或 ~/.claude/skills —— 三组位置互不相交，
    导致 campaign / gem 节点在 Claude 侧安装时一律 "not found"。

    优先级：WQ_SKILLS_DIR 环境变量 > Claude 安装位 > 历史 Agent 安装位 >
    仓库自带 Claude/skills（最后兜底，保证 clone 即可用）。
    """
    roots = []

    env = os.environ.get("WQ_SKILLS_DIR")
    if env:
        roots.extend(part for part in env.split(os.pathsep) if part)

    # Claude 安装位（install_claude_skills.ps1 / install_now.py 的目标集合）
    for var, *parts in (
        ("APPDATA", "Claude", "skills"),
        ("APPDATA", "Anthropic", "Claude", "skills"),
        ("LOCALAPPDATA", "Claude", "skills"),
        ("LOCALAPPDATA", "Anthropic", "Claude", "skills"),
    ):
        base = os.environ.get(var)
        if base:
            roots.append(os.path.join(base, *parts))
    roots.append(os.path.expanduser("~/.claude/skills"))

    # 历史 Agent 安装位
    roots.append(os.path.expanduser("~/.qoder-cn/skills"))
    roots.append(os.path.expanduser("~/.cursor/skills"))
    roots.append(os.path.expanduser("~/.workbuddy/skills"))

    # 仓库自带副本（最后兜底）
    roots.append(str(REPO_ROOT / "Claude" / "skills"))

    seen = set()
    ordered = []
    for r in roots:
        if r and r not in seen:
            seen.add(r)
            ordered.append(r)
    return tuple(ordered)


#: 兼容旧引用；求值时刻的快照，动态解析一律走 _skill_roots()
_SKILL_ROOTS = _skill_roots()

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
    for root in _skill_roots():
        candidate = os.path.join(root, skill_name)
        if os.path.isdir(candidate):
            return candidate
    return None


def resolve_toolkit_dir() -> Optional[str]:
    """定位 wq-brain-campaign-toolkit/scripts（含 WQ_TOOLKIT_DIR 覆盖）。"""
    env = os.environ.get("WQ_TOOLKIT_DIR")
    if env and os.path.isdir(env):
        return env
    for root in _skill_roots():
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


# ---------------------------------------------------------------------------
# 平台客户端与台账基元（2026-09-05 从 judge/submit_alpha/superalpha 上提）
# ---------------------------------------------------------------------------

def get_brain_client():
    """延迟导入 brain_client 单例（避免循环依赖与启动开销）。

    三节点（judge / submit_alpha / superalpha）此前逐字重复本函数，
    现统一在此：把 world-quant-brain-mcp/ 临时插入 sys.path 后导入。
    """
    import sys

    mcp_dir = str(REPO_ROOT / "world-quant-brain-mcp")
    if mcp_dir not in sys.path:
        sys.path.insert(0, mcp_dir)
    from brain_api import brain_client  # noqa

    return brain_client


def run_async(coro):
    """在同步节点里执行异步 brain_client 方法。

    无运行中事件循环时新建 loop；已在运行中（如 MCP async 工具上下文）
    则切到独立线程跑，避免 `asyncio.run()` 嵌套报错。

    注意：superalpha 原为简化版（缺"运行中循环"分支），统一到此处后
    在 async 上下文里的行为由"抛错"变为"线程执行"，属修复而非回归。
    """
    import asyncio
    import concurrent.futures

    logger = logging.getLogger(__name__)
    try:
        try:
            asyncio.get_running_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            try:
                return loop.run_until_complete(coro)
            finally:
                loop.close()
        # 已在运行中的事件循环：用独立线程跑
        with concurrent.futures.ThreadPoolExecutor(max_workers=1) as pool:
            return pool.submit(lambda: asyncio.run(coro)).result()
    except Exception as e:
        logger.warning(f"async brain call failed: {e}")
        return {"__error__": str(e)}


def persist_workflow_record(
    store,
    prefix: str,
    alpha_id: str,
    payload: Dict[str, Any],
) -> None:
    """把节点结果写入 WORKFLOW 台账（失败只告警，不抛给调用方）。

    judge / submit_alpha 的 `_finalize` 结构相同（if store → try upsert
    → except 告警），仅台账 key 前缀与字段不同；差异由 prefix + payload
    参数化，公共的容错与日志收在此处。
    """
    if not store:
        return
    try:
        store.upsert_ledger("WORKFLOW", f"{prefix}_{alpha_id}", payload)
    except Exception as e:
        logging.getLogger(__name__).warning(
            f"Failed to save {prefix} record for {alpha_id}: {e}"
        )
