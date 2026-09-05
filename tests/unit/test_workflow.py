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


def test_executor_dry_run_returns_plan_without_executing(monkeypatch):
    # 契约：dry-run 会调用节点但注入 _context.dry_run=True，节点须构建计划
    # 即停（无 subprocess / 无写库 / 不建目录）。
    # 2026-09-05 更正注释：原文写"batch_track 节点不感知 dry_run → 走 subprocess"
    # 已过期 —— executor 自 2026-09-01 起按 inspect.signature 透传 dry_run，且
    # 2026-09-05 起 7 个节点统一从 _context 读 dry_run。全节点的 dry-run 契约
    # 由 tests/unit/test_skill_integrity.py 逐节点覆盖；此处保留 campaign 作为
    # "命令构建即停"的代表用例。
    from wqb.workflow.nodes import campaign as camp
    calls = []
    orig = camp.run
    def spy(**kw):
        calls.append(kw)
        return orig(**kw)
    monkeypatch.setattr(camp, "run", spy)
    import wqb.workflow.registry as reg_mod
    monkeypatch.setitem(reg_mod.get_registry()._nodes, "campaign", spy)

    ex = WorkflowExecutor()
    r = ex.execute("campaign", {"region": "KOR", "stage": "S5"}, dry_run=True)
    assert r.success is True
    assert r.dry_run is True
    # 新契约：输出含节点构建的真实计划（campaign 构建到 toolkit 命令即停）
    out = r.output or {}
    assert out.get("dry_run") is True
    assert out.get("success") is True
    # dry-run 上下文已注入节点
    assert calls and calls[0]["_context"].get("dry_run") is True


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


def test_feature_engineering_builds_prefix_summary(monkeypatch, tmp_path):
    from wqb.store import CampaignStore
    from wqb.workflow.nodes import feature_engineering as fe

    store = CampaignStore(str(tmp_path / "camp.db"))
    try:
        store.upsert_field_catalog("IND", {
            "dataset": "analyst45",
            "region": "IND",
            "data_type": "MATRIX",
            "fields": [
                {"id": "anl_est_eps", "type": "MATRIX", "coverage": 0.91},
                {"id": "anl_rev_fy1", "type": "MATRIX", "coverage": 0.88},
                {"id": "news_sent_score", "type": "VECTOR", "coverage": 0.42},
            ],
        })

        monkeypatch.setattr(fe, "resolve_skill_dir", lambda name: "C:/skill")
        # 2026-09-03: 适配异步模式 — mock _run_feature_engineering_pipeline_async
        # 异步版本立即返回 success + pid，ledger 写入在后台线程完成。
        # 测试需要模拟后台线程的 ledger 写入行为。
        def _mock_async_pipeline(**kw):
            # 模拟异步立即返回
            store = kw.get("store")
            s1_key = kw.get("s1_key")
            # 模拟后台线程的 ledger 写入
            if store and s1_key:
                prefix_summary = store.build_field_prefix_clusters(
                    region=kw["region"], dataset=kw["dataset_id"],
                    prefix_depth=1, top_n=10, samples_per_cluster=5, persist=True,
                )
                pool_payload = store.build_candidate_field_pool(
                    region=kw["region"], dataset=kw["dataset_id"], persist=True,
                )
                candidate_field_pool = pool_payload.get("candidate_field_pool", [])
                ledger_data = {
                    "generated_at": "2026-09-03T00:00:00",
                    "region": kw["region"],
                    "dataset_id": kw["dataset_id"],
                    "delay": kw["delay"],
                    "universe": kw["universe"],
                    "data_category": kw["data_category"],
                    "ideas_md_path": "C:/tmp/ideas.md",
                    "field_whitelist": candidate_field_pool or ["anl_est_eps"],
                    "candidate_field_pool": candidate_field_pool,
                    "preprocessing": {"ts_backfill": "sparse fields"},
                    "field_prefix_summary": prefix_summary or {},
                    "source": "feature_engineering_node",
                }
                store.upsert_ledger(kw["region"], s1_key, ledger_data)
            return {
                "step": "feature_engineering_pipeline",
                "success": True,
                "async": True,
                "pid": 12345,
                "task_id": kw.get("task_id", "test"),
                "task_file": kw.get("task_file", "/tmp/test.json"),
            }
        monkeypatch.setattr(fe, "_run_feature_engineering_pipeline_async", _mock_async_pipeline)

        out = fe.run(
            region="IND",
            dataset_id="analyst45",
            delay=1,
            universe="TOP3000",
            data_category="analyst",
            force_regen=True,
            _context={"store": store},
        )
        assert out["success"] is True
        assert out["async"] is True
        assert out["pid"] == 12345
        # 异步模式：ledger 写入在 mock 中已完成，验证 DB 状态
        got = store.get_field_prefix_clusters("IND", "analyst45")
        assert got is not None
        assert got["dataset"] == "analyst45"
        got_pool = store.get_candidate_field_pool("IND", "analyst45")
        assert got_pool is not None
        assert got_pool["pool_size"] >= 1
        s1 = store.get_ledger("IND", "s1_analyst45_d1")
        assert s1 is not None
        assert s1["field_whitelist"] == got_pool["candidate_field_pool"]
    finally:
        store.close()


