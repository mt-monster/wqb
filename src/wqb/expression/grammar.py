"""wqb.expression.grammar — minimal recursive-descent expression parser.

Parses BRAIN-style expressions like ``subtract(rank(close), rank(volume))``
into a small AST used by the validator and shape classifier. Identifiers are
returned as ``Node`` leaves; function calls as ``Node`` with args.
"""

from __future__ import annotations

import re
from typing import List, Optional, Set

_TOKEN_RE = re.compile(r"\s*([A-Za-z_][A-Za-z0-9_]*|\d+(?:\.\d+)?|[(),])")


class Node:
    """AST node: a call (args non-empty) or a leaf identifier/number."""

    __slots__ = ("name", "args", "is_call")

    def __init__(self, name: str, args: Optional[List["Node"]] = None):
        self.name = name
        self.args = args if args is not None else []
        self.is_call = args is not None

    def __repr__(self) -> str:  # pragma: no cover - debugging aid
        if self.is_call:
            return f"{self.name}({', '.join(repr(a) for a in self.args)})"
        return self.name


class ParseError(ValueError):
    """Raised when an expression cannot be parsed."""


def _tokenize(expr: str) -> List[str]:
    tokens: List[str] = []
    pos = 0
    while pos < len(expr):
        m = _TOKEN_RE.match(expr, pos)
        if not m:
            raise ParseError(f"Unexpected character at position {pos}: {expr[pos:]!r}")
        tokens.append(m.group(1))
        pos = m.end()
    return tokens


def parse_expression(expr: str) -> Node:
    """Parse an expression string into an AST ``Node``."""
    tokens = _tokenize(expr)
    pos = [0]

    def peek() -> Optional[str]:
        return tokens[pos[0]] if pos[0] < len(tokens) else None

    def parse_atom() -> Node:
        tok = peek()
        if tok is None:
            raise ParseError("Unexpected end of expression")
        if not (tok[0].isalpha() or tok[0] == "_"):
            raise ParseError(f"Expected identifier, got {tok!r}")
        pos[0] += 1
        if peek() == "(":
            pos[0] += 1
            args: List[Node] = []
            if peek() != ")":
                while True:
                    args.append(parse_atom())
                    nxt = peek()
                    if nxt == ",":
                        pos[0] += 1
                        continue
                    break
            if peek() != ")":
                raise ParseError("Expected ')'")
            pos[0] += 1
            return Node(tok, args)
        return Node(tok)

    root = parse_atom()
    if pos[0] != len(tokens):
        raise ParseError(f"Trailing tokens: {tokens[pos[0]:]!r}")
    return root


def extract_identifiers(expr: str) -> Set[str]:
    """Return every identifier (operators + fields) in an expression."""
    return {t for t in _tokenize(expr)
            if t[0].isalpha() or t[0] == "_"}


def call_children(node: Node) -> List[Node]:
    """Return the call children of a node ([] for leaves)."""
    return node.args if node.is_call else []
