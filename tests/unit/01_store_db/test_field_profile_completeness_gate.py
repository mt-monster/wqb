# -*- coding: utf-8 -*-
"""field_profile_completeness_gate 守护：全字段探测禁止抽样的机械闸契约。"""
from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[3]
GATE_PATH = REPO_ROOT / "tools" / "gates" / "field_profile_completeness_gate.py"

spec = importlib.util.spec_from_file_location("fpc_gate", GATE_PATH)
gate = importlib.util.module_from_spec(spec)
sys.modules["fpc_gate"] = gate
spec.loader.exec_module(gate)


def _write(tmp_path: Path, body: str) -> Path:
    p = tmp_path / "profile.md"
    p.write_text(body, encoding="utf-8")
    return p


def test_complete_profile_passes(tmp_path):
    p = _write(tmp_path, """# ds
## 1. 字段全表
| 字段 | 类型 | cov | aC | 含义 |
|---|---|---|---|---|
| `alpha_f1` | MATRIX | .9 | 1 | a |
| `beta_f2` | VECTOR | .8 | 2 | b |
## 10. 实测
| 字段 | longCount |
|---|---:|
| `alpha_f1` | 527 |
| `beta_f2` | 118 |
""")
    res = gate.check_profile(p)
    assert res["ok"] is True, res["problems"]
    assert res["full_field_count"] == 2


def test_placeholder_row_fails(tmp_path):
    """分母用 `*_active` 通配占位 ⇒ FAIL（清单不全就谈不上全量）。"""
    p = _write(tmp_path, """# ds
## 1. 字段全表
| 字段 | 类型 |
|---|---|
| `alpha_f1` | MATRIX |
| `*_active`（8 个同构孪生） | VECTOR |
## 10. 实测
| 字段 | longCount |
|---|---:|
| `alpha_f1` | 527 |
""")
    res = gate.check_profile(p)
    assert res["ok"] is False
    assert any("通配" in s for s in res["problems"])


def test_missing_field_readout_fails(tmp_path):
    """声明了字段但无实测读数 ⇒ FAIL。"""
    p = _write(tmp_path, """# ds
## 1. 字段全表
| 字段 | 类型 |
|---|---|
| `alpha_f1` | MATRIX |
| `beta_f2` | VECTOR |
## 10. 实测
| 字段 | longCount |
|---|---:|
| `alpha_f1` | 527 |
""")
    res = gate.check_profile(p)
    assert res["ok"] is False
    assert "beta_f2" in res["missing_ids"]


def test_bold_numbers_count_as_readout(tmp_path):
    """历史档案用 **527** 粗体数字，必须认作实测读数。"""
    p = _write(tmp_path, """# ds
## 1. 字段全表
| 字段 | 类型 |
|---|---|
| `alpha_f1` | MATRIX |
## 10. 实测
| 字段 | longCount |
|---|---:|
| `alpha_f1` | **527** (88%) |
""")
    res = gate.check_profile(p)
    assert res["ok"] is True, res["problems"]
    assert res["measured_with_readout"] == 1


def test_real_fhp_profile_passes():
    """真实档案：fund_holdings_panel 30 字段全量探测后必须 PASS。"""
    p = REPO_ROOT / "tracking" / "KOR" / "reference" / "datasets" / "fund_holdings_panel.md"
    if not p.exists():
        pytest.skip("fhp 档案不存在")
    res = gate.check_profile(p)
    assert res["ok"] is True, res["problems"]
    assert res["full_field_count"] == 30
