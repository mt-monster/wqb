"""wqb.expression.validator — batch diversity gates and shape classification.

``check_batch`` enforces the diversity gates before a batch may be
dispatched to ``create_multi_simulation``:

1. ``shape_signatures`` — ≥2 distinct shape signatures.
2. ``outer_wrappers`` — ≥2 distinct outermost operators.
3. ``group_vars`` — when group operators appear, ≥2 distinct group vars.
4. ``windows`` — ≥2 distinct lookback windows (when windows are used).
"""

from __future__ import annotations

import re
from typing import Dict, List, Set, Tuple

from wqb.config import GHOST_OPERATORS, SHAPE_CLASSES, get_operator_family
from wqb.expression.grammar import Node, ParseError, parse_expression, extract_identifiers

# Binary combiners whose two operands form a "shape".
_BINARY_COMBINERS = {"subtract", "divide", "add", "multiply", "max", "min"}

# Group variables are not datafields.
_GROUP_VARS = {
    "market", "sector", "subindustry", "industry", "country",
    "exchange", "currency", "quantile",
}

# Operators + constants never count as datafields.
_NON_FIELD_NAMES = _GROUP_VARS | GHOST_OPERATORS | {"true", "false", "nan"}


def _is_operator(name: str) -> bool:
    return get_operator_family(name) != "NONE" or name in GHOST_OPERATORS


def _fields_of(node: Node) -> Set[str]:
    """Collect datafield identifiers from an AST."""
    out: Set[str] = set()
    stack = [node]
    while stack:
        n = stack.pop()
        if n.is_call:
            stack.extend(n.args)
        else:
            name = n.name.lower()
            if name in _NON_FIELD_NAMES:
                continue
            if re.fullmatch(r"\d+(?:\.\d+)?", name):
                continue
            if not _is_operator(name):
                out.add(name)
    return out


def _outer_wrapper(node: Node) -> str:
    return node.name if node.is_call else ""


def _window_bucket(expr: str) -> str:
    """Bucket the largest numeric window used in the expression."""
    numbers = [int(float(m)) for m in re.findall(r"\b(\d+(?:\.\d+)?)\b", expr)]
    if not numbers:
        return "none"
    top = max(numbers)
    if top <= 5:
        return "short"
    if top <= 20:
        return "mid"
    if top <= 60:
        return "long"
    return "xlong"


def _arg_family(arg: Node) -> str:
    """Family of the pre-op wrapping an operand (NONE for raw fields)."""
    if arg.is_call:
        return get_operator_family(arg.name)
    return "NONE"


def _shape_signature(expr: str) -> Tuple[str, str, str, str, str]:
    """5-tuple: (top_op, combiner, fam_a, fam_b, window_bucket)."""
    try:
        root = parse_expression(expr)
    except ParseError:
        return ("INVALID", "", "NONE", "NONE", "none")
    top = root.name if root.is_call else ""
    if root.is_call and root.name in _BINARY_COMBINERS and len(root.args) >= 2:
        fam_a = _arg_family(root.args[0])
        fam_b = _arg_family(root.args[1])
        return (top, root.name, fam_a, fam_b, _window_bucket(expr))
    return (top, "", "NONE", "NONE", _window_bucket(expr))


def classify_shape(expr: str) -> str:
    """Classify a binary-combiner expression into a shape class.

    S0: both operands raw fields. S1: same non-NONE family both sides.
    S5: one side wrapped, other raw. S4: two different families.
    S9: anything else.
    """
    try:
        root = parse_expression(expr)
    except ParseError:
        return "S9"
    if root.is_call and root.name in _BINARY_COMBINERS and len(root.args) >= 2:
        fam_a = _arg_family(root.args[0])
        fam_b = _arg_family(root.args[1])
        if fam_a == "NONE" and fam_b == "NONE":
            return "S0"
        if fam_a != "NONE" and fam_b != "NONE":
            return "S1" if fam_a == fam_b else "S4"
        return "S5"
    return "S9"


def _group_vars_of(node: Node) -> Set[str]:
    out: Set[str] = set()
    stack = [node]
    while stack:
        n = stack.pop()
        if not n.is_call:
            continue
        if n.name.startswith("group_") and len(n.args) >= 2:
            gv = n.args[1]
            if not gv.is_call:
                out.add(gv.name)
        stack.extend(n.args)
    return out


