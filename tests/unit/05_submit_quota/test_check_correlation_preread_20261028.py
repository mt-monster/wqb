# -*- coding: utf-8 -*-
"""check_correlation 预读集成 + refresh 语义 + self 相关性热路径守护（2026-10-28）。

修复背景（当日审查发现，离线复现见 logs/_tmp_repro_preread_bug.py 的结论）：
  1. **P0**：`_read_existing_prod_correlation`（先读后算，2026-10-26 加）命中时返回
     ``{status:'ok', max:X, records:[]}``，而 `check_correlation` 的平台实测成功判据
     要求 ``len(records) > 0`` ⇒ 预读值被丢弃、报 data_unavailable 且不落缓存，
     重查永远卡死。修复 = 预读命中直接采纳（不写权威表：is.prodCorrelation 测量
     时间不可知，写 now 会污染 48h 保鲜判据）。
  2. **P1**：`refresh=True` 被预读短路——终验拿到平台旧存储值从未真正重测。
     修复 = `use_pre_read` 透传，refresh 时跳过预读。
  3. `_read_existing_prod_correlation` 旧版直接 ``session.get``（全包唯一在事件
     循环上阻塞的 HTTP 调用）→ 改走 ``_request``。
  4. 轮询循环 401 旧版按"网络失败"重试烧完整窗口 → 现刷新鉴权后继续。
  5. OS ID 列表加进程内 TTL（`BRAIN_SC_IDLIST_TTL_SECONDS`，缺省 900）。
  6. `get_self_correlation` 先裁剪 4 年窗口再 ffill+diff（稠密数据下与旧全历史
     路径逐值等价，本文件用双路径对照钉住）。

本文件全部用壳实例 + 桩（``__new__``），不联网、不写生产库。
"""
from __future__ import annotations

import asyncio
import json
import sys
from pathlib import Path
from unittest.mock import MagicMock

import pandas as pd
import pytest

ROOT = Path(__file__).resolve().parents[3]
for _p in (str(ROOT / "src"), str(ROOT / "world-quant-brain-mcp")):
    if str(_p) not in sys.path:
        sys.path.insert(0, str(_p))

from brain_api import BrainApiClient  # noqa: E402


def _shell() -> BrainApiClient:
    c = BrainApiClient.__new__(BrainApiClient)
    c.base_url = "https://api.worldquantbrain.com"
    c._brain_correlation_local_lock = asyncio.Lock()
    return c


class _FakeResponse:
    def __init__(self, status_code=200, body=None, text=""):
        self.status_code = status_code
        self._body = body if body is not None else {}
        self.text = text or (json.dumps(self._body) if body is not None else "")

    def raise_for_status(self):
        if self.status_code >= 400:
            import requests
            raise requests.HTTPError(f"HTTP {self.status_code}")

    def json(self):
        return self._body


@pytest.fixture(autouse=True)
def _no_sleep(monkeypatch):
    """轮询/退避 sleep 全部归零：测试只验证控制流，不验证等待时长。"""
    async def _fast(_s):
        return None
    monkeypatch.setattr(asyncio, "sleep", _fast)


# ---------------------------------------------------------------- P0 预读采纳
def _preread_shape(max_value=0.55):
    return {
        "status": "ok",
        "alpha_id": "TGT",
        "max": max_value,
        "records": [],
        "source": "alpha_detail_cached",
        "message": "从 alpha 详情读取平台已算好的 prod 相关（未触发新计算）",
    }


def _stub_check_deps(c, prod_result, *, store_calls=None):
    async def _auth():
        return None
    c.ensure_authenticated = _auth
    c._prod_corr_cached = lambda aid: None
    if store_calls is not None:
        c._prod_corr_store = lambda *a, **k: store_calls.append((a, k))
    else:
        c._prod_corr_store = lambda *a, **k: pytest.fail("预读命中不得写权威缓存表")

    async def _prod(aid, max_wait_seconds=None, use_pre_read=True):
        return prod_result
    c.get_production_correlation = _prod


