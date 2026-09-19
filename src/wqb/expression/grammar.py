"""wqb.expression.grammar — minimal recursive-descent expression parser.

Parses BRAIN FASTEXPR-style expressions like
``subtract(rank(close), rank(volume))`` into a small AST used by the validator
and shape classifier. Identifiers are returned as ``Node`` leaves; function
calls as ``Node`` with args.

Accepted syntax (the subset of FASTEXPR that the alpha-expression-verifier PLY
validator accepts, plus ``&&`` / ``||`` which the platform allows):

* operator calls with positional args and ``name=value`` keyword args —
  ``bucket(rank(x), range="0,1,0.25")``, ``winsorize(x, std=4)``;
* numeric literals, signed (``5``, ``0.25``, ``-1``) and string literals
  (``"0,1,0.25"`` or ``'algo1'``);
* prefix unary minus — ``-rank(x)``;
* infix comparison (``< <= > >= == !=``), logical (``&& ||``) and arithmetic
  (``+ - * /``) operators with C-like precedence
  (``||`` < ``&&`` < comparison < ``+ -`` < ``* /`` < unary ``-``).

Not accepted (``ParseError``): parenthesised grouping ``(a + b) * c``, the
ternary ``?:``, ``;``-separated multi-statement expressions, and a bare literal
(``123`` / ``"x"``) as the whole expression.
"""

from __future__ import annotations

import re
from typing import List, Optional, Set

# One token per match; whitespace is skipped by ``_tokenize`` itself.
# Two-character operators must precede their one-character prefixes.
_TOKEN_RE = re.compile(
    r"[A-Za-z_][A-Za-z0-9_]*"       # identifier: operator / field / kwarg name
    r"|\d+(?:\.\d+)?"               # number (sign is a separate '-' token)
    r"|\"[^\"]*\"|'[^']*'"          # string literal, either quote style
    r"|==|!=|<=|>=|&&|\|\|"         # two-char infix operators
    r"|[<>=+\-*/(),]"               # one-char operators and punctuation
)
_NUMBER_RE = re.compile(r"-?\d+(?:\.\d+)?")

_COMPARISON_OPS = frozenset({"==", "!=", "<", "<=", ">", ">="})
# Binary operators from loosest to tightest binding; all left-associative.
_BINARY_LEVELS = (
    frozenset({"||"}),
    frozenset({"&&"}),
    _COMPARISON_OPS,
    frozenset({"+", "-"}),
    frozenset({"*", "/"}),
)


def _is_identifier(tok: str) -> bool:
    return tok[:1].isalpha() or tok[:1] == "_"


def _is_number(tok: str) -> bool:
    return tok[:1].isdigit()


def _is_string(tok: str) -> bool:
    return tok[:1] in ("'", '"')


def _leaf_kind(name: str) -> str:
    if _is_string(name):
        return "string"
    if _NUMBER_RE.fullmatch(name):
        return "number"
    return "ident"


class Node:
    """AST node.

    ``kind`` is one of:

    * ``"call"``   — operator call; ``name`` is the operator, ``args`` the
      positional args followed by any ``kwarg`` nodes.
    * ``"ident"``  — bare identifier leaf (datafield, group var, ``true`` …).
    * ``"number"`` — numeric literal leaf; ``name`` is the literal text with
      the sign folded in (``"-1"``, ``"0.25"``).
    * ``"string"`` — string literal leaf; ``name`` keeps the quotes
      (``'"0,1,0.25"'``).
    * ``"kwarg"``  — keyword argument ``name=value``; ``args == [value]``.
    * ``"unary"``  — prefix operator (``name == "-"``); ``args == [operand]``.
    * ``"binop"``  — infix operator (``name`` in ``< <= > >= == != && || + - * /``);
      ``args == [lhs, rhs]``.

    ``is_call`` is True for every node with children (call/kwarg/unary/binop)
    so tree walkers written against the original two-kind API keep descending;
    test ``kind == "call"`` to match operator calls specifically.
    """

    __slots__ = ("name", "args", "is_call", "kind")

    def __init__(self, name: str, args: Optional[List["Node"]] = None,
                 kind: Optional[str] = None):
        self.name = name
        self.args = args if args is not None else []
        self.is_call = args is not None
        if kind is None:
            kind = "call" if self.is_call else _leaf_kind(name)
        self.kind = kind

    def __repr__(self) -> str:  # pragma: no cover - debugging aid
        if self.kind == "kwarg":
            return f"{self.name}={self.args[0]!r}"
        if self.kind == "unary":
            return f"{self.name}{self.args[0]!r}"
        if self.kind == "binop":
            return f"{self.args[0]!r} {self.name} {self.args[1]!r}"
        if self.is_call:
            return f"{self.name}({', '.join(repr(a) for a in self.args)})"
        return self.name


