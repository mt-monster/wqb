# -*- coding: utf-8 -*-
"""_gate_expr_checks.py - gate.py 拆分·表达式级检查核心（2026-11-15 拆分，gate.py 为 facade）。

内容：工作区依赖解析（verifier/op_arity/vector_wrap/family_ceiling）、字段白名单、
check_one（闸1-5 逐条判定）、毒模式结构判定助手、窗口提取、GATE_REGISTRY、
gate_signature/cache_key（逐条缓存指纹）。
mutable 全局（_arity_check/_check_family_ceiling/wrap_naked_vectors）归本模块所有，
_resolve_workspace_deps 在此模块内 late-resolve——其它模块禁止按名快照引用（会被打回），
须用模块引用（import _gate_expr_checks; _gate_expr_checks._arity_check）在调用时读。
"""
import hashlib
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _lib.common import load_json
from _lib.skill_roots import skill_roots as _skill_roots


# 复用工作区 tools/lib 下的 vector_wrap（单一权威源）：--fix 自动裹 vec_* 聚合。
# P1-2 (2026-08-31): 家族天花板预检——复用 src/wqb/expression/validator.py 的
# check_family_ceiling（主导腿信号族占比 ≥2/3 拦截，wave94/95/98/104 实证 SELF≥0.9）。
# 工作区根目录可达时动态导入，不可达则降级跳过（保持 toolkit 独立性）。
def _workspace_src_dirs(campaign_dir=None):
    """工作区 src/ 候选路径——与 `_lib/wqb_store` 同一套工作区解析（2026-09-27 R19 补充）。

    此前：WQB_WORKSPACE_ROOT / WQB_ROOT / WQ_PROJECT_ROOT > 本目录上溯 5 级 > 硬编码盘符。
    "上溯 5 级"在仓库内布局落到仓库的上一级（build_wave 2026-09-09 修过的同一 off-by-one），
    .mcp.json 原样 env 又不含这三个变量（节点注入的是 WQB_WORKSPACE）——op_arity 不可达，
    每条表达式都记 [ARITY_UNKNOWN]，静态闸 39/39 全拦（KOR 真实环境复现；第二轮演练补了
    WQB_ROOT 而没暴露）。现：WQB_WORKSPACE_ROOT（本脚本历史变量名，保留兼容）> 战役目录上溯
    > WQB_WORKSPACE > WQB_ROOT > WQ_PROJECT_ROOT > toolkit 自身上溯 > cwd 上溯 > 历史盘符（仅当真实存在）。
    """
    from _lib.wqb_store import _workspace_roots
    roots = []
    for r in [os.environ.get("WQB_WORKSPACE_ROOT")] + _workspace_roots(campaign_dir):
        if r and r not in roots:
            roots.append(r)
    return [os.path.join(root, "src") for root in roots]


def _load_family_ceiling(campaign_dir=None):
    """尝试导入工作区 validator.check_family_ceiling，不可达返回 None。"""
    for src in _workspace_src_dirs(campaign_dir):
        if os.path.isfile(os.path.join(src, "wqb", "expression", "validator.py")):
            if src not in sys.path:
                sys.path.insert(0, src)
            try:
                from wqb.expression.validator import check_family_ceiling
                return check_family_ceiling
            except Exception:
                return None
    return None

_check_family_ceiling = _load_family_ceiling()


def _load_arity_check(campaign_dir=None):
    """闸1 的算子元数/命名参数检查（catalog 驱动）；不可达返回 None。

    2026-09-07 事故根因：verifier 的 PLY 签名表是手写的，hump 漏标 keyword_only，
    于是 hump(x, 0.005) 一路绿灯烧掉整批 multisim。op_arity 改从平台 catalog 的
    definition 串自动推导签名（``name = <字面量>`` 即命名参数），杜绝手写漏标。
    """
    for src in _workspace_src_dirs(campaign_dir):
        if os.path.isfile(os.path.join(src, "wqb", "expression", "op_arity.py")):
            if src not in sys.path:
                sys.path.insert(0, src)
            try:
                from wqb.expression.op_arity import check_expression as _chk
                return _chk
            except Exception:
                return None
    return None


_arity_check = _load_arity_check()


def _load_call_counter(campaign_dir=None):
    """闸1b-2 的调用点计数器（表达式内 ``name(...)`` 次数）；不可达返回 None。

    与 1b 共用同一个 op_arity 模块，但取的是**另一个函数**：
    1b 用 ``check_expression``（逐调用点验元数/命名参数），
    1c 用 ``iter_call_sites``（数调用点总数）。两者口径不同、不可互相替代。
    """
    for src in _workspace_src_dirs(campaign_dir):
        if os.path.isfile(os.path.join(src, "wqb", "expression", "op_arity.py")):
            if src not in sys.path:
                sys.path.insert(0, src)
            try:
                from wqb.expression.op_arity import iter_call_sites
                return iter_call_sites
            except Exception:
                return None
    return None


_call_counter = _load_call_counter()

#: 闸1b-2 阈值：表达式内函数调用点数必须 **< 10**（铁律口径=函数调用计数，2026-10-03）。
#:
#: 为什么是「调用点数」而不是平台返回的 distinct operator_count：
#: 两者语义不同——`ts_rank(ts_delta(group_rank(x)))` 只有 3 个不同算子、
#: 但有 3 个调用点；而同一算子嵌套两次（如 `ts_zscore(ts_zscore(x))`）
#: distinct=1 而调用点=2。铁律要拦的是**结构复杂度**，故按调用点计。
#:
#: 阈值取 10（非 15/20）的实证依据（2026-10-03 实测真实 DB）：
#: 全库 expressions 73,182 条中 ≥10 调用点占 **8.2%**；
#: 但 **sharpe ≥ 1.58 的达标行中 ≥10 调用点的占 0%（0/32）**
#: ⇒ 卡 10 不会拦掉任何已达标候选，与平台实际产出无冲突。
MAX_OP_CALLS = 10


def _find_tools_lib(campaign_dir=None):
    """工作区 tools/lib（vector_wrap 单一权威源）：WQB_TOOLS_LIB > 与 src/ 同一套工作区候选。"""
    env = os.environ.get("WQB_TOOLS_LIB")
    if env and os.path.isfile(os.path.join(env, "vector_wrap.py")):
        return env
    for src in _workspace_src_dirs(campaign_dir):
        c = os.path.join(os.path.dirname(src), "tools", "lib")
        if os.path.isfile(os.path.join(c, "vector_wrap.py")):
            return c
    return None


def _load_vector_wrap(campaign_dir=None):
    lib = _find_tools_lib(campaign_dir)
    if not lib:
        return None
    if lib not in sys.path:
        sys.path.insert(0, lib)
    try:
        from vector_wrap import wrap_naked_vectors as _wrap
        return _wrap
    except Exception:
        return None


wrap_naked_vectors = _load_vector_wrap()

#: 闸门环境缺失（verifier / op_arity 不可达）的逐条标记：说明"没校验"，不是表达式本身的缺陷。
#: 带这些标记的结论不进逐条缓存（环境修好后必须重判）；wave_gate 回写时不据此判 fail。
ENV_UNKNOWN_TAGS = ("[SYNTAX_UNKNOWN]", "[ARITY_UNKNOWN]")