def check_batch(expressions: List[str]) -> Tuple[bool, str, Dict]:
    """Validate a batch of expressions against the 5 diversity gates.

    Returns ``(ok, reason, details)`` where details carries ``gates``,
    ``per_expression`` and ``total``.
    """
    per_expression: List[Dict] = []
    signatures: Set[Tuple] = set()
    wrappers: Set[str] = set()
    group_vars: Set[str] = set()
    windows: Set[str] = set()
    has_group_ops = False

    for expr in expressions:
        try:
            root = parse_expression(expr)
        except ParseError:
            root = None
        fields = _fields_of(root) if root else set()
        if root is not None:
            wrappers.add(_outer_wrapper(root))
            group_vars |= _group_vars_of(root)
            has_group_ops = has_group_ops or any(
                n.name.startswith("group_")
                for n in _iter_calls(root)
            )
        sig = _shape_signature(expr)
        signatures.add(sig)
        if sig[4] != "none":
            windows.add(sig[4])
        per_expression.append({
            "expression": expr,
            "shape_class": classify_shape(expr),
            "shape_signature": [str(x) for x in sig],
            "fields": sorted(fields),
        })

    gates: Dict[str, Dict] = {
        "shape_signatures": {
            "passed": len(signatures) >= 2,
            "detail": f"{len(signatures)} distinct shape signature(s)",
        },
        "outer_wrappers": {
            "passed": len(wrappers) >= 2,
            "detail": f"{len(wrappers)} distinct outer wrapper(s)",
        },
        "group_vars": {
            "passed": (not has_group_ops) or len(group_vars) >= 2,
            "detail": f"group vars: {sorted(group_vars) or 'none'}",
        },
        "windows": {
            "passed": len(windows) >= 2,
            "detail": f"window buckets: {sorted(windows) or 'none'}",
        },
    }

    failed = [name for name, g in gates.items() if not g["passed"]]
    ok = not failed
    reason = "" if ok else "failed gates: " + ", ".join(failed)
    details = {
        "gates": gates,
        "per_expression": per_expression,
        "total": len(expressions),
        "failed_gates": failed,
    }
    return ok, reason, details


def _iter_calls(node: Node):
    stack = [node]
    while stack:
        n = stack.pop()
        if n.is_call:
            yield n
            stack.extend(n.args)


# ---------- P0-2 / P1-2 增强预检（2026-08-31） ----------

# 信号族标签：按字段前缀/数据集类别自动归类（用于同族叠加拦截）
_SIGNAL_FAMILY_PREFIXES = {
    "momentum": ("momentum", "mom", "ts_returns", "ts_delta"),
    "value": ("book", "pe", "pb", "ps", "earnings_yield", "ebitda"),
    "quality": ("roe", "roa", "margin", "profitability", "accrual"),
    "volatility": ("vol", "std", "variance", "beta", "ivol"),
    "liquidity": ("volume", "turnover", "amihud", "liquidity", "adv"),
    "sentiment": ("sentiment", "news", "snt", "nws", "social"),
    "analyst": ("analyst", "anl", "estimate", "revision", "eps"),
}


def _signal_family(fields: Set[str]) -> str:
    """按字段前缀归类信号族（用于同族叠加拦截）。

    长前缀优先匹配（避免 'volume' 被 'vol' 抢先归 volatility）。
    """
    text = " ".join(sorted(fields)).lower()
    # 按前缀长度降序排序，长前缀优先（volume > vol, momentum > mom）
    for fam, prefixes in sorted(_SIGNAL_FAMILY_PREFIXES.items(),
                                key=lambda kv: -max(len(p) for p in kv[1])):
        if any(p in text for p in sorted(prefixes, key=len, reverse=True)):
            return fam
    return "other"


def _jaccard(a: Set[str], b: Set[str]) -> float:
    if not a or not b:
        return 0.0
    return len(a & b) / len(a | b)


