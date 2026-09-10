# -*- coding: utf-8 -*-
"""build_wave.py - 统一选波器。

能力:
  - 全历史去重：对战役目录全部 <region>_wave*_exprs.json / candidates/*.json 建表达式
    哈希集，重复候选直接丢弃（KOR 实测 92/854 重复 = 11% 配额浪费）
  - 算子树分桶：根调用 + 第一个函数参数作桶键（如 add>multiply、rank>ts_av_diff），
    取代 startswith 前缀碰撞分桶
  - 骨架配给制：按 reference/<region>_generation_constraints.json 的 skeleton_quota
    限制 linear_mix 占比（默认 ≤50%），强制事件门控/group/ratio 骨架进入候选（直击 CW 墙根因）
  - near-miss 加权：wave_results 表 near 池 + 台账 near_pool 的字段，候选优先
  - 波内字段去重：同一字段在单波出现次数上限

用法:
  python build_wave.py --campaign-dir <DIR> --file candidates/new_exprs.json --wave 01A [--size 48] [--per-bucket 8]
输出:
  candidates/<region>_wave<wave>_exprs.json
"""
import argparse
import collections
import datetime
import glob
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _lib.common import (CampaignContext, add_campaign_arg, bucket_key,
                         expr_fields, load_json, load_platform_constraints, norm_expr,
                         read_exprs_file, skeleton)
from _lib.ledger import make_ledger_store
from _lib import rules as rules_mod
from _lib.wqb_store import get_store

# 波指纹：把本波绑定到当前 GEM priors 文件的 sha256（KB 状态可回溯）。
# 缺失（文件未生成）记 None，不作为选波失败条件。
try:
    from assemble_priors import priors_sha as _priors_sha
except Exception:  # 模块缺失时降级，不影响选波主流程
    _priors_sha = None

try:
    from _lib.diversity_enhancer import enhance_if_needed
    _DIVERSITY_AVAILABLE = True
except Exception as _e:  # 模块缺失或依赖不全时降级
    _DIVERSITY_AVAILABLE = False
    _DIVERSITY_ERR = str(_e)
else:
    _DIVERSITY_ERR = None


def _workspace_root_from_campaign(campaign_dir):
    """从 campaign_dir 向上推导工作区根（与 wqb_store._workspace_roots 同源信号）。

    skill 安装位（%USERPROFILE%\\.claude\\skills\\...）与工作区不同树，靠 __file__ 向上
    永远找不到；但 campaign_dir 总是形如 <工作区根>/tracking/<REGION>，向上两三层
    即命中。认据：存在 src/wqb 或 data/wqb.db。找不到时回落环境变量。
    """
    if campaign_dir:
        p = os.path.abspath(campaign_dir)
        for _ in range(8):
            if os.path.isdir(os.path.join(p, "src", "wqb")) or \
                    os.path.isfile(os.path.join(p, "data", "wqb.db")):
                return p
            parent = os.path.dirname(p)
            if parent == p:
                break
            p = parent
    for env in ("WQB_WORKSPACE_ROOT", "WQB_ROOT", "WQ_PROJECT_ROOT"):
        root = os.environ.get(env)
        if root and os.path.isdir(os.path.join(root, "src", "wqb")):
            return root
    return None


def _workspace_src_from_campaign(campaign_dir):
    """工作区 src/ 目录（wqb 规范核心包所在）。"""
    root = _workspace_root_from_campaign(campaign_dir)
    if root:
        src = os.path.join(root, "src")
        if os.path.isdir(os.path.join(src, "wqb")):
            return src
    return None


def _retry_diversity_import(campaign_dir):
    """救回多样性增强：把的工作区 src 注入 sys.path 并重载 _lib.diversity_enhancer。

    2026-09-09：_lib/diversity_enhancer.py 靠 __file__ 向上找 src/wqb，在 skill 安装位
    下必然 ImportError。但它把异常吃掉只设模块内 DIVERSITY_AVAILABLE=False，模块
    本身仍可导入 —— 于是 build_wave 的 _DIVERSITY_AVAILABLE 是 True（假可用），实际调用
    enhance_if_needed 时内部降级返回原列表，「多样性增强」这一选波维度每波都未生效
    （wave_meta.diversity_enhanced 恒为 false）。本函数按内部真实状态判定并强制重载。
    """
    global _DIVERSITY_AVAILABLE, _DIVERSITY_ERR, enhance_if_needed
    # 真实可用性看模块内部的 DIVERSITY_AVAILABLE，不是看导入是否抛异常
    try:
        import _lib.diversity_enhancer as _de
        inner_ok = bool(getattr(_de, "DIVERSITY_AVAILABLE", False))
    except Exception:
        inner_ok = False
    if inner_ok:
        _DIVERSITY_AVAILABLE = True
        _DIVERSITY_ERR = None
        return True
    src = _workspace_src_from_campaign(campaign_dir)
    if not src:
        _DIVERSITY_AVAILABLE = False
        _DIVERSITY_ERR = ("wqb 不可用且未能从 campaign_dir 推导工作区根；"
                          "设 WQB_WORKSPACE_ROOT 可解")
        return False
    if src not in sys.path:
        sys.path.insert(0, src)
    for mod in [m for m in list(sys.modules)
                if m == "_lib.diversity_enhancer" or m.startswith("_lib.diversity_enhancer.")]:
        del sys.modules[mod]
    try:
        import _lib.diversity_enhancer as _de2
        from _lib.diversity_enhancer import enhance_if_needed as _enh
    except Exception as _e2:
        _DIVERSITY_AVAILABLE = False
        _DIVERSITY_ERR = str(_e2)
        return False
    if not getattr(_de2, "DIVERSITY_AVAILABLE", False):
        _DIVERSITY_AVAILABLE = False
        _DIVERSITY_ERR = "重载后 wqb 仍不可导入"
        return False
    enhance_if_needed = _enh
    _DIVERSITY_AVAILABLE = True
    _DIVERSITY_ERR = None
    print(f"[diversity] 工作区 src 解析成功，多样性增强已启用 <- {src}")
    return True


