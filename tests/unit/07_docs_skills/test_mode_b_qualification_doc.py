# -*- coding: utf-8 -*-
"""Mode B 资格判定表（skills 审查 OP-18 / HP-15 / OP-11 / OP-13）的守护。

  1. 文档判定表的数值与动作文案 = `mode_b_config._DEFAULT_GLOBAL`（单一真相源，改了代码不改文档会失败）；
  2. `load_mode_b_config` 的覆盖优先级 = 文档 §3（区域 ledger > 区域 thresholds > GLOBAL ledger > 内置默认）；
  3. 任何 skill 文档不得再写「未达资格线 / 未达标 → 一律判死」（旧双标量闸，会误杀旁路 A–E）。
"""
import re
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[3]
SK = ROOT / "Claude" / "skills"
DOC = SK / "wq-brain-alpha-optimization-v1" / "references" / "mode-b-qualification.md"
sys.path.insert(0, str(ROOT / "src"))

from wqb.workflow import mode_b_config as M  # noqa: E402


def _doc() -> str:
    return DOC.read_text(encoding="utf-8")


def _row(text: str, marker: str) -> str:
    rows = [ln for ln in text.splitlines() if ln.startswith("|") and marker in ln]
    assert rows, f"判定表里找不到 {marker} 行"
    return rows[0]


def test_main_gate_numbers_match_code():
    row = _row(_doc(), "`main_gate`")
    g = M._DEFAULT_GLOBAL["main_gate"]
    assert str(g["sharpe_min"]) in row and str(g["fitness_min"]) in row


@pytest.mark.parametrize("name", sorted(M._DEFAULT_GLOBAL["bypass_rules"]))
def test_bypass_rows_match_code(name):
    rule = M._DEFAULT_GLOBAL["bypass_rules"][name]
    row = _row(_doc(), f"`{name}`")
    for k, v in rule.items():
        if isinstance(v, (int, float)) and k != "mode_b_action":
            assert str(v) in row, f"{name}.{k}={v} 未出现在文档判定表的该行"
    assert rule["mode_b_action"] in row, f"{name} 的 mode_b_action 文案与代码不一致"


def test_hard_kill_line_matches_code():
    row = _row(_doc(), "`dead_end`")
    assert str(M._DEFAULT_GLOBAL["hard_kill"]["two_year_sharpe_max"]) in row
    assert "2Y ≥ 1.2 永不判死" in row


def test_doc_declares_the_judge_node_blind_spot():
    """judge 节点不喂 robust_sharpe / prod_corr / returns_median → A/B/D 在该入口恒不命中；文档必须如实写。"""
    text = _doc()
    assert "A / B / D 在该入口恒不命中" in text
    src = (ROOT / "src" / "wqb" / "workflow" / "nodes" / "judge.py").read_text(encoding="utf-8")
    call = src.split("verdict = _evaluate_mode_b(", 1)[1].split(")", 1)[0]
    for fed in ("sharpe", "fitness", "two_year_sharpe", "margin", "turnover", "returns"):
        assert fed in call
    for not_fed in ("robust_sharpe", "prod_corr", "returns_median", "other_dims_all_pass"):
        assert not_fed not in call, f"judge 节点现在喂了 {not_fed}：请更新文档 §4 的覆盖范围表"


class _Store:
    def __init__(self, data):
        self._d = data

    def get_ledger(self, region, key):
        return self._d.get((region, key))


def _cfg(monkeypatch, *, glob=None, region_file=None, region_ledger=None):
    monkeypatch.setattr(M, "_read_thresholds_file", lambda region: region_file)
    data = {}
    if glob is not None:
        data[("GLOBAL", "mode_b_qualification")] = glob
    if region_ledger is not None:
        data[("ZZZ", "mode_b_qualification")] = region_ledger
    return M.load_mode_b_config(_Store(data), region="ZZZ")


def test_precedence_matches_doc_section_3(monkeypatch):
    glob = {"main_gate": {"sharpe_min": 1.3, "fitness_min": 0.9}}
    file_ = {"$ref": "GLOBAL/mode_b_qualification", "_overrides": {"sharpe_min": 1.4}}
    reg = {"sharpe_min": 1.5}

    assert _cfg(monkeypatch)["main_gate"] == {"sharpe_min": 1.25, "fitness_min": 0.8}                      # 4 内置
    assert _cfg(monkeypatch, glob=glob)["main_gate"] == {"sharpe_min": 1.3, "fitness_min": 0.9}            # 3 GLOBAL
    got = _cfg(monkeypatch, glob=glob, region_file=file_)["main_gate"]
    assert got == {"sharpe_min": 1.4, "fitness_min": 0.9}                                                  # 2 区域文件 > GLOBAL（单字段）
    got = _cfg(monkeypatch, glob=glob, region_file=file_, region_ledger=reg)
    assert got["main_gate"] == {"sharpe_min": 1.5, "fitness_min": 0.9} and got["_source"] == "region_ledger:ZZZ"   # 1 区域 ledger


