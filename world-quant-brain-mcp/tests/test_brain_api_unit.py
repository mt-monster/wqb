"""brain_api 单元测试 (MCP venv) — 模型默认值 / datafields 检索 (无网络)。

导入 brain_api 即实例化 brain_client 单例 (不联网); 被测方法通过
`BrainApiClient.__new__` 构造空壳实例 + monkeypatch 平台方法, 避免真实请求。
"""
import asyncio

import pytest

import brain_api
from brain_api import BrainApiClient, SimulationData, SimulationSettings


# ---------------------------------------------------------------------------
# 模型默认值
# ---------------------------------------------------------------------------

def test_simulation_settings_defaults():
    s = SimulationSettings()
    assert s.region == "USA"
    assert s.delay == 1
    assert s.universe == "TOP3000"
    assert s.language == "FASTEXPR"
    assert s.truncation == 0.0


def test_singleton_exists():
    assert isinstance(brain_api.brain_client, BrainApiClient)
    assert brain_api.brain_client.base_url


# ---------------------------------------------------------------------------
# pre_submit_check tests removed (2026-10-02) — 方法已删除
# ---------------------------------------------------------------------------
# 旧 pre_submit_check 是宽松的本地启发式（Sharpe>1.3 / Fitness>0.75 / Turnover 4%-40% /
# Returns>4%，预检异常即放行 = fail-open），2026-09-29 起提交路由改用 fail-closed 的
# src/wqb/workflow/nodes/submit_alpha.py::_submit_gate，生产调用方为 0，方法与其单测已于
# 2026-10-02 一并删除（skills 审查 SP-13 / T0-4 / 步 8 评估 F10）。
# 新的口径守护在 tests/unit/01_store_db/test_threshold_relations.py::test_submit_gate_thresholds_are_pinned。


def make_shell():
    return BrainApiClient.__new__(BrainApiClient)


# ---------------------------------------------------------------------------
# get_submission_quota tests removed (2026-08-25 user request)
# ---------------------------------------------------------------------------
# def _mk_quota_client(results): ...
# def test_quota_estimate_window(): ...
# def test_quota_estimate_exhausted(): ...
# def test_quota_daily_view(): ...


# ---------------------------------------------------------------------------
# get_datafields targeted search (must hit platform, not unscoped dump cache)
# ---------------------------------------------------------------------------

def test_get_datafields_passes_search_to_api():
    c = make_shell()
    c.redis_client = None
    c._isos_data = None
    c.base_url = "https://api.worldquantbrain.com"
    captured = {}

    async def fake_auth():
        return None

    async def fake_req(method, url, *, op_name, **kwargs):
        captured["params"] = kwargs.get("params")
        fid = "probability_label1_2quantile_20day_eur_ohlcma"
        return {"results": [{"id": fid, "name": fid}], "count": 1}

    c.ensure_authenticated = fake_auth
    c._request_json_with_retries = fake_req
    c.log = lambda *a, **k: None
    c._generate_cache_key = lambda *a, **k: "k"
    c._get_cached_data = lambda k: (_ for _ in ()).throw(AssertionError("search must not read unscoped cache"))
    c._set_cached_data = lambda *a, **k: (_ for _ in ()).throw(AssertionError("search must not write unscoped cache"))

    fid = "probability_label1_2quantile_20day_eur_ohlcma"
    payload = asyncio.run(c.get_datafields(
        region="EUR", universe="TOP1200", delay=1, search=fid, filter_sharpe=False))
    assert captured["params"]["search"] == fid
    assert "dataset.id" not in captured["params"]
    assert payload["results"][0]["id"] == fid


def test_get_datafields_unscoped_omits_search_param():
    c = make_shell()
    c.redis_client = None
    c._isos_data = None
    c.base_url = "https://api.worldquantbrain.com"
    captured = {}

    async def fake_auth():
        return None

    async def fake_req(method, url, *, op_name, **kwargs):
        captured["params"] = kwargs.get("params")
        return {"results": [{"id": "close", "name": "close"}], "count": 1}

    c.ensure_authenticated = fake_auth
    c._request_json_with_retries = fake_req
    c.log = lambda *a, **k: None
    c._generate_cache_key = lambda *a, **k: "k"
    c._get_cached_data = lambda k: None
    c._set_cached_data = lambda *a, **k: None

    asyncio.run(c.get_datafields(region="EUR", universe="TOP1200", delay=1, filter_sharpe=False))
    assert "search" not in captured["params"]
