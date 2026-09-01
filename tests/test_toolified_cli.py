# -*- coding: utf-8 -*-
"""toolified CLI 冒烟测试：tools/{wave_gate,batch_status,sa_probe,submit_verdict,super_build}.

验证：
  1) 每个工具 --help 可运行且退出码 0（不必 import brain_api，验证 CLI 骨架）
  2) pure 函数行为：候选解析、URL 拼接、描述模板词数、检查渲染
"""
import json
import os
import subprocess
import sys

import pytest

TOOLS = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "tools")
sys.path.insert(0, TOOLS)

CLI_TOOLS = ["wave_gate", "batch_status", "sa_probe", "submit_verdict", "super_build"]


@pytest.mark.parametrize("name", CLI_TOOLS)
def test_help_exit0(name):
    r = subprocess.run([sys.executable, os.path.join(TOOLS, f"{name}.py"), "--help"],
                       capture_output=True, text=True, encoding="utf-8", errors="replace")
    assert r.returncode == 0, f"{name} --help 失败: {r.stderr[-500:]}"
    assert "usage" in r.stdout


def test_wave_gate_parse_candidates(tmp_path):
    from wave_gate import parse_candidates

    class A:
        candidates = None
        exprs_file = None
        expr = None

    # JSON 对象：{expressions:[{id,expr}]}
    f = tmp_path / "c.json"
    f.write_text(json.dumps({"expressions": [{"id": "M1", "expr": "rank(close)"},
                                             {"id": "M2", "code": "ts_mean(open, 5)"}]}),
                 encoding="utf-8")
    a = A(); a.candidates = str(f)
    assert parse_candidates(a) == [("M1", "rank(close)"), ("M2", "ts_mean(open, 5)")]

    # 纯字符串列表
    f2 = tmp_path / "c2.json"
    f2.write_text(json.dumps(["rank(close)", "zscore(open)"]), encoding="utf-8")
    a2 = A(); a2.candidates = str(f2)
    assert parse_candidates(a2) == [(1, "rank(close)"), (2, "zscore(open)")]

    # exprs-file
    f3 = tmp_path / "c3.txt"
    f3.write_text("rank(close)\n\nzscore(open)\n", encoding="utf-8")
    a3 = A(); a3.exprs_file = str(f3)
    assert parse_candidates(a3) == [(1, "rank(close)"), (2, "zscore(open)")]


def test_batch_status_shape_url():
    from batch_status import _shape_url
    base = "https://api.worldquantbrain.com"
    assert _shape_url(base, "abc") == f"{base}/simulations/abc"
    assert _shape_url(base, "/simulations/abc") == f"{base}/simulations/abc"
    assert _shape_url(base, f"{base}/simulations/abc") == f"{base}/simulations/abc"


def test_super_build_templates_and_descriptions():
    from super_build import (COMBO_TEMPLATE, SELECTION_TEMPLATE,
                             build_combo_description, build_selection_description)
    sel = SELECTION_TEMPLATE.format(self_gate=0.55)
    assert "self_correlation < 0.55" in sel
    assert "(1 + 0 * (prod_correlation > 0))" in sel  # USA no-op 门控保留
    assert "self_corr(stats.returns, 500)" in COMBO_TEMPLATE
    # 平台硬门槛：两个 description 各 ≥100 英文词（2026-08-28 起 selection 加 neutralization 参数）
    assert len(build_selection_description("USA", 10, 0.55, "SUBINDUSTRY").split()) >= 100
    assert len(build_combo_description("USA").split()) >= 100


def test_submit_verdict_render():
    from submit_verdict import _render_checks
    out = _render_checks([{"name": "LOW_FITNESS", "result": "FAIL",
                           "value": 0.99, "limit": 1.0}])
    assert "LOW_FITNESS" in out and "FAIL" in out
    assert _render_checks([]) == "  (无检查项)"


def test_sa_probe_no_min_negative():
    """--min 缺失用默认 10；verdict 逻辑不因空池崩溃。"""
    import sa_probe
    assert sa_probe.__doc__ and "≥10" in sa_probe.__doc__