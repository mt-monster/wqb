# -*- coding: utf-8 -*-
"""gate.py - 战役统一提交前闸门（8 闸 + 可选闸0 + sha1 缓存）。

闸0 语义反模式（可选，--gate0，默认关闭保持兼容）：恒等式（subtract/divide 同参恒零/恒1、
    add(x,0)/multiply(x,1)/power(x,1) 等恒等或恒常量形式）、裸字段表达式（整式单一字段 ID）、
    元数据字段（periodend/periodtype/fyearend/periodnum/analyststart/curfperiod/curperiod）作信号腿
闸1 语法：import alpha-expression-verifier 直调（WQ_VALIDATOR_DIR 优先；缺失标 SYNTAX_UNKNOWN 报警）
闸2 字段白名单：--dataset 自动派生 reference/<region>_<ds>_fields.json（typed catalog 优先）
    或 <region>_<ds>_field_whitelist.json（legacy 兼容）
闸3 类型：catalog 有字段级 type 时数据驱动判定 VECTOR 包裹（fn_spans 解析，不再正则猜）；
    legacy 白名单退 strip 启发式；MATRIX 禁 vec_*
闸4 平台不可访问算子（ts_min/ts_max，必须对 idents 判定而非 ops_used——历史死代码教训）
    + quantile 仅 1 参（本层加严，不改 verifier 签名表）+ 白名单 banned_patterns（scope 感知）
闸5 毒模式：平台级（toolkit config/platform_constraints.json）+ 区域级（reference 生成约束）正则拦截
闸6 批级多样性：diversity_audit 的 next_round_injections 契约强制（每批至少 N 条用注入算子
    + 骨架配额；repair 批豁免，--skip-diversity-gate 逃生；P0-2 过期契约转 FAIL-CLOSED 并自动续约）
闸7 longCount 真实性校验（--sanity-longcount）：对 VECTOR 字段从 typed catalog 读取实际 longCount，
    低于 80 标记 WARN（platform cov 在小宇宙区域系统性误导，见 MEA f72-CF/model25-cb/model31-auditor）
闸8 EVENT 类型自动检测（--sanity-event-type）：检查 typed catalog 中字段 type==EVENT 且表达式
    未使用 ts_event_* 算子时标记 FAIL（fundamental6 整集报废教训）

缓存 cache/gate_cache.json，key=sha1(dataset+换行+expr)，幂等跳过。

用法:
  python gate.py --campaign-dir <DIR> --dataset model219 --file candidates/xxx_exprs.json
  python gate.py --campaign-dir <DIR> --dataset model219 --expr "rank(close)"
  python gate.py --campaign-dir <DIR> --dataset model219 --file candidates/xxx.json --batch-type repair
  python gate.py --campaign-dir <DIR> --file candidates/xxx.json --dataset <ds> --sanity-all
退出码: 0=全 PASS, 1=存在 FAIL
"""
import argparse
import collections
import hashlib
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _lib.common import (CampaignContext, add_campaign_arg, atomic_write, load_json,
                         load_platform_constraints, read_exprs_any, skeleton, expr_fields)
from _lib.ledger import LedgerStore, make_ledger_store
from _lib import rules as rules_mod

# 知识闸（KB-aware）：复用 assemble_priors 的读取能力，保证 gate 永远对照结构化 KB。
try:
    from assemble_priors import load_priors_file, assemble_priors_dict, priors_sha
except Exception:  # 模块缺失时降级为"无 KB 可用"
    load_priors_file = None
    assemble_priors_dict = None
    priors_sha = None

# 复用工作区 tools/lib 下的 vector_wrap（单一权威源）：--fix 自动裹 vec_* 聚合。
# P1-2 (2026-08-31): 家族天花板预检——复用 src/wqb/expression/validator.py 的
# check_family_ceiling（主导腿信号族占比 ≥2/3 拦截，wave94/95/98/104 实证 SELF≥0.9）。
# 工作区根目录可达时动态导入，不可达则降级跳过（保持 toolkit 独立性）。
def _load_family_ceiling():
    """尝试导入工作区 validator.check_family_ceiling，不可达返回 None。"""
    # 候选路径：环境变量 > 常见相对位置（toolkit scripts -> 工作区根）
    cands = []
    env_root = os.environ.get("WQB_WORKSPACE_ROOT")
    if env_root:
        cands.append(env_root)
    # toolkit scripts 目录 -> ../../../../../ -> 工作区根（Qoder skills 布局）
    here = os.path.dirname(os.path.abspath(__file__))
    cands.append(os.path.normpath(os.path.join(here, "..", "..", "..", "..", "..")))
    for root in cands:
        src = os.path.join(root, "src")
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