def env_unknown(issues):
    return any(str(i).startswith(ENV_UNKNOWN_TAGS) for i in (issues or []))


def _resolve_workspace_deps(campaign_dir):
    """模块加载时还不知道战役目录；那时没解析到的工作区依赖，按战役目录上溯再解析一次。"""
    global _arity_check, _call_counter, _check_family_ceiling, wrap_naked_vectors
    if _arity_check is None:
        _arity_check = _load_arity_check(campaign_dir)
    if _call_counter is None:
        _call_counter = _load_call_counter(campaign_dir)
    if _check_family_ceiling is None:
        _check_family_ceiling = _load_family_ceiling(campaign_dir)
    if wrap_naked_vectors is None:
        wrap_naked_vectors = _load_vector_wrap(campaign_dir)

_VALIDATOR = None


def _validator_dirs():
    """verifier 候选目录（顺序由 `_lib/skill_roots.py` 单源维护，2026-09-11 收敛）。

    历史：此处曾内联 3 个历史安装位、漏了主安装位 `~/.claude/skills` 与仓库副本。
    """
    dirs = [os.environ.get("WQ_VALIDATOR_DIR")]
    dirs += [os.path.join(root, "alpha-expression-verifier", "scripts")
             for root in _skill_roots()]
    return dirs


def get_validator():
    """闸1 verifier；缺失返回 None（调用方标 SYNTAX_UNKNOWN，绝不静默放过）。"""
    global _VALIDATOR
    if _VALIDATOR is not None:
        return _VALIDATOR or None
    for d in _validator_dirs():
        if d and os.path.isfile(os.path.join(d, "validator.py")):
            sys.path.insert(0, d)
            from validator import ExpressionValidator
            _VALIDATOR = ExpressionValidator()
            # 查找顺序里主目录已安装副本在仓库副本之前（旧拷贝可能落后）：每个进程打印一次所用路径，
            # 让「验证行为」可复现；写 stderr，不污染 stdout 的 JSON 报告（skills 审查 TR-09）
            print(f"[gate] 闸1 verifier = {d}", file=sys.stderr)
            return _VALIDATOR
    _VALIDATOR = False  # 标记已探测且缺失
    return None


def _ghost_ops(pc):
    """幽灵算子（平台不存在；回测 ERROR 并连坐整批 CANCELLED）。

    并集：platform_constraints.ghost_ops ∪ wqb.config.GHOST_OPERATORS（后者更全，MCP operator_audit 同源）；
    去掉 inaccessible_ops（ts_min/ts_max：平台有但本账号 ERROR，走闸4，不重复报）。
    2026-09-29：此前 ghost 只靠「不在 known_ops → 被当成未验证字段」间接拦下，报错文案是
    「未验证字段」，会把幽灵算子误导成字段问题。
    """
    pre = pc.get("_ghost_all")
    if pre is not None:
        return set(pre)
    names = set(pc.get("ghost_ops") or [])
    try:
        from wqb.config import GHOST_OPERATORS
        names |= set(GHOST_OPERATORS)
    except Exception:
        pass
    return names - set(pc.get("inaccessible_ops") or [])


def load_whitelist(ctx, dataset):
    """typed catalog 优先（DB），legacy 文件兜底。返回 (verified_ids, data_type, field_types, banned)。"""
    try:
        from _lib.wqb_store import load_catalog
        d = load_catalog(ctx, dataset)
        if d and d.get("fields"):
            fts = {f["id"]: f.get("type") for f in d.get("fields", [])}
            return set(fts), d.get("data_type", "MATRIX"), fts, d.get("banned_patterns", [])
    except Exception:
        pass
    cat = ctx.catalog_path(dataset)
    if os.path.exists(cat):
        d = load_json(cat)
        fts = {f["id"]: f.get("type") for f in d.get("fields", [])}
        return set(fts), d.get("data_type", "MATRIX"), fts, d.get("banned_patterns", [])
    wl = ctx.whitelist_path(dataset)
    if os.path.exists(wl):
        d = load_json(wl)
        if "verified_fields" in d:
            return set(d["verified_fields"]), d.get("data_type", "MATRIX"), {}, d.get("banned_patterns", [])
        fts = {f["id"]: f.get("type") for f in d.get("fields", [])}
        return set(fts), d.get("data_type", "MATRIX"), fts, d.get("banned_patterns", [])
    raise FileNotFoundError(
        f"无白名单/catalog：先跑 scan_fields.py --campaign-dir {ctx.dir} --dataset {dataset}")


def merge_whitelists(ctx, datasets):
    """合并多个 typed catalog，供跨金字塔慢×快表达式一次过闸 2。"""
    ids, fts, banned = set(), {}, []
    dtype = "MATRIX"
    for ds in datasets:
        if not ds:
            continue
        w, dt, ft, bn = load_whitelist(ctx, ds)
        ids |= w
        fts.update(ft)
        banned.extend(bn or [])
        # 修复（2026-09-01）：原 `dt == "VECTOR" and not fts` 中 not fts 恒为 False，
        # 合并后 dtype 恒 MATRIX 导致 --fix 的 VECTOR 包裹分支永不触发；改为按字段级类型判定
        if dt == "VECTOR" or any(t == "VECTOR" for t in ft.values()):
            dtype = "VECTOR"
    return ids, dtype, fts, banned


def fn_spans(expr):
    """解析全部函数调用区间 -> [(start, end, fn_name)]（数据驱动 VECTOR 包裹判定）。"""
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


def naked_vector_fields(expr, fields, field_types, vec_wrap_ops):
    """字段级 type==VECTOR 且未被 vec_* 直接包裹的字段列表（数据驱动）。"""
    spans = fn_spans(expr)
    naked = []
    for f in fields:
        if field_types.get(f) != "VECTOR":
            continue
        for m in re.finditer(r"\b" + re.escape(f) + r"\b", expr):
            inner = min((sp for sp in spans if sp[0] <= m.start() < sp[1]),
                        key=lambda sp: sp[1] - sp[0], default=None)
            if inner is None or inner[2] not in vec_wrap_ops:
                naked.append(f)
            break
    return sorted(set(naked))


def legacy_strip_naked(expr, fields, vec_wrap_ops):
    """legacy 白名单无字段级 type 时的 strip 启发式。"""
    stripped = expr
    for op in vec_wrap_ops:
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



def _ts_over_vec(expr: str) -> bool:
    """任一 ts_* 调用的括号体内出现 vec_*(（JPN 2026-09-19 实证必 ERROR）。"""
    if "vec_" not in expr or "ts_" not in expr:
        return False
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

