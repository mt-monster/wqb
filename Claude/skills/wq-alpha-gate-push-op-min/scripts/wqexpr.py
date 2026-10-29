# -*- coding: utf-8 -*-
"""WQ BRAIN alpha 表达式的最小解析器 + 压缩改写规则（只读、零副作用、无第三方依赖）。

语法覆盖：函数调用 `name(a, b, k=v)`、标识符（字段/轴/常量）、数字、括号、
中缀 `+ - * /`、字符串字面量（如 bucket 的 range='0,1,0.05'）。

算子的「调用点数」口径与平台一致：
    OP_CALL_RE = r"\\b([a-z][a-z0-9_]{2,})\\s*\\("      # 名称( 形式的调用点个数
（与 tools/build_gate_prior_from_inventory.py::op_count 同源）
"""
from __future__ import annotations

import re
from collections import Counter
from typing import Any, Dict, List, Optional, Tuple

# ------------------------------------------------------------------ 词法

_TOKEN_RE = re.compile(
    r"""
    (?P<ws>\s+)
  | (?P<num>\d+(?:\.\d+)?)
  | (?P<str>'[^']*'|"[^"]*")
  | (?P<ident>[A-Za-z_][A-Za-z0-9_]*)
  | (?P<op>[(),=+\-*/])
    """,
    re.VERBOSE,
)


class ParseError(ValueError):
    """表达式语法错误。"""


class Node:
    """表达式 AST 节点。

    kind:
      'call'  -> name(args=[...], kwargs={...})
      'ident' -> name（字段名 / 轴名 / 常量名）
      'num'   -> text
      'str'   -> text（含引号）
      'bin'   -> op, left, right
    """

    __slots__ = ("kind", "name", "args", "kwargs", "op", "left", "right", "text")

    def __init__(self, kind: str, **kw: Any) -> None:
        self.kind = kind
        self.name = kw.get("name")
        self.args = kw.get("args") or []
        self.kwargs = kw.get("kwargs") or {}
        self.op = kw.get("op")
        self.left = kw.get("left")
        self.right = kw.get("right")
        self.text = kw.get("text")

    # ---------------------------------------------------------- 序列化
    def to_str(self) -> str:
        if self.kind == "call":
            parts = [a.to_str() for a in self.args]
            parts += [f"{k}={v.to_str()}" for k, v in self.kwargs.items()]
            return f"{self.name}({', '.join(parts)})"
        if self.kind == "ident":
            return self.name
        if self.kind in ("num", "str"):
            return self.text
        if self.kind == "bin":
            return f"{self.left.to_str()} {self.op} {self.right.to_str()}"
        raise ParseError(f"unknown node kind {self.kind}")

    def __repr__(self) -> str:  # pragma: no cover
        return f"<Node {self.to_str()}>"


# ------------------------------------------------------------------ 语法


def _tokenize(text: str) -> List[Tuple[str, str]]:
    out, pos = [], 0
    while pos < len(text):
        m = _TOKEN_RE.match(text, pos)
        if not m:
            raise ParseError(f"无法识别的字符 at {pos}: {text[pos:pos+20]!r}")
        pos = m.end()
        kind = m.lastgroup
        if kind == "ws":
            continue
        out.append((kind, m.group()))
    return out


