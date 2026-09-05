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


def history_hashes(ctx, exclude_path=None, exclude_waves=None):
    seen = set()
    try:
        st = get_store(ctx)
        for e in st.history_expressions(ctx.region, exclude_waves=exclude_waves):
            seen.add(norm_expr(e))
        st.close()
    except Exception:
        pass
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
            exprs = [r["expression"] for r in rows
                     if r.get("expression") and r.get("status") != "superseded"]
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
            for op, v in ft.items():
                if not (isinstance(v, dict) and v.get("op")):
                    continue
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
                if expr and expr not in cov_exprs:
                    cov_exprs.append(expr)
            if cov_exprs:
                before = set(exprs)
                new_exprs = [e for e in cov_exprs if e not in before]
                exprs = new_exprs + exprs  # 契约因子优先（头部）
                cov_injected = len(new_exprs)
                if cov_injected:
                    print(f"[coverage] 注入契约 {act.get('_rule_id')} 的 {cov_injected} 个因子 "
                          f"(骨架实例化 {skeleton_used}，legacy 回退 {skeleton_fallback}，"
                          f"required={len(act.get('required_operators', []))} 算子)")
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
                picked = [item["regular"] for item in enhanced_list]
                sk_dist = collections.Counter(skeleton(e) for e in picked)
                fam_dist = collections.Counter(
                    family_map[norm_expr(e)] for e in picked if norm_expr(e) in family_map)
                print(f"[diversity] 增强 {diversity_report.get('original_count')} -> "
                      f"{diversity_report.get('enhanced_count')} 表达式")

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
                for _op, _v in _ft.items():
                    if not (isinstance(_v, dict) and _v.get("skeleton") and _v.get("template")):
                        continue
                    if _op not in _req or _op in _used_ops:
                        continue
                    try:
                        from _lib import operator_coverage as _oc
                        _rp, _hvp, _af = _oc.dataset_role_pool(ctx, a.dataset)
                        if not _af:
                            break
                        _e, _f, _m = _oc.instantiate_factor(
                            _op, _rp, window=20,
                            semantics={_op: {"template": _v.get("template"),
                                            "meaning": _v.get("meaning") or "",
                                            "category": _v.get("category")}})
                        if _e and _e not in picked and _e not in _added:
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
                else:
                    print(f"[diversity-heal] warn: 命中 {_hits}/{_need} 且骨架补齐失败"
                          f"（无 catalog/角色池空），波将依赖 gate 闸6 裁决")
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
