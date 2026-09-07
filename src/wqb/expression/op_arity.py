# -*- coding: utf-8 -*-
"""wqb.expression.op_arity — 算子元数 + 命名参数闸（catalog 驱动）。

事故背景（2026-09-07）：``hump(x, 0.005)`` 通过了本地语法闸（wave_gate 报
"语法 8/8 PASS"），平台却回 ``Invalid number of inputs : 2, should be exactly
1 input(s).`` —— 2 条畸形表达式让平台 **CANCEL 掉整个 8 条 multisim**
（id 2Vt1RwZw4KGcajcZxpWLyW），浪费 8 个槽位而不是 2 个。

根因不是"参数个数写错"，而是 **命名参数被当成位置参数**：catalog 签名
``hump(x, hump = 0.01)`` 里的 ``=`` 标记 ``hump`` 为 **命名参数**，只能写成
``hump(x, hump=0.005)``；对照 ``ts_decay_linear(x, d, dense = false)`` —— ``d``
是位置参数（无 ``=``），只有 ``dense`` 是命名参数。

本模块把这条规则从"逐个算子打补丁"（gate.py 闸4 里硬编码的 quantile arity、
``_op_signatures.py`` 里手写的 UNARY_OPS/BINARY_OPS）升级为 **从 catalog 自动
推导的通用闸**：

    catalog definition ──parse──> OpSignature(positional / named / variadic)
    表达式 ──scan 调用点──> 逐个 call site 比对 ──> 违规即 FAIL

签名推导规则（从 102 条 live definition 实证得出）：

* 无 ``=`` 的形参          → 位置参数（必填），如 ``ts_mean(x, d)`` 的 x、d
* ``name = <字面量>``      → **命名参数**（named-only），如 ``hump(x, hump=0.01)``、
  ``rank(x, rate=2)``、``quantile(x, driver=gaussian, sigma=1.0)``
* ``name = <单字母占位符>`` → 位置可选参数，如 ``ts_backfill(x, lookback = d, k=1)``
  的 ``lookback``（``d`` 是"你来填天数"的占位符而非默认值；仓库里
  ``ts_backfill(x, 120)`` 这种位置写法有 2800+ 处历史实证，绝不能误杀）
* ``...`` / ``..``         → 变参，位置参数无上限，如 ``max(x, y, ..)``

**未知算子一律放行**：幽灵算子由 :mod:`wqb.expression.operator_audit` 负责，
本闸只管它在 catalog 里认得的算子，避免双重误报。

数据源优先级：

1. ``$WQB_OPERATORS_CATALOG``
2. ``docs/reference/operators_catalog.json``（``get_operators`` 的实时快照，权威；
   随仓库版本化，刷新走 ``tools/refresh_operator_catalog.py``）
3. ``research-data/operators_platform_*.json``（本机抓的历史快照，未入库）
4. ``docs/reference/operators_notes.md``（离线兜底；只覆盖 REGULAR 域 77 个算子，
   与 catalog 逐条比对签名零差异，缺的 17 个全是 COMBO 域 reduce_*/combo_a）

CLI::

    python -m wqb.expression.op_arity "hump(close, 0.005)" "rank(close, rate=2)"
"""

from __future__ import annotations

import glob
import json
import os
import re
from dataclasses import dataclass, field
from functools import lru_cache
from typing import Dict, Iterable, List, Optional, Sequence, Tuple

__all__ = [
    "OpSignature",
    "ArityError",
    "parse_definition",
    "load_signatures",
    "iter_call_sites",
    "check_expression",
    "check_expressions",
    "ensure_safe_for_dispatch",
    "format_report",
]

_REPO_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__)))))

#: 引号字符（平台文档里混用直引号与中文弯引号，例如 kth_element 的 ignore=“NaN”）
_QUOTES = '"\'“”‘’'
_CLOSING_QUOTES = '”’'
_OPENING_QUOTES = '“‘'

#: 单字母占位符（``lookback = d`` 里的 d 表示"你来填"，不是默认值）
_PLACEHOLDER_RE = re.compile(r"^[a-z]$")

