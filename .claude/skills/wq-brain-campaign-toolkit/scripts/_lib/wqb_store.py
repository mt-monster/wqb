# -*- coding: utf-8 -*-
"""Locate wqb.store.CampaignStore from toolkit scripts (workspace src/)."""
from __future__ import annotations

import os
import sys
from pathlib import Path


def _walk_up(start):
    """从 start 向上（≤8 层）找工作区标记 src/wqb 或 data/wqb.db；找不到返回 None。"""
    if not start:
        return None
    p = Path(start).resolve()
    for _ in range(8):
        if (p / "src" / "wqb").is_dir() or (p / "data" / "wqb.db").exists():
            return str(p)
        if p.parent == p:
            break
        p = p.parent
    return None


def _workspace_roots(campaign_dir=None):
    """候选工作区根，按优先级去重。

    显式环境变量按原样采信；推断来源（战役目录 / 本文件 / cwd 上溯）要求命中工作区标记。
    2026-09-27 R19：历史默认 `D:\\coding\\traeCN_project\\wqb` 此前无条件兜底——仓库不在该
    路径时，`_lib/ledger` 在 cwd 下拼出相对路径 "D:\\coding\\…\\data\\wqb.db" 直接崩溃，
    tools/wave_gate.py 的同款兜底则造出杂散目录与空库。2026-09-29（X-14）起该历史默认路径
    彻底移除：只认环境变量与「战役目录 / 本文件 / cwd 上溯」这些真实可验证的来源。
    """
    cands = [
        _walk_up(campaign_dir),
        os.environ.get("WQB_WORKSPACE"),
        os.environ.get("WQB_ROOT"),
        os.environ.get("WQ_PROJECT_ROOT"),
        _walk_up(os.path.dirname(os.path.abspath(__file__))),   # 仓库内的 toolkit
        _walk_up(os.getcwd()),
    ]
    roots = []
    for r in cands:
        if r and r not in roots:
            roots.append(r)
    return roots


def resolve_db_path(ctx=None):
    """toolkit 内战役库路径的唯一解析（2026-09-27 R19）。

    get_store 与 `_lib/ledger.SqliteLedgerStore` / `_lib/registry.RegistryStore` /
    `_lib/wave_results.WaveResultsStore` 共用——此前前者按战役目录上溯、后三者只认
    WQB_WORKSPACE 否则落硬编码盘符，同一次 assemble-priors 会读两个库。
    顺序：WQB_DB_PATH > 战役目录上溯 > WQB_WORKSPACE > WQB_ROOT > WQ_PROJECT_ROOT
    > 本文件上溯 > cwd 上溯。
    """
    env = os.environ.get("WQB_DB_PATH")
    if env:
        return env
    roots = _workspace_roots(getattr(ctx, "dir", None) if ctx is not None else None)
    if not roots:
        raise FileNotFoundError(
            "找不到 wqb 工作区（含 src/wqb 或 data/wqb.db 的目录）：设 WQB_DB_PATH 指向库文件，"
            "或设 WQB_WORKSPACE 指向工作区根")
    return os.path.join(roots[0], "data", "wqb.db")


def get_store(ctx=None):
    """Return a CampaignStore bound to resolve_db_path(ctx) (WQB_DB_PATH first)."""
    cdir = getattr(ctx, "dir", None) if ctx is not None else None
    for root in _workspace_roots(cdir):
        src = os.path.join(root, "src")
        if os.path.isdir(os.path.join(src, "wqb")):
            if src not in sys.path:
                sys.path.insert(0, src)
            from wqb.store import CampaignStore
            return CampaignStore(resolve_db_path(ctx))
    raise ImportError("wqb.store not found; set WQB_ROOT to the wqb workspace")


def load_catalog(ctx, dataset):
    store = get_store(ctx)
    try:
        return store.get_field_catalog(ctx.region, dataset)
    finally:
        store.close()


def save_catalog(ctx, catalog):
    store = get_store(ctx)
    try:
        return store.upsert_field_catalog(ctx.region, catalog)
    finally:
        store.close()


def list_catalog_datasets(ctx):
    """该区 DB 里已有字段目录的数据集名列表（文件面枚举的 DB 替代，2026-10-01）。"""
    store = get_store(ctx)
    try:
        return store.list_catalog_datasets(ctx.region)
    finally:
        store.close()


def load_ranking(ctx):
    store = get_store(ctx)
    try:
        return store.get_ranking(ctx.region)
    finally:
        store.close()


def save_ranking(ctx, payload):
    store = get_store(ctx)
    try:
        store.upsert_ranking(ctx.region, payload)
    finally:
        store.close()