def _find_tools_lib():
    env = os.environ.get("WQB_TOOLS_LIB")
    if env and os.path.isfile(os.path.join(env, "vector_wrap.py")):
        return env
    cands = [
        os.path.join(os.environ["WQB_ROOT"], "tools", "lib") if os.environ.get("WQB_ROOT") else None,
        r"D:\coding\traeCN_project\wqb\tools\lib",
    ]
    for c in cands:
        if c and os.path.isfile(os.path.join(c, "vector_wrap.py")):
            return c
    return None


_TOOLS_LIB = _find_tools_lib()
if _TOOLS_LIB and _TOOLS_LIB not in sys.path:
    sys.path.insert(0, _TOOLS_LIB)
try:
    from vector_wrap import wrap_naked_vectors
except Exception:
    wrap_naked_vectors = None

_VALIDATOR = None


def _validator_dirs():
    home = os.path.expanduser("~")
    return [
        os.environ.get("WQ_VALIDATOR_DIR"),
        os.path.join(home, ".workbuddy", "skills", "alpha-expression-verifier", "scripts"),
        os.path.join(home, ".qoder-cn", "skills", "alpha-expression-verifier", "scripts"),
    ]


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
            return _VALIDATOR
    _VALIDATOR = False  # 标记已探测且缺失
    return None


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
    idents = set(re.findall(r"[a-zA-Z_][a-zA-Z0-9_]*", expr))
    # 命名参数名（std=4 / cat= 等）不是字段也不是算子——排除避免误报（winsorize std 实证）
    kw_args = set(re.findall(r"([a-zA-Z_][a-zA-Z0-9_]*)\s*=", expr))
    fields = idents - known_ops - group_ids - price_vol - driver_args - kw_args
    ops_used = (idents - kw_args) & known_ops
    # 闸2 白名单
    unknown = sorted(fields - verified)
    if unknown:
        issues.append(f"[FIELD] 未验证字段: {unknown}")
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
    for pp in poison_patterns:
        if pp.get("severity", "block") != "block":
            continue
        if re.search(pp["regex"], expr):
            issues.append(f"[POISON:{pp['name']}] {pp['rule']}")
    out = {"fields": sorted(fields), "issues": issues, "pass": not issues}
    if fixed_expr is not None:
        out["fixed_expr"] = fixed_expr
    return out


def cache_key(dataset, expr):
    return hashlib.sha1(f"{dataset}\n{expr}".encode()).hexdigest()


def batch_digest(exprs):
    """批级幂等标识（内容哈希）：同批重跑闸门不重复计数消费。"""
    payload = json.dumps(sorted(re.sub(r"\s+", "", e) for e in exprs), ensure_ascii=False)
    return hashlib.sha1(payload.encode()).hexdigest()


def _extract_exposure_from_idea(idea_text):
    """从 GEM idea 文本提取 expected_exposure（收益来源标签）。

    GEM 按 concept_first_rules 输出：
      - **Expected Exposure**: value / momentum / quality / lowvol / liquidity / sentiment / ...
    缺失返回 None（旧 idea 兼容）。
    """
    if not idea_text:
        return None
    # 2026-09-01 兼容兜底格式 "**Expected Exposure** (inferred): xxx"
    # （GEM _ensure_expected_exposure 推断追加的行带 (inferred) 标记）
    m = re.search(r"\*\*Expected Exposure\*\*[^\n:]*:\s*([^\n]+)", idea_text, re.IGNORECASE)
    if not m:
        return None
    raw = m.group(1).strip().strip('`').strip()
    # 标准化：小写、去空格、去标点
    return re.sub(r"[^a-z0-9_]", "", raw.lower().replace(" ", "_")) or None