def _fields_fallback(expr: str) -> Set[str]:
    """字段提取 fallback：正则直接提取标识符后过滤算子。

    parse_expression/extract_identifiers 都依赖 _tokenize，不支持数字参数
    （ts_delta(close, 10) 的 10）和特殊字符（winsorize(close, std=4) 的 =）。
    本函数用正则直接提取所有标识符，容错任意参数形式。
    """
    idents = re.findall(r"[A-Za-z_][A-Za-z0-9_]*", expr)
    return {i.lower() for i in idents
            if i.lower() not in _NON_FIELD_NAMES and not _is_operator(i.lower())}


def check_combo_orthogonality(expr_a: str, expr_b: str,
                              max_field_jaccard: float = 0.3) -> Tuple[bool, str, Dict]:
    """P0-2 组合前正交性预检：两腿组合发批前判定是否同族叠加。

    判据（IND behavioral_signals + risk70/pv30 实证 prod_corr<0.3 为有效组合）：
    1. 字段集 Jaccard 相似度 <= max_field_jaccard（默认 0.3）
    2. 信号族不同（同族组合 = 同周期/同逻辑叠加，KOR 实证全灭）

    返回 (ok, reason, details)。ok=True 表示正交性达标，允许组合发批。
    """
    # 优先 AST 解析，失败则 fallback 到标识符提取（容错数字参数）
    try:
        fields_a = _fields_of(parse_expression(expr_a))
    except ParseError:
        fields_a = _fields_fallback(expr_a)
    try:
        fields_b = _fields_of(parse_expression(expr_b))
    except ParseError:
        fields_b = _fields_fallback(expr_b)
    fam_a = _signal_family(fields_a)
    fam_b = _signal_family(fields_b)
    jac = _jaccard(fields_a, fields_b)
    details = {
        "fields_a": sorted(fields_a), "fields_b": sorted(fields_b),
        "field_jaccard": round(jac, 3),
        "signal_family_a": fam_a, "signal_family_b": fam_b,
        "max_field_jaccard": max_field_jaccard,
    }
    if fam_a == fam_b and fam_a != "other":
        return False, f"同族叠加拦截：两腿同属信号族 '{fam_a}'（KOR 同周期互组全灭教训）", details
    if jac > max_field_jaccard:
        return False, f"字段集 Jaccard {jac:.2f} > {max_field_jaccard}（正交性不足）", details
    return True, f"正交性达标：信号族 {fam_a}×{fam_b}，字段 Jaccard {jac:.2f}", details


def check_family_ceiling(expressions: List[str],
                         dominant_leg_min_share: float = 2.0 / 3.0) -> Tuple[bool, str, Dict]:
    """P1-2 家族扩展天花板预检：主导腿不变时任何快腿微调与母配方 SELF≥0.9。

    判据（wave94/95/98/104 四次实证）：
    - 提取每条表达式的主导腿（出现频次最高的字段）
    - 若某字段在 >= dominant_leg_min_share（默认 2/3）的表达式中都是主导腿，
      则该批属同族微调，标记高 SELF 风险，建议跳过仿真节省配额。

    返回 (ok, reason, details)。ok=True 表示无天花板风险，可发批。
    """
    if len(expressions) < 2:
        return True, "批次过小，跳过天花板检测", {"total": len(expressions)}
    # 统计每条表达式的主导腿（第一个字段，近似主导腿）
    # 优先 AST 解析，失败则 fallback 到标识符提取（容错数字参数）
    dominant_legs: List[str] = []
    for expr in expressions:
        fields: Set[str] = set()
        try:
            fields = _fields_of(parse_expression(expr))
        except ParseError:
            fields = _fields_fallback(expr)
        dominant_legs.append(sorted(fields)[0] if fields else "")
    from collections import Counter
    counts = Counter(d for d in dominant_legs if d)
    if not counts:
        return True, "无法提取主导腿，跳过天花板检测", {"total": len(expressions)}
    top_leg, top_n = counts.most_common(1)[0]
    share = top_n / len(expressions)
    details = {
        "dominant_leg": top_leg, "dominant_count": top_n,
        "total": len(expressions), "share": round(share, 3),
        "threshold": round(dominant_leg_min_share, 3),
        "all_legs": dict(counts),
    }
    if share >= dominant_leg_min_share:
        return False, (
            f"家族扩展天花板：主导腿 '{top_leg}' 占 {share:.0%}（>= {dominant_leg_min_share:.0%}），"
            f"与母配方 SELF 相关必然≥0.9（wave94/95/98/104 实证），建议跳过仿真"
        ), details
    return True, f"主导腿占比 {share:.0%} < {dominant_leg_min_share:.0%}，无天花板风险", details