def check_one(expr, wl, dataset, poison_patterns, pc, fix=False):
    verified, data_type, field_types, banned = wl
    known_ops = set(pc["known_ops"])
    group_ids = set(pc["group_identifiers"])
    price_vol = set(pc["price_volume_fields"])
    driver_args = set(pc["driver_args"])
    vec_ops = set(pc["vector_only_ops"])
    inaccessible = set(pc["inaccessible_ops"])
    fixed_expr = None
    # --fix: VECTOR 数据集下先把裸用的 VECTOR 字段自动裹上 vec_* 再检测（幂等）
    if fix and data_type == "VECTOR" and field_types and wrap_naked_vectors is not None:
        vfields = [f for f, t in field_types.items() if t == "VECTOR"]
        new_expr, wrapped = wrap_naked_vectors(expr, vfields)
        if wrapped:
            fixed_expr = new_expr
            expr = new_expr
    issues = []
    # 非阻断告警通道（2026-09-17）：SOP 里"须给出解释即可放行"的规则（如非标准窗口）
    # 不应进 `issues`（那会直接判 FAIL），但也不能静默 —— 单独收集，由调用方展示。
    warnings = []
    # 闸1 语法
    v = get_validator()
    if v is None:
        issues.append("[SYNTAX_UNKNOWN] verifier 缺失（设 WQ_VALIDATOR_DIR 指定 "
                      "alpha-expression-verifier/scripts）")
    else:
        try:
            r = v.check_expression(expr)
            if not r.get("valid"):
                issues.append(f"[SYNTAX] {r.get('errors')}")
        except Exception as e:
            issues.append(f"[SYNTAX] verifier error: {e}")
    # 闸1b 算子元数 + 命名参数（verifier 的手写签名表查不出，见模块头事故记录）
    if _arity_check is None:
        issues.append("[ARITY_UNKNOWN] op_arity 不可达（设 WQB_WORKSPACE 指向工作区根），"
                      "算子元数/命名参数未校验")
    else:
        try:
            issues.extend(_arity_check(expr))
        except Exception as e:
            issues.append(f"[ARITY] op_arity error: {e}")
    # 闸1b-2 算子复杂度（2026-10-03）：表达式内函数调用点数必须 < 10。
    # 记忆铁律（.workbuddy/memory/MEMORY.md §0 组合形态纪律）此前只有条文、
    # 无任何机器执行点——是「唯一宣称只登记不执行」的典型漏网。本闸补上执行点。
    # op_arity 不可达时不在此重复报（1b 已报 ARITY_UNKNOWN，说明"没校验"）。
    if _call_counter is not None:
        try:
            n_calls = len(_call_counter(expr))
            if n_calls >= MAX_OP_CALLS:
                issues.append(
                    f"[OPS] 算子调用点数 {n_calls} ≥ {MAX_OP_CALLS}"
                    f"（铁律：表达式内函数调用计数须 <10；复杂表达式在 2Y/SUB/"
                    f"INVESTABILITY 上更难破，且往往是把实现路径约束误当结构性约束"
                    f"的产物——判无解前先扫等价算子替换）")
        except Exception as e:
            issues.append(f"[OPS] 调用点计数 error: {e}")
    idents = set(re.findall(r"[a-zA-Z_][a-zA-Z0-9_]*", expr))
    # 命名参数名（std=4 / cat= 等）不是字段也不是算子——排除避免误报（winsorize std 实证）
    kw_args = set(re.findall(r"([a-zA-Z_][a-zA-Z0-9_]*)\s*=", expr))
    fields = idents - known_ops - group_ids - price_vol - driver_args - kw_args
    ops_used = (idents - kw_args) & known_ops
    # 闸2 白名单（幽灵算子单独报，不混进「未验证字段」）
    ghost_hit = sorted((idents - kw_args) & _ghost_ops(pc))
    if ghost_hit:
        issues.append(f"[GHOST] 幽灵算子（平台不存在，回测 ERROR 并连坐整批 CANCELLED）: {ghost_hit}")
    unknown = sorted(fields - verified - set(ghost_hit))
    if unknown:
        issues.append(f"[FIELD] 未验证字段: {unknown}")
    # 闸2b 区域非法 group 字段（2026-09-19，JPN wave7/8 实证：sector/subindustry/industry 在 JPN
    # 是 'Invalid data field'，POST 可接受、执行必 ERROR 并连坐整批 CANCELLED）。
    # 名单在 platform_constraints.json `region_invalid_group_fields`，region 由 main() 注入 pc["_region"]。
    _bad_groups = set((pc.get("region_invalid_group_fields") or {}).get(str(pc.get("_region") or "").upper(), []))
    if _bad_groups:
        hit = sorted((idents - kw_args) & _bad_groups)
        if hit:
            issues.append(f"[FIELD] 区域 {pc.get('_region')} 不支持的 group 字段: {hit}"
                          "（平台 Invalid data field，整批连坐）")
    # 闸2b-2 区域不可用普通字段 + VECTOR 上套 ts_*（2026-09-19，JPN 无 pv1 实证；名单/开关在
    # platform_constraints.json `region_invalid_fields` / `region_vector_ts_forbidden`）。
    _reg = str(pc.get("_region") or "").upper()
    _bad_fields = set((pc.get("region_invalid_fields") or {}).get(_reg, []))
    if _bad_fields:
        hit = sorted((idents - kw_args) & _bad_fields)
        if hit:
            issues.append(f"[FIELD] 区域 {_reg} 无该基础字段: {hit}（平台 Invalid data field，整批连坐）")
    if _reg in {str(r).upper() for r in (pc.get("region_vector_ts_forbidden") or [])} and _ts_over_vec(expr):
        issues.append(f"[FIELD] 区域 {_reg} 禁止 ts_*(…vec_*(…)) 组合（平台 Invalid data field close，整批连坐）")
    # 闸3 类型：按字段 type 判定（跨集 mix 时 data_type 不能代表全部腿）
    used_vec = [f for f in fields if field_types.get(f) == "VECTOR"]
    if used_vec or data_type == "VECTOR":
        naked = (naked_vector_fields(expr, fields, field_types, vec_ops) if field_types
                 else legacy_strip_naked(expr, fields, vec_ops))
        if naked:
            issues.append(f"[EVENT] 事件型字段必须经 vec_* 聚合: {naked}")
    elif data_type == "MATRIX":
        bad = ops_used & vec_ops
        if bad:
            issues.append(f"[TYPE] MATRIX 数据集禁用 vec_*: {sorted(bad)}")
    # 闸4 不可访问算子 + quantile arity + banned_patterns
    # 注意：ts_min/ts_max 不在 known_ops 中，必须对 idents 判定（对 ops_used 判定是死代码）
    inac = idents & inaccessible
    if inac:
        issues.append(f"[INACCESSIBLE] 平台不可访问算子(整批CANCELLED元凶): {sorted(inac)}")
    # 负 lookbehind 排除 ts_quantile 等前缀算子（2026-08-26 wave40: ts_quantile 的
    # 子串被误匹配导致 [ARITY] quantile 2 参误报；与仓库 tools/gate.py 同步修复）
    for qm in re.finditer(r"(?<![A-Za-z0-9_])quantile\(", expr):
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
        if args != pc.get("quantile_arity", 1):
            issues.append(f"[ARITY] quantile 仅 {pc.get('quantile_arity', 1)} 参, 当前 {args}")
    for bp in banned:
        scope = bp.get("scope", "all")
        if scope == "vector_dataset" and data_type == "MATRIX":
            continue
        if re.search(bp["pattern"], expr):
            issues.append(f"[BANNED] {bp.get('reason', bp['pattern'])}")
    # 闸5 毒模式
    # 2026-09-17 结构判定加固：weighted_signal_mix 正则要求两条腿都紧跟
    # (rank|zscore|ts_rank|group_rank|normalize|scale)，而真实语料主流是
    # subtract(0, rank(x)) 这类镜像腿 → 实测 81% 漏网（抽 220 条真闸只 block 19%）。
    # 遂补一个**形状无关**的结构判定：任何 add( 的顶层实参中 ≥2 个以「系数*」开头
    # 即判加权混合（含嵌套，如 quantile(add(multiply(0.7,X), multiply(0.3,Y)))）。
    # 等权 add(rank(a), rank(b)) 不拦（无系数）；单腿系数缩放 0.5*rank(a) 不拦（<2 条腿）。
    structural_mix = _detect_weighted_mix_structural(expr)
    # 2026-09-28 补充：「等权」加两条独立信号腿同样违规（既有判定明文豁免等权 → 实测漏网）。
    # 详见 _detect_equal_weight_leg_add 文档；KOR wave189/190 实证 7 条漏网已作废。
    _non_field = known_ops | group_ids | driver_args | kw_args
    _eq_hits = _find_equal_weight_leg_add(expr, _non_field, pc.get("_field_dataset"),
                                          bool(pc.get("_single_dataset_batch")))
    structural_equal_leg = any(not h["same_dataset"] for h in _eq_hits)
    if any(h["same_dataset"] for h in _eq_hits):
        warnings.append(
            "[SAME_DATASET_LEG_ADD] add() 相加的腿全部引用**同一数据集**字段 ⇒ 同源豁免，"
            "不按闸5 拦截（官方 ATOM 定义只约束字段同源、不约束组合结构）。"
            "但同源两腿相加不产生新信息、且权重本身是过拟合通道 ⇒ 派发前必须登记权重来源"
            "（等权 / 由经济含义决定的配比），禁止试多个权重挑最好看的一个。"
            "见 tracking/DEU/atom_orthogonal/MECHANISM_FIRST_DISPATCH_CHECKLIST_20261112.md")
    # 2026-09-29 X-3：中缀 `+`（权重在右 / 无 add( 的写法）与价差规则（跨数据集 / 带系数）。
    infix_sum, infix_spreads = _detect_infix_leg_sum(expr, _non_field)
    spread_weighted, spread_cross = _spread_findings(
        infix_spreads + _collect_func_spreads(expr, _non_field), _non_field, price_vol,
        pc.get("_field_dataset"), pc.get("_declared_spread_pairs"))
    structural_only = False
    for pp in poison_patterns:
        if pp.get("severity", "block") != "block":
            continue
        if pp.get("_structural") and pp["name"] in (
                "weighted_signal_mix_structural", "equal_weight_leg_add",
                "infix_leg_sum", "spread_cross_dataset"):
            # 结构判定的命中在循环外统一追加（见下），此处只标记存在性
            structural_only = True
            continue
        if re.search(pp["regex"], expr):
            issues.append(f"[POISON:{pp['name']}] {pp['rule']}")
    if structural_equal_leg:
        for pp in poison_patterns:
            if pp.get("name") == "equal_weight_leg_add":
                issues.append(f"[POISON:{pp['name']}] {pp['rule']}")
                break
        else:
            issues.append(
                "[POISON:equal_weight_leg_add] add() 等权相加两条独立信号腿 = 混信号调参，"
                "全局禁止（无论 add(multiply(0.4,...)) 还是 0.4A+0.6B）。"
                "合规替代：①单信号结构 ts_scale / subtract(rank(A), rank(B))（价差：两腿同源且有单一经济含义）"
                "②换算子几何 group_rank/group_zscore/ts_quantile ③换字段组合或换信号概念（Mode B）。"
                "不得靠增删腿数或调权重修不达标信号。"
            )
    if infix_sum:
        for pp in poison_patterns:
            if pp.get("name") == "infix_leg_sum":
                issues.append(f"[POISON:{pp['name']}] {pp['rule']}")
                break
        else:
            issues.append(
                "[POISON:infix_leg_sum] 中缀 `+` 相加两条以上独立信号腿 = 与 add(A,B) 同罪的混信号调参"
                "（无论权重在左/右/无），全局禁止。合规替代：单信号结构 / 同源价差 / 换信号概念（Mode B）。")
    if spread_cross:
        for pp in poison_patterns:
            if pp.get("name") == "spread_cross_dataset":
                issues.append(f"[POISON:{pp['name']}] {pp['rule']}")
                break
        else:
            issues.append(
                "[POISON:spread_cross_dataset] subtract 的两腿来自不同数据集，"
                "且该集对未声明经济含义 = 拼腿（用户 2026-10-01 修正：跨集价差合规，"
                "但须以 declared_cross_spreads 声明方向性经济解释：背离/对冲/预期-约束缺口）。")
    if spread_weighted:
        warnings.append(
            "[SPREAD_WEIGHTED] 价差腿带数值系数（靠调权重凑指标属违规族，见 spread_signal_ruling）；"
            "请去掉系数或给出经济解释")
    if structural_mix:
        for pp in poison_patterns:
            if pp.get("name") == "weighted_signal_mix_structural":
                issues.append(f"[POISON:{pp['name']}] {pp['rule']}")
                break
        else:
            # 配置缺失时兜底（配置是单一事实源，但判定器不应因此静默失效）
            issues.append(
                "[POISON:weighted_signal_mix_structural] "
                "任一 add( 顶层实参 ≥2 个以「系数*」开头 = 加权混合，"
                "用户 2026-09-13 路线 A 全局禁止（防过拟合）。"
            )
    # 闸9 窗口白名单（2026-09-17 新增，默认 warning 不阻断）
    # 依据：SOP 两处（ra-pipeline 步 4 / brain-make-some-gem）都要求"只用标准窗口
    # 1/5/22/66/252/504/1008/1260；其他窗口须给出解释或实测证据"，但**此前只写在散文里、
    # 零机械守护**；实测全库 23% 用了非白名单窗口（Top 恰为 20/10/120/60）——
    # 与 `_lib/operator_coverage.py::_DEFAULT_WINDOWS` 的旧默认值完全吻合。
    # SOP 允许"给出解释后用"，故**默认**记 warning 不阻断；
    # `window_whitelist_enforce=true` 时升为 block（2026-09-17 补：实测当日新语料
    # 违规率 26.5%，散文约束无效，需可选硬门）。
    wl_raw = pc.get("window_whitelist") or []
    if wl_raw:
        allowed = {int(w) for w in wl_raw}
        off = sorted({w for w in expression_windows(expr) if w not in allowed})
        if off:
            msg = (f"[WINDOW] 非标准窗口 {off}（白名单 {sorted(allowed)}）；"
                   f"SOP 要求给出解释或实测证据")
            if pc.get("window_whitelist_enforce"):
                issues.append(msg + " ［enforce 模式：window_whitelist_enforce=true］")
            else:
                warnings.append(msg)
    out = {"fields": sorted(fields), "issues": issues,
           "warnings": warnings, "pass": not issues}
    if fixed_expr is not None:
        out["fixed_expr"] = fixed_expr
    return out