#: 命名实参：``name=value``（排除 ``==`` ``!=`` ``>=`` ``<=``）
_NAMED_ARG_RE = re.compile(r"^\s*([A-Za-z_][A-Za-z0-9_]*)\s*=(?!=)")

#: 调用点：标识符紧跟左括号
_CALL_SITE_RE = re.compile(r"(?<![A-Za-z0-9_.])([A-Za-z_][A-Za-z0-9_]*)\s*\(")

# ---------------------------------------------------------------------------
# 实证覆盖：catalog definition 表达不了 / 写成中缀式的算子。
# 每条都必须给出理由——这里是唯一允许手写签名的地方。
# ---------------------------------------------------------------------------

#: definition 只写 ``(x, y, filter=false)``，但 description 明写 "two or more
#: inputs"（``multiply`` 的 definition 里有 ``...``，add/subtract 没有）。
_VARIADIC_BY_DESCRIPTION = {"add", "subtract", "multiply"}

#: 比较/逻辑算子的 definition 是中缀式（``input1 < input2``），推不出函数签名；
#: 但表达式里常写成函数调用 ``less(a, b)``，补上二元签名闭掉这个洞。
_INFIX_BINARY_OPS = {
    "less", "greater", "equal", "not_equal", "less_equal", "greater_equal",
}


class ArityError(ValueError):
    """算子元数 / 命名参数违规。"""


@dataclass(frozen=True)
class OpSignature:
    """一个算子的调用契约。

    ``min_positional``/``max_positional`` 是位置参数的闭区间（variadic 时上界
    为 ``None``）；``named`` 是允许出现的命名参数集合。
    """

    name: str
    positional: Tuple[str, ...] = ()
    min_positional: int = 0
    max_positional: Optional[int] = 0
    named: Tuple[str, ...] = ()
    variadic: bool = False
    definition: str = ""

    @property
    def named_set(self) -> frozenset:
        return frozenset(self.named)

    def describe(self) -> str:
        pos = ", ".join(self.positional) or "-"
        nm = ", ".join(f"{n}=" for n in self.named) or "-"
        tail = "+变参" if self.variadic else ""
        return f"{self.name}: 位置[{pos}]{tail} 命名[{nm}]"


# ---------------------------------------------------------------------------
# 文本切分工具
# ---------------------------------------------------------------------------

def _split_top_level(text: str, sep: str = ",") -> List[str]:
    """按顶层 ``sep`` 切分，跳过括号内与引号内的分隔符。"""
    parts: List[str] = []
    buf: List[str] = []
    depth = 0
    quote = ""
    for ch in text:
        if quote:
            buf.append(ch)
            # 弯引号成对但字符不同，任一右引号都收尾
            if ch == quote or (quote in _OPENING_QUOTES and ch in _CLOSING_QUOTES):
                quote = ""
            continue
        if ch in _QUOTES:
            quote = ch
            buf.append(ch)
            continue
        if ch in "([{":
            depth += 1
        elif ch in ")]}":
            depth -= 1
        if ch == sep and depth == 0:
            parts.append("".join(buf))
            buf = []
            continue
        buf.append(ch)
    parts.append("".join(buf))
    return parts


def _match_paren(text: str, open_idx: int) -> int:
    """返回 ``text[open_idx] == '('`` 对应右括号的下标；不匹配返回 -1。"""
    depth = 0
    quote = ""
    for i in range(open_idx, len(text)):
        ch = text[i]
        if quote:
            if ch == quote or (quote in _OPENING_QUOTES and ch in _CLOSING_QUOTES):
                quote = ""
            continue
        if ch in _QUOTES:
            quote = ch
            continue
        if ch == "(":
            depth += 1
        elif ch == ")":
            depth -= 1
            if depth == 0:
                return i
    return -1


# ---------------------------------------------------------------------------
# definition → OpSignature
# ---------------------------------------------------------------------------

def _is_placeholder(value: str) -> bool:
    """``lookback = d`` 里的 ``d``：占位符（可位置传参），不是字面默认值。"""
    return bool(_PLACEHOLDER_RE.match(value.strip()))


