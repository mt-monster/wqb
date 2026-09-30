# -*- coding: utf-8 -*-
"""R3（审计 N3）：WebDataScope RA / PPA 资格门失败计数只有一份实现——src/wqb/config.py。

world-quant-brain-mcp/mcp_core.py 在仓库布局下直接引用它；Docker 镜像只打包 MCP 目录（没有 src/），
用 mcp_core 里的冻结副本。本文件逐项断言副本与 wqb.config 一致（改口径只改 wqb.config，再同步副本），
并守住 N3 的回归：同一组 checks，生产口径 failed_ra=3，旧的 config 分叉实现给 0。
"""
import ast
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[3]
for _p in (REPO_ROOT / "src", REPO_ROOT / "tools"):
    if str(_p) not in sys.path:
        sys.path.insert(0, str(_p))

from wqb import config as C  # noqa: E402

MCP_CORE = REPO_ROOT / "world-quant-brain-mcp" / "mcp_core.py"
EXPECTED_IMPORTS = {"RA_2Y_NAMES", "RA_CHECK_NAMES", "PPA_CHECK_NAMES",
                    "check_counts_as_failed", "compute_webdata_failed_counts"}

#: N3 实证的那组 checks（沙箱第一轮 §12 步 8）
N3_CHECKS = [
    {"name": "LOW_2Y_SHARPE", "result": "WARNING", "value": 0.9, "limit": 1.0},
    {"name": "IS_LADDER_SHARPE", "result": "WARNING", "value": 1.1, "limit": 1.2},
    {"name": "LOW_SUB_UNIVERSE_SHARPE", "result": "FAIL", "value": 0.4, "limit": 0.6},
]

BATTERY = [
    [],
    None,
    N3_CHECKS,
    [{"name": "LOW_SHARPE", "result": "PASS", "value": 0.8}],          # PASS 但 value<1：PPA 仍计
    [{"name": "LOW_SHARPE", "result": "FAIL", "value": 1.3}],
    [{"name": "LOW_ROBUST_UNIVERSE_SHARPE.WITH_RATIO", "result": "FAIL", "value": 2.43, "limit": 2.44}],
    [{"name": "HIGH_TURNOVER", "result": "PENDING"}, {"name": "LOW_TURNOVER", "result": "ERROR"}],
    [{"name": "CONCENTRATED_WEIGHT", "result": None}, "not-a-dict", 7,
     {"name": "HIGH_DRAWDOWN", "result": "FAIL"}, {"name": "MATCHES_PYRAMID", "result": "PASS"}],
]


def _frozen_copy():
    """执行 mcp_core.py 中 `except ImportError:` 分支（Docker 冻结副本）得到其定义，不导入 mcp_core 本体。"""
    tree = ast.parse(MCP_CORE.read_text(encoding="utf-8"))
    for node in ast.walk(tree):
        if not isinstance(node, ast.Try):
            continue
        imports = [s for s in node.body if isinstance(s, ast.ImportFrom) and s.module == "wqb.config"]
        if not imports:
            continue
        names = {alias.name for s in imports for alias in s.names}
        ns = {}
        exec(compile(ast.Module(body=node.handlers[0].body, type_ignores=[]), str(MCP_CORE), "exec"), ns)
        return names, ns
    raise AssertionError("mcp_core.py 里找不到 `from wqb.config import …` 的 try/except 块")


def test_mcp_core_references_wqb_config():
    names, _ = _frozen_copy()
    assert names == EXPECTED_IMPORTS


def test_frozen_copy_matches_canonical_names():
    _, ns = _frozen_copy()
    assert ns["_RA_CHECK_NAMES"] == C.RA_CHECK_NAMES
    assert ns["_PPA_CHECK_NAMES"] == C.PPA_CHECK_NAMES
    assert tuple(ns["_RA_2Y_NAMES"]) == tuple(C.RA_2Y_NAMES)
    for res in ("PASS", "PENDING", "FAIL", "WARNING", "ERROR", None):
        assert ns["_ra_bad"](res) is C.check_counts_as_failed(res)


@pytest.mark.parametrize("checks", BATTERY)
def test_frozen_copy_counts_like_canonical(checks):
    _, ns = _frozen_copy()
    assert ns["_failed_counts"](checks) == C.compute_webdata_failed_counts(checks)


def test_n3_regression_production_semantics():
    out = C.compute_webdata_failed_counts(N3_CHECKS)
    assert out["failed_ra"] == 3            # 旧 config 分叉实现：0（只数 FAIL，且名单缺这三项）
    assert out["ra_failed_names"] == ["LOW_2Y_SHARPE", "IS_LADDER_SHARPE", "LOW_SUB_UNIVERSE_SHARPE"]
    assert out["failed_ppa"] == 1           # LOW_SUB_UNIVERSE_SHARPE 也在 PPA 名单
    assert not {"HIGH_DRAWDOWN", "LOW_SELFCORR", "LOW_PNL"} & C.RA_CHECK_NAMES   # 平台不存在的项
    assert "LOW_ROBUST_UNIVERSE_SHARPE.WITH_RATIO" in C.RA_CHECK_NAMES


def test_build_gate_prior_uses_canonical_objects():
    import build_gate_prior_from_inventory as bgp

    assert bgp.RA_CHECK_NAMES is C.RA_CHECK_NAMES
    assert bgp.RA_2Y_NAMES is C.RA_2Y_NAMES
    assert bgp.ra_bad is C.check_counts_as_failed
    alpha = {"is": {"checks": N3_CHECKS}}
    n, names, _extra, _pyr = bgp.screen_checks(alpha)
    assert n == 3 and names == C.compute_webdata_failed_counts(N3_CHECKS)["ra_failed_names"]
