# -*- coding: utf-8 -*-
"""tests/unit/04_gates/test_category_coverage_audit.py — 数据集层穷尽性闸单测。

守三件事（2026-11-06 事故：本地缓存当平台全表 ⇒「某 category 已穷尽」系统性失真）：
  1. 分母必须是平台全表 —— 空集 / 分页不全 / 快照不完整都不得产出 EXHAUSTED；
  2. 分子是「DB 回测记录 ∪ 显式清单」，只认回测证据与显式声明；
  3. category 不存在必须报错 —— 空差集不能被读成「已穷尽」。
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

_GATES = str(Path(__file__).resolve().parents[3] / "tools" / "gates")
if _GATES not in sys.path:
    sys.path.insert(0, _GATES)

import category_coverage_audit as cca  # noqa: E402

ITEMS = [
    {"id": "other455", "category": {"id": "OTHER"}, "fieldCount": 1500},
    {"id": "other567", "category": {"id": "OTHER"}},
    {"id": "other699", "category": "other"},          # 裸字符串形态
    {"id": "model238", "category": {"id": "MODEL"}},
    {"id": "pv13", "category": {"id": "PV"}},
]

BASE = ["--region", "EUR", "--universe", "TOPCS1600", "--delay", "1", "--no-db"]


def _payload(items, complete=True):
    return {"region": "EUR", "universe": "TOPCS1600", "delay": 1,
            "platform_count": len(items), "complete": complete,
            "pages": 1, "datasets": items}


def _run_main(monkeypatch, argv, payload):
    monkeypatch.setattr(cca, "fetch_platform_datasets", lambda *a, **k: payload)
    return cca.main(argv)


# ---------------- 解析层 ----------------

def test_category_of_handles_nested_dict_plain_string_and_type():
    assert cca._category_of({"category": {"id": "OTHER", "name": "Other"}}) == "OTHER"
    assert cca._category_of({"category": "other"}) == "other"
    assert cca._category_of({"type": "PV"}) == "PV"
    assert cca._category_of({}) == ""


def test_histogram_counts_all_categories():
    hist = cca.category_histogram(ITEMS)
    assert hist["OTHER"] == 2 and hist["other"] == 1
    assert hist["MODEL"] == 1 and hist["PV"] == 1
    assert sum(hist.values()) == len(ITEMS)


def test_resolve_category_is_case_insensitive():
    assert (cca.resolve_category(ITEMS, "other") or "").upper() == "OTHER"


def test_resolve_category_unknown_raises_not_empty_result():
    """「面不存在」与「面已测完」差集都为空，必须靠报错区分。"""
    with pytest.raises(cca.SourceError):
        cca.resolve_category(ITEMS, "SOCIALMEDIA")


# ---------------- 判据层 ----------------

def test_build_report_exhausted_only_when_diff_empty():
    rep = cca.build_report(ITEMS, "OTHER", {"other455", "OTHER567", "other699"})
    assert rep["platform_total"] == 3
    assert rep["untested"] == []
    assert rep["verdict"] == "EXHAUSTED"


def test_build_report_not_exhausted_when_one_missing():
    rep = cca.build_report(ITEMS, "OTHER", {"other455", "other567"})
    assert rep["untested"] == ["other699"]
    assert rep["verdict"] == "NOT_EXHAUSTED"


def test_build_report_never_exhausted_on_empty_scope():
    assert cca.build_report([], "OTHER", {"other455"})["verdict"] == "NOT_EXHAUSTED"


def test_extra_local_compares_against_full_platform_face():
    """回归：extra_local 曾按 category 子集比较，把本区其它 category 全误报成「本地多出」。"""
    rep = cca.build_report(ITEMS, "OTHER", set(), local=["model238", "pv13", "ghost_ds"])
    assert rep["extra_local"] == ["ghost_ds"]


# ---------------- 分子来源 ----------------

def test_load_tested_file_accepts_json_and_csv(tmp_path):
    j = tmp_path / "t.json"
    j.write_text(json.dumps({"datasets": ["other455", {"id": "other567"}]}), encoding="utf-8")
    assert cca.load_tested_file(j) == {"other455", "other567"}

    c = tmp_path / "t.txt"
    c.write_text("other455, other567\n# comment\nother699", encoding="utf-8")
    assert cca.load_tested_file(c) == {"other455", "other567", "other699"}


def test_snapshot_roundtrip_and_incomplete_rejected(tmp_path):
    p = tmp_path / "snap.json"
    cca.save_snapshot(_payload(ITEMS), p)
    assert len(cca.load_snapshot(p)["datasets"]) == len(ITEMS)

    bad = tmp_path / "bad.json"
    bad.write_text(json.dumps(_payload(ITEMS, complete=False)), encoding="utf-8")
    with pytest.raises(cca.SourceError):
        cca.load_snapshot(bad)


# ---------------- CLI 退出码 ----------------

def test_main_exit_0_when_exhausted(monkeypatch, capsys):
    rc = _run_main(monkeypatch,
                   BASE + ["--category", "OTHER", "--tested", "other455,other567,other699"],
                   _payload(ITEMS))
    assert rc == cca.EXIT_EXHAUSTED
    assert "EXHAUSTED" in capsys.readouterr().out


def test_main_exit_1_when_diff_nonempty(monkeypatch):
    rc = _run_main(monkeypatch, BASE + ["--category", "OTHER", "--tested", "other455"],
                   _payload(ITEMS))
    assert rc == cca.EXIT_NOT_EXHAUSTED


def test_main_fail_closed_when_pagination_incomplete(monkeypatch):
    """分母没拉全 ⇒ 只能是数据源错误，不能是「未穷尽」也不能是「穷尽」。"""
    rc = _run_main(monkeypatch, BASE + ["--category", "OTHER"],
                   _payload(ITEMS, complete=False))
    assert rc == cca.EXIT_ERROR


def test_main_fail_closed_when_platform_returns_nothing(monkeypatch):
    rc = _run_main(monkeypatch, BASE, _payload([]))
    assert rc == cca.EXIT_ERROR


def test_main_fail_closed_on_unknown_category(monkeypatch):
    rc = _run_main(monkeypatch, BASE + ["--category", "SOCIALMEDIA"], _payload(ITEMS))
    assert rc == cca.EXIT_ERROR


def test_main_snapshot_region_mismatch_is_error(tmp_path):
    p = tmp_path / "s.json"
    cca.save_snapshot(dict(_payload(ITEMS), region="USA"), p)
    assert cca.main(BASE + ["--snapshot", str(p)]) == cca.EXIT_ERROR
