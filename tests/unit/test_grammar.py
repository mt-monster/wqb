# -*- coding: utf-8 -*-
"""单元测试：wqb.expression.grammar（递归下降表达式解析器）。

覆盖解析/标识符抽取/子树提取三条主路径、全部 ParseError 分支，以及 2026-09-12
补齐的 FASTEXPR 语法：一元负号/负数字面量、``name=value`` kwargs（字符串/数字值）、
中缀比较 + ``&&``/``||`` + 算术运算符——此前这三类合法表达式在 ``_tokenize`` 就抛
ParseError，导致 ghost-audit 硬闸（campaign_intel ghost-audit / MCP operator_audit）
对合法表达式 fail-closed。
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

# 用户报告的三条触发 fail-closed 的合法表达式（PLY validator 已接受）。
EXPR_UNARY_MINUS = "-rank(ts_sum(pv47_spret, 5))"
EXPR_KWARG = 'group_rank(x, bucket(rank(y), range="0,1,0.25"))'
EXPR_COMPARISON = "trade_when(ts_count_nans(x, 5) < 5, rank(x), -1)"


# ---------------------------------------------------------------------------
# Node 构造与标志
# ---------------------------------------------------------------------------

def test_leaf_node_is_not_call():
    n = Node("close")
    assert n.is_call is False
    assert n.args == []
    assert n.name == "close"
    assert n.kind == "ident"


def test_call_node_is_call_with_args():
    leaf = Node("close")
    n = Node("rank", [leaf])
    assert n.is_call is True
    assert n.args == [leaf]
    assert n.kind == "call"


def test_leaf_kind_is_inferred_from_text():
    assert Node("5").kind == "number"
    assert Node("-1").kind == "number"
    assert Node("0.25").kind == "number"
    assert Node('"0,1,0.25"').kind == "string"
    assert Node("'algo1'").kind == "string"
    assert Node("_hidden").kind == "ident"


def test_node_repr_leaf_and_call():
    assert repr(Node("close")) == "close"
    assert repr(Node("rank", [Node("close")])) == "rank(close)"
    assert repr(Node("sub", [Node("a"), Node("b")])) == "sub(a, b)"


def test_node_repr_round_trips_new_forms():
    for expr in (EXPR_UNARY_MINUS, EXPR_KWARG, EXPR_COMPARISON,
                 "a < b && c >= d || e != f", "add(0.4 * rank(a), b - c)"):
        assert repr(parse_expression(expr)) == expr


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


def test_parse_numeric_literal_argument_becomes_number_leaf():
    """数字实参（decay/window）进入 AST 为 number 叶子，不再抛 ParseError。

    此前的最小解析器按设计拒绝数字实参；FASTEXPR 支持后
    ``trade_when(ts_count_nans(x, 5) < 5, ...)`` 这类表达式必须可解析。
    """
    n = parse_expression("decay_linear(close, 5)")
    assert n.args[0].kind == "ident"
    assert n.args[1].kind == "number"
    assert n.args[1].name == "5"
    assert n.args[1].is_call is False
    n = parse_expression("ts_zscore(rank(close), 20)")
    assert n.args[1].name == "20"
    n = parse_expression("winsorize(close, 0.25)")
    assert n.args[1].name == "0.25"


def test_parse_empty_call():
    n = parse_expression("f()")
    assert n.is_call is True
    assert n.args == []


# ---------------------------------------------------------------------------
# 形式 1：一元负号 / 负数字面量
# ---------------------------------------------------------------------------

def test_parse_leading_unary_minus_on_call():
    n = parse_expression(EXPR_UNARY_MINUS)
    assert n.kind == "unary"
    assert n.name == "-"
    assert n.is_call is True  # 有子节点 → 旧式遍历器可继续下钻
    assert len(n.args) == 1
    inner = n.args[0]
    assert inner.kind == "call" and inner.name == "rank"
    assert inner.args[0].name == "ts_sum"
    assert inner.args[0].args[0].name == "pv47_spret"
    assert inner.args[0].args[1].kind == "number"


def test_parse_negative_literal_as_first_argument():
    n = parse_expression("multiply(-1, rank(x))")
    assert n.name == "multiply"
    assert n.args[0].kind == "number"
    assert n.args[0].name == "-1"
    assert n.args[0].is_call is False
    assert n.args[1].name == "rank"


def test_parse_negative_literal_as_last_argument():
    n = parse_expression("trade_when(cond, alpha, -1)")
    assert [a.name for a in n.args] == ["cond", "alpha", "-1"]
    assert n.args[2].kind == "number"


def test_parse_negative_float_and_spaced_sign():
    assert parse_expression("f(x, -0.5)").args[1].name == "-0.5"
    assert parse_expression("f(x, - 3)").args[1].name == "-3"


def test_parse_unary_minus_on_identifier_and_nested():
    n = parse_expression("rank(-close)")
    assert n.args[0].kind == "unary"
    assert n.args[0].args[0].name == "close"
    n = parse_expression("winsorize(-ts_delta(x, 5), std=4)")
    assert n.args[0].kind == "unary"
    assert n.args[0].args[0].name == "ts_delta"


def test_parse_double_negation_folds_number():
    n = parse_expression("f(x, --5)")
    assert n.args[1].kind == "number"
    assert n.args[1].name == "5"


# ---------------------------------------------------------------------------
# 形式 2：name=value 关键字参数
# ---------------------------------------------------------------------------

def test_parse_kwarg_with_string_value():
    n = parse_expression(EXPR_KWARG)
    assert n.name == "group_rank"
    bucket = n.args[1]
    assert bucket.name == "bucket"
    assert bucket.args[0].name == "rank"
    kw = bucket.args[1]
    assert kw.kind == "kwarg"
    assert kw.name == "range"
    assert kw.is_call is True
    assert len(kw.args) == 1
    assert kw.args[0].kind == "string"
    assert kw.args[0].name == '"0,1,0.25"'
    assert kw.args[0].is_call is False


def test_parse_kwarg_with_single_quoted_string_value():
    n = parse_expression("combo_a(alpha, nlength=252, mode='algo1')")
    assert [a.kind for a in n.args] == ["ident", "kwarg", "kwarg"]
    assert n.args[1].name == "nlength" and n.args[1].args[0].name == "252"
    assert n.args[2].name == "mode" and n.args[2].args[0].name == "'algo1'"


def test_parse_kwarg_with_number_value():
    n = parse_expression("winsorize(close, std=4)")
    kw = n.args[1]
    assert kw.kind == "kwarg" and kw.name == "std"
    assert kw.args[0].kind == "number" and kw.args[0].name == "4"


def test_parse_kwarg_with_negative_identifier_and_call_values():
    n = parse_expression("f(x, a=-1, b=True, c=rank(y))")
    assert n.args[1].args[0].name == "-1"
    assert n.args[2].args[0].kind == "ident"
    assert n.args[3].args[0].kind == "call"


def test_parse_string_literal_may_contain_commas_and_parens():
    n = parse_expression('bucket(rank(x), buckets="0.2,0.5,(0.8)")')
    assert n.args[1].args[0].name == '"0.2,0.5,(0.8)"'
    assert len(n.args) == 2


# ---------------------------------------------------------------------------
# 形式 3：中缀比较 / && / || / 算术
# ---------------------------------------------------------------------------

def test_parse_comparison_inside_call():
    n = parse_expression(EXPR_COMPARISON)
    assert n.name == "trade_when"
    cond = n.args[0]
    assert cond.kind == "binop"
    assert cond.name == "<"
    assert cond.is_call is True
    assert cond.args[0].name == "ts_count_nans"
    assert cond.args[0].args[1].name == "5"
    assert cond.args[1].kind == "number" and cond.args[1].name == "5"
    assert n.args[1].name == "rank"
    assert n.args[2].name == "-1"


@pytest.mark.parametrize("op", ["<", "<=", ">", ">=", "==", "!="])
def test_parse_every_comparison_operator(op):
    n = parse_expression(f"rank(close) {op} 0.5")
    assert n.kind == "binop"
    assert n.name == op
    assert n.args[0].name == "rank"
    assert n.args[1].name == "0.5"


def test_parse_logical_and_or_precedence():
    # && 比 || 结合更紧；比较比 && 更紧。
    n = parse_expression("a < b || c >= d && e != f")
    assert n.name == "||"
    assert n.args[0].name == "<"
    assert n.args[1].name == "&&"
    assert n.args[1].args[0].name == ">="
    assert n.args[1].args[1].name == "!="


def test_parse_platform_distribution_probe_expression():
    n = parse_expression("0 < scale_down(close) && scale_down(close) < 0.25")
    assert n.name == "&&"
    assert n.args[0].name == "<" and n.args[0].args[0].name == "0"
    assert n.args[1].name == "<" and n.args[1].args[1].name == "0.25"


def test_parse_infix_arithmetic_precedence():
    n = parse_expression("a + b * c - d")
    assert n.name == "-"
    assert n.kind == "binop"
    assert n.args[0].name == "+"
    assert n.args[0].args[1].name == "*"
    assert n.args[1].name == "d"


def test_parse_scaled_linear_mix_skeleton():
    n = parse_expression("add(0.4*rank(a), 0.3*rank(b))")
    assert n.name == "add"
    assert n.args[0].kind == "binop" and n.args[0].name == "*"
    assert n.args[0].args[0].name == "0.4"
    assert n.args[0].args[1].name == "rank"


def test_parse_binary_minus_vs_unary_minus():
    n = parse_expression("ts_ir(a - b, 20)")
    assert n.args[0].kind == "binop" and n.args[0].name == "-"
    n = parse_expression("f(a - -b)")
    assert n.args[0].kind == "binop"
    assert n.args[0].args[1].kind == "unary"


def test_parse_comparison_binds_looser_than_arithmetic():
    n = parse_expression("a + b < c * d")
    assert n.name == "<"
    assert n.args[0].name == "+"
    assert n.args[1].name == "*"


# ---------------------------------------------------------------------------
# 词法：空白容错
# ---------------------------------------------------------------------------

def test_parse_tolerates_surrounding_and_embedded_whitespace():
    n = parse_expression("  rank(\n close )\t\n")
    assert n.name == "rank" and n.args[0].name == "close"
    assert parse_expression("rank(close) ").name == "rank"


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
    """括号分组仍不支持（保持既有行为）。"""
    with pytest.raises(ParseError):
        parse_expression("(close)")
    with pytest.raises(ParseError):
        parse_expression("(a > b) && (c < d)")


def test_parse_error_numeric_root():
    with pytest.raises(ParseError):
        parse_expression("123")


def test_parse_error_bare_literal_root():
    """负数 / 字符串字面量单独成表达式也不是 alpha。"""
    with pytest.raises(ParseError):
        parse_expression("-1")
    with pytest.raises(ParseError):
        parse_expression('"abc"')


def test_parse_error_empty():
    with pytest.raises(ParseError):
        parse_expression("")


def test_parse_error_unexpected_char():
    with pytest.raises(ParseError):
        parse_expression("rank@close")


@pytest.mark.parametrize("expr", ["a & b", "a | b", "!a", "a ? b : c", "x; y"])
def test_parse_error_unsupported_operator_chars(expr):
    with pytest.raises(ParseError):
        parse_expression(expr)


def test_parse_error_unterminated_string():
    with pytest.raises(ParseError):
        parse_expression('bucket(rank(x), range="0,1')


def test_parse_error_trailing_comma():
    with pytest.raises(ParseError):
        parse_expression("foo(bar,)")


def test_parse_error_kwarg_without_value():
    with pytest.raises(ParseError):
        parse_expression("winsorize(close, std=)")


def test_parse_error_dangling_operators():
    with pytest.raises(ParseError):
        parse_expression("rank(close) <")
    with pytest.raises(ParseError):
        parse_expression("rank(close) && ")
    with pytest.raises(ParseError):
        parse_expression("a = b")


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


def test_extract_identifiers_unary_minus_form():
    assert extract_identifiers(EXPR_UNARY_MINUS) == {"rank", "ts_sum", "pv47_spret"}
    assert extract_identifiers("multiply(-1, rank(x))") == {"multiply", "rank", "x"}
    assert extract_identifiers("trade_when(cond, alpha, -1)") == {"trade_when", "cond", "alpha"}


def test_extract_identifiers_kwarg_form_excludes_kwarg_name_and_string():
    ids = extract_identifiers(EXPR_KWARG)
    assert ids == {"group_rank", "x", "bucket", "rank", "y"}
    assert "range" not in ids
    # 字符串内容不是标识符（ignore="NAN" 不得产出 NAN）
    ids = extract_identifiers('ts_backfill(x, 66, k=1, ignore="NAN")')
    assert ids == {"ts_backfill", "x"}


def test_extract_identifiers_comparison_form():
    assert extract_identifiers(EXPR_COMPARISON) == {"trade_when", "ts_count_nans", "x", "rank"}
    assert extract_identifiers("a < b && c >= d || e == f") == {"a", "b", "c", "d", "e", "f"}
    assert extract_identifiers("add(0.4*rank(a), b - c)") == {"add", "rank", "a", "b", "c"}


def test_extract_identifiers_keeps_equality_operands():
    # ``==`` 不是 kwarg 赋值，两侧标识符都要保留。
    assert extract_identifiers("a == b") == {"a", "b"}


def test_extract_identifiers_still_rejects_garbage():
    with pytest.raises(ParseError):
        extract_identifiers("rank@close")


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


def test_call_children_descend_through_unary_kwarg_and_binop():
    assert call_children(parse_expression(EXPR_UNARY_MINUS))[0].name == "rank"
    kw = parse_expression(EXPR_KWARG).args[1].args[1]
    assert call_children(kw)[0].kind == "string"
    cond = parse_expression(EXPR_COMPARISON).args[0]
    assert [c.name for c in call_children(cond)] == ["ts_count_nans", "5"]
