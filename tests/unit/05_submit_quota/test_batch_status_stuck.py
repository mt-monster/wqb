# -*- coding: utf-8 -*-
"""2026-11-23：`tools/batch_status.py` 死批判据（用户「三、优化空间」第 4 条落地）。

背景：KOR imb5 T2 批（45NT32bLm5439bbuq32Q06r）在 20min 时被人工判死并重发，
结果原批与重发批最终都 COMPLETE——平台只是排队/注册慢。判死过早白烧一批配额。

判据必须是**三条件同时成立**，单次查询不足以判死：
  ① 进度停滞（同一 progress 指纹）
  ② children=0（未注册）
  ③ 停滞时长 ≥ stuck_after（缺省 25min）
"""
import importlib.util
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[3]


def _load():
    spec = importlib.util.spec_from_file_location(
        "batch_status_stuck", REPO_ROOT / "tools" / "batch_status.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _batch(bid="B1", child_count=0, terminal=0, progress=0.35, all_terminal=False):
    return {
        "batch_id": bid,
        "kind": "multisim",
        "child_count": child_count,
        "terminal": terminal,
        "all_terminal": all_terminal,
        "children": [],
        "parent_progress": progress,
    }


def test_first_seen_is_not_stuck():
    """单次查询（首次见到）绝不能判死——这是 20min 误判的根因。"""
    mod = _load()
    state = {}
    out = mod.detect_stuck([_batch()], state, now=1000.0, stuck_after=1500)
    assert out[0]["verdict"] == "OK"
    assert out[0]["stalled_s"] == 0.0


def test_stalled_past_threshold_is_stuck_suspect():
    mod = _load()
    state = {}
    b = _batch()
    mod.detect_stuck([b], state, now=1000.0, stuck_after=1500)   # 首次登记
    out = mod.detect_stuck([b], state, now=2600.0, stuck_after=1500)  # 1601s 后
    assert out[0]["verdict"] == "STUCK_SUSPECT"
    assert out[0]["stalled_s"] >= 1500


def test_stalled_but_under_threshold_is_ok():
    """20min(1200s) < 25min 阈值 ⇒ 仍 OK（对应 KOR T2 误判场景）。"""
    mod = _load()
    state = {}
    b = _batch()
    mod.detect_stuck([b], state, now=1000.0, stuck_after=1500)
    out = mod.detect_stuck([b], state, now=2200.0, stuck_after=1500)  # 1200s
    assert out[0]["verdict"] == "OK"


def test_progress_change_resets_clock():
    """进度推进（0.35→0.8）⇒ 重新计时，不得判死（平台在推进）。"""
    mod = _load()
    state = {}
    mod.detect_stuck([_batch(progress=0.35)], state, now=1000.0, stuck_after=1500)
    out = mod.detect_stuck([_batch(progress=0.8)], state, now=3000.0, stuck_after=1500)
    assert out[0]["verdict"] == "OK"
    assert out[0]["stalled_s"] == 0.0


def test_children_registered_is_not_stuck():
    """children 已注册（哪怕 0/8 terminal）⇒ 不是"注册滞后"，不适用死批判据。"""
    mod = _load()
    state = {}
    b = _batch(child_count=8, terminal=0, progress=None)
    mod.detect_stuck([b], state, now=1000.0, stuck_after=1500)
    out = mod.detect_stuck([b], state, now=9000.0, stuck_after=1500)
    assert out[0]["verdict"] == "OK"


def test_terminal_batch_never_stuck():
    mod = _load()
    state = {}
    b = _batch(all_terminal=True)
    mod.detect_stuck([b], state, now=1000.0, stuck_after=1500)
    out = mod.detect_stuck([b], state, now=9000.0, stuck_after=1500)
    assert out[0]["verdict"] == "OK"


def test_non_queue_progress_is_not_stuck():
    """progress=0.9（已过排队期）即使 children=0 也不属于"排队卡死"形态。"""
    mod = _load()
    state = {}
    b = _batch(progress=0.9)
    mod.detect_stuck([b], state, now=1000.0, stuck_after=1500)
    out = mod.detect_stuck([b], state, now=9000.0, stuck_after=1500)
    assert out[0]["verdict"] == "OK"


def test_multiple_batches_independent_state():
    mod = _load()
    state = {}
    a = _batch("A", progress=0.35)
    b = _batch("B", progress=0.15)
    mod.detect_stuck([a, b], state, now=1000.0, stuck_after=1500)
    out = mod.detect_stuck([a, b], state, now=3000.0, stuck_after=1500)
    assert {o["batch_id"]: o["verdict"] for o in out} == {
        "A": "STUCK_SUSPECT", "B": "STUCK_SUSPECT"}


def test_fetch_one_carries_progress():
    """fetch_one 必须把 progress 带出来，否则 detect_stuck 拿不到指纹。"""
    import asyncio

    mod = _load()

    class _Resp:
        status_code = 200
        text = "x"

        def json(self):
            return {"status": "RUNNING", "progress": 0.35}

    class _Brain:
        base_url = "https://api.example"

        async def ensure_authenticated(self):
            pass

        async def _request(self, method, url, **kw):
            return _Resp()

        def _simulation_error_message(self, data):
            return ""

    out = asyncio.run(mod.fetch_one(_Brain(), "https://api.example/simulations/X"))
    assert out["progress"] == 0.35


def test_repeated_detect_does_not_reset_clock():
    """同 progress 指纹反复调用不得重置停滞时钟（只有 progress 变化才重置）。"""
    mod = _load()
    state = {}
    b = _batch()
    mod.detect_stuck([b], state, now=1000.0, stuck_after=1500)
    r1 = mod.detect_stuck([b], state, now=3000.0, stuck_after=1500)
    r2 = mod.detect_stuck([b], state, now=3001.0, stuck_after=1500)
    assert r1[0]["verdict"] == "STUCK_SUSPECT"
    assert r2[0]["stalled_s"] == pytest.approx(2001.0)  # 从首次见到算起，未重置
