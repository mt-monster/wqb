# -*- coding: utf-8 -*-
"""pipeline_pregate.py - 生成侧预闸（2026-09-15 ②：把闸门里最高频的两类 FAIL 前移到生成器）。

审计实证（832 份 gate_results）：
  - `[ARITY] quantile 仅 1 参` 312 次命中——其中 481/499 是 `quantile(x, driver="gaussian")`
    （含 `sigma=1.0`）。gaussian 正是平台默认 driver，`quantile(x)` 与之**语义完全相同**，
    所以这里做无损归一化，而不是丢弃。其他 driver（cauchy/uniform）保持原样交给闸门。
  - `[POISON:weighted_leg_mix_*]` / `nested_three_leg_add` 74 次——用户 2026-09-09 定案的
    全局纪律（禁 add(multiply(w,A),multiply(w,B)) 混信号调参）。生成器落盘前直接丢弃，
    规则正则与 toolkit `config/platform_constraints.json` 同源（不复制一份数字）。

纯标准库。找不到 platform_constraints.json 时毒模式检查静默降级（只做 quantile 归一化）。
"""
from __future__ import annotations

import json
import os
import re

try:  # 同目录 skill_roots（与 toolkit _lib/skill_roots.py 同序）
    from skill_roots import candidate_paths_under_skill
except Exception:  # pragma: no cover - 离线/被单独 import 时
    candidate_paths_under_skill = None

_QUANTILE_RE = re.compile(r"(?<![A-Za-z0-9_])quantile\(")
#: 可无损删除的尾参：driver="gaussian"（平台默认）± sigma=1.0（平台默认）
_DEFAULT_TAIL_RE = re.compile(
    r'^\s*driver\s*=\s*"?gaussian"?\s*(?:,\s*sigma\s*=\s*1(?:\.0+)?\s*)?$'
)


def _split_args(expr: str, start: int):
    """从 start（紧跟 '(' 之后）扫描到匹配的 ')'；返回 (args: list[str], end_index)。"""
    depth, i, cur, parts = 0, start, start, []
    while i < len(expr):
        c = expr[i]
        if c == "(":
            depth += 1
        elif c == ")":
            if depth == 0:
                parts.append(expr[cur:i])
                return parts, i
            depth -= 1
        elif c == "," and depth == 0:
            parts.append(expr[cur:i])
            cur = i + 1
        i += 1
    return None, -1


def normalize_quantile(expr: str):
    """`quantile(x, driver="gaussian"[, sigma=1.0])` → `quantile(x)`（语义不变）。返回 (expr, n_changed)。"""
    out, n, pos = expr, 0, 0
    while True:
        m = _QUANTILE_RE.search(out, pos)
        if not m:
            break
        args, end = _split_args(out, m.end())
        if args is None:
            break
        if len(args) > 1 and _DEFAULT_TAIL_RE.match(",".join(args[1:]).strip()):
            out = out[: m.end()] + args[0].strip() + out[end:]
            n += 1
        pos = m.end()
    return out, n


# ---------------------------------------------------------------- 2026-09-19 新增三类预闸
# 实证（IND w171/w172、JPN w7）：GEM 反复渲染 `hump(x, 0.01)`（位置参数，平台只认 hump=）、
# `bucket(rank(x))`（缺 range/buckets，平台 ERROR 且整批连坐）、以及区域不存在的 group 字段
# （JPN 无 sector/subindustry/industry）。三者都是"生成层就能确定"的平台约束，
# 却一路裸奔到 wave_gate（hump 能拦、bucket 拦不住）甚至仿真（连坐 CANCELLED）。
# 另：CLAUDE.md 只允许 1/5/22/66/252/504/1008/1260 标准窗，GEM 却大量产 20/60/63/250，
# 这里对"明显是标准窗口近似值"的做无损归一化，其他非标窗保留交闸门 WARN。

