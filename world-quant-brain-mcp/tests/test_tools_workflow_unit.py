# -*- coding: utf-8 -*-
"""workflow_* MCP 工具单测：confirm_submit 透传不变量（无网络）.

背景：tools_workflow 是 `wqb.workflow` 节点到 MCP 的薄包装层。confirm_submit 是
submit_alpha / superalpha / judge 三个节点上的敏感决策开关（默认 False = 不提交），
一旦在包装层被吞掉或默认值被翻转，就会出现"以为没提交其实提交了"的事故。

本文件只验证包装层契约，不打网络：
  - confirm_submit 显式传入时原样落到 executor 收到的 params（bool 类型不丢失）
  - 未传时 MCP 层默认 False 且仍会写入 params（节点侧依赖该 key 存在）
  - dry_run / 其它可选参数同路径透传，未被默认值覆盖
  - registry 的 optional_params 声明与函数签名一致（防文档/校验漂移）
  - 工具注册齐全（拆模块不丢工具）

注：tools_workflow 每次调用都通过 `_get_workflow_executor()` 运行时重取
`wqb.workflow.execute` 绑定，因此打桩必须落在 `wqb.workflow.executor.get_executor`
（`execute` 便捷函数的运行时依赖），而不是替换 module 上的 `execute` 属性。
"""
import inspect
import os
import sys

MCP_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# tests/conftest.py 只注入 MCP_DIR；wqb 包在仓库根 src/ 下。
# 与 tools_workflow._get_workflow_executor 的延迟导入保持一致的路径注入方式。
SRC_DIR = os.path.normpath(os.path.join(MCP_DIR, "..", "src"))
if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

import mcp_core
import tools_workflow
from wqb.workflow import executor as wf_executor
from wqb.workflow.executor import WorkflowExecutor, WorkflowResult

CONFIRM_NODES = ("workflow_submit_alpha", "workflow_superalpha", "workflow_judge")


# ---------------------------------------------------------------------------
# 打桩辅助
# ---------------------------------------------------------------------------

class _RecordingExecutor:
    """替身 executor：原样记录 (node_name, params, kwargs)，返回可 to_dict 的结果。"""

    def __init__(self):
        self.calls = []

    def execute(self, node_name, params, **kwargs):
        self.calls.append((node_name, dict(params), kwargs))
        return WorkflowResult(success=True, node=node_name, params=params)

    def execute_chain(self, chain, **kwargs):
        return [self.execute(step["node"], step.get("params", {}), **kwargs)
                for step in chain]


def _install_recorder(monkeypatch):
    """打桩 get_executor，让 workflow 包看到的 execute 便捷函数走替身."""
    recorder = _RecordingExecutor()

    def fake_get_executor():
        return recorder

    # wqb.workflow 包 __init__ 只重导出 execute（from .executor import execute），
    # 包级命名空间没有 get_executor，而 execute 便捷函数在 executor 模块内部
    # 按模块全局解析 get_executor —— 因此只需打桩 executor 模块本身。
    monkeypatch.setattr(wf_executor, "get_executor", fake_get_executor)
    # 重置默认 executor 单例，避免复用真实执行器
    wf_executor._default_executor = None
    return recorder


# ---------------------------------------------------------------------------
# 工具注册 + 签名契约
# ---------------------------------------------------------------------------

def test_workflow_tools_all_registered():
    """7 个 workflow_* 工具必须全部注册到 MCP（防拆分丢工具）。"""
    registered = set(mcp_core.mcp._tool_manager._tools.keys())
    expected = {
        "workflow_list_nodes",
        "workflow_execute",
        "workflow_batch_track",
        "workflow_submit_alpha",
        "workflow_superalpha",
        "workflow_judge",
        "workflow_gem",
        "workflow_campaign",
    }
    missing = expected - registered
    assert not missing, f"workflow 工具丢失: {sorted(missing)}"


def test_confirm_submit_exposed_and_defaults_false():
    """三个敏感节点的 confirm_submit 必须在 MCP 签名上暴露且默认 False.

    默认值必须是字面量 False：若被翻转成 True，调用方省略参数时会静默提交。
    """
    for name in CONFIRM_NODES:
        sig = inspect.signature(getattr(tools_workflow, name))
        assert "confirm_submit" in sig.parameters, f"{name} 未暴露 confirm_submit"
        p = sig.parameters["confirm_submit"]
        assert p.default is False, (
            f"{name} confirm_submit 默认值必须是 False，实际 {p.default!r}"
        )