#: 引号内内容（如 bucket 的 range="0,1,0.1"）不参与窗口识别
_QUOTED_RE = re.compile(r'"[^"]*"|\'[^\']*\'')
#: 窗口候选：裸整数且后接 `,` 或 `)`；排除 `std=4` 这类命名参数与 `0.5` 这类小数
_WINDOW_TOKEN_RE = re.compile(r"(?<![=\w.])(\d{1,4})(?=\s*[,)])")

#: 加权混合结构判定：「实参以 系数* 开头」的系数形态（含负号/整数/小数）
_COEF_PREFIX_RE = re.compile(r"^\s*-?\d*\.?\d+\s*\*")
#: add( 出现位置（用于括号平衡扫描所有 add 实参，含嵌套）
_ADD_OPEN_RE = re.compile(r"\badd\s*\(")


def _top_level_args(expr, start):
    """从 `add(` 的左括号后开始，括号平衡地切分顶层实参列表。

    start 指向左括号**之后**第一个字符。返回 (args, end)；
    括号不平衡时返回 (None, start)——宁可漏判不可误伤。
    """
    depth = 1
    i = start
    args, cur = [], []
    n = len(expr)
    while i < n and depth > 0:
        ch = expr[i]
        if ch == "(":
            depth += 1
        elif ch == ")":
            depth -= 1
            if depth == 0:
                break
        elif ch == "," and depth == 1:
            args.append("".join(cur))
            cur = []
            i += 1
            continue
        cur.append(ch)
        i += 1
    if depth != 0:
        return None, start  # 不平衡：放弃（语法层会另报）
    args.append("".join(cur))
    return args, i


