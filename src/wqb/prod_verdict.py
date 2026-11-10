# -*- coding: utf-8 -*-
"""``check_correlation`` 返回体的**唯一判据解析**（2026-11-10 审查 P2 / 第二批）。

此前仓库里有 8 份各自为政的解析拷贝（``judge`` / ``corr_check`` /
``batch_submit_verdict`` / ``submit_inventory`` / ``submit_alpha`` / ``triage_prodcorr_batch``
/ ``campaign_intel`` / ``backfill_prod_corr``），字段名分四套
（``checks.production.max_correlation`` / 顶层 ``max_correlation`` / ``correlation.max`` /
``get_production_correlation().max``），且对 ``provisional`` / ``from_cache`` / ``stale`` /
``pending`` / ``busy`` / ``data_unavailable`` 的处理互不相同——有的把预读值当终值放行，
有的把缺值当 0.0，有的缺值直接 ``pass=True``。

本模块把这些语义收敛成一处：

* ``value``    —— 数值（越界 / 缺失一律 None，**绝不伪造 0**）
* ``usable``   —— 是否可**用于放行**（平台实测或可信缓存；预读/非实时来源只能证伪）
* ``passes``   —— ``value < threshold``；无法判定时为 None（调用方必须 fail-closed）
* ``provenance`` —— ``platform_live`` / ``cache`` / ``preread`` / ``nonrealtime`` / ``unavailable``
* ``status``   —— ``ok`` / ``pending`` / ``correlation_busy`` / ``data_unavailable`` / ``error``

铁律：**拿不到可用值时 ``passes`` 必须是 None，调用方不得据此放行。**
"""
from __future__ import annotations

from typing import Any, Dict, Optional

from .config import PRODCORR_CEILING

#: 平台明确「还没算好 / 拿不到 / 服务不可用」的状态——一律不可判闸
_UNAVAILABLE_STATUSES = frozenset({"pending", "correlation_busy", "data_unavailable",
                                   "platform_unavailable"})


def _non_realtime_sources() -> frozenset:
    try:
        from .store import NON_REALTIME_SOURCES
        return frozenset(NON_REALTIME_SOURCES)
    except Exception:  # noqa: BLE001 - store 不可用时退回同口径内置集合
        return frozenset({"manual", "legacy", "alphas_backfill",
                          "checkpoint_backfill", "triage_local"})


def _extract_block(result: Dict[str, Any]) -> Dict[str, Any]:
    """兼容四套字段名，统一取出 production 块。"""
    d = result.get("result", result) if isinstance(result, dict) else {}
    if not isinstance(d, dict):
        return {}
    checks = d.get("checks")
    if isinstance(checks, dict):
        prod = checks.get("production")
        if isinstance(prod, dict):
            return prod
    # 顶层兜底（get_production_correlation 直返 / 旧版返回体）
    for key in ("correlation", "production"):
        blk = d.get(key)
        if isinstance(blk, dict) and ("max" in blk or "max_correlation" in blk):
            return blk
    if "max_correlation" in d or "max" in d:
        return d
    return {}


def _coerce_value(raw: Any) -> Optional[float]:
    if raw is None:
        return None
    try:
        v = float(raw)
    except (TypeError, ValueError):
        return None
    if not (0.0 <= v <= 1.0):
        return None
    return v


def prod_verdict(result: Any, threshold: Optional[float] = None) -> Dict[str, Any]:
    """把 ``check_correlation`` 返回体解析成统一判据。

    ``threshold`` 缺省取 :data:`wqb.config.PRODCORR_CEILING`（0.7，唯一事实源）。
    返回 dict 见模块 docstring。**本函数不做任何网络/DB 调用**。
    """
    thr = float(PRODCORR_CEILING if threshold is None else threshold)
    out: Dict[str, Any] = {
        "value": None, "usable": False, "passes": None, "threshold": thr,
        "provenance": "unavailable", "source": None, "from_cache": False,
        "cached_at": None, "age_hours": None, "stale": None,
        "status": "error", "reason": "",
    }
    if not isinstance(result, dict):
        out["reason"] = "check_correlation 返回非 dict"
        return out
    if result.get("__error__"):
        out["reason"] = f"check_correlation 调用失败：{result['__error__']}"
        return out

    blk = _extract_block(result)
    status = str(blk.get("status") or result.get("status") or "ok")
    out["status"] = status
    out["source"] = blk.get("source") or result.get("source")
    out["from_cache"] = bool(blk.get("from_cache") or result.get("from_cache"))
    out["cached_at"] = blk.get("cached_at") or result.get("cached_at")

    if status in _UNAVAILABLE_STATUSES:
        out["reason"] = f"prod 未出数（status={status}）→ 不可判闸"
        return out

    raw = blk.get("max_correlation")
    if raw is None:
        raw = blk.get("max")
    value = _coerce_value(raw)
    out["value"] = value
    if value is None:
        out["reason"] = f"prod 无有效数值（raw={raw!r}）→ 不可判闸"
        return out
    out["passes"] = value < thr

    # 来源分层
    provisional = bool(blk.get("provisional") or result.get("provisional"))
    src = str(out["source"] or "").strip().lower()
    if provisional or src == "alpha_detail_cached":
        out["provenance"] = "preread"
        out["reason"] = "预读值（测量时间不可知）：只许证伪，不许放行"
    elif out["from_cache"] and (not src or src in _non_realtime_sources()):
        out["provenance"] = "nonrealtime"
        out["reason"] = f"缓存值来源不可信（source={out['source']!r}）：只许证伪，不许放行"
    elif out["from_cache"]:
        out["provenance"] = "cache"
        out["usable"] = True
        out["reason"] = f"48h 内缓存实测值（source={out['source']!r}）"
    else:
        out["provenance"] = "platform_live"
        out["usable"] = True
        out["reason"] = "平台本轮实测值"

    # 时效信息（有则带上，供调用方参考；保鲜判定本身在缓存层）
    cdata = blk.get("correlation_data")
    if isinstance(cdata, dict):
        out["age_hours"] = cdata.get("age_hours")
        out["stale"] = cdata.get("stale")
    lk = blk.get("last_known") or result.get("last_known")
    if out["age_hours"] is None and isinstance(lk, dict):
        out["age_hours"] = lk.get("age_hours")
        out["stale"] = lk.get("stale")
    return out


def gate_allowed(result: Any, threshold: Optional[float] = None) -> bool:
    """提交/评审闸的**唯一放行判据**：必须有可用值且 < 阈值。

    缺值 / 预读 / 非实时来源 / 异常一律 False（fail-closed）。
    """
    v = prod_verdict(result, threshold)
    return bool(v["usable"] and v["passes"] is True)
