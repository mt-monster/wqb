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
    r"C:\Users\MENGTAO\.workbuddy\skills\alpha-expression-verifier\scripts",
    r"D:\coding\traeCN_project\wqb\.cursor\skills\alpha-expression-verifier\scripts",
    r"C:\Users\MENGTAO\.qoder-cn\skills\alpha-expression-verifier\scripts",
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
KNOWN_OPS = {op for ops in OP_FAMILIES.values() for op in ops}
VECTOR_ONLY_OPS = {"vec_avg", "vec_max", "vec_min", "vec_sum", "vec_count", "vec_norm"}
VEC_WRAP_OPS = ("vec_avg", "vec_max", "vec_min", "vec_sum", "vec_count", "vec_norm")
INACCESSIBLE_OPS = {"ts_min", "ts_max"}
GROUP_IDENTIFIERS = {"sector", "subindustry", "industry", "market", "country", "exchange"}
PRICE_VOLUME = {"open", "high", "low", "close", "volume", "returns", "vwap", "cap", "sharesout", "adv20"}
DRIVER_ARGS = {"gaussian", "uniform", "cauchy"}


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
        return set(fts), d.get("data_type", "MATRIX"), fts, d.get("banned_patterns", [])
    wl = os.path.join(campaign_dir, "reference", f"{region.lower()}_{dataset}_field_whitelist.json")
    if os.path.exists(wl):
        d = json.load(open(wl, encoding="utf-8"))
        if "verified_fields" in d:
            return set(d["verified_fields"]), d.get("data_type", "MATRIX"), {}, d.get("banned_patterns", [])
        fts = {f["id"]: f.get("type") for f in d.get("fields", [])}
        return set(fts), d.get("data_type", "MATRIX"), fts, d.get("banned_patterns", [])
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


def check_one(expr, wl, dataset, poison_patterns):
    verified, data_type, field_types, banned = wl
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
    return {"fields": sorted(fields), "issues": issues, "pass": not issues}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--campaign-dir", required=True, help="战役根目录 (如 tracking/EUR)")
    ap.add_argument("--file")
    ap.add_argument("--expr")
    ap.add_argument("--dataset", required=True)
    ap.add_argument("--no-cache", action="store_true")
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
    cache = {} if a.no_cache else load_cache(a.campaign_dir)
    dirty = False
    report, all_pass = [], True
    for i, e in enumerate(exprs, 1):
        ck = cache_key(a.dataset, e)
        if ck in cache:
            item = dict(cache[ck])
            item["index"] = i
            item["cached"] = True
        else:
            item = check_one(e, wl, a.dataset, poison)
            item["index"] = i
            cache[ck] = {k: item[k] for k in ("fields", "issues", "pass")}
            dirty = True
        all_pass = all_pass and item["pass"]
        report.append(item)
    if dirty and not a.no_cache:
        save_cache(a.campaign_dir, cache)
    print(json.dumps({"all_pass": all_pass, "dataset": a.dataset, "total": len(exprs),
                      "passed": sum(r["pass"] for r in report),
                      "cached": sum(1 for r in report if r.get("cached")),
                      "report": report}, ensure_ascii=False, indent=1))
    sys.exit(0 if all_pass else 1)


if __name__ == "__main__":
    main()