def test_confirm_submit_declared_in_registry_optional_params():
    """registry 元数据必须声明 confirm_submit，否则 executor 的参数校验会拒绝它.

    workflow_* 传入的 params 会经过 WorkflowExecutor.execute -> registry.validate_params，
    未声明的 key 可能被丢弃/报错，导致确认开关失效。
    """
    _, get_registry = tools_workflow._get_workflow_executor()
    reg = get_registry()
    node_of_tool = {
        "workflow_submit_alpha": "submit_alpha",
        "workflow_superalpha": "superalpha",
        "workflow_judge": "judge",
    }
    for tool, node in node_of_tool.items():
        meta = reg.get_meta(node)
        assert meta is not None, f"节点 {node} 未注册"
        assert "confirm_submit" in meta.optional_params, (
            f"{node} 的 optional_params 缺少 confirm_submit: {meta.optional_params}"
        )


# ---------------------------------------------------------------------------
# confirm_submit 透传
# ---------------------------------------------------------------------------

def test_submit_alpha_confirm_submit_true_passthrough(monkeypatch):
    rec = _install_recorder(monkeypatch)
    tools_workflow.workflow_submit_alpha(alpha_id="a1", confirm_submit=True)

    assert len(rec.calls) == 1
    node, params, kwargs = rec.calls[0]
    assert node == "submit_alpha"
    assert params["confirm_submit"] is True
    assert params["alpha_id"] == "a1"
    assert kwargs.get("dry_run") is False


def test_submit_alpha_confirm_submit_false_default_still_sent(monkeypatch):
    """省略 confirm_submit 时 MCP 层必须默认 False 且显式写入 params.

    节点 submit_alpha.run 用 `if confirm_submit:` 判断，key 缺失与 False 等价，
    但显式写入可让 execute 的返回值/日志/台账里看到实际确认态。
    """
    rec = _install_recorder(monkeypatch)
    out = tools_workflow.workflow_submit_alpha(alpha_id="a1")

    node, params, kwargs = rec.calls[0]
    assert node == "submit_alpha"
    assert params["confirm_submit"] is False
    assert out["params"]["confirm_submit"] is False


def test_submit_alpha_all_fields_passthrough(monkeypatch):
    rec = _install_recorder(monkeypatch)
    tools_workflow.workflow_submit_alpha(
        alpha_id="a9",
        name="prod-9",
        color="BLUE",
        tags=["PowerPool", "x"],
        descriptions="desc",
        force=True,
        confirm_submit=False,
        verify_timeout=60,
        dry_run=True,
    )

    _, params, kwargs = rec.calls[0]
    assert params == {
        "alpha_id": "a9",
        "name": "prod-9",
        "color": "BLUE",
        "tags": ["PowerPool", "x"],
        "descriptions": "desc",
        "force": True,
        "confirm_submit": False,
        "verify_timeout": 60,
    }
    assert kwargs == {"dry_run": True}


def test_submit_alpha_empty_tags_become_empty_list(monkeypatch):
    """tags=None 归一为 []（节点 run 内部再兜底为 PowerPoolSelected）。"""
    rec = _install_recorder(monkeypatch)
    tools_workflow.workflow_submit_alpha(alpha_id="a1")
    assert rec.calls[0][1]["tags"] == []


def test_superalpha_confirm_submit_true_passthrough(monkeypatch):
    rec = _install_recorder(monkeypatch)
    tools_workflow.workflow_superalpha(
        region="KOR",
        components=["a1", "a2"],
        selection="sel",
        combo="cbo",
        neutralization="INDUSTRY",
        confirm_submit=True,
        dry_run=False,
    )

    node, params, kwargs = rec.calls[0]
    assert node == "superalpha"
    assert params["confirm_submit"] is True
    assert params["components"] == ["a1", "a2"]
    assert params["neutralization"] == "INDUSTRY"
    assert kwargs == {"dry_run": False}


def test_superalpha_confirm_submit_defaults_false(monkeypatch):
    rec = _install_recorder(monkeypatch)
    out = tools_workflow.workflow_superalpha(region="KOR", components=["a1", "a2"])

    _, params, kwargs = rec.calls[0]
    assert params["confirm_submit"] is False
    # 可选表达式缺省保持 None，不能补成空串（节点侧以 None 判定"自动生成"）
    assert params["selection"] is None
    assert params["combo"] is None
    assert out["params"]["confirm_submit"] is False


def test_judge_confirm_submit_true_passthrough(monkeypatch):
    rec = _install_recorder(monkeypatch)
    tools_workflow.workflow_judge(
        alpha_id="a7", trend_window_days=180, llm_enabled=False, confirm_submit=True
    )

    node, params, kwargs = rec.calls[0]
    assert node == "judge"
    assert params == {
        "alpha_id": "a7",
        "trend_window_days": 180,
        "llm_enabled": False,
        "confirm_submit": True,
    }
    assert kwargs == {"dry_run": False}


