# -*- coding: utf-8 -*-
"""表达式骨架签名与同族去重（2026-09-17 新增，#5 生成期骨架去重）。

## 为什么需要
实测（全库 22,024 条）：

| 组 | 条数 | 唯一骨架 | 复用率 | ≥8 条大簇覆盖 |
|---|---|---|---|---|
| 8月 `source=gem` | 1,663 | 121 | 13.7 | 89.2% |
| **近 3 天** | **8,317** | **661** | **12.6** | **89.2%** |

即 **89.2% 的产出落在"同一骨架 ≥8 条"的大簇里** —— 典型的**同族兄弟变体**
（同骨架换字段）。这类变体在平台上 SELF 相关 0.9+，会**自相残杀**（实测
`alphas.self_correlation` 最高 **0.9445**）。

## 与既有 `skeleton_quota` 的关系（互补，不是重复）
既有机制（`_lib/rules.py::issue_contract` + `gate.py` 闸6）管的是**族级配额**——
按 5 分类 `linear_mix / event_gated / group / ratio / single`。
但实测近 3 天 Top3 骨架（`ts_corr` / `subtract(rank,rank)` / `divide`）**分属不同族**，
族级配额**已经满足**，而**结构级复用依然极端**。
本模块补的正是这一层：**签名级**去重。

## 与仓库内其他 6 个"骨架"实现的区别（勿混用）
- `_lib/common.py::skeleton()` —— **5 分类语义族**（配额用）
- `tools/wave_gate.py::_extract_skeleton()` —— 数字→N 但**保留字段名**
  → 无法识别"同骨架换字段"的兄弟变体，**不适合去重**
- `src/wqb/expression/validator.py::_shape_signature()` —— 5 元组形状
- `tools/quality_predict.py::classify_skeleton()` / `tools/ab_test_framework.py::skeleton()`
- `src/wqb/workflow/nodes/gem_wave.py::_auto_skeleton()` —— 曾经的 3 桶子串匹配（已改用本模块）

**本模块的判定口径**：`字段/分组变量 → F`、`数字 → N`、**算子按"后面是否紧跟 `(`"识别**
（不依赖任何算子白名单，故不会因目录漂移而失准）；保留 `( ) ,` 以保存元数结构。

## 用法
    from wqb.expression.skeleton import structural_signature, dedup_by_skeleton
    sig = structural_signature("rank(ts_backfill(close, 66))")   # 'rank ( ts_backfill ( F , N ) )'
    kept, dropped = dedup_by_skeleton(items, max_per_skeleton=3)
"""

from __future__ import annotations

import re
from typing import Any, Dict, List, Optional, Sequence, Tuple

__all__ = [
    "structural_signature",
    "extract_fields",
    "group_axes",
    "dedup_by_skeleton",
    "skeleton_distribution",
    "DEFAULT_MAX_PER_SKELETON",
    "DEFAULT_MAX_SHARE",
]

#: 单个骨架在**一批**内的默认上限（条）
DEFAULT_MAX_PER_SKELETON = 3
#: 单个骨架在**一批**内的默认占比上限（超过则从最大的骨架开始截断）
DEFAULT_MAX_SHARE = 0.25

_TOKEN_RE = re.compile(r"[A-Za-z_][A-Za-z0-9_]*|\d+\.?\d*")
_PUNCT = set("(),")


def structural_signature(expr: str) -> str:
    """表达式 → 结构签名（字段→F、数字→N、算子原样、保留括号与逗号）。

    算子判定用**结构特征**（token 后是否紧跟 `(`），不查算子白名单 ——
    避免与 `data/operators_verified.json` 的目录漂移耦合。

    >>> structural_signature("rank(ts_backfill(close, 66))")
    'rank ( ts_backfill ( F , N ) )'
    >>> structural_signature("rank(ts_backfill(open, 66))") == structural_signature("rank(ts_backfill(close, 66))")
    True
    """
    if not expr:
        return ""
    out: List[str] = []
    i = 0
    n = len(expr)
    while i < n:
        ch = expr[i]
        if ch in _PUNCT:
            out.append(ch)
            i += 1
            continue
        m = _TOKEN_RE.match(expr, i)
        if not m:
            i += 1  # 运算符/空白等一律忽略（不影响结构判定）
            continue
        tok = m.group(0)
        i = m.end()
        if tok[0].isdigit():
            out.append("N")
            continue
        # 向后看一个非空白字符：是 `(` 则为算子，否则为字段/分组变量
        j = i
        while j < n and expr[j] in " \t":
            j += 1
        out.append(tok if (j < n and expr[j] == "(") else "F")
    return " ".join(out)


