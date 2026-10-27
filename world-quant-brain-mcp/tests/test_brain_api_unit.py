"""brain_api 单元测试 (MCP venv) — 提交前体检 / 配额估算 / 模型默认值 (无网络)。

导入 brain_api 即实例化 brain_client 单例 (不联网); 被测方法通过
`BrainApiClient.__new__` 构造空壳实例 + monkeypatch 平台方法, 避免真实请求。
"""
import asyncio

import pytest
import requests

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
# pre_submit_check (提交前体检 — 本地启发式)
# ---------------------------------------------------------------------------

def _details(sharpe=2.0, fitness=1.2, turnover=0.15, returns=0.08, margin=0.0010,
             region="EUR", checks=None):
    return {
        "settings": {"region": region, "delay": 1},
        "is": {
            "sharpe": sharpe, "fitness": fitness, "turnover": turnover,
            "returns": returns, "margin": margin,
            "checks": checks or [],
        },
    }


def make_shell():
    return BrainApiClient.__new__(BrainApiClient)


def test_pre_submit_pass():
    c = make_shell()
    r = c.pre_submit_check(_details())
    assert r["passed"] is True and r["failures"] == []


def test_pre_submit_sharpe_fail():
    c = make_shell()
    r = c.pre_submit_check(_details(sharpe=1.2))
    assert r["passed"] is False
    assert any("Sharpe" in f for f in r["failures"])


def test_pre_submit_turnover_local_window():
    c = make_shell()
    assert c.pre_submit_check(_details(turnover=0.02))["passed"] is False    # < 4%
    assert c.pre_submit_check(_details(turnover=0.45))["passed"] is False    # > 40%
    assert c.pre_submit_check(_details(turnover=0.15))["passed"] is True


def test_pre_submit_margin_is_warning_not_failure():
    """2026-08-13 修复回归: margin 是本地启发式, 平台不检查 — 只能 warning。
    EUR qMNEG2Z2 (6.12bp) 曾在此被误拦, 真实拒因是 PROD_CORRELATION。"""
    c = make_shell()
    r = c.pre_submit_check(_details(margin=0.000612, region="EUR"))
    assert r["passed"] is True                 # 不再拦截
    assert any("margin" in w.lower() for w in r["warnings"])


def test_pre_submit_captures_is_check_fail():
    c = make_shell()
    r = c.pre_submit_check(_details(checks=[{"name": "LOW_2Y_SHARPE", "result": "FAIL",
                                             "value": 1.2, "limit": 1.58}]))
    assert r["passed"] is False
    assert any("LOW_2Y_SHARPE" in f for f in r["failures"])


def test_pre_submit_no_is_data():
    c = make_shell()
    r = c.pre_submit_check({"settings": {"region": "EUR"}})
    assert r["passed"] is False and "No IS data" in r["reason"]


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


# ---------------------------------------------------------------------------
# get_datafields pagination contract (live-verified 2026-10-20)
#
# Regression for the 2026-10-18 analyst7 field profile that recorded 299/1111
# fields: dataset-scoped pulls were capped at 300 client-side. The platform
# (EUR/D1/TOP2500) paginates dataset-scoped queries to any depth at limit=50,
# caps `search` at the first 100 matches (offset+limit<=100, deeper = HTTP 400),
# and reports an *unfiltered* `count` under search.
# ---------------------------------------------------------------------------

@pytest.fixture
def fast_sleep(monkeypatch):
    async def _no_sleep(*_a, **_k):
        return None
    monkeypatch.setattr(asyncio, "sleep", _no_sleep)


def _mk_paged_client(responder):
    """Build an empty-shell client whose platform call is a responder.

    ``responder(offset, params)`` returns the page payload or raises.
    """
    c = make_shell()
    c.redis_client = None
    c._isos_data = None
    c.base_url = "https://api.worldquantbrain.com"
    calls = []
    cache = {}
    key_params = {}

    async def fake_auth():
        return None

    async def fake_req(method, url, *, op_name, **kwargs):
        params = kwargs["params"]
        calls.append(params["offset"])
        return responder(params["offset"], params)

    def fake_key(kind, params):
        key_params.update(params)
        return "k"

    c.ensure_authenticated = fake_auth
    c._request_json_with_retries = fake_req
    c.log = lambda *a, **k: None
    c._generate_cache_key = fake_key
    c._get_cached_data = lambda k: None
    c._set_cached_data = lambda k, payload, ttl=None: cache.update(payload=payload)
    return c, calls, cache, key_params


def _field_page(fields, offset, limit=50, count=None):
    return {"results": fields[offset:offset + limit],
            "count": len(fields) if count is None else count}


def _http_error(code):
    exc = requests.HTTPError("%d Client Error" % code)
    resp = requests.Response()
    resp.status_code = code
    exc.response = resp
    return exc


def test_get_datafields_scoped_pulls_past_old_300_cap(fast_sleep):
    """dataset.id pull must fetch all 1111 fields (23 pages), not stop at 300."""
    fields = [{"id": "f%d" % i, "name": "f%d" % i} for i in range(1111)]

    def responder(offset, _params):
        return _field_page(fields, offset)

    c, calls, cache, key_params = _mk_paged_client(responder)
    payload = asyncio.run(c.get_datafields(
        region="EUR", universe="TOP2500", delay=1,
        dataset_id="analyst7", filter_sharpe=False))

    assert payload["count"] == 1111
    assert len(payload["results"]) == 1111
    assert payload["platform_count"] == 1111
    assert payload["complete"] is True
    assert payload["pages_fetched"] == 23
    assert "pagination_truncated" not in payload
    assert calls == list(range(0, 1111, 50))
    # A complete dump is cached; the key carries the version that invalidates
    # pre-fix truncated dumps and the caller-owned cap.
    assert cache["payload"]["complete"] is True
    assert key_params["cache_version"] == 2 and key_params["max_fields"] is None