def test_judge_confirm_submit_defaults_false(monkeypatch):
    rec = _install_recorder(monkeypatch)
    tools_workflow.workflow_judge(alpha_id="a7")
    _, params, _ = rec.calls[0]
    assert params["confirm_submit"] is False
    assert params["trend_window_days"] == 365
    assert params["llm_enabled"] is True


def test_confirm_submit_bool_type_not_coerced(monkeypatch):
    """显式传入的 bool 必须保持 bool 身份，不被转成 int/str。"""
    rec = _install_recorder(monkeypatch)
    tools_workflow.workflow_judge(alpha_id="a1", confirm_submit=True)
    val = rec.calls[0][1]["confirm_submit"]
    assert type(val) is bool and val is True


# ---------------------------------------------------------------------------
# 通用 execute 路径 + dry_run 透传
# ---------------------------------------------------------------------------

def test_workflow_execute_nodes_dry_run_forwarded(monkeypatch):
    rec = _install_recorder(monkeypatch)
    out = tools_workflow.workflow_execute(
        "batch_track",
        {"region": "KOR", "wave": "36A", "dataset": "fundamental78"},
        dry_run=True,
    )

    node, params, kwargs = rec.calls[0]
    assert node == "batch_track"
    assert params["region"] == "KOR"
    assert kwargs == {"dry_run": True}
    assert out["success"] is True


def test_batch_track_defaults_forwarded(monkeypatch):
    """concurrency 默认已从 5 改为 7（七槽填槽），必须原样到达 executor。"""
    rec = _install_recorder(monkeypatch)
    tools_workflow.workflow_batch_track(
        region="KOR", wave="36A", dataset="fundamental78"
    )

    _, params, kwargs = rec.calls[0]
    assert params["concurrency"] == 7
    assert params["max_rounds"] == 3
    assert kwargs == {"dry_run": False}


def test_gem_and_campaign_confirm_free_tools_shape(monkeypatch):
    """gem / campaign 不暴露 confirm_submit（无提交动作），字段各自透传。"""
    rec = _install_recorder(monkeypatch)
    tools_workflow.workflow_gem(
        region="KOR", dataset_id="fundamental78", delay=1,
        universe="TOP3000", data_category="fundamental", detached=False,
    )
    tools_workflow.workflow_campaign(
        region="KOR", stage="S2", dataset="fundamental78", wave="36A",
        subcommand="gate", extra_args=["--json"],
    )

    assert len(rec.calls) == 2
    gem_params = rec.calls[0][1]
    campaign_params = rec.calls[1][1]
    assert "confirm_submit" not in gem_params
    assert "confirm_submit" not in campaign_params
    assert gem_params["universe"] == "TOP3000"
    assert gem_params["detached"] is False
    assert campaign_params["subcommand"] == "gate"
    assert campaign_params["extra_args"] == ["--json"]


def test_workflow_list_nodes_shape(monkeypatch):
    """list_nodes 必须返回 count 与每项元数据，且不触发执行。"""
    rec = _install_recorder(monkeypatch)
    out = tools_workflow.workflow_list_nodes()

    assert rec.calls == []
    assert out["count"] == len(out["nodes"])
    assert out["count"] == 7
    names = {n["name"] for n in out["nodes"]}
    assert {"submit_alpha", "superalpha", "judge"} <= names
    for item in out["nodes"]:
        assert set(item) == {"name", "description", "category", "phase",
                             "required_params", "optional_params"}
        if item["name"] in {"submit_alpha", "superalpha", "judge"}:
            assert "confirm_submit" in item["optional_params"]


def test_workflow_result_to_dict_carries_confirm_submit(monkeypatch):
    """返回给 MCP 调用方的 payload 里能看到 confirm_submit（审计/台账依赖）。"""
    rec = _install_recorder(monkeypatch)
    out = tools_workflow.workflow_submit_alpha(alpha_id="a1", confirm_submit=True)

    assert out["success"] is True
    assert out["node"] == "submit_alpha"
    assert out["params"]["confirm_submit"] is True


def test_stub_does_not_touch_real_executor(monkeypatch):
    """回归保护：打桩后真实执行器单例不被创建（确保测试无副作用）。"""
    _install_recorder(monkeypatch)
    tools_workflow.workflow_judge(alpha_id="a1", confirm_submit=False)
    assert wf_executor._default_executor is None
    assert isinstance(WorkflowExecutor, type)
