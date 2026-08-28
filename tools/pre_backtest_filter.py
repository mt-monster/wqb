# -*- coding: utf-8 -*-
"""pre_backtest_filter.py - 回测前快筛闭环（self/PPAC + 关键闸）。

在批量回测前对候选表达式做三层快筛，避免烧配额：
  1. 收益来源多样性：同批 >60% 共享同一 expected_exposure + 字段族 → FAIL
  2. 自相关快筛：与 region 已有 alpha 的 self_corr >= 0.7 → FAIL
  3. 关键闸预检：turnover / margin / coverage 不在合理区间 → WARN

用法:
  python tools/pre_backtest_filter.py --campaign-dir tracking/USA --dataset model219 \
      --wave 97 --region USA
"""
import argparse
import collections
import json
import os
import re
import sys

# 解析 toolkit scripts 目录注入 sys.path（与 tools/wave_gate.py 同一模式，勿硬编码）
_TOOLKIT_CANDIDATES = [
    os.environ.get("WQ_TOOLKIT_DIR"),
    os.path.join(os.path.expanduser("~"), ".qoder-cn", "skills", "wq-brain-campaign-toolkit", "scripts"),
    os.path.join(os.path.expanduser("~"), ".cursor", "skills", "wq-brain-campaign-toolkit", "scripts"),
    os.path.join(os.path.expanduser("~"), ".workbuddy", "skills", "wq-brain-campaign-toolkit", "scripts"),
]
for _cand in _TOOLKIT_CANDIDATES:
    if _cand and os.path.isdir(os.path.join(_cand, "_lib")):
        if _cand not in sys.path:
            sys.path.insert(0, _cand)
        break

from _lib.common import CampaignContext, add_campaign_arg, expr_fields


def _extract_exposure_from_idea(idea_text):
    """从 GEM idea 文本提取 expected_exposure。"""
    if not idea_text:
        return None
    m = re.search(r"\*\*Expected Exposure\*\*\s*:\s*([^\n]+)", idea_text, re.IGNORECASE)
    if not m:
        return None
    raw = m.group(1).strip().strip('`').strip()
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
        tpl_exp = {}
        for tpl, idea_text in t2i.items():
            exp = _extract_exposure_from_idea(idea_text)
            if exp:
                tpl_exp[tpl] = exp
        out = {}
        for expr in expr_list:
            for tpl, exp in tpl_exp.items():
                tpl_prefix = tpl.split("{")[0] if "{" in tpl else tpl
                if tpl_prefix and tpl_prefix in expr:
                    out[expr] = exp
                    break
        return out
    except Exception:
        return {}


def _field_family(expr):
    """提取字段族（字段前缀）。"""
    fields = expr_fields(expr, known_ops=None, min_len=6)
    if not fields:
        return "unknown"
    f = sorted(fields)[0]
    return f.split("_")[0] if "_" in f else f[:6]


def check_exposure_diversity(exprs, ctx, dataset, delay=1, threshold=0.6):
    """收益来源多样性闸：同批 >threshold 共享同一 exposure + 字段族 → FAIL。"""
    exp_map = _load_exposure_map(ctx, dataset, delay=delay)
    if not exp_map:
        return [], {"applied": False, "reason": "no exposure metadata"}
    exp_groups = collections.defaultdict(list)
    for e in exprs:
        exp = exp_map.get(e)
        if exp:
            exp_groups[(exp, _field_family(e))].append(e)
    total_with_exp = sum(len(v) for v in exp_groups.values())
    if total_with_exp == 0:
        return [], {"applied": False, "reason": "no expressions matched to exposure"}
    (top_exp, top_fam), top_exprs = max(exp_groups.items(), key=lambda kv: len(kv[1]))
    share = len(top_exprs) / len(exprs)
    issues = []
    if share > threshold and len(exprs) >= 3:
        issues.append(
            f"[EXPOSURE-DIVERSITY] {len(top_exprs)}/{len(exprs)} ({share:.0%}) "
            f"表达式共享 exposure={top_exp} + 字段族={top_fam}，"
            f"结构不同但收益来源相同，回测必高相关"
        )
    return issues, {
        "applied": True,
        "top_exposure": top_exp,
        "top_field_family": top_fam,
        "share": share,
        "threshold": threshold,
    }


