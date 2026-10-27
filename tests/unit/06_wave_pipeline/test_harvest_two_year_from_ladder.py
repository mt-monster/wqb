# -*- coding: utf-8 -*-
"""2026-10-23：2Y 读数的第二个载体 IS_LADDER_SHARPE 必须回落到 two_year_sharpe。

证据（IND/wave232，10/29 颗）：`JjP0Ja5l` 等 alpha 的 `is.checks` 里**只有**
`IS_LADDER_SHARPE`（value 2.82），没有 `LOW_2Y_SHARPE`；而 `get_alpha_details`
的 `metrics.two_year_sharpe` 同样是 2.82 —— 两者是同一个 2Y 读数的不同载体
（`wqb.config.RA_2Y_NAMES` 把两项都收作 2Y）。

两条采集路径此前都只认 `LOW_2Y_SHARPE`：
  ① `tools/harvest_multisim.py::_extract_two_year_sharpe`
  ② `wqb_db_mcp._flatten_platform_alpha`

后果：`backtest_results.two_year_sharpe` 与 `alphas.two_year_sharpe` 整列落空 ⇒
字段画像 `best_2y`（`count_institutional_sellers_security` 被低报成 −0.15）、
提交队列、Mode B 判死规则一起失真。
"""
import importlib
import importlib.util
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[3]
TOOLS = REPO_ROOT / "tools"


def _load_harvest():
    """按文件路径加载 tools/harvest_multisim.py（tools/ 不是包）。"""
    spec = importlib.util.spec_from_file_location("_hm_2y_under_test", TOOLS / "harvest_multisim.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


@pytest.fixture(scope="module")
def hm():
    return _load_harvest()


def _checks(*pairs):
    return [{"name": n, "result": "PASS", "value": v, "limit": 1.58} for n, v in pairs]


# ---------------------------------------------------------------- ① harvest 采集层

def test_harvest_reads_two_year_from_ladder_when_low_2y_missing(hm):
    """IND 实测形态：只有 IS_LADDER_SHARPE，2Y 必须等于它而不是 None。"""
    assert hm._extract_two_year_sharpe({}, _checks(("IS_LADDER_SHARPE", 2.82))) == 2.82


def test_harvest_prefers_low_2y_over_ladder(hm):
    """两项都在时以 LOW_2Y_SHARPE 为准（专名优先，别被 ladder 覆盖）。"""
    got = hm._extract_two_year_sharpe(
        {}, _checks(("LOW_2Y_SHARPE", 3.01), ("IS_LADDER_SHARPE", 2.82)))
    assert got == 3.01


def test_harvest_falls_back_to_is_two_year_sharpe(hm):
    """checks 两项都没有时，仍认 is.twoYearSharpe 直读。"""
    assert hm._extract_two_year_sharpe({"twoYearSharpe": 2.55}, []) == 2.55


def test_harvest_does_not_invent_two_year(hm):
    """checks 为空且无 is 直读 ⇒ None（缺失要如实暴露，不能瞎填）。"""
    assert hm._extract_two_year_sharpe({}, []) is None


# ---------------------------------------------------------------- ② DB 收批拍平层

@pytest.fixture(scope="module")
def db_mcp(tmp_path_factory):
    """wqb_db_mcp 模块（只测纯函数，不连库）；缺 MCP 依赖时跳过。"""
    pytest.importorskip("mcp")
    if str(REPO_ROOT) not in sys.path:
        sys.path.insert(0, str(REPO_ROOT))
    return importlib.import_module("wqb_db_mcp")


def _raw_platform_alpha(*pairs):
    """GET /alphas/{id} 的原始形态：指标与 checks 在 is 块里。"""
    return {
        "id": "t2y_ladder",
        "status": "UNSUBMITTED",
        "stage": "IS",
        "regular": {"code": "rank(ts_delta(close, 5))"},
        "is": {"sharpe": 3.12, "fitness": 2.42, "turnover": 0.24,
               "checks": list(_checks(*pairs))},
    }


def test_flatten_maps_ladder_to_two_year(db_mcp):
    row = db_mcp._flatten_platform_alpha(_raw_platform_alpha(("IS_LADDER_SHARPE", 2.82)))
    assert row["two_year_sharpe"] == 2.82
    assert row["is_ladder_sharpe"] == 2.82


def test_flatten_prefers_low_2y(db_mcp):
    row = db_mcp._flatten_platform_alpha(
        _raw_platform_alpha(("LOW_2Y_SHARPE", 3.01), ("IS_LADDER_SHARPE", 2.82)))
    assert row["two_year_sharpe"] == 3.01
    assert row["is_ladder_sharpe"] == 2.82


def test_flatten_keeps_explicit_two_year(db_mcp):
    """上游 metrics 已给 two_year_sharpe 时不被 ladder 覆盖。"""
    raw = _raw_platform_alpha(("IS_LADDER_SHARPE", 2.82))
    raw["metrics"] = {"two_year_sharpe": 3.11}
    row = db_mcp._flatten_platform_alpha(raw)
    assert row["two_year_sharpe"] == 3.11


# ---------------------------------------------------------------- ③ 修数工具（必须与采集层同口径）

def _load_repair():
    spec = importlib.util.spec_from_file_location(
        "_br_2y_under_test", TOOLS / "data-repair" / "backfill_alpha_metrics_from_platform.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


@pytest.fixture(scope="module")
def repair():
    return _load_repair()


def test_repair_tool_reads_ladder_as_two_year(repair):
    """`extract_is_metrics` 也被 `sync_platform_alphas.py` 复用 —— 同样要回落 ladder。"""
    ty, _sub, ladder = repair.extract_is_metrics(
        _raw_platform_alpha(("IS_LADDER_SHARPE", 2.82)))
    assert (ty, ladder) == (2.82, 2.82)


def test_repair_tool_prefers_low_2y(repair):
    ty, _sub, ladder = repair.extract_is_metrics(
        _raw_platform_alpha(("LOW_2Y_SHARPE", 3.01), ("IS_LADDER_SHARPE", 2.82)))
    assert (ty, ladder) == (3.01, 2.82)
