# -*- coding: utf-8 -*-
"""skills 审查处置台账（docs/skills_review_closure.json）守护：评审条目 → 处置 → 关闭证据（报告 Part C 的教训）。

上一轮评审 9 个 P0 完全关闭 0 个，直接原因是没有登记也没有机检。本测试保证：报告里每个条目 ID 都有处置；
状态合法；fixed 必须指向真实存在的文件；needs-platform 必须写清怎么复核。
收尾时把 STRICT 置 True：要求没有任何 open。
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))

import closure_ledger as CL  # noqa: E402

#: 全部处置完毕后置 True（收尾提交里做）；此前允许 open 存在，但每个 ID 必须有条目
STRICT = True


def test_every_report_id_has_a_disposition_and_it_is_valid():
    errs = CL.check(strict=STRICT)
    assert not errs, "处置台账问题（python tools/closure_ledger.py check 可复现）：\n  " + "\n  ".join(errs[:40])


def test_report_id_extraction_is_complete():
    ids = CL.report_ids()
    assert len(ids) >= 700
    for must in ("T0-1", "T0-20", "X-1", "X-19", "SB-25", "RA-131", "P0-1", "IX-20"):
        assert must in ids, f"报告 ID 抽取漏了 {must}"


def test_range_expansion_and_render_smoke(tmp_path, monkeypatch):
    assert CL.expand(["SB-03..SB-05", "X-1"]) == ["SB-03", "SB-04", "SB-05", "X-1"]
    assert CL.expand(["RA-098..RA-100"]) == ["RA-098", "RA-099", "RA-100"]
    monkeypatch.setattr(CL, "OUT_MD", tmp_path / "closure.md")
    CL.cmd_render(None)
    txt = (tmp_path / "closure.md").read_text(encoding="utf-8")
    assert "| SB-01 |" in txt and "## T0" in txt


def test_a_fixed_item_whose_verify_pointer_went_stale_is_reported(monkeypatch):
    """关闭证据（verify）指向的测试被改名 / 删除后，「已修」就失去依据——必须变红（PW-09 就曾指向已改名的测试）。"""
    ghost = "test_" + "renamed_" + "away_" + "4242"           # 拼接：字面量不出现在本文件里，否则「文件里找得到名字」会误判通过
    items = {
        "ZZ-01": {"status": "fixed", "where": "AGENTS.md", "note": "x", "verify": f"tests/unit/test_closure_ledger.py::{ghost}"},
        "ZZ-02": {"status": "fixed", "where": "AGENTS.md", "note": "x", "verify": "tests/unit/no_such_file_" + "4242.py"},
        "ZZ-03": {"status": "fixed", "where": "AGENTS.md", "note": "x",
                  "verify": "tests/unit/test_closure_ledger.py::test_report_id_extraction_is_complete"},
        "ZZ-04": {"status": "needs-platform", "note": "x", "verify": "在平台上先调用 get_operators，看返回里有没有该算子"},
    }
    monkeypatch.setattr(CL, "load", lambda: {"items": items})
    monkeypatch.setattr(CL, "report_ids", lambda: {k: {} for k in items})
    errs = CL.check()
    assert any(e.startswith("ZZ-01") and ghost in e for e in errs), errs
    assert any(e.startswith("ZZ-02") and "不存在的文件" in e for e in errs), errs
    assert not any(e.startswith(("ZZ-03", "ZZ-04")) for e in errs), errs