def test_get_datafields_scoped_http_error_is_fatal(fast_sleep):
    """A mid-pagination 4xx must raise, never return a silent partial catalog."""
    fields = [{"id": "f%d" % i} for i in range(150)]

    def responder(offset, _params):
        if offset == 50:
            raise _http_error(403)
        return _field_page(fields, offset, count=150)

    c, calls, cache, _ = _mk_paged_client(responder)
    with pytest.raises(requests.HTTPError):
        asyncio.run(c.get_datafields(
            region="EUR", universe="TOP2500", delay=1,
            dataset_id="analyst7", filter_sharpe=False))
    assert calls == [0, 50]
    assert "payload" not in cache


def test_get_datafields_scoped_short_page_raises(fast_sleep):
    """Ending short of the declared count is a failed catalog, not a smaller one."""
    fields = [{"id": "f%d" % i} for i in range(57)]

    def responder(offset, _params):
        # Platform claims 1111 but stops after 57 rows (silent truncation).
        return _field_page(fields, offset, count=1111)

    c, calls, cache, _ = _mk_paged_client(responder)
    with pytest.raises(RuntimeError, match="incomplete pull"):
        asyncio.run(c.get_datafields(
            region="EUR", universe="TOP2500", delay=1,
            dataset_id="analyst7", filter_sharpe=False))
    assert calls == [0, 50]
    assert "payload" not in cache


def test_get_datafields_scoped_no_progress_raises(fast_sleep):
    """Repeated rows from a shifting offset window must not pass as progress."""
    page = [{"id": "f%d" % i} for i in range(50)]

    def responder(offset, _params):
        return {"results": page, "count": 1111}

    c, calls, cache, _ = _mk_paged_client(responder)
    with pytest.raises(RuntimeError, match="no progress"):
        asyncio.run(c.get_datafields(
            region="EUR", universe="TOP2500", delay=1,
            dataset_id="analyst7", filter_sharpe=False))
    assert calls == [0, 50]
    assert "payload" not in cache


def test_get_datafields_search_window_is_reported_and_not_cached(fast_sleep):
    """Search exposes only the first 100 matches and must never be cached."""
    fields = [{"id": "x_field_%d" % i, "name": "x_field_%d" % i}
              for i in range(150)]

    def responder(offset, _params):
        # Under search the platform count is the unfiltered total (4757).
        return _field_page(fields, offset, count=4757)

    c, calls, cache, _ = _mk_paged_client(responder)
    payload = asyncio.run(c.get_datafields(
        region="EUR", universe="TOP2500", delay=1,
        search="x", filter_sharpe=False))

    assert calls == [0, 50]                      # no third page request
    assert payload["count"] == 100
    assert payload["platform_count"] == 4757
    assert payload["complete"] is False
    assert payload["pagination_truncated"] is True
    assert payload["truncated_reason"] == "search_window_capped"
    assert "payload" not in cache


def test_get_datafields_search_400_past_window_stops_cleanly(fast_sleep):
    """Platform-side 400 beyond the search window is a window cap, not a failure."""
    fields = [{"id": "x_field_%d" % i, "name": "x_field_%d" % i}
              for i in range(150)]

    def responder(offset, _params):
        if offset > 0:
            raise _http_error(400)   # platform rejects search offset>=50 here
        return _field_page(fields, offset, count=4757)

    c, calls, cache, _ = _mk_paged_client(responder)
    payload = asyncio.run(c.get_datafields(
        region="EUR", universe="TOP2500", delay=1,
        search="x", filter_sharpe=False))
    assert calls == [0, 50]
    assert payload["count"] == 50
    assert payload["truncated_reason"] == "search_window_capped"
    assert payload["complete"] is False
    assert "payload" not in cache


def test_get_datafields_unscoped_default_cap_is_declared(fast_sleep):
    """Unscoped dumps keep the 300-row guard but must report it as truncated."""
    fields = [{"id": "f%d" % i} for i in range(4757)]

    def responder(offset, _params):
        return _field_page(fields, offset)

    c, calls, cache, _ = _mk_paged_client(responder)
    payload = asyncio.run(c.get_datafields(
        region="EUR", universe="TOP2500", delay=1, filter_sharpe=False))

    assert payload["count"] == 300
    assert payload["platform_count"] == 4757
    assert payload["complete"] is False
    assert payload["pagination_truncated"] is True
    assert payload["truncated_reason"] == "max_fields_cap"
    assert payload["pages_fetched"] == 6
    assert calls == [0, 50, 100, 150, 200, 250]
    # The intentional capped listing is still cacheable.
    assert cache["payload"]["truncated_reason"] == "max_fields_cap"


def test_get_datafields_scoped_respects_explicit_max_fields(fast_sleep):
    """An explicit caller cap on a scoped pull is honoured and reported."""
    fields = [{"id": "f%d" % i} for i in range(1111)]

    def responder(offset, _params):
        return _field_page(fields, offset)

    c, calls, cache, key_params = _mk_paged_client(responder)
    payload = asyncio.run(c.get_datafields(
        region="EUR", universe="TOP2500", delay=1,
        dataset_id="analyst7", filter_sharpe=False, max_fields=120))

    assert payload["count"] == 120
    assert payload["truncated_reason"] == "max_fields_cap"
    assert payload["complete"] is False
    assert calls == [0, 50, 100]
    assert key_params["max_fields"] == 120