_NAMED_ONLY_RE = re.compile(r"(?<![A-Za-z0-9_])(hump)\(")
_BUCKET_RE = re.compile(r"(?<![A-Za-z0-9_])bucket\(")
_NUM_RE = re.compile(r"^\s*-?\d+(?:\.\d+)?\s*$")

#: 非标窗 → 标准窗（只归一"数值上贴着标准窗"的；差距大的不动，留给闸门告警）
WINDOW_ALIASES = {20: 22, 21: 22, 60: 66, 63: 66, 65: 66, 250: 252, 255: 252,
                  500: 504, 1000: 1008, 1250: 1260}
STANDARD_WINDOWS = (1, 5, 22, 66, 252, 504, 1008, 1260)
#: 第 N 个位置参数是窗口的时序算子（N 从 0 起）；只归一这些位置，不碰阈值/常数
_TS_WINDOW_ARG = {
    "ts_mean": 1, "ts_sum": 1, "ts_std_dev": 1, "ts_zscore": 1, "ts_rank": 1, "ts_delta": 1,
    "ts_delay": 1, "ts_decay_linear": 1, "ts_backfill": 1, "ts_av_diff": 1, "ts_ir": 1,
    "ts_max": 1, "ts_min": 1, "ts_arg_max": 1, "ts_arg_min": 1, "ts_product": 1,
    "ts_scale": 1, "ts_quantile": 1, "ts_kurtosis": 1, "ts_skewness": 1, "ts_count_nans": 1,
    "ts_returns": 1, "ts_max_diff": 1, "ts_corr": 2, "ts_covariance": 2, "ts_regression": 2,
}
_TS_CALL_RE = re.compile(r"(?<![A-Za-z0-9_])(" + "|".join(sorted(_TS_WINDOW_ARG, key=len, reverse=True)) + r")\(")
_GROUP_FIELD_RE_TPL = r"(?<![A-Za-z0-9_])(?:%s)(?![A-Za-z0-9_])"


def normalize_named_only(expr: str):
    """`hump(x, 0.01)` → `hump(x, hump=0.01)`（平台签名 hump(x, hump=...)，位置参数报 ARITY）。
    返回 (expr, n_changed)。"""
    out, n, pos = expr, 0, 0
    while True:
        m = _NAMED_ONLY_RE.search(out, pos)
        if not m:
            break
        args, end = _split_args(out, m.end())
        if args is None:
            break
        if len(args) == 2 and _NUM_RE.match(args[1]):
            fn = m.group(1)
            out = out[: m.end()] + args[0].strip() + f", {fn}=" + args[1].strip() + out[end:]
            n += 1
        pos = m.end()
    return out, n


def normalize_bucket(expr: str):
    """`bucket(rank(x))`（缺 range/buckets）→ `bucket(rank(x), range="0,1,0.1")`；
    输入不是 rank(...)（值域未知）时不补默认值，返回 (expr, n_changed, n_unfixable)。"""
    out, n, bad, pos = expr, 0, 0, 0
    while True:
        m = _BUCKET_RE.search(out, pos)
        if not m:
            break
        args, end = _split_args(out, m.end())
        if args is None:
            break
        tail = ",".join(args[1:])
        if "range" not in tail and "buckets" not in tail:
            if args[0].strip().startswith("rank("):
                out = out[: m.end()] + args[0].strip() + ', range="0,1,0.1"' + out[end:]
                n += 1
            else:
                bad += 1
        pos = m.end()
    return out, n, bad


def normalize_windows(expr: str):
    """时序算子窗口位置的非标准值 → 最近标准窗（只按 WINDOW_ALIASES 表，无损近似）。
    返回 (expr, n_changed, remaining_nonstandard: list[int])。"""
    out, n, pos = expr, 0, 0
    remaining = []
    while True:
        m = _TS_CALL_RE.search(out, pos)
        if not m:
            break
        fn = m.group(1)
        args, end = _split_args(out, m.end())
        if args is None:
            break
        k = _TS_WINDOW_ARG[fn]
        if len(args) > k and _NUM_RE.match(args[k]) and "." not in args[k]:
            w = int(args[k].strip())
            if w in WINDOW_ALIASES:
                args[k] = " " + str(WINDOW_ALIASES[w])
                out = out[: m.end()] + ",".join(args) + out[end:]
                n += 1
            elif w not in STANDARD_WINDOWS:
                remaining.append(w)
        pos = m.end()
    return out, n, remaining