def _load_exposure_map(ctx, dataset, delay=1):
    """从 DB idea ledger 加载 expression -> expected_exposure 映射。"""
    try:
        from _lib.wqb_store import get_store
        st = get_store(ctx)
        try:
            idea = st.get_idea(ctx.region, dataset, delay)
        finally:
            st.close()
        if not idea or not isinstance(idea, dict):
            return {}
        t2i = idea.get("template_to_idea") or {}
        expr_list = idea.get("expression_list") or []
        # template -> exposure
        tpl_exp = {}
        for tpl, idea_text in t2i.items():
            exp = _extract_exposure_from_idea(idea_text)
            if exp:
                tpl_exp[tpl] = exp
        # expression -> exposure（模板是 expression 的前缀/包含关系）
        out = {}
        for expr in expr_list:
            for tpl, exp in tpl_exp.items():
                # 模板中的 {variable} 已被替换为具体字段，做包含匹配
                tpl_prefix = tpl.split("{")[0] if "{" in tpl else tpl
                if tpl_prefix and tpl_prefix in expr:
                    out[expr] = exp
                    break
        return out
    except Exception:
        return {}


def check_batch_diversity(exprs, ctx, batch_type="explore", skip=False, dataset=None, delay=1):
    """闸6 批级多样性：强制落地多样性注入契约 + 收益来源多样性。

    契约来源（优先级）：
      1. 自学习规则引擎 explore_contract 规则（rules_mod.get_active_contract）——新路径
      2. 台账 diversity_audit_latest.next_round_injections——旧路径 fallback（兼容）
    规则：
      - batch_type 在契约 exempt 中（默认 repair）→ 豁免
      - consumed_batches 达到 expires_after_batches → 契约过期失效
      - 批内容哈希已在 consumed_batches → 已消费，不重复计数
      - 不达标 → issues 非空，拒绝提交（必须补注多样性槽位后重过闸）
    收益来源多样性（2026-08-26 新增）：
      - 从 DB idea ledger 提取每条 expression 的 expected_exposure
      - 同批 >60% 表达式共享同一 exposure 且字段族相同 → FAIL（伪多样性）
      - 无 exposure 元信息 → WARN 不阻断（向后兼容）
    返回 (issues, consume_ref)：consume_ref 仅在契约生效且全部达标时非空，
    为 {"digest":..., "rule_id":...|None}，由 main 在总闸通过后回写消费（幂等）。
    """
    if skip:
        return [], None

    # ---- P1-2 家族天花板预检（2026-08-31 新增，WARN 不阻断） ----
    # 主导腿信号族占比 ≥2/3 的批（wave94/95/98/104 实证 SELF≥0.9 必死），
    # 与闸6 的骨架/算子/exposure 多样性互补（字段信号族维度）。
    # WARN 不阻断：避免与现有契约冲突，仅提示建议分散。
    # 位置：skip 之后、契约检查之前——无论契约是否存在都执行的通用检查。
    if _check_family_ceiling is not None and len(exprs) >= 3:
        try:
            _fc_ok, _fc_reason, _fc_details = _check_family_ceiling(exprs)
            if not _fc_ok:
                print(f"[DIVERSITY-WARN][P1-2] 家族天花板预警：{_fc_reason}；"
                      f"建议分散信号族（momentum/value/quality/volatility/liquidity/sentiment/analyst）")
        except Exception as _e:
            print(f"[DIVERSITY-WARN][P1-2] 家族天花板预检异常（不阻断）: {_e}")

    # P0-2 (2026-08-25): 契约过期 = 静默 fail-open 修复。
    #   原 get_active_contract 在 consumed>=expires 时返回 None，使闸6 静默 vacuous 通过、
    #   四层多样性保证在无人察觉下悄悄失效。现以三态判定：
    #     - expired -> FAIL-CLOSED（阻断提交） + 自动续约新契约，要求重跑闸门按新契约校验本批
    #     - none    -> 维持现状（P0-3 待修：缺失契约亦应 fail-closed）
    #     - active  -> 正常校验
    inj = None
    rule_id = None
    try:
        _cstate, _cact = rules_mod.get_contract_expiry_state(ctx, batch_type=batch_type)
    except Exception:
        _cstate, _cact = "none", None
    if _cstate == "expired":
        _new_rid = rules_mod.renew_contract(ctx, _cact)
        _msg = (f"已自动续约新契约 {_new_rid}" if _new_rid
                else "自动续约失败，请手动调用 issue_contract 续约")
        return [f"[DIVERSITY-EXPIRED] 多样性注入契约已消费满 "
                f"{len(_cact.get('consumed_batches', []))}/"
                f"{_cact.get('expires_after_batches', 10)} 批，保证已静默失效；"
                f"{_msg}，请重跑闸门按新契约校验本批"], None
    if _cstate == "active":
        inj = _cact
        rule_id = _cact.get("_rule_id")
    # 旧路径 fallback：台账契约（兼容）
    if inj is None:
        try:
            state = make_ledger_store(ctx).load()
        except Exception:
            return [], None
        if not state:
            return [], None
        inj = (state.get("diversity_audit_latest") or {}).get("next_round_injections")
        if not inj:
            return [], None
        if batch_type in inj.get("exempt", []):
            return [], None
        # P0-2 旧路径同样 fail-closed：台账契约过期不再静默通过
        if len(inj.get("consumed_batches", [])) >= inj.get("expires_after_batches", 10):
            return [f"[DIVERSITY-EXPIRED] 台账多样性契约已消费满 "
                    f"{len(inj.get('consumed_batches', []))}/{inj.get('expires_after_batches', 10)} 批，"
                    f"保证已失效；请续约后重跑闸门"], None
    consumed = inj.get("consumed_batches", [])
    digest = batch_digest(exprs)
    if digest in consumed:
        return [], None
    issues = []
    req_ops = set(inj.get("required_operators", []))
    if req_ops:
        # fix(2026-08-25): (算子,字段) 组合去重计数——原实现只数"用了 required 算子的
        #   表达式条数"，导致两条 group_neutralize(同字段) 被误判为 2 份多样性。
        #   现改为：对每个含 required 算子的表达式，将其与表达式内全部叶子字段
        #   （不被 '(' 紧跟的非数字标识符）配对，按 (算子,字段) 互异组合计数。
        #   注：嵌套 required 算子会被扁平计为同一表达式的字段组合，属保守（不会虚增多样性）。
        _op_call = re.compile(r"([a-zA-Z_][a-zA-Z0-9_]*)\s*\(")
        # 叶子字段 = 不被 '(' 紧跟（忽略空白）的标识符，且非纯数字。
        # 用 \b 锁词边界，避免贪婪回退把算子名 group_neutralize 截成 group_neutraliz 当字段。
        _leaf = lambda e: {t for t in re.findall(r"([a-zA-Z_][a-zA-Z0-9_]*)\b(?!\s*\()", e)
                           if not t.isdigit()}

        def _expr_combos(e):
            ops_present = set(_op_call.findall(e)) & req_ops
            return {(op, f) for op in ops_present for f in _leaf(e)}

        per_expr = [_expr_combos(e) for e in exprs]
        combos = set().union(*per_expr) if per_expr else set()
        op_hits = len(combos)
        need = inj.get("per_batch_min_operators", 2)
        if op_hits < need:
            issues.append(
                f"[DIVERSITY] 注入算子(字段组合)达标 {op_hits}/{need}：每批至少 {need} 个"
                f"互异 (算子,字段) 组合使用 {sorted(req_ops)} 之一"
                f"（契约 issued_at={inj.get('issued_at')}）")
        # 可选冗余粗筛（无需收益数据）：两条表达式的 (算子,字段) 组合集完全相同
        #   = 结构性近重复信号，建议保留其一避免浪费配额（非阻断 WARN）。
        _sig_counter = collections.Counter(frozenset(c) for c in per_expr)
        for _s, _c in _sig_counter.items():
            if _c > 1 and _s:
                print(f"[DIVERSITY-WARN] 结构性近重复信号（{_c} 条共享组合集 "
                      f"{sorted(_s)}）——建议保留其一，避免浪费配额")
    skel_counts = collections.Counter(skeleton(e) for e in exprs)
    for name, quota in (inj.get("skeleton_quota") or {}).items():
        if skel_counts.get(name, 0) < quota:
            issues.append(f"[DIVERSITY] 骨架 {name} 达标 {skel_counts.get(name, 0)}/{quota}")

    # ---- 收益来源多样性闸（2026-08-26 新增） ----
    # 从 DB idea ledger 提取 expected_exposure，同批 >60% 共享同一 exposure 且字段族相同 → FAIL
    if dataset:
        exp_map = _load_exposure_map(ctx, dataset, delay=delay)
        if exp_map:
            # 提取字段族（字段前缀，如 starmine_/fnd72_/oth455_）
            def _field_family(e):
                fields = expr_fields(e, known_ops=None, min_len=6)
                if not fields:
                    return "unknown"
                # 取第一个字段的前缀（下划线第一段）
                f = sorted(fields)[0]
                return f.split("_")[0] if "_" in f else f[:6]

            exp_groups = collections.defaultdict(list)
            for e in exprs:
                exp = exp_map.get(e)
                if exp:
                    exp_groups[(exp, _field_family(e))].append(e)
            total_with_exp = sum(len(v) for v in exp_groups.values())
            if total_with_exp > 0:
                # 找最大组
                (top_exp, top_fam), top_exprs = max(exp_groups.items(), key=lambda kv: len(kv[1]))
                share = len(top_exprs) / len(exprs)
                if share > 0.6 and len(exprs) >= 3:
                    issues.append(
                        f"[DIVERSITY-EXPOSURE] 收益来源伪多样性：{len(top_exprs)}/{len(exprs)} "
                        f"({share:.0%}) 表达式共享 exposure={top_exp} + 字段族={top_fam}，"
                        f"结构不同但收益来源相同，回测必高相关；请换字段组合或换 exposure"
                    )
                elif share > 0.4:
                    print(f"[DIVERSITY-WARN] 收益来源集中：{share:.0%} 表达式共享 "
                          f"exposure={top_exp} + 字段族={top_fam}（建议分散）")
        else:
            print(f"[DIVERSITY-WARN] 无 expected_exposure 元信息（dataset={dataset}），"
                  f"收益来源多样性闸降级为 WARN；请确保 GEM prompt 要求输出 Expected Exposure")

    consume_ref = None if issues else {"digest": digest, "rule_id": rule_id}
    return issues, consume_ref


