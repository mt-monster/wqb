# -*- coding: utf-8 -*-
"""tests/unit/04_gates/test_full_coverage_gate.py — EUR 全量覆盖闸单测。

覆盖 tools/full_coverage_gate.py 三闸：
  - 字段全量覆盖闸：extract_fields / apply_field_gate
  - 模板族全量闸：apply_family_gate
  - 边界算子穷举闸：_extract_numeric_args / _extract_axis_args / apply_boundary_gate

同时通过 subprocess 覆盖 CLI 端行为（--gate-mode、--near-gate、--json）。
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

_TOOLS = str(Path(__file__).resolve().parents[3] / "tools")
if _TOOLS not in sys.path:
    sys.path.insert(0, _TOOLS)

import full_coverage_gate as fcg  # noqa: E402

BOUNDARY_CONFIG = {
    "operators": {
        "ts_mean": {
            "kind": "window",
            "legal_values": [5, 22, 66, 252],
            "min_coverage_for_near_gate": 2,
        },
        "group_rank": {
            "kind": "axis",
            "legal_axes": ["industry", "sector", "subindustry", "market"],
            "min_coverage_for_near_gate": 2,
            "must_include": ["subindustry", "industry"],
        },
        "signed_power": {
            "kind": "exponent",
            "legal_values": [2.0, 2.5, 3.0],
            "min_coverage_for_near_gate": 3,
        },
    }
}


# ---------------- extractors ----------------


def test_extract_ops_ignores_reserved():
    assert "or" not in fcg.extract_ops("and(a, or(b, c))")


def test_extract_fields_excludes_ops_and_kwargs():
    fields = fcg.extract_fields("rank(ts_mean(foo, 252))")
    assert fields == {"foo"}


def test_extract_numeric_args_skips_embedded_numbers_in_field_names():
    # 关键回归：mdl238_global_rank 里的 238 不能当参数
    got = fcg._extract_numeric_args("rank(ts_mean(mdl238_global_rank, 252))")
    assert ("ts_mean", 252.0) in got
    assert all(v != 238.0 for _op, v in got)


def test_extract_numeric_args_kwarg_form():
    got = fcg._extract_numeric_args("rank(winsorize(foo, std=2))")
    assert ("winsorize", 2.0) in got


def test_extract_axis_args_matches_right_call():
    # 关键回归：group_rank(..., exchange) 应记为 group_rank 的 axis，不是外层 rank 的
    got = fcg._extract_axis_args("rank(group_rank(foo, exchange))")
    assert ("group_rank", "exchange") in got
    assert ("rank", "exchange") not in got


# ---------------- field_coverage gate ----------------


def test_field_gate_full_coverage_passes():
    exprs = ["rank(foo)", "rank(bar)", "rank(baz)"]
    known = {"foo", "bar", "baz"}
    r = fcg.apply_field_gate(exprs, known, 1.0, "enforce")
    assert r["verdict"] == "PASS"
    assert r["coverage"] == 1.0


def test_field_gate_missing_fails():
    exprs = ["rank(foo)"]
    known = {"foo", "bar", "baz"}
    r = fcg.apply_field_gate(exprs, known, 1.0, "enforce")
    assert r["verdict"] == "FAIL"
    assert r["coverage"] == pytest.approx(1 / 3, abs=1e-3)
    assert set(r["missing_sample"]) == {"bar", "baz"}


def test_field_gate_warn_mode_downgrades():
    r = fcg.apply_field_gate(["rank(foo)"], {"foo", "bar"}, 1.0, "warn")
    assert r["verdict"] == "WARN"


# ---------------- family gate ----------------


def test_family_gate_passes_when_history_enough(tmp_path):
    # 造一个 campaign_dir，同名 dataset 前缀的 3 个候选文件，各带一个 template_family
    cd = tmp_path / "campaign"
    (cd / "candidates").mkdir(parents=True)
    (cd / "candidates" / "model238_wave1.json").write_text(
        json.dumps({"expressions": [{"expr": "x", "template_family": "fam_a"}]}, indent=1),
        encoding="utf-8",
    )
    (cd / "candidates" / "model238_wave2.json").write_text(
        json.dumps({"expressions": [{"expr": "y", "family_id": "fam_b"}]}, indent=1),
        encoding="utf-8",
    )
    (cd / "candidates" / "model238_wave3.json").write_text(
        json.dumps({"expressions": [{"expr": "z", "family": "fam_c"}]}, indent=1),
        encoding="utf-8",
    )
    r = fcg.apply_family_gate(str(cd), "model238", min_families=3, exprs=["x"], mode="enforce")
    assert r["verdict"] == "PASS"
    assert set(r["used_families"]) == {"fam_a", "fam_b", "fam_c"}


def test_family_gate_warns_on_insufficient(tmp_path):
    r = fcg.apply_family_gate(str(tmp_path), "model238", min_families=3, exprs=["x"], mode="warn")
    assert r["verdict"] == "WARN"
    assert r["total"] == 0


# ---------------- boundary gate ----------------


def test_boundary_gate_flags_illegal_value():
    r = fcg.apply_boundary_gate(
        ["rank(ts_mean(foo, 77))"], BOUNDARY_CONFIG, near_gate=False, mode="enforce"
    )
    assert r["verdict"] == "FAIL"
    assert r["illegal_count"] == 1
    assert r["illegal"][0]["value"] == 77.0


def test_boundary_gate_flags_illegal_axis():
    r = fcg.apply_boundary_gate(
        ["rank(group_rank(foo, exchange))"], BOUNDARY_CONFIG, near_gate=False, mode="enforce"
    )
    assert r["verdict"] == "FAIL"
    assert r["illegal"][0]["illegal_axes"] == ["exchange"]


def test_boundary_gate_near_gate_rejects_insufficient_coverage():
    # signed_power 单档不够 min_coverage=3
    r = fcg.apply_boundary_gate(
        ["rank(signed_power(foo, 2.5))"], BOUNDARY_CONFIG, near_gate=True, mode="enforce"
    )
    assert r["verdict"] == "FAIL"
    assert any(i["op"] == "signed_power" for i in r["incomplete"])


def test_boundary_gate_passes_clean_expr():
    r = fcg.apply_boundary_gate(
        ["rank(ts_mean(foo, 252))"], BOUNDARY_CONFIG, near_gate=False, mode="enforce"
    )
    assert r["verdict"] == "PASS"


def test_boundary_gate_ignores_unknown_ops_but_reports_them():
    r = fcg.apply_boundary_gate(
        ["rank(some_unknown_op(foo))"], BOUNDARY_CONFIG, near_gate=False, mode="warn"
    )
    # 未知算子不算 FAIL，但要报出来
    assert r["verdict"] == "PASS"
    assert "some_unknown_op" in r["unknown_ops"]


# ---------------- CLI end-to-end ----------------


SCRIPT = Path(__file__).resolve().parents[3] / "tools" / "full_coverage_gate.py"


def _run_cli(args, check_return=False):
    return subprocess.run(
        [sys.executable, str(SCRIPT), *args],
        capture_output=True, text=True, encoding="utf-8",
    )


def test_cli_off_mode_reports_all_gates():
    p = _run_cli([
        "--region", "EUR", "--dataset", "model238",
        "--expr", "rank(ts_mean(mdl238_global_rank,252))",
        "--gate-mode", "off", "--json",
    ])
    assert p.returncode == 0
    data = json.loads(p.stdout)
    assert data["mode"] == "off"
    assert len(data["gates"]) == 3
    # off 模式下 verdict 保持 FAIL 但整体仍 exit 0
    assert all(g["verdict"] in ("PASS", "FAIL", "WARN") for g in data["gates"])


def test_cli_enforce_mode_fails_with_missing_fields():
    p = _run_cli([
        "--region", "EUR", "--dataset", "model238",
        "--expr", "rank(ts_mean(mdl238_global_rank,252))",
        "--gate-mode", "enforce", "--json",
    ])
    assert p.returncode == 1
    data = json.loads(p.stdout)
    assert data["ok"] is False


def test_cli_near_gate_flag_exposes_incomplete():
    p = _run_cli([
        "--region", "EUR", "--dataset", "model238",
        "--expr", "rank(ts_mean(mdl238_global_rank,252))",
        "--gate-mode", "warn", "--near-gate", "--json",
    ])
    assert p.returncode == 0
    data = json.loads(p.stdout)
    b = [g for g in data["gates"] if g["gate"] == "boundary_ops"][0]
    assert b["near_gate"] is True
    # ts_mean 只用了 1 档但 min_cov=2 → incomplete
    assert any(i["op"] == "ts_mean" for i in b["incomplete"])


def test_cli_missing_candidates_errors():
    p = _run_cli(["--region", "EUR", "--dataset", "model238", "--gate-mode", "warn"])
    assert p.returncode == 2
