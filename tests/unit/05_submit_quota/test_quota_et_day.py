# -*- coding: utf-8 -*-
"""提交配额的 ET 日历日口径：tools/quota_status.py 与 toolkit pipeline.py 同一实现（wqb.timeutil + OS 池）。

回归（skills 审查 T0-14 / P0-3）：
  * pipeline.py 曾优先读 `activities/submissions`——该端点是快照 {yesterday,current,previous,ytd}，无 `results`，
    解析成空列表 → 被当作「今日 0 提交」，配额永远显示满额；
  * 两处都写死 ET=UTC-4，2026-11-01 起日界漂移 1 小时。
"""
import datetime as dt
import importlib.util
import io
import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[3]
TK_SCRIPTS = ROOT / "Claude" / "skills" / "wq-brain-campaign-toolkit" / "scripts"
UTC = dt.timezone.utc


def _u(*a):
    return dt.datetime(*a, tzinfo=UTC)


@pytest.fixture(scope="module")
def pipeline():
    for p in (str(ROOT / "src"), str(TK_SCRIPTS)):
        if p not in sys.path:
            sys.path.insert(0, p)
    spec = importlib.util.spec_from_file_location("_pipeline_quota_test", TK_SCRIPTS / "pipeline.py")
    mod = importlib.util.module_from_spec(spec)
    sys.modules["_pipeline_quota_test"] = mod
    spec.loader.exec_module(mod)
    return mod


class _Api:
    """只回 OS 池；任何对 activities 端点的请求都视为回归。"""

    def __init__(self, results):
        self.results, self.paths = results, []

    def get(self, path):
        self.paths.append(path)
        assert "activities/submissions" not in path, "不得再读 activities/submissions（快照端点，无 today）"
        return io.StringIO(json.dumps({"results": self.results}))


def _row(ts):
    return {"id": "A" + ts[-6:], "dateSubmitted": ts, "settings": {"region": "USA"}}


def test_counts_only_the_current_et_day(pipeline):
    now = _u(2026, 9, 29, 15, 0)                      # ET 2026-09-29 11:00
    rows = [_row("2026-09-29T05:00:00-04:00"),        # 今日（ET）
            _row("2026-09-29T13:00:00Z"),             # 今日
            _row("2026-09-28T23:59:00-04:00"),        # 昨日 23:59 ET
            _row("2026-09-27T12:00:00Z")]
    api = _Api(rows)
    q = pipeline.submission_quota(api, 4, now=now)
    assert (q["used"], q["remaining"], q["et_day"], q["source"]) == (2, 2, "2026-09-29", "os_alphas")
    assert api.paths == ["/users/self/alphas?stage=OS&limit=100&order=-dateSubmitted"]


def test_day_boundary_is_dst_aware(pipeline):
    """2026-11-02 04:30Z：EST 下是 11-01 23:30 → 仍属 11-01；写死 UTC-4 会误算成 11-02。"""
    rows = [_row("2026-11-01T22:00:00-05:00")]        # = 11-02 03:00Z，ET 日 11-01
    q = pipeline.submission_quota(_Api(rows), 4, now=_u(2026, 11, 2, 4, 30))
    assert q["et_day"] == "2026-11-01" and q["used"] == 1
    q2 = pipeline.submission_quota(_Api(rows), 4, now=_u(2026, 11, 2, 5, 0))   # 00:00 EST：新的一天
    assert q2["et_day"] == "2026-11-02" and q2["used"] == 0
    assert "13:00 GMT+8" in q2["_note"]


def test_full_quota_reports_zero_remaining(pipeline):
    rows = [_row(f"2026-09-29T0{i}:00:00-04:00") for i in range(1, 5)]
    q = pipeline.submission_quota(_Api(rows), 4, now=_u(2026, 9, 29, 20, 0))
    assert (q["used"], q["remaining"]) == (4, 0)


def test_pipeline_source_has_no_activities_reader_or_fixed_offset(pipeline):
    text = (TK_SCRIPTS / "pipeline.py").read_text(encoding="utf-8")
    code = "\n".join(ln for ln in text.splitlines() if not ln.strip().startswith("#"))
    assert "_submitted_ts_from_activities" not in code
    assert "timedelta(hours=4)" not in code and "hours=4)" not in code


def test_quota_status_tool_uses_timeutil_and_counts_et_today():
    spec = importlib.util.spec_from_file_location("_quota_status_tool", ROOT / "tools" / "quota_status.py")
    mod = importlib.util.module_from_spec(spec)
    if str(ROOT / "src") not in sys.path:
        sys.path.insert(0, str(ROOT / "src"))
    spec.loader.exec_module(mod)                       # 已加 __main__ 守卫：导入不再执行
    res = [_row("2026-11-01T22:00:00-05:00"), _row("2026-11-02T06:00:00Z"), {"id": "x"}, {"dateSubmitted": "bad"}]
    got = mod.todays_submissions(res, _u(2026, 11, 2, 4, 30))
    assert len(got) == 1 and got[0][2] == "2026-11-01T22:00:00-05:00"      # 仅第 1 条（ET 11-01 22:00）
    text = (ROOT / "tools" / "quota_status.py").read_text(encoding="utf-8")
    assert "timezone(timedelta(hours=-4))" not in text
