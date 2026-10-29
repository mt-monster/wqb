# -*- coding: utf-8 -*-
"""相关性消费方的「缓存优先」语义守卫（2026-10-28 P0-3）。

改的是一条**默认值**，而默认值最容易在重构中悄悄回退（旧版三个消费方都无条件
``refresh=True``：每查一条都强制平台重算，账号级单并发下代价 195s 冷却 / 次）。
本文件钉三件事：

1. ``tools/corr_check.py::_query`` 把 ``refresh`` 原样透传，缺省 False；
2. ``tools/verdict/submit_inventory.py::fetch_corr`` 的返回形态与 provisional 语义
   （预读值 ⇒ ``provisional=True``，调用方不得记成「刚测过」）；
3. ``fetch_corr`` 的 busy 退避、self 回退、终态不重试；
4. **AST 反查**：provisional 分支里不得出现 ``save_ckpt`` / ``persist_live_corr``
   （写下去就把「测量时间不可知」污染成「刚测过」，48h 保鲜判据失效），
   ``tools/data-repair/check_corr.py`` 的 ``--refresh`` 必须是显式开关。

全部离线：brain 用假对象，sleep 用桩，不碰平台与生产库。
"""
from __future__ import annotations

import ast
import asyncio
import importlib.util
import sys
import types
from pathlib import Path
from types import SimpleNamespace

import pytest

ROOT = Path(__file__).resolve().parents[3]
for _p in (str(ROOT / "src"), str(ROOT / "world-quant-brain-mcp")):
    if str(_p) not in sys.path:
        sys.path.insert(0, str(_p))

CORR_CHECK = ROOT / "tools" / "corr_check.py"
SUBMIT_INVENTORY = ROOT / "tools" / "verdict" / "submit_inventory.py"
REPAIR_CHECK = ROOT / "tools" / "data-repair" / "check_corr.py"


def _load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


@pytest.fixture(scope="module")
def corr_check():
    return _load(CORR_CHECK, "corr_check_under_test")


@pytest.fixture(scope="module")
def submit_inventory():
    return _load(SUBMIT_INVENTORY, "submit_inventory_under_test")


@pytest.fixture(scope="module")
def repair_check():
    return _load(REPAIR_CHECK, "repair_check_under_test")


# ---------------------------------------------------------------- corr_check._query
class _RecordingBrain:
    def __init__(self, responses):
        self.responses = list(responses)
        self.calls: list = []

    async def check_correlation(self, aid, correlation_type="production",
                                threshold=0.7, refresh=False):
        self.calls.append({"aid": aid, "type": correlation_type,
                           "threshold": threshold, "refresh": refresh})
        r = self.responses.pop(0)
        if isinstance(r, Exception):
            raise r
        return r


def _args(**kw):
    base = dict(threshold=0.7, refresh=False)
    base.update(kw)
    return SimpleNamespace(**base)


class TestCorrCheckQuery:
    def test_default_is_cache_first_and_shape_maps(self, corr_check):
        brain = _RecordingBrain([{
            "all_passed": True,
            "checks": {"production": {
                "max_correlation": 0.55, "source": "cache:corr_cache",
                "from_cache": True, "provisional": False}},
        }])
        got: dict = {}
        statuses, ra = asyncio.run(
            corr_check._query(brain, "A1", ["production"], _args(), got))
        assert brain.calls[0]["refresh"] is False, "缺省必须缓存优先"
        assert brain.calls[0]["threshold"] == 0.7
        assert got["A1"]["production"] == {
            "max": 0.55, "pass_": True, "source": "cache:corr_cache",
            "provisional": False, "from_cache": True}
        assert statuses == {} and ra == 0.0

    def test_refresh_flag_is_propagated(self, corr_check):
        brain = _RecordingBrain([{"checks": {"production": {"max_correlation": 0.4}}}])
        asyncio.run(corr_check._query(brain, "A1", ["production"],
                                      _args(refresh=True), {}))
        assert brain.calls[0]["refresh"] is True

    def test_second_round_skips_types_already_answered(self, corr_check):
        brain = _RecordingBrain([])
        got = {"A1": {"production": {"max": 0.4}}}
        statuses, _ra = asyncio.run(
            corr_check._query(brain, "A1", ["production"], _args(), got))
        assert brain.calls == [] and statuses == {}

    def test_pending_status_and_retry_after_surfaced(self, corr_check):
        brain = _RecordingBrain([{
            "status": "correlation_busy",
            "retry_after": 180,
            "inflight": True,
            "checks": {"production": {"status": "correlation_busy",
                                      "retry_after": 180}},
        }])
        got: dict = {}
        statuses, ra = asyncio.run(
            corr_check._query(brain, "A1", ["production"], _args(), got))
        assert statuses == {"production": "correlation_busy"}
        assert ra == 180.0
        assert got == {}, "busy/pending 不是数值，不得写进 got"

    def test_exception_marks_error_without_aborting(self, corr_check):
        brain = _RecordingBrain([RuntimeError("boom")])
        got: dict = {}
        statuses, ra = asyncio.run(
            corr_check._query(brain, "A1", ["production"], _args(), got))
        assert statuses == {"production": "error"} and ra == 0.0 and got == {}

    def test_types_are_independent(self, corr_check):
        brain = _RecordingBrain([
            {"checks": {"production": {"max_correlation": 0.5}}},
            {"checks": {"self": {"max_correlation": 0.2}}},
        ])
        got: dict = {}
        asyncio.run(corr_check._query(brain, "A1", ["production", "self"],
                                      _args(), got))
        assert [c["type"] for c in brain.calls] == ["production", "self"]
        assert got["A1"]["self"]["max"] == 0.2


