# -*- coding: utf-8 -*-
"""`slots.is_full()` 与 `pipeline._refill`：区分「槽位已满」与「不仲裁」（2026-10-04）。

缺陷：2026-10-02 的死锁修复让 `pipeline._refill` 走 `acquire(nonblock=True)`，并把**任何** None 都当「槽位已满、
跳过补批」。但 `acquire` 在 `cap<=0`（`WQB_GLOBAL_SLOTS=0`，文档里的「0 关闭」）与目录不可用时也返回 None，
含义恰好相反——「不仲裁，照常提交」。结果：关闭仲裁时，重发 / 补批永远提交不出去，主循环空等 30 分钟才放弃；
`tests/unit/02_workflow/test_pipeline_error_isolation.py::test_run_round_resubmits_survivors_once` 因此整体挂住，
全量 pytest（含 pre-commit 的 `pytest tests/ -x`）在它身上卡死。

修法：`slots.is_full()`（只读、不建 token）——仅「仲裁开着且在飞 >= cap」才算满；`_refill` 在 None 之后再问它。

守三件事：
  1. `is_full` 的四种取值（不仲裁 / 目录缺失 / 未满 / 已满）；
  2. `acquire(nonblock=True)` 在「满」与「不仲裁」下**都**返回 None——这正是需要 `is_full` 区分的原因（反向前提）；
  3. 不仲裁时 `_run_round` 的重发批真的会被提交（有界：把等待上限压到 0、sleep 打桩，回归时快速失败而不是挂 30 分钟）。
"""
import importlib
import os
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[3]
TOOLKIT_SCRIPTS = REPO_ROOT / "Claude" / "skills" / "wq-brain-campaign-toolkit" / "scripts"


def _slots(monkeypatch, tmp_path, cap):
    if str(TOOLKIT_SCRIPTS) not in sys.path:
        sys.path.insert(0, str(TOOLKIT_SCRIPTS))
    monkeypatch.setenv("WQB_SLOTS_DIR", str(tmp_path / "slots"))
    monkeypatch.setenv("WQB_GLOBAL_SLOTS", str(cap))
    sys.modules.pop("_lib.slots", None)
    return importlib.import_module("_lib.slots")


# ---------------------------------------------------------------- is_full

def test_is_full_false_when_arbitration_is_off(monkeypatch, tmp_path):
    sl = _slots(monkeypatch, tmp_path, cap=0)
    assert sl.is_full() is False


def test_is_full_false_when_the_slots_dir_does_not_exist(monkeypatch, tmp_path):
    sl = _slots(monkeypatch, tmp_path, cap=1)
    assert not (tmp_path / "slots").exists()
    assert sl.is_full() is False


def test_is_full_tracks_live_tokens_against_the_cap(monkeypatch, tmp_path):
    sl = _slots(monkeypatch, tmp_path, cap=2)
    t1 = sl.acquire("a", log=lambda *_: None)
    assert t1 and sl.is_full() is False            # 1 < 2
    t2 = sl.acquire("b", log=lambda *_: None)
    assert t2 and sl.is_full() is True             # 2 >= 2
    sl.release(t1)
    assert sl.is_full() is False                   # 释放后又有空位


def test_is_full_accepts_an_explicit_cap(monkeypatch, tmp_path):
    sl = _slots(monkeypatch, tmp_path, cap=5)
    assert sl.acquire("a", log=lambda *_: None)
    assert sl.is_full(cap=1) is True
    assert sl.is_full(cap=0) is False


# ---------------------------------------------------------------- 反向前提：None 有两种含义

def test_nonblock_acquire_returns_none_both_when_full_and_when_off(monkeypatch, tmp_path):
    sl = _slots(monkeypatch, tmp_path, cap=1)
    assert sl.acquire("a", log=lambda *_: None)
    assert sl.acquire("b", nonblock=True, log=lambda *_: None) is None     # 满
    assert sl.is_full() is True
    off = _slots(monkeypatch, tmp_path / "off", cap=0)
    assert off.acquire("c", nonblock=True, log=lambda *_: None) is None    # 不仲裁
    assert off.is_full() is False                                           # 同样是 None，但不是「满」


