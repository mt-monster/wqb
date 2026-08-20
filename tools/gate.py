# -*- coding: utf-8 -*-
"""gate.py - 通用提交前闸门（区域无关）。

取代 KOR 专用版，支持任意战役目录。自动派生 catalog 路径 <campaign-dir>/reference/<region>_<dataset>_fields.json。

用法:
  python tools/gate.py --campaign-dir tracking/EUR --dataset ai_equity_alpha --file candidates/xxx_exprs.json
  python tools/gate.py --campaign-dir tracking/KOR --dataset model219 --expr "rank(close)"
退出码: 0=全 PASS, 1=存在 FAIL
"""
import argparse
import hashlib
import json
import os
import re
import sys

# 添加 tools/lib 到路径
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "lib"))

# ---- verifier：import 直调，路径搜索 .workbuddy 优先 ----
_VALIDATOR_DIRS = [
    os.environ.get("WQ_VALIDATOR_DIR"),
    os.environ.get("WQ_VALIDATOR_DIR", os.path.join(os.path.expanduser("~"), ".workbuddy", "skills", "alpha-expression-verifier", "scripts")),
    r"D:\coding\traeCN_project\wqb\.cursor\skills\alpha-expression-verifier\scripts",
    os.environ.get("WQ_VALIDATOR_DIR", os.path.join(os.path.expanduser("~"), ".workbuddy", "skills", "alpha-expression-verifier", "scripts")),
]
_VALIDATOR = None


def get_validator():
    global _VALIDATOR
    if _VALIDATOR is not None:
        return _VALIDATOR
    for d in _VALIDATOR_DIRS:
        if d and os.path.isfile(os.path.join(d, "validator.py")):
            sys.path.insert(0, d)
            from validator import ExpressionValidator
            _VALIDATOR = ExpressionValidator()
            return _VALIDATOR
    raise RuntimeError("未找到 alpha-expression-verifier（设 WQ_VALIDATOR_DIR 指定）")


# 从 src/wqb/config.py 导入平台权威算子列表
_REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _REPO_ROOT not in sys.path:
    sys.path.insert(0, _REPO_ROOT)
from src.wqb.config import OP_FAMILIES
from vector_wrap import wrap_naked_vectors
KNOWN_OPS = {op for ops in OP_FAMILIES.values() for op in ops}
VECTOR_ONLY_OPS = {"vec_avg", "vec_max", "vec_min", "vec_sum", "vec_count", "vec_norm"}
VEC_WRAP_OPS = ("vec_avg", "vec_max", "vec_min", "vec_sum", "vec_count", "vec_norm")
INACCESSIBLE_OPS = {"ts_min", "ts_max"}
GROUP_IDENTIFIERS = {"sector", "subindustry", "industry", "market", "country", "exchange"}
PRICE_VOLUME = {"open", "high", "low", "close", "volume", "returns", "vwap", "cap", "sharesout", "adv20"}
DRIVER_ARGS = {"gaussian", "uniform", "cauchy"}

# VECTOR 字段禁止直接包裹的算子 (event 输入不支持, 2026-08-18 wave34 教训)
# 这些算子直接包裹 VECTOR 字段会报 "does not support event inputs"
VECTOR_FORBIDDEN_OPS = {
    'ts_backfill', 'ts_delta', 'divide', 'subtract', 'add', 'multiply',
    'ts_zscore', 'ts_rank', 'ts_corr', 'ts_covariance', 'ts_regression',
    'ts_mean', 'ts_sum', 'ts_std_dev', 'ts_product', 'ts_av_diff',
    'ts_kurtosis', 'ts_arg_max', 'ts_arg_min', 'ts_max_diff',
    'ts_scale', 'ts_delay', 'ts_quantile', 'ts_count_nans',
    'ts_decay_linear', 'ts_ir', 'ts_returns', 'ts_step',
    'rank', 'zscore', 'scale', 'normalize', 'quantile',
    'winsorize', 'bucket', 'tail', 'trade_when',
    'group_mean', 'group_rank', 'group_backfill', 'group_scale',
    'group_count', 'group_zscore', 'group_std_dev', 'group_sum',
    'group_neutralize', 'group_cartesian_product',
    'power', 'signed_power', 'log', 'sqrt', 'abs', 'inverse', 'reverse',
    'sign', 'pasteurize', 'densify', 'max', 'min',
    'if_else', 'equal', 'not_equal', 'greater', 'greater_equal',
    'less', 'less_equal', 'or', 'and', 'not', 'is_nan',
    'days_from_last_change', 'last_diff_value', 'kth_element',
    'hump', 'ts_target_tvr_decay', 'ts_target_tvr_hump',
}