def test_gem_consumes_field_prefix_summary(monkeypatch, tmp_path):
    from wqb.store import CampaignStore
    from wqb.workflow.nodes import gem

    store = CampaignStore(str(tmp_path / "camp.db"))
    try:
        store.upsert_field_catalog("IND", {
            "dataset": "analyst45",
            "region": "IND",
            "data_type": "MATRIX",
            "fields": [
                {"id": "anl_est_eps", "type": "MATRIX", "coverage": 0.91},
                {"id": "anl_rev_fy1", "type": "MATRIX", "coverage": 0.88},
                {"id": "news_sent_score", "type": "VECTOR", "coverage": 0.42},
            ],
        })
        store.build_field_prefix_clusters("IND", "analyst45")

        monkeypatch.setattr(gem, "resolve_skill_dir", lambda name: "C:/gem")
        monkeypatch.setattr(gem.os.path, "exists", lambda p: True)
        monkeypatch.setattr(gem, "_find_final_expressions", lambda *a, **k: "C:/tmp/final_expressions.json")
        monkeypatch.setattr(gem, "_run_quality_estimation", lambda **kw: {
            "step": "quality_estimation",
            "success": True,
            "expected_pass": 1,
            "expected_review": 0,
            "expected_block": 0,
            "expected_block_count": 0,
            "diversity_risks": [],
            "details": {"field_prefix_summary": kw.get("field_prefix_summary") or {}},
        })

        class _Proc:
            """模拟 Popen 行为（2026-09-03: 适配 gem 从 run 改为 Popen 的异步化）。

            提供 stdout/stderr 的 readline/close 以满足 gem 的 detached 分支读取
            task_id 的路径；本测试用 detached=False 固定走同步 communicate 路径。
            """
            returncode = 0
            stdout = type("Pipe", (), {
                "readline": lambda self: "",
                "close": lambda self: None,
            })()
            stderr = type("Pipe", (), {
                "readline": lambda self: "",
                "close": lambda self: None,
            })()

            def communicate(self, timeout=None):
                return ("ok", "")

        class _DummyFile:
            def __enter__(self):
                return self
            def __exit__(self, exc_type, exc, tb):
                return False

        monkeypatch.setattr(gem.subprocess, "Popen", lambda *a, **k: _Proc())
        monkeypatch.setattr("builtins.open", lambda *a, **k: _DummyFile())

        # patch json.load for final expressions file read
        orig_json_load = gem.json.load
        monkeypatch.setattr(gem.json, "load", lambda f: [{"expression": "rank(anl_est_eps)"}])

        out = gem.run(
            region="IND",
            dataset_id="analyst45",
            delay=1,
            universe="TOP3000",
            data_category="analyst",
            detached=False,  # 2026-09-03: 本测试验证 field_prefix_summary →
            # quality_estimation 的数据流转，该链位于 gem 的同步（非 detached）
            # 路径；detached 模式在拿到 task_id 后即返回，不产出这两个键。
            _context={"store": store},
        )
        assert out["success"] is True
        assert out["field_prefix_summary"]["dataset"] == "analyst45"
        assert out["candidate_field_pool"]
        assert out["quality_estimation"]["details"]["field_prefix_summary"]["total_fields"] == 3

        monkeypatch.setattr(gem.json, "load", orig_json_load)
    finally:
        store.close()


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
    # 2026-09-01 统一口径：分类一律以平台 category 为准（data/wqb.db 快照存大写，
    # 如 ANALYST/MODEL）；DB 无记录时回退前缀推断（小写）。
    # GEM 管道内做 .lower() 比较，大小写不敏感。
    assert _common.infer_data_category("analyst45") in ("analyst", "ANALYST")
    assert _common.infer_data_category("model238") in ("model", "MODEL")
    assert _common.infer_data_category("news76") in ("news", "NEWS")
    assert _common.infer_data_category("fundamental94") in ("fundamental", "FUNDAMENTAL")
    assert _common.infer_data_category("xyz") == "other"


def test_wq_py_resolves_to_venv_or_python():
    py = _common.wq_py()
    # 至少返回一个非空字符串，且是 .exe 或 "python"
    assert py
    assert py == "python" or py.endswith(".exe") or py.endswith("/python")
