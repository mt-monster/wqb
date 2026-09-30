# -*- coding: utf-8 -*-
"""模板形状配额（shape quota）：把一波候选表达式归到「形状族」，机检 ra-pipeline 步 4 §4.5.1 的配额准则。

准则（2026-09-28 v2.3，反模板同质化）：每波候选须覆盖 ≥ `MIN_FAMILIES` 个形状族，且 `trade_when` 类条件式占比 ≤ `MAX_TRADE_WHEN_SHARE`。
背景：wave84 / 85 实测——19 条选中仅约 9 个算子形状、`trade_when` 占比 62%；而平台已验证算子 103 个、KB 模板库 141 条零调用。

分类是**启发式**（不是统计推导）：看表达式里出现了哪些「定义架构」的算子。每条表达式只归一个**主形状族**——按下表优先级取第一个命中的
（越能定义整条 alpha 架构的越靠前；`winsorize` / `group_zscore` 这类包在外面的预处理垫底）。谱系「不限于」下表，没命中的归 `plain`
（rank / ts_* 的基础形状）——`plain` 也算一个族，但只占一个名额，不会因为它「什么都没有」而被当成多样性。

| 族 | 命中 | 说明 |
|---|---|---|
| trade_when | `trade_when(` | 条件式（事件门控） |
| if_else | `if_else(` | 趋势状态机（Alpha#9 / #10 形状） |
| arg_extrema | `ts_arg_max(` / `ts_arg_min(` | 时点定位 |
| freshness | `days_from_last_change(` | 新鲜度 |
| ts_corr | `ts_corr(` | 共振 |
| spread | `subtract(rank(A), rank(B))` 或中缀 `rank(A) - rank(B)` | 价差几何（同源、有经济含义才合规，见步 7 §7.7.2） |
| ratio | `divide(` 或中缀 `/` | 比值几何 |
| convexity | `signed_power(` | 凸性 |
| ts_zscore | `ts_zscore(` | 状态 |
| truncation | `winsorize(` / `group_zscore(` | 截断 + 分组标准化 |
| plain | 以上都没有 | 基础形状 |

不做的事：不判合规（比值 / 价差是否满足 §7.7.2 的前提、是否混信号，归闸 5 与人）；不入闸链（闸 6 才是批级多样性的权威，本检查是步 5 前的人可读体检）；
乘法交互 `multiply(主, 辅)` 不列为形状——它是形态库的灰区（`structural-interaction-forms.md`），落到 `plain` 或其它含有的族。
"""
from __future__ import annotations

import re
from collections import Counter
from typing import Any, Dict, Iterable, List, Optional

#: 每波至少覆盖的形状族数。3 = 能打破实测病态「trade_when + 基础形状」两种形状的最小值（wave84 / 85）；准则原文取值，不随波大小缩放。
MIN_FAMILIES = 3
#: `trade_when` 类条件式占比上限。准则原文取值；wave84 / 85 实测 62%（远超）。
MAX_TRADE_WHEN_SHARE = 0.40
#: 单一族占比超过它时只给提示、不改裁决。0.60 与闸 6「收益来源多样性」同口径（同批 > 60% 表达式共享同一 exposure → FAIL，见 gate.py
#: `check_batch_diversity`）——配额达标（≥3 族、trade_when ≤ 40%）不等于形状均衡，这一行让人看见。
DOMINANT_HINT_SHARE = 0.60
#: 候选少于这个数时，「≥ MIN_FAMILIES 个族」在构造上就不可能满足（探针批 / 单信号验证波本来就是 2–3 条同族），裁决记 n/a，不判 FAIL。
MIN_CANDIDATES = 3

PLAIN = "plain"
#: 主形状族的优先级（先命中先归）——见模块文档。
FAMILY_PRIORITY = ("trade_when", "if_else", "arg_extrema", "freshness", "ts_corr", "spread", "ratio", "convexity",
                   "ts_zscore", "truncation", PLAIN)

_CALL = re.compile(r"\b([A-Za-z_][A-Za-z0-9_]*)\s*\(")
_RANK_LIKE = ("rank", "group_rank", "ts_rank", "zscore", "group_zscore")

VERDICT_PASS = "pass"
VERDICT_FAIL = "fail"
VERDICT_NA = "n/a"


# ----------------------------------------------------------------------------- 解析
def _matching_paren(s: str, open_idx: int) -> int:
    """`s[open_idx]` 是 `(`，返回与之配对的 `)` 的下标；不配对返回 -1。"""
    depth = 0
    for i in range(open_idx, len(s)):
        if s[i] == "(":
            depth += 1
        elif s[i] == ")":
            depth -= 1
            if depth == 0:
                return i
    return -1


def _split_args(inner: str) -> List[str]:
    """顶层逗号切分（括号内的逗号不切）。"""
    args, depth, cur = [], 0, []
    for ch in inner:
        if ch == "(":
            depth += 1
        elif ch == ")":
            depth -= 1
        if ch == "," and depth == 0:
            args.append("".join(cur).strip())
            cur = []
        else:
            cur.append(ch)
    args.append("".join(cur).strip())
    return args