def _parse_one_form(params_raw: str):
    """解析单个 ``name(...)`` 形式，返回 (positional, named, variadic, optional_from)。"""
    positional: List[str] = []
    named: List[str] = []
    variadic = False
    optional_from: Optional[int] = None

    if not params_raw.strip():
        return positional, named, variadic, optional_from

    for raw in _split_top_level(params_raw):
        part = raw.strip()
        if not part:
            continue
        # 变参标记 "..." / ".."，可能贴在形参后面（``min(x, y ..)``）
        if ".." in part:
            variadic = True
            part = part.replace("...", "").replace("..", "").strip()
            if not part:
                continue
        m = _NAMED_ARG_RE.match(part)
        if m:
            key = m.group(1)
            value = part[m.end():].strip()
            if _is_placeholder(value):
                # 占位符默认值 → 仍是位置参数，但可省略
                if optional_from is None:
                    optional_from = len(positional)
                positional.append(key)
            else:
                named.append(key)
            continue
        # 裸形参：位置且必填
        positional.append(part)
    return positional, named, variadic, optional_from


def parse_definition(name: str, definition: str) -> Optional[OpSignature]:
    """把 catalog 的 ``definition`` 串解析成 :class:`OpSignature`。

    一个 definition 可能含多种写法（``bucket`` 有 ``range=`` 与 ``buckets=``
    两式，中间用 "or" 分行）；此时取所有形式的**并集**（命名参数取并、位置
    参数下界取最小），保证任一合法写法都不被误杀。
    """
    if not definition:
        return None
    ident = re.escape(name)
    forms = []
    for m in re.finditer(rf"(?<![A-Za-z0-9_]){ident}\s*\(", definition):
        open_idx = definition.index("(", m.end() - 1)
        close_idx = _match_paren(definition, open_idx)
        if close_idx < 0:
            continue
        forms.append(_parse_one_form(definition[open_idx + 1:close_idx]))
    if not forms:
        return None

    positional = max((f[0] for f in forms), key=len)
    # 命名参数保持 definition 里的声明顺序（不能排序：报错提示要按位置对号入座，
    # tail(x, lower, upper, newval) 排序后会给出 lower/newval/upper 的错误建议）
    named: List[str] = []
    for form in forms:
        for n in form[1]:
            if n not in named:
                named.append(n)
    variadic = any(f[2] for f in forms) or name in _VARIADIC_BY_DESCRIPTION

    # 下界：所有形式里必填位置参数最少的那个
    mins = [opt_from if opt_from is not None else len(pos)
            for pos, _nm, _va, opt_from in forms]
    min_positional = min(mins) if mins else 0
    max_positional = None if variadic else len(positional)
    return OpSignature(
        name=name,
        positional=tuple(positional),
        min_positional=min_positional,
        max_positional=max_positional,
        named=tuple(named),
        variadic=variadic,
        definition=definition.strip(),
    )


# ---------------------------------------------------------------------------
# catalog 加载
# ---------------------------------------------------------------------------

def _catalog_candidates() -> List[str]:
    cands = [os.environ.get("WQB_OPERATORS_CATALOG"),
             os.path.join(_REPO_ROOT, "docs", "reference", "operators_catalog.json"),
             os.path.join(_REPO_ROOT, "data", "operators_catalog.json")]
    cands.extend(sorted(glob.glob(os.path.join(
        _REPO_ROOT, "research-data", "operators_platform_*.json")), reverse=True))
    return [c for c in cands if c]


def _iter_catalog_entries(payload) -> Iterable[dict]:
    """兼容 MCP 原样输出 / ``{"results": [...]}`` / 裸 list 三种形态。"""
    if isinstance(payload, dict):
        for key in ("result", "results", "operators"):
            if key in payload:
                yield from _iter_catalog_entries(payload[key])
                return
        return
    if isinstance(payload, list):
        for item in payload:
            if isinstance(item, dict) and "name" in item:
                yield item


def _load_from_catalog(path: str) -> Dict[str, OpSignature]:
    with open(path, encoding="utf-8") as f:
        payload = json.load(f)
    out: Dict[str, OpSignature] = {}
    for entry in _iter_catalog_entries(payload):
        name = str(entry.get("name") or "").strip()
        if not name:
            continue
        sig = parse_definition(name, entry.get("definition") or "")
        if sig is not None:
            out[name] = sig
    return out


