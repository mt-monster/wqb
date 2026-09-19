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


def _expr_of(item: Any, expr_key: str) -> str:
    if isinstance(item, str):
        return item
    if isinstance(item, dict):
        v = item.get(expr_key) or item.get("expression") or item.get("expr") or ""
        return str(v)
    return ""


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