class _Parser:
    def __init__(self, tokens: List[Tuple[str, str]]) -> None:
        self.toks = tokens
        self.i = 0

    def peek(self) -> Optional[Tuple[str, str]]:
        return self.toks[self.i] if self.i < len(self.toks) else None

    def next(self) -> Tuple[str, str]:
        if self.i >= len(self.toks):
            raise ParseError("表达式意外结束")
        t = self.toks[self.i]
        self.i += 1
        return t

    def expect(self, val: str) -> None:
        t = self.next()
        if t[1] != val:
            raise ParseError(f"期望 {val!r} 实际 {t[1]!r}")

    # expr := term (('+'|'-') term)*
    def parse_expr(self) -> Node:
        node = self.parse_term()
        while True:
            t = self.peek()
            if t and t[0] == "op" and t[1] in ("+", "-"):
                self.next()
                node = Node("bin", op=t[1], left=node, right=self.parse_term())
            else:
                return node

    # term := factor (('*'|'/') factor)*
    def parse_term(self) -> Node:
        node = self.parse_factor()
        while True:
            t = self.peek()
            if t and t[0] == "op" and t[1] in ("*", "/"):
                self.next()
                node = Node("bin", op=t[1], left=node, right=self.parse_factor())
            else:
                return node

    def parse_factor(self) -> Node:
        t = self.next()
        kind, val = t
        if kind == "num":
            return Node("num", text=val)
        if kind == "str":
            return Node("str", text=val)
        if kind == "ident":
            nxt = self.peek()
            if nxt and nxt[0] == "op" and nxt[1] == "(":
                self.next()  # consume '('
                args: List[Node] = []
                kwargs: Dict[str, Node] = {}
                if self.peek() and self.peek()[1] == ")":
                    self.next()
                    return Node("call", name=val, args=args, kwargs=kwargs)
                while True:
                    # 判断是否 kwarg:  ident '='
                    save = self.i
                    is_kw = False
                    if self.peek() and self.peek()[0] == "ident":
                        self.next()
                        if self.peek() and self.peek()[1] == "=":
                            kw_name, is_kw = self.toks[save][1], True
                        else:
                            self.i = save
                    if is_kw:
                        self.next()  # '='
                        kwargs[kw_name] = self.parse_expr()
                    else:
                        args.append(self.parse_expr())
                    nxt = self.next()
                    if nxt[1] == ")":
                        break
                    if nxt[1] != ",":
                        raise ParseError(f"期望 , 或 ) 实际 {nxt[1]!r}")
                return Node("call", name=val, args=args, kwargs=kwargs)
            return Node("ident", name=val)
        if kind == "op" and val == "(":
            node = self.parse_expr()
            self.expect(")")
            return node
        raise ParseError(f"意外的 token {val!r}")


def parse(expr: str) -> Node:
    """把表达式解析成 AST。"""
    p = _Parser(_tokenize(expr))
    node = p.parse_expr()
    if p.peek() is not None:
        raise ParseError(f"尾部有多余 token: {p.peek()}")
    return node


# ------------------------------------------------------------------ 统计


def iter_calls(node: Node):
    """深度优先遍历所有 call 节点。"""
    if node is None:
        return
    if node.kind == "call":
        yield node
        for a in node.args:
            yield from iter_calls(a)
        for v in node.kwargs.values():
            yield from iter_calls(v)
    elif node.kind == "bin":
        yield from iter_calls(node.left)
        yield from iter_calls(node.right)


def iter_idents(node: Node):
    """遍历所有 ident 节点（字段名 / 轴名）。"""
    if node is None:
        return
    if node.kind == "ident":
        yield node
    elif node.kind == "call":
        for a in node.args:
            yield from iter_idents(a)
        for v in node.kwargs.values():
            yield from iter_idents(v)
    elif node.kind == "bin":
        yield from iter_idents(node.left)
        yield from iter_idents(node.right)


def op_count(expr: str) -> int:
    """算子调用点数（平台口径）。"""
    return len(re.findall(r"\b([a-z][a-z0-9_]{2,})\s*\(", expr or ""))


def per_op(node: Node) -> Counter:
    return Counter(c.name for c in iter_calls(node))


def fields_used(node: Node) -> List[str]:
    """粗略列出字段名（ident 里长度 >=4 且未出现在算子名中的）。"""
    ops = {c.name for c in iter_calls(node)}
    seen, out = set(), []
    for ident in iter_idents(node):
        n = ident.name
        if n in ops or n in seen:
            continue
        seen.add(n)
        out.append(n)
    return out


# ------------------------------------------------------------------ 压缩规则

#: (规则 id, 说明, 是否无损)
RULES: Dict[str, str] = {
    "C3.1": "reverse(reverse(x)) -> x",
    "C3.2": "rank(rank(x)) -> rank(x)",
    "C3.3": "group_rank(group_rank(x,g),g) -> group_rank(x,g)",
    "C3.4": "add(x,0)/multiply(x,1)/subtract(x,0) -> x",
    "C3.5": "ts_mean/ts_sum/ts_delay 窗<=1 -> x",
    "C3.7": "abs(abs(x)) -> abs(x)",
    "C3.8": "signed_power(x,1) -> x",
    "C1": "multiply(rank(x),rank(x)) / multiply(a,a) -> rank(x) / a  (重复腿合并)",
    "C10": "winsorize(group_rank(x,ax),std=k) 外层 winsorize 消融测试",
    "C4": "ts_decay_linear/hump(ts_mean(x,a)) -> ts_target_tvr_decay(x,target_tvr=t)",
}

_LOSSLESS = {"C3.1", "C3.2", "C3.3", "C3.4", "C3.5", "C3.7", "C3.8"}


