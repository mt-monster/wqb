# -*- coding: utf-8 -*-
"""workflow 模块单元测试：executor / registry / judge 纯函数 / _common 工具.

覆盖此前无测试的关键路径：
  - executor.execute 的未知节点/缺参数/dry-run 行为
  - registry 节点发现与参数校验
  - judge._eval_platform_check / _eval_correlation / _compute_final_verdict 纯函数
  - _common.infer_data_category 与 wq_py 路径解析
"""
import os
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from wqb.workflow.executor import WorkflowExecutor, WorkflowResult  # noqa: E402
from wqb.workflow.registry import get_registry  # noqa: E402
from wqb.workflow import _common  # noqa: E402


# ---------------------------------------------------------------------------
# executor
# ---------------------------------------------------------------------------

def test_executor_unknown_node():
    ex = WorkflowExecutor()
    r = ex.execute("does_not_exist", {})
    assert isinstance(r, WorkflowResult)
    assert r.success is False
    assert "Unknown workflow node" in r.error


def test_executor_missing_required_params():
    ex = WorkflowExecutor()
    # batch_track 需要 region/wave/dataset
    r = ex.execute("batch_track", {})
    assert r.success is False
    assert "Missing required params" in r.error


def test_executor_dry_run_returns_plan_without_executing():
    ex = WorkflowExecutor()
    r = ex.execute("batch_track", {"region": "KOR", "wave": "1", "dataset": "ds"},
                   dry_run=True)
    assert r.success is True
    assert r.dry_run is True
    assert "plan" in r.output
    assert "batch_track" in r.output["plan"]


def test_executor_workflow_result_to_dict_shape():
    r = WorkflowResult(success=True, node="x", params={})
    d = r.to_dict()
    assert set(["success", "node", "params", "output", "error", "duration_sec",
                "timestamp", "dry_run", "metadata"]) <= set(d.keys())


# ---------------------------------------------------------------------------
# registry
# ---------------------------------------------------------------------------

def test_registry_lists_all_seven_nodes():
    r = get_registry()
    nodes = r.list_nodes()
    assert set(nodes) == {
        "batch_track", "submit_alpha", "superalpha", "judge", "gem",
        "campaign", "feature_engineering",
    }


def test_registry_validate_params():
    r = get_registry()
    # gem 需要 region/dataset_id/delay/universe
    missing = r.validate_params("gem", {"region": "KOR"})
    assert "dataset_id" in missing and "delay" in missing and "universe" in missing
    assert r.validate_params("gem", {"region": "KOR", "dataset_id": "d",
                                     "delay": 1, "universe": "TOP3000"}) == []


def test_registry_meta_has_no_fallback_cli():
    """fallback_cli 字段已移除（executor 伪 fallback 已砍）。"""
    r = get_registry()
    for node in r.list_nodes():
        meta = r.get_meta(node)
        assert not hasattr(meta, "fallback_cli")


# ---------------------------------------------------------------------------
# judge 纯函数
# ---------------------------------------------------------------------------

def _import_judge_helpers():
    from wqb.workflow.nodes import judge
    return judge


def test_judge_platform_check_unavailable():
    judge = _import_judge_helpers()
    g = judge._eval_platform_check({"__error__": "no network"})
    assert g["pass"] is False and g["unavailable"] is True


def test_judge_platform_check_pass():
    judge = _import_judge_helpers()
    details = {"result": {"is": {"sharpe": 1.8, "fitness": 1.2,
                                 "two_year_sharpe": 1.7, "checks": []}}}
    g = judge._eval_platform_check(details)
    assert g["pass"] is True


def test_judge_platform_check_fail_on_sharpe():
    judge = _import_judge_helpers()
    details = {"result": {"is": {"sharpe": 1.0, "fitness": 1.2, "checks": []}}}
    g = judge._eval_platform_check(details)
    assert g["pass"] is False
    assert "sharpe" in g["reason"]


def test_judge_correlation_unavailable_passes():
    judge = _import_judge_helpers()
    g = judge._eval_correlation({"__error__": "timeout"})
    assert g["pass"] is True and g["unavailable"] is True


def test_judge_correlation_blocks_on_prod():
    judge = _import_judge_helpers()
    corr = {"result": {"checks": {"production": {"max_correlation": 0.75}}}}
    g = judge._eval_correlation(corr)
    assert g["pass"] is False
    assert "prod" in g["reason"]


def test_judge_compute_final_verdict():
    judge = _import_judge_helpers()
    # 硬闸失败 -> BLOCK
    gates = [{"gate": "platform_check", "pass": False}]
    assert judge._compute_final_verdict(gates) == "BLOCK"
    # 全过 + 无负年 -> READY
    gates = [{"gate": "platform_check", "pass": True},
             {"gate": "correlation", "pass": True},
             {"gate": "yearly_attribution", "pass": True, "negative_years": []}]
    assert judge._compute_final_verdict(gates) == "READY"
    # 有负年 -> REVIEW
    gates = [{"gate": "platform_check", "pass": True},
             {"gate": "correlation", "pass": True},
             {"gate": "yearly_attribution", "pass": True, "negative_years": [2020]}]
    assert judge._compute_final_verdict(gates) == "REVIEW"


# ---------------------------------------------------------------------------
# _common 工具
# ---------------------------------------------------------------------------

def test_infer_data_category():
    assert _common.infer_data_category("analyst45") == "analyst"
    assert _common.infer_data_category("model238") == "model"
    assert _common.infer_data_category("news76") == "news"
    assert _common.infer_data_category("fundamental94") == "fundamental"
    assert _common.infer_data_category("xyz") == "other"


def test_wq_py_resolves_to_venv_or_python():
    py = _common.wq_py()
    # 至少返回一个非空字符串，且是 .exe 或 "python"
    assert py
    assert py == "python" or py.endswith(".exe") or py.endswith("/python")
