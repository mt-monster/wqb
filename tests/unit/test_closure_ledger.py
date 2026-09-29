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
STRICT = False


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