_SKEL_NUM_RE = re.compile(r"(?<![A-Za-z0-9_])-?\d+(?:\.\d+)?(?![A-Za-z0-9_])")
_SKEL_ID_RE = re.compile(r"[A-Za-z_][A-Za-z0-9_]*")
_SKEL_KW_RE = re.compile(r"([A-Za-z_][A-Za-z0-9_]*)\s*=")


def skeleton_signature(expr: str) -> str:
    """骨架签名：字段 → F、数字 → N、算子/命名参数名/group 关键字保留。
    同签名 = 同一机制的字段替换变体（JPN analyst_revision_horizons 实证：1026 字段 × 模板
    渲染出 7538 条，几乎全是同骨架换字段）。"""
    kws = set(_SKEL_KW_RE.findall(expr))
    ops = set(re.findall(r"([A-Za-z_][A-Za-z0-9_]*)\s*\(", expr))
    keep = ops | kws | {"industry", "sector", "subindustry", "market", "country", "exchange", "gaussian", "cauchy", "uniform"}

    def _id(m):
        t = m.group(0)
        return t if t in keep else "F"
    out = _SKEL_NUM_RE.sub("N", expr)
    out = _SKEL_ID_RE.sub(_id, out)
    return re.sub(r"\s+", "", out)


def cap_per_skeleton(expressions, max_per_skeleton: int):
    """每个骨架签名最多保留 max_per_skeleton 条（保序，先到先得）。返回 (kept, n_dropped, n_skeletons)。"""
    if not max_per_skeleton or max_per_skeleton <= 0:
        return list(expressions), 0, 0
    count = {}
    kept, dropped = [], 0
    for e in expressions:
        k = skeleton_signature(e)
        c = count.get(k, 0)
        if c >= max_per_skeleton:
            dropped += 1
            continue
        count[k] = c + 1
        kept.append(e)
    return kept, dropped, len(count)


def region_invalid_group_fields(region: str | None):
    """区域不可用的 group 字段（profile 硬事实）。JPN 2026-09-15 实测：sector/subindustry/
    industry 是 'Invalid data field'（POST 可接受，执行必 ERROR 并连坐）。
    可用环境变量 WQB_INVALID_GROUP_FIELDS="a,b" 覆盖/补充（逗号分隔）。"""
    table = {"JPN": ("sector", "subindustry", "industry")}
    fields = list(table.get((region or "").upper(), ()))
    env = os.environ.get("WQB_INVALID_GROUP_FIELDS")
    if env:
        fields += [x.strip() for x in env.split(",") if x.strip()]
    return tuple(dict.fromkeys(fields))


def region_invalid_fields(region: str | None):
    """区域不可用的普通字段（profile 硬事实）。JPN/TOP1600/D1 2026-09-19 实测：**没有 pv1 数据集**，
    close/open/high/low/volume/returns/vwap/cap/sharesout/adv20 全部 'Invalid data field close'。
    可用环境变量 WQB_INVALID_FIELDS="a,b" 覆盖/补充。"""
    table = {"JPN": ("close", "open", "high", "low", "volume", "returns", "vwap", "cap",
                     "sharesout", "adv20", "adv60", "adv120")}
    fields = list(table.get((region or "").upper(), ()))
    env = os.environ.get("WQB_INVALID_FIELDS")
    if env:
        fields += [x.strip() for x in env.split(",") if x.strip()]
    return tuple(dict.fromkeys(fields))