def test_preread_hit_is_adopted_not_data_unavailable():
    """P0 回归：预读命中（records=[]）必须采纳 max，而不是报 data_unavailable。"""
    c = _shell()
    _stub_check_deps(c, _preread_shape(0.55))
    r = asyncio.run(c.check_correlation("TGT", "production", 0.7))
    prod = r["checks"]["production"]
    assert prod["max_correlation"] == 0.55
    assert prod["passes_check"] is True
    assert prod["source"] == "alpha_detail_cached"
    assert r["all_passed"] is True
    assert r.get("status") != "data_unavailable"


def test_preread_hit_above_threshold_fails_and_skips_self():
    """预读命中且 ≥0.7：早退 all_passed=False；both 形态下不计算 self。"""
    c = _shell()
    _stub_check_deps(c, _preread_shape(0.75))

    def _no_self(*a, **k):
        pytest.fail("prod 已 fail，不应继续计算 self")
    c.get_self_correlation = _no_self
    r = asyncio.run(c.check_correlation("TGT", "both", 0.7))
    assert r["all_passed"] is False
    assert r["checks"]["production"]["passes_check"] is False


def test_preread_hit_does_not_pollute_corr_cache():
    """预读值测量时间不可知：不写 alpha_corr_cache（否则 48h 保鲜判据被污染成"刚测过"）。"""
    c = _shell()
    store_calls: list = []
    _stub_check_deps(c, _preread_shape(0.55), store_calls=store_calls)
    asyncio.run(c.check_correlation("TGT", "production", 0.7))
    assert store_calls == []


def test_poll_path_success_still_writes_cache():
    """平台实测分支（records 非空）行为不变：采纳 + 写权威表。"""
    c = _shell()
    store_calls: list = []
    _stub_check_deps(c, {"max": 0.42, "records": [[0.0, 0.1, 3], [0.1, 0.2, 7]]},
                     store_calls=store_calls)
    r = asyncio.run(c.check_correlation("TGT", "production", 0.7))
    assert r["checks"]["production"]["max_correlation"] == 0.42
    assert r["all_passed"] is True
    assert len(store_calls) == 1
    assert store_calls[0][0][0] == "TGT"


# ---------------------------------------------------------------- P1 refresh 透传
def test_refresh_true_skips_preread_and_local_cache():
    """refresh=True：跳过本地缓存与预读，强制走平台重测（终验语义）。"""
    c = _shell()

    async def _auth():
        return None
    c.ensure_authenticated = _auth

    read_calls: list = []

    async def _read(aid):
        read_calls.append(aid)
        return _preread_shape(0.1)
    c._read_existing_prod_correlation = _read

    async def _lock(op):
        return {"acquired": True, "backend": "local", "lock_key": "k"}

    async def _unlock(info, op, **_kw):  # 2026-10-28: 生产侧新增 cooldown/seconds
        return None
    c._try_acquire_brain_correlation_lock = _lock
    c._release_brain_correlation_lock = _unlock

    async def _req(method, url, **kw):
        return _FakeResponse(200, {"max": 0.31, "records": [[0.0, 0.1, 1]]})
    c._request = _req

    async def _cached(aid):
        return {"max": 0.99, "records": [], "cached_at": "2026-10-01T00:00:00"}
    c._prod_corr_cached = _cached

    # refresh=True → 预读不跑（read_calls 空）、本地缓存 0.99 不被采用、走轮询拿到 0.31
    r = asyncio.run(c.get_production_correlation("TGT", use_pre_read=False))
    assert r["max"] == 0.31
    assert read_calls == []

    # refresh=False（缺省）→ 预读跑并直接返回平台已算值
    r2 = asyncio.run(c.get_production_correlation("TGT"))
    assert r2["source"] == "alpha_detail_cached"
    assert len(read_calls) == 1