def _load_from_notes(path: str) -> Dict[str, OpSignature]:
    """兜底：解析 ``docs/reference/operators_notes.md`` 的制表符表格。

    行形如 ``Category<TAB>definition<TAB>Count<TAB>Scope<TAB>Level``；算子名取
    definition 里第一个 ``name(`` 的标识符。
    """
    out: Dict[str, OpSignature] = {}
    with open(path, encoding="utf-8") as f:
        for line in f:
            cols = [c.strip() for c in line.rstrip("\n").split("\t")]
            if len(cols) < 2 or cols[0].lower() in ("category", ""):
                continue
            definition = cols[1]
            m = _CALL_SITE_RE.search(definition)
            if not m:
                continue
            sig = parse_definition(m.group(1), definition)
            if sig is not None:
                out.setdefault(m.group(1), sig)
    return out


def _apply_overrides(sigs: Dict[str, OpSignature]) -> Dict[str, OpSignature]:
    for name in _INFIX_BINARY_OPS:
        if name not in sigs:
            sigs[name] = OpSignature(
                name=name, positional=("input1", "input2"),
                min_positional=2, max_positional=2,
                definition=f"{name}(input1, input2)  # 中缀式补签名",
            )
    return sigs


@lru_cache(maxsize=4)
def load_signatures(path: Optional[str] = None) -> Dict[str, OpSignature]:
    """加载算子签名表；``path`` 为空时按优先级自动探测。"""
    paths = [path] if path else _catalog_candidates()
    for p in paths:
        if p and os.path.isfile(p):
            sigs = _load_from_catalog(p)
            if sigs:
                return _apply_overrides(sigs)
    notes = os.path.join(_REPO_ROOT, "docs", "reference", "operators_notes.md")
    if os.path.isfile(notes):
        sigs = _load_from_notes(notes)
        if sigs:
            return _apply_overrides(sigs)
    return _apply_overrides({})


# ---------------------------------------------------------------------------
# 表达式扫描
# ---------------------------------------------------------------------------

@dataclass
class CallSite:
    """表达式里的一个 ``name(...)`` 调用点。"""

    name: str
    positional: List[str] = field(default_factory=list)
    named: List[Tuple[str, str]] = field(default_factory=list)
    raw: str = ""


def iter_call_sites(expr: str) -> List[CallSite]:
    """扫描表达式里所有 ``name(...)`` 调用点（含嵌套）。

    不建完整 AST：逐个调用点独立取平衡括号内容再按顶层逗号切分，因此天然
    容忍 ``+ - * /``、比较符、``;`` 多语句、字符串常量与任意嵌套。
    """
    sites: List[CallSite] = []
    for m in _CALL_SITE_RE.finditer(expr):
        open_idx = m.end() - 1
        close_idx = _match_paren(expr, open_idx)
        if close_idx < 0:
            continue
        inner = expr[open_idx + 1:close_idx]
        site = CallSite(name=m.group(1), raw=inner)
        if inner.strip():
            for raw_arg in _split_top_level(inner):
                arg = raw_arg.strip()
                if not arg:
                    continue
                nm = _NAMED_ARG_RE.match(arg)
                if nm:
                    site.named.append((nm.group(1), arg[nm.end():].strip()))
                else:
                    site.positional.append(arg)
        sites.append(site)
    return sites


def check_expression(expr: str,
                     signatures: Optional[Dict[str, OpSignature]] = None
                     ) -> List[str]:
    """校验单条表达式的算子元数 + 命名参数；返回错误列表（空 = PASS）。

    catalog 里没有的算子一律跳过（幽灵算子归 operator_audit 管），本闸不
    制造双重误报。
    """
    sigs = signatures if signatures is not None else load_signatures()
    errors: List[str] = []
    for site in iter_call_sites(expr):
        sig = sigs.get(site.name)
        if sig is None:
            continue
        n_pos = len(site.positional)

        # 1) 位置参数过多——平台的 "Invalid number of inputs" 就是这一条
        if sig.max_positional is not None and n_pos > sig.max_positional:
            msg = (f"[ARITY] {site.name} 只接受 {sig.max_positional} 个位置参数，"
                   f"实际 {n_pos} 个（平台报 \"Invalid number of inputs : {n_pos}, "
                   f"should be exactly {sig.max_positional} input(s).\"）")
            if sig.named:
                overflow = site.positional[sig.max_positional:]
                # 多出的个数与命名参数个数一致时才敢逐个对号入座；否则只列可选项，
                # 免得给出 quantile(x, 0.5) -> "driver=0.5" 这种误导性建议。
                if len(overflow) == len(sig.named):
                    hint = ", ".join(f"{k}={v}"
                                     for k, v in zip(sig.named, overflow))
                    msg += f"；多出的参数是命名参数，应写作 {hint}"
                else:
                    hint = ", ".join(f"{k}=" for k in sig.named)
                    msg += f"；多出的参数只能用命名参数传（可用: {hint}）"
            msg += f"　签名: {sig.definition}"
            errors.append(msg)
        # 2) 位置参数过少
        elif n_pos < sig.min_positional:
            errors.append(
                f"[ARITY] {site.name} 至少需要 {sig.min_positional} 个位置参数，"
                f"实际 {n_pos} 个　签名: {sig.definition}")

        # 3) 命名参数不存在 / 与位置参数重名 / 重复
        seen = set()
        for key, _value in site.named:
            if key not in sig.named_set:
                if key in sig.positional:
                    errors.append(
                        f"[KWARG] {site.name} 的 '{key}' 是位置参数，不能写成 "
                        f"'{key}='　签名: {sig.definition}")
                else:
                    allowed = ", ".join(sig.named) or "无"
                    errors.append(
                        f"[KWARG] {site.name} 没有命名参数 '{key}'（可用: {allowed}）"
                        f"　签名: {sig.definition}")
            elif key in seen:
                errors.append(f"[KWARG] {site.name} 的命名参数 '{key}' 重复")
            seen.add(key)
    return errors


def check_expressions(expressions: Sequence,
                      signatures: Optional[Dict[str, OpSignature]] = None
                      ) -> Dict:
    """批量校验；返回 ``{ok, total, passed, items:[{id, expression, errors}]}``。

    ``expressions`` 元素可以是字符串，也可以是 ``(id, expr)`` 二元组。
    """
    sigs = signatures if signatures is not None else load_signatures()
    items: List[Dict] = []
    for i, item in enumerate(expressions, 1):
        if isinstance(item, (tuple, list)) and len(item) == 2:
            cid, expr = item
        else:
            cid, expr = i, item
        errs = check_expression(str(expr), sigs)
        items.append({"id": cid, "expression": expr,
                      "valid": not errs, "errors": errs})
    passed = sum(1 for it in items if it["valid"])
    return {"ok": passed == len(items), "total": len(items),
            "passed": passed, "items": items,
            "signatures_loaded": len(sigs)}


def format_report(report: Dict) -> str:
    lines = [f"[arity] {report['passed']}/{report['total']} PASS "
             f"(签名表 {report['signatures_loaded']} 个算子)"]
    for it in report["items"]:
        if it["valid"]:
            continue
        lines.append(f"  FAIL {it['id']}: {it['expression']}")
        lines.extend(f"        {e}" for e in it["errors"])
    return "\n".join(lines)


def ensure_safe_for_dispatch(expressions: Sequence[str]) -> None:
    """发批前硬闸：任一表达式元数违规即抛 :class:`ArityError`。"""
    report = check_expressions(expressions)
    if not report["ok"]:
        bad = [it for it in report["items"] if not it["valid"]]
        detail = "; ".join(f"{it['expression']} -> {it['errors']}" for it in bad)
        raise ArityError(f"{len(bad)} 条表达式元数违规: {detail}")


def _main(argv: List[str]) -> int:
    if not argv:
        sigs = load_signatures()
        print(f"签名表: {len(sigs)} 个算子")
        for name in sorted(sigs):
            print("  " + sigs[name].describe())
        return 0
    report = check_expressions(argv)
    print(format_report(report))
    return 0 if report["ok"] else 1


if __name__ == "__main__":  # pragma: no cover
    import sys

    raise SystemExit(_main(sys.argv[1:]))