#: ts_*(...vec_*(...)) 在这些区域必 ERROR（JPN 2026-09-19 实证：rank(vec_avg(f)) COMPLETE，
#: 其上任何 ts_delta/ts_delay/ts_zscore/ts_backfill 链均 'Invalid data field close'——VECTOR 日频对齐依赖 pv1）
_VECTOR_TS_FORBIDDEN_REGIONS = ("JPN",)
_TS_OVER_VEC_RE = re.compile(r"\bts_[a-z_]+\s*\((?:[^()]|\([^()]*\))*?\bvec_[a-z]+\s*\(")


def vector_ts_forbidden(region: str | None) -> bool:
    env = os.environ.get("WQB_VECTOR_TS_FORBIDDEN_REGIONS")
    regions = tuple(x.strip().upper() for x in env.split(",")) if env else _VECTOR_TS_FORBIDDEN_REGIONS
    return (region or "").upper() in regions


def has_ts_over_vec(expr: str) -> bool:
    """任一 ts_* 调用的实参文本里出现 vec_*(（允许一层嵌套括号）。"""
    if "vec_" not in expr or "ts_" not in expr:
        return False
    if _TS_OVER_VEC_RE.search(expr):
        return True
    # 深嵌套兜底：逐个 ts_ 调用取完整括号体
    for m in re.finditer(r"\bts_[a-z_]+\s*\(", expr):
        depth, i = 0, m.end() - 1
        while i < len(expr):
            if expr[i] == "(":
                depth += 1
            elif expr[i] == ")":
                depth -= 1
                if depth == 0:
                    break
            i += 1
        if "vec_" in expr[m.end():i]:
            return True
    return False


def load_poison_patterns():
    """从 toolkit config/platform_constraints.json 读 severity=block 的毒模式正则。"""
    paths = []
    env = os.environ.get("WQ_TOOLKIT_DIR")
    if env:
        paths.append(os.path.join(env, "..", "config", "platform_constraints.json"))
        paths.append(os.path.join(env, "config", "platform_constraints.json"))
    if candidate_paths_under_skill:
        paths.extend(candidate_paths_under_skill(
            "wq-brain-campaign-toolkit", "config", "platform_constraints.json"))
    for p in paths:
        p = os.path.normpath(p)
        if not os.path.isfile(p):
            continue
        try:
            with open(p, "r", encoding="utf-8-sig") as f:
                d = json.load(f)
        except Exception:
            continue
        pats = []
        for pp in d.get("poison_patterns") or []:
            if not isinstance(pp, dict) or pp.get("severity", "block") != "block":
                continue
            try:
                pats.append((pp.get("name") or "?", re.compile(pp["regex"])))
            except Exception:
                continue
        return pats, p
    return [], None


