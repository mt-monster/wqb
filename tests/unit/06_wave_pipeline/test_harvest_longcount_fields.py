# -*- coding: utf-8 -*-
"""2026-09-29：harvest 采集层的 is 段持仓广度字段（longCount/shortCount/pnl/bookSize）回归守护。

背景：实测 `backtest_results.long_count` 只填了 9.2%（830/9010）、`pnl`/`book_size` 只有 0.8%。
根因是 `harvest_multisim.fetch_alpha_details` 的展平字典**从来没取过 is.longCount** ——
下游 `_to_backtest_rows` 虽然写了 `"long_count": a.get("long_count")`，但上游压根没产出这个键。

本文件守护三件事：
  1. is 段字段被正确抽取（驼峰 → 蛇形）；
  2. is 段缺失时回退 `is.metrics`；
  3. **longCount=0 不能被 `or` 吞成 None**（0 是 falsy；库里确有 long_count=0 的真实记录，
     正是最需要暴露的 CONCENTRATED_WEIGHT 案例）。
"""
import asyncio
import json
import importlib.util
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[3]
TOOLS = REPO_ROOT / "tools"


def _load_harvest():
    """按文件路径加载 tools/harvest_multisim.py（tools/ 不是包）。"""
    spec = importlib.util.spec_from_file_location("_hm_under_test", TOOLS / "harvest_multisim.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


@pytest.fixture(scope="module")
def hm():
    return _load_harvest()


# ---------------------------------------------------------------- fake brain

class _Resp:
    def __init__(self, payload, status=200):
        self._p = payload
        self.status_code = status
        self.text = json.dumps(payload)

    def json(self):
        return self._p


class _Brain:
    def __init__(self, payload, status=200):
        self._payload = payload
        self._status = status

    async def _request(self, method, url, **kwargs):
        return _Resp(self._payload, self._status)


def _alpha(is_dict, extra=None):
    d = {"id": "xYz123", "status": "UNSUBMITTED", "type": "REGULAR",
         "settings": {"region": "KOR", "universe": "TOP600", "delay": 1}}
    d["is"] = is_dict
    if extra:
        d.update(extra)
    return d


# ---------------------------------------------------------------- tests

def test_is_longcount_is_extracted(hm):
    """is.longCount/shortCount/pnl/bookSize → 蛇形键。"""
    payload = _alpha({"sharpe": 1.9, "fitness": 1.2, "longCount": 251, "shortCount": 249,
                      "pnl": 1234567, "bookSize": 20000000,
                      "returns": 0.1531, "drawdown": 0.0284})
    out = asyncio.run(hm.fetch_alpha_details(_Brain(payload), "xYz123"))
    assert out["long_count"] == 251
    assert out["short_count"] == 249
    assert out["pnl"] == 1234567
    assert out["book_size"] == 20000000
    assert out["returns"] == 0.1531
    assert out["drawdown"] == 0.0284


def test_metrics_fallback_when_is_missing(hm):
    """is 顶层无该键时回退 is.metrics（harvest_multisim_alphas 的返回形态）。"""
    payload = _alpha({"sharpe": 1.9, "longCount": None,
                      "metrics": {"longCount": 300, "shortCount": 290, "pnl": 42, "bookSize": 7}})
    out = asyncio.run(hm.fetch_alpha_details(_Brain(payload), "xYz123"))
    assert out["long_count"] == 300
    assert out["short_count"] == 290
    assert out["pnl"] == 42
    assert out["book_size"] == 7


def test_zero_longcount_is_preserved(hm):
    """★ longCount=0 必须保留为 0，不能被 `or` 短路成 None。

    库里确有 long_count=0 的记录（ASI/intraday_pv_feats，同时标 CONCENTRATED_WEIGHT），
    这是最需要暴露的坏样本；若被吞成 NULL，回补脚本会反复重拉且指标失真。
    """
    payload = _alpha({"sharpe": 0.0, "longCount": 0, "shortCount": 0,
                      "pnl": 0, "bookSize": 0})
    out = asyncio.run(hm.fetch_alpha_details(_Brain(payload), "xYz123"))
    assert out["long_count"] == 0, "longCount=0 被吞成 None：0 是 falsy，禁止用 `or` 取回退"
    assert out["short_count"] == 0
    assert out["pnl"] == 0
    assert out["book_size"] == 0


def test_zero_with_metrics_fallback_stays_zero(hm):
    """is.longCount=0 且 metrics 有值 → 仍应取 0（is 优先，非空即止）。"""
    payload = _alpha({"longCount": 0, "metrics": {"longCount": 999}})
    out = asyncio.run(hm.fetch_alpha_details(_Brain(payload), "xYz123"))
    assert out["long_count"] == 0


def test_to_backtest_rows_passes_breadth_and_size(hm):
    """_to_backtest_rows 必须把 pnl/book_size（与既有的 long/short）一起透传。"""
    rows = hm._to_backtest_rows([{
        "alpha_id": "xYz123", "expression": "rank(x)", "sharpe": 1.9,
        "long_count": 251, "short_count": 249, "pnl": 1234567, "book_size": 20000000,
    }])
    r = rows[0]
    assert (r["long_count"], r["short_count"]) == (251, 249)
    assert (r["pnl"], r["book_size"]) == (1234567, 20000000)


def test_to_backtest_rows_zero_not_dropped(hm):
    rows = hm._to_backtest_rows([{"alpha_id": "z", "long_count": 0, "short_count": 0}])
    assert rows[0]["long_count"] == 0 and rows[0]["short_count"] == 0