def extract_fields(expr: str) -> frozenset:
    """提取表达式中的实际数据字段名（用于 L2 去重时区分不同信号）。

    与 :func:`structural_signature` 共享同一套分词逻辑（_TOKEN_RE），
    但**保留**而非替换字段名：

    - 后跟 ``(`` 的 token → 算子（跳过，不计入字段集合）
    - 数字 token → 参数（跳过）
    - 其余 → 字段名（保留）

    典型用例：区分 ``rank(ts_backfill(close,66))`` 与
    ``rank(ts_backfill(open,66))``——两者骨架相同（``rank(ts_backfill(F,N))``），
    但字段不同（``{close}`` vs ``{open}``），是不同信号不应互相去重。

    >>> sorted(extract_fields("rank(ts_backfill(close, 66))"))
    ['close']
    >>> sorted(extract_fields("rank(ts_backfill(open, 66))"))
    ['open']
    >>> extract_fields("rank(ts_backfill(close,66))") == extract_fields("rank(ts_backfill(close, 99))")
    True
    """
    if not expr:
        return frozenset()
    fields: set[str] = set()
    i = 0
    n = len(expr)
    while i < n:
        ch = expr[i]
        if ch in _PUNCT:
            i += 1
            continue
        m = _TOKEN_RE.match(expr, i)
        if not m:
            i += 1  # 运算符/空白等一律忽略
            continue
        tok = m.group(0)
        i = m.end()
        if tok[0].isdigit():
            continue
        # 向后看一个非空白字符：是 `(` 则为算子（跳过），否则为字段
        j = i
        while j < n and expr[j] in " \t":
            j += 1
        if j >= n or expr[j] != "(":
            fields.add(tok)
    return frozenset(fields)


def _expr_of(item: Any, expr_key: str) -> str:
    if isinstance(item, str):
        return item
    if isinstance(item, dict):
        v = item.get(expr_key) or item.get("expression") or item.get("expr") or ""
        return str(v)
    return ""


# ---------------------------------------------------------------------------
# 分组轴（group axis）—— 骨架签名必须补回来的那一维
# ---------------------------------------------------------------------------
#: 分组算子清单。单一事实源 = `wqb.config.OP_FAMILIES["GROUP"]`；下表只补**平台确有
#: 而本仓目录漏收**的算子（漏收会让该算子的分组轴取不到 ⇒ 不同族被误判同族，
#: 所以这里只做加法不做减法）。
_GROUP_OPS_EXTRA = frozenset({"group_backfill"})

#: 分组键（传给 group_* 的字面量）。事实源 = `wqb.expression.atom.GROUPING_KEYS`。
_GROUPING_KEYS_FALLBACK = frozenset("""
industry sector subindustry supersector subsector industrygroup sectorgroup
market exchange country group asset region
""".split())

_KWARG_RE = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*\s*=")
_NUMBER_RE = re.compile(r"^-?\d+(?:\.\d+)?$")
_CALL_HEAD_RE = re.compile(r"^([A-Za-z_][A-Za-z0-9_]*)\s*\(")


def _group_ops() -> frozenset:
    """分组算子集合（config 优先，config 不可用时退回本模块兜底表）。"""
    try:
        from ..config import OP_FAMILIES
        ops = OP_FAMILIES.get("GROUP")
        if ops:
            return frozenset(ops) | _GROUP_OPS_EXTRA
    except Exception:  # pragma: no cover - config 缺失时退化
        pass
    return _GROUP_OPS_EXTRA | frozenset((
        "group_neutralize", "group_rank", "group_zscore", "group_mean", "group_sum",
        "group_max", "group_min", "group_scale", "group_median", "group_count",
        "group_first", "group_last", "group_percentage", "group_std_dev",
        "group_kurtosis", "group_skewness", "group_regression", "group_arg_max",
        "group_arg_min"))


def _grouping_keys() -> frozenset:
    try:
        from .atom import GROUPING_KEYS
        return frozenset(GROUPING_KEYS)
    except Exception:  # pragma: no cover
        return _GROUPING_KEYS_FALLBACK


def _call_args(expr: str, open_paren: int) -> List[str]:
    """`(` 之后的顶层实参（括号平衡切分；不平衡时返回已切出的部分）。"""
    depth, i, n = 1, open_paren + 1, len(expr)
    args: List[str] = []
    cur: List[str] = []
    while i < n and depth > 0:
        ch = expr[i]
        if ch == "(":
            depth += 1
        elif ch == ")":
            depth -= 1
            if depth == 0:
                break
        elif ch == "," and depth == 1:
            args.append("".join(cur))
            cur = []
            i += 1
            continue
        cur.append(ch)
        i += 1
    args.append("".join(cur))
    return args