# ---------------------------------------------------------------- _run_round：不仲裁时重发批要真的提交

class _Ctx:
    region = "JPN"
    settings = {"region": "JPN", "universe": "TOP1600"}


def _pipeline_mod():
    if str(TOOLKIT_SCRIPTS) not in sys.path:
        sys.path.insert(0, str(TOOLKIT_SCRIPTS))
    for m in ("pipeline", "review_wave", "metrics_cache", "gate", "_lib.rules",
              "_lib.region_kb", "_lib.wqb_store", "_lib.ledger", "_lib.common",
              "_lib.api", "_lib.poller", "_lib.slots", "_lib"):
        sys.modules.pop(m, None)
    return importlib.import_module("pipeline")


def test_run_round_resubmits_when_arbitration_is_off_and_fails_fast_instead_of_hanging(monkeypatch, tmp_path):
    pl = _pipeline_mod()
    culprit_errs = [
        {"child": "x", "status": "ERROR", "error": "Invalid data field close.", "expr": "rank(bad)"},
        {"child": "y", "status": "CANCELLED", "error": "CANCELLED", "expr": "rank(ok1)"},
    ]
    plan = {"ms1": ("ERROR", {"children": ["x", "y"]}, culprit_errs),
            "ms2": ("COMPLETE", {"children": []}, [])}
    order, submitted = list(plan), []

    def fake_submit(api, settings, exprs):
        msid = order[len(submitted)]
        submitted.append((msid, [pl.item_expr(e) for e in exprs]))
        return msid

    def fake_update(ck, bi, batch, msid, status, detail, api):
        rec = next((b for b in ck["batches"] if b.get("multisim") == msid), None) or {"exprs": batch, "multisim": msid}
        if rec not in ck["batches"]:
            ck["batches"].append(rec)
        rec["status"] = status
        if status == "ERROR":
            rec["errors"] = plan[msid][2]
        elif status == "COMPLETE":
            rec["alphas"] = ["A" + msid]
        return rec

    monkeypatch.setattr(pl, "submit_batch", fake_submit)
    monkeypatch.setattr(pl, "_poll_single_batch", lambda api, msid, pcfg, bi: (bi, plan[msid][0], plan[msid][1]))
    monkeypatch.setattr(pl, "_update_ck_batch", fake_update)
    monkeypatch.setattr(pl, "_mark_culprits_in_db", lambda ctx, wave, culprits: len(culprits))
    monkeypatch.setattr(pl, "ckpt_save", lambda ctx, ck, d: None)
    monkeypatch.setenv("WQB_GLOBAL_SLOTS", "0")                    # 不仲裁
    monkeypatch.setenv("WQB_SLOTS_DIR", str(tmp_path / "slots"))
    # 回归时快速失败：把「等外部释放槽位」的上限压到 0、sleep 打桩——旧实现会走到「放弃剩余批」，ms2 不会被提交
    monkeypatch.setattr(pl, "_EXTERNAL_SLOT_WAIT_SEC", 0)
    monkeypatch.setattr(pl.time, "sleep", lambda s: None)

    ck = {"wave": "7", "batches": [], "item_overrides": {}}
    pl._run_round(api=None, ctx=_Ctx(), ck=ck, round_batches=[["rank(bad)", "rank(ok1)"]],
                  n_slots=1, pcfg={}, checkpoint_dir=None, round_idx=1, pending_batches=[])
    assert submitted == [("ms1", ["rank(bad)", "rank(ok1)"]), ("ms2", ["rank(ok1)"])], \
        f"不仲裁时重发批没被提交（_refill 又把 None 当成了「槽位已满」）：{submitted}"
