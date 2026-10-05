# -*- coding: utf-8 -*-
"""提交配额的类型化口径（REGULAR / SUPER 分流计数）—— **唯一实现**。

背景（2026-10-05 事故）：`tools/quota_status.py` 与
``src/wqb/workflow/nodes/submit_alpha.py::_quota_gate`` 都把 OS 池里
**当日提交总数**当成 REGULAR 用量。但平台对 REGULAR（4/ET 日）与
SUPER（1/ET 日）是**两条独立配额线** ⇒ 混合计数会**高估 REGULAR 用量**，
在 REGULAR 仍有余额时误报满额、拦下合法提交。

实测：2026-10-05 当日 4 颗提交中有 1 颗是 SUPER
（``d51nKZJE`` / ``IND_S_10comp_1nKZJE``），工具报 REGULAR ``4/4``，
**实际为 3/4（仍有 1 个余额）** —— 该误报导致一次合法提交被无谓推迟。

判型依据（按可靠性降序）：
  1. 记录自带 ``type`` 字段 —— 首选。``get_user_alphas(stage="OS")`` 实测返回
     ``'REGULAR'`` / ``'SUPER'``。
  2. ``settings`` 含 SUPER 专有键 ``selectionHandling`` / ``selectionLimit`` /
     ``componentActivation`` —— 次选。
  3. ``name`` 命名含 ``_S_``（SUPER）/ ``_R_``（REGULAR）—— 兜底。

⚠ **不可用 ``pyramids`` 判型**：该字段在 ``get_alpha_details`` 里对 SUPER 缺失，
但在 ``get_user_alphas`` 列表端点里 SUPER 也有值 ⇒ **端点相关，禁外推**。
"""
from __future__ import annotations

import datetime as _dt
from typing import Any, Dict, Iterable, List, Optional

# ET 日配额上限（平台口径；REGULAR 与 SUPER 相互独立）
REGULAR_DAILY_LIMIT = 4
SUPER_DAILY_LIMIT = 1

# SUPER 专有 settings 键（任一出现即判 SUPER）
_SUPER_SETTINGS_KEYS = ("selectionHandling", "selectionLimit", "componentActivation")

KIND_REGULAR = "REGULAR"
KIND_SUPER = "SUPER"
KIND_UNKNOWN = "UNKNOWN"


def alpha_kind(record: Dict[str, Any]) -> str:
    """判定一条 alpha 记录属于哪条配额线。

    返回 ``'REGULAR'`` / ``'SUPER'`` / ``'UNKNOWN'``。
    纯函数，不抛异常（记录残缺时退化为 UNKNOWN，由调用方按保守口径处理）。
    """
    if not isinstance(record, dict):
        return KIND_UNKNOWN

    # 1) 首选：记录自带 type
    t = str(record.get("type") or "").strip().upper()
    if t in (KIND_REGULAR, KIND_SUPER):
        return t

    # 2) 次选：SUPER 专有 settings 键
    settings = record.get("settings")
    if isinstance(settings, dict):
        if any(k in settings for k in _SUPER_SETTINGS_KEYS):
            return KIND_SUPER

    # 3) 兜底：命名约定 <REGION>_<R|S>_<family>_<seq>
    name = str(record.get("name") or "")
    if "_S_" in name:
        return KIND_SUPER
    if "_R_" in name:
        return KIND_REGULAR

    return KIND_UNKNOWN


def parse_submitted_at(raw: Any) -> Optional[_dt.datetime]:
    """解析 ``dateSubmitted``。失败（缺失 / 非法）返回 ``None``。"""
    if not raw:
        return None
    try:
        return _dt.datetime.fromisoformat(str(raw).replace("Z", "+00:00"))
    except ValueError:
        return None


def probe_today(results: Optional[Iterable[Dict[str, Any]]], now_utc: Optional[_dt.datetime] = None) -> Dict[str, Any]:
    """统计 ``results`` 中 ``dateSubmitted`` 落在**当前 ET 日历日**的条目，并按类型分流。

    纯函数（ET 日界经 ``wqb.timeutil``，含夏令时）。返回::

        {
          "et_day": "2026-10-05",
          "regular_used": 3, "regular_limit": 4, "regular_remaining": 1,
          "regular_explicit": 3, "unclassified_used": 0,
          "super_used": 1,   "super_limit": 1,   "super_remaining": 0,
          "entries": [{"region","alpha_id","dateSubmitted","kind"}, ...],
        }

    **记账口径（保守）**：``regular_used`` = 显式 REGULAR + **未判型**。
    判不出类型的条目仍占 REGULAR 预算 —— 宁可少放行，也不虚假释放额度；
    反之（未知不计入）会让闸放行，虽有平台 403 兜底（零成本）但白跑一次 POST。
    真实 OS 端点每条都带 ``type``，故 ``unclassified_used`` 在实践中应为 0，
    一旦非 0 即提示上游字段缺失，调用方应告警让人复核。
    """
    from .timeutil import et_date, et_today

    today = et_today(now_utc)
    entries: List[Dict[str, Any]] = []
    for x in results or []:
        if not isinstance(x, dict):
            continue
        d = parse_submitted_at(x.get("dateSubmitted"))
        if d is None or et_date(d) != today:
            continue
        entries.append({
            "region": (x.get("settings") or {}).get("region") if isinstance(x.get("settings"), dict) else None,
            "alpha_id": x.get("id"),
            "dateSubmitted": x.get("dateSubmitted"),
            "kind": alpha_kind(x),
        })

    regular_explicit = sum(1 for e in entries if e["kind"] == KIND_REGULAR)
    super_used = sum(1 for e in entries if e["kind"] == KIND_SUPER)
    unclassified_used = sum(1 for e in entries if e["kind"] == KIND_UNKNOWN)
    regular_used = regular_explicit + unclassified_used

    return {
        "et_day": today,
        "regular_used": regular_used,
        "regular_explicit": regular_explicit,
        "unclassified_used": unclassified_used,
        "regular_limit": REGULAR_DAILY_LIMIT,
        "regular_remaining": max(0, REGULAR_DAILY_LIMIT - regular_used),
        "super_used": super_used,
        "super_limit": SUPER_DAILY_LIMIT,
        "super_remaining": max(0, SUPER_DAILY_LIMIT - super_used),
        "entries": entries,
    }
