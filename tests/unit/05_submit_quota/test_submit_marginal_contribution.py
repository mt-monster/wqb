# -*- coding: utf-8 -*-
"""Step 1.7 边际贡献（`performance_comparison`）守护。

口径沿革：2026-11-04 接入时定案「只能报告，永远不能拦」；**2026-11-08 用户明令
「如果边际贡献为负你就阻断不准提交」⇒ 升为否决闸**（`run()` Step 1.7 里置 blocked）。
本文件锁四条不变量：

1. **可用性 fail-open**：调用抛异常 / 返回 `__error__` / 空 dict / 缺 `stats` —— 四种失败形态
   一律 `available=False` 且**不得带 `blocked`**，提交链路照常往下走（「ΔS 不可得」≠「ΔS 为负」）。
   `blocked` 只能由 `run()` 依据 `dilutive` 置位，本函数自身永不置位 —— 避免两层各自判定。

2. **负值 ⇒ 硬闸**：`ΔSharpe < 0` 时 `dilutive=True`、`risk_note` 须写明「硬闸：提交阻断」，
   由 `run()` 在 `confirm_submit=True` 时阻断（见 test_submit_marginal_wiring.py）。
   2026-11-04 的反例依据（EUR V5：ΔS −0.04 但 F/DD/TO 全改善）记录在节点 docstring 里，
   作为**遗留风险说明**保留，不再作为放行依据。

3. **基准不可跨 alpha 比较**：`partition` 必须原样透出。实测同批 DEU/D1 两颗候选
   分属 `EQUITY:DEU:1`（before S 3.04）与 `EQUITY:DEU:1:POWER_POOL`（before S 1.73）
   —— 丢掉分区字段会让 ΔS 被误当成可横向排序的分数。

另：本步位于 `confirm_submit` 条件**之外**，`confirm_submit=False` 的预检同样产出数值。
"""
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
for _p in (REPO_ROOT / "src",):
    if str(_p) not in sys.path:
        sys.path.insert(0, str(_p))

from wqb.workflow.nodes.submit_alpha import _marginal_contribution  # noqa: E402


class _Raises:
    async def performance_comparison(self, alpha_id):
        raise RuntimeError("network down")


class _ErrorDict:
    async def performance_comparison(self, alpha_id):
        return {"__error__": "timeout"}


class _Empty:
    async def performance_comparison(self, alpha_id):
        return {}


class _NoStats:
    async def performance_comparison(self, alpha_id):
        return {"partitionName": "EQUITY:DEU:1"}


class _Dilutive:
    async def performance_comparison(self, alpha_id):
        return {
            "partitionName": "EQUITY:DEU:1:POWER_POOL",
            "stats": {
                "before": {"sharpe": 1.73, "fitness": 1.37, "turnover": 0.127,
                           "returns": 0.0799, "drawdown": 0.0608},
                "after": {"sharpe": 1.60, "fitness": 1.30, "turnover": 0.130,
                          "returns": 0.0750, "drawdown": 0.0700},
            },
        }


class _Dispersive:
    async def performance_comparison(self, alpha_id):
        return {
            "partitionName": "EQUITY:DEU:1",
            "stats": {
                "before": {"sharpe": 3.04, "fitness": 2.55, "turnover": 0.1453,
                           "returns": 0.102, "drawdown": 0.0337},
                "after": {"sharpe": 3.13, "fitness": 2.61, "turnover": 0.146,
                          "returns": 0.1018, "drawdown": 0.031},
            },
        }


def test_all_failure_modes_are_fail_open():
    """四类失败形态：available=False，且绝不出现 blocked 键（否则会变成隐性硬闸）。"""
    for name, client in (
        ("raises", _Raises()),
        ("error_dict", _ErrorDict()),
        ("empty", _Empty()),
        ("no_stats", _NoStats()),
    ):
        r = _marginal_contribution(client, "FAKE")
        assert r["step"] == "marginal_contribution", name
        assert r["available"] is False, name
        assert "blocked" not in r, f"{name}: 信息项不得携带 blocked"
        assert r.get("note"), f"{name}: 失败需留下原因"


def test_dilutive_marks_hard_gate():
    """ΔSharpe<0 ⇒ dilutive=True，risk_note 必须写明「硬闸：提交阻断」。"""
    r = _marginal_contribution(_Dilutive(), "FAKE")
    assert r["available"] is True
    assert "blocked" not in r, "blocked 由 run() 置位，本函数不得自带"
    assert r["dilutive"] is True
    assert r["delta"]["sharpe"] < 0
    assert "稀释" in (r["risk_note"] or "")
    assert "硬闸" in (r["risk_note"] or ""), "负值必须给出闸门级别的措辞"
    assert "阻断" in (r["note"] or "")


def test_dispersive_marks_positive_contribution():
    r = _marginal_contribution(_Dispersive(), "FAKE")
    assert r["available"] is True
    assert r["dilutive"] is False
    assert r["delta"]["sharpe"] > 0
    assert "分散" in (r["risk_note"] or "")


def test_partition_is_always_exposed_when_available():
    """partition 必须透出——跨分区 ΔS 不可比，缺了就会被误当排序分数。"""
    for client in (_Dilutive(), _Dispersive()):
        r = _marginal_contribution(client, "FAKE")
        assert r["partition"], "available=True 时必须带 partition"
        assert r["note"] and "同一分区" in r["note"]


def test_metrics_delta_is_computed_not_passed_through():
    """Δ 由本函数计算（而非信平台），且五指标齐全。"""
    r = _marginal_contribution(_Dispersive(), "FAKE")
    assert set(r["delta"]) == {"sharpe", "fitness", "turnover", "returns", "drawdown"}
    assert abs(r["delta"]["sharpe"] - 0.09) < 1e-9
    # drawdown 改善 = 数值下降 ⇒ Δ 为负
    assert r["delta"]["drawdown"] < 0
