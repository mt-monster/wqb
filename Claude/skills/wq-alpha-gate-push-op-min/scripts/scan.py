#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""逐算子双通道扫描器：删除候选 + 替换候选 + 参数扫描（用户指令 2026-10-31）。

对表达式里的**每个算子节点**（逐层 L1/L2/L3/L4）生成两类实验候选，并把每个数值参数展开成扫描档位：

  ① 删除通道（--delete）：把该算子删除后，表达式是否更精简（算子数 -1 以上）且指标不坍塌？
     - 单参包裹删除  f(x) -> x          （rank / reverse / abs）
     - 恒等元素删除  add(x,0)/multiply(x,1)/subtract(x,0) -> x
     - 重复腿合并    multiply(a,a) -> a
  ② 替换通道（--replace）：把该算子替换成金融含义等价的另一算子后，指标是否更精简且不坍塌？
     - 时序层  ts_av_diff<->ts_zscore、ts_rank<->ts_quantile(gaussian)、ts_mean<->ts_sum、ts_delta<->ts_zscore
     - 截面层  rank<->zscore、group_rank<->group_zscore、group_neutralize<->vector_neut
     - 每个候选标注：数学等价（rank 吸收单调变换，无需实测）vs 语义等价（需实测）
  ③ 参数扫描（--params）：把每个数值参数按 0.5/0.75/1.25/1.5 倍展开成扫描变体。
     ts_* 窗口参数额外补扫绝对值阶梯 [21,63,126,252,504,756]（倍数扫描漏跨量级甜点）。