# ---------- P0-A 方向一致性预检（2026-08-31） ----------

# 显式翻转结构正则（识别表达式符号倾向）：
#   reverse(x) / multiply(-1, x) / multiply(x, -1) / divide(-1, x) / 前缀负算子
# 注意：len 是偶数时翻转相互抵消（负负得正）。
_FLIP_PATTERNS = (
    r"reverse\s*\(",
    r"multiply\s*\(\s*-\s*1(?:\.0+)?\s*,",
    r"multiply\s*\([^,]+,\s*-\s*1(?:\.0+)?\s*\)",
    r"divide\s*\(\s*-\s*1(?:\.0+)?\s*,",
    r"(?<![\w)])-\s*(?:rank|zscore|ts_|winsorize|signed_power|group_rank|group_zscore|subtract|add|multiply|divide)\s*\(",
)
_FLIP_RX = [re.compile(p) for p in _FLIP_PATTERNS]


def _expr_sign(expr: str) -> int:
    """检测表达式显式符号倾向：-1 = 含奇数个翻转结构，+1 = 无翻转/偶数个翻转。

    注意：只能识别显式翻转（reverse/乘负/前缀负），ts_delta 等方向由数据决定
    不在此列；此处仅作组合前的静态参考（真正的方向以 IS 回测 Sharpe 符号为准）。
    """
    n_flip = sum(len(rx.findall(expr)) for rx in _FLIP_RX)
    return -1 if n_flip % 2 == 1 else 1


def check_combo_direction(expr_a: str, expr_b: str,
                          sharpe_a: float = None, sharpe_b: float = None) -> Tuple[bool, str, Dict]:
    """P0-A 组合前方向一致性预检：两腿方向相反会互相抵消。

    两级检测：
    1. 静态符号倾向（无回测数据时）：检测显式翻转结构差异——一腿翻转一腿常规
       且字段集高度重叠时提示风险（WARN 不阻断，静态方向不可定）。
    2. 回测后方向检查（传入 sharpe_a/sharpe_b）：两腿 IS Sharpe 符号相反
       → 确定性抵消风险，建议对负腿乘以 -1 翻转后再组合。

    返回 (ok, reason, details)。ok=False 仅当回测符号相反（有数据可判定）；
    静态翻转差异为 WARN 提示，不阻断。
    """
    sign_a, sign_b = _expr_sign(expr_a), _expr_sign(expr_b)
    # 静态翻转差异：一腿翻转一腿常规，且字段集有重叠 → 提示（不阻断）
    details: Dict = {
        "static_sign_a": sign_a, "static_sign_b": sign_b,
        "static_flip_conflict": sign_a != sign_b,
        "has_is_results": sharpe_a is not None and sharpe_b is not None,
    }
    if sharpe_a is not None and sharpe_b is not None:
        details["sharpe_a"] = sharpe_a
        details["sharpe_b"] = sharpe_b
        if (sharpe_a > 0 > sharpe_b) or (sharpe_b > 0 > sharpe_a):
            neg_leg = "A" if sharpe_a < 0 else "B"
            return False, (
                f"方向抵消风险：Sharpe 符号相反（A={sharpe_a:.2f}, B={sharpe_b:.2f}），"
                f"组合将互相抵消；建议对{neg_leg}腿乘以 -1 翻转后再组合"
            ), details
        return True, f"方向一致：Sharpe 同号（A={sharpe_a:.2f}, B={sharpe_b:.2f}），可组合", details
    # 无回测数据：静态提示
    if sign_a != sign_b:
        return True, (
            f"静态翻转结构差异（A={sign_a:+d}, B={sign_b:+d}）：一腿显式翻转一腿常规，"
            f"若字段经济意义同向建议先翻转对齐；实际方向以 IS Sharpe 为准（未传入，不阻断）"
        ), details
    return True, f"静态符号一致（A={sign_a:+d}, B={sign_b:+d}）", details