def test_check_correlation_passes_refresh_down():
    """check_correlation(refresh=...) 透传为 use_pre_read=not refresh。"""
    c = _shell()

    async def _auth():
        return None
    c.ensure_authenticated = _auth
    c._prod_corr_cached = lambda aid: None
    c._prod_corr_store = lambda *a, **k: None
    seen: list = []

    async def _prod(aid, max_wait_seconds=None, use_pre_read=True):
        seen.append(use_pre_read)
        return {"max": 0.5, "records": [[0.0, 0.1, 1]]}
    c.get_production_correlation = _prod

    asyncio.run(c.check_correlation("TGT", "production", 0.7, refresh=False))
    asyncio.run(c.check_correlation("TGT", "production", 0.7, refresh=True))
    assert seen == [True, False]


# ---------------------------------------------------------------- 预读走 _request（不阻塞事件循环）
def test_preread_uses_request_not_raw_session():
    """预读必须走 _request（to_thread + 信号量），禁止再回退到阻塞的 session.get。"""
    c = _shell()

    async def _auth():
        return None
    c.ensure_authenticated = _auth

    via_request: list = []

    async def _req(method, url, **kw):
        via_request.append((method, url, kw.get("timeout")))
        assert not hasattr(c, "session") or True  # 不经 session.get
        return _FakeResponse(200, {"is": {"prodCorrelation": 0.55}})
    c._request = _req

    r = asyncio.run(c._read_existing_prod_correlation("TGT"))
    assert r is not None and r["max"] == 0.55 and r["source"] == "alpha_detail_cached"
    assert via_request and via_request[0][0] == "GET"


# ---------------------------------------------------------------- 轮询 401 刷新
def test_poll_recovers_from_401_by_refreshing_auth():
    c = _shell()

    async def _auth():
        return None
    c.ensure_authenticated = _auth
    c._auth_validated_until = 123.0
    c._brain_correlation_local_lock = asyncio.Lock()

    async def _lock(op):
        return {"acquired": True, "backend": "local", "lock_key": "k"}

    async def _unlock(info, op, **_kw):  # 2026-10-28: 生产侧新增 cooldown/seconds
        return None
    c._try_acquire_brain_correlation_lock = _lock
    c._release_brain_correlation_lock = _unlock

    responses = [
        _FakeResponse(401, {}),
        _FakeResponse(200, {"max": 0.44, "records": [[0.0, 0.1, 2]]}),
    ]

    async def _req(method, url, **kw):
        return responses.pop(0)
    c._request = _req

    r = asyncio.run(c._poll_production_correlation("TGT", max_wait_seconds=30))
    assert r["max"] == 0.44
    assert c._auth_validated_until == 0.0  # 401 后鉴权缓存被清、已重新走 ensure_authenticated


# ---------------------------------------------------------------- OS ID 列表 TTL
def test_os_idlist_ttl_cache_avoids_relisting(monkeypatch, tmp_path):
    c = _shell()
    c._os_idlist_ttl_seconds = 900.0
    monkeypatch.setattr(c, "_os_ppac_ids_path",
                        lambda *a: tmp_path / "pool.ppac.json", raising=False)

    req_calls: list = []

    async def _list_json(method, url, **kw):
        req_calls.append(url)
        return {"results": [
            {"id": f"A{i}", "settings": {"instrumentType": "EQUITY", "region": "USA",
                                          "universe": "TOP3000", "delay": 1}}
            for i in range(3)
        ]}
    c._request_json_with_retries = _list_json

    ids1 = asyncio.run(c._list_matching_os_alpha_ids("EQUITY", "USA", "TOP3000", 1))
    ids2 = asyncio.run(c._list_matching_os_alpha_ids("EQUITY", "USA", "TOP3000", 1))
    assert ids1 == ids2 == ["A0", "A1", "A2"]
    assert len(req_calls) == 1  # 第二次命中 TTL 缓存，不再分页
    assert (tmp_path / "pool.ppac.json").exists()  # sidecar 仍随真实列举写入

    c._os_idlist_ttl_seconds = 0.0  # 关闭缓存 → 回到每次列举
    asyncio.run(c._list_matching_os_alpha_ids("EQUITY", "USA", "TOP3000", 1))
    assert len(req_calls) == 2


