#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""gradient_coverage.py — 梯度覆盖率审计 / 缺臂计划 / 算子 lint（2026-11-23 落地）。

为什么有这个工具
----------------
用户 2026-11-23 质询「所有梯度都测完了吗」。当时台账写的是「全轴穷尽」，实际把平台
读回的真实表达式拆成 9 层后，**4 个算子类别轴一格未扫**（L1 vec 折叠 / L4 时序 /
L5·L8 外层 group / 分组轴）。补齐 45 臂后 S 不变但 2Y +0.15 / sub +0.05 / robust +0.08。

根因不是「少跑了几个臂」，而是 **没有任何机制回答"缺哪几个臂"** —— 全靠人记。
本工具把这件事机械化：读表达式 → 拆层 → 按 catalog 同类算子全集算覆盖率 → 输出缺臂计划。

对应六条落地纪律（用户「三、优化空间 全部落地」）
-------------------------------------------------
A. **覆盖率审计**：`audit` 输出每层 tested / missing / coverage（本工具本体）
B. **settings 与算子臂分家**：`plan` 把 settings 轴单独列成"一值一批"，
   并拒绝对批级参数生成同批臂（`GRADIENT_BATCH_LEVEL_SETTINGS`）
C. **扫描顺序固定**：缺臂按 `GRADIENT_SCAN_ORDER`（杠杆量级降序）排序，语义层在前
D. **算子 lint**：`lint` 委托 `wqb.expression.op_arity` 做存在性 + 元数校验
   （幽灵算子 / 命名参数写错，本地离线可查，不用等平台 CANCEL 整批）
E. **闸门导向**：`audit` 顺带打印每条臂的 `checks.fail` 缺口（limit−value），
   limit 一律取平台下发的值，本地不另立一套数字
F. **收割归属**：`--exprs` 支持直接吃 `harvest_multisim_alphas` 的 JSON
   （同批 children 顺序 = 提交顺序，平台对同码返回同一 alpha id，已实测）

三个子命令
----------
::

    # A/E 审计：本波覆盖了哪些层×类别，缺什么，离闸多远
    python tools/research/gradient_coverage.py audit --exprs logs/_tmp_batch.json
    python tools/research/gradient_coverage.py audit --alpha-id vR1poWNz --alpha-id A1xXeJqW

    # A/B/C 缺臂计划：给出下一批该测哪些（自动跳过 no-op、标注需人工复核参数的替换）
    python tools/research/gradient_coverage.py plan --alpha-id A1xXeJqW --max-arms 10 \
        --out logs/_tmp_plan.json

    # D lint：派批前离线查算子名/元数（替代"平台 CANCEL 整批才发现"）
    python tools/research/gradient_coverage.py lint --exprs logs/_tmp_plan.json

诚实边界
--------
- `plan` 生成的是**候选**，不是可无条件派发的臂：`review` 非空的替换改变了参数语义
  （典型 `group_backfill(x,group,d)` ↔ `group_mean(x,weight,group)`，同 arity≠同语义，
  2026-11-22 已因机械替换踩过 UNITS 整批失败）。
- 不派发回测（用户硬约束：派发只用 MCP `create_multi_simulation`）。
- 不判断哪个算子更好 —— 好坏由回测 Δ 表回答。
- 层归属是**结构近似**（按 category + 嵌套深度），不是经济语义判定。

与既有工具的**分工**（别当重复实现）
------------------------------------
- `tools/gates/operator_coverage_audit.py`：管**面** —— 「全平台 103 个算子里，本战役
  哪些从没用过」（`--checklist` / `--glob` / `--wave`）。
- 本工具：管**点** —— 「这一条基线表达式拆成若干层后，**每层的同类可换算子**还缺哪几个，
  下一个臂该写什么」，并把 settings 轴与 no-op 律一起处理。
两者数据源相同（`operators_catalog.json`），但回答的问题不同：那一个防「整类没用过」，
本工具防「用过同类的一个就以为那一层扫完了」。