def _load_vector_wrap(campaign_dir=None):
    """载入 tools/lib/vector_wrap.wrap_naked_vectors（单一权威源，与 gate.py 同模式）。

    2026-09-09：原相对推导从 __file__ 向上 5 层，在 skill 安装位下落到
    ``C:\\Users\\tools\\lib`` 而返回 None，使得契约因子的 VECTOR 包裹静默不生效。
    现优先用 campaign_dir 推导工作区根（与 DB 定位同源），环境变量次之。
    """
    cands = []
    env = os.environ.get("WQB_TOOLS_LIB")
    if env:
        cands.append(env)
    root = _workspace_root_from_campaign(campaign_dir)
    if root:
        cands.append(os.path.join(root, "tools", "lib"))
    for e in ("WQB_ROOT", "WQB_WORKSPACE_ROOT", "WQ_PROJECT_ROOT"):
        r = os.environ.get(e)
        if r:
            cands.append(os.path.join(r, "tools", "lib"))
    for c in cands:
        if c and os.path.isfile(os.path.join(c, "vector_wrap.py")):
            if c not in sys.path:
                sys.path.insert(0, c)
            try:
                from vector_wrap import wrap_naked_vectors
                return wrap_naked_vectors
            except Exception:
                return None
    return None


def _vector_field_ids(ctx, dataset):
    """从 typed catalog 取本数据集的 VECTOR 字段名列表（供 wrap_naked_vectors 消费）。"""
    if not dataset:
        return []
    try:
        from _lib.wqb_store import load_catalog
        cat = load_catalog(ctx, dataset) or {}
    except Exception:
        return []
    out = []
    for f in (cat.get("fields") or []):
        if not isinstance(f, dict):
            continue
        fid = f.get("id")
        if fid and str(f.get("type", "")).upper() == "VECTOR":
            out.append(fid)
    return out


def _dataset_data_type(ctx, dataset):
    """本数据集的 data_type（VECTOR/MATRIX）；无法判定时返回 None。"""
    if not dataset:
        return None
    try:
        from _lib.wqb_store import load_catalog
        cat = load_catalog(ctx, dataset) or {}
    except Exception:
        return None
    dt = str(cat.get("data_type") or "").upper()
    if dt in ("VECTOR", "MATRIX"):
        return dt
    dist = cat.get("type_distribution") or {}
    if dist:
        return max(dist, key=lambda k: dist[k])
    return None


def _drop_type_mismatched(exprs, data_type, known_ops=None):
    """丢弃与当前数据集类型不兼容的因子（与 gate 闸3 TYPE 判定同源）。

    2026-09-09：契约模板里的 vec_* 是【签发时按 anchor 数据集类型固化的字面量】，
    而实例化用的是当前波次数据集的角色池 —— 两者类型可能不匹配（anchor 含 VECTOR
    而当前集是纯 MATRIX），而字面量无法被角色池过滤掉。EUR wave142 实测：
    dl_riskfree_returns（纯 MATRIX）拿到了 vec_max(...) 因子，撞 gate 的
    [TYPE] MATRIX 数据集禁用 vec_* 闸。这里在注入前按同一权威名单预先过滤，
    不白占候选名额（否则七槽会被注定过不了闸的因子挤掉）。
    """
    if data_type != "MATRIX" or not exprs:
        return exprs, []
    try:
        vec_ops = set(load_platform_constraints().get("vector_only_ops", []))
    except Exception:
        return exprs, []
    if not vec_ops:
        return exprs, []
    kept, dropped = [], []
    tok = re.compile(r"([a-zA-Z_][a-zA-Z0-9_]*)\s*\(")
    for e in exprs:
        used = set(tok.findall(e or ""))
        if used & vec_ops:
            dropped.append(e)
        else:
            kept.append(e)
    return kept, dropped