def load_settings(campaign_dir):
    p = os.path.join(campaign_dir, "config", "settings.json")
    if not os.path.exists(p):
        raise FileNotFoundError(f"settings.json 不存在: {p}")
    return json.load(open(p, encoding="utf-8"))


def get_cache_path(campaign_dir):
    return os.path.join(campaign_dir, "cache", "gate_cache.json")


def load_cache(campaign_dir):
    p = get_cache_path(campaign_dir)
    try:
        return json.load(open(p, encoding="utf-8"))
    except Exception:
        return {}


def save_cache(campaign_dir, c):
    p = get_cache_path(campaign_dir)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    tmp = p + ".tmp"
    json.dump(c, open(tmp, "w", encoding="utf-8"), ensure_ascii=False)
    os.replace(tmp, p)


def cache_key(dataset, expr):
    return hashlib.sha1(f"{dataset}\n{expr}".encode()).hexdigest()


def load_whitelist(campaign_dir, region, dataset):
    """typed catalog 优先，legacy 白名单兜底。"""
    cat = os.path.join(campaign_dir, "reference", f"{region.lower()}_{dataset}_fields.json")
    if os.path.exists(cat):
        d = json.load(open(cat, encoding="utf-8"))
        fts = {f["id"]: f.get("type") for f in d.get("fields", [])}
        # 横截面股票覆盖检查 (2026-08-18 wave34 教训)
        low_stock_coverage = d.get("low_stock_coverage", False)
        estimated_stock_count = d.get("estimated_stock_count", 0)
        return set(fts), d.get("data_type", "MATRIX"), fts, d.get("banned_patterns", []), low_stock_coverage, estimated_stock_count
    wl = os.path.join(campaign_dir, "reference", f"{region.lower()}_{dataset}_field_whitelist.json")
    if os.path.exists(wl):
        d = json.load(open(wl, encoding="utf-8"))
        if "verified_fields" in d:
            return set(d["verified_fields"]), d.get("data_type", "MATRIX"), {}, d.get("banned_patterns", []), False, 0
        fts = {f["id"]: f.get("type") for f in d.get("fields", [])}
        return set(fts), d.get("data_type", "MATRIX"), fts, d.get("banned_patterns", []), False, 0
    raise FileNotFoundError(f"无白名单/catalog：先跑 scan_fields.py --campaign-dir {campaign_dir} --dataset {dataset}")


def fn_spans(expr):
    """解析全部函数调用区间 -> [(start, end, fn_name)]。"""
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


def naked_vector_fields(expr, fields, field_types):
    """字段级 type==VECTOR 且未被 vec_* 直接包裹的字段列表。"""
    spans = fn_spans(expr)
    naked = []
    for f in fields:
        if field_types.get(f) != "VECTOR":
            continue
        for m in re.finditer(r"\b" + re.escape(f) + r"\b", expr):
            inner = min((sp for sp in spans if sp[0] <= m.start() < sp[1]),
                        key=lambda sp: sp[1] - sp[0], default=None)
            if inner is None or inner[2] not in VEC_WRAP_OPS:
                naked.append(f)
                break
    return sorted(set(naked))


def legacy_strip_naked(expr, fields):
    """legacy 白名单无字段级 type 时的 strip 启发式。"""
    stripped = expr
    for op in VEC_WRAP_OPS:
        for m in list(re.finditer(op + r"\(", stripped)):
            depth, j = 0, m.end() - 1
            while j < len(stripped):
                if stripped[j] == "(":
                    depth += 1
                elif stripped[j] == ")":
                    depth -= 1
                    if depth == 0:
                        break
                j += 1
            stripped = stripped[:m.start()] + " " * (j - m.start() + 1) + stripped[j + 1:]
    return sorted({f for f in fields if re.search(r"\b" + re.escape(f) + r"\b", stripped)})


def _is_leaf_expr(expr):
    """判断是否为叶子节点(非函数调用)"""
    return not re.match(r'^\s*[a-zA-Z_][a-zA-Z0-9_]*\s*\(', expr.strip())