def _calls(expr: str) -> List[Dict[str, Any]]:
    """表达式里的全部函数调用：`{"name", "start", "end", "args"}`（配对失败的调用被丢弃）。"""
    out = []
    for m in _CALL.finditer(expr):
        open_idx = m.end() - 1
        close = _matching_paren(expr, open_idx)
        if close < 0:
            continue
        out.append({"name": m.group(1), "start": m.start(), "end": close, "args": _split_args(expr[open_idx + 1:close])})
    return out


def _starts_with_rank_like(arg: str) -> bool:
    m = _CALL.match(arg.strip())
    return bool(m) and m.group(1) in _RANK_LIKE


def _is_spread(expr: str, calls: List[Dict[str, Any]]) -> bool:
    for c in calls:
        if c["name"] == "subtract" and len(c["args"]) >= 2 and all(_starts_with_rank_like(a) for a in c["args"][:2]):
            return True
        if c["name"] in _RANK_LIKE:                                        # 中缀：rank(A) - rank(B)
            tail = expr[c["end"] + 1:].lstrip()
            if tail.startswith("-") and _starts_with_rank_like(tail[1:]):
                return True
    return False


# ----------------------------------------------------------------------------- 分类
def shape_tags(expr: str) -> List[str]:
    """表达式命中的全部形状族（按优先级排序；一个都没命中返回 `["plain"]`）。"""
    e = str(expr or "")
    calls = _calls(e)
    names = {c["name"] for c in calls}
    hit = {
        "trade_when": "trade_when" in names,
        "if_else": "if_else" in names,
        "arg_extrema": bool(names & {"ts_arg_max", "ts_arg_min"}),
        "freshness": "days_from_last_change" in names,
        "ts_corr": "ts_corr" in names,
        "spread": _is_spread(e, calls),
        "ratio": "divide" in names or "/" in e,
        "convexity": "signed_power" in names,
        "ts_zscore": "ts_zscore" in names,
        "truncation": bool(names & {"winsorize", "group_zscore"}),
    }
    tags = [f for f in FAMILY_PRIORITY if hit.get(f)]
    return tags or [PLAIN]


def primary_family(expr: str) -> str:
    """主形状族：优先级最高的命中族。"""
    return shape_tags(expr)[0]


# ----------------------------------------------------------------------------- 配额
def check_quota(expressions: Iterable[str], min_families: int = MIN_FAMILIES,
                max_trade_when_share: float = MAX_TRADE_WHEN_SHARE, min_candidates: int = MIN_CANDIDATES
                ) -> Dict[str, Any]:
    """一波候选 → 配额裁决。

    返回 `{"verdict": pass|fail|n/a, "n", "n_families", "families": {族: 条数}, "trade_when_share",
    "dominant_family", "dominant_share", "issues": [...], "notes": [...]}`。
    `n/a` = 候选不足 `min_candidates`（配额在构造上无法满足，不判）；空串 / 空白表达式不算候选。
    """
    exprs = [str(x).strip() for x in expressions if str(x or "").strip()]
    n = len(exprs)
    fam = Counter(primary_family(x) for x in exprs)
    tw = fam.get("trade_when", 0)
    tw_share = round(tw / n, 4) if n else 0.0
    top, top_n = (fam.most_common(1)[0] if fam else (None, 0))
    res: Dict[str, Any] = {
        "verdict": VERDICT_PASS, "n": n, "n_families": len(fam),
        "families": {f: fam[f] for f in FAMILY_PRIORITY if f in fam},
        "trade_when_share": tw_share, "dominant_family": top,
        "dominant_share": round(top_n / n, 4) if n else 0.0,
        "thresholds": {"min_families": min_families, "max_trade_when_share": max_trade_when_share,
                       "min_candidates": min_candidates},
        "issues": [], "notes": [],
    }
    if n < min_candidates:
        res["verdict"] = VERDICT_NA
        res["notes"].append(f"候选 {n} 条 < {min_candidates}：「≥ {min_families} 个形状族」在构造上无法满足（探针批 / 单信号验证波），不判")
        return res
    if len(fam) < min_families:
        res["issues"].append(f"形状族只有 {len(fam)} 个（{', '.join(res['families'])}），须 ≥ {min_families}")
    if tw_share > max_trade_when_share:
        res["issues"].append(f"trade_when 占比 {tw_share:.0%}（{tw}/{n}），须 ≤ {max_trade_when_share:.0%}")
    if res["issues"]:
        res["verdict"] = VERDICT_FAIL
    elif res["dominant_share"] > DOMINANT_HINT_SHARE:
        res["notes"].append(f"提示（不影响裁决）：{top} 一族占 {res['dominant_share']:.0%}——配额达标不等于形状均衡")
    return res
