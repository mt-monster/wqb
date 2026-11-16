# -*- coding: utf-8 -*-
"""把一条回测事实解释成可复用的经验字段（纯函数，无 DB / 无工具依赖）。

判定口径：
- `walls` 由 `review_wave.walls()` 产出（本模块不重复实现阈值逻辑）；本模块只做
  **规范化 / 优先级 / 归类**，把平台 check 名（`LOW_2Y_SHARPE` / `CONCENTRATED_WEIGHT` …）
  映射到稳定的经验词汇。
- `outcome` 与 `failure_class` 是**派生标签**，不是提交判定：提交仍只认
  `submit_verdict` + 用户确认。
"""
from __future__ import annotations

import json
from typing import Any, Dict, Iterable, List, Optional, Sequence

from wqb.config import GATES_PLATFORM, PRODCORR_CEILING

#: 主墙优先级：越靠前越“决定性”。未知/缺数据永远排最后。
WALL_PRIORITY = (
    "CW",
    "RN_EXPOSURE",
    "PROD",
    "SELF",
    "SUB",
    "2Y",
    "SHARPE",
    "FITNESS",
    "MARGIN",
    "TVR",
    "RA",
    "UNKNOWN",
)

#: 原始 check 名 → 规范墙名。顺序敏感：`LOW_2Y_SHARPE` 必须先命中 2Y，
#: `LOW_SUB_UNIVERSE_SHARPE` 必须先命中 SUB。
_ALIASES = (
    ("PROD", ("PROD",)),
    ("SELF", ("SELF",)),
    ("CW", ("CONCENTRATED", "CW")),
    ("RN_EXPOSURE", ("RN_EXPOSURE",)),
    ("SUB", ("SUB_UNIVERSE",)),
    ("2Y", ("2Y", "LADDER")),
    ("SHARPE", ("SHARPE",)),
    ("FITNESS", ("FITNESS",)),
    ("MARGIN", ("MARGIN",)),
    ("TVR", ("TURNOVER", "TVR")),
    ("RA", ("RA_",)),
)

#: 不能靠调参解决的墙（供 next_action / distill 的 structural 标记）
STRUCTURAL_WALLS = frozenset({"RN_EXPOSURE", "SELF"})

_CLASS_BY_WALL = {
    "PROD": "prod",
    "SELF": "self",
    "CW": "cw",
    "RN_EXPOSURE": "rn",
    "SUB": "sub",
    "2Y": "2y",
    "SHARPE": "sharpe",
    "FITNESS": "fitness",
    "MARGIN": "margin",
    "TVR": "turnover",
    "RA": "ra",
    "UNKNOWN": "unknown",
}

_NEXT_ACTION = {
    "PROD": "reduce_prod_or_stop_family",
    "SELF": "diversify_skeleton",
    "CW": "group_neutral_or_pool_diversify",
    "RN_EXPOSURE": "no_param_tuning_stop",
    "SUB": "change_group_axis_or_compress_tail",
    "2Y": "time_aggregate_or_mode_b",
    "SHARPE": "strengthen_signal_or_new_dataset",
    "FITNESS": "raise_signal_to_turnover_ratio",
    "MARGIN": "lower_turnover_or_stronger_signal",
    "TVR": "adjust_decay_or_truncation",
    "RA": "fix_platform_check",
    "UNKNOWN": "collect_more_evidence",
}


def _num(v: Any) -> Optional[float]:
    if isinstance(v, bool):
        return None
    if isinstance(v, (int, float)):
        return float(v)
    try:
        return float(str(v).strip())
    except (TypeError, ValueError):
        return None


def canonical_wall(name: Any) -> str:
    """平台 check 名 / 墙名 → 规范墙名。无法识别时返回 `UNKNOWN`。"""
    s = str(name or "").strip().upper()
    if not s:
        return "UNKNOWN"
    if s in ("NO_DATA", "UNKNOWN") or s.endswith("_UNKNOWN"):
        return "UNKNOWN"
    for canon, tokens in _ALIASES:
        if any(tok in s for tok in tokens):
            return canon
    return "UNKNOWN"


def primary_wall(walls: Optional[Iterable[Any]]) -> Optional[str]:
    """按 `WALL_PRIORITY` 取第一堵；只有未知墙时返回 `UNKNOWN`；无墙返回 None。"""
    if walls is None:
        return None
    canon = [canonical_wall(w) for w in walls]
    if not canon:
        return None
    ranked = sorted(canon, key=lambda w: WALL_PRIORITY.index(w) if w in WALL_PRIORITY else 99)
    return ranked[0]


def metrics_from(row: Dict[str, Any]) -> Dict[str, Any]:
    """从回测行 / 评审行提取指标（兼容 margin_bp / turnover_pct / prod_corr 等别名）。"""
    margin = _num(row.get("margin"))
    margin_bp = _num(row.get("margin_bp"))
    if margin is None and margin_bp is not None:
        margin = margin_bp / 10000.0
    turnover = _num(row.get("turnover"))
    turnover_pct = _num(row.get("turnover_pct"))
    if turnover is None and turnover_pct is not None:
        turnover = turnover_pct / 100.0
    out = {
        "sharpe": _num(row.get("sharpe")),
        "fitness": _num(row.get("fitness")),
        "turnover": turnover,
        "margin": margin,
        "returns": _num(row.get("returns")),
        "drawdown": _num(row.get("drawdown")),
        "two_year_sharpe": _num(row.get("two_year_sharpe", row.get("two_year"))),
        "sub_universe_sharpe": _num(row.get("sub_universe_sharpe", row.get("sub"))),
        "risk_neutralized_sharpe": _num(
            row.get("risk_neutralized_sharpe", row.get("rn_sharpe"))),
        "robust_sharpe": _num(row.get("robust_sharpe")),
        "robust_limit": _num(row.get("robust_limit")),
        "long_count": _num(row.get("long_count")),
        "short_count": _num(row.get("short_count")),
        "prod_correlation": _num(row.get("prod_correlation", row.get("prod_corr"))),
        "self_correlation": _num(row.get("self_correlation", row.get("self_corr"))),
        "is_ladder_sharpe": _num(row.get("is_ladder_sharpe")),
    }
    return {k: v for k, v in out.items() if v is not None}


