# -*- coding: utf-8 -*-
"""Locate wqb.store.CampaignStore from toolkit scripts (workspace src/)."""
from __future__ import annotations

import os
import sys
from pathlib import Path


def _workspace_roots(campaign_dir=None):
    roots = [
        os.environ.get("WQB_ROOT"),
        os.environ.get("WQ_PROJECT_ROOT"),
        r"D:\coding\traeCN_project\wqb",
    ]
    if campaign_dir:
        p = Path(campaign_dir).resolve()
        for _ in range(8):
            if (p / "src" / "wqb").is_dir() or (p / "data" / "wqb.db").exists():
                roots.insert(0, str(p))
                break
            if p.parent == p:
                break
            p = p.parent
    return [r for r in roots if r]


def get_store(ctx=None):
    """Return a CampaignStore bound to data/wqb.db (or WQB_DB_PATH)."""
    cdir = getattr(ctx, "dir", None) if ctx is not None else None
    for root in _workspace_roots(cdir):
        src = os.path.join(root, "src")
        if os.path.isdir(os.path.join(src, "wqb")):
            if src not in sys.path:
                sys.path.insert(0, src)
            from wqb.store import CampaignStore
            db = os.environ.get("WQB_DB_PATH") or os.path.join(root, "data", "wqb.db")
            return CampaignStore(db)
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
