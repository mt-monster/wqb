# -*- coding: utf-8 -*-
"""wqb.timeutil：ET 日历日口径（skills 审查 T0-14，2026-09-29）。

关键点：提交配额 00:00 ET 重置。美国夏令时 2026-11-01 结束后，00:00 ET 在 GMT+8 是 13:00 而不是 12:00；
此前两处实现把 ET 写死成 UTC-4，日界会漂移 1 小时。
"""
import datetime as dt
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT / "src") not in sys.path:
    sys.path.insert(0, str(ROOT / "src"))

from wqb import timeutil as T  # noqa: E402

UTC = dt.timezone.utc


def _u(*a):
    return dt.datetime(*a, tzinfo=UTC)


def test_dst_transition_dates_2026():
    start, end = T._dst_bounds_utc(2026)
    assert start == _u(2026, 3, 8, 7)       # 2026-03-08 02:00 EST
    assert end == _u(2026, 11, 1, 6)        # 2026-11-01 02:00 EDT（本仓库时间炸弹：2026-11-01）


@pytest.mark.parametrize("now,expect_day,expect_start,expect_hour", [
    # 夏令时：00:00 EDT = 04:00Z = 12:00 GMT+8
    (_u(2026, 9, 29, 15, 0), "2026-09-29", _u(2026, 9, 29, 4), 12),
    (_u(2026, 9, 29, 3, 59), "2026-09-28", _u(2026, 9, 28, 4), 12),      # 04:00Z 之前仍是前一个 ET 日
    (_u(2026, 9, 29, 4, 0), "2026-09-29", _u(2026, 9, 29, 4), 12),
    # 冬令时：00:00 EST = 05:00Z = 13:00 GMT+8
    (_u(2026, 11, 2, 4, 59), "2026-11-01", _u(2026, 11, 1, 4), 12),      # 11-01 当天 00:00 仍是 EDT；ET 日=11-01
    (_u(2026, 11, 2, 5, 0), "2026-11-02", _u(2026, 11, 2, 5), 13),
    (_u(2026, 12, 15, 4, 59), "2026-12-14", _u(2026, 12, 14, 5), 13),
])
def test_day_bounds_and_gmt8_reset_hour(now, expect_day, expect_start, expect_hour):
    assert T.et_today(now) == expect_day
    start, nxt = T.et_day_bounds_utc(now)
    assert start == expect_start and start <= now < nxt
    assert T.et_reset_hour_gmt8(now) == expect_hour


def test_dst_change_days_are_not_24_hours():
    s, n = T.et_day_bounds_utc(_u(2026, 11, 1, 12))          # 秋季回拨日：25h
    assert n - s == dt.timedelta(hours=25)
    s, n = T.et_day_bounds_utc(_u(2026, 3, 8, 12))           # 春季跳表日：23h
    assert n - s == dt.timedelta(hours=23)
    s, n = T.et_day_bounds_utc(_u(2026, 7, 4, 12))
    assert n - s == dt.timedelta(hours=24)


def test_fixed_utc_minus_4_would_be_wrong_after_november_first():
    """回归：旧实现（固定 UTC-4）在 2026-11-02 04:30Z 会把它算成 11-02（应为 11-01，EST 下 04:30Z = 23:30 前一日）。"""
    t = _u(2026, 11, 2, 4, 30)
    old = (t - dt.timedelta(hours=4)).strftime("%Y-%m-%d")
    assert old == "2026-11-02"
    assert T.et_date(t) == "2026-11-01"


def test_naive_datetime_is_treated_as_utc():
    assert T.et_date(dt.datetime(2026, 9, 29, 3, 0)) == "2026-09-28"


@pytest.mark.skipif(T._NY is None, reason="无 tz 数据库（Windows 未装 tzdata）：规则回退是唯一实现，无从比对")
def test_rule_fallback_equals_zoneinfo_hourly_2024_2030():
    """规则回退（Windows 无 tzdata 时的唯一实现）与 zoneinfo 逐小时一致。"""
    t = _u(2024, 1, 1)
    end = _u(2030, 12, 31)
    step = dt.timedelta(hours=1)
    real_ny = T._NY
    bad = []
    while t < end:
        via_zone = t.astimezone(real_ny)
        via_rule = t.astimezone(T._rule_offset_utc(t))
        if via_zone.utcoffset() != via_rule.utcoffset():
            bad.append(t)
            if len(bad) > 3:
                break
        t += step
    assert not bad, f"规则回退与 zoneinfo 不一致：{bad}"
    # 日界（午夜）也一致
    d = dt.date(2024, 1, 1)
    while d < dt.date(2031, 1, 1):
        zone_mid = dt.datetime.combine(d, dt.time(0), tzinfo=real_ny).astimezone(UTC)
        dst = T._nth_sunday(d.year, 3, 2) < d <= T._nth_sunday(d.year, 11, 1)
        rule_mid = dt.datetime.combine(d, dt.time(0), tzinfo=UTC) + dt.timedelta(hours=4 if dst else 5)
        assert zone_mid == rule_mid, d
        d += dt.timedelta(days=1)


def test_module_works_without_zoneinfo(monkeypatch):
    """模拟 Windows 无 tz 数据库：走规则回退，结果不变。"""
    monkeypatch.setattr(T, "_NY", None)
    assert T.et_today(_u(2026, 11, 2, 4, 59)) == "2026-11-01"
    assert T.et_reset_hour_gmt8(_u(2026, 12, 15, 12)) == 13
    assert T.et_reset_hour_gmt8(_u(2026, 9, 29, 12)) == 12
    s, n = T.et_day_bounds_utc(_u(2026, 11, 1, 12))
    assert n - s == dt.timedelta(hours=25)