# ---------------------------------------------------------------- submit_inventory.fetch_corr
class _CorrBrain:
    def __init__(self, corr_results, self_results=None):
        self.corr_results = list(corr_results)
        self.self_results = list(self_results or [])
        self.calls: list = []
        self.self_calls: list = []

    async def check_correlation(self, aid, correlation_type="production",
                                threshold=0.7, refresh=False):
        self.calls.append({"aid": aid, "type": correlation_type,
                           "threshold": threshold, "refresh": refresh})
        r = self.corr_results.pop(0)
        if isinstance(r, Exception):
            raise r
        return r

    async def check_self_correlation(self, aid, correlation_type="self"):
        self.self_calls.append(aid)
        r = self.self_results.pop(0)
        if isinstance(r, Exception):
            raise r
        return r


def _ok(prod, selfc=None, *, source="platform_poll", from_cache=False,
        provisional=False, cached_at=None):
    return {
        "status": "ok", "all_passed": True,
        "checks": {
            "production": {"max_correlation": prod, "source": source,
                           "from_cache": from_cache, "provisional": provisional,
                           "cached_at": cached_at},
            "self": {"max_correlation": selfc},
        },
    }


class TestFetchCorr:
    def test_cache_hit_shape(self, submit_inventory):
        brain = _CorrBrain([_ok(0.51, 0.2, source="cache:corr_cache",
                                from_cache=True, cached_at="2026-10-27T00:00:00")])
        r = asyncio.run(submit_inventory.fetch_corr(brain, "A1", False, 10))
        assert brain.calls[0]["refresh"] is False
        assert r["status"] == "ok"
        assert r["prod"] == 0.51 and r["self"] == 0.2
        assert r["from_cache"] is True and r["cached_at"] == "2026-10-27T00:00:00"
        assert r["provisional"] is False and r["prod_source"] == "cache:corr_cache"
        assert r["source"] == "platform_live"
        assert brain.self_calls == []

    def test_pre_read_marks_provisional(self, submit_inventory):
        brain = _CorrBrain([_ok(0.62, 0.1, source="alpha_detail_cached",
                                provisional=True)])
        r = asyncio.run(submit_inventory.fetch_corr(brain, "A1", False, 10))
        assert r["provisional"] is True
        assert r["prod_source"] == "alpha_detail_cached"
        assert r["from_cache"] is False and r["cached_at"] is None

    def test_busy_retries_once_after_retry_after(self, submit_inventory, monkeypatch):
        slept: list = []

        async def _sleep(sec):
            slept.append(sec)
        monkeypatch.setattr(submit_inventory, "asyncio",
                            types.SimpleNamespace(sleep=_sleep))
        brain = _CorrBrain([
            {"status": "correlation_busy", "retry_after": 5},
            _ok(0.5, 0.2),
        ])
        r = asyncio.run(submit_inventory.fetch_corr(brain, "A1", False, max_wait=10))
        assert r["status"] == "ok" and r["prod"] == 0.5
        assert slept == [5.0] and len(brain.calls) == 2
        assert [c["refresh"] for c in brain.calls] == [False, False]

    def test_busy_beyond_window_is_not_retried(self, submit_inventory, monkeypatch):
        async def _no_sleep(_sec):
            pytest.fail("超过窗口的 retry_after 不该再睡")
        monkeypatch.setattr(submit_inventory, "asyncio",
                            types.SimpleNamespace(sleep=_no_sleep))
        brain = _CorrBrain([{"status": "correlation_busy", "retry_after": 300}])
        r = asyncio.run(submit_inventory.fetch_corr(brain, "A1", False, max_wait=10))
        assert r == {"status": "correlation_busy"}
        assert len(brain.calls) == 1

    def test_terminal_status_is_returned_verbatim(self, submit_inventory):
        brain = _CorrBrain([{"status": "data_unavailable",
                             "retry_after": 0}])
        r = asyncio.run(submit_inventory.fetch_corr(brain, "A1", False, 10))
        assert r == {"status": "data_unavailable"} and len(brain.calls) == 1

    def test_self_falls_back_to_local_pool_endpoint(self, submit_inventory):
        brain = _CorrBrain([_ok(0.5, None)], self_results=[{"max_correlation": 0.16}])
        r = asyncio.run(submit_inventory.fetch_corr(brain, "A1", False, 10))
        assert r["self"] == 0.16
        assert r["source"] == "platform_live+self_local_pool"
        assert brain.self_calls == ["A1"]

    def test_self_fallback_failure_keeps_none(self, submit_inventory):
        brain = _CorrBrain([_ok(0.5, None)], self_results=[RuntimeError("x")])
        r = asyncio.run(submit_inventory.fetch_corr(brain, "A1", False, 10))
        assert r["self"] is None and r["source"] == "platform_live"

    def test_platform_exception_becomes_status(self, submit_inventory):
        brain = _CorrBrain([RuntimeError("token expired")])
        r = asyncio.run(submit_inventory.fetch_corr(brain, "A1", False, 10))
        assert r["status"].startswith("RuntimeError")


