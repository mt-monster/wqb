"""MCP 静态门禁（_toolkit_gate_check）单元测试 — 无网络。

覆盖 2026-11-20 补的**形态 A 三项**（算子存在性 / 元数 / 命名参数）：
这三种错误在平台侧表现为「父 multisim 状态 ERROR、出错条 ERROR、其余全部 CANCELLED」，
即整批槽位净损失；补进闸后它们在本地就被拦下。

另含 `ts_target_tvr_*` 的 `target_tvr` 平台必填规则（catalog 名义有默认值但平台报
``Required attribute "target_tvr" must have a value.``）。
"""
import os
import sys
from unittest.mock import patch

import pytest

MCP_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
REPO_ROOT = os.path.dirname(MCP_DIR)
SRC = os.path.join(REPO_ROOT, "src")
if SRC not in sys.path:
    sys.path.insert(0, SRC)


@pytest.fixture(scope="module")
def gate():
    """导入 tools_sim 并返回 _toolkit_gate_check。

    闸依赖 platform_constraints.json（fail-closed）与 verifier；缺任一 ⇒
    用例断言「必须拦下形态 A 三项」会失败，故先检查前置条件。
    """
    if MCP_DIR not in sys.path:
        sys.path.insert(0, MCP_DIR)
    import tools_sim
    pc = tools_sim._load_toolkit_pc()
    if pc is None:
        pytest.skip("platform_constraints.json 不可达（静态闸 fail-closed，需 skill 目录）")
    return tools_sim


def _issues(gate_mod, exprs):
    res = gate_mod._toolkit_gate_check(exprs)
    if res is None:
        return {}
    return {int(k): v for k, v in res["failed_expressions"].items()}


def test_ghost_operator_blocked(gate):
    """幽灵算子 ts_max 必须被本地拦下（否则整批 CANCELLED）。"""
    issues = _issues(gate, ["group_rank(ts_max(close, 252), industry)"])
    assert issues, "ts_max 应被静态闸拦下"
    joined = "; ".join(issues.get(1, []))
    assert "OP_ARITY" in joined or "INACCESSIBLE_OP" in joined, joined


def test_arity_too_few_args_blocked(gate):
    """元数不足（ts_rank 只给 1 个参数）必须被拦下。"""
    issues = _issues(gate, ["group_rank(ts_rank(close), industry)"])
    assert issues, "ts_rank(x) 应被静态闸拦下"
    assert any("ARITY" in s or "SYNTAX" in s for s in issues.get(1, [])), issues


def test_arity_too_many_positional_blocked(gate):
    """位置参数过多必须被拦下。"""
    issues = _issues(gate, ["group_rank(ts_rank(close, 252, extra), industry)"])
    assert issues, "ts_rank(x,252,extra) 应被静态闸拦下"


def test_tvr_target_required_blocked(gate):
    """ts_target_tvr_decay 缺 target_tvr ⇒ 平台必填 → 必须本地拦下。"""
    issues = _issues(gate, ["ts_target_tvr_decay(close, lambda_min=0, lambda_max=1)"])
    assert issues, "缺 target_tvr 应被静态闸拦下"
    assert any("target_tvr" in s for s in issues.get(1, [])), issues.get(1)


def test_tvr_target_supplied_passes(gate):
    """显式给出 target_tvr 的写法不该被拦（除其它闸外）。"""
    res = gate._toolkit_gate_check(["ts_target_tvr_decay(close, lambda_min=0, lambda_max=1, target_tvr=0.1)"])
    assert res is None or 1 not in res["failed_expressions"]


def test_valid_expression_passes(gate):
    """正常表达式不得被新闸误拒（防假阳性阻断生产）。"""
    res = gate._toolkit_gate_check(["group_rank(ts_zscore(ts_backfill(close, 66), 252), industry)"])
    assert res is None or 1 not in res["failed_expressions"]


# --- 2026-11-23 REGULAR scope 闸（平台 get_operators 103 个零漂移核对）---

@pytest.mark.parametrize("expr", [
    "generate_stats(alpha)",                  # COMBO-only
    "combo_a(alpha, nlength=250)",            # COMBO-only
    "rank(reduce_sum(alpha))",                # COMBO-only reduce_*
    "rank(self_corr(close))",                 # COMBO-only
    "rank(close) + universe_size",            # SELECTION-only（无参形态）
])
def test_non_regular_scope_blocked(gate, expr):
    """COMBO/SELECTION-only 算子进 REGULAR 批 ⇒ 本地必须拦下（否则整批 CANCELLED）。"""
    issues = _issues(gate, [expr])
    assert issues, f"{expr} 应被 REGULAR scope 闸拦下"
    assert any("[SCOPE]" in s for s in issues.get(1, [])), issues


def test_regular_scope_passes(gate):
    """REGULAR 域算子不得被 scope 闸误拒。"""
    res = gate._toolkit_gate_check(["group_rank(ts_zscore(ts_backfill(close, 66), 252), industry)"])
    assert res is None or 1 not in res["failed_expressions"]