def _pick_axis(args: List[str]) -> str:
    """从 group_* 的实参里挑出**分组参数**。

    规则（按优先级）：
      1. 位置实参里命中分组键词表（industry / sector / subindustry / market …）→ 取它；
      2. 否则取**最后一个非数字、非字符串**的位置实参（group_backfill(x, group, d) 的
         数字窗口 d 会被跳过 ⇒ 落到 group）；实参本身是调用时取调用文本
         （`densify(pv13)` 这类自定义分组）；
      3. 实参是**嵌套分组算子**时返回空串（轴由内层调用决定，内层会被单独扫描）。
    """
    positional = []
    for a in args:
        s = (a or "").strip()
        if not s or _KWARG_RE.match(s):
            continue
        positional.append(s)
    keys = _grouping_keys()
    for s in positional:
        if s.lower() in keys:
            return s.lower()
    group_ops = _group_ops()
    for s in reversed(positional):
        if _NUMBER_RE.match(s) or s[:1] in ("'", '"'):
            continue
        m = _CALL_HEAD_RE.match(s)
        if m and m.group(1) in group_ops:
            return ""          # 嵌套分组算子 → 轴归内层
        return re.sub(r"\s+", "", s)
    return ""


def group_axes(expr: str) -> Tuple[str, ...]:
    """表达式的**分组轴** → 排序后的 ``("算子:轴", ...)`` 元组。

    为什么必须单独抽（2026-10-23 USA 事故）：
    :func:`structural_signature` 把字段/分组变量一律替换成 ``F``，于是
    ``group_rank(ts_zscore(x, 252), subindustry)`` 与 ``group_rank(ts_zscore(x, 252),
    industry)`` 的主体形状**完全一样** —— 只按主体去重会把两个不同信号族当成同族
    （USA ``d5KzLo7v`` / ``zqrGqVXo`` 即如此被误判 PROD_SIBLING 判死）。

    >>> group_axes("group_rank(x, industry)")
    ('group_rank:industry',)
    >>> group_axes("group_rank(x, industry)") == group_axes("group_rank(x, sector)")
    False
    >>> group_axes("rank(ts_mean(x, 22))")
    ()
    """
    if not expr:
        return ()
    ops = _group_ops()
    out = set()
    for m in re.finditer(r"([A-Za-z_][A-Za-z0-9_]*)\s*\(", expr):
        op = m.group(1)
        if op not in ops:
            continue
        axis = _pick_axis(_call_args(expr, m.end() - 1))
        out.add("%s:%s" % (op, axis) if axis else "%s:?" % op)
    return tuple(sorted(out))


def dedup_by_skeleton(
    items: Sequence[Any],
    max_per_skeleton: int = DEFAULT_MAX_PER_SKELETON,
    max_share: Optional[float] = DEFAULT_MAX_SHARE,
    expr_key: str = "expression",
    signature_sink: Optional[List[Dict[str, Any]]] = None,
) -> Tuple[List[Any], List[Any]]:
    """按结构签名去重，返回 `(保留, 丢弃)`，**保持输入顺序**。

    规则（两条同时施加，取更严者）：
    1. 每个签名最多保留 `max_per_skeleton` 条；
    2. 任一签名占比不超过 `max_share`（None 关闭）。

    选留策略：**保留先出现的**（确定性；GEM 输出通常已按概念优先级排序，
    先出现者代表更高优先级的概念，不引入额外假设）。

    `signature_sink` 给定时，会把每个输入的 `{index, signature, kept}` 追加进去，
    便于调用方做统计/落库。
    """
    total = len(items)
    per_cap = max_per_skeleton if max_per_skeleton and max_per_skeleton > 0 else total
    share_cap = int(total * max_share) if (max_share and total) else total
    cap = max(1, min(per_cap, share_cap)) if total else 0

    seen: Dict[str, int] = {}
    kept: List[Any] = []
    dropped: List[Any] = []
    for idx, item in enumerate(items):
        sig = structural_signature(_expr_of(item, expr_key))
        cnt = seen.get(sig, 0)
        keep = cnt < cap
        if keep:
            seen[sig] = cnt + 1
            kept.append(item)
        else:
            dropped.append(item)
        if signature_sink is not None:
            signature_sink.append({"index": idx, "signature": sig, "kept": keep})
    return kept, dropped


def skeleton_distribution(items: Sequence[Any], expr_key: str = "expression") -> Dict[str, Any]:
    """返回签名分布统计（唯一骨架数 / 复用率 / 最大簇占比 / ≥8 条大簇覆盖）。"""
    sigs: Dict[str, int] = {}
    for it in items:
        s = structural_signature(_expr_of(it, expr_key))
        sigs[s] = sigs.get(s, 0) + 1
    n = len(items)
    if not n:
        return {"n": 0, "unique": 0, "reuse_rate": 0.0,
                "top_share": 0.0, "big_cluster_share": 0.0, "top": []}
    top = sorted(sigs.items(), key=lambda kv: -kv[1])[:5]
    return {
        "n": n,
        "unique": len(sigs),
        "reuse_rate": round(n / len(sigs), 2),
        "top_share": round(top[0][1] / n, 4),
        "big_cluster_share": round(
            sum(v for v in sigs.values() if v >= 8) / n, 4),
        "top": [{"count": c, "share": round(c / n, 4), "signature": s[:120]}
                for s, c in top],
    }
