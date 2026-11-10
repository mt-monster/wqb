# -*- coding: utf-8 -*-
r"""CPPAP 就绪度判据守护测试（2026-11-10）。

锁死四条经平台实证的判据，防止回退到「66 颗带标签池＝CPPAP 成分」的错误前提：
1. ``themes`` 是当期资格前置闸，无当期主题 ⇒ ``NO_LEVERAGE``；
2. 当期池 <5 条评奖线时，即使 WEAK 也不摘（``HOLD_LOW_COUNT``）；
3. ``EDGE``（低 margin 但低换手）永不摘（论坛实测 BC 反掉 .053）；
4. margin 只作**软标记**，绝不作为提交硬闸（MEMORY §8）。

另验证治理台账最终态会校正过期快照的 tags。
"""
from __future__ import annotations

import json
import sys
from pathlib import Path
from types import SimpleNamespace

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools" / "gates"))

import ppa_readiness as R  # noqa: E402
import ppa_tag_apply as A  # noqa: E402

THEME = "GLB/D1 Power Pool Nov`26"


def row(aid="X", themes=None, tags=None, margin=20.0, to=0.05):
    tags = tags if tags is not None else ["CH_REG", "PowerPoolSelected"]
    return dict(id=aid, region="GLB", themes=themes if themes is not None else [THEME],
                tags=tags, ppa=("PowerPoolSelected" in tags),
                margin_bp=margin, turnover=to, sharpe=2.0, fitness=1.5)


# ---------------------------------------------------------------- 1 当期主题识别

def test_detect_current_theme_picks_latest_month():
    rows = [row(themes=["OTHER/D1 Power Pool Sept`26"]),
            row(themes=["D1 Power Pool Oct`26"]),
            row(themes=[THEME])]
    assert R.detect_current_theme(rows) == THEME
    assert R.month_rank(THEME) > R.month_rank("OTHER/D1 Power Pool Sept`26")


def test_no_current_theme_is_no_leverage():
    x = R.classify(row(themes=[], margin=92.46, to=0.036), THEME, 1)
    assert x["action"] == "NO_LEVERAGE"
    assert x["quality_band"] == "ANCHOR"
    assert "themes" in x["reason"]


# ---------------------------------------------------------------- 2 低条数保护

def test_sole_current_entry_is_held_not_removed():
    """上一轮的真实教训：JjeMlmXA 是当期唯一参赛货，摘了清零池子。"""
    x = R.classify(row(aid="JjeMlmXA", margin=2.66, to=0.3193), THEME, 1)
    assert x["quality_band"] == "WEAK"
    assert x["action"] == "HOLD_LOW_COUNT"
    assert "清零参赛资格" in x["reason"]


def test_remove_only_when_pool_reaches_prize_line():
    x = R.classify(row(margin=2.66, to=0.3193), THEME, 5)
    assert x["action"] == "CONSIDER_REMOVE"


# ---------------------------------------------------------------- 3 EDGE 永不摘

def test_edge_is_kept_and_never_selected_for_removal():
    x = R.classify(row(margin=8.0, to=0.10), THEME, 5)
    assert x["quality_band"] == "EDGE"
    assert x["action"] == "KEEP_TAG"
    got = A.select([x], SimpleNamespace(add=False, allow_no_leverage=False,
                                        force_low_count=False, limit=10))
    assert got == []


def test_default_apply_selects_nothing_on_real_plan():
    plan = json.loads((ROOT / "results" / "ppa_readiness_20261110.json").read_text(encoding="utf-8"))
    got = A.select(plan["items"], SimpleNamespace(add=False, allow_no_leverage=False,
                                                  force_low_count=False, limit=10))
    assert got == []
    assert plan["current_theme_entries"] < R.MIN_ENTRIES_FOR_PRIZE


# ---------------------------------------------------------------- 4 margin 仅软标记

def test_margin_is_soft_flag_not_hard_gate():
    f = R.candidate_soft_flag(8.0)
    assert f["meets_floor"] is False and f["meets_target"] is False
    assert "不得作为提交硬闸" in f["note"]
    assert R.candidate_soft_flag(15.0)["meets_target"] is True


# ---------------------------------------------------------------- 5 台账校正

def test_ledger_final_state_corrects_stale_snapshot(monkeypatch, tmp_path):
    led = tmp_path / "log.jsonl"
    led.write_text("\n".join([
        json.dumps({"seq": 1, "action": "remove_power_pool_selected",
                    "alpha_id": "JjeMlmXA", "after_tags": []}),
        json.dumps({"seq": 3, "action": "rollback",
                    "alpha_id": "JjeMlmXA", "restored_tags": ["PowerPoolSelected"]}),
    ]), encoding="utf-8")
    monkeypatch.setattr(R, "LEDGER", led)
    rows, applied = R.apply_ledger_corrections([row(aid="JjeMlmXA", tags=[])])
    assert applied == ["JjeMlmXA"]
    assert rows[0]["tags"] == ["PowerPoolSelected"]
    assert rows[0]["ppa"] is True
