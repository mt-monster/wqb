# -*- coding: utf-8 -*-
"""atom.py — WorldQuant BRAIN "atom / combined" 信号分类（纯函数，单一口径源）。

平台 "Atom Alpha" = 单数据集 alpha：表达式引用的所有**数据字段**来自同一 dataset。
基础行情字段（returns/volume/close…）本身是"市场"这一个数据源，计为单一伪数据集
``BASE_MARKET``；分组键（industry/sector/market…）中性、不计数。一旦出现第二个数据集
的字段即判 combined。

判定 = 抽取数据字段 → 逐字段解析数据集 → distinct 数据集数 ≤1 为 atom，≥2 为 combined，
存在未解析字段为 unknown。

抽取器三处关键修正（2026-09-30 实证）——此前把非字段 token 误判为字段：
  1. 剥字符串字面量：``driver="gaussian"`` / ``buckets="2,5,6,7,10"`` 里的值不是字段。
  2. 排除 ``name=`` 左值：关键字参数名（filter/rettype/lag/sigma/range/hump…）与
     赋值变量名都不是字段；用 ``=(?!=)`` 同时覆盖 kwarg 与赋值。
  3. 赋值检测不再依赖 ``;`` 分句：多行（换行分隔）表达式的变量名（M5/B/Mx22/D90_22…）
     也一并排除。

本模块只做纯文本/映射计算，不做任何 DB/网络 IO；字段→数据集的取数由调用方注入
``resolve(field) -> (kind, dataset)`` 回调（store 侧批量查 DB，tools 侧用 AtomResolver）。
"""
from __future__ import annotations

import re
from typing import Callable, Iterable

#: 基础行情 / 参考字段 —— 平台始终可用，归属单一伪数据集 BASE_MARKET，参与计数。
BASE_MARKET_NAME = "BASE_MARKET"
BASE_MARKET_FIELDS = frozenset("""
returns volume close open high low cap price prc
vwap bid ask bid_price ask_price mid_price spread
dividend sharesout shares_out share_out sharesoutstanding shares_outstanding
adv20 adv60 adv120 adv252 adv10 adv5 adv190
open_interest turnover_vol turnover
amihud illiq log_ret log_return
""".split())

#: 分组维度键（传给 group_* / *_neutralize 的字面量，不是数据集；大小写不敏感）。
GROUPING_KEYS = frozenset("""
industry sector subindustry supersector subsector industrygroup sectorgroup
market exchange country group asset region
""".split())

#: 保留字（既非字段也非变量）。
RESERVED = frozenset("""nan null none true false""".split())

_COMMENT_RE = re.compile(r"/\*.*?\*/|//[^\n]*")
_STRING_RE = re.compile(r'"(?:[^"\\]|\\.)*"|\'(?:[^\'\\]|\\.)*\'')
_IDENT_RE = re.compile(r"[A-Za-z_][A-Za-z0-9_]*")
_CALL_RE = re.compile(r"([A-Za-z_][A-Za-z0-9_]*)\s*\(")
_ASSIGN_RE = re.compile(r"([A-Za-z_][A-Za-z0-9_]*)\s*=(?!=)")


def strip_comments(expr: str) -> str:
    return _COMMENT_RE.sub(" ", expr or "")


def strip_strings(expr: str) -> str:
    return _STRING_RE.sub(" ", expr or "")


def extract_fields(expr: str) -> list[str]:
    """抽取候选数据字段 token（已剔除算子调用、赋值/kwarg 左值、字符串、保留字）。

    不剔除基础行情字段与分组键——它们交解析器判定类别后决定是否计数。
    """
    s = strip_strings(strip_comments(expr))
    op_calls = set(_CALL_RE.findall(s))
    assigned = set(_ASSIGN_RE.findall(s))
    out: list[str] = []
    seen: set[str] = set()
    for tok in _IDENT_RE.findall(s):
        if tok in op_calls or tok in assigned:
            continue
        if tok.lower() in RESERVED:
            continue
        if tok not in seen:
            seen.add(tok)
            out.append(tok)
    return out


def resolve_kind(field: str, dataset_map) -> tuple[str, str | None]:
    """按 base/grouping → dataset_map 的顺序解析字段类别。

    dataset_map：field_name → dataset_name 的映射（缺失/None 视为未收录）。
    返回 (kind, dataset)，kind ∈ {base, grouping, dataset, unknown}。
    """
    if field in BASE_MARKET_FIELDS:
        return ("base", BASE_MARKET_NAME)
    if field.lower() in GROUPING_KEYS:
        return ("grouping", None)
    ds = dataset_map.get(field)
    return ("dataset", ds) if ds else ("unknown", None)


def has_non_ascii(text: str) -> bool:
    """表达式里是否含非 ASCII 字符（中文注释占位 / 损坏行）。"""
    return any(ord(c) > 127 for c in (text or ""))


def classify_stale(expr: str, unknown_fields: Iterable[str]) -> str:
    """对 unknown 判定结果做数据清洗细分。

    返回 ``'dirty'``（损坏 / 非表达式行）或 ``'stale_field'``（引用平台已下架字段）。

    判定依据（2026-09-30 实证，对 1142 条 unknown 全量复核）：
      - 含非 ASCII：多为中文注释占位（``'capex/cfo再投资动量'``）或笔记
        （``'M窗口504.40+e3.60'``），根本不是可执行表达式 → ``dirty``。
      - 残留未声明短变量（抽取器已剔除赋值 / kwarg 左值）：截断表达式
        （``'...mu'`` / ``'...sh'``）或裸变量 → ``dirty``。
      - 其余：字段名像真实字段却不在 ``fields`` 表 → 平台已下架 → ``stale_field``。
    """
    if has_non_ascii(expr):
        return "dirty"
    for f in unknown_fields:
        if len(f) <= 2 and f.isalpha() and f.lower() not in RESERVED:
            return "dirty"
    return "stale_field"


def classify_atom(
    expr: str,
    dataset_map,
    *,
    resolve: Callable[[str], tuple[str, str | None]] | None = None,
) -> dict:
    """判定单条表达式的 atom / combined 属性。

    dataset_map: field→dataset 映射（批量预取，主路径）。
    resolve:    可选回调，覆盖默认解析（tools 侧 DB 逐查用）。给了就以它为准。
    """
    fields = extract_fields(expr)
    _resolve = resolve or (lambda f: resolve_kind(f, dataset_map))
    base_fields: list[str] = []
    grouping: list[str] = []
    datasets: set[str] = set()
    unknown: list[str] = []
    for f in fields:
        kind, ds = _resolve(f)
        if kind == "base":
            base_fields.append(f)
            datasets.add(ds or BASE_MARKET_NAME)
        elif kind == "grouping":
            grouping.append(f)
        elif kind == "dataset":
            datasets.add(ds)
        else:
            unknown.append(f)
    if unknown:
        verdict = "unknown"
    elif len(datasets) <= 1:
        verdict = "atom"
    else:
        verdict = "combined"
    return {
        "verdict": verdict,
        "n_datasets": len(datasets),
        "datasets": sorted(datasets),
        "n_fields": len(fields),
        "base_fields": sorted(set(base_fields)),
        "grouping_keys": sorted(set(grouping)),
        "unknown_fields": sorted(set(unknown)),
    }
