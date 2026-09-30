# -*- coding: utf-8 -*-
"""PPA 人工通道的交接单与回写（skills 审查 SB-22）：离线纯函数测试。"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "src"))

import ppa_handoff as H  # noqa: E402

DETAIL = {
    "id": "AbCd1234", "status": "UNSUBMITTED",
    "settings": {"region": "DEU", "universe": "TOP2500", "delay": 1},
    "regular": {"code": "group_neutralize(rank(ts_zscore(ts_backfill(est_eps, 66), 252)), industry)"},
    "is": {"sharpe": 1.12, "fitness": 0.8, "turnover": 0.12, "checks": [
        {"name": "LOW_SHARPE", "result": "PASS", "value": 1.12},
        {"name": "HIGH_TURNOVER", "result": "PASS"},
        {"name": "LOW_SUB_UNIVERSE_SHARPE", "result": "PENDING"},
    ]},
}


def test_counts_operators_and_fields():
    total, distinct = H.count_operators("rank(rank(ts_mean(a, 5)))")
    assert (total, distinct) == (3, 2)
    assert H.count_fields("rank(ts_mean(est_eps, 5))") == 1


def test_sheet_marks_what_is_automatic_and_what_needs_a_human():
    md = H.build_sheet(DETAIL)
    assert "PPA 人工提交交接单：AbCd1234" in md and "DEU / TOP2500 / D1" in md
    assert "Failed PPA = 0 ✔" in md and "LOW_SUB_UNIVERSE_SHARPE" in md      # PENDING 被点名
    assert "PPAC" in md and "**待填**" in md and "主题窗口" in md
    assert "agent 到这里**停下并交接**" in md and "不重复催" in md
    assert "PPAC < 0.5：0.41  ✔" in H.build_sheet(DETAIL, ppac=0.41)
    assert "0.62  ✘" in H.build_sheet(DETAIL, ppac=0.62)


def test_sheet_flags_a_failed_ppa_gate():
    bad = {**DETAIL, "is": {**DETAIL["is"], "checks": [{"name": "HIGH_TURNOVER", "result": "FAIL"}]}}
    assert "Failed PPA = 1 ✘（HIGH_TURNOVER）" in H.build_sheet(bad)


class _Store:
    def __init__(self):
        self.calls = []

    def upsert_submission(self, alpha_id, **kw):
        self.calls.append((alpha_id, kw))
        return {"action": "inserted", "alpha_id": alpha_id}


def test_record_refuses_until_platform_confirms_submission():
    s = _Store()
    ok, msg = H.record_submission(s, dict(DETAIL, status="UNSUBMITTED"))
    assert not ok and "还没有提交成功" in msg and s.calls == []
    ok, _ = H.record_submission(s, dict(DETAIL, status="ACTIVE"))            # 缺 dateSubmitted 也不写
    assert not ok and s.calls == []


def test_record_writes_ppa_submission_once_confirmed():
    s = _Store()
    ok, msg = H.record_submission(s, dict(DETAIL, status="ACTIVE", dateSubmitted="2026-09-29T10:00:00-04:00"))
    assert ok and "已回写" in msg
    aid, kw = s.calls[0]
    assert aid == "AbCd1234" and kw["submission_type"] == "PPA" and kw["region"] == "DEU"
    assert kw["submitted_at"] == "2026-09-29T10:00:00-04:00" and kw["verdict"]["channel"] == "web_ui"
