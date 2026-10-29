# -*- coding: utf-8 -*-
"""corr_timing — ``[corr-t]`` 结构化打点的解析与汇总（2026-10-28 P2-8）。

写入方（唯一实现）：``world-quant-brain-mcp/brain_mixin_spcread._corr_log_timing``；
``check_correlation`` 的缓存命中另有一处调用点（``brain_mixin_correlation``）。
两边字段名必须与本模块 ``FIELDS`` 一致（守护测试逐项比对）。

日志行形态::

    [INFO] [corr-t] {"alpha": "ABC123", "elapsed_ms": 1234, "event": "success", ...}

为什么要单独打点：平台 prod 相关性是**账号级单并发**，一次查询可能包含
「预读 → 排队 → 轮询 → 冷却」四段；普通日志只有人类可读的一句话，无法回答
「14 小时里到底花了多少时间、花在哪一段」（见 ``reports/prod_corr_timing_20261028.md``）。

事件语义（决定折线怎么读）：

===================================  ==========================================
event                                含义
===================================  ==========================================
``cache_hit``                         本地 48h 缓存命中（零平台请求）
``pre_read_hit``                      平台已算好的 ``is.prodCorrelation`` 预读命中
``inflight_join``                     同 alpha 正在算 → 等到了预读结果（省一次计算）
``same_alpha_join``                   跨进程锁 holder 恰是同 alpha → 等到结果
``same_alpha_wait_timeout``           同上但等待窗口内没拿到（随后必有 ``busy``）
``inflight_busy``                     同 alpha 在飞且等待超时 → 返回 busy，不重触发
``busy``                              锁/冷却占用 → fail-fast 拒绝
``success``                           平台轮询拿到值
``pending``                           轮询窗口耗尽仍未出数（时间真花掉了）
``terminal``                          4xx 终态（立即失败，不重试）
===================================  ==========================================

⚠ ``same_alpha_wait_timeout`` 是 ``busy`` 的**前导事件**，不进结果率分母
（否则一次失败会被数两次）。
"""

from __future__ import annotations

import json
import os
from datetime import datetime
from typing import Any, Dict, Iterable, List, Optional, Sequence

#: 日志行里的前缀（``self.log`` 会在前面再拼 ``[INFO] ``）。
MARKER = "[corr-t] "

#: 拿到数值的事件（判闸可用）。
GOT_VALUE_EVENTS = ("cache_hit", "pre_read_hit", "inflight_join",
                    "same_alpha_join", "success")

#: 没拿到数值的**终局**事件。``same_alpha_wait_timeout`` 不在内——
#: 它是前导事件，同一次调用随后还会有一条 ``busy``。
NO_VALUE_EVENTS = ("busy", "inflight_busy", "pending", "terminal")

#: 一次调用的全部可能终局（结果率分母）。
OUTCOME_EVENTS = GOT_VALUE_EVENTS + NO_VALUE_EVENTS

#: 走到平台轮询的事件（真实占用账号单并发槽）。
PLATFORM_EVENTS = ("success", "pending", "terminal")

#: 通过等待拿到结果（省掉一次平台计算）的事件。
JOIN_EVENTS = ("inflight_join", "same_alpha_join")

#: 打点字段全集。写入侧新增字段要先加到这里（守护测试比对）。
FIELDS = (
    "event", "alpha", "elapsed_ms", "ts", "pid", "status", "max", "source",
    "attempts", "computed", "retry_after", "cooldown", "http_status",
    "inflight_n", "platform_retry_after", "holder",
)