def is_lossless(rule_id: str) -> bool:
    return rule_id in _LOSSLESS


def _is_zero(n: Node) -> bool:
    return n.kind == "num" and float(n.text) == 0.0


def _is_one(n: Node) -> bool:
    return n.kind == "num" and float(n.text) == 1.0


def _same(a: Node, b: Node) -> bool:
    return a.to_str() == b.to_str()


def find_rewrites(node: Node) -> List[Dict[str, Any]]:
    """返回可改写点列表：{rule, where, before, after, op_saved, note}。"""
    out: List[Dict[str, Any]] = []

    def add(rule: str, where: Node, after: str, saved: int, note: str = "") -> None:
        out.append(
            {
                "rule": rule,
                "where": where.to_str(),
                "after": after,
                "op_saved": saved,
                "lossless": is_lossless(rule),
                "note": note or RULES.get(rule, ""),
            }
        )

    def walk(n: Node) -> None:
        if n.kind == "call":
            for a in n.args:
                walk(a)
            for v in n.kwargs.values():
                walk(v)

            # C3.1 / C3.2 / C3.7 单参幂等
            single = {"reverse": "C3.1", "rank": "C3.2", "abs": "C3.7"}
            if n.name in single and len(n.args) == 1:
                inner = n.args[0]
                if inner.kind == "call" and inner.name == n.name:
                    add(single[n.name], n, inner.args[0].to_str(), 2)

            # C3.3 group_rank 同轴
            if n.name == "group_rank" and len(n.args) >= 2:
                inner = n.args[0]
                if (
                    inner.kind == "call"
                    and inner.name == "group_rank"
                    and len(inner.args) >= 2
                    and _same(inner.args[1], n.args[1])
                ):
                    add("C3.3", n, f"group_rank({inner.args[0].to_str()}, {n.args[1].to_str()})", 1)

            # C3.4 恒等元素
            if n.name in ("add", "subtract", "multiply") and len(n.args) == 2:
                a, b = n.args
                if n.name in ("add", "subtract") and _is_zero(b):
                    add("C3.4", n, a.to_str(), 1)
                if n.name == "multiply" and (_is_one(a) or _is_one(b)):
                    keep = b if _is_one(a) else a
                    add("C3.4", n, keep.to_str(), 1)

            # C3.5 窗<=1
            if n.name in ("ts_mean", "ts_sum", "ts_delay") and len(n.args) == 2:
                w = n.args[1]
                if w.kind == "num" and float(w.text) <= 1.0:
                    add("C3.5", n, n.args[0].to_str(), 1)

            # C3.8 signed_power(x,1)
            if n.name == "signed_power" and len(n.args) == 2 and _is_one(n.args[1]):
                add("C3.8", n, n.args[0].to_str(), 1)

            # C1 重复腿（multiply 的两个参数同构）
            if n.name == "multiply" and len(n.args) == 2 and _same(n.args[0], n.args[1]):
                a = n.args[0]
                after = a.to_str() if a.kind != "call" or a.name != "rank" else f"rank({a.args[0].to_str()})"
                add("C1", n, after, 1, "两腿完全同构 ⇒ 冗余；实测常使 S 上升")

            # C10 外层 winsorize（顶层 group_rank 包裹）——只在根附近提示
            if n.name == "winsorize" and n.args and n.args[0].kind == "call" and n.args[0].name == "group_rank":
                add("C10", n, n.args[0].to_str(), 1, "外层 winsorize 消融（std>=3 曾提供 +0.02 S）")

            # C4 双平滑折叠
            if n.name in ("ts_decay_linear", "hump") and n.args and n.args[0].kind == "call":
                inn = n.args[0]
                if inn.name == "ts_mean" and inn.args:
                    add("C4", n, f"ts_target_tvr_decay({inn.args[0].to_str()}, target_tvr=<测>)", 1)

        elif n.kind == "bin":
            walk(n.left)
            walk(n.right)

    walk(node)
    return out


def compress_report(expr: str) -> Dict[str, Any]:
    """一次性给出算子审计 + 改写候选。"""
    node = parse(expr)
    return {
        "expr": expr,
        "op_count": op_count(expr),
        "per_op": dict(per_op(node).most_common()),
        "fields": fields_used(node),
        "rewrites": sorted(find_rewrites(node), key=lambda r: (not r["lossless"], -r["op_saved"])),
    }


__all__ = [
    "parse", "op_count", "per_op", "fields_used",
    "find_rewrites", "compress_report", "Node", "ParseError", "RULES", "is_lossless",
]