def _load_arity_check(campaign_dir=None):
    """载入 wqb.expression.op_arity.check_expression（与 gate.py 闸1 同源权威）。

    2026-09-09：多样性增强的变异引擎不仅会吃掉外层算子，还会产出算子元数
    不足的式子（EUR wave140 id=11474：trade_when 需 3 参只给 2）。结构体检（括号/
    顶层逗号/根调用）挡不住这类错误，必须复用平台元数校验的单一权威源，
    不自己手写元数表（手写表必与平台 catalog 漂移，正是 2026-09-07 hump 事故的根因）。
    """
    src = _workspace_src_from_campaign(campaign_dir)
    if not src:
        return None
    if not os.path.isfile(os.path.join(src, "wqb", "expression", "op_arity.py")):
        return None
    if src not in sys.path:
        sys.path.insert(0, src)
    try:
        from wqb.expression.op_arity import check_expression as _chk
        return _chk
    except Exception:
        return None


def _expr_structurally_sane(expr, arity_check=None):
    """表达式结构体检：括号平衡 + 单一根调用 + 无顶层逗号。

    2026-09-09：diversity_enhancer 的变异引擎会产出「吃掉外层算子」的残缺式
    （实测：group_mean(vec_avg(a), vec_sum(b), sector) 被变异成
    「vec_avg(a), vec_sum(b), sector」）。该残缺式括号计数恰好平衡（内外层各自
    平衡），所以单看括号数抓不到 —— 必须同时查「顶层逗号」与「根调用形式」。
    本函数作为选波消费端的 fail-safe 守卫：无论上游如何变异，残缺式不得入候选池。
    """
    if not expr or not isinstance(expr, str):
        return False
    s = expr.strip()
    if s.count("(") != s.count(")"):
        return False
    # 顶层逗号 = 根调用被剥掉的铁证（合法单表达式顶层不可能有逗号）
    depth = 0
    for ch in s:
        if ch == "(":
            depth += 1
        elif ch == ")":
            depth -= 1
            if depth < 0:
                return False
        elif ch == "," and depth == 0:
            return False
    # 根必须是 func(...) 形式
    if not re.match(r"^[a-zA-Z_][a-zA-Z0-9_]*\(.*\)$", s, re.S):
        return False
    # 算子元数校验（平台 catalog 驱动的单一权威源）：挡住变异引擎产出的
    # 「参数个数不对」类非法式（如 trade_when 需 3 参只给 2）。
    if arity_check is not None:
        try:
            res = arity_check(s)
        except Exception:
            return True  # 校验器自身异常时不阻断（fail-open），交由 gate 闸1 兜底
        if isinstance(res, tuple):
            ok = res[0] if res else True
        elif isinstance(res, dict):
            ok = res.get("valid", res.get("ok", True))
        elif isinstance(res, list):
            ok = len(res) == 0
        else:
            ok = bool(res)
        if not ok:
            return False
    return True


def history_hashes(ctx, exclude_path=None, exclude_waves=None):
    seen = set()
    # 2026-09-06：DB 读失败原为 `except Exception: pass` —— 静默 fail-open。
    # 「全量切库」后战役目录已基本不再写 <region>_wave*_exprs.json / candidates/*.json，
    # 文件语料只剩历史残留，DB 一旦读不到，去重就退化成"几乎什么都不认识"，
    # 而调用方看到的仍是一个正常的 n_dup 数字。现在必须喊出来。
    try:
        st = get_store(ctx)
        for e in st.history_expressions(ctx.region, exclude_waves=exclude_waves):
            seen.add(norm_expr(e))
        st.close()
    except Exception as _e:
        print(f"[dedup][WARN] 读 DB 历史表达式失败：{_e}；"
              f"本波去重将只依赖文件语料（切库后已近乎为空），重复率会被严重低估")
    excl = os.path.normcase(os.path.abspath(exclude_path)) if exclude_path else None
    files = glob.glob(ctx.path(f"{ctx.prefix}_wave*_exprs.json")) + \
        glob.glob(ctx.path("candidates", "*.json"))
    for f in files:
        if excl and os.path.normcase(os.path.abspath(f)) == excl:
            continue
        try:
            for e in read_exprs_file(f):
                seen.add(norm_expr(e))
        except Exception:
            continue
    return seen


def near_fields(ctx):
    """wave_results 表 near 池 + 台账 near_pool 的字段集合（增强优先）。

    2026-08-22 起：reviews/*.json 已淘汰，near 池从 wave_results.full_payload.near 读。
    保留台账 near_pool 作为补充来源。
    """
    flds = set()
    import re
    # wave_results 表 near 池（替代 reviews/*.json）
    try:
        from _lib.wave_results import WaveResultsStore
        wr = WaveResultsStore(ctx.region)
        for row in wr.list():
            full = wr.get(row["wave_number"])
            if not full or not full.get("full_payload"):
                continue
            payload = json.loads(full["full_payload"]) if isinstance(full["full_payload"], str) else full["full_payload"]
            for n in (payload.get("near") or []):
                for tok in re.findall(r"[a-zA-Z_][a-zA-Z0-9_]*", n.get("code", "")):
                    if len(tok) > 6:
                        flds.add(tok)
    except Exception:
        pass
    # 台账 near_pool（单轨 DB 模式：走 make_ledger_store）
    try:
        led = make_ledger_store(ctx).load()
    except Exception:
        led = {}
    for entry in led.get("near_pool", []):
        for n in entry.get("near", []):
            for tok in re.findall(r"[a-zA-Z_][a-zA-Z0-9_]*", str(n.get("id", ""))):
                if len(tok) > 6:
                    flds.add(tok)
    return flds


