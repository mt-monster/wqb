# -*- coding: utf-8 -*-
"""wqb.timeutil — 美东（ET）日历日口径的唯一实现（纯标准库，Windows 无需 tzdata）。

提交配额按 **ET 日历日**重置（00:00 ET；REGULAR 4 颗 / SUPER 1 颗 / PPA 1 颗，三者并行）。

2026-09-29 整改（skills 审查 T0-14 / SB-21 / IX-22）：此前 ``tools/quota_status.py`` 与 toolkit
``pipeline.py`` 各自把 ET 写死成 UTC-4（EDT）。美国夏令时 2026-11-01 结束后，00:00 ET 对应的
GMT+8 时刻从 12:00 变成 **13:00**，写死 UTC-4 的实现日界会漂移 1 小时，
「00:00 ET = 12:00 GMT+8」这句话也随之在冬令时失效。

实现：优先 ``zoneinfo.ZoneInfo("America/New_York")``；缺 tz 数据库（Windows 未装 tzdata）时回退到
本模块的美国夏令时规则（2007 年起：3 月第二个周日 02:00 → 11 月第一个周日 02:00，本地时间）。
两条路径的等价性由 tests/unit/test_timeutil.py 逐小时比对（2024–2030）。
"""
from __future__ import annotations

import datetime as _dt
from typing import Optional, Tuple

_UTC = _dt.timezone.utc
_EST = _dt.timezone(_dt.timedelta(hours=-5), "EST")
_EDT = _dt.timezone(_dt.timedelta(hours=-4), "EDT")

try:  # pragma: no cover - 取决于环境是否有 tz 数据库
    from zoneinfo import ZoneInfo as _ZoneInfo
    _NY = _ZoneInfo("America/New_York")
except Exception:  # ZoneInfoNotFoundError / ImportError
    _NY = None


def _nth_sunday(year: int, month: int, n: int) -> _dt.date:
    """month 月第 n 个周日（n>=1）。"""
    first = _dt.date(year, month, 1)
    offset = (6 - first.weekday()) % 7          # 距第一个周日的天数（周一=0 … 周日=6）
    return first + _dt.timedelta(days=offset + 7 * (n - 1))


def _dst_bounds_utc(year: int) -> Tuple[_dt.datetime, _dt.datetime]:
    """夏令时区间 [start, end)（UTC）：3 月第二个周日 02:00 EST(=07:00Z) → 11 月第一个周日 02:00 EDT(=06:00Z)。"""
    start = _dt.datetime.combine(_nth_sunday(year, 3, 2), _dt.time(7, 0), tzinfo=_UTC)
    end = _dt.datetime.combine(_nth_sunday(year, 11, 1), _dt.time(6, 0), tzinfo=_UTC)
    return start, end


def _rule_offset_utc(now_utc: _dt.datetime) -> _dt.tzinfo:
    """给定 UTC 时刻，返回该时刻的 ET 固定偏移（EDT/EST）。"""
    start, end = _dst_bounds_utc(now_utc.year)
    return _EDT if start <= now_utc < end else _EST


def to_et(dt: _dt.datetime) -> _dt.datetime:
    """tz-aware datetime → ET（含夏令时）。naive 视为 UTC。"""
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=_UTC)
    if _NY is not None:
        return dt.astimezone(_NY)
    utc = dt.astimezone(_UTC)
    return utc.astimezone(_rule_offset_utc(utc))


def et_now(now_utc: Optional[_dt.datetime] = None) -> _dt.datetime:
    return to_et(now_utc or _dt.datetime.now(_UTC))


def et_date(dt: _dt.datetime) -> str:
    """该时刻所在的 ET 日历日（YYYY-MM-DD）。"""
    return to_et(dt).strftime("%Y-%m-%d")


def et_today(now_utc: Optional[_dt.datetime] = None) -> str:
    return et_now(now_utc).strftime("%Y-%m-%d")


def et_day_bounds_utc(now_utc: Optional[_dt.datetime] = None) -> Tuple[_dt.datetime, _dt.datetime]:
    """当前 ET 日历日的 [start_utc, next_start_utc)。DST 切换日长度 23h / 25h，不是固定 24h。"""
    local = et_now(now_utc)
    d = local.date()
    return _et_midnight_utc(d), _et_midnight_utc(d + _dt.timedelta(days=1))


def _et_midnight_utc(d: _dt.date) -> _dt.datetime:
    """ET 本地 d 日 00:00 对应的 UTC 时刻（切换发生在 02:00，午夜无歧义）。"""
    if _NY is not None:
        return _dt.datetime.combine(d, _dt.time(0, 0), tzinfo=_NY).astimezone(_UTC)
    # 规则回退：午夜偏移 = -4（EDT）当且仅当 第二个周日(3月) < d <= 第一个周日(11月)
    dst = _nth_sunday(d.year, 3, 2) < d <= _nth_sunday(d.year, 11, 1)
    off = _dt.timedelta(hours=4 if dst else 5)
    return _dt.datetime.combine(d, _dt.time(0, 0), tzinfo=_UTC) + off


def et_reset_hour_gmt8(now_utc: Optional[_dt.datetime] = None) -> int:
    """当前生效的「00:00 ET 在 GMT+8 是几点」：夏令时 12，冬令时 13。文档只写公式，不写死 12:00。"""
    start_utc, _ = et_day_bounds_utc(now_utc)
    return (start_utc.astimezone(_dt.timezone(_dt.timedelta(hours=8)))).hour