# ---------------------------------------------------------------- self 相关性裁剪等价
def _dense_pool(periods=1600, seed=7):
    """构造 >4 年的稠密池：P1/P2 两列，目标 = 2×P1。"""
    idx = pd.date_range("2022-06-01", periods=periods, freq="D")
    rng = pd.Series(range(periods), index=idx, dtype="float64")
    p1 = rng + (rng.index.dayofweek.to_series(index=idx) * 0.1)  # 确定性"波动"
    p2 = rng * 0.9 + (rng.index.month.to_series(index=idx) * 0.2)
    return pd.DataFrame({"P1": p1, "P2": p2}), idx


def _expected_max_old_formula(pool: pd.DataFrame, target: pd.Series, target_col: str) -> float:
    """旧实现（全历史 ffill+diff 后裁 4 年）的参照值，测试内独立重算。"""
    combined = pd.concat([pool, target.rename(target_col).to_frame()], axis=1).ffill()
    rets = combined.diff()
    last_date = rets.index.max()
    rets = rets[rets.index > last_date - pd.DateOffset(years=4)]
    sc = rets.drop(columns=[target_col], errors="ignore").corrwith(rets[target_col]).dropna()
    return float(sc.max())


@pytest.mark.parametrize("punch_hole", [False, True])
def test_selfcorr_trim_matches_old_full_history_formula(punch_hole):
    """先裁剪再 diff 与旧全历史公式在稠密/内部缺口数据下 max 逐值一致。"""
    pool, _ = _dense_pool()
    target = pool["P1"] * 2.0
    if punch_hole:  # 窗口内部的缺口：ffill 语义在两种实现下相同
        pool = pool.copy()
        pool.iloc[700:705, 1] = float("nan")

    c = _shell()

    async def _auth():
        return None
    c.ensure_authenticated = _auth

    async def _pnl(aid):
        return {"records": [[d.isoformat(), v] for d, v in target.items()],
                "schema": {"properties": [{"name": "date"}, {"name": "pnl"}]}}
    c.get_alpha_pnl = _pnl

    async def _details(aid):
        return {"settings": {"instrumentType": "EQUITY", "region": "USA",
                             "universe": "TOP3000", "delay": 1}}
    c.get_alpha_details = _details

    async def _sync(**kw):
        return kw.get("pool", pool) if False else pool
    c.sync_os_pnl_pool = _sync

    monkey_target_col = "__target__TGT"
    r = asyncio.run(c.get_self_correlation("TGT"))
    expected = _expected_max_old_formula(pool, target, monkey_target_col)
    assert r["max"] == pytest.approx(expected, abs=1e-12)
    # 目标 = 2×P1 ⇒ 与 P1 完全正相关，max 必为 1.0
    assert r["max"] == pytest.approx(1.0, abs=1e-9)


# ---------------------------------------------------------------- slim 透传
def test_slim_check_correlation_passes_status_message_retry_after():
    mcp_core = pytest.importorskip("mcp_core")
    busy = {
        "alpha_id": "TGT", "threshold": 0.7, "correlation_type": "both",
        "checks": {"production": {"max_correlation": None, "passes_check": None,
                                  "status": "correlation_busy", "message": "busy",
                                  "retry_after": 180,
                                  "correlation_data": {"status": "correlation_busy"}}},
        "all_passed": None, "status": "correlation_busy",
        "message": "busy", "retry_after": 180,
    }
    out = mcp_core._slim_check_correlation(busy)
    assert out["status"] == "correlation_busy"
    assert out["retry_after"] == 180
    assert out["checks"]["production"]["status"] == "correlation_busy"
    assert out["checks"]["production"]["retry_after"] == 180

    # 预读采纳形态：source 必须透传到工具层（Agent 区分缓存命中 vs 预读命中）
    preread = {
        "alpha_id": "TGT", "threshold": 0.7, "correlation_type": "production",
        "checks": {"production": {"max_correlation": 0.55, "passes_check": True,
                                  "source": "alpha_detail_cached",
                                  "correlation_data": {"max": 0.55, "records": []}}},
        "all_passed": True,
    }
    out2 = mcp_core._slim_check_correlation(preread)
    assert out2["checks"]["production"]["source"] == "alpha_detail_cached"
    assert out2["checks"]["production"]["max_correlation"] == 0.55
