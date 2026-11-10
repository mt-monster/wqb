# -*- coding: utf-8 -*-
"""tests/unit/04_gates/test_morphology_gate.py — 通用「字段形态→构型」前置闸单测。

覆盖 tools/gates/morphology_gate.py：
  - classify_morphology / classify_family / used_vec_ops / feature_present
  - check_batch 五闸 M1-M5（形态证据/构型匹配/VECTOR聚合多样性/族多样性/区域破墙）
  - 通用性：无区域配置的 region 跳过 M5（不写死区域）
  - check_death_verdict 判死资格
  - subprocess CLI（--spec/--region/--verdict，退出码 0/1/2）
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

_REPO = Path(__file__).resolve().parents[3]
_GATE_DIR = str(_REPO / "tools" / "gates")
if _GATE_DIR not in sys.path:
    sys.path.insert(0, _GATE_DIR)

import morphology_gate as mg  # noqa: E402

GATE_PY = _REPO / "tools" / "gates" / "morphology_gate.py"


def _probe(fid, expr, shape=None, dtype="MATRIX", **meta):
    fm = {"type": dtype, "coverage": 0.95}
    if shape:
        fm["distribution_shape"] = shape
    fm.update(meta)
    return {"field_id": fid, "expression": expr, "field_meta": fm}


PV_EXPR = ("scale(vector_neut(trade_when(rank(adv20)>0.1, ts_kurtosis(ts_backfill(close,5),140), -1), "
           "power(rank(rsk68_weight_dadv),0.5)), shortscale=0.5)")
SH_EXPR = ("hump(subtract(group_rank(divide(vec_sum(ts_backfill(a,44)), vec_avg(ts_backfill(b,44))), "
           "industry), 0.5), hump=0.003)")


# ---------------- classifiers ----------------

def test_classify_morphology_explicit_shape():
    assert mg.classify_morphology({"distribution_shape": "zero_inflated"}) == "zero_inflated"
    assert mg.classify_morphology({"distribution_shape": "ratio_level"}) == "ratio_level"


def test_classify_morphology_vector_fallback():
    assert mg.classify_morphology({"type": "VECTOR"}) == "flow_level"


def test_classify_morphology_sparse_fallback():
    assert mg.classify_morphology({"type": "MATRIX", "non_zero_rate": 0.05}) == "zero_inflated"


def test_classify_family():
    assert mg.classify_family(PV_EXPR) == "info_gate"      # trade_when 先于 ts_shape
    assert mg.classify_family(SH_EXPR) == "group_compare"  # group_rank
    assert mg.classify_family("rank(close)") == "free_explore"


def test_used_vec_ops():
    assert mg.used_vec_ops(SH_EXPR) == {"vec_sum", "vec_avg"}
    assert mg.used_vec_ops("rank(close)") == set()


def test_feature_present_word_boundary():
    assert mg.feature_present("trade_when(rank(adv20)>0.1, x, -1)", ["trade_when"])
    assert not mg.feature_present("hump(x)", ["trade_when"])


# ---------------- check_batch 五闸 ----------------

def _good_batch():
    return [
        _probe("pv_close", PV_EXPR, shape="return_distribution"),
        _probe("vec_ratio", SH_EXPR, shape="ratio_level", dtype="VECTOR"),
    ]


def test_good_batch_passes():
    r = mg.check_batch(_good_batch(), "KOR")
    assert r["ok"], r["errors"]
    assert len(r["families_used"]) >= 2
    assert len(r["vec_ops_used"]) >= 2


def test_m1_missing_field_meta_fails():
    probes = [{"field_id": "x", "expression": SH_EXPR}]
    r = mg.check_batch(probes, "KOR")
    assert not r["ok"]
    assert any("[M1]" in e for e in r["errors"])


def test_m2_morphology_config_mismatch_fails():
    # zero_inflated 却用裸 group_rank（无流动性门控/尾部矩）
    probes = [_probe("sparse", "group_rank(ts_backfill(vec_avg(x),44),sector)",
                     shape="zero_inflated", dtype="VECTOR"),
              _probe("ok", SH_EXPR, shape="ratio_level", dtype="VECTOR")]
    r = mg.check_batch(probes, "KOR")
    assert any("[M2]" in e and "sparse" in e for e in r["errors"])


def test_m3_vector_aggregation_diversity_fails():
    # 两条都只用 vec_avg ⇒ 聚合多样性不足
    e1 = "hump(subtract(group_rank(divide(vec_avg(a),vec_avg(b)),industry),0.5),hump=0.003)"
    e2 = "hump(subtract(group_rank(divide(vec_avg(c),vec_avg(d)),sector),0.5),hump=0.003)"
    probes = [_probe("v1", e1, shape="ratio_level", dtype="VECTOR"),
              _probe("v2", e2, shape="ratio_level", dtype="VECTOR")]
    r = mg.check_batch(probes, "KOR")
    assert any("[M3]" in e for e in r["errors"])


def test_m4_family_diversity_fails():
    # 两条同族（都 group_compare）⇒ 族多样性不足
    e2 = "group_zscore(divide(vec_sum(a),vec_avg(b)),industry)"
    probes = [_probe("v1", SH_EXPR, shape="ratio_level", dtype="VECTOR"),
              _probe("v2", e2, shape="ratio_level", dtype="VECTOR")]
    r = mg.check_batch(probes, "KOR")
    assert any("[M4]" in e for e in r["errors"])


def test_m5_region_wall_batch_coverage():
    # KOR 有配置：批次须覆盖 liquidity_gate + smoothing
    r = mg.check_batch(_good_batch(), "KOR")
    assert r["region_config_loaded"] is True
    assert not any("[M5]" in e for e in r["errors"])


def test_universality_region_without_config_skips_m5():
    # 无配置 region（XXX）⇒ M5 跳过，核心闸仍生效（不写死区域）
    r = mg.check_batch(_good_batch(), "XXX")
    assert r["region_config_loaded"] is False
    assert r["ok"], r["errors"]
    assert not any("[M5]" in e for e in r["errors"])


def test_single_probe_skips_family_diversity():
    r = mg.check_batch([_probe("pv_close", PV_EXPR, shape="return_distribution")], "XXX")
    assert not any("[M4]" in e for e in r["errors"])


# ---------------- death verdict ----------------

def test_death_verdict_missing_constraints():
    r = mg.check_death_verdict("XXX", "some_ds")
    assert r["ok"] is False


# ---------------- CLI ----------------

def _run_cli(args):
    return subprocess.run([sys.executable, str(GATE_PY)] + args,
                          capture_output=True, text=True, cwd=str(_REPO))


def test_cli_good_exit0(tmp_path):
    spec = tmp_path / "good.json"
    spec.write_text(json.dumps(_good_batch()), encoding="utf-8")
    p = _run_cli(["--spec", str(spec), "--region", "KOR"])
    assert p.returncode == 0, p.stdout + p.stderr
    assert json.loads(p.stdout)["ok"] is True


def test_cli_bad_exit1(tmp_path):
    spec = tmp_path / "bad.json"
    spec.write_text(json.dumps([{"field_id": "x", "expression": "rank(close)"}]), encoding="utf-8")
    p = _run_cli(["--spec", str(spec), "--region", "KOR"])
    assert p.returncode == 1
    assert json.loads(p.stdout)["ok"] is False


def test_cli_no_input_exit2():
    p = _run_cli(["--region", "KOR"])
    assert p.returncode == 2
