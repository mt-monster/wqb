# -*- coding: utf-8 -*-
"""2026-09-19 连坐隔离回归（pipeline.py `_isolate_error_batch` / `_run_round` 重发）。

背景：平台 multisim 语义是"任一子模拟 ERROR → 同批其余 CANCELLED"。JPN w7/w8 实测
一条 `bucket()` 缺 range / 一个平台不认的字段，整批 8 条连坐，10 批丢 8 批 64 条。
此前 SOP 只把"隔离坏式重发"写成人工协议，pipeline 自身不处理。

本测试纯本地：api / submit_batch / poll 全部打桩，不联网、不写库（store 打桩）。
"""
import importlib
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
TOOLKIT_SCRIPTS = REPO_ROOT / "Claude" / "skills" / "wq-brain-campaign-toolkit" / "scripts"


def _pipeline_mod():
    if str(TOOLKIT_SCRIPTS) not in sys.path:
        sys.path.insert(0, str(TOOLKIT_SCRIPTS))
    for m in ("pipeline", "review_wave", "metrics_cache", "gate", "_lib.rules",
              "_lib.region_kb", "_lib.wqb_store", "_lib.ledger", "_lib.common",
              "_lib.api", "_lib.poller", "_lib"):
        sys.modules.pop(m, None)
    return importlib.import_module("pipeline")


# ---------------------------------------------------------------- _isolate_error_batch

def test_isolate_splits_culprit_from_cancelled_siblings():
    pl = _pipeline_mod()
    batch = ["rank(a)", "bucket(rank(b))", "rank(c)"]
    errs = [
        {"child": "c1", "status": "CANCELLED", "error": "CANCELLED", "expr": "rank(a)"},
        {"child": "c2", "status": "ERROR",
         "error": 'At least one of "buckets", "range" is required.', "expr": "bucket(rank(b))"},
        {"child": "c3", "status": "CANCELLED", "error": "CANCELLED", "expr": "rank(c)"},
    ]
    culprits, survivors = pl._isolate_error_batch(batch, errs)
    assert [c["expr"] for c in culprits] == ["bucket(rank(b))"]
    assert "range" in culprits[0]["error"]
    assert survivors == ["rank(a)", "rank(c)"]        # 保序、不含坏式


def test_isolate_returns_empty_when_platform_gives_no_expression():
    pl = _pipeline_mod()
    batch = ["rank(a)", "rank(b)"]
    errs = [{"child": "c1", "status": "ERROR", "error": "boom", "expr": ""},
            {"child": "c2", "status": "CANCELLED", "error": "CANCELLED", "expr": ""}]
    assert pl._isolate_error_batch(batch, errs) == ([], [])   # 定位不到坏式 → 不盲目重发


def test_isolate_handles_dict_items_with_per_item_settings():
    pl = _pipeline_mod()
    batch = [{"expr": "rank(a)", "settings": {"decay": 2}}, "rank(b)"]
    errs = [{"child": "c1", "status": "ERROR", "error": "bad", "expr": "rank(a)"},
            {"child": "c2", "status": "CANCELLED", "error": "CANCELLED", "expr": "rank(b)"}]
    culprits, survivors = pl._isolate_error_batch(batch, errs)
    assert culprits[0]["expr"] == "rank(a)"
    assert survivors == ["rank(b)"]


# ---------------------------------------------------------------- _run_round 重发一次、不死循环

class _Ctx:
    region = "JPN"
    settings = {"region": "JPN", "universe": "TOP1600"}


def _install_fakes(pl, monkeypatch, plan):
    """plan: msid -> (status, detail, errs)。submit 按顺序发 msid；poll 按 plan 返回。"""
    order = list(plan.keys())
    submitted = []

    def fake_submit(api, settings, exprs):
        msid = order[len(submitted)]
        submitted.append((msid, [pl.item_expr(e) for e in exprs]))
        return msid

    def fake_poll(api, msid, pcfg, bi):
        st, detail, _ = plan[msid]
        return bi, st, detail

    def fake_update(ck, bi, batch, msid, status, detail, api):
        rec = next((b for b in ck["batches"] if b.get("multisim") == msid), None)
        if not rec:
            rec = {"exprs": batch, "multisim": msid}
            ck["batches"].append(rec)
        rec["status"] = status
        if status == "ERROR":
            rec["errors"] = plan[msid][2]
        elif status == "COMPLETE":
            rec["alphas"] = ["A" + msid]
        return rec

    monkeypatch.setattr(pl, "submit_batch", fake_submit)
    monkeypatch.setattr(pl, "_poll_single_batch", fake_poll)
    monkeypatch.setattr(pl, "_update_ck_batch", fake_update)
    monkeypatch.setattr(pl, "_mark_culprits_in_db", lambda ctx, wave, culprits: len(culprits))
    monkeypatch.setattr(pl, "ckpt_save", lambda ctx, ck, d: None)
    monkeypatch.setenv("WQB_GLOBAL_SLOTS", "0")   # 单测不做账户级槽位仲裁（不落 token 文件）
    return submitted