def consume_diversity(ctx, consume_ref):
    """闸6 契约消费回写（幂等，digest 去重）。

    rule_id 命中走规则引擎新路径（explore_contract），否则台账 fallback
    （diversity_audit_latest.next_round_injections.consumed_batches）。
    CLI main 与 pipeline 批级闸共用，保持两入口消费口径一致。
    """
    if not consume_ref:
        return
    digest = consume_ref["digest"]
    rule_id = consume_ref.get("rule_id")
    if rule_id:
        try:
            rules_mod.consume_contract(ctx, rule_id, digest)
        except Exception as e:
            print(f"[rules] 契约消费回写异常: {e}", file=sys.stderr)
    else:
        store = make_ledger_store(ctx)

        def consume(d):
            inj = (d.get("diversity_audit_latest") or {}).get("next_round_injections")
            if inj is not None:
                cb = inj.setdefault("consumed_batches", [])
                if digest not in cb:
                    cb.append(digest)

        store.update(consume)


# ---- 闸 7/8：数据质量预检（2026-08-23） ----

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
            cat_path = ctx.catalog_path(dataset)
            if os.path.exists(cat_path):
                cat = load_json(cat_path)
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


def check_sanity_event_type(ctx, dataset, exprs, field_types):
    """闸8：字段 type==EVENT 且表达式未使用 ts_event_* 算子 → FAIL。"""
    issues = []
    if not field_types:
        return issues
    EVENT_OPS = {"ts_event_avg", "ts_event_count", "ts_event_max", "ts_event_min",
                 "ts_event_rank", "ts_event_sum", "ts_event_zscore", "ts_event_delta"}
    for e in exprs:
        ops_used = set(re.findall(r'[a-zA-Z_][a-zA-Z0-9_]*\(', e))
        has_event_op = bool(ops_used & EVENT_OPS)
        field_ids = _parse_field_ids(e)
        for fid in field_ids:
            if field_types.get(fid) == "EVENT" and not has_event_op:
                issues.append(
                    f"[SANITY-EVENT-TYPE] {fid}: type=EVENT but no ts_event_* operator used "
                    f"(all non-event operators will error; see MEA fundamental6 trap)"
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


def check_priors(ctx, exprs, dataset, require_priors=False):
    """知识闸（KB-aware）：提交前波必须对照结构化 KB，否则静默漏掉已知死路。

    返回 dict: {applied, pass, sha, source, issues:[{code,severity,detail}]}

    行为：
      [PRIORS-MISSING]       priors 文件与 DB 兜底均无可用 KB
          severity = fail（若 --require-priors）否则 warn
      [PRIORS-DEADEND-HIT]   波数据集或表达式字段命中某 dead_end family
          severity = fail（若 --require-priors）否则 warn

    取数优先级：落盘 priors 文件 -> DB 兜底 assemble_priors_dict（保证闸永远 KB-aware，
    不依赖 assemble-priors 先跑过）。WARN 默认仅提示；--require-priors 上升为 FAIL。
    """
    issues = []

    # 1) 取 priors：优先落盘文件，缺失则 DB 兜底
    priors, source = None, "none"
    if load_priors_file is not None:
        try:
            priors = load_priors_file(ctx)
            if priors is not None:
                source = "file"
        except Exception:
            priors = None
    if not isinstance(priors, dict) or not (priors.get("wins") or priors.get("dead_ends")):
        if assemble_priors_dict is not None:
            try:
                priors = assemble_priors_dict(ctx)
                source = "db_fallback"
            except Exception:
                priors = None
    if not isinstance(priors, dict) or not (priors.get("wins") or priors.get("dead_ends")):
        sev = "fail" if require_priors else "warn"
        issues.append({"code": "PRIORS-MISSING", "severity": sev,
                       "detail": "无可用 KB（文件缺失且 DB 兜底为空）；GEM 可能重探已知死路"})
        return {"applied": False, "pass": sev != "fail", "sha": None,
                "source": source, "issues": issues}

    sha = None
    if priors_sha is not None:
        try:
            sha = priors_sha(ctx)
        except Exception:
            sha = None

    # 2) dead_end 命中检测（波数据集 + 表达式字段 vs dead_end family）
    dead = [d for d in (priors.get("dead_ends") or []) if isinstance(d, dict)]
    if dead and dataset:
        known_ops = set()
        try:
            known_ops = set(load_platform_constraints().get("known_ops", []))
        except Exception:
            pass
        fields = set()
        for e in exprs:
            fields |= expr_fields(e, known_ops)
        ds_l = dataset.lower()
        for d in dead:
            fam = (d.get("family") or "").lower()
            if not fam:
                continue
            hit = (ds_l in fam) or fam.startswith(ds_l) or any(f.lower() in fam for f in fields)
            if hit:
                sev = "fail" if require_priors else "warn"
                issues.append({
                    "code": "PRIORS-DEADEND-HIT", "severity": sev,
                    "detail": f"波数据集/字段命中 dead_end family='{d.get('family')}' "
                              f"reason={(d.get('reason') or '')[:120]}",
                })

    applied_pass = not any(i["severity"] == "fail" for i in issues)
    return {"applied": True, "pass": applied_pass, "sha": sha,
            "source": source, "issues": issues}


def main():
    ap = argparse.ArgumentParser(description="战役提交前 8 闸预检（+可选闸0 语义反模式）")
    add_campaign_arg(ap)
    ap.add_argument("--file")
    ap.add_argument("--expr")
    ap.add_argument("--from-db", action="store_true", help="从 expressions 表读本波候选")
    ap.add_argument("--wave", default=None, help="波号（--from-db 必填；写入 gate_results）")
    ap.add_argument("--dataset", required=True)
    ap.add_argument("--datasets", default="",
                    help="逗号分隔额外数据集，与 --dataset 合并白名单（跨金字塔 mix）")
    ap.add_argument("--no-cache", action="store_true")
    ap.add_argument("--cache-file", default=None,
                    help="缓存文件重定向（默认 <campaign>/cache/gate_cache.json；干跑验证用临时路径）")
    ap.add_argument("--batch-type", default="explore",
                    help="批次类型：explore=探索批（默认，受闸6 约束）；repair=修复/设置变体批（豁免）")
    ap.add_argument("--skip-diversity-gate", action="store_true",
                    help="跳过闸6 批级多样性强制（逃生阀，需在台账记录原因）")
    ap.add_argument("--fix", action="store_true",
                    help="自动修复：VECTOR 数据集下裸用的 VECTOR 字段裹上 vec_* 后再检测（幂等，输出 fixed_expr）")
    ap.add_argument("--sanity-longcount", action="store_true",
                    help="闸7：longCount 真实性校验（VECTOR 字段实际 longCount < 80 标记 WARN）")
    ap.add_argument("--sanity-event-type", action="store_true",
                    help="闸8：EVENT 类型自动检测（字段 type==EVENT 且未用 ts_event_* 标记 FAIL）")
    ap.add_argument("--sanity-all", action="store_true",
                    help="一次性跑闸 7+8（--sanity-longcount + --sanity-event-type）")
    ap.add_argument("--gate0", action="store_true",
                    help="闸0：语义反模式检查（恒等式/裸字段/元数据字段腿；默认关闭，命中即 FAIL）")
    ap.add_argument("--require-priors", action="store_true",
                    help="知识闸硬约束：priors 缺失或波命中 dead_end family 时 FAIL（默认仅 WARN）")
    a = ap.parse_args()
    ctx = CampaignContext(a.campaign_dir)

    if a.from_db:
        if not a.wave:
            ap.error("--from-db 需要 --wave")
        from _lib.wqb_store import get_store
        st = get_store(ctx)
        try:
            rows = st.list_expressions(ctx.region, str(a.wave), dataset=a.dataset)
            if not rows:
                rows = st.list_expressions(ctx.region, str(a.wave))
            exprs = [r["expression"] for r in rows
                     if r.get("expression") and r.get("status") != "superseded"]
        finally:
            st.close()
        if not exprs:
            ap.error(f"db 无表达式: {ctx.region} wave={a.wave} dataset={a.dataset}")
    elif a.file:
        exprs = read_exprs_any(a.file)
    elif a.expr:
        exprs = [a.expr]
    else:
        ap.error("need --from-db / --file / --expr")

    extra = [x.strip() for x in (a.datasets or "").split(",") if x.strip()]
    ds_all = [a.dataset] + [x for x in extra if x != a.dataset]
    wl = merge_whitelists(ctx, ds_all) if len(ds_all) > 1 else load_whitelist(ctx, a.dataset)
    pc = load_platform_constraints()
    poison = list(pc.get("poison_patterns", []))
    cons_path = ctx.constraints_path()
    if os.path.exists(cons_path):  # 区域特有 poison 追加（平台级勿复制进区域文件）
        poison += load_json(cons_path).get("poison_patterns", [])

    # --fix 会改写表达式，缓存键与原始表达式不一致，禁用缓存以免污染
    use_cache = not a.no_cache and not a.fix
    cache = {}
    cache_path = a.cache_file
    if use_cache and cache_path:
        cache = load_json(cache_path) if os.path.exists(cache_path) else {}
    elif use_cache:
        try:
            from _lib.wqb_store import get_store
            st = get_store(ctx)
            cache = st.get_ledger(ctx.region, f"gate_cache_{a.dataset}") or {}
            if not isinstance(cache, dict):
                cache = {}
            st.close()
        except Exception:
            cache = {}
    dirty = False
    report, all_pass = [], True
    for i, e in enumerate(exprs, 1):
        ck = cache_key(a.dataset, e)
        if use_cache and ck in cache:
            item = dict(cache[ck])
            item["index"] = i
            item["cached"] = True
        else:
            item = check_one(e, wl, a.dataset, poison, pc, fix=a.fix)
            item["index"] = i
            if use_cache:
                cache[ck] = {k: item[k] for k in ("fields", "issues", "pass")}
                dirty = True
        all_pass = all_pass and item["pass"]
        report.append(item)
    if dirty and use_cache:
        if cache_path:
            atomic_write(cache_path, cache)
        else:
            try:
                from _lib.wqb_store import get_store
                st = get_store(ctx)
                st.upsert_ledger(ctx.region, f"gate_cache_{a.dataset}", cache)
                st.close()
            except Exception:
                pass
    # 闸 7/8：数据质量预检（--sanity-* / --sanity-all）
    sanity_issues = []
    run_longcount = a.sanity_all or a.sanity_longcount
    run_event = a.sanity_all or a.sanity_event_type
    if run_longcount or run_event:
        _, data_type, field_types, _ = wl
        if run_longcount:
            sanity_issues.extend(check_sanity_longcount(ctx, a.dataset, exprs, field_types))
        if run_event:
            sanity_issues.extend(check_sanity_event_type(ctx, a.dataset, exprs, field_types))
        if sanity_issues:
            all_pass = False
    # 闸0 语义反模式（可选，--gate0；与闸 1-5 并列，不计入 check_one 的 issues）
    gate0_blocked = []
    if a.gate0:
        known_ops0 = set(pc["known_ops"])
        for e in exprs:
            g0 = check_semantic_gate0(e, known_ops=known_ops0)
            if g0:
                gate0_blocked.append({"expr": e, "issues": g0})
        if gate0_blocked:
            all_pass = False
    # 闸6 批级多样性（仅批量模式；契约存在且生效时强制）
    # --fix 时用修复后的表达式统计骨架/算子，与最终提交一致
    # 2026-09-01 单表达式豁免：单条调试（--expr）凑不齐批级配额（≥2 shapes/骨架配比），
    # 多样性闸自动跳过并注明；批级多样性约束仍由 build_wave/wave_gate 在批量场景强制。
    exprs_for_diversity = [r.get("fixed_expr", exprs[r["index"] - 1]) for r in report]
    if len(exprs_for_diversity) <= 1 and not a.skip_diversity_gate:
        dissues, consume_ref = [], None
        print("[DIVERSITY-SKIP] 单表达式模式：批级多样性闸不适用（≥2 表达式才评估），仅静态闸结果生效")
    else:
        dissues, consume_ref = check_batch_diversity(exprs_for_diversity, ctx, batch_type=a.batch_type,
                                                     skip=a.skip_diversity_gate, dataset=a.dataset)
    if dissues:
        all_pass = False
    if consume_ref is not None and all_pass:
        consume_diversity(ctx, consume_ref)
    # 知识闸（KB-aware）：对照结构化 KB，避免重探已知死路 / 收不到胜方配方
    priors_gate = check_priors(ctx, exprs, a.dataset, require_priors=a.require_priors)
    if not priors_gate["pass"]:
        all_pass = False
    payload = {"all_pass": all_pass, "dataset": a.dataset, "total": len(exprs),
                      "passed": sum(r["pass"] for r in report),
                      "cached": sum(1 for r in report if r.get("cached")),
                      "sanity_gates": {
                          "applied": bool(sanity_issues) or run_longcount or run_event,
                          "pass": not sanity_issues,
                          "issues": sanity_issues},
                      "diversity_gate": {
                          "applied": consume_ref is not None or bool(dissues),
                          "pass": not dissues,
                          "issues": dissues,
                          "consumed": consume_ref is not None},
                      "priors_gate": priors_gate,
                      "report": report}
    if a.gate0:  # 仅在开启时附加，缺省输出结构与历史完全一致
        payload["gate0"] = {"checked": len(exprs), "blocked": gate0_blocked}
    if a.wave:
        try:
            from _lib.wqb_store import get_store
            st = get_store(ctx)
            st.upsert_gate_result(ctx.region, str(a.wave), a.dataset, payload)
            st.close()
        except Exception as e:
            print(f"[gate] 入库异常: {e}", file=sys.stderr)
    print(json.dumps(payload, ensure_ascii=False, indent=1))
    sys.exit(0 if all_pass else 1)


if __name__ == "__main__":
    main()