# ---------------------------------------------------------------------------
# 解析
# ---------------------------------------------------------------------------
def parse_line(line: str) -> Optional[Dict[str, Any]]:
    """从一行日志里抽出 ``[corr-t] {...}`` 记录；无标记 / 非 JSON → ``None``。

    用 ``raw_decode`` 而非 ``json.loads``：日志文件是 stdout/stderr 合并写，
    行尾可能粘连其它输出，整体 loads 会因尾随字符失败。
    """
    if not line:
        return None
    idx = line.find(MARKER)
    if idx < 0:
        return None
    raw = line[idx + len(MARKER):].strip()
    if not raw:
        return None
    try:
        rec, _end = json.JSONDecoder().raw_decode(raw)
    except ValueError:
        return None
    if not isinstance(rec, dict):
        return None
    ev = rec.get("event")
    if not isinstance(ev, str) or not ev:
        return None
    rec["event"] = ev
    rec["alpha"] = str(rec.get("alpha") or "")
    try:
        rec["elapsed_ms"] = max(0, int(float(rec.get("elapsed_ms") or 0)))
    except (TypeError, ValueError):
        rec["elapsed_ms"] = 0
    return rec


def parse_lines(lines: Iterable[str]) -> List[Dict[str, Any]]:
    """解析多行日志，只保留合法打点（顺序不变）。"""
    out: List[Dict[str, Any]] = []
    for line in lines:
        rec = parse_line(line)
        if rec is not None:
            out.append(rec)
    return out


def parse_file(path: str, encoding: str = "utf-8") -> List[Dict[str, Any]]:
    """解析日志文件。读不到 → ``[]``（调用方负责提示）；解码错误用替换符。"""
    try:
        with open(path, "r", encoding=encoding, errors="replace") as f:
            return parse_lines(f)
    except OSError:
        return []


# ---------------------------------------------------------------------------
# 汇总
# ---------------------------------------------------------------------------
def _pct(sorted_vals: Sequence[int], q: float) -> int:
    """最近秩分位数（空序列 → 0）。纯函数，便于单测。"""
    if not sorted_vals:
        return 0
    if q <= 0:
        return sorted_vals[0]
    if q >= 100:
        return sorted_vals[-1]
    k = int(round((q / 100.0) * (len(sorted_vals) - 1)))
    return sorted_vals[max(0, min(k, len(sorted_vals) - 1))]


def _ts_of(rec: Dict[str, Any]) -> Optional[datetime]:
    ts = rec.get("ts")
    if not isinstance(ts, str) or not ts:
        return None
    for fmt in ("%Y-%m-%dT%H:%M:%S", "%Y-%m-%d %H:%M:%S"):
        try:
            return datetime.strptime(ts, fmt)
        except ValueError:
            continue
    return None


def _sec(ms: int) -> float:
    return round(ms / 1000.0, 1)


