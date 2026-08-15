"""brain_api 单元测试 (MCP venv) — 提交前体检 / 配额估算 / 模型默认值 (无网络)。

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
# get_submission_quota (48h rolling, mock OS 池)
# ---------------------------------------------------------------------------

def _mk_quota_client(results):
    c = make_shell()

    async def fake_get_user_alphas(**kwargs):
        return {"results": results}

    c.get_user_alphas = fake_get_user_alphas
    return c


def test_quota_estimate_window():
    import datetime as dt
    now = dt.datetime.now(dt.timezone.utc)

    def sub(ago_h, aid):
        return {"id": aid, "dateSubmitted": (now - dt.timedelta(hours=ago_h)).isoformat()}

    c = _mk_quota_client([sub(1, "a1"), sub(20, "a2"), sub(60, "a3")])
    q = asyncio.run(c.get_submission_quota(window_hours=48, limit=4))
    assert q["used"] == 2 and q["remaining"] == 2
    assert q["hours_until_release"] is not None


def test_quota_estimate_exhausted():
    import datetime as dt
    now = dt.datetime.now(dt.timezone.utc)

    def sub(ago_h, aid):
        return {"id": aid, "dateSubmitted": (now - dt.timedelta(hours=ago_h)).isoformat()}

    c = _mk_quota_client([sub(1, "a1"), sub(2, "a2"), sub(3, "a3"), sub(4, "a4")])
    q = asyncio.run(c.get_submission_quota())
    assert q["remaining"] == 0


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
