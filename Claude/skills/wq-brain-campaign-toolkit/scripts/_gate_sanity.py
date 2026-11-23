# -*- coding: utf-8 -*-
"""_gate_sanity.py - gate.py 拆分·闸7 longCount 真实性 / 闸8 EVENT 类型 / 闸0 语义反模式。

依赖 _gate_expr_checks：fn_spans（括号跨度的通用助手）。
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _lib.common import load_json, load_platform_constraints
from _gate_expr_checks import fn_spans

def _parse_field_ids(expr):
    """从表达式中提取字段标识符（简单启发式，不依赖 verifier）。"""
    try:
        inaccessible = set(load_platform_constraints().get("inaccessible_ops", []))
    except Exception:
        inaccessible = set()
    ids = set()
    for tok in re.findall(r'[a-zA-Z_][a-zA-Z0-9_]*', expr):
        if tok not in inaccessible:
            ids.add(tok)
    return ids


def check_sanity_longcount(ctx, dataset, exprs, field_types):
    """闸7：对 VECTOR 字段检查 typed catalog 中的 longCount，低于 80 WARN。"""
    issues = []
    if not field_types:
        return issues
    all_fields = set()
    for e in exprs:
        all_fields |= _parse_field_ids(e)
    for fid in all_fields:
        ftype = field_types.get(fid)
        if ftype == "VECTOR":
            cat = _sanity_catalog(ctx, dataset)
            if isinstance(cat, dict):
                for f in cat.get("fields", []):
                    if f["id"] == fid:
                        lc = f.get("longCount", f.get("long_count", -1))
                        if 0 <= lc < 80:
                            issues.append(
                                f"[SANITY-LONGCOUNT] {fid}: longCount={lc} < 80 "
                                f"(platform cov may be misleading; see MEA f72/model25/model31 traps)"
                            )
                        break
    return issues


def _sanity_catalog(ctx, dataset):
    """取 typed catalog 供 longCount sanity 用（DB 优先，文件兜底；都没有返回 None）。"""
    try:
        from _lib.wqb_store import load_catalog
        d = load_catalog(ctx, dataset)
        if d and d.get("fields"):
            return d
    except Exception:
        pass
    cat_path = ctx.catalog_path(dataset)
    if os.path.exists(cat_path):
        try:
            return load_json(cat_path)
        except Exception:
            return None
    return None


def check_sanity_event_type(ctx, dataset, exprs, field_types):
    """闸8：表达式引用了 type==EVENT 的字段 → FAIL（2026-09-29 更正口径）。

    旧口径「type==EVENT 且未用 ts_event_* 才 FAIL」**不可满足**：ts_event_* 在平台不存在——
    tracking/KOR/TOOLKIT_CHECKLIST.md 记 Wave 16（other553）实测「102 个算子中无 ts_event_* 系列，
    8/8 ERROR」；闸1 也把它当未知函数拦，known_ops 亦无。结果是旧闸 8 的修复建议（去用 ts_event_*）
    照做必挂。EVENT 字段在标准算子下的行为**未验证**（MEA fundamental6 整集报废教训），
    故只要引用就 FAIL：先用 2 条探针（create_multi_simulation 最少 2 条——平台拒
    单元素数组；2026-11-21 起单仿真 create_simulation 已从 MCP 层删除）确认再放量。
    """
    issues = []
    if not field_types:
        return issues
    for e in exprs:
        for fid in _parse_field_ids(e):
            if field_types.get(fid) == "EVENT":
                issues.append(
                    f"[SANITY-EVENT-TYPE] {fid}: type=EVENT。平台无 ts_event_* 算子（KOR wave16 实测 "
                    f"8/8 ERROR），标准算子在 EVENT 字段上的行为未验证（MEA fundamental6 整集报废）："
                    f"先 1 条探针确认可用再放量，勿去找 ts_event_*"
                )
    return issues


# ---- 闸 0：语义反模式（可选闸，--gate0 开启，默认关闭保持兼容） ----
# 生成端实测三类废品会穿过闸 1-8 烧回测配额：
#   a) 恒等式 subtract(x, x) / divide(x, x)（同字段自相减/除恒等于 0/1）
#   b) 裸字段表达式（整式就是单个字段 ID，无任何算子加工）
#   c) 元数据字段作信号腿（periodend/periodtype/fyearend 等日期/分类码字段）

_GATE0_META_RE = re.compile(
    r"(periodend|periodtype|fyearend|periodnum|analyststart|curfperiod|curperiod)",
    re.IGNORECASE)
_GATE0_NUM_RE = re.compile(r"^[+-]?(\d+(\.\d+)?|\.\d+)$")
# 第二参数取对应数值时构成恒等或恒常量：add(x,0)=x, subtract(x,0)=x,
# multiply(x,1)=x / multiply(x,0)=0, divide(x,1)=x, power(x,1)=x / power(x,0)=1
_GATE0_NOOP_SECOND = {"add": {0.0}, "subtract": {0.0}, "multiply": {0.0, 1.0},
                      "divide": {1.0}, "power": {0.0, 1.0}}


def split_top_level_args(inner):
    """按顶层逗号切分函数调用内层字符串（嵌套括号内的逗号不切）。"""
    args, depth, buf = [], 0, []
    for c in inner:
        if c == "(":
            depth += 1
        elif c == ")":
            depth -= 1
        if c == "," and depth == 0:
            args.append("".join(buf))
            buf = []
        else:
            buf.append(c)
    if buf or inner.strip():
        args.append("".join(buf))
    return args


def check_semantic_gate0(expr, known_ops=None):
    """闸0 语义反模式检查。返回 issues 列表（空表=通过）。

    known_ops：已知算子名集合（如 pc["known_ops"]），元数据判定时排除算子名；
    缺省 None 时仅按标识符模式判定。
    """
    issues = []
    # b) 裸字段：整式即单一标识符，无任何算子调用
    if re.match(r"^[a-zA-Z_][a-zA-Z0-9_]*$", expr.strip()):
        issues.append("[BARE_FIELD] 裸字段表达式无信号加工")
    # a) 恒等式：遍历全部函数调用区间（含嵌套）
    for s, e, fn in fn_spans(expr):
        args = split_top_level_args(expr[s + len(fn) + 1:e])
        if fn in ("subtract", "divide") and len(args) >= 2:
            if args[0].strip() == args[1].strip():
                issues.append(f"[IDENTITY] x-x 或 x/x 恒零/恒1: {fn}")
        elif fn in _GATE0_NOOP_SECOND and len(args) >= 2:
            a1 = args[1].strip()
            if _GATE0_NUM_RE.match(a1) and float(a1) in _GATE0_NOOP_SECOND[fn]:
                issues.append(f"[IDENTITY] x-x 或 x/x 恒零/恒1: {fn}")
    # c) 元数据字段腿（排除已知算子名）
    ops = set(known_ops) if known_ops else set()
    for tok in re.findall(r"[a-zA-Z_][a-zA-Z0-9_]*", expr):
        if tok in ops:
            continue
        if _GATE0_META_RE.search(tok):
            issues.append(f"[META_FIELD] 元数据字段不可作信号腿: {tok}")
    return issues

