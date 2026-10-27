"""`batch_get_alpha_metrics` 的归一化回归（2026-10-23）。

平台原始 alpha 结构是 ``{"is": {...}, "regular": {...}}``；``brain_client.get_alpha_details``
返回的就是这个原始结构。``batch_get_alpha_metrics`` 原先直接读 ``d["metrics"]``，于是
所有指标取不到、全为 None，prescreen 把 10/10 颗正常 alpha 误判成 REJECT。

修复方式：先过 ``_slim_alpha_response``（与 ``get_alpha_details`` 工具同一份归一化），
再读 ``metrics`` / ``ra``。本测试同时覆盖 2Y 双载体（``IS_LADDER_SHARPE`` / ``LOW_2Y_SHARPE``）。
"""
import asyncio

import tools_alpha


def _raw_alpha(checks):
    return {
        "id": "A1",
        "status": "UNSUBMITTED",
        "stage": "IS",
        "is": {
            "sharpe": 2.0,
            "fitness": 1.5,
            "turnover": 0.2,
            "margin": 0.001,
            "returns": 0.1,
            "drawdown": 0.05,
            "selfCorrelation": 0.3,
            "prodCorrelation": 0.6,
            "investabilityConstrained": {"sharpe": 1.5, "fitness": 1.1},
            "checks": checks,
        },
    }


PASS_CHECKS = [
    {"name": "LOW_SHARPE", "result": "PASS", "value": 2.0, "limit": 1.25},
    {"name": "LOW_FITNESS", "result": "PASS", "value": 1.5, "limit": 1.0},
    {"name": "IS_LADDER_SHARPE", "result": "PASS", "value": 2.1, "limit": 1.58, "year": 2},
    {"name": "LOW_ROBUST_UNIVERSE_SHARPE", "result": "PASS", "value": 1.2, "limit": 1.0},
    {"name": "LOW_SUB_UNIVERSE_SHARPE", "result": "PASS", "value": 1.1, "limit": 1.0},
]


def _run(monkeypatch, raw):
    async def fake_get_alpha_details(alpha_id):
        assert alpha_id == "A1"
        return raw

    monkeypatch.setattr(tools_alpha.brain_client, "get_alpha_details", fake_get_alpha_details)
    return asyncio.run(tools_alpha.batch_get_alpha_metrics(["A1"]))


def test_batch_metrics_reads_normalized_platform_fields(monkeypatch):
    out = _run(monkeypatch, _raw_alpha(PASS_CHECKS))

    assert out["success"] == 1 and out["failed"] == 0
    row = out["results"][0]
    assert row["error"] is None
    assert row["status"] == "UNSUBMITTED"

    # 核心回归：指标不能是 None。
    assert row["sharpe"] == 2.0
    assert row["fitness"] == 1.5
    assert row["turnover"] == 0.2
    assert row["margin"] == 0.001
    assert row["returns"] == 0.1
    assert row["drawdown"] == 0.05
    assert row["self_correlation"] == 0.3
    assert row["prod_correlation"] == 0.6

    # checks 里的子弹头指标与 RA 计数也要经归一化透传。
    assert row["two_year_sharpe"] == 2.1
    assert row["robust_universe_sharpe"] == 1.2
    assert row["sub_universe_sharpe"] == 1.1
    assert row["investability_sharpe"] == 1.5
    assert row["investability_fitness"] == 1.1
    assert row["investability_ratio"] == 0.75
    assert row["failed_ra_count"] == 0

    # 全硬闸满足（prod 0.6 < 0.7）⇒ READY。
    assert out["prescreen"]["READY"] == ["A1"]


def test_batch_metrics_low_2y_carrier(monkeypatch):
    checks = [
        {"name": "LOW_SHARPE", "result": "PASS", "value": 2.0, "limit": 1.25},
        {"name": "LOW_FITNESS", "result": "PASS", "value": 1.5, "limit": 1.0},
        {"name": "LOW_2Y_SHARPE", "result": "PASS", "value": 2.2, "limit": 1.58},
        {"name": "LOW_ROBUST_UNIVERSE_SHARPE", "result": "PASS", "value": 1.2, "limit": 1.0},
    ]
    out = _run(monkeypatch, _raw_alpha(checks))
    assert out["results"][0]["two_year_sharpe"] == 2.2


def test_batch_metrics_low_investability_does_not_block_ready(monkeypatch):
    # 决策固化：IND 的提交层 /check 当前不下发 LOW_INVESTABILITY_CONSTRAINED_SHARPE，
    # 因此 invest_S / S 只作风险监控，不能把低比值直接判成 REVIEW/REJECT。
    raw = _raw_alpha(PASS_CHECKS)
    raw["is"]["investabilityConstrained"] = {"sharpe": 0.5, "fitness": 0.4}
    out = _run(monkeypatch, raw)
    row = out["results"][0]
    assert row["investability_ratio"] == 0.25
    assert out["prescreen"]["READY"] == ["A1"]


def test_batch_metrics_missing_investability_is_none(monkeypatch):
    raw = _raw_alpha(PASS_CHECKS)
    raw["is"].pop("investabilityConstrained")
    out = _run(monkeypatch, raw)
    row = out["results"][0]
    assert row["investability_sharpe"] is None
    assert row["investability_ratio"] is None


def test_batch_metrics_failed_ra_is_counted_and_not_ready(monkeypatch):
    # headline 指标全达标，但一条非 Sharpe 的 RA 检查 FAIL ⇒ 不能 READY。
    checks = [
        {"name": "LOW_SHARPE", "result": "PASS", "value": 2.0, "limit": 1.25},
        {"name": "LOW_FITNESS", "result": "PASS", "value": 1.5, "limit": 1.0},
        {"name": "IS_LADDER_SHARPE", "result": "PASS", "value": 2.1, "limit": 1.58, "year": 2},
        {"name": "LOW_ROBUST_UNIVERSE_SHARPE", "result": "PASS", "value": 1.2, "limit": 1.0},
        {"name": "CONCENTRATED_WEIGHT", "result": "FAIL", "value": 0.5, "limit": 0.1},
    ]
    out = _run(monkeypatch, _raw_alpha(checks))
    row = out["results"][0]
    assert row["failed_ra_count"] == 1
    assert "A1" not in out["prescreen"]["READY"]
    assert "A1" in out["prescreen"]["REVIEW"]