# ---------------------------------------------------------------- 结构性反查
class TestProvisionalMustNotPersist:
    def _fn(self, path: Path, name: str):
        tree = ast.parse(path.read_text(encoding="utf-8"))
        for node in tree.body:
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name == name:
                return node
        pytest.fail(f"{path.name} 找不到 {name}()")

    def test_provisional_branch_writes_no_checkpoint(self, submit_inventory):
        run = self._fn(SUBMIT_INVENTORY, "run")   # 逐条汇总在主循环 run() 里
        branches = [
            n for n in ast.walk(run)
            if isinstance(n, ast.If) and "provisional" in ast.unparse(n.test)
        ]
        assert branches, "run() 里找不到 provisional 分支（口径漂移？）"
        banned = {"save_ckpt", "persist_live_corr"}
        for br in branches:
            calls = set()
            for n in ast.walk(ast.Module(body=br.body, type_ignores=[])):
                if isinstance(n, ast.Call):
                    name = getattr(n.func, "id", None) or getattr(n.func, "attr", None)
                    if name:
                        calls.add(name)
            # 只钉「预读分支体内」不落盘；else 分支（实测值）照常写
            assert not (calls & banned), f"provisional 分支不得 {sorted(calls & banned)}"
            src = ast.unparse(ast.Module(body=br.body, type_ignores=[]))
            assert "platform_pre_read" in src and "corr_provisional" in src

    def test_repair_check_refresh_is_opt_in(self, repair_check):
        tree = ast.parse(REPAIR_CHECK.read_text(encoding="utf-8"))
        fn = next(n for n in tree.body
                  if isinstance(n, ast.AsyncFunctionDef) and n.name == "main")
        args = [a.arg for a in fn.args.args]
        assert args[1] == "refresh"
        assert isinstance(fn.args.defaults[0], ast.Constant)
        assert fn.args.defaults[0].value is False, "缺省必须是缓存优先"

    def test_repair_check_main_default_does_not_refresh(self, repair_check, monkeypatch):
        calls: list = []

        class _B:
            async def ensure_authenticated(self):
                return None

            async def check_self_correlation(self, aid):
                return {"max_correlation": 0.1}

            async def check_correlation(self, aid, refresh=False):
                calls.append(refresh)
                return {"status": "ok"}

        monkeypatch.setattr(repair_check, "brain_client", _B())
        asyncio.run(repair_check.main("A1"))
        asyncio.run(repair_check.main("A1", refresh=True))
        assert calls == [False, True]

    def test_repair_check_flag_gate_reads_dash_refresh(self):
        src = REPAIR_CHECK.read_text(encoding="utf-8")
        assert 'refresh="--refresh" in flags' in src.replace("'", '"')
        assert 'check_correlation(aid, refresh=refresh)' in src

    def test_corr_check_has_refresh_store_true(self):
        tree = ast.parse(CORR_CHECK.read_text(encoding="utf-8"))
        found = False
        for n in ast.walk(tree):
            if not isinstance(n, ast.Call):
                continue
            name = getattr(n.func, "attr", None)
            if name != "add_argument":
                continue
            strs = [a.value for a in n.args if isinstance(a, ast.Constant)]
            if "--refresh" in strs:
                kws = {kw.arg: kw.value for kw in n.keywords}
                assert isinstance(kws.get("action"), ast.Constant)
                assert kws["action"].value == "store_true"
                found = True
        assert found, "--refresh 必须存在且是 store_true（缺省 False）"
