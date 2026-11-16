# -*- coding: utf-8 -*-
"""经验索引 / 蒸馏的 toolkit 薄壳（2026-11-15）。

**只做委托，不复制任何判定逻辑**：实现在 `src/wqb/knowledge/`。技能装到仓库外时
`wqb` 可能不可导入——那种场景服务的是真实战役运行而非 pytest，降级为一次性告警并
返回 None，不阻断 pipeline（与 `_lib/db.py` 的委托模式一致）。
"""
from __future__ import annotations

_WARNED = False


def _warn_once():
    global _WARNED
    if not _WARNED:
        _WARNED = True
        print("[knowledge][WARN] wqb.knowledge 不可导入，跳过经验索引/蒸馏"
              "（技能装在仓库外？）")


def refresh_from_review(ctx, wave, rows, settings=None, thresholds=None, dry_run=False):
    """stage_review 收批后写 attempt_knowledge。异常由调用方决定是否阻断。"""
    try:
        from wqb.knowledge.capture import refresh_attempt_knowledge
    except Exception:
        _warn_once()
        return None
    from _lib.wqb_store import get_store

    st = get_store(ctx)
    try:
        return refresh_attempt_knowledge(
            st, ctx.region, wave, rows=rows, settings=settings,
            thresholds=thresholds, dry_run=dry_run)
    finally:
        st.close()


def distill_and_publish(ctx, wave, dry_run=False):
    """P2：波级蒸馏 + 区域级统计发布。异常由调用方决定是否阻断。"""
    try:
        from wqb.knowledge.distill import distill_wave, publish_region_stats
    except Exception:
        _warn_once()
        return None
    from _lib.wqb_store import get_store

    st = get_store(ctx)
    try:
        lesson = distill_wave(st, ctx.region, wave)
        published = None if dry_run else publish_region_stats(st, ctx.region, lesson)
        return {"wave_lessons": lesson, "published": published, "dry_run": bool(dry_run)}
    finally:
        st.close()


def write_digest(ctx, dry_run=False):
    """P4：刷新 `tracking/<R>/priors/experience_digest.md`（机器段，保留人工笔记）。"""
    try:
        from wqb.knowledge.digest import write_region_digest
    except Exception:
        _warn_once()
        return None
    from _lib.wqb_store import get_store
    import os

    if dry_run:
        return None
    path = os.path.join(ctx.dir, "priors", "experience_digest.md")
    st = get_store(ctx)
    try:
        return write_region_digest(st, ctx.region, path)
    finally:
        st.close()