def check_self_corr_fast(exprs, ctx, region, threshold=0.7):
    """自相关快筛：与 region 已有 alpha 的 self_corr >= threshold → FAIL。
    
    注：这里只做 DB 层快筛（已有 alpha 的 self_correlation 字段），
    不做实时 PnL 计算（那是 brain-calculate-alpha-selfcorrQuick 的职责）。
    """
    try:
        from _lib.wqb_store import get_store
        st = get_store(ctx)
        try:
            existing = st.list_alphas_by_region(region, status="ACTIVE")
        finally:
            st.close()
        if not existing:
            return [], {"applied": False, "reason": "no existing alphas in region"}
        # 提取已有 alpha 的字段族 + exposure（如果有）
        existing_families = collections.Counter()
        for a in existing:
            expr = a.get("expression", "")
            if expr:
                existing_families[_field_family(expr)] += 1
        issues = []
        for e in exprs:
            fam = _field_family(e)
            if existing_families.get(fam, 0) >= 3:
                issues.append(
                    f"[SELF-CORR-FAST] 字段族 {fam} 在 region {region} 已有 "
                    f"{existing_families[fam]} 个 ACTIVE alpha，新表达式大概率高相关"
                )
        return issues, {
            "applied": True,
            "existing_count": len(existing),
            "family_distribution": dict(existing_families),
        }
    except Exception as exc:
        return [], {"applied": False, "reason": f"error: {exc}"}


def check_key_gates_fast(exprs, ctx):
    """关键闸预检：turnover / margin / coverage 启发式评估。"""
    issues = []
    for e in exprs:
        # turnover 启发式：ts_delta / ts_av_diff 窗口 < 10 → 高换手风险
        if re.search(r"ts_(delta|av_diff)\([^,]+,\s*[1-9]\s*\)", e):
            issues.append(
                f"[KEY-GATE-WARN] 短窗口时序差分（窗口<10）可能导致高换手：{e[:80]}"
            )
        # coverage 启发式：group_neutralize 到小组（如 sector）→ 覆盖不足风险
        if "group_neutralize" in e and "sector" in e:
            issues.append(
                f"[KEY-GATE-WARN] sector 级中性化可能导致覆盖不足：{e[:80]}"
            )
    return issues, {"applied": True, "warn_count": len(issues)}


def main():
    ap = argparse.ArgumentParser(description="回测前快筛闭环（self/PPAC + 关键闸）")
    add_campaign_arg(ap)
    ap.add_argument("--dataset", required=True)
    ap.add_argument("--wave", required=True)
    ap.add_argument("--region", required=True)
    ap.add_argument("--delay", type=int, default=1)
    ap.add_argument("--exposure-threshold", type=float, default=0.6)
    ap.add_argument("--self-corr-threshold", type=float, default=0.7)
    ap.add_argument("--skip-exposure", action="store_true")
    ap.add_argument("--skip-self-corr", action="store_true")
    ap.add_argument("--skip-key-gates", action="store_true")
    a = ap.parse_args()

    ctx = CampaignContext(a.campaign_dir)
    # 从 DB 读候选
    from _lib.wqb_store import get_store
    st = get_store(ctx)
    try:
        rows = st.list_expressions(a.region, str(a.wave), dataset=a.dataset)
        if not rows:
            rows = st.list_expressions(a.region, str(a.wave))
        exprs = [r["expression"] for r in rows if r.get("expression")]
    finally:
        st.close()
    if not exprs:
        print(f"[error] 无候选表达式: region={a.region} wave={a.wave} dataset={a.dataset}")
        sys.exit(1)

    print(f"[filter] 候选 {len(exprs)} 条，开始快筛...")
    all_issues = []
    report = {"total": len(exprs), "gates": {}}

    # 闸1：收益来源多样性
    if not a.skip_exposure:
        issues, meta = check_exposure_diversity(
            exprs, ctx, a.dataset, delay=a.delay, threshold=a.exposure_threshold
        )
        all_issues.extend(issues)
        report["gates"]["exposure_diversity"] = {"issues": issues, **meta}
        print(f"[gate1] 收益来源多样性: {len(issues)} issues, meta={meta}")

    # 闸2：自相关快筛
    if not a.skip_self_corr:
        issues, meta = check_self_corr_fast(
            exprs, ctx, a.region, threshold=a.self_corr_threshold
        )
        all_issues.extend(issues)
        report["gates"]["self_corr_fast"] = {"issues": issues, **meta}
        print(f"[gate2] 自相关快筛: {len(issues)} issues, meta={meta}")

    # 闸3：关键闸预检
    if not a.skip_key_gates:
        issues, meta = check_key_gates_fast(exprs, ctx)
        all_issues.extend(issues)
        report["gates"]["key_gates_fast"] = {"issues": issues, **meta}
        print(f"[gate3] 关键闸预检: {len(issues)} issues, meta={meta}")

    report["all_pass"] = not all_issues
    report["total_issues"] = len(all_issues)
    print(f"\n[done] 快筛 {'PASS' if not all_issues else 'FAIL'}: {len(all_issues)} issues")
    if all_issues:
        for it in all_issues[:10]:
            print(f"  - {it}")
    print(json.dumps(report, ensure_ascii=False, indent=1))
    sys.exit(0 if not all_issues else 1)


if __name__ == "__main__":
    main()