def pregate(expressions, log=print, region=None, normalize_window=True, max_per_skeleton=None):
    """生成侧预闸：quantile 无损归一化 + 毒模式丢弃
    + （2026-09-19）hump 命名参数归一 / bucket 缺 range 补默认或丢弃 / 区域非法 group 字段丢弃
    / 非标窗口归一到最近标准窗 / 同骨架换字段变体封顶（max_per_skeleton，默认读环境变量
    WQB_GEM_MAX_PER_SKELETON，缺省 12；0 关闭）。返回 (kept, report)。"""
    if max_per_skeleton is None:
        try:
            max_per_skeleton = int(os.environ.get("WQB_GEM_MAX_PER_SKELETON", "12"))
        except ValueError:
            max_per_skeleton = 12
    poison, src = load_poison_patterns()
    bad_groups = region_invalid_group_fields(region)
    bad_group_re = re.compile(_GROUP_FIELD_RE_TPL % "|".join(map(re.escape, bad_groups))) if bad_groups else None
    bad_fields = region_invalid_fields(region)
    bad_field_re = re.compile(r"\b(?:%s)\b" % "|".join(map(re.escape, bad_fields))) if bad_fields else None
    vec_ts_bad = vector_ts_forbidden(region)
    kept, dropped, n_norm = [], [], 0
    n_named = n_bucket = n_bucket_bad = n_win = n_group = n_field = n_vec_ts = 0
    nonstd = {}
    seen = set()
    for e in expressions:
        if not isinstance(e, str) or not e.strip():
            continue
        e2, n = normalize_quantile(e.strip())
        n_norm += n
        e2, n = normalize_named_only(e2)
        n_named += n
        e2, n, bad = normalize_bucket(e2)
        n_bucket += n
        if bad:
            n_bucket_bad += 1
            dropped.append(("bucket_missing_range", e2))
            continue
        if bad_group_re and bad_group_re.search(e2):
            n_group += 1
            dropped.append(("region_invalid_group_field", e2))
            continue
        if bad_field_re and bad_field_re.search(e2):
            n_field += 1
            dropped.append(("region_invalid_field", e2))
            continue
        if vec_ts_bad and has_ts_over_vec(e2):
            n_vec_ts += 1
            dropped.append(("region_vector_ts_forbidden", e2))
            continue
        if normalize_window:
            e2, n, rem = normalize_windows(e2)
            n_win += n
            for w in rem:
                nonstd[w] = nonstd.get(w, 0) + 1
        hit = next((name for name, rx in poison if rx.search(e2)), None)
        if hit:
            dropped.append((hit, e2))
            continue
        if e2 in seen:
            continue
        seen.add(e2)
        kept.append(e2)
    _NON_POISON = ("bucket_missing_range", "region_invalid_group_field",
                   "region_invalid_field", "region_vector_ts_forbidden")
    n_poison = sum(1 for name, _ in dropped if name not in _NON_POISON)
    kept, n_skel_dropped, n_skel = cap_per_skeleton(kept, max_per_skeleton)
    report = {"in": len(expressions), "kept": len(kept), "quantile_normalized": n_norm,
              "poison_dropped": n_poison, "poison_source": src,
              "named_arg_normalized": n_named, "bucket_range_added": n_bucket,
              "bucket_dropped": n_bucket_bad, "invalid_group_dropped": n_group,
              "invalid_field_dropped": n_field, "vector_ts_dropped": n_vec_ts,
              "windows_normalized": n_win, "nonstandard_windows": nonstd,
              "skeleton_capped": n_skel_dropped, "skeletons": n_skel,
              "max_per_skeleton": max_per_skeleton}
    if n_skel_dropped:
        log(f"[pregate] 同骨架换字段变体封顶 {max_per_skeleton}/骨架：{n_skel} 个骨架，丢弃 {n_skel_dropped} 条模板展开")
    if n_norm:
        log(f"[pregate] quantile 默认 driver 归一化 {n_norm} 处（quantile(x, driver=\"gaussian\") → quantile(x)，语义不变）")
    if n_named:
        log(f"[pregate] hump 位置参数 → 命名参数 {n_named} 处（hump(x, k) → hump(x, hump=k)）")
    if n_bucket or n_bucket_bad:
        log(f"[pregate] bucket 缺 range：rank 输入补 range=\"0,1,0.1\" {n_bucket} 处，非 rank 输入丢弃 {n_bucket_bad} 条")
    if n_group:
        log(f"[pregate] 区域 {region} 非法 group 字段 {bad_groups} 丢弃 {n_group} 条")
    if n_win:
        log(f"[pregate] 非标窗口归一到标准窗 {n_win} 处（{WINDOW_ALIASES}）")
    if nonstd:
        log(f"[pregate] warn: 仍含非标准窗口（CLAUDE.md 要求给出经济含义或实测证据）: "
            f"{dict(sorted(nonstd.items()))}")
    if n_poison:
        log(f"[pregate] 毒模式丢弃 {n_poison} 条（规则源 {src}）:")
        for name, ex in [d for d in dropped if d[0] not in _NON_POISON][:8]:
            log(f"[pregate]   - [{name}] {ex[:110]}")
    elif src is None:
        log("[pregate] warn: 未找到 platform_constraints.json，毒模式预闸未生效（闸5 仍会兜底）")
    return kept, report