def _detect_weighted_mix_structural(expr):
    """闸5 结构判定：任一 ``add(...)`` 的顶层实参中 ≥2 个以「系数*」开头。

    形状无关（星号中缀 / multiply 函数式 / 镜像腿 subtract(0, rank(x)) 均命中），
    覆盖正则 weighted_signal_mix 实测 81% 的漏网形态（含嵌套 add）。
    等权 add(rank(a), rank(b)) 与单腿缩放 0.5*rank(a) 不算（<2 条系数腿）。
    """
    for m in _ADD_OPEN_RE.finditer(expr):
        args, _ = _top_level_args(expr, m.end())
        if not args or len(args) < 2:
            continue
        if sum(1 for a in args if _COEF_PREFIX_RE.match(a)) >= 2:
            return True
    return False


#: 纯数值实参（epsilon / 常数）：不是信号腿
_NUM_ONLY_RE = re.compile(r"^\s*[-+]?(?:\d+\.?\d*|\.\d+)(?:[eE][-+]?\d+)?\s*$")   # 含 1e-3 科学计数法
_IDENT_TOKEN_RE = re.compile(r"[A-Za-z_][A-Za-z0-9_]*")
_INT_TOKEN_RE = re.compile(r"\b\d+\b")


def _is_signal_leg(arg, non_field):
    """实参是否为「信号腿」：至少引用一个数据字段（非算子/非分组标签/非参数名），且非纯常数。

    `add(abs(x), 0.01)` 里的 `0.01` 是 epsilon 标量 → 不算腿（该形态全局在用，必须放行）。
    """
    a = (arg or "").strip()
    if not a or _NUM_ONLY_RE.match(a):
        return False
    for tok in _IDENT_TOKEN_RE.findall(a):
        if tok not in non_field and not tok.startswith(
                ("ts_", "group_", "vec_", "reduce_", "bucket_", "quantile_")):
            return True
    return False


def _normalize_numbers(s):
    """把窗口/常数归一成 N，用于判断两条腿是否只是「同形态不同窗口」。"""
    return _INT_TOKEN_RE.sub("N", re.sub(r"\s+", "", s or ""))


#: 函数式除法 `divide(`（分母位判定的第二个来源）
_DIV_OPEN_RE = re.compile(r"\bdivide\s*\(")
_IDENT_LEAD_RE = re.compile(r"[A-Za-z_][A-Za-z0-9_]*")
_NUM_LEAD_RE = re.compile(r"[-+]?(?:\d+\.?\d*|\.\d+)(?:[eE][-+]?\d+)?")


def _paren_close(expr, i):
    """`expr[i] == '('`：返回配对 `)` **之后**的下标；不平衡返回 None。"""
    depth = 0
    for j in range(i, len(expr)):
        if expr[j] == "(":
            depth += 1
        elif expr[j] == ")":
            depth -= 1
            if depth == 0:
                return j + 1
    return None


def _operand_span(expr, i):
    """从 i 起跳空白，取一个右操作数的 (start, end)：括号组 / 函数调用 / 标识符 / 数值。"""
    n = len(expr)
    while i < n and expr[i].isspace():
        i += 1
    if i >= n:
        return None
    start = i
    if expr[i] == "(":
        end = _paren_close(expr, i)
        return (start, end) if end else None
    m = _IDENT_LEAD_RE.match(expr, i)
    if m:
        j = m.end()
        k = j
        while k < n and expr[k].isspace():
            k += 1
        if k < n and expr[k] == "(":                 # 函数调用：吃掉整对括号
            end = _paren_close(expr, k)
            return (start, end) if end else (start, j)
        return (start, j)
    m = _NUM_LEAD_RE.match(expr, i)
    if m:
        return (start, m.end())
    return None


def _top_level_arg_spans(expr, start):
    """同 `_top_level_args`，但返回每个顶层实参的 `(start, end)` 位置；不平衡返回 None。"""
    spans, depth, cur_start = [], 1, start
    i, n = start, len(expr)
    while i < n and depth > 0:
        ch = expr[i]
        if ch == "(":
            depth += 1
        elif ch == ")":
            depth -= 1
            if depth == 0:
                break
        elif ch == "," and depth == 1:
            spans.append((cur_start, i))
            cur_start = i + 1
        i += 1
    if depth != 0:
        return None
    spans.append((cur_start, i))
    return spans


def _denominator_spans(expr):
    """分母位区间（2026-10-27 新增）：中缀 `/` 的右操作数 + `divide(` 的第二实参。

    背景（`reports/codebase_governance_review_20261027.md` §4 P0-P4）：`(X−Y)/(X+Y)` 与
    `divide(subtract(a,b), add(a,b))` 是**净额/总额归一化**的标准单信号写法，但等权腿判定
    曾在分母位照样拦下，且与分子位 `divide(add(rank(a),rank(b)), 2)`（该拦）判据混同。
    引号内（`range="0,1,0.1"` 之类）的 `/` 不参与。
    """
    spans = []
    quoted = [m.span() for m in _QUOTED_RE.finditer(expr)]
    for i, ch in enumerate(expr):
        if ch != "/" or any(s <= i < e for s, e in quoted):
            continue
        sp = _operand_span(expr, i + 1)
        if sp:
            spans.append(sp)
    for m in _DIV_OPEN_RE.finditer(expr):
        arg_spans = _top_level_arg_spans(expr, m.end())
        if arg_spans and len(arg_spans) == 2:
            spans.append(arg_spans[1])
    return spans


