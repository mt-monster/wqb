# -*- coding: utf-8 -*-
"""tests/unit/04_gates/test_basket_diversity_gate.py — 篮子簇识别+结构多样性闸单测。

覆盖 tools/gates/basket_diversity_gate.py：
  - identify_clusters 连通分量（链式近亲、无近亲）
  - structural_diversity 数据集/机制分布 + 过度集中
  - review_basket 默认阈值读 config、WARN vs --strict FAIL
  - subprocess CLI 退出码 0/1/2
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

import basket_diversity_gate as bdg  # noqa: E402
from wqb import config as wqb_config  # noqa: E402

GATE_PY = _REPO / "tools" / "gates" / "basket_diversity_gate.py"


def _matrix():
    # A-B 0.8, B-C 0.75, A-C 0.2 => 阈值0.7下 A,B,C 连成一簇（经 B）
    return {"A": {"B": 0.8, "C": 0.2}, "B": {"A": 0.8, "C": 0.75}, "C": {"A": 0.2, "B": 0.75}}


# ---------------- identify_clusters ----------------

def test_clusters_chain_connected():
    cl = bdg.identify_clusters(["A", "B", "C"], _matrix(), 0.7)
    assert cl == [["A", "B", "C"]]


def test_clusters_high_threshold_none():
    # 阈值0.9：只有 A-B 0.8 不达0.9 => 无簇
    assert bdg.identify_clusters(["A", "B", "C"], _matrix(), 0.9) == []


def test_clusters_abs_negative_corr():
    m = {"A": {"B": -0.85}, "B": {"A": -0.85}}
    assert bdg.identify_clusters(["A", "B"], m, 0.7) == [["A", "B"]]


def test_clusters_singleton_excluded():
    m = {"A": {"B": 0.1}, "B": {"A": 0.1}, "C": {}}
    assert bdg.identify_clusters(["A", "B", "C"], m, 0.7) == []


# ---------------- structural_diversity ----------------

def test_diversity_counts_and_over():
    meta = {"A": {"dataset": "d1", "family": "f1"}, "B": {"dataset": "d1", "family": "f2"},
            "C": {"dataset": "d2", "family": "f1"}}
    d = bdg.structural_diversity(["A", "B", "C"], meta, warn_per_dataset=2)
    assert d["dataset_counts"]["d1"] == 2
    assert d["over_concentrated"] == []  # 2 不 > 2
    d1 = bdg.structural_diversity(["A", "B", "C"], meta, warn_per_dataset=1)
    assert d1["over_concentrated"] == [{"dataset": "d1", "count": 2}]


def test_diversity_unknown_dataset_not_flagged():
    meta = {"A": {}, "B": {}}
    d = bdg.structural_diversity(["A", "B"], meta, warn_per_dataset=1)
    assert d["over_concentrated"] == []


# ---------------- review_basket ----------------

def test_review_default_threshold_from_config():
    meta = {"A": {"dataset": "d1"}, "B": {"dataset": "d2"}, "C": {"dataset": "d3"}}
    r = bdg.review_basket(["A", "B", "C"], _matrix(), meta)
    assert r["threshold"] == wqb_config.BASKET_MUTUAL_CORR_MAX == 0.7
    assert r["clusters"] == [["A", "B", "C"]]
    assert r["ok"] is True  # 非 strict，簇仅 WARN
    assert any("近亲簇" in w for w in r["warnings"])


def test_review_strict_over_concentration_fails():
    meta = {"A": {"dataset": "d1"}, "B": {"dataset": "d1"}, "C": {"dataset": "d1"}}
    r = bdg.review_basket(["A", "B", "C"], _matrix(), meta, warn_per_dataset=2, strict=True)
    assert r["ok"] is False
    assert any("同源集中" in e for e in r["errors"])


def test_review_nonstrict_over_concentration_warns():
    meta = {"A": {"dataset": "d1"}, "B": {"dataset": "d1"}, "C": {"dataset": "d1"}}
    r = bdg.review_basket(["A", "B", "C"], _matrix(), meta, warn_per_dataset=2, strict=False)
    assert r["ok"] is True
    assert any("同源集中" in w for w in r["warnings"])


def test_review_clean_basket_no_warnings():
    m = {"A": {"B": 0.1}, "B": {"A": 0.1}}
    meta = {"A": {"dataset": "d1"}, "B": {"dataset": "d2"}}
    r = bdg.review_basket(["A", "B"], m, meta)
    assert r["ok"] is True
    assert r["clusters"] == []
    assert r["warnings"] == []


# ---------------- CLI ----------------

def _run(args):
    return subprocess.run([sys.executable, str(GATE_PY)] + args,
                          capture_output=True, text=True, cwd=str(_REPO))


def test_cli_exit0(tmp_path):
    mx = tmp_path / "m.json"; mx.write_text(json.dumps(_matrix()), encoding="utf-8")
    meta = {"A": {"dataset": "d1"}, "B": {"dataset": "d2"}, "C": {"dataset": "d3"}}
    mt = tmp_path / "meta.json"; mt.write_text(json.dumps(meta), encoding="utf-8")
    p = _run(["--matrix", str(mx), "--meta", str(mt)])
    assert p.returncode == 0, p.stdout + p.stderr
    assert json.loads(p.stdout)["ok"] is True


def test_cli_strict_exit1(tmp_path):
    mx = tmp_path / "m.json"; mx.write_text(json.dumps(_matrix()), encoding="utf-8")
    meta = {"A": {"dataset": "d1"}, "B": {"dataset": "d1"}, "C": {"dataset": "d1"}}
    mt = tmp_path / "meta.json"; mt.write_text(json.dumps(meta), encoding="utf-8")
    p = _run(["--matrix", str(mx), "--meta", str(mt), "--strict"])
    assert p.returncode == 1
    assert json.loads(p.stdout)["ok"] is False


def test_cli_bad_input_exit2(tmp_path):
    mt = tmp_path / "meta.json"; mt.write_text("{}", encoding="utf-8")
    p = _run(["--matrix", str(tmp_path / "nonexist.json"), "--meta", str(mt)])
    assert p.returncode == 2
