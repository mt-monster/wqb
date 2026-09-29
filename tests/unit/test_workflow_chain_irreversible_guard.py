# -*- coding: utf-8 -*-
"""「提交类节点不入链」由代码强制（skills 审查 X-9 / RA-116）。

此前这条只是 `workflow_chain` docstring 里的一句话：链里放一个 `confirm_submit=True` 的 submit_alpha，
链就会照跑、真的 POST /alphas/{id}/submit（通过即提交，无撤回）。现在 `execute_chain` 在执行任何步骤之前先检查。
"""
import os
import sys

import pytest

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(ROOT, "src"))

from wqb.workflow import executor as EX  # noqa: E402


def _step(node, **params):
    return {"node": node, "params": params}


def test_flags_only_irreversible_nodes_with_truthy_confirm():
    chain = [
        _step("campaign", region="KOR", stage="S0"),
        _step("submit_alpha", alpha_id="A1", confirm_submit=True),
        _step("superalpha", region="KOR", components=[], confirm_submit="true"),
        _step("submit_alpha", alpha_id="A2"),                         # 缺省 = 只预检
        _step("submit_alpha", alpha_id="A3", confirm_submit=False),   # 显式 False
        _step("submit_alpha", alpha_id="A4", confirm_submit="false"),  # 字符串 false 不算真
        _step("gem", region="KOR", confirm_submit=True),              # 非提交类节点，不归这条管
    ]
    assert EX.chain_irreversible_steps(chain) == [(1, "submit_alpha"), (2, "superalpha")]


@pytest.mark.parametrize("bad", [None, [], [None], ["x"], [{"node": "submit_alpha", "params": None}],
                                 [{"node": "submit_alpha", "params": "oops"}]])
def test_tolerates_malformed_chains(bad):
    assert EX.chain_irreversible_steps(bad) == []


@pytest.mark.parametrize("dry_run", [False, True])
def test_execute_chain_refuses_whole_chain_without_running_anything(tmp_path, monkeypatch, dry_run):
    ex = EX.WorkflowExecutor(db_path=str(tmp_path / "wqb.db"))

    def boom(*a, **k):  # 任何步骤被执行都算失败
        raise AssertionError("守卫必须在执行任何步骤之前拒绝整链")

    monkeypatch.setattr(ex, "execute", boom)
    chain = [_step("campaign", region="KOR", stage="S0"),
             _step("submit_alpha", alpha_id="A1", confirm_submit=True)]
    res = ex.execute_chain(chain, dry_run=dry_run)
    assert len(res) == 1 and res[0].success is False and res[0].node == "submit_alpha"
    assert res[0].dry_run is dry_run
    assert "不可逆" in res[0].error and "第 2 步" in res[0].error
    assert res[0].metadata["guard"] == "irreversible_chain_step" and res[0].metadata["steps"] == [1]


def test_precheck_only_submit_step_is_allowed_into_a_chain(tmp_path, monkeypatch):
    ex = EX.WorkflowExecutor(db_path=str(tmp_path / "wqb.db"))
    called = []

    def fake_execute(node, params, dry_run=False):
        called.append(node)
        return EX.WorkflowResult(success=True, node=node, params=params, dry_run=dry_run)

    monkeypatch.setattr(ex, "execute", fake_execute)
    res = ex.execute_chain([_step("submit_alpha", alpha_id="A1")], dry_run=True)
    assert called == ["submit_alpha"] and res[0].success


def test_guard_is_documented_where_agents_read_it():
    src = open(os.path.join(ROOT, "world-quant-brain-mcp", "tools_workflow.py"), encoding="utf-8").read()
    assert "execute_chain" in src and "整链拒绝" in src