def load_family_map(exprs_path=None, meta_file=None):
    """加载 final_expressions_meta.json 的 expr->family 映射（P3: family 标签贯穿分桶）。

    显式 --meta-file 优先；否则在 --file 同目录自动探测 final_expressions_meta.json。
    返回 {norm_expr(expr): family}；无 meta 时返回 {}（回落算子树分桶）。
    """
    cands = []
    if meta_file:
        cands.append(meta_file)
    if exprs_path:
        cands.append(os.path.join(os.path.dirname(os.path.abspath(exprs_path)),
                                  "final_expressions_meta.json"))
    for p in cands:
        if not p or not os.path.exists(p):
            continue
        try:
            data = load_json(p)
        except Exception:
            continue
        items = data if isinstance(data, list) else (
            data.get("metas") or data.get("items") or [] if isinstance(data, dict) else [])
        fam_map = {}
        for it in items:
            if not isinstance(it, dict):
                continue
            ex, fam = it.get("expr"), it.get("family")
            if ex and fam:
                fam_map[norm_expr(ex)] = str(fam)
        if fam_map:
            print(f"[family] meta 载入 {len(fam_map)} 条 family 标签 <- {p}")
            return fam_map
    return {}


def main():
    ap = argparse.ArgumentParser(description="战役统一选波器")
    add_campaign_arg(ap)
    ap.add_argument("--file", default=None, help="兼容：表达式 JSON（已废弃，请 --from-db）")
    ap.add_argument("--from-db", action="store_true", help="从 expressions 表读 GEM/上游候选")
    ap.add_argument("--dataset", default=None, help="数据集（--from-db 时用于定位 GEM 源）")
    ap.add_argument("--wave", required=True)
    ap.add_argument("--size", type=int, default=48)
    ap.add_argument("--per-bucket", type=int, default=8)
    ap.add_argument("--meta-file", default=None,
                    help="final_expressions_meta.json 路径（family 标签分桶）；缺省在 --file 同目录自动探测")
    ap.add_argument("--max-field-repeat", type=int, default=3)
    ap.add_argument("--enhance-diversity", default="always", choices=["auto", "always", "never"],
                    help="多样性增强模式：always=强制增强（默认），auto=不足时增强，never=禁用")
    ap.add_argument("--auto-coverage", default="auto", choices=["auto", "always", "never"],
                    help="算子全覆盖：auto=无活跃契约时自动签发并注入（默认）；"
                         "always=每波强制重签；never=禁用（不签发不注入）")
    ap.add_argument("--coverage-per-wave", type=int, default=12,
                    help="自动签发时本波覆盖的欠用算子数（默认 12）")
    a = ap.parse_args()
    ctx = CampaignContext(a.campaign_dir)
    # 2026-09-09：ctx 就绪后补一次工作区 src 解析，救回模块级导入失败的多样性增强
    # （skill 安装位与工作区不同树时 __file__ 向上推导必然失败）。
    _retry_diversity_import(a.campaign_dir)
    # 算子名单（平台约束单一事实源）：字段重复上限只统计真字段，算子 token 不占额度
    known_ops = set(load_platform_constraints().get("known_ops", []))

    quota = {"linear_mix": 0.5}
    cons_path = ctx.constraints_path()
    if os.path.exists(cons_path):
        quota = load_json(cons_path)["injection_rules"]["skeleton_quota"]
        quota = {k.split("(")[0]: v for k, v in quota.items()}
    lm_cap = quota.get("linear_mix", 0.5)

    exprs = []
    if a.from_db or not a.file:
        st = get_store(ctx)
        try:
            rows = st.list_expressions(ctx.region, str(a.wave), dataset=a.dataset)
            if not rows and a.dataset:
                delay = ctx.settings.get("delay", 1)
                src_wave = f"s2_{a.dataset}_d{delay}"
                rows = st.list_expressions(ctx.region, src_wave, dataset=a.dataset)
            # 2026-09-09 D11 修复：候选读取同时排除 dropped 与 superseded。
            # 此前只排 superseded，Agent 手动 dropped 的零 alpha 骨架（iso_week_number
            # 等日历哑字段）会被重选回 selected，纪律废弃形同虚设。
            exprs = [r["expression"] for r in rows
                     if r.get("expression") and r.get("status") not in ("superseded", "dropped")]
        finally:
            st.close()
        if not exprs and a.file:
            exprs = read_exprs_file(a.file)
        elif not exprs:
            raise SystemExit(f"[build_wave] db 无候选: {ctx.region} wave={a.wave} dataset={a.dataset}")
    else:
        exprs = read_exprs_file(a.file)

    # ---- 算子全覆盖：自动签发（③b）+ 自动注入契约因子（③a）（region 无关） ----
    # 2026-08-18：plan_coverage_wave 签发的 explore_contract 带 factor_templates
    # （每个 required 算子的有经济含义实例化因子）。build_wave 自动注入候选池头部，
    # 让 required 算子参与分桶/配给，闸6 能命中（否则候选无这些算子会被闸6 卡死）。
    # --auto-coverage：auto=无活跃契约时自动签发下一波；always=每波强制重签；never=禁用。
    cov_injected = 0
    cov_signed = None
    if a.auto_coverage != "never":
        try:
            from _lib import operator_coverage as oc
            act0 = rules_mod.get_active_contract(ctx, batch_type="explore")
            need_sign = (a.auto_coverage == "always") or (act0 is None)
            if need_sign:
                plan = oc.plan_coverage_wave(
                    ctx, cover_per_wave=a.coverage_per_wave,
                    semantic=True, write_candidates=False)  # 注入走 factor_templates，不落盘
                cov_signed = plan.get("contract_rule_id")
                tag = "强制重签" if a.auto_coverage == "always" else "无活跃契约自动签发"
                print(f"[coverage] {tag}：{cov_signed} "
                          f"（anchor={plan.get('anchor_dataset')}，"
                          f"required={plan.get('n_cover')}，degraded={plan.get('degraded')}）")
        except Exception as _se:
            print(f"[coverage] 自动签发跳过：{_se}")
    # 注入活跃契约的实例化因子（2026-08-25 ②：骨架优先，按当前数据集实例化）
    # 修复双重失效：(a) 锚点字段表达式跨数据集撞 FIELD 闸；(b) 固定表达式被历史去重杀死。
    # 优先级：骨架（template+roles，用当前 --dataset 的 catalog 角色池实例化）> legacy expr。
    try:
        act = rules_mod.get_active_contract(ctx, batch_type="explore")
        if act:
            ft = act.get("factor_templates") or {}
            cov_exprs = []
            skeleton_used, skeleton_fallback = 0, 0
            legacy_used, legacy_skipped = 0, 0
            for op, v in ft.items():
                if not isinstance(v, dict):
                    continue
                # 2026-09-09 修复（legacy 契约死锁）：签发端把算子名同时写在 dict key
                # 和 value["op"] 两处，但 2026-09-03 之前签发的旧契约只有 key、value 内
                # 无 "op" 字段。原守卫 `v.get("op")` 会把旧契约的模板 12/12 全部跳过，
                # 导致 coverage_injected 恒为 0、契约 required 算子永不进候选池、gate 闸6
                # 每波必然 FAIL；而 need_sign=(always) or (act0 is None) 又因旧契约仍
                # active 而永不重签 —— 形成死锁（EUR 实测卡死 7 波）。
                # 现以 key 兜底：value["op"] 优先，缺失时回落 dict key。
                op = v.get("op") or op
                expr = None
                if v.get("skeleton") and v.get("template") and a.dataset:
                    # 骨架路径：用当前波次数据集的角色池实例化
                    try:
                        from _lib import operator_coverage as _oc
                        _role_pool, _hv, _af = _oc.dataset_role_pool(ctx, a.dataset)
                        if _af:
                            expr, _flds, _mean = _oc.instantiate_factor(
                                op, _role_pool, window=20,
                                semantics={op: {
                                    "template": v.get("template"),
                                    "roles": v.get("roles") or ["signal_any", "window"],
                                    "meaning": v.get("meaning") or "",
                                    "category": v.get("category"),
                                }})
                            if expr:
                                skeleton_used += 1
                    except Exception as _ske:
                        print(f"[coverage] 骨架实例化失败 {op}: {_ske}")
                if expr is None and v.get("expr"):
                    expr = v["expr"]  # legacy 锚点表达式回退
                    if v.get("skeleton"):
                        skeleton_fallback += 1
                    else:
                        legacy_used += 1
                if expr and expr not in cov_exprs:
                    cov_exprs.append(expr)
            # 2026-09-09 修复：契约因子也要过 VECTOR 自动包裹。骨架实例化用的是
            # catalog 里的裸字段名，VECTOR 数据集（如 fund_holdings_panel）下会直接
            # 撞 gate 的 [EVENT] 事件型字段必须经 vec_* 聚合 闸（EUR wave137 实测
            # 注入 4 条中 3 条被拦）。GEM 侧有同一道处理（run_pipeline 的
            # [vector-wrap]），契约注入侧漏了 —— 复用 tools/lib 单一权威源补齐。
            _wrap = _load_vector_wrap(a.campaign_dir)
            _vfields = _vector_field_ids(ctx, a.dataset) if _wrap else []
            if _wrap and _vfields:
                _n_wrapped = 0
                _fixed = []
                for _e in cov_exprs:
                    _ne, _wf = _wrap(_e, _vfields)
                    if _wf:
                        _n_wrapped += 1
                    _fixed.append(_ne)
                # 包裹后可能产生重复，去重保序
                _seen, _uniq = set(), []
                for _e in _fixed:
                    if _e not in _seen:
                        _seen.add(_e)
                        _uniq.append(_e)
                cov_exprs = _uniq
                if _n_wrapped:
                    print(f"[coverage] vector-wrap 修复 {_n_wrapped} 条裸用 VECTOR 字段的契约因子"
                          f"（数据集 {a.dataset} 含 {len(_vfields)} 个 VECTOR 字段）")
            # 类型不兼容过滤：MATRIX 数据集丢弃带 vec_* 的因子（契约模板字面量
            # 是签发时按 anchor 集类型固化的，与当前波次集可能不匹配）。
            _dtype = _dataset_data_type(ctx, a.dataset)
            cov_exprs, _dropped = _drop_type_mismatched(cov_exprs, _dtype)
            if _dropped:
                print(f"[coverage] 类型过滤：丢弃 {len(_dropped)} 条与 {a.dataset}"
                      f"（{_dtype}）不兼容的 vec_* 因子（否则必撞 gate 闸3 TYPE）")
            if cov_exprs:
                before = set(exprs)
                new_exprs = [e for e in cov_exprs if e not in before]
                exprs = new_exprs + exprs  # 契约因子优先（头部）
                cov_injected = len(new_exprs)
                if cov_injected:
                    print(f"[coverage] 注入契约 {act.get('_rule_id')} 的 {cov_injected} 个因子 "
                          f"(骨架实例化 {skeleton_used}，legacy 回退 {skeleton_fallback}，"
                          f"旧契约 expr {legacy_used}，"
                          f"required={len(act.get('required_operators', []))} 算子)")
                elif legacy_used and not skeleton_used:
                    # 旧契约的固定 expr 已全部被历史去重吃掉 —— 这是重签契约的信号，
                    # 不能静默（静默则闸6 每波 FAIL 而无人知道该重签）。
                    print(f"[coverage] WARN: 旧契约 {act.get('_rule_id')} 的 {legacy_used} 个 "
                          f"legacy expr 已全部命中历史去重，注入 0 条；骨架路径不可用"
                          f"（模板无 skeleton）。请用 --auto-coverage always 重签契约以激活"
                          f"按当前数据集实例化的骨架注入，否则闸6 每波必然 FAIL。")
    except Exception as _ce:
        print(f"[coverage] 契约注入跳过：{_ce}")

    # ---- L3 规则硬门：选波前排除命中 dead_end 规则的骨架/模式 ----
    uni = ctx.settings.get("universe")
    dead_rules = rules_mod.apply_rules(ctx, "dead_end",
                                       {"region": ctx.region, "universe": uni})
    if dead_rules:
        before = len(exprs)
        blocked = []
        for r in dead_rules:
            pat = (r.get("action") or {}).get("block_pattern")
            if pat:
                import re as _re
                kept = [e for e in exprs if not _re.search(pat, e)]
                blocked += [e for e in exprs if e not in kept]
                exprs = kept
        if blocked:
            print(f"[rules][dead_end] 排除 {len(blocked)}/{before} 条命中判死规则的表达式")
    # 策略规则提示（不拦截，仅提示当前上下文可用策略）
    for r in rules_mod.apply_rules(ctx, "strategy",
                                   {"region": ctx.region, "universe": uni}):
        print(f"[rules][strategy:{r['rule_id']}] {r.get('action', {}).get('message', '')}")

    delay = ctx.settings.get("delay", 1)
    src_wave = f"s2_{a.dataset}_d{delay}" if a.dataset else None
    hist = history_hashes(
        ctx, exclude_path=a.file,
        exclude_waves=[str(a.wave)] + ([src_wave] if src_wave else []),
    )
    deduped = [e for e in exprs if norm_expr(e) not in hist]
    n_dup = len(exprs) - len(deduped)

    nf = near_fields(ctx)
    # near-miss 加权：含 near 字段者优先，其余保持原序
    deduped.sort(key=lambda e: 0 if expr_fields(e, known_ops) & nf else 1)

    # P3: family 标签（skeleton mode meta）增强分桶；无标签式回落算子树 bucket_key
    family_map = load_family_map(a.file, a.meta_file)

    def wave_bucket(expr):
        fam = family_map.get(norm_expr(expr))
        return f"family:{fam}" if fam else bucket_key(expr)

    buckets = collections.defaultdict(list)
    for e in deduped:
        buckets[wave_bucket(e)].append(e)
    bucket_sizes = {k: len(v) for k, v in sorted(buckets.items())}  # 抽样前记录桶规模

    picked, field_count, lm_count = [], collections.Counter(), 0
    # 轮转分桶抽样：每桶最多 per-bucket；linear_mix 骨架受配额约束
    progress = True
    while progress and len(picked) < a.size:
        progress = False
        for bk in sorted(buckets):
            lst = buckets[bk]
            while lst and len(picked) < a.size:
                e = lst[0]
                sk = skeleton(e)
                if sk == "linear_mix" and lm_count >= max(1, int(a.size * lm_cap)):
                    break  # 该桶剩余留到下轮（linear_mix 已满配额）
                if sum(1 for f in expr_fields(e, known_ops) if field_count[f] >= a.max_field_repeat) > 0:
                    lst.pop(0)  # 字段超限，弃此式看下一式
                    continue
                lst.pop(0)
                picked.append(e)
                for f in expr_fields(e, known_ops):
                    field_count[f] += 1
                if sk == "linear_mix":
                    lm_count += 1
                progress = True
                if len([x for x in picked if wave_bucket(x) == bk]) >= a.per_bucket:
                    break

    sk_dist = collections.Counter(skeleton(e) for e in picked)
    fam_dist = collections.Counter(
        family_map[norm_expr(e)] for e in picked if norm_expr(e) in family_map)

    # 多样性增强（可选）
    diversity_report = None
    if a.enhance_diversity != "never":
        if not _DIVERSITY_AVAILABLE:
            print(f"[diversity] 模块不可用，已禁用：{_DIVERSITY_ERR}")
        else:
            alpha_list_for_enhance = [{"regular": e, "settings": {}} for e in picked]
            enhanced_list, diversity_report = enhance_if_needed(
                alpha_list_for_enhance, mode=a.enhance_diversity)
            if diversity_report.get("enhanced"):
                # enhance_if_needed 返回元素键为 "regular"（保持输入格式），非 "expression"
                candidate = [item["regular"] for item in enhanced_list]
                _arity = _load_arity_check(a.campaign_dir)
                # 2026-09-09 fail-safe 守卫：上游 enhance_diversity 会「变异 + 追加
                # novel/random + 裁剪重排」，返回列表与输入已不一一对应，而包装层
                # 仍按索引写回 —— 实测会把变异引擎产出的残缺式（外层算子被吃掉）
                # 塞进候选池，导致 gate 语法闸 FAIL（EUR wave139 id=11471：
                # group_mean(vec_avg(a), vec_sum(b), sector) 变成裸参数列表）。
                # 这里逐条体检，不合格则整批回退到增强前：宁可不增强，不注入非法式。
                bad = [e for e in candidate if not _expr_structurally_sane(e, _arity)]
                if bad:
                    print(f"[diversity] WARN: 增强产出 {len(bad)}/{len(candidate)} 条非法式"
                          f"（结构残缺或算子元数不符），整批回退到增强前。"
                          f"示例：{bad[0][:88]}")
                    diversity_report["enhanced"] = False
                    diversity_report["rejected_broken"] = len(bad)
                    diversity_report["broken_examples"] = bad[:3]
                elif len(candidate) != len(picked):
                    # 数量不一致 = 上游追加/裁剪过，按索引写回必然张冠李戴
                    print(f"[diversity] WARN: 增强后数量 {len(candidate)} != 原 {len(picked)}，"
                          f"上游已追加/裁剪，按索引写回会张冠李戴，整批回退到增强前。")
                    diversity_report["enhanced"] = False
                    diversity_report["count_mismatch"] = {
                        "original": len(picked), "enhanced": len(candidate)}
                else:
                    picked = candidate
                    sk_dist = collections.Counter(skeleton(e) for e in picked)
                    fam_dist = collections.Counter(
                        family_map[norm_expr(e)] for e in picked if norm_expr(e) in family_map)
                    print(f"[diversity] 增强 {diversity_report.get('original_count')} -> "
                          f"{diversity_report.get('enhanced_count')} 表达式（结构体检全通过）")

    # ④ 多样性自愈（2026-08-25）：选波结果若命中契约 required 算子数不足，
    # 用骨架按当前数据集实例化补齐（限一轮补注），保证落库波结构性过闸6，
    # 不依赖调用方记得传 ideas 文件或 gate 后回环。
    try:
        _act = rules_mod.get_active_contract(ctx, batch_type="explore")
        if _act:
            _req = set(_act.get("required_operators") or [])
            _need = (_act.get("per_batch_min_operators") or 2)
            _pat = re.compile(r"([a-zA-Z_][a-zA-Z0-9_]*)\s*\(")

            def _op_hits(cands):
                return sum(1 for e in cands if _req & {t for t in _pat.findall(e)})

            _hits = _op_hits(picked)
            if _req and _hits < _need:
                _ft = _act.get("factor_templates") or {}
                _added, _used_ops = [], set()
                # 2026-09-09：区分自愈失败的三种原因，不再一律归因“无 catalog/角色池空”。
                # 旧契约（模板无 skeleton）根本无法走骨架路径，归因错误会把人引向
                # 查 catalog，而真正该做的是重签契约。
                _n_sk_tpl = sum(1 for _v in _ft.values()
                                if isinstance(_v, dict) and _v.get("skeleton") and _v.get("template"))
                _pool_empty = False
                # 自愈产出的因子同样需过 VECTOR 包裹（与上方契约注入路径同因）。
                _wrap2 = _load_vector_wrap(a.campaign_dir)
                _vf2 = _vector_field_ids(ctx, a.dataset) if _wrap2 else []
                _dtype2 = _dataset_data_type(ctx, a.dataset)
                for _op, _v in _ft.items():
                    if not (isinstance(_v, dict) and _v.get("skeleton") and _v.get("template")):
                        continue
                    _op = _v.get("op") or _op
                    if _op not in _req or _op in _used_ops:
                        continue
                    try:
                        from _lib import operator_coverage as _oc
                        _rp, _hvp, _af = _oc.dataset_role_pool(ctx, a.dataset)
                        if not _af:
                            _pool_empty = True
                            break
                        _e, _f, _m = _oc.instantiate_factor(
                            _op, _rp, window=20,
                            semantics={_op: {"template": _v.get("template"),
                                            "meaning": _v.get("meaning") or "",
                                            "category": _v.get("category")}})
                        if _e and _e not in picked and _e not in _added:
                            if _wrap2 and _vf2:
                                _e, _ = _wrap2(_e, _vf2)
                            # 类型不兼容的自愈产物同样丢弃（与契约注入路径同因）
                            _kept2, _drop2 = _drop_type_mismatched([_e], _dtype2)
                            if not _kept2:
                                continue
                            # 避开历史去重：命中历史哈希则换窗口重试一次
                            if norm_expr(_e) in {norm_expr(x) for x in picked + _added}:
                                continue
                            _added.append(_e)
                            _used_ops.add(_op)
                            if _hits + len(_added) >= _need:
                                break
                    except Exception:
                        continue
                if _added:
                    picked = _added + picked
                    sk_dist = collections.Counter(skeleton(e) for e in picked)
                    cov_injected += len(_added)
                    print(f"[diversity-heal] 自愈补齐 {len(_added)} 条 "
                          f"(命中 {_hits}->{_hits + len(_added)}/{_need}，ops={sorted(_used_ops)})")
                elif _n_sk_tpl == 0:
                    print(f"[diversity-heal] warn: 命中 {_hits}/{_need} 且无法自愈——"
                          f"活跃契约 {_act.get('_rule_id')} 的 {len(_ft)} 个模板全部无 skeleton"
                          f"（旧格式契约），骨架实例化路径不可用。"
                          f"解锁：用 --auto-coverage always 重签契约；否则闸6 每波必然 FAIL。")
                elif _pool_empty:
                    print(f"[diversity-heal] warn: 命中 {_hits}/{_need} 且骨架补齐失败"
                          f"（dataset={a.dataset} 无 catalog/角色池空），波将依赖 gate 闸6 裁决")
                else:
                    print(f"[diversity-heal] warn: 命中 {_hits}/{_need} 且骨架实例化未产出新表达式"
                          f"（模板 {len(_ft)} 个/带 skeleton {_n_sk_tpl} 个），波将依赖 gate 闸6 裁决")
    except Exception as _he:
        print(f"[diversity-heal] 跳过：{_he}")

    # 波指纹：绑定到当前 GEM priors 文件 sha256（KB 状态可回溯；缺失记 None）
    try:
        _psha = _priors_sha(ctx) if _priors_sha else None
    except Exception:
        _psha = None

    meta = {
        "wave": a.wave, "source": a.file or "db", "region": ctx.region,
        "created_at": datetime.datetime.now().isoformat(timespec="seconds"),
        "priors_sha": _psha,
        "input": len(exprs), "duplicates_dropped": n_dup, "selected": len(picked),
        "coverage_injected": cov_injected,
        "coverage_signed": cov_signed,
        "buckets": bucket_sizes,
        "skeleton_distribution": dict(sk_dist),
        "family_tagged": sum(1 for e in picked if norm_expr(e) in family_map),
        "family_distribution": dict(fam_dist),
        "linear_mix_cap": lm_cap,
        "diversity_enhanced": bool(diversity_report and diversity_report.get("enhanced")),
    }
    st = get_store(ctx)
    try:
        st.upsert_expressions(
            ctx.region, str(a.wave),
            [{"expression": e, "status": "selected", "dataset": a.dataset} for e in picked],
            dataset=a.dataset, status="selected",
        )
        if diversity_report:
            st.upsert_ledger(ctx.region, f"diversity_report_w{a.wave}", diversity_report)
        st.upsert_ledger(ctx.region, f"wave_meta_{a.wave}", meta)
    finally:
        st.close()
    print(json.dumps(meta, ensure_ascii=False, indent=1))
    print(f"wave -> db expressions/{ctx.region}/{a.wave} n={len(picked)}")


if __name__ == "__main__":
    main()