def _robust_ratio(metrics: Dict[str, Any]) -> Optional[float]:
    v = metrics.get("robust_sharpe")
    if v is None:
        return None
    lim = metrics.get("robust_limit") or 1.0
    try:
        return float(v) / (float(lim) or 1.0)
    except (TypeError, ValueError):
        return None


def is_structural(walls: Optional[Sequence[Any]], metrics: Dict[str, Any]) -> bool:
    """结构性墙：RN/SELF 命中，或 robust 只有 limit 的一小截（<0.5）。

    与 `review_wave.structurally_dead` 同口径；2Y 墙单独不算结构死（可用时间聚合救）。
    """
    canon = {canonical_wall(w) for w in (walls or [])}
    if canon & STRUCTURAL_WALLS:
        return True
    rr = _robust_ratio(metrics)
    if rr is not None and rr < 0.5:
        return True
    return False


def _gates_pass(metrics: Dict[str, Any]) -> bool:
    s = metrics.get("sharpe")
    f = metrics.get("fitness")
    return (s is not None and s > float(GATES_PLATFORM["sharpe_min"])
            and f is not None and f > float(GATES_PLATFORM["fitness_min"]))


def outcome(
    status: Any,
    metrics: Dict[str, Any],
    walls: Optional[Sequence[Any]],
    ra_failed: Optional[Sequence[Any]],
    near_sharpe_min: float = 1.0,
) -> str:
    """win / near / dead / error / unknown。

    - `walls is None` 表示“尚未做墙诊断”，此时用平台硬线粗判，不把缺数据当死；
    - `walls == []` 表示已诊断且无墙 → 达标的强信号（仍需 RA clean）。
    """
    st = str(status or "").strip().upper()
    if st in ("ERROR", "FAIL", "FAILED", "CANCELLED", "CANCELED"):
        return "error"
    sharpe = metrics.get("sharpe")
    if sharpe is None:
        return "unknown"
    # RA 状态三态：[] = 已知全过；非空 = 有失败；None = 未知。
    # `None` 不得当成"全过"——那会把没读过 RA 的行误判成 win（N35 同源纪律）。
    clean = (ra_failed is not None and len(ra_failed) == 0)
    if walls is None:
        if _gates_pass(metrics) and clean:
            return "win"
    else:
        real = [w for w in walls if canonical_wall(w) != "UNKNOWN"]
        if not real and clean and _gates_pass(metrics):
            return "win"
    if is_structural(walls, metrics):
        return "dead"
    if sharpe > float(near_sharpe_min):
        return "near"
    return "dead"


def failure_class(primary: Optional[str], outcome_value: str) -> str:
    if outcome_value == "error":
        return "platform_error"
    if outcome_value == "win":
        return "pass"
    if not primary:
        return "unknown"
    return _CLASS_BY_WALL.get(canonical_wall(primary), "unknown")


def next_action(primary: Optional[str], structural: bool) -> str:
    if structural:
        return "mode_b_structural_or_stop"
    if not primary:
        return "keep"
    return _NEXT_ACTION.get(canonical_wall(primary), "collect_more_evidence")


def _as_dict(payload: Any) -> Dict[str, Any]:
    if isinstance(payload, dict):
        return payload
    if isinstance(payload, str) and payload:
        try:
            d = json.loads(payload)
            return d if isinstance(d, dict) else {}
        except Exception:
            return {}
    return {}


def checks_non_pass(payload: Any, *, cap: int = 50) -> List[Dict[str, Any]]:
    """平台 checks 里非 PASS/PENDING 的项（保留 name/result/limit/value）。

    `payload` 可以是 `backtest_results.payload_json` 解析后的 dict 或原始字符串。
    """
    d = _as_dict(payload)
    out: List[Dict[str, Any]] = []
    for c in (d.get("checks") or []):
        if not isinstance(c, dict):
            continue
        result = str(c.get("result") or "").upper()
        if result in ("PASS", "PENDING"):
            continue
        item = {"name": c.get("name"), "result": c.get("result")}
        for k in ("limit", "value"):
            if c.get(k) is not None:
                item[k] = c.get(k)
        out.append(item)
        if len(out) >= cap:
            return out
    if out:
        return out
    # 旧指标缓存行只有 failed_checks（全部 FAIL 项名）
    for name in (d.get("failed_checks") or []):
        out.append({"name": name, "result": "FAIL"})
        if len(out) >= cap:
            break
    return out


def pseudo_walls(metrics: Dict[str, Any], *, prod_ceiling: float = PRODCORR_CEILING) -> List[str]:
    """把 prod/self 相关性读数转成伪墙（它们不在 review_wave.walls 的词表里）。"""
    out = []
    pc = metrics.get("prod_correlation")
    if pc is not None and pc >= float(prod_ceiling):
        out.append("PROD")
    sc = metrics.get("self_correlation")
    if sc is not None and sc >= float(GATES_PLATFORM.get("self_corr_max", 0.7)):
        out.append("SELF")
    return out