def _mask_denominators(expr):
    """把分母位内容整体替换成常量 `0`，供「加和/等权腿」判定扫描用。

    替换而非删除：留住占位才能维持 `divide(a, b)` 的二元形状与「1 腿 + 标量」语义
    （`0` 被 `_is_signal_leg` 判为纯常数，不是信号腿）。分母位内部的嵌套加和一并屏蔽 ——
    「除数整体是归一化分量」时它的内部结构不构成「两条独立信号腿相加」。
    """
    spans = _denominator_spans(expr)
    if not spans:
        return expr
    mask = [False] * len(expr)
    for s, e in spans:
        for k in range(max(0, s), min(e, len(expr))):
            mask[k] = True
    out, i, n = [], 0, len(expr)
    while i < n:
        if mask[i]:
            out.append("0")
            while i < n and mask[i]:
                i += 1
        else:
            out.append(expr[i])
            i += 1
    return "".join(out)


_LEG_IDENT_RE = re.compile(r"[A-Za-z_][A-Za-z0-9_]*")


def _legs_all_same_dataset(legs, non_field, field_dataset, single_dataset_batch):
    """两条腿引用的字段是否**全部来自同一数据集**（同源豁免判定，2026-11-12 用户裁定）。

    依据：
      - 官方 ATOM 定义只约束「所有数据字段来自同一数据集」，**不约束组合结构**；
        group 字段（industry / country 等）是豁免字段，不计入数据集数量限制。
        （forum post 32032672214807，201 赞科普帖；平台 single-dataset-alphas 文档）
      - 官方对 ATOM 的设计逻辑表述：「同一数据集下字段类型更统一，**降低混信号风险**」
        ⇒ 同源本身就在降低混信号，与禁 add(A,B) 的**防调参过拟合**目的不冲突。
      - 但仍须登记权重来源（防「试几个权重挑最好看」），故本级只降为 **warn**，不直接放行。

    fail-closed：无法把每条腿的字段全部解析到**同一个**数据集时返回 False（维持 block）。
    """
    if single_dataset_batch:
        return True
    if not field_dataset:
        return False
    ds_of_legs = []
    for leg in legs:
        ids = {t for t in _LEG_IDENT_RE.findall(leg or "") if t not in non_field}
        if not ids:
            return False
        ds = {field_dataset.get(i) for i in ids}
        if len(ds) != 1 or None in ds:
            return False
        ds_of_legs.append(next(iter(ds)))
    return len(set(ds_of_legs)) == 1


def _find_equal_weight_leg_add(expr, non_field, field_dataset=None, single_dataset_batch=False):
    """扫描所有「≥2 条形态不同的信号腿被 add() 相加」的位置，标注是否同源。

    返回 [{legs, same_dataset}]；空列表 = 无命中。
    """
    hits = []
    for m in _ADD_OPEN_RE.finditer(_mask_denominators(expr)):
        args, _ = _top_level_args(expr, m.end())
        if not args or len(args) < 2:
            continue
        legs = [a for a in args if _is_signal_leg(a, non_field)]
        if len(legs) < 2:
            continue
        if len({_normalize_numbers(a) for a in legs}) < 2:
            continue
        hits.append({
            "legs": legs,
            "same_dataset": _legs_all_same_dataset(legs, non_field, field_dataset,
                                                   single_dataset_batch),
        })
    return hits


def _detect_equal_weight_leg_add(expr, non_field, field_dataset=None, single_dataset_batch=False):
    """闸5 结构判定（2026-09-28 新增）：「等权」加两条**独立信号腿**同样违规。

    背景：既有 `_detect_weighted_mix_structural` 只拦「实参以 系数* 开头」的腿，
    **明文豁免等权 add(rank(a), rank(b))**。而全局纪律是「不得把两条独立信号腿
    加权相加，无论写成 add(multiply(0.4,...)) 还是 0.4A+0.6B」——等权即 0.5A+0.5B，
    属同一违规族。实证代价：KOR wave189/190 共 7 条 `add(group_rank(腿A), group_rank(腿B))`
    （含 S=2.11/F=1.80/2Y=1.89 的漂亮结果）全部通过闸5 → 已全部作废。

    判定：某 `add(` 的顶层实参中 ≥2 个是信号腿，且这些腿**形态不同**
    （归一化数字后仍不相等 —— 仅窗口不同的同形态叠加视为单信号多窗平滑，放行）。
    `add(abs(x), 0.01)`（1 条腿 + 标量）、`add(ts_mean(x,22), ts_mean(x,66))`
    （同形态不同窗）均放行。

    **分母位跳过（2026-10-27，P0-P4）**：`divide(x, add(A,B))` / `x/(A+B)` 里的 `add` 是
    归一化的除数，不是「两条独立信号腿相加」⇒ `_mask_denominators` 先屏蔽分母位再扫描。

    **同源豁免（2026-11-12，用户裁定）**：命中的 add() 里所有腿引用的字段**全部来自
    同一数据集**时不算混信号（官方 ATOM 口径：同源降低混信号风险），降为 warning
    [SAME_DATASET_LEG_ADD]，由 check_one 追加；仍须登记权重来源。
    """
    return any(not h["same_dataset"] for h in _find_equal_weight_leg_add(
        expr, non_field, field_dataset, single_dataset_batch))


#: 顶层出现这些字符的片段不做「加减号切项」（比较 / 三元 / 逻辑 / 命名参数）——宁可漏判不可误伤
_NO_SPLIT_CHARS = frozenset("?:<>=!&|")
_OPERAND_END_RE = re.compile(r"[A-Za-z0-9_.)\"']")
_SUBTRACT_OPEN_RE = re.compile(r"\bsubtract\s*\(")


def _iter_segments(expr):
    """产出表达式本身，以及每一层括号内的每个顶层实参（递归；含分组括号）。"""
    yield expr
    stack = []
    for i, ch in enumerate(expr):
        if ch == "(":
            stack.append(i)
        elif ch == ")" and stack:
            args, _ = _top_level_args(expr, stack.pop() + 1)
            for a in args or []:
                yield a


def _split_signed_terms(seg):
    """按顶层二元 ``+`` / ``-`` 把片段切成 ``[(sign, term)]``。

    一元号并入项；科学计数法 ``1e-3`` 不切；含比较/三元/逻辑运算符或括号不平衡时返回 None。
    """
    s = _QUOTED_RE.sub('""', seg or "")
    depth, terms, cur, sign, prev = 0, [], [], "+", ""
    i, n = 0, len(s)
    while i < n:
        ch = s[i]
        if ch == "(":
            depth += 1
        elif ch == ")":
            depth -= 1
            if depth < 0:
                return None
        elif depth == 0 and ch in _NO_SPLIT_CHARS:
            return None
        elif depth == 0 and ch in "+-" and prev and _OPERAND_END_RE.match(prev):
            if not (prev in "eE" and i >= 2 and (s[i - 2].isdigit() or s[i - 2] == ".")):
                terms.append((sign, "".join(cur).strip()))
                cur, sign, prev = [], ch, ch
                i += 1
                continue
        cur.append(ch)
        if not ch.isspace():
            prev = ch
        i += 1
    if depth != 0:
        return None
    terms.append((sign, "".join(cur).strip()))
    out = []
    for sg, t in terms:
        while t[:1] in ("-", "+"):                    # 一元号并入符号
            if t[0] == "-":
                sg = "-" if sg == "+" else "+"
            t = t[1:].strip()
        if t:
            out.append((sg, t))
    return out


