# -*- coding: utf-8 -*-
"""atom.py — WorldQuant BRAIN "atom / combined" 信号分类（纯函数，单一口径源）。

口径锚定平台官方文档 **`single-dataset-alphas`**（"❗ Single Dataset Alphas"，
lastModified 2026-09-18；平台原文，2026-10-26 复核）：

1. 「Single Dataset Alphas must utilize data fields from **only one dataset**, with
   exceptions for the following **6 permitted grouping fields** – country, exchange,
   market, sector, industry and subindustry.」
2. 「The use of **`inst_pnl()` and `convert()`** operators is considered as utilizing
   the **pv1** dataset since these operators rely on pv1 data for calculations.」

⇒ 「ATOM」是论坛对官方 Single Dataset Alpha 的简称（MH33574《四类 Alpha》），
   **判据只有两条：非豁免字段的 dataset id 唯一 + 无 inst_pnl/convert**。

实现要点（2026-10-26 纠正，此前两处与官方原文不符）：
  a. 基础行情字段（returns/volume/close/cap/vwap…）属于 **pv1 数据集**，此前记为伪数据集
     ``BASE_MARKET`` ⇒ 同一个 pv1 数据集被数成两个，``pv1 字段 + returns`` 会被误判 combined。
     现统一归到 ``pv1``（保留 ``BASE_MARKET_NAME`` 旧名作别名）。
  b. ``inst_pnl`` / ``convert`` 此前完全不检查 ⇒ 非 pv1 集上用了它们仍被判 atom（假阳）。
     现按官方原文计为引用 pv1。
  c. 豁免分组字段收窄为官方那 6 个（此前还含 region/asset/group/supersector 等自造键；
     若某数据集恰有同名字段，会被误当豁免 ⇒ 假阳）。

判定 = 抽取数据字段 → 逐字段解析数据集 → distinct 数据集数 ≤1 且无 pv1 算子 ⇒ atom；
≥2 ⇒ combined；存在未解析字段 ⇒ unknown（fail-closed，不猜）。

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

#: 基础行情 / 参考字段 —— 官方口径属 **pv1** 数据集（`returns`/`close`/`cap`… 都是 pv1 字段）。
#: 名字仍是数据集 id，参与 distinct 计数；旧名 ``BASE_MARKET`` 保留为别名以免外部引用断裂。
PV1_DATASET = "pv1"
BASE_MARKET_NAME = PV1_DATASET
BASE_MARKET_FIELDS = frozenset("""
returns volume close open high low cap price prc
vwap bid ask bid_price ask_price mid_price spread
dividend sharesout shares_out share_out sharesoutstanding shares_outstanding
adv20 adv60 adv120 adv252 adv10 adv5 adv190
open_interest turnover_vol turnover
amihud illiq log_ret log_return
""".split())

#: 官方原文：使用这些算子即"视为使用 pv1 数据集"，与显式写 pv1 字段同罪。
PV1_OPERATORS = frozenset("inst_pnl convert".split())

#: 官方豁免的分组字段 —— **恰好这 6 个**，多一个都不豁免（`single-dataset-alphas` 原文）。
GROUPING_KEYS = frozenset("""
country exchange market sector industry subindustry
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
        return ("base", PV1_DATASET)
    if field.lower() in GROUPING_KEYS:
        return ("grouping", None)
    ds = dataset_map.get(field)
    return ("dataset", ds) if ds else ("unknown", None)


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
    # 官方原文：inst_pnl() / convert() 视为使用 pv1 ⇒ 只在非 pv1 集上才改变判决，
    # 但这里一律计入 datasets，由 distinct 计数自然处理（pv1 集自身仍是 atom）。
    pv1_ops = sorted(set(_CALL_RE.findall(strip_strings(strip_comments(expr)))) & PV1_OPERATORS)
    base_fields: list[str] = []
    grouping: list[str] = []
    datasets: set[str] = set()
    unknown: list[str] = []
    for f in fields:
        kind, ds = _resolve(f)
        if kind == "base":
            base_fields.append(f)
            datasets.add(ds or PV1_DATASET)
        elif kind == "grouping":
            grouping.append(f)
        elif kind == "dataset":
            datasets.add(ds)
        else:
            unknown.append(f)
    if pv1_ops:
        datasets.add(PV1_DATASET)
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
        "pv1_operators": pv1_ops,
        "unknown_fields": sorted(set(unknown)),
    }