def _split_args_simple(s):
    """简单参数分割(不考虑嵌套引号)"""
    args, depth, cur = [], 0, ''
    for ch in s:
        if ch in '([':
            depth += 1
        elif ch in ')]':
            depth -= 1
        if ch == ',' and depth == 0:
            args.append(cur.strip())
            cur = ''
            continue
        cur += ch
    if cur.strip():
        args.append(cur.strip())
    return args


def vector_forbidden_wrap_fields(expr, fields, field_types):
    """检测 VECTOR 字段被禁止算子直接包裹 (2026-08-18 wave34 教训)
    
    若字段类型=VECTOR 且被 ts_backfill/ts_delta/divide/subtract/add 等直接包裹 → 报错
    这些算子直接包裹 VECTOR 字段会报 "does not support event inputs"
    """
    if not field_types:
        return []
    
    # 提取所有 VECTOR 字段
    vector_fields = {f for f, t in field_types.items() if t == 'VECTOR'}
    if not vector_fields:
        return []
    
    issues = []
    
    # 递归检查表达式
    def _walk(e, path=''):
        m = re.match(r'^\s*([a-zA-Z_][a-zA-Z0-9_]*)\s*\((.*)\)\s*$', e, re.S)
        if not m:
            return
        name, inner = m.group(1), m.group(2)
        loc = path + name
        
        # 检查当前算子是否禁止直接包裹 VECTOR 字段
        if name in VECTOR_FORBIDDEN_OPS:
            args = _split_args_simple(inner)
            for a in args:
                if _is_leaf_expr(a):
                    a_name = a.strip().split('=')[-1].strip() if '=' in a else a.strip()
                    if a_name in vector_fields:
                        issues.append(
                            f'[TYPE] VECTOR 字段 "{a_name}" 不能被 {name} 直接包裹 '
                            f'(event 输入不支持, 会报 "does not support event inputs"); '
                            f'请先用 vec_avg/vec_sum 聚合: {name}(vec_avg({a_name}), ...)'
                        )
        
        # 递归检查参数
        args = _split_args_simple(inner)
        for a in args:
            _walk(a, loc + '>')
    
    _walk(expr)
    return issues