def _split_factors(term):
    """按顶层 ``*`` / ``/`` 切因子（括号平衡）。"""
    depth, cur, out = 0, [], []
    for ch in term or "":
        if ch == "(":
            depth += 1
        elif ch == ")":
            depth -= 1
        if depth == 0 and ch in "*/":
            out.append("".join(cur).strip())
            cur = []
            continue
        cur.append(ch)
    out.append("".join(cur).strip())
    return [f for f in out if f]


def _leg_has_coef(leg):
    """腿是否带数值系数：中缀 ``rank(A)*0.6`` / ``0.6*rank(A)`` / ``rank(A)/2``，或 ``multiply(0.6, …)``。"""
    factors = _split_factors(leg)
    if len(factors) >= 2 and any(_NUM_ONLY_RE.match(f) for f in factors) \
            and any(not _NUM_ONLY_RE.match(f) for f in factors):
        return True
    m = re.match(r"^\s*multiply\s*\(", leg or "")
    if m:
        args, _ = _top_level_args(leg, m.end())
        if args and len(args) == 2 and any(_NUM_ONLY_RE.match(a) for a in args):
            return True
    return False


def _detect_infix_leg_sum(expr, non_field):
    """闸5 结构判定（2026-09-29）：**中缀** ``+`` / 同号多腿相加，与 ``add(...)`` 同罪。

    背景（skills 审查 X-3 实测）：``rank(A)*0.6 + rank(B)*0.4``（权重在右）、
    ``scale(rank(A)) + scale(-rank(B))*0.35``（V9 顶层形态）、HP-05 的
    ``ts_decay_linear(s,5)*rank(v*c) + ts_decay_linear(s,10)*(1-rank(v*c))`` 全部放行，而数学等价的
    ``add(...)`` 被拦——同一结构，写法不同判定相反。既有 add 检测只认函数式 ``add(``。

    判定：任一片段（整式 / 每层括号内的每个顶层实参）按顶层 ``+ -`` 切项后，信号腿 ≥2 且
    **不是**「恰好一正一负」的价差，且腿形态（归一化数字后）不全相同 → 违规。
    放行：``abs(x)+0.01``（1 腿+标量）、``ts_mean(x,22)+ts_mean(x,66)``（同形态仅窗口差，与 add 一致）、
    一正一负价差（交给 spread 规则：同源 + 经济含义，用户 2026-09-28 裁定）。
    **分母位跳过（2026-10-27，P0-P4）**：``(A−B)/(A+B)`` 的 ``+`` 在除号右侧 ⇒ 违规判定
    走 `_mask_denominators` 后的表达式；**价差收集仍走原式**（分母里的真价差照旧交 spread 规则）。
    返回 ``(violates, spreads)``，spreads = 中缀价差 ``[(legA, legB)]``。
    """
    violates, spreads = False, []
    for seg in _iter_segments(_mask_denominators(expr)):
        terms = _split_signed_terms(seg)
        if not terms or len(terms) < 2:
            continue
        legs = [(sg, t) for sg, t in terms if _is_signal_leg(t, non_field)]
        if len(legs) < 2:
            continue
        pos = [t for sg, t in legs if sg == "+"]
        neg = [t for sg, t in legs if sg == "-"]
        if len(legs) == 2 and len(pos) == 1 and len(neg) == 1:
            continue
        if len({_normalize_numbers(t) for _, t in legs}) >= 2:
            violates = True
    for seg in _iter_segments(expr):
        terms = _split_signed_terms(seg)
        if not terms or len(terms) < 2:
            continue
        legs = [(sg, t) for sg, t in terms if _is_signal_leg(t, non_field)]
        if len(legs) == 2 and len({sg for sg, _ in legs}) == 2:
            pos = [t for sg, t in legs if sg == "+"]
            neg = [t for sg, t in legs if sg == "-"]
            spreads.append((pos[0], neg[0]))
    return violates, spreads


def _collect_func_spreads(expr, non_field):
    """函数式价差 ``subtract(A, B)``（两腿都是信号腿）。``subtract(0, rank(x))`` 这类镜像腿不算。"""
    out = []
    for m in _SUBTRACT_OPEN_RE.finditer(expr):
        args, _ = _top_level_args(expr, m.end())
        if args and len(args) == 2 and all(_is_signal_leg(a, non_field) for a in args):
            out.append((args[0].strip(), args[1].strip()))
    return out


def _leg_fields(leg, non_field, price_vol):
    return {t for t in _IDENT_TOKEN_RE.findall(leg or "")
            if t not in non_field and t not in price_vol
            and not t.startswith(("ts_", "group_", "vec_", "reduce_", "bucket_", "quantile_"))}


def _leg_dataset(leg, non_field, price_vol, field_dataset):
    """腿涉及的**数据集集合**（不含算子名/常量）。空集 = 无法归属（不参与跨集判定）。"""
    if not field_dataset:
        return set()
    return {field_dataset[f] for f in _leg_fields(leg, non_field, price_vol)
            if field_dataset.get(f)}


def _spread_findings(spreads, non_field, price_vol, field_dataset=None,
                     declared_spread_pairs=None):
    """价差规则（用户 2026-09-28 裁定 + 2026-10-01 修正 spread_signal_ruling）。

    * 腿带数值系数（``0.6*rank(A) - 0.4*rank(B)``）= 靠调权重凑指标 → ``weighted``（仅告警，不阻断）。

    **跨数据集价差判定（2026-10-01 用户修正）**：判据从「字段分属不同数据集」改为
    「**跨集 且 未声明经济含义**」。

    用户 2026-10-01 澄清：``rank(预期A) − rank(约束B)``（A/B 来自**不同数据集、最好不同更新节奏**）
    是**合规且鼓励**的独立信号（属 §7.7.2 ⑤ 换信号概念，两腿独立 → self-corr 低）。
    旧版把「跨集」本身当违规是对用户口径的误读——跨集价差与同源价差是**两类**合规形态：
      ① **同源价差**（``spread_signal_ruling``）：同一经济量对偶两侧 + 同数据集，差值可一句话说清；
      ② **跨集价差**（本条）：不同数据集/不同经济概念两条腿，差值须有一个**方向性经济解释**
         （背离 / 对冲 / 预期-约束缺口），而非无脑平均。
    两类的共同违规内核 = **无经济含义的机械拼腿**（``add`` 一律违规，含等权）。
    因机器无法自动判「有无经济含义」，改用**显式声明**机制：

    * 调用方通过 ``declared_spread_pairs``（或平台级 ``declared_cross_spreads``）声明
      **本波认定的经济含义价差族**（``(A集, B集)`` 或 ``(A集, B集, note)``）；
    * 命中已声明的 (A集,B集) 组合 → **放行**（不阻断，也不告警）；
    * 跨集但**未声明** → 仍阻断（``cross``），提示「如为有意设计，请声明经济含义」。

    ``declared_spread_pairs`` 为 ``None``/空 → 保持旧行为吗？不：**空声明 = 全部跨集阻断**，
    与旧版一致（向后兼容），但错误消息会指引声明路径。
    """
    weighted, cross = [], []
    declared = set()
    for item in (declared_spread_pairs or []):
        if isinstance(item, (list, tuple)) and len(item) >= 2:
            declared.add(frozenset((str(item[0]), str(item[1]))))
    for a, b in spreads:
        if _leg_has_coef(a) or _leg_has_coef(b):
            weighted.append((a, b))
        if field_dataset:
            da = _leg_dataset(a, non_field, price_vol, field_dataset)
            db = _leg_dataset(b, non_field, price_vol, field_dataset)
            if da and db and da.isdisjoint(db):
                # 跨集：检查是否存在「已声明」的集对组合（任一双向匹配即视为已声明含义）
                if any(frozenset((x, y)) in declared for x in da for y in db):
                    continue  # 已声明经济含义 → 放行
                cross.append((a, b))
    return weighted, cross