def summarize(records: Iterable[Dict[str, Any]], top: int = 5) -> Dict[str, Any]:
    """把打点记录汇总成报告体（可直接 ``json.dumps``）。

    返回键：records / alphas / window / by_event / outcomes / time_s /
    sources / retry_after / top_alphas / repeat_alphas。
    """
    recs = [r for r in records if isinstance(r, dict) and r.get("event")]
    by_event_ms: Dict[str, List[int]] = {}
    per_alpha: Dict[str, Dict[str, Any]] = {}
    ts_list: List[datetime] = []
    sources: Dict[str, int] = {}
    retry_after: List[int] = []
    computed_true = computed_total = 0

    for r in recs:
        ev = str(r.get("event"))
        ms = int(r.get("elapsed_ms") or 0)
        by_event_ms.setdefault(ev, []).append(ms)
        aid = str(r.get("alpha") or "")
        if aid:
            pa = per_alpha.setdefault(aid, {"alpha": aid, "events": 0, "elapsed_ms": 0,
                                            "events_set": set()})
            pa["events"] += 1
            pa["elapsed_ms"] += ms
            pa["events_set"].add(ev)
        t = _ts_of(r)
        if t is not None:
            ts_list.append(t)
        if ev in GOT_VALUE_EVENTS and r.get("source"):
            src = str(r.get("source"))
            sources[src] = sources.get(src, 0) + 1
        if ev in ("busy", "pending", "inflight_busy"):
            try:
                ra = int(float(r.get("retry_after") or 0))
            except (TypeError, ValueError):
                ra = 0
            if ra > 0:
                retry_after.append(ra)
        if ev == "success":
            computed_total += 1
            if r.get("computed"):
                computed_true += 1

    by_event: Dict[str, Dict[str, float]] = {}
    for ev, vals in sorted(by_event_ms.items()):
        s = sorted(vals)
        by_event[ev] = {
            "count": len(s),
            "sum_s": _sec(sum(s)),
            "median_s": _sec(_pct(s, 50)),
            "p90_s": _sec(_pct(s, 90)),
            "max_s": _sec(s[-1] if s else 0),
        }

    def _count(events: Iterable[str]) -> int:
        return sum(by_event.get(e, {}).get("count", 0) for e in events)

    got = _count(GOT_VALUE_EVENTS)
    miss = _count(NO_VALUE_EVENTS)
    denom = got + miss
    window: Dict[str, Any] = {"first": None, "last": None, "span_h": None}
    if ts_list:
        lo, hi = min(ts_list), max(ts_list)
        window = {"first": lo.strftime("%Y-%m-%dT%H:%M:%S"),
                  "last": hi.strftime("%Y-%m-%dT%H:%M:%S"),
                  "span_h": round((hi - lo).total_seconds() / 3600.0, 2)}

    top_alphas = sorted(
        ({"alpha": p["alpha"], "events": p["events"], "elapsed_s": _sec(p["elapsed_ms"]),
          "kinds": sorted(p["events_set"])} for p in per_alpha.values()),
        key=lambda x: (-x["elapsed_s"], -x["events"], x["alpha"]),
    )[:max(1, int(top))]
    repeat_alphas = sorted(
        ({"alpha": p["alpha"], "events": p["events"], "kinds": sorted(p["events_set"])}
         for p in per_alpha.values() if p["events"] > 1),
        key=lambda x: (-x["events"], x["alpha"]),
    )[:10]

    ra_sorted = sorted(retry_after)
    return {
        "records": len(recs),
        "alphas": len(per_alpha),
        "window": window,
        "by_event": by_event,
        "outcomes": {
            "got_value": got,
            "no_value": miss,
            "value_rate": round(got / denom, 3) if denom else None,
            "joins": _count(JOIN_EVENTS),
            "cache_hits": _count(("cache_hit",)),
            "pre_read_hits": _count(("pre_read_hit",)),
            "platform_polls": _count(PLATFORM_EVENTS),
            "computed": computed_true,
            "computed_of_success": computed_total,
        },
        "time_s": {
            "platform_success": by_event.get("success", {}).get("sum_s", 0.0),
            "platform_pending": by_event.get("pending", {}).get("sum_s", 0.0),
            "join_wait": round(
                by_event.get("inflight_join", {}).get("sum_s", 0.0)
                + by_event.get("same_alpha_join", {}).get("sum_s", 0.0), 1),
            "same_alpha_wait_timeout": by_event.get(
                "same_alpha_wait_timeout", {}).get("sum_s", 0.0),
        },
        "sources": dict(sorted(sources.items(), key=lambda kv: (-kv[1], kv[0]))),
        "retry_after": {
            "count": len(ra_sorted),
            "median_s": _pct(ra_sorted, 50),
            "max_s": ra_sorted[-1] if ra_sorted else 0,
        },
        "top_alphas": top_alphas,
        "repeat_alphas": repeat_alphas,
    }


def default_log_path() -> str:
    """缺省日志位：``<repo>/logs/wq-brain-http.log``（``start_wq_mcp.py`` 的落点）。"""
    try:
        from wqb.paths import repo_root
        root = str(repo_root())
    except Exception:  # pragma: no cover - 仓库外使用（技能安装位）时退回 cwd
        root = os.getcwd()
    return os.path.join(root, "logs", "wq-brain-http.log")