本脚本**只生成候选表达式**（JSON），零平台调用、零队列成本；是否派发实测 / 采纳由调用方按
references/scan-protocol.md 决定。判定只走平台（submit_batch + check_correlation）。
"""
from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from typing import Any, Dict, List, Optional, Tuple

sys.path.insert(0, __file__.rsplit("/", 1)[0])

from wqexpr import (  # noqa: E402
    Node,
    ParseError,
    find_rewrites,
    iter_calls,
    op_count,
    parse,
)

# ------------------------------------------------------------------ 常量

#: 单参包裹算子：f(x) 可安全删除为 x（省 1 算子，信号尺度会变，必实测）
SINGLE_ARG_WRAP = {
    "rank", "reverse", "abs",           # 原有
    "log", "sqrt", "inverse", "sign",   # 数学包裹：对数/平方根/倒数/符号
    "normalize", "scale",               # 归一化包裹
    "densify", "pasteurize",            # 数据清洗包裹
    "not",                              # 逻辑取反
}

#: 等价替换表：算子 -> [(新算子, 数学等价?, kwarg 补充/None, 备注)]
#:   数学等价 = 外层单调算子会吸收内层变换，无需实测（仅省算子或换实现时用）
#:   kwarg 补充 = 新算子需要额外补的 kwargs（如 ts_quantile 的 driver）
#:   "NEED_AXIS" 占位 = 需要人工提供分组轴，无法自动适配
EQUIV: Dict[str, List[Tuple[str, bool, Optional[Any], str]]] = {
    # 时序层（L3）
    "ts_av_diff": [("ts_zscore", False, None, "相对均值偏离：未归一 vs 波动归一（语义等价，需实测）")],
    "ts_zscore": [("ts_av_diff", False, None, "波动归一 vs 未归一偏离（语义等价，需实测）")],
    "ts_rank": [("ts_quantile", True, {"driver": "gaussian"}, "时序分位：rank vs gaussian 分位（数学等价，rank 吸收单调变换）")],
    "ts_quantile": [("ts_rank", True, None, "gaussian 分位 vs rank（数学等价）")],
    "ts_mean": [("ts_sum", False, None, "窗口均值 vs 窗口和（尺度差，语义等价，需实测）"),
                ("ts_decay_linear", False, None, "均值 vs 线性衰减（语义等价，需实测）")],
    "ts_sum": [("ts_mean", False, None, "窗口和 vs 窗口均值（语义等价，需实测）")],
    "ts_delta": [("ts_zscore", False, None, "差分 vs 标准化动量（语义等价，需实测）")],
    "ts_std_dev": [("ts_ir", False, None, "波动率 vs 风险调整 IR（语义等价，需实测）")],
    "ts_ir": [("ts_std_dev", False, None, "IR vs 波动率（语义等价，需实测）")],
    "ts_scale": [("ts_zscore", False, None, "缩放归一 vs zscore 归一（语义等价，需实测）")],
    "ts_regression": [("ts_corr", False, None, "回归斜率 vs 相关系数（语义等价，需实测）")],
    "ts_corr": [("ts_covariance", False, None, "相关系数 vs 协方差（语义等价，需实测）"),
                ("ts_regression", False, None, "相关 vs 回归（语义等价，需实测）")],
    "ts_covariance": [("ts_corr", False, None, "协方差 vs 相关系数（语义等价，需实测）")],
    "ts_returns": [("ts_delta", False, None, "对数收益率 vs 简单差分（语义等价，需实测）")],
    "ts_kurtosis": [("ts_std_dev", False, None, "峰度 vs 波动率（语义等价，需实测）")],
    "ts_arg_max": [("ts_arg_min", False, None, "最大值位置 vs 最小值位置（语义对称，需实测）")],
    "ts_arg_min": [("ts_arg_max", False, None, "最小值位置 vs 最大值位置（语义对称，需实测）")],
    "ts_delay": [("ts_backfill", False, None, "延迟 vs 回填（语义等价，需实测）")],
    "ts_product": [("ts_sum", False, None, "窗口乘积 vs 窗口和（语义等价，需实测）")],
    "ts_max_diff": [("ts_delta", False, None, "最大差 vs 差分（语义等价，需实测）")],
    "ts_count_nans": [("ts_backfill", False, None, "NaN 计数 vs 回填（语义等价，需实测）")],
    "ts_target_tvr_decay": [("ts_decay_linear", False, None, "TVR 衰减 vs 线性衰减（语义等价，需实测）")],
    "ts_target_tvr_hump": [("hump", False, None, "TVR 驼峰 vs 驼峰（语义等价，需实测）")],
    # 截面层（L2/L4）
    "rank": [("zscore", False, None, "截面 rank vs zscore（语义等价，需实测）"),
             ("group_rank", False, "NEED_AXIS", "rank -> group_rank 需人工给分组轴")],
    "zscore": [("rank", False, None, "截面 zscore vs rank（语义等价，需实测）")],
    "group_rank": [("group_zscore", False, None, "组内 rank vs zscore（语义等价，需实测）"),
                   ("rank", False, None, "group_rank(x,g) -> rank(x) 丢弃分组轴（需实测）")],
    "group_zscore": [("group_rank", False, None, "组内 zscore vs rank（语义等价，需实测）")],
    # ⚠ 2026-10-31 实测连坐教训：group_neutralize 第2参必须是 Unit[Group:1]（bucket/group_rank 等），
    # vector_neut 第2参是任意向量轴（如 ts_backfill 结果 Unit[]）。两者参数单位语义不同，
    # 直接替换会触发平台 "Incompatible unit ... expected Unit[Group:1]" ⇒ 整批 CANCELLED（连坐）。
    # 故标 NEED_UNIT 占位，不自动生成表达式。
    "group_neutralize": [("vector_neut", False, "NEED_UNIT", "组去均值 vs 向量正交化：第2参单位不同（Group vs 向量），需人工确认轴单位，不自动替换")],
    "vector_neut": [("group_neutralize", False, "NEED_UNIT", "向量正交化 vs 组去均值：第2参单位不同（向量 vs Group），需人工确认轴单位，不自动替换")],
    "winsorize": [("rank", False, None, "截尾 vs 截面 rank（语义等价，需实测）")],
    "group_mean": [("group_sum", False, None, "组均值 vs 组和（尺度差，语义等价，需实测）")],
    "group_sum": [("group_mean", False, None, "组和 vs 组均值（语义等价，需实测）")],
    "group_scale": [("group_zscore", False, None, "组内缩放 vs 组内 zscore（语义等价，需实测）")],
    "group_std_dev": [("group_scale", False, None, "组内波动 vs 组内缩放（语义等价，需实测）")],
    "group_count": [("group_sum", False, None, "组计数 vs 组和（语义等价，需实测）")],
    "group_backfill": [("ts_backfill", False, None, "组内回填 vs 时序回填（语义等价，需实测）")],
    "normalize": [("scale", False, None, "归一化 vs 缩放（语义等价，需实测）")],
    "scale": [("normalize", False, None, "缩放 vs 归一化（语义等价，需实测）")],
    "quantile": [("rank", True, None, "分位数 vs rank（数学等价，rank 吸收单调变换）")],
    "pasteurize": [("rank", False, None, "巴氏化 vs rank（语义等价，需实测）")],
    # 向量层（L1，VECTOR 字段降维）
    "vec_avg": [("vec_sum", False, None, "向量均值 vs 向量和（尺度差，语义等价，需实测）")],
    "vec_sum": [("vec_avg", False, None, "向量和 vs 向量均值（语义等价，需实测）")],
    "vec_max": [("vec_min", False, None, "向量最大 vs 向量最小（语义对称，需实测）")],
    "vec_min": [("vec_max", False, None, "向量最小 vs 向量最大（语义对称，需实测）")],
    "vec_stddev": [("vec_range", False, None, "向量标准差 vs 向量极差（语义等价，需实测）")],
    "vec_range": [("vec_stddev", False, None, "向量极差 vs 向量标准差（语义等价，需实测）")],
    "vec_count": [("vec_sum", False, None, "向量计数 vs 向量和（语义等价，需实测）")],
    # 数学层（L1）
    "log": [("sqrt", False, None, "对数压缩 vs 平方根压缩（语义等价，需实测）")],
    "sqrt": [("log", False, None, "平方根 vs 对数（语义等价，需实测）")],
    "inverse": [("reverse", False, None, "倒数 vs 反转（语义等价，需实测）")],
    "signed_power": [("power", False, None, "带符号幂 vs 绝对幂（语义等价，需实测）")],
    "power": [("signed_power", False, None, "绝对幂 vs 带符号幂（语义等价，需实测）")],
    "max": [("min", False, None, "逐元素最大 vs 最小（语义对称，需实测）")],
    "min": [("max", False, None, "逐元素最小 vs 最大（语义对称，需实测）")],
    # 逻辑层（L4 门控）
    "if_else": [("trade_when", False, "NEED_UNIT", "条件选择 vs 条件交易：第2/3参语义不同（值 vs 持仓），需人工确认，不自动替换")],
    "trade_when": [("if_else", False, "NEED_UNIT", "条件交易 vs 条件选择：参数语义不同（持仓 vs 值），需人工确认，不自动替换")],
    "greater": [("less", False, None, "大于 vs 小于（语义对称，需实测）")],
    "less": [("greater", False, None, "小于 vs 大于（语义对称，需实测）")],
    "greater_equal": [("less_equal", False, None, "大于等于 vs 小于等于（语义对称，需实测）")],
    "less_equal": [("greater_equal", False, None, "小于等于 vs 大于等于（语义对称，需实测）")],
    "equal": [("not_equal", False, None, "等于 vs 不等于（语义对称，需实测）")],
    "not_equal": [("equal", False, None, "不等于 vs 等于（语义对称，需实测）")],
    "and": [("or", False, None, "逻辑与 vs 逻辑或（语义对称，需实测）")],
    "or": [("and", False, None, "逻辑或 vs 逻辑与（语义对称，需实测）")],
    # SA/combo 专用算子（普通 alpha 不可用，仅标注占位，不自动生成表达式）
    "combo_a": [("generate_stats", False, "SA_ONLY", "SA combo 专用，普通 alpha 不可用")],
    "generate_stats": [("combo_a", False, "SA_ONLY", "SA combo 专用，普通 alpha 不可用")],
    "self_corr": [("None", False, "SA_ONLY", "SA 相关性计算专用")],
    "universe_size": [("None", False, "SA_ONLY", "SA 宇宙规模查询专用")],
    # 基础运算（L1，删除通道已覆盖恒等元素，此处补替换通道）
    "add": [("subtract", False, None, "加法 vs 减法（语义对称，需实测）")],
    "subtract": [("add", False, None, "减法 vs 加法（语义对称，需实测）")],
    "multiply": [("divide", False, None, "乘法 vs 除法（语义对称，需实测）")],
    "divide": [("multiply", False, None, "除法 vs 乘法（语义对称，需实测）")],
    # 分桶 / 事件型 / 特殊
    "bucket": [("rank", False, None, "分桶 vs rank（语义等价，需实测）")],
    "hump": [("ts_target_tvr_hump", False, None, "驼峰 vs TVR驼峰（语义等价，需实测）")],
    "tail": [("winsorize", False, None, "截尾 vs 缩尾（语义等价，需实测）")],
    "ts_backfill": [("group_backfill", False, None, "时序回填 vs 组内回填（语义等价，需实测）")],
    "ts_step": [("ts_delta", False, None, "步进 vs 差分（语义等价，需实测）")],
    "days_from_last_change": [("ts_delta", False, None, "距上次变化天数 vs 差分（语义等价，需实测）")],
    "last_diff_value": [("ts_delta", False, None, "上次不同值 vs 差分（语义等价，需实测）")],
    "kth_element": [("ts_arg_max", False, None, "第k元素 vs 最大值位置（语义等价，需实测）")],
    "group_cartesian_product": [("group_count", False, None, "笛卡尔积 vs 组计数（语义等价，需实测）")],
    "in": [("equal", False, None, "成员判断 vs 等于（语义等价，需实测）")],
    "is_nan": [("ts_count_nans", False, None, "NaN判断 vs NaN计数（语义等价，需实测）")],
    # SA 组合层专用 reduce_*（普通 REGULAR alpha 不可用，仅标注占位）
    "reduce_avg": [("None", False, "SA_ONLY", "SA 组合层专用")],
    "reduce_choose": [("None", False, "SA_ONLY", "SA 组合层专用")],
    "reduce_count": [("None", False, "SA_ONLY", "SA 组合层专用")],
    "reduce_ir": [("None", False, "SA_ONLY", "SA 组合层专用")],
    "reduce_kurtosis": [("None", False, "SA_ONLY", "SA 组合层专用")],
    "reduce_max": [("None", False, "SA_ONLY", "SA 组合层专用")],
    "reduce_min": [("None", False, "SA_ONLY", "SA 组合层专用")],
    "reduce_norm": [("None", False, "SA_ONLY", "SA 组合层专用")],
    "reduce_percentage": [("None", False, "SA_ONLY", "SA 组合层专用")],
    "reduce_powersum": [("None", False, "SA_ONLY", "SA 组合层专用")],
    "reduce_range": [("None", False, "SA_ONLY", "SA 组合层专用")],
    "reduce_skewness": [("None", False, "SA_ONLY", "SA 组合层专用")],
    "reduce_stddev": [("None", False, "SA_ONLY", "SA 组合层专用")],
    "reduce_sum": [("None", False, "SA_ONLY", "SA 组合层专用")],
}

#: 参数扫描档位（倍数）
SCAN_FACTORS = [0.5, 0.75, 1.25, 1.5]

#: 时序窗口绝对值阶梯（标准交易日跨度，2026-11-03 教训：倍数扫描漏跨量级甜点）
TS_WINDOW_LADDER = [21, 63, 126, 252, 504, 756]

# ------------------------------------------------------------------ 分层

#: 层 -> 算子名集合（启发式，仅作候选标注参考）
_LAYER_MAP: List[Tuple[str, set]] = [
    ("L1 提取", {"divide", "multiply", "subtract", "add"}),
    ("L2 归一", {"rank", "zscore", "winsorize", "bucket"}),
    ("L3 时序", {"ts_mean", "ts_sum", "ts_zscore", "ts_rank", "ts_quantile", "ts_delta",
                 "ts_av_diff", "ts_decay_linear", "ts_target_tvr_decay", "ts_backfill",
                 "ts_delay", "ts_regression", "ts_arg_min", "ts_arg_max"}),
    ("L4 截面", {"group_rank", "group_zscore", "group_neutralize", "group_scale", "vector_neut"}),
]


def layer_of(op: str) -> str:
    for name, ops in _LAYER_MAP:
        if op in ops:
            return name
    return "L? 其他"


# ------------------------------------------------------------------ AST 替换

def _subst(node: Node, target: str, repl: Node) -> Tuple[Node, bool]:
    """把 node 中所有 to_str()==target 的子节点替换成 repl。返回 (新节点, 是否改过)。"""
    if node.to_str() == target:
        return repl, True
    if node.kind == "call":
        new_args, ch = [], False
        for a in node.args:
            na, c = _subst(a, target, repl)
            new_args.append(na)
            ch |= c
        new_kw, chk = {}, False
        for k, v in node.kwargs.items():
            nv, c = _subst(v, target, repl)
            new_kw[k] = nv
            chk |= c
        if ch or chk:
            return Node("call", name=node.name, args=new_args, kwargs=new_kw), True
        return node, False
    if node.kind == "bin":
        nl, c1 = _subst(node.left, target, repl)
        nr, c2 = _subst(node.right, target, repl)
        if c1 or c2:
            return Node("bin", op=node.op, left=nl, right=nr), True
        return node, False
    return node, False


def _subst_call(node: Node, target: str, new_name: str,
                new_args: List[Node], new_kwargs: Dict[str, Node]) -> Tuple[Node, bool]:
    """把 target 这个 call 节点整体替换成 new_name(new_args, new_kwargs)。"""
    repl = Node("call", name=new_name, args=new_args, kwargs=new_kwargs)
    return _subst(node, target, repl)


# ------------------------------------------------------------------ ① 删除通道

def delete_candidates(expr: str) -> List[Dict[str, Any]]:
    """删除通道：每个可安全删除的算子节点 -> 删除后表达式。"""
    try:
        node = parse(expr)
    except ParseError:
        return []
    canon = node.to_str()
    base = op_count(canon)
    out: List[Dict[str, Any]] = []
    seen: set = set()

    # (a) 单参包裹删除 f(x) -> x
    for call in iter_calls(node):
        if call.name in SINGLE_ARG_WRAP and len(call.args) == 1:
            target = call.to_str()
            if target in seen:
                continue
            new_node, ch = _subst(node, target, call.args[0])
            if not ch:
                continue
            ne = new_node.to_str()
            if ne == canon or op_count(ne) >= base:
                continue
            seen.add(target)
            out.append({
                "kind": "del_wrap",
                "target_op": call.name,
                "layer": layer_of(call.name),
                "target": target,
                "op_before": base,
                "op_after": op_count(ne),
                "op_saved": base - op_count(ne),
                "expr": ne,
                "lossless": False,
                "note": f"删除 {call.name}(·) 包裹 → 直接透传内层（信号尺度/归一会变，必实测）",
            })

    # (b) 恒等元素 + 重复腿（复用 find_rewrites 的 C3.4 / C1）
    for r in find_rewrites(node):
        if r["rule"] in ("C3.4", "C1") and r["op_saved"] > 0:
            ne = canon.replace(r["where"], r["after"])
            if ne == canon or ne in seen:
                continue
            seen.add(ne)
            out.append({
                "kind": "del_identity" if r["rule"] == "C3.4" else "del_dupleg",
                "target_op": r["rule"],
                "layer": layer_of(r["rule"]),
                "target": r["where"],
                "op_before": base,
                "op_after": op_count(ne),
                "op_saved": r["op_saved"],
                "expr": ne,
                "lossless": r.get("lossless", False),
                "note": r.get("note", ""),
            })

    out.sort(key=lambda d: (not d["lossless"], -d["op_saved"], d["expr"]))
    return out


# ------------------------------------------------------------------ ② 替换通道

def _adapt(old_args: List[Node], old_kw: Dict[str, Node],
           new_name: str, extra_kw: Optional[Any]) -> Tuple[Optional[List[Node]], Optional[Dict[str, Node]], str]:
    """按新算子 arity 裁剪参数。返回 (args, kwargs, note) 或 (None, None, 原因)。"""
    # NEED_AXIS 占位：需要人工轴
    if extra_kw == "NEED_AXIS":
        return None, None, "需要人工提供分组轴，无法自动适配"
    # NEED_UNIT 占位：第2参单位语义不同（Group vs 向量），直接替换会单位错整批连坐
    if extra_kw == "NEED_UNIT":
        return None, None, "第2参单位语义不同（Group vs 向量），需人工确认轴单位，不自动替换"
    # ts_quantile -> ts_rank：去掉 driver kwarg
    if new_name == "ts_rank" and "driver" in old_kw:
        old_kw = {k: v for k, v in old_kw.items() if k != "driver"}
    # 丢弃「新算子用不上的尾参」：如 group_rank(x,g) -> rank(x) 只保留第一个位置参数
    keep = len(old_args)
    if new_name in ("rank", "zscore", "abs", "reverse"):
        keep = 1
    new_args = old_args[:keep]
    new_kw = dict(old_kw)
    if extra_kw:
        for k, v in extra_kw.items():
            new_kw[k] = Node("ident", name=v) if isinstance(v, str) else Node("num", text=str(v))
    return new_args, new_kw, ""


def replace_candidates(expr: str) -> List[Dict[str, Any]]:
    """替换通道：每个算子节点 -> 金融含义等价的替换表达式。"""
    try:
        node = parse(expr)
    except ParseError:
        return []
    canon = node.to_str()
    base = op_count(canon)
    out: List[Dict[str, Any]] = []
    seen: set = set()

    for call in iter_calls(node):
        if call.name not in EQUIV:
            continue
        for new_op, math_eq, extra_kw, note in EQUIV[call.name]:
            new_args, new_kw, why = _adapt(call.args, call.kwargs, new_op, extra_kw)
            if new_args is None:
                # 无法自动适配 -> 记一条占位（不生成表达式）
                tag = (call.to_str(), new_op, "need_axis")
                if tag not in seen:
                    seen.add(tag)
                    out.append({
                        "kind": "rep_equiv",
                        "target_op": call.name,
                        "replaced_by": new_op,
                        "layer": layer_of(call.name),
                        "math_equivalent": math_eq,
                        "expr": None,
                        "op_before": base,
                        "op_after": base,
                        "note": note + "；" + why,
                    })
                continue
            new_node, ch = _subst_call(node, call.to_str(), new_op, new_args, new_kw)
            if not ch:
                continue
            ne = new_node.to_str()
            if ne == canon or ne in seen:
                continue
            seen.add(ne)
            out.append({
                "kind": "rep_equiv",
                "target_op": call.name,
                "replaced_by": new_op,
                "layer": layer_of(call.name),
                "math_equivalent": math_eq,
                "expr": ne,
                "op_before": base,
                "op_after": op_count(ne),
                "op_saved": base - op_count(ne),
                "note": note,
            })

    out.sort(key=lambda d: (not d["math_equivalent"], d["target_op"]))
    return out


# ------------------------------------------------------------------ ③ 参数扫描

def param_scan(expr: str) -> List[Dict[str, Any]]:
    """参数扫描：每个数值参数 -> 0.5/0.75/1.25/1.5 倍档位变体。"""
    try:
        node = parse(expr)
    except ParseError:
        return []
    canon = node.to_str()
    base = op_count(canon)
    out: List[Dict[str, Any]] = []
    seen: set = set()

    for call in iter_calls(node):
        for i, a in enumerate(call.args):
            if a.kind != "num":
                continue
            v = float(a.text)
            # 时序窗口参数（ts_* 的位置参数 idx>=1，即 lookback）必须正整数：
            # ×0.75/×1.25 会出非整数（如 49.5），且 repr(33.0) 带 ".0" ⇒ 平台
            # "Got invalid value \"33.0\" for attribute \"lookback\"" 全批 ERROR。
            # 故窗口参数强制 round 取整并输出无小数点字符串；标量参数（权重/幂）保留小数。
            is_window = call.name.startswith("ts_") and i >= 1

            # ── 倍数扫描 ──
            for f in SCAN_FACTORS:
                if is_window:
                    nv = int(round(v * f))
                    if nv <= 0 or nv == int(round(v)):
                        continue
                    text = str(nv)
                else:
                    nv = round(v * f, 4)
                    if nv <= 0 or abs(nv - v) < 1e-9:
                        continue
                    text = repr(nv)
                new_args = [x for x in call.args]
                new_args[i] = Node("num", text=text)
                new_node, ch = _subst_call(node, call.to_str(), call.name, new_args, call.kwargs)
                if not ch:
                    continue
                ne = new_node.to_str()
                if ne == canon or ne in seen:
                    continue
                seen.add(ne)
                out.append({
                    "kind": "param",
                    "target_op": call.name,
                    "layer": layer_of(call.name),
                    "param_idx": i,
                    "old_value": v,
                    "new_value": float(nv),
                    "factor": f,
                    "expr": ne,
                    "op_before": base,
                    "op_after": op_count(ne),
                })

            # ── 绝对值阶梯扫描（仅 ts_* 窗口，2026-11-03 教训）──
            # 倍数扫描漏跨量级甜点（如 ts_rank 120→504 = 4.2×，倍数扫描覆盖不了）
            if is_window:
                v_int = int(round(v))
                for ladder_val in TS_WINDOW_LADDER:
                    if ladder_val == v_int or ladder_val <= 0:
                        continue
                    text = str(ladder_val)
                    new_args = [x for x in call.args]
                    new_args[i] = Node("num", text=text)
                    new_node, ch = _subst_call(node, call.to_str(), call.name, new_args, call.kwargs)
                    if not ch:
                        continue
                    ne = new_node.to_str()
                    if ne == canon or ne in seen:
                        continue
                    seen.add(ne)
                    out.append({
                        "kind": "param",
                        "target_op": call.name,
                        "layer": layer_of(call.name),
                        "param_idx": i,
                        "old_value": v,
                        "new_value": float(ladder_val),
                        "factor": round(ladder_val / v, 3) if v else None,
                        "ladder": True,
                        "expr": ne,
                        "op_before": base,
                        "op_after": op_count(ne),
                    })

    out.sort(key=lambda d: (d["target_op"], d["param_idx"], d["old_value"]))
    return out


# ------------------------------------------------------------------ 汇总

def scan_report(expr: str, do_delete: bool = True,
                do_replace: bool = True, do_params: bool = True) -> Dict[str, Any]:
    try:
        node = parse(expr)
    except ParseError as exc:
        return {"expr": expr, "error": str(exc)}
    canon = node.to_str()
    base = op_count(canon)
    per = Counter(c.name for c in iter_calls(node))
    report: Dict[str, Any] = {
        "expr": canon,
        "op_count": base,
        "per_op": dict(per.most_common()),
        "layers": {},
        "delete_candidates": delete_candidates(canon) if do_delete else [],
        "replace_candidates": replace_candidates(canon) if do_replace else [],
        "param_variants": param_scan(canon) if do_params else [],
    }
    for c in iter_calls(node):
        report["layers"].setdefault(layer_of(c.name), []).append(c.name)
    return report


# ------------------------------------------------------------------ CLI

def main() -> None:
    ap = argparse.ArgumentParser(description="WQ alpha 逐算子双通道扫描（删除+替换+参数，纯本地）")
    src = ap.add_mutually_exclusive_group(required=True)
    src.add_argument("--expr")
    src.add_argument("--file")
    ap.add_argument("--delete", action="store_true", help="生成删除候选")
    ap.add_argument("--replace", action="store_true", help="生成等价替换候选")
    ap.add_argument("--params", action="store_true", help="生成参数扫描变体")
    ap.add_argument("--json", action="store_true", help="JSON 输出（默认人类可读）")
    ap.add_argument("--out", help="把候选表达式写到文件（每行一个，可喂 submit_batch）")
    args = ap.parse_args()

    do_delete = args.delete or not (args.replace or args.params)
    do_replace = args.replace or not (args.delete or args.params)
    do_params = args.params or not (args.delete or args.replace)

    exprs = [args.expr] if args.expr else [
        ln.strip() for ln in open(args.file, encoding="utf-8")
        if ln.strip() and not ln.startswith("#")
    ]

    all_out: List[str] = []
    for e in exprs:
        rep = scan_report(e, do_delete, do_replace, do_params)
        if "error" in rep:
            print(f"[scan] 跳过无法解析: {rep['error']}", file=sys.stderr)
            continue
        if args.out:
            for c in (rep["delete_candidates"] + rep["replace_candidates"] + rep["param_variants"]):
                if c.get("expr"):
                    all_out.append(c["expr"])
        if not args.json:
            print("=" * 76)
            print(f"表达式（{rep['op_count']} 算子）: {rep['expr']}")
            print(f"逐算子: {rep['per_op']}")
            print(f"分层: {json.dumps(rep['layers'], ensure_ascii=False)}")
            for title, key in [("① 删除候选", "delete_candidates"),
                               ("② 替换候选", "replace_candidates"),
                               ("③ 参数变体", "param_variants")]:
                items = rep[key]
                print(f"\n--- {title}（{len(items)}） ---")
                for c in items:
                    if c["kind"] == "param":
                        print(f"  [param] {c['target_op']}[{c['param_idx']}] {c['old_value']}→{c['new_value']} (×{c['factor']})")
                        print(f"     {c['expr'][:190]}")
                    elif c.get("expr"):
                        tag = "数学等价" if c.get("math_equivalent") else ("无损" if c.get("lossless") else "需实测")
                        print(f"  [{c['kind']}] {c['target_op']}→{c.get('replaced_by','(删)')}  {c['op_before']}→{c['op_after']} 算子 ({tag})  [{c['layer']}]")
                        print(f"     {c['expr'][:190]}")
                    else:
                        print(f"  [{c['kind']}] {c['target_op']}→{c.get('replaced_by')}  无法自动适配: {c['note']}")
        else:
            print(json.dumps(rep, ensure_ascii=False))

    if args.out and all_out:
        with open(args.out, "w", encoding="utf-8") as fh:
            fh.write("\n".join(all_out) + "\n")
        print(f"\n[scan] 已写出 {len(all_out)} 条候选 -> {args.out}", file=sys.stderr)


if __name__ == "__main__":
    main()
