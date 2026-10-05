# -*- coding: utf-8 -*-
"""wqb.quota — 提交配额的唯一实现口径（ET 日历日；REGULAR 与 SUPER 是两条独立线）。

**取数口径**：列 ``stage=OS`` 按 ``dateSubmitted`` 倒序，数**当前 ET 日历日**的条目。
不得读 ``activities/submissions`` —— 该端点只有 ``{yesterday, current, previous, ytd}``
快照、**没有 today**，且 ``ytd.end`` 停在昨天 ⇒ 极易误判「今日 0 提交、配额全空」
（2026-09-21 事故：当日被并行会话用掉 2 个后仍显示「昨日 5」，第 3 颗撞
``REGULAR_SUBMISSION(4/4)`` 配额墙）。

★ 2026-10-05 类型化修正：此前各处把「今日提交**总数**」当 REGULAR 用量。平台对
REGULAR（4/ET 日）与 SUPER（1/ET 日）是**两条独立**配额线，混合计数会**高估** REGULAR
用量 ⇒ 在 REGULAR 仍有余额时误拦合法提交（实测当日 4 颗里 1 颗为 SUPER，报 4/4 实为 3/4）。

**判型**：首选平台记录自带的 ``type`` 字段；判不了的**按保守口径计入 REGULAR** 并单列
``unclassified_used`` —— 多算只是少提交一颗（可等 403 兜底），漏算才会把配额判松。
若 ``unclassified_used`` 持续非 0，说明上游返回的记录缺 ``type`` 字段，需复核取数路径。

ET 日界复用 `wqb.timeutil`（America/New_York，含夏令时；冬令时 00:00 ET = 13:00 GMT+8）。

消费点（不得各自另算一套）：
  * ``tools/quota_status.py`` —— 命令行实况；
  * ``src/wqb/workflow/nodes/submit_alpha.py`` 的 ``_quota_gate`` —— 提交路由前置闸（fail-open）。
"""
from __future__ import annotations

import datetime as _dt
from typing import Any, Dict, List, Optional

from .timeutil import et_date, et_today

#: REGULAR 每日提交配额上限（ET 日历日）。
REGULAR_DAILY_LIMIT = 4
#: SUPER 每日提交配额上限（ET 日历日）；与 REGULAR 互不占用。
SUPER_DAILY_LIMIT = 1

#: `entries[].kind` 取值；判不了型时用这个字面量（消费方按字符串宽度打印，不能是 None）。
KIND_REGULAR = "REGULAR"
KIND_SUPER = "SUPER"
KIND_UNCLASSIFIED = "UNCLASSIFIED"


def alpha_kind(record: Any) -> Optional[str]:
    """一条提交记录的信号类型：``REGULAR`` / ``SUPER``；缺 ``type`` 或无法识别 → ``None``。

    只认平台自带的 ``type`` 字段，不做名字/ID 猜测 —— 猜错会把 SUPER 当 REGULAR 计数，
    正是本次修正要消除的那类误差。判不了由 ``probe_today`` 保守归入 REGULAR。
    """
    if not isinstance(record, dict):
        return None
    t = record.get("type")
    if not isinstance(t, str):
        return None
    up = t.strip().upper()
    if up == KIND_REGULAR:
        return KIND_REGULAR
    if up == KIND_SUPER:
        return KIND_SUPER
    return None


def parse_submitted_ts(raw: Any) -> Optional[_dt.datetime]:
    """``dateSubmitted``（ISO8601，可能以 ``Z`` 结尾）→ aware datetime；不可解析 → None。"""
    if not isinstance(raw, str) or not raw:
        return None
    try:
        return _dt.datetime.fromisoformat(raw.replace("Z", "+00:00"))
    except ValueError:
        return None


def probe_today(results: Any, now_utc: Optional[_dt.datetime] = None) -> Dict[str, Any]:
    """按 ET 日历日统计当日提交用量，并按类型分线。

    Args:
        results: ``GET /users/self/alphas?stage=OS&order=-dateSubmitted`` 的 ``results`` 列表。
        now_utc: 注入「现在」以做纯函数测试；缺省取真实当前 UTC。

    Returns:
        ``{et_day, entries, regular_explicit, super_used, unclassified_used,
        regular_used, regular_limit, regular_remaining,
        super_limit, super_remaining, total_today}``
        —— ``regular_used = regular_explicit + unclassified_used``（保守口径）。
    """
    today = et_today(now_utc)
    entries: List[Dict[str, Any]] = []
    for x in results or []:
        if not isinstance(x, dict):
            continue
        ds = x.get("dateSubmitted") or ""
        d = parse_submitted_ts(ds)
        if d is None or et_date(d) != today:
            continue
        kind = alpha_kind(x)
        entries.append({
            "alpha_id": x.get("id"),
            "region": (x.get("settings") or {}).get("region"),
            "dateSubmitted": ds,
            "kind": kind or KIND_UNCLASSIFIED,
        })

    regular_explicit = sum(1 for e in entries if e["kind"] == KIND_REGULAR)
    super_used = sum(1 for e in entries if e["kind"] == KIND_SUPER)
    unclassified_used = sum(1 for e in entries if e["kind"] == KIND_UNCLASSIFIED)
    regular_used = regular_explicit + unclassified_used

    return {
        "et_day": today,
        "entries": entries,
        "total_today": len(entries),
        "regular_explicit": regular_explicit,
        "super_used": super_used,
        "unclassified_used": unclassified_used,
        "regular_used": regular_used,
        "regular_limit": REGULAR_DAILY_LIMIT,
        "regular_remaining": max(0, REGULAR_DAILY_LIMIT - regular_used),
        "super_limit": SUPER_DAILY_LIMIT,
        "super_remaining": max(0, SUPER_DAILY_LIMIT - super_used),
    }
