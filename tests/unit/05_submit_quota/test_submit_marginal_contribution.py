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


# ---------------------------------------------------------------------------
# 2026-11-13 分级硬闸：ΔSharpe / ΔReturns 硬拦，成本指标只告警
# ---------------------------------------------------------------------------

class _CostlyPositive:
    """ΔS>0、ΔRet>0，但换手与回撤都变差 —— 只应软告警，不得阻断。"""

    async def performance_comparison(self, alpha_id):
        return {
            "partitionName": "EQUITY:DEU:1",
            "stats": {
                "before": {"sharpe": 3.04, "fitness": 2.55, "turnover": 0.1453,
                           "returns": 0.102, "drawdown": 0.0337},
                "after": {"sharpe": 3.13, "fitness": 2.61, "turnover": 0.150,
                          "returns": 0.1025, "drawdown": 0.040},
            },
        }


class _FullyPositive:
    """五项按方向全部达标。"""

    async def performance_comparison(self, alpha_id):
        return {
            "partitionName": "EQUITY:DEU:1",
            "stats": {
                "before": {"sharpe": 3.04, "fitness": 2.55, "turnover": 0.1453,
                           "returns": 0.102, "drawdown": 0.0337},
                "after": {"sharpe": 3.13, "fitness": 2.61, "turnover": 0.140,
                          "returns": 0.1025, "drawdown": 0.030},
            },
        }


def test_returns_negative_marks_hard_gate():
    """ΔSharpe>0 但 ΔReturns<0 ⇒ hard_blocked=True（新增硬项），dilutive 仍为 False。"""
    r = _marginal_contribution(_Dispersive(), "FAKE")
    assert r["available"] is True
    assert r["dilutive"] is False, "dilutive 仍只表达 ΔSharpe<0，供 Step 1.8 复用"
    assert "blocked" not in r, "blocked 由 run() 置位，本函数不得自带"
    assert r["delta"]["sharpe"] > 0 and r["delta"]["returns"] < 0
    assert r["hard_blocked"] is True
    assert r["hard_failures"] == ["returns"], r["hard_failures"]
    assert "组合分散" in (r["risk_note"] or ""), "risk_note 仍按 ΔSharpe 语义产出"
    assert "阻断" in (r["hard_gate_note"] or "")


def test_cost_metrics_are_soft_warnings_only():
    """ΔTurnover>0 / ΔDrawdown>0 只进 soft_warnings，绝不触发硬闸。"""
    r = _marginal_contribution(_CostlyPositive(), "FAKE")
    assert r["hard_blocked"] is False
    assert r["hard_failures"] == []
    assert "turnover" in r["soft_warnings"] and "drawdown" in r["soft_warnings"]
    assert r["direction_ok"]["turnover"] is False
    assert r["direction_ok"]["drawdown"] is False
    assert r["direction_ok"]["sharpe"] is True
    assert r["direction_ok"]["returns"] is True
    assert "不阻断" in (r["hard_gate_note"] or "")


def test_all_directional_metrics_pass():
    r = _marginal_contribution(_FullyPositive(), "FAKE")
    assert r["hard_blocked"] is False
    assert r["soft_warnings"] == []
    assert all(v is True for v in r["direction_ok"].values())
    assert "方案D通过" in (r["hard_gate_note"] or "")


def test_direction_rule_is_exposed():
    """方向定义与硬项清单必须随结果透出，便于审计与口径同步。"""
    r = _marginal_contribution(_FullyPositive(), "FAKE")
    rule = r["direction_rule"]
    assert set(rule["higher_is_better"]) == {"sharpe", "fitness", "returns"}
    assert set(rule["lower_is_better"]) == {"turnover", "drawdown"}
    assert set(rule["hard_block_metrics"]) == {"sharpe", "fitness"}
    assert set(rule["pair_cost_metrics"]) == {"turnover", "drawdown"}
    assert rule["scheme"].startswith("D:")


class _FitnessNegative:
    """ΔS>0、ΔRet>0，但换手抬高把 ΔFitness 压负 —— 复合成本信号，应硬拦。"""

    async def performance_comparison(self, alpha_id):
        return {
            "partitionName": "EQUITY:DEU:1",
            "stats": {
                "before": {"sharpe": 3.00, "fitness": 2.35, "turnover": 0.13,
                           "returns": 0.080, "drawdown": 0.0337},
                "after": {"sharpe": 3.10, "fitness": 1.97, "turnover": 0.20,
                          "returns": 0.081, "drawdown": 0.030},
            },
        }


def test_fitness_negative_marks_hard_gate():
    """2026-11-13 追加：Fitness 与 Sharpe/Returns 同属正向族，ΔF<0 亦硬拦。"""
    r = _marginal_contribution(_FitnessNegative(), "FAKE")
    assert r["available"] is True
    assert r["dilutive"] is False
    assert r["hard_blocked"] is True
    assert r["hard_failures"] == ["fitness"], r["hard_failures"]
    assert r["direction_ok"]["fitness"] is False
    assert "turnover" in r["soft_warnings"], "成本指标仍只作软告警"
    assert "阻断" in (r["hard_gate_note"] or "")


class _DiversificationOffset:
    """ΔRet<0 但 ΔTO/ΔDD 同步下降、ΔS/ΔF 上升 —— 健康分散化，方案 D 必须放行。"""

    async def performance_comparison(self, alpha_id):
        return {
            "partitionName": "EQUITY:DEU:1",
            "stats": {
                "before": {"sharpe": 3.00, "fitness": 2.35, "turnover": 0.13,
                           "returns": 0.080, "drawdown": 0.0337},
                "after": {"sharpe": 3.10, "fitness": 2.50, "turnover": 0.12,
                          "returns": 0.078, "drawdown": 0.030},
            },
        }


def test_pair_offset_passes():
    """方案 D 核心：收益降但成本同步降 ⇒ 分散化补偿，不阻断。"""
    r = _marginal_contribution(_DiversificationOffset(), "FAKE")
    assert r["hard_blocked"] is False
    assert r["hard_failures"] == []
    assert r["pair_rule"]["triggered"] is False
    assert r["pair_rule"]["offset"] is True
    assert r["pair_rule"]["cost_metrics_up"] == []
    assert "returns" in r["soft_warnings"], "收益下降仍须作为归因软告警"
    assert "分散化补偿" in (r["hard_gate_note"] or "")


def test_pair_triggered_blocks():
    """收益降 + 成本升 ⇒ 双重恶化，returns 进硬失败列表。"""
    r = _marginal_contribution(_Dispersive(), "FAKE")
    assert r["hard_blocked"] is True
    assert r["hard_failures"] == ["returns"]
    assert r["pair_rule"]["triggered"] is True
    assert "turnover" in r["pair_rule"]["cost_metrics_up"]