def check_one(expr, wl, dataset, poison_patterns, fix=False):
    verified, data_type, field_types, banned, low_stock_coverage, estimated_stock_count = wl
    fixed_expr = None
    # --fix: VECTOR 数据集下先把裸用的 VECTOR 字段自动裹上 vec_* 再检测（幂等）
    if fix and data_type == "VECTOR" and field_types:
        vfields = [f for f, t in field_types.items() if t == "VECTOR"]
        new_expr, wrapped = wrap_naked_vectors(expr, vfields)
        if wrapped:
            fixed_expr = new_expr
            expr = new_expr
    issues = []
    # 闸1 语法
    try:
        r = get_validator().check_expression(expr)
        if not r.get("valid"):
            issues.append(f"[SYNTAX] {r.get('errors')}")
    except Exception as e:
        issues.append(f"[SYNTAX] verifier error: {e}")
    idents = set(re.findall(r"[a-zA-Z_][a-zA-Z0-9_]*", expr))
    fields = idents - KNOWN_OPS - GROUP_IDENTIFIERS - PRICE_VOLUME - DRIVER_ARGS
    ops_used = idents & KNOWN_OPS
    # 闸2 白名单
    unknown = sorted(fields - verified)
    if unknown:
        issues.append(f"[FIELD] 未验证字段: {unknown}")
    # 闸2.5 横截面股票覆盖检查 (2026-08-18 wave34 教训)
    if low_stock_coverage:
        issues.append(f"[COVERAGE] 数据集横截面股票覆盖不足: 预估 {estimated_stock_count} 个 < 100, 易致 CONCENTRATED_WEIGHT/信号稀疏")
    # 闸3 类型
    if data_type == "MATRIX":
        bad = ops_used & VECTOR_ONLY_OPS
        if bad:
            issues.append(f"[TYPE] MATRIX 数据集禁用 vec_*: {sorted(bad)}")
    elif data_type == "VECTOR" and fields:
        naked = (naked_vector_fields(expr, fields, field_types) if field_types
                 else legacy_strip_naked(expr, fields))
        if naked:
            issues.append(f"[EVENT] 事件型字段必须经 vec_* 聚合: {naked}")
    # 闸3.5 VECTOR 字段禁止直接包裹检查 (2026-08-18 wave34 教训)
    # 若字段类型=VECTOR 且被 ts_backfill/ts_delta/divide/subtract/add 等直接包裹 → 报错
    forbidden_wrap = vector_forbidden_wrap_fields(expr, fields, field_types)
    issues.extend(forbidden_wrap)
    # 闸4 不可访问算子 + quantile arity + banned_patterns
    inac = idents & INACCESSIBLE_OPS
    if inac:
        issues.append(f"[INACCESSIBLE] 平台不可访问算子(整批CANCELLED元凶): {sorted(inac)}")
    for qm in re.finditer(r"quantile\(", expr):
        depth, args, i = 0, 1, qm.end()
        while i < len(expr) and depth >= 0:
            c = expr[i]
            if c == "(":
                depth += 1
            elif c == ")":
                depth -= 1
            elif c == "," and depth == 0:
                args += 1
            i += 1
        if args != 1:
            issues.append(f"[ARITY] quantile 仅 1 参, 当前 {args}")
    for bp in banned:
        scope = bp.get("scope", "all")
        if scope == "vector_dataset" and data_type == "MATRIX":
            continue
        if re.search(bp["pattern"], expr):
            issues.append(f"[BANNED] {bp.get('reason', bp['pattern'])}")
    # 闸5 毒模式
    for pp in poison_patterns:
        if re.search(pp["regex"], expr):
            issues.append(f"[POISON:{pp['name']}] {pp['rule']}")
    out = {"fields": sorted(fields), "issues": issues, "pass": not issues}
    if fixed_expr is not None:
        out["fixed_expr"] = fixed_expr
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--campaign-dir", required=True, help="战役根目录 (如 tracking/EUR)")
    ap.add_argument("--file")
    ap.add_argument("--expr")
    ap.add_argument("--dataset", required=True)
    ap.add_argument("--no-cache", action="store_true")
    ap.add_argument("--fix", action="store_true",
                    help="自动修复：VECTOR 数据集下裸用的 VECTOR 字段裹上 vec_* 后再检测（幂等）")
    a = ap.parse_args()

    settings = load_settings(a.campaign_dir)
    region = settings["region"]

    if a.file:
        d = json.load(open(a.file, encoding="utf-8"))
        exprs = d if isinstance(d, list) else (d.get("expressions") or d.get("exprs") or [])
    elif a.expr:
        exprs = [a.expr]
    else:
        ap.error("need --file or --expr")
    # 支持 [{code, note}] 或纯字符串列表
    exprs = [e.get("code") if isinstance(e, dict) else e for e in exprs]
    exprs = [e for e in exprs if isinstance(e, str)]

    wl = load_whitelist(a.campaign_dir, region, a.dataset)
    cons_path = os.path.join(a.campaign_dir, "reference", f"{region.lower()}_generation_constraints.json")
    poison = json.load(open(cons_path, encoding="utf-8")).get("poison_patterns", []) \
        if os.path.exists(cons_path) else []
    # --fix 会改写表达式，缓存键与原始表达式不一致，禁用缓存以免污染
    use_cache = not a.no_cache and not a.fix
    cache = {} if not use_cache else load_cache(a.campaign_dir)
    dirty = False
    report, all_pass = [], True
    for i, e in enumerate(exprs, 1):
        ck = cache_key(a.dataset, e)
        if use_cache and ck in cache:
            item = dict(cache[ck])
            item["index"] = i
            item["cached"] = True
        else:
            item = check_one(e, wl, a.dataset, poison, fix=a.fix)
            item["index"] = i
            if use_cache:
                cache[ck] = {k: item[k] for k in ("fields", "issues", "pass")}
                dirty = True
        all_pass = all_pass and item["pass"]
        report.append(item)
    if dirty and use_cache:
        save_cache(a.campaign_dir, cache)
    print(json.dumps({"all_pass": all_pass, "dataset": a.dataset, "total": len(exprs),
                      "passed": sum(r["pass"] for r in report),
                      "cached": sum(1 for r in report if r.get("cached")),
                      "report": report}, ensure_ascii=False, indent=1))
    sys.exit(0 if all_pass else 1)


if __name__ == "__main__":
    main()