def test_run_round_resubmits_survivors_once(monkeypatch):
    pl = _pipeline_mod()
    culprit_errs = [
        {"child": "x", "status": "ERROR", "error": "Invalid data field close.", "expr": "rank(bad)"},
        {"child": "y", "status": "CANCELLED", "error": "CANCELLED", "expr": "rank(ok1)"},
        {"child": "z", "status": "CANCELLED", "error": "CANCELLED", "expr": "rank(ok2)"},
    ]
    plan = {
        "ms1": ("ERROR", {"children": ["x", "y", "z"]}, culprit_errs),   # 首批：1 坏 2 无辜
        "ms2": ("COMPLETE", {"children": []}, []),                          # 重发批 COMPLETE
    }
    submitted = _install_fakes(pl, monkeypatch, plan)
    ck = {"wave": "7", "batches": [], "item_overrides": {}}
    completed, failed, _ = pl._run_round(
        api=None, ctx=_Ctx(), ck=ck, round_batches=[["rank(bad)", "rank(ok1)", "rank(ok2)"]],
        n_slots=1, pcfg={}, checkpoint_dir=None, round_idx=1, pending_batches=[])
    # 重发批只含无辜兄弟、保序
    assert submitted == [("ms1", ["rank(bad)", "rank(ok1)", "rank(ok2)"]),
                         ("ms2", ["rank(ok1)", "rank(ok2)"])]
    assert completed == 1 and failed == 1
    retry = [b for b in ck["batches"] if b.get("retry_of")]
    assert len(retry) == 1 and retry[0]["retry_of"] == "ms1"
    first = next(b for b in ck["batches"] if b.get("multisim") == "ms1")
    assert [c["expr"] for c in first["isolated_culprits"]] == ["rank(bad)"]


def test_run_round_retry_batch_error_is_not_retried_again(monkeypatch):
    pl = _pipeline_mod()
    errs1 = [{"child": "x", "status": "ERROR", "error": "bad", "expr": "rank(bad)"},
             {"child": "y", "status": "CANCELLED", "error": "CANCELLED", "expr": "rank(ok)"}]
    errs2 = [{"child": "p", "status": "ERROR", "error": "bad again", "expr": "rank(ok)"}]
    plan = {
        "ms1": ("ERROR", {"children": ["x", "y"]}, errs1),
        "ms2": ("ERROR", {"children": ["p"]}, errs2),   # 重发批也 ERROR → 到此为止
    }
    submitted = _install_fakes(pl, monkeypatch, plan)
    ck = {"wave": "7", "batches": [], "item_overrides": {}}
    pl._run_round(api=None, ctx=_Ctx(), ck=ck, round_batches=[["rank(bad)", "rank(ok)"]],
                  n_slots=1, pcfg={}, checkpoint_dir=None, round_idx=1, pending_batches=[])
    assert [m for m, _ in submitted] == ["ms1", "ms2"]     # 没有第三次提交


def test_run_round_retry_has_priority_over_pending(monkeypatch):
    pl = _pipeline_mod()
    errs1 = [{"child": "x", "status": "ERROR", "error": "bad", "expr": "rank(bad)"},
             {"child": "y", "status": "CANCELLED", "error": "CANCELLED", "expr": "rank(ok)"}]
    plan = {
        "ms1": ("ERROR", {"children": ["x", "y"]}, errs1),
        "ms2": ("COMPLETE", {"children": []}, []),   # 应是重发批（优先于 pending）
        "ms3": ("COMPLETE", {"children": []}, []),   # pending 批
    }
    submitted = _install_fakes(pl, monkeypatch, plan)
    ck = {"wave": "7", "batches": [], "item_overrides": {}}
    pl._run_round(api=None, ctx=_Ctx(), ck=ck, round_batches=[["rank(bad)", "rank(ok)"]],
                  n_slots=1, pcfg={}, checkpoint_dir=None, round_idx=1,
                  pending_batches=[["rank(p1)", "rank(p2)"]])
    assert submitted[1] == ("ms2", ["rank(ok)"])
    assert submitted[2] == ("ms3", ["rank(p1)", "rank(p2)"])


def test_run_round_isolation_can_be_disabled(monkeypatch):
    pl = _pipeline_mod()
    errs1 = [{"child": "x", "status": "ERROR", "error": "bad", "expr": "rank(bad)"},
             {"child": "y", "status": "CANCELLED", "error": "CANCELLED", "expr": "rank(ok)"}]
    plan = {"ms1": ("ERROR", {"children": ["x", "y"]}, errs1)}
    submitted = _install_fakes(pl, monkeypatch, plan)
    ck = {"wave": "7", "batches": [], "item_overrides": {}}
    pl._run_round(api=None, ctx=_Ctx(), ck=ck, round_batches=[["rank(bad)", "rank(ok)"]],
                  n_slots=1, pcfg={}, checkpoint_dir=None, round_idx=1,
                  pending_batches=[], isolate_errors=False)
    assert [m for m, _ in submitted] == ["ms1"]


def test_isolate_falls_back_to_child_index_when_no_expression(monkeypatch):
    """JPN isotest2 实测：子模拟 GET 不回 regular → 按 children 顺序（= 提交顺序）定位坏式。"""
    pl = _pipeline_mod()
    batch = ["group_count(a, b)", "rank(ts_mean(a, 22))", "rank(ts_delta(b, 5))"]
    errs = [
        {"child": "c1", "idx": 0, "status": "ERROR", "error": "Incompatible unit for input of group_count", "expr": ""},
        {"child": "c2", "idx": 1, "status": "CANCELLED", "error": "CANCELLED", "expr": ""},
        {"child": "c3", "idx": 2, "status": "ERROR", "error": "Invalid data field close.", "expr": ""},
    ]
    culprits, survivors = pl._isolate_error_batch(batch, errs)
    assert [c["expr"] for c in culprits] == ["group_count(a, b)", "rank(ts_delta(b, 5))"]
    assert survivors == ["rank(ts_mean(a, 22))"]
    # errs 未覆盖整批（子模拟数 != 表达式数）→ 不按序猜
    assert pl._isolate_error_batch(batch, errs[:2]) == ([], [])