def expression_windows(expr, lo=2, hi=2000):
    """提取表达式里的**窗口类整数**（ts_*/group_*/bucket 的窗口位）。

    判定：裸整数（前不接 `=`、`.`、字母）且后接 `,` 或 `)`，取值在 [lo, hi]。
    刻意**不**按算子白名单区分"窗口位"——FASTEXPR 里 `ts_corr(a,b,20)` 与
    `ts_decay_linear(x,66)` 的窗口都在末位，形状一致，无需枚举算子。
    引号串（bucket range）先剔除，避免 `range="0,1,0.1"` 里的 `1` 被误判。
    """
    if not expr:
        return []
    s = _QUOTED_RE.sub('""', expr)
    return [int(m.group(1)) for m in _WINDOW_TOKEN_RE.finditer(s)
            if lo <= int(m.group(1)) <= hi]


def _canon(obj):
    """JSON 规范化（set→有序 list、dict 键排序），保证同一输入在不同进程得到同一指纹。"""
    if isinstance(obj, dict):
        return {str(k): _canon(v) for k, v in sorted(obj.items(), key=lambda kv: str(kv[0]))}
    if isinstance(obj, (set, frozenset)):
        return sorted((_canon(v) for v in obj), key=lambda v: json.dumps(v, sort_keys=True, default=str))
    if isinstance(obj, (list, tuple)):
        return [_canon(v) for v in obj]
    return obj


#: 闸注册表（唯一来源）。(id, 名称, 性质, 开关/缺省, 说明)。性质：block=命中即 FAIL；warn=只告警。
GATE_REGISTRY = (
    ("0", "语义反模式", "block", "--gate0（默认关闭）", "恒等式 / 裸字段 / 元数据字段作信号腿（穿透闸 1–8 的废品）"),
    ("1", "语法", "block", "常开", "alpha-expression-verifier 直调；缺失标 SYNTAX_UNKNOWN"),
    ("1b", "算子元数 + 命名参数", "block", "常开", "op_arity（catalog 驱动）；缺失标 ARITY_UNKNOWN"),
    ("1b-2", "算子复杂度（调用点数 <10）", "block", "常开（MAX_OP_CALLS 可调）",
     "铁律：表达式内函数调用计数须 <10；与 distinct operator_count 口径不同。实测过平台 Sharpe 线（`config.PLATFORM_CHECK_LINES`）的达标行 0 条触线"),
    ("2", "字段白名单", "block", "常开（--dataset）", "typed catalog 优先 → legacy 兜底"),
    ("2b", "区域非法 group 字段", "block", "常开（platform_constraints.region_invalid_group_fields）",
     "如 JPN 的 sector/industry/subindustry 是 Invalid data field，整批连坐"),
    ("2b-2", "区域不可用字段 + VECTOR 上套 ts_*", "block",
     "常开（region_invalid_fields / region_vector_ts_forbidden）", "如 JPN 无 pv1 字段"),
    ("3", "类型", "block", "常开", "VECTOR 需 vec_* 包裹（数据驱动）；MATRIX 禁 vec_*"),
    ("4", "平台不可访问算子 + quantile 元数 + banned_patterns", "block", "常开",
     "ts_min/ts_max 等（对全部 idents 判定，不是 ops_used）"),
    ("5", "毒模式", "block", "常开",
     "平台级 platform_constraints 正则 + 结构判定（add 加权 / add 等权 / 中缀 + / 跨数据集价差）+ 区域级生成约束"),
    ("6", "批级多样性", "block", "常开（--skip-diversity-gate 为逃生阀）", "diversity_audit 契约强制；repair 批豁免"),
    ("7", "longCount 真实性", "warn", "--sanity-longcount", "VECTOR 字段实际 longCount < 80 → WARN"),
    ("8", "EVENT 类型", "block", "--sanity-event-type", "引用 type==EVENT 字段 → FAIL（平台无 ts_event_*；先单条探针）"),
    ("9", "非标准窗口", "warn", "常开；window_whitelist_enforce=true 升 block（缺省 false）",
     "白名单 1/5/22/66/252/504/1008/1260；其他窗口须给出解释或实测证据"),
)


def render_gate_table():
    """Markdown 闸表（文档由此生成 / 与测试比对）。"""
    rows = ["| 闸 | 名称 | 性质 | 开关 | 说明 |", "|---|---|---|---|---|"]
    for gid, name, kind, sw, note in GATE_REGISTRY:
        rows.append(f"| 闸{gid} | {name} | {kind} | {sw} | {note} |")
    return "\n".join(rows)


#: 判定器代码版本：闸 1-5 的判定代码（非配置）变更时递增，让逐条缓存失效（配置变更已由 poison/pc 入签名）。
GATE_CODE_VERSION = "2026-10-27.1"   # 2026-10-27 分母位跳过（P0-P4）令旧缓存结论失效


def gate_signature(ds_all, wl, poison, pc):
    """闸 1-5 逐条判定的全部外部输入指纹：数据集集合 + 合并白名单（字段 / 类型 / banned）
    + 毒模式 + 平台约束（含区域）。任一变化都必须让逐条缓存失效（2026-09-27 R21）。"""
    ids, dtype, fts, banned = wl
    blob = json.dumps(_canon({"datasets": sorted(set(ds_all)), "ids": ids, "dtype": dtype,
                              "field_types": fts or {}, "banned": banned or [],
                              "poison": poison, "pc": pc, "code": GATE_CODE_VERSION}),
                      ensure_ascii=False, sort_keys=True, default=str)
    return hashlib.sha1(blob.encode("utf-8")).hexdigest()[:16]


def cache_key(dataset, expr, sig=""):
    # 2026-09-27 R21：键纳入 sig（gate_signature）。此前只有 (主 dataset, 表达式)：漏声明
    # --datasets 第二腿时的 [FIELD] 失败被缓存，补声明重跑 cached=39/39、结论不变——
    # KOR 唯一出过 ACTIVE 的跨集配方（评级修正 × multi_source_model）被持续拦截（真实复现）。
    return hashlib.sha1(f"{dataset}\n{sig}\n{expr}".encode()).hexdigest()


def batch_digest(exprs):
    """批级幂等标识（内容哈希）：同批重跑闸门不重复计数消费。"""
    payload = json.dumps(sorted(re.sub(r"\s+", "", e) for e in exprs), ensure_ascii=False)
    return hashlib.sha1(payload.encode()).hexdigest()