def test_legacy_thresholds_without_ref_are_read_as_main_gate_overrides(monkeypatch):
    got = _cfg(monkeypatch, region_file={"sharpe_min": 1.5, "fitness_min": 1.0})["main_gate"]
    assert got == {"sharpe_min": 1.5, "fitness_min": 1.0}


def test_overrides_below_the_global_floor_are_clamped_not_applied(monkeypatch):
    """2026-10-04 下限锁：区域文件、区域台账（自适应学习）写得比 GLOBAL 主闸低，读时钳回下限，原值留在 `_clamped_from`。"""
    cfg = _cfg(monkeypatch, region_file={"sharpe_min": 1.0, "fitness_min": 0.6})
    assert cfg["main_gate"] == {"sharpe_min": 1.25, "fitness_min": 0.8}
    assert cfg["_clamped_from"] == {"sharpe_min": 1.0, "fitness_min": 0.6}
    glob = {"main_gate": {"sharpe_min": 1.3, "fitness_min": 0.9}}
    cfg = _cfg(monkeypatch, glob=glob, region_ledger={"sharpe_min": 1.15, "fitness_min": 0.68})
    assert cfg["main_gate"] == {"sharpe_min": 1.3, "fitness_min": 0.9} and cfg["_floor"] == glob["main_gate"]
    assert cfg["_clamped_from"] == {"sharpe_min": 1.15, "fitness_min": 0.68}


def test_no_real_region_thresholds_file_sets_the_main_gate_below_the_floor():
    """仓库里 13 个战役目录的 thresholds.json 都不得把主闸写到内置下限以下（新写放宽值即红）。"""
    import json
    floor = M._DEFAULT_GLOBAL["main_gate"]
    bad = []
    for p in sorted((ROOT / "tracking").glob("*/config/thresholds.json")):
        mbq = json.loads(p.read_text(encoding="utf-8-sig")).get("mode_b_qualification") or {}
        vals = dict(mbq.get("_overrides") or {})
        if "$ref" not in mbq:
            vals.update({k: mbq[k] for k in ("sharpe_min", "fitness_min") if mbq.get(k) is not None})
        for k in ("sharpe_min", "fitness_min"):
            if vals.get(k) is not None and float(vals[k]) < float(floor[k]):
                bad.append(f"{p.parent.parent.name}: {k}={vals[k]} < {floor[k]}")
    assert not bad, "区域只能收紧 Mode B 主闸：\n" + "\n".join(bad)


def test_regions_can_only_override_the_main_gate_not_bypass_or_kill_line(monkeypatch):
    glob = {"main_gate": {"sharpe_min": 1.3, "fitness_min": 0.9},
            "bypass_rules": {"E_2y_strong": {"two_year_sharpe_min": 1.4, "sharpe_min": 0.9}},
            "hard_kill": {"two_year_sharpe_max": 1.1}}
    cfg = _cfg(monkeypatch, glob=glob, region_ledger={"sharpe_min": 1.0, "bypass_rules": {"x": 1}, "hard_kill": {"y": 2}})
    assert cfg["bypass_rules"] == glob["bypass_rules"] and cfg["hard_kill"] == glob["hard_kill"]


_STALE = re.compile(r"(未达资格线|未达标|未达线)[^。\n]{0,40}判死|资格线[^。\n]{0,30}一律判死")
_OK_CONTEXT = re.compile(r"bypass|旁路|mode-b-qualification|作废")


def test_no_skill_doc_says_below_qualification_means_dead():
    bad = []
    for p in sorted(SK.rglob("*.md")):
        if p == DOC:
            continue
        lines = p.read_text(encoding="utf-8").splitlines()
        for i, ln in enumerate(lines):
            if _STALE.search(ln):
                ctx = "\n".join(lines[max(0, i - 3): i + 4])
                if not _OK_CONTEXT.search(ctx):
                    bad.append(f"{p.relative_to(ROOT)}:{i + 1}: {ln.strip()[:90]}")
    assert not bad, "「未达资格线/未达标 → 判死」是旧双标量闸（会误杀旁路 A–E），改为引用 mode-b-qualification.md：\n" + "\n".join(bad)