class ParseError(ValueError):
    """Raised when an expression cannot be parsed."""


def _tokenize(expr: str) -> List[str]:
    tokens: List[str] = []
    pos = 0
    end = len(expr)
    while pos < end:
        if expr[pos].isspace():
            pos += 1
            continue
        m = _TOKEN_RE.match(expr, pos)
        if not m:
            raise ParseError(f"Unexpected character at position {pos}: {expr[pos:]!r}")
        tokens.append(m.group(0))
        pos = m.end()
    return tokens


class _Parser:
    """Precedence-climbing recursive descent over a token list."""

    def __init__(self, tokens: List[str]):
        self._tokens = tokens
        self._pos = 0

    def peek(self, ahead: int = 0) -> Optional[str]:
        i = self._pos + ahead
        return self._tokens[i] if i < len(self._tokens) else None

    def take(self) -> str:
        tok = self._tokens[self._pos]
        self._pos += 1
        return tok

    def remaining(self) -> List[str]:
        return self._tokens[self._pos:]

    def parse_expression(self) -> Node:
        return self._parse_binary(0)

    def _parse_binary(self, level: int) -> Node:
        if level == len(_BINARY_LEVELS):
            return self._parse_unary()
        node = self._parse_binary(level + 1)
        ops = _BINARY_LEVELS[level]
        while self.peek() in ops:
            op = self.take()
            rhs = self._parse_binary(level + 1)
            node = Node(op, [node, rhs], kind="binop")
        return node

    def _parse_unary(self) -> Node:
        if self.peek() != "-":
            return self._parse_primary()
        self.take()
        operand = self._parse_unary()
        if operand.kind == "number":
            # Fold the sign into the literal: ``multiply(-1, x)`` → Node("-1").
            text = operand.name[1:] if operand.name.startswith("-") else "-" + operand.name
            return Node(text)
        return Node("-", [operand], kind="unary")

    def _parse_primary(self) -> Node:
        tok = self.peek()
        if tok is None:
            raise ParseError("Unexpected end of expression")
        if _is_identifier(tok):
            self.take()
            if self.peek() != "(":
                return Node(tok)
            self.take()
            args = self._parse_args()
            if self.peek() != ")":
                raise ParseError("Expected ')'")
            self.take()
            return Node(tok, args)
        if _is_number(tok) or _is_string(tok):
            self.take()
            return Node(tok)
        if tok == "(":
            raise ParseError("Parenthesised grouping is not supported")
        raise ParseError(f"Expected identifier, got {tok!r}")

    def _parse_args(self) -> List[Node]:
        args: List[Node] = []
        if self.peek() == ")":
            return args
        while True:
            args.append(self._parse_arg())
            if self.peek() != ",":
                return args
            self.take()

    def _parse_arg(self) -> Node:
        tok = self.peek()
        if tok is not None and _is_identifier(tok) and self.peek(1) == "=":
            self.take()
            self.take()
            return Node(tok, [self.parse_expression()], kind="kwarg")
        return self.parse_expression()


def parse_expression(expr: str) -> Node:
    """Parse an expression string into an AST ``Node``."""
    parser = _Parser(_tokenize(expr))
    root = parser.parse_expression()
    if parser.remaining():
        raise ParseError(f"Trailing tokens: {parser.remaining()!r}")
    if root.kind in ("number", "string"):
        raise ParseError(f"A bare literal is not an expression: {expr!r}")
    return root


def extract_identifiers(expr: str) -> Set[str]:
    """Return every identifier (operators + fields) in an expression.

    Keyword-argument names (``std`` in ``winsorize(x, std=4)``) and the
    contents of string literals are not operators or fields and are excluded.
    """
    tokens = _tokenize(expr)
    return {t for i, t in enumerate(tokens)
            if _is_identifier(t)
            and not (i + 1 < len(tokens) and tokens[i + 1] == "=")}


def call_children(node: Node) -> List[Node]:
    """Return the children of a node ([] for leaves)."""
    return node.args if node.is_call else []
