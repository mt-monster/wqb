# -*- coding: utf-8 -*-
"""vector_wrap.py - VECTOR(event) 字段裸用的通用自动修复。

平台规则：VECTOR 类型字段必须先经 vec_* 聚合算子转成标量(MATRIX)，
才能被 ts_*/divide/subtract/add/rank 等常规算子使用，否则平台报
"does not support event inputs"（HTTP 400）。

本模块提供幂等重写器 wrap_naked_vectors()：
  - 扫描表达式中所有 VECTOR 字段；
  - 若某字段出现位置的最内层函数包裹不是 vec_*，则自动裹上聚合算子；
  - 已正确包裹的字段保持不变（幂等，可重复调用）。

聚合算子选择：
  - 字段名含 count/sum/vol(量)/num 等"计数/求和"语义 -> vec_sum
  - 其余默认 -> vec_avg（均值，最稳健、量纲中立）

被 gate.py / 表达式生成端 / MCP 提交前预检三处复用。
"""
import re

VEC_WRAP_OPS = ("vec_avg", "vec_max", "vec_min", "vec_sum", "vec_count", "vec_norm")

# 计数/求和语义 -> vec_sum；否则 vec_avg
_SUM_HINTS = ("count", "sum", "num", "vol", "qty", "amount", "total")


def _fn_spans(expr):
    """解析全部函数调用区间 -> [(start, end, fn_name)]（end 为闭括号索引）。"""
    spans, stack = [], []
    i = 0
    while i < len(expr):
        m = re.match(r"[a-zA-Z_][a-zA-Z0-9_]*", expr[i:])
        if m and i + len(m.group(0)) < len(expr) and expr[i + len(m.group(0))] == "(":
            stack.append((m.group(0), i))
            i += len(m.group(0)) + 1
            continue
        if expr[i] == "(":
            stack.append((None, i))
        elif expr[i] == ")" and stack:
            fn, s = stack.pop()
            if fn:
                spans.append((s, i, fn))
        i += 1
    return spans


def _pick_agg(field):
    low = field.lower()
    return "vec_sum" if any(h in low for h in _SUM_HINTS) else "vec_avg"


def _innermost_fn(spans, pos):
    """字段起始位置 pos 所在的最内层函数名（无则 None）。"""
    inner = min((sp for sp in spans if sp[0] <= pos < sp[1]),
                key=lambda sp: sp[1] - sp[0], default=None)
    return inner[2] if inner else None


def wrap_naked_vectors(expr, vector_fields, agg=None):
    """把 expr 中裸用的 VECTOR 字段自动裹上 vec_* 聚合。幂等。

    参数:
      expr: 原始表达式字符串
      vector_fields: 本数据集中 type==VECTOR 的字段名列表
      agg: 强制指定聚合算子（None 则按字段语义自动选择）
    返回:
      (new_expr, wrapped_fields)
      new_expr: 修复后的表达式（若无裸用字段则与原文相同）
      wrapped_fields: 本次实际被裹上聚合的字段名列表（已裹过的不计入）
    """
    if not vector_fields:
        return expr, []
    spans = _fn_spans(expr)
    # 收集需要包裹的字段（存在至少一处裸用）
    to_wrap = []
    for f in vector_fields:
        for m in re.finditer(r"\b" + re.escape(f) + r"\b", expr):
            if _innermost_fn(spans, m.start()) not in VEC_WRAP_OPS:
                to_wrap.append(f)
                break
    if not to_wrap:
        return expr, []

    new_expr = expr
    # 逐字段从后往前替换，避免索引偏移
    for f in sorted(to_wrap, key=len, reverse=True):
        agg_op = agg or _pick_agg(f)
        # 匹配"未被 vec_( 直接包裹"的字段出现位置：
        # 前面不是 "vec_xxx(" 紧挨着的字段名
        pattern = re.compile(r"(?<![a-zA-Z0-9_])" + re.escape(f) + r"(?![a-zA-Z0-9_])")
        out, last = [], 0
        for m in pattern.finditer(new_expr):
            # 已裹过的（前面紧邻 "vec_xxx("）跳过
            prefix = new_expr[max(0, m.start() - 9):m.start()]
            if re.search(r"vec_[a-z]+\($", prefix):
                continue
            out.append(new_expr[last:m.start()])
            out.append(f"{agg_op}({f})")
            last = m.end()
        out.append(new_expr[last:])
        new_expr = "".join(out)
    return new_expr, sorted(to_wrap)
