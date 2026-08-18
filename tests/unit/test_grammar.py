# -*- coding: utf-8 -*-
"""单元测试：wqb.expression.grammar（递归下降表达式解析器）。

此前该核心模块零测试覆盖；本文件补齐解析/标识符抽取/子树提取三条主路径
及全部 ParseError 分支，确保 validator 与 shape classifier 的依赖稳定。
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

import pytest

from wqb.expression.grammar import (
    Node,
    ParseError,
    call_children,
    extract_identifiers,
    parse_expression,
)


# ---------------------------------------------------------------------------
# Node 构造与标志
# ---------------------------------------------------------------------------

def test_leaf_node_is_not_call():
    n = Node("close")
    assert n.is_call is False
    assert n.args == []
    assert n.name == "close"


def test_call_node_is_call_with_args():
    leaf = Node("close")
    n = Node("rank", [leaf])
    assert n.is_call is True
    assert n.args == [leaf]


def test_node_repr_leaf_and_call():
    assert repr(Node("close")) == "close"
    assert repr(Node("rank", [Node("close")])) == "rank(close)"
    assert repr(Node("sub", [Node("a"), Node("b")])) == "sub(a, b)"


# ---------------------------------------------------------------------------
# parse_expression — 正常路径
# ---------------------------------------------------------------------------

def test_parse_plain_identifier():
    n = parse_expression("close")
    assert n.name == "close"
    assert n.is_call is False


def test_parse_single_arg_call():
    n = parse_expression("rank(close)")
    assert n.name == "rank"
    assert n.is_call is True
    assert len(n.args) == 1
    assert n.args[0].name == "close"


def test_parse_two_arg_call():
    n = parse_expression("subtract(rank(close), rank(volume))")
    assert n.name == "subtract"
    assert len(n.args) == 2
    assert n.args[0].name == "rank"
    assert n.args[0].args[0].name == "close"
    assert n.args[1].name == "rank"
    assert n.args[1].args[0].name == "volume"


def test_parse_nested_deep_call():
    n = parse_expression("ts_zscore(divide(close, volume))")
    assert n.name == "ts_zscore"
    assert n.args[0].name == "divide"
    assert n.args[0].args[0].name == "close"
    assert n.args[0].args[1].name == "volume"


def test_parse_rejects_numeric_literal_argument():
    """最小解析器只接受标识符实参；数字字面量（如 decay/window）按设计不进入 AST。

    真实 BRAIN 表达式含数字参数，调用方需在传入前剥离或跳过——本测试锁定此行为，
    防止未来有人误以为 parse_expression 能吞下 ``decay_linear(x, 5)`` 这类表达式。
    """
    with pytest.raises(ParseError):
        parse_expression("decay_linear(close, 5)")
    with pytest.raises(ParseError):
        parse_expression("ts_zscore(rank(close), 20)")


# ---------------------------------------------------------------------------
# parse_expression — 错误分支（ParseError）
# ---------------------------------------------------------------------------

def test_parse_error_trailing_tokens():
    with pytest.raises(ParseError):
        parse_expression("rank(close) extra")


def test_parse_error_missing_close_paren():
    with pytest.raises(ParseError):
        parse_expression("rank(close")


def test_parse_error_leading_paren():
    with pytest.raises(ParseError):
        parse_expression("(close)")


def test_parse_error_numeric_root():
    with pytest.raises(ParseError):
        parse_expression("123")


def test_parse_error_empty():
    with pytest.raises(ParseError):
        parse_expression("")


def test_parse_error_unexpected_char():
    with pytest.raises(ParseError):
        parse_expression("rank@close")


def test_parse_error_trailing_comma():
    with pytest.raises(ParseError):
        parse_expression("foo(bar,)")


def test_parse_error_propagates_value_error():
    assert issubclass(ParseError, ValueError)
    with pytest.raises(ValueError):
        parse_expression("rank(close")


# ---------------------------------------------------------------------------
# extract_identifiers
# ---------------------------------------------------------------------------

def test_extract_identifiers_basic():
    ids = extract_identifiers("subtract(rank(close), rank(volume))")
    assert ids == {"subtract", "rank", "close", "volume"}


def test_extract_identifiers_excludes_numbers_and_punct():
    ids = extract_identifiers("decay_linear(close, 5)")
    assert "close" in ids
    assert "decay_linear" in ids
    assert "5" not in ids


def test_extract_identifiers_underscore_prefix():
    ids = extract_identifiers("_hidden_field")
    assert "_hidden_field" in ids


def test_extract_identifiers_empty():
    assert extract_identifiers("") == set()


# ---------------------------------------------------------------------------
# call_children
# ---------------------------------------------------------------------------

def test_call_children_of_call():
    n = parse_expression("rank(close)")
    kids = call_children(n)
    assert len(kids) == 1
    assert kids[0].name == "close"


def test_call_children_of_leaf_is_empty():
    n = Node("close")
    assert call_children(n) == []