数据源
------
- 算子目录：`docs/reference/operators_catalog.json`（`get_operators` 实时快照）
- 同类可换集合：复用 `tools/research/operator_swap_matrix.py` 的 `CATEGORY_SINGLE_INPUT`
- 扫描顺序 / 参数层 / no-op 律 / 批级设置：`src/wqb/config.py`（唯一事实源）
"""
from __future__ import annotations

import argparse
import asyncio
import json
import os
import re
import sys
from typing import Any, Dict, Iterable, List, Optional, Sequence, Tuple

TOOLS_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROOT = os.path.dirname(TOOLS_DIR)
for _p in (os.path.join(ROOT, "src"), os.path.join(ROOT, "world-quant-brain-mcp"), TOOLS_DIR,
           os.path.dirname(os.path.abspath(__file__))):
    if _p not in sys.path:
        sys.path.insert(0, _p)

from wqb.config import (  # noqa: E402
    GRADIENT_AMPLITUDE_PROBES,
    GRADIENT_BATCH_LEVEL_SETTINGS,
    GRADIENT_GROUPING_AXES,
    GRADIENT_NOOP_LAWS,
    GRADIENT_PARAM_LAYERS,
    GRADIENT_SCAN_ORDER,
    GRADIENT_TAIL_Q_PROBES,
    GRADIENT_WINDOW_PROBES,
)

import operator_swap_matrix as osm  # noqa: E402  （复用 catalog / noop / 替换实现）

_CATEGORY_LAYER = {
    "Vector": "L1_vector_fold",
    "Arithmetic": "L2_arithmetic",
    "Logical": "L3_logical",
    "Time Series": "L4_time_series",
    "Cross Sectional": "L6_cross_sectional",
    "Transformational": "L7_transform",
    # Group 按嵌套深度拆 L5/L8，见 annotate_layers
}
_AXIS_OPS = {"group_cartesian_product"}
_RANK_LIKE = {"rank", "group_rank", "quantile", "ts_quantile"}
_CALL_RE = re.compile(r"([A-Za-z_][A-Za-z0-9_]*)\s*\(")


# ---------------------------------------------------------------------------
# 解析：表达式 → 槽位（op 调用点）
# ---------------------------------------------------------------------------

def _match_paren(text: str, open_idx: int) -> int:
    """返回与 ``text[open_idx] == '('`` 配对的 ``)`` 索引；不配平返回 -1。"""
    depth = 0
    in_str: Optional[str] = None
    for i in range(open_idx, len(text)):
        ch = text[i]
        if in_str:
            if ch == in_str:
                in_str = None
            continue
        if ch in ("'", '"'):
            in_str = ch
            continue
        if ch == "(":
            depth += 1
        elif ch == ")":
            depth -= 1
            if depth == 0:
                return i
    return -1


def _split_top(text: str, sep: str = ",") -> List[str]:
    parts, buf, depth, in_str = [], [], 0, None
    for ch in text:
        if in_str:
            buf.append(ch)
            if ch == in_str:
                in_str = None
            continue
        if ch in ("'", '"'):
            in_str = ch
            buf.append(ch)
        elif ch in "([{":
            depth += 1
            buf.append(ch)
        elif ch in ")]}":
            depth -= 1
            buf.append(ch)
        elif ch == sep and depth == 0:
            parts.append("".join(buf).strip())
            buf = []
        else:
            buf.append(ch)
    if "".join(buf).strip():
        parts.append("".join(buf).strip())
    return parts


def split_slots(expr: str) -> List[Dict[str, Any]]:
    """把表达式拆成算子调用槽位列表。

    每个槽位：``{op, start, end, depth, args, arg_text}``。
    ``depth`` = 该调用名出现时已打开的左括号数（顶层调用为 0）。
    """
    slots: List[Dict[str, Any]] = []
    depth = 0
    i = 0
    n = len(expr)
    while i < n:
        ch = expr[i]
        if ch == "(":
            depth += 1
            i += 1
            continue
        if ch == ")":
            depth -= 1
            i += 1
            continue
        if ch.isalpha() or ch == "_":
            j = i
            while j < n and (expr[j].isalnum() or expr[j] == "_"):
                j += 1
            name = expr[i:j]
            k = j
            while k < n and expr[k].isspace():
                k += 1
            if k < n and expr[k] == "(":
                end = _match_paren(expr, k)
                if end < 0:
                    raise ValueError(f"括号不配平：{expr[:80]}…")
                slots.append({
                    "op": name,
                    "start": i,
                    "end": end + 1,
                    "depth": depth,
                    "args": _split_top(expr[k + 1:end]),
                    "arg_text": expr[k + 1:end],
                })
                depth += 1  # 该调用的左括号已进入（其 ')' 在后续扫描里自然减掉）
                i = k + 1
                continue
            i = j
            continue
        i += 1
    return slots


def annotate_layers(expr: str, cat: Dict[str, dict]) -> List[Dict[str, Any]]:
    """给槽位打上层标签（L1…L8）；group 类按嵌套深度拆内/外层。"""
    slots = split_slots(expr)
    for s in slots:
        s["category"] = cat.get(s["op"], {}).get("category", "unknown")
        s["layer"] = _CATEGORY_LAYER.get(s["category"], "L99_other")
        if s["op"] in _AXIS_OPS:
            s["layer"] = "L9_grouping_axis"
    group_slots = sorted(
        [s for s in slots if s["category"] == "Group" and s["op"] not in _AXIS_OPS],
        key=lambda s: s["depth"],
    )
    for idx, s in enumerate(group_slots):
        # 最外层（depth 最小）→ L8；其余（含唯一一个时的那个）→ L5
        s["layer"] = "L8_group_outer" if (len(group_slots) >= 2 and idx == 0) else "L5_group_inner"
    return slots


def _sig_map():
    try:
        from wqb.expression.op_arity import load_signatures
        return load_signatures()
    except Exception:  # pragma: no cover - catalog 缺失时的降级
        return {}


def grouping_axes(slots: Sequence[Dict[str, Any]], sigs: Optional[dict] = None) -> List[str]:
    """提取分组轴（group_* 的 ``group`` 位置参数 / 组合轴表达式）。"""
    sigs = sigs if sigs is not None else _sig_map()
    out: List[str] = []
    for s in slots:
        if s.get("category") != "Group":
            continue
        if s["op"] in _AXIS_OPS:
            out.append(s["arg_text"].strip())
            continue
        idx = None
        sig = sigs.get(s["op"])
        if sig and "group" in getattr(sig, "positional", ()):
            idx = sig.positional.index("group")
        elif s["args"]:
            idx = len(s["args"]) - 1
        if idx is not None and idx < len(s["args"]):
            arg = s["args"][idx].strip()
            if re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", arg):
                out.append(arg)
    return list(dict.fromkeys(out))


def windows_of(slots: Sequence[Dict[str, Any]]) -> List[int]:
    """提取 ts_* 槽位里的窗口常数（全数字的位置参数）。"""
    out: List[int] = []
    for s in slots:
        if s.get("category") != "Time Series" and not s["op"].startswith("ts_"):
            continue
        for a in s["args"][1:]:
            a = a.split("=")[-1].strip()
            if a.isdigit():
                out.append(int(a))
                break
    return sorted(set(out))


def tail_qs_of(slots: Sequence[Dict[str, Any]]) -> List[Tuple[float, float]]:
    out: List[Tuple[float, float]] = []
    for s in slots:
        if s["op"] != "tail":
            continue
        lo = hi = None
        for a in s["args"]:
            if "=" in a:
                k, v = a.split("=", 1)
                k, v = k.strip(), v.strip()
                try:
                    if k == "lower":
                        lo = float(v)
                    elif k == "upper":
                        hi = float(v)
                except ValueError:
                    pass
        if lo is not None and hi is not None:
            out.append((lo, hi))
    return out


def amplitude_of(slots: Sequence[Dict[str, Any]]) -> List[Tuple[str, float]]:
    out: List[Tuple[str, float]] = []
    for s in slots:
        if s["op"] not in ("winsorize", "signed_power", "quantile", "ts_quantile"):
            continue
        for a in s["args"][1:]:
            if "=" in a:
                k, v = a.split("=", 1)
                k, v = k.strip(), v.strip()
                try:
                    out.append((f"{s['op']}.{k}", float(v)))
                except ValueError:
                    pass
            else:
                try:
                    out.append((f"{s['op']}.positional", float(a)))
                except ValueError:
                    pass
    return out


# ---------------------------------------------------------------------------
# 覆盖率审计（A） + 闸门缺口（E）
# ---------------------------------------------------------------------------

def _universe(layer: str) -> List[str]:
    """该层的同类可换算子全集（来自 operator_swap_matrix 的人工核对白名单）。"""
    cat_name = {
        "L1_vector_fold": "Vector",
        "L2_arithmetic": "Arithmetic",
        "L3_logical": "Logical",
        "L4_time_series": "Time Series",
        "L5_group_inner": "Group",
        "L6_cross_sectional": "Cross Sectional",
        "L7_transform": "Transformational",
        "L8_group_outer": "Group",
    }.get(layer)
    if not cat_name:
        return []
    return sorted(osm.CATEGORY_SINGLE_INPUT.get(cat_name, set()))


def audit(expressions: Sequence[str], alphas: Optional[Sequence[dict]] = None) -> Dict[str, Any]:
    """按层统计 tested / missing / coverage；并汇总闸门缺口。"""
    cat = osm._load_catalog()
    sigs = _sig_map()
    tested_ops: Dict[str, set] = {}
    axes: set = set()
    wins: set = set()
    tqs: set = set()
    amps: set = set()
    for expr in expressions:
        slots = annotate_layers(expr, cat)
        for s in slots:
            tested_ops.setdefault(s["layer"], set()).add(s["op"])
        axes.update(grouping_axes(slots, sigs))
        wins.update(windows_of(slots))
        tqs.update(tail_qs_of(slots))
        amps.update(v for _, v in amplitude_of(slots))

    layers: Dict[str, Dict[str, Any]] = {}
    for layer in GRADIENT_SCAN_ORDER:
        uni: List[str] = []
        got: List[str] = []
        missing: Optional[List[str]] = None
        if layer == "L9_grouping_axis":
            uni = list(GRADIENT_GROUPING_AXES)
            got = [x for x in uni if x in axes]
        elif layer == "L10_window":
            uni = [str(w) for w in GRADIENT_WINDOW_PROBES]
            got = [str(w) for w in sorted(wins)]
        elif layer == "L11_amplitude":
            uni = [f"{v:g}" for v in GRADIENT_AMPLITUDE_PROBES.get("winsorize_std", ())]
            got = [f"{v:g}" for v in sorted(amps)] if amps else []
        elif layer == "L12_tail_q":
            uni = [f"{lo:g}/{hi:g}" for lo, hi in GRADIENT_TAIL_Q_PROBES]
            got = [f"{lo:g}/{hi:g}" for lo, hi in sorted(tqs)] if tqs else []
        elif layer == "L13_settings":
            uni = list(GRADIENT_BATCH_LEVEL_SETTINGS)
            cur = {}
            if alphas:
                cur = (alphas[0].get("settings") or {})
            def _get(k):
                camel = "".join(w.capitalize() if i else w for i, w in enumerate(k.split("_")))
                return cur.get(k, cur.get(camel))
            got = [f"{k}={_get(k)}" for k in uni if _get(k) is not None]
            missing = [k for k in uni if _get(k) is None]
        else:
            uni = _universe(layer)
            got = sorted(tested_ops.get(layer, set()))
        if missing is None:
            missing = [x for x in uni if x not in got]
        got_in_uni = [x for x in got if x in uni]

        manual = layer == "L13_settings"
        layers[layer] = {
            "tested": got,
            "tested_in_universe": got_in_uni,
            "missing": missing,
            "universe": uni,
            "coverage": ("manual（批级：一值一批）" if manual
                         else (f"{len(got_in_uni)}/{len(uni)}" if uni else "n/a")),
            "param_layer": layer in GRADIENT_PARAM_LAYERS,
            "closed": (False if manual else (not missing if uni else True)),
            "manual": manual,
        }

    noop_warnings: List[str] = []
    for expr in expressions:
        slots = annotate_layers(expr, cat)
        name = expr[:60] + "…" if len(expr) > 60 else expr
        if slots and slots[0]["op"] in _RANK_LIKE:
            noop_warnings.append(f"[{name}] {GRADIENT_NOOP_LAWS['truncation_after_rank']}")
        if any(s["op"] == "group_rank" for s in slots) and any(
            s["op"] in ("quantile", "signed_power", "winsorize") for s in slots
        ):
            noop_warnings.append(f"[{name}] {GRADIENT_NOOP_LAWS['monotone_before_group_rank']}")
        if any(s["op"] == "ts_backfill" for s in slots) and any(
            s["op"] == "group_backfill" for s in slots
        ):
            noop_warnings.append(
                f"[{name}] {GRADIENT_NOOP_LAWS['inner_backfill_makes_group_backfill_noop']}")

    gate_gaps: Dict[str, List[dict]] = {}
    for a in alphas or []:
        aid = a.get("alpha_id") or a.get("id") or "?"
        checks = (a.get("checks") or {})
        fails = checks.get("fail")
        if not fails:
            raw = (a.get("is") or {}).get("checks") or []
            fails = [c for c in raw if str(c.get("result", "")).upper() in ("FAIL", "ERROR")]
        rows = []
        for f in fails:
            if not isinstance(f, dict):
                continue
            val, lim = f.get("value"), f.get("limit")
            gap = None
            try:
                gap = round(float(lim) - float(val), 4)
            except (TypeError, ValueError):
                pass
            rows.append({"check": f.get("name"), "value": val, "limit": lim, "gap": gap})
        if rows:
            gate_gaps[aid] = rows

    return {
        "expressions": len(expressions),
        "layers": layers,
        "open_layers": [k for k, v in layers.items() if not v["closed"]],
        "grouping_axes_found": sorted(axes),
        "noop_warnings": noop_warnings,
        "gate_gaps": gate_gaps,
        "scan_order": list(GRADIENT_SCAN_ORDER),
        "param_layers": sorted(GRADIENT_PARAM_LAYERS),
    }


# ---------------------------------------------------------------------------
# 缺臂计划（A/B/C） —— 生成候选，不派发
# ---------------------------------------------------------------------------

def _pos_names(op: str, sigs: dict) -> Tuple[str, ...]:
    sig = sigs.get(op)
    return tuple(getattr(sig, "positional", ()) or ())


def _needs_param_review(from_op: str, to_op: str, sigs: dict) -> Optional[str]:
    """同 arity 但参数位语义不同 ⇒ 机械替换会静默改变含义（2026-11-22 UNITS 事故同源）。"""
    a, b = _pos_names(from_op, sigs), _pos_names(to_op, sigs)
    if not a or not b:
        return None
    if a[1:] != b[1:]:
        return f"参数位语义不同：{from_op}{a} → {to_op}{b}（须人工核对顺序/量纲）"
    return None


def plan(expressions: Sequence[str], max_arms: int = 10,
         layers: Optional[Iterable[str]] = None,
         all_slots: bool = False) -> Dict[str, Any]:
    """按 `GRADIENT_SCAN_ORDER` 生成缺臂（语义层优先），settings 轴单独列出。"""
    if not expressions:
        raise ValueError("plan 需要至少一个基线表达式")
    cat = osm._load_catalog()
    sigs = _sig_map()
    audit_rep = audit(expressions)
    wanted = set(layers) if layers else set(GRADIENT_SCAN_ORDER)

    arms: List[Dict[str, Any]] = []
    skipped: List[Dict[str, str]] = []
    skipped_arity: List[Dict[str, str]] = []
    seen: set = set()

    def _push(layer: str, expr: str, **meta):
        if expr in seen:
            return
        seen.add(expr)
        arms.append({"layer": layer, "expression": expr, **meta})

    for layer in GRADIENT_SCAN_ORDER:
        if layer not in wanted or len(arms) >= max_arms:
            continue
        info = audit_rep["layers"].get(layer) or {}
        missing = info.get("missing") or []
        if not missing:
            continue

        if layer in ("L11_amplitude", "L12_tail_q", "L13_settings"):
            # 参数层 / 批级设置：不作为表达式臂生成，交由 settings_plan
            continue

        base = expressions[0]
        slots = annotate_layers(base, cat)

        if layer == "L9_grouping_axis":
            chosen = [s for s in slots if s.get("category") == "Group"
                      and s["op"] not in _AXIS_OPS]
            for axis in missing:
                expr = _replace_group_arg(base, chosen, axis, sigs)
                _push(layer, expr, from_value="axis", to_value=axis)
            continue

        if layer == "L10_window":
            for w in missing:
                expr = _replace_window(base, int(w))
                if expr:
                    _push(layer, expr, from_value="window", to_value=w)
            continue

        for s in slots:
            if s["layer"] != layer or len(arms) >= max_arms:
                continue
            same = [x for x in slots if x["op"] == s["op"]]
            if not all_slots and s is not same[0]:
                continue  # 默认只规划每层每算子的首个槽位，避免同类槽位灌满 max_arms
            nth = same.index(s) + 1  # operator_swap_matrix 的 nth 是 1-based
            for cand in missing:
                if len(arms) >= max_arms:
                    break
                reason = osm._noop_reason(base, s["op"], cand, nth=nth, cat=cat)
                if reason:
                    bucket = skipped_arity if reason.startswith("arity") else skipped
                    note = reason
                    if bucket is skipped_arity:
                        note = (f"{reason}；**需手工重排参数位**——同 arity≠同语义的机械替换"
                                f"曾致 UNITS 整批失败（2026-11-22 group_backfill↔group_mean）")
                    bucket.append({"layer": layer, "op": f"{s['op']}→{cand}", "reason": note})
                    continue
                expr = osm._replace_op(base, s["op"], cand, nth=nth)
                review = _needs_param_review(s["op"], cand, sigs)
                _push(layer, expr, from_op=s["op"], to_op=cand,
                      needs_param_review=review, nth=nth)
        if len(arms) >= max_arms:
            break

    settings_plan = {
        "rule": "批级参数：同一批内所有臂共享 ⇒ 一值一批，禁止与表达式臂混排",
        "keys": [k for k in GRADIENT_BATCH_LEVEL_SETTINGS],
        "batches": [
            {"setting": k, "values": [], "note": "每值单独一批，批内只放 3 个代表臂"}
            for k in GRADIENT_BATCH_LEVEL_SETTINGS
        ],
        "noop_warning": (
            GRADIENT_NOOP_LAWS["truncation_after_rank"]
            if (expressions and annotate_layers(expressions[0], cat)
                and annotate_layers(expressions[0], cat)[0]["op"] in _RANK_LIKE)
            else None
        ),
    }
    return {
        "baseline": expressions[0],
        "arms": arms[:max_arms],
        "skipped_noop": skipped,
        "skipped_arity_manual": skipped_arity,
        "settings_plan": settings_plan,
        "coverage_after_plan": _coverage_preview(audit_rep, arms),
    }


def _replace_group_arg(expr: str, group_slots: Sequence[Dict[str, Any]],
                       axis: str, sigs: dict) -> str:
    """只替换 group_* 调用的 group 位置实参，其余逐字冻结。"""
    # 从内向外改，避免位置漂移
    out = expr
    for s in sorted(group_slots, key=lambda x: -x["start"]):
        idx = None
        sig = sigs.get(s["op"])
        if sig and "group" in _pos_names(s["op"], sigs):
            idx = sig.positional.index("group")
        elif s["args"]:
            idx = len(s["args"]) - 1
        if idx is None or idx >= len(s["args"]):
            continue
        args = list(s["args"])
        args[idx] = axis
        new_call = f"{s['op']}({', '.join(args)})"
        out = out[:s["start"]] + new_call + out[s["end"]:]
    return out


def _replace_window(expr: str, window: int) -> Optional[str]:
    """替换第一个 ts_* 调用里的窗口常数。"""
    slots = split_slots(expr)
    for s in sorted(slots, key=lambda x: -x["start"]):
        if not s["op"].startswith("ts_") or len(s["args"]) < 2:
            continue
        args = list(s["args"])
        for i in range(1, len(args)):
            if args[i].strip().isdigit():
                args[i] = str(window)
                new_call = f"{s['op']}({', '.join(args)})"
                return expr[:s["start"]] + new_call + expr[s["end"]:]
    return None


def _coverage_preview(audit_rep: dict, arms: Sequence[dict]) -> Dict[str, str]:
    """计划执行后的覆盖率（按 to_op / to_value 记账）。"""
    out: Dict[str, str] = {}
    for layer, info in audit_rep["layers"].items():
        if info.get("manual"):
            out[layer] = "manual"
            continue
        uni = [str(x) for x in (info.get("universe") or [])]
        if not uni:
            out[layer] = "n/a"
            continue
        tested = {str(x) for x in (info.get("tested_in_universe") or info.get("tested") or [])}
        for a in arms:
            if a.get("layer") != layer:
                continue
            if a.get("to_op"):
                tested.add(str(a["to_op"]))
            if a.get("to_value") is not None:
                tested.add(str(a["to_value"]))
        out[layer] = f"{len(tested & set(uni))}/{len(uni)}"
    return out


# ---------------------------------------------------------------------------
# 算子 lint（D）
# ---------------------------------------------------------------------------

def lint(expressions: Sequence[str]) -> Dict[str, Any]:
    """委托 `wqb.expression.op_arity`：算子存在性 + 元数 + 命名参数（离线）。"""
    from wqb.expression.op_arity import check_expressions, format_report
    report = check_expressions(list(expressions))
    return {"ok": bool(report.get("ok")), "report": report,
            "text": format_report(report)}


# ---------------------------------------------------------------------------
# 取数：--alpha-id / --exprs
# ---------------------------------------------------------------------------

def _load_exprs_file(path: str) -> List[str]:
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    out: List[str] = []

    def _walk(node):
        if isinstance(node, str):
            out.append(node)
        elif isinstance(node, dict):
            for k in ("code", "expression", "expr"):
                if isinstance(node.get(k), str):
                    out.append(node[k])
                    return
            for v in node.values():
                _walk(v)
        elif isinstance(node, list):
            for v in node:
                _walk(v)

    _walk(data)
    return list(dict.fromkeys(out))


def _fetch_alphas(alpha_ids: Sequence[str]) -> List[dict]:
    """用 brain_client 取 alpha 详情（与 MCP 同源；只读）。"""
    from brain_api import brain_client

    async def _run():
        rows = []
        for aid in alpha_ids:
            d = await brain_client.get_alpha_details(aid)
            rows.append(d)
        return rows

    return asyncio.run(_run())


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def _print_audit(rep: dict) -> None:
    print(f"表达式数：{rep['expressions']}")
    print("\n层覆盖率（按杠杆量级降序）：")
    for layer in rep["scan_order"]:
        info = rep["layers"].get(layer) or {}
        if not info:
            continue
        flag = "✅" if info["closed"] else "⛔"
        tag = "（参数层）" if info["param_layer"] else ""
        cov = info["coverage"]
        miss = "" if info["closed"] else "  缺：" + ", ".join(info["missing"][:12])
        print(f"  {flag} {layer:<20} {cov:>8}{tag}{miss}")
    if rep["grouping_axes_found"]:
        print(f"\n分组轴实测：{', '.join(rep['grouping_axes_found'])}")
    if rep["noop_warnings"]:
        print("\nNO-OP 提示：")
        for w in dict.fromkeys(rep["noop_warnings"]):
            print(f"  · {w}")
    if rep["gate_gaps"]:
        print("\n闸门缺口（limit 取平台下发值）：")
        for aid, rows in rep["gate_gaps"].items():
            parts = [f"{r['check']} {r['value']}→{r['limit']}(差{r['gap']})" for r in rows]
            print(f"  {aid}: " + "; ".join(parts))
    if rep["open_layers"]:
        print(f"\n开放层：{', '.join(rep['open_layers'])}")
    else:
        print("\n全部层已关闭（但请注意：覆盖率 ≠ 达到闸门；离闸距离见上）。")


def _print_plan(rep: dict) -> None:
    print(f"基线：{rep['baseline'][:110]}{'…' if len(rep['baseline']) > 110 else ''}")
    print(f"\n缺臂候选（{len(rep['arms'])} 条，按扫描顺序）：")
    for i, a in enumerate(rep["arms"], 1):
        print(f"  {i:>2}. [{a['layer']}] {a.get('from_op', a.get('from_value'))}"
              f"→{a.get('to_op', a.get('to_value'))}")
        print(f"      {a['expression']}")
        if a.get("needs_param_review"):
            print(f"      ⚠ REVIEW: {a['needs_param_review']}")
    if rep["skipped_noop"]:
        print("\n已跳过（no-op）：")
        for s in rep["skipped_noop"]:
            print(f"  · [{s['layer']}] {s['op']} —— {s['reason']}")
    sp = rep["settings_plan"]
    print(f"\n设置轴（{sp['rule']}）：")
    print("  keys: " + ", ".join(sp["keys"]))
    if sp.get("noop_warning"):
        print(f"  ⚠ {sp['noop_warning']}")
    print("\n覆盖率预览（执行本计划后）：" + ", ".join(
        f"{k}={v}" for k, v in rep["coverage_after_plan"].items()))


def _main(argv: Optional[Sequence[str]] = None) -> int:
    ap = argparse.ArgumentParser(
        description="梯度覆盖率审计 / 缺臂计划 / 算子 lint（见模块 docstring）")
    sub = ap.add_subparsers(dest="cmd", required=True)

    def _common(p):
        p.add_argument("--exprs", help="表达式 JSON（字符串数组 / 对象数组 / harvest 输出）")
        p.add_argument("--alpha-id", action="append", default=[],
                       help="alpha id（可重复；用 brain_client 取 code，需平台会话）")
        p.add_argument("--json", dest="json_out", help="把结果写成 JSON")

    p_audit = sub.add_parser("audit", help="覆盖率 + 闸门缺口")
    _common(p_audit)

    p_plan = sub.add_parser("plan", help="生成缺臂候选")
    _common(p_plan)
    p_plan.add_argument("--max-arms", type=int, default=10)
    p_plan.add_argument("--layers", help="只在这些层生成，逗号分隔")
    p_plan.add_argument("--all-slots", action="store_true",
                        help="同类算子有多个槽位时逐个规划（默认只规划首个）")
    p_plan.add_argument("--out", help="把候选写成 JSON（可直接喂 preflight）")

    p_lint = sub.add_parser("lint", help="离线算子存在性/元数校验")
    _common(p_lint)

    args = ap.parse_args(argv)

    exprs: List[str] = []
    alphas: List[dict] = []
    if args.exprs:
        exprs.extend(_load_exprs_file(args.exprs))
    if args.alpha_id:
        alphas = _fetch_alphas(args.alpha_id)
        for d in alphas:
            code = d.get("code") or (d.get("regular") or {}).get("code")
            if code:
                exprs.append(code)
    if not exprs:
        ap.error("需要 --exprs 或 --alpha-id 提供至少一条表达式")

    if args.cmd == "audit":
        rep = audit(exprs, alphas)
        _print_audit(rep)
        if args.json_out:
            with open(args.json_out, "w", encoding="utf-8") as f:
                json.dump(rep, f, ensure_ascii=False, indent=2)
        return 0

    if args.cmd == "plan":
        layers = [x.strip() for x in args.layers.split(",")] if args.layers else None
        rep = plan(exprs, max_arms=args.max_arms, layers=layers,
                   all_slots=args.all_slots)
        _print_plan(rep)
        payload = [a["expression"] for a in rep["arms"]]
        target = args.out or args.json_out
        if target:
            with open(target, "w", encoding="utf-8") as f:
                json.dump(payload, f, ensure_ascii=False, indent=2)
            print(f"\n已写 {len(payload)} 条候选 → {target}")
        return 0

    if args.cmd == "lint":
        rep = lint(exprs)
        print(rep["text"])
        if args.json_out:
            with open(args.json_out, "w", encoding="utf-8") as f:
                json.dump(rep["report"], f, ensure_ascii=False, indent=2)
        return 0 if rep["ok"] else 1

    return 2


if __name__ == "__main__":
    raise SystemExit(_main())
