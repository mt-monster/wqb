# -*- coding: utf-8 -*-
"""diversity_audit.py - 多样性审计累积进台账。

每次运行把算子/字段/骨架分布追加进台账 diversity_history（累积可看趋势），
并更新 diversity_audit_latest。骨架五分类与 KNOWN_OPS 来自 toolkit
config/platform_constraints.json（单一事实源，可用平台 get_operators 刷新后回写）。

B 方案闭环（评估→执行强制）：
  - next_round_injections：机器可读注入契约（下 10 轮强制探索的算子族 + 骨架配额），
    由 gate.py 闸6 在提交前强制拦截不达标批次；repair 批豁免，过期自动失效。
  - injection_landing：对上一条契约的落地对账（哪些算子/骨架用了、哪些没落地）。
  批次构建端参考 diversity_slots.py 打印契约照做。

用法:
  python diversity_audit.py --campaign-dir <DIR>              # 扫描全部 wave 文件 + 写台账
  python diversity_audit.py --campaign-dir <DIR> --no-ledger  # 只打印
"""
import argparse
import collections
import datetime
import glob
import json
import os
import re
import sys

# 注入优先级：多样性评估后强制要求下 10 轮探索的算子族（按价值排序；不在
# known_ops 中的会被 audit 自动跳过）。
INJECTION_PRIORITY = [
    "ts_rank", "ts_scale", "ts_zscore", "ts_corr", "ts_kurtosis", "ts_skewness",
    "bucket", "trade_when", "if_else", "group_rank", "group_zscore",
    "ts_arg_max", "ts_arg_min", "ts_moment", "hump", "step",
    # 增强流水线 v2：非线性变换族（known_ops 确认在册；ts_kurtosis 等未在册的自动被排除）
    "signed_power", "log", "sqrt", "power", "winsorize", "ts_std_dev", "ts_ir",
    "ts_av_diff", "ts_decay_linear", "ts_delta", "ts_mean", "ts_sum",
    "normalize", "pasteurize", "group_neutralize", "group_mean", "divide", "delta",
]
# 骨架占比低于该阈值时强制每批配额（B 方案：直击 single 占比 80% 的同质化）
SKELETON_UNDERREP_RATIO = 0.15
MAX_REQUIRED_OPERATORS = 4
INJECTION_EXPIRY_BATCHES = 10
INJECTION_EXEMPT = ["repair"]

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _lib.common import (CampaignContext, add_campaign_arg, load_json,
                         load_platform_constraints, read_exprs_file, skeleton)
from _lib.ledger import LedgerStore, make_ledger_store
from _lib import rules as rules_mod


def audit(ctx, known_ops, pattern=None, prev_injections=None):
    """扫描并统计多样性。

    pattern: 可选 glob 覆盖（默认 {prefix}_wave*_exprs.json + candidates/*.json）。
    prev_injections: 上一条注入契约（台账里读），用于计算注入落地率对账。
    2026-08-18 GBR 复盘：战役 wave 命名不统一（wave09_expressions.json / probe_*.json /
    stageA_exprs.json 等），默认 glob 会把探针表达式混入正式 wave 统计、且不同批次
    扫描集合漂移导致 diversity_history 不可比。修复：报告显式列出 scanned_files，
    并按文件名分类计数（wave/probe/other），供口径核对。
    """
    ops, fields, skel = collections.Counter(), collections.Counter(), collections.Counter()
    total, uniq = 0, set()
    if pattern:
        files = sorted(glob.glob(ctx.path(pattern)))
    else:
        files = sorted(glob.glob(ctx.path(f"{ctx.prefix}_wave*_exprs.json")) +
                       glob.glob(ctx.path("candidates", "*.json")))
    for f in files:
        try:
            exprs = read_exprs_file(f)
        except Exception:
            continue
        for e in exprs:
            total += 1
            uniq.add(re.sub(r"\s+", "", e))
            skel[skeleton(e)] += 1
            for tok in re.findall(r"[a-zA-Z_][a-zA-Z0-9_]*\(", e):
                ops[tok[:-1]] += 1
            for t in set(re.findall(r"[a-zA-Z_][a-zA-Z0-9_]*", e)):
                if len(t) > 6 and t not in known_ops:
                    fields[t] += 1
    used = {op for op in known_ops if ops.get(op, 0) > 0}
    # 扫描文件分类计数（口径核对）：wave=正式波次 / probe=探针 / other=其他
    src_counts = collections.Counter()
    for f in files:
        base = os.path.basename(f).lower()
        if "probe" in base or "stagea" in base or "repair" in base:
            src_counts["probe"] += 1
        elif "wave" in base:
            src_counts["wave"] += 1
        else:
            src_counts["other"] += 1
    # ---- 下 10 轮强制注入契约（B 方案①：结构化契约，gate 闸6 强制） ----
    unused_priority = [op for op in INJECTION_PRIORITY if op in known_ops and op not in used]
    skel_quota = {}
    if total:
        for name in ("ratio", "event_gated", "group"):
            if skel.get(name, 0) / total < SKELETON_UNDERREP_RATIO:
                skel_quota[name] = 1
    next_injections = None
    if unused_priority or skel_quota:
        next_injections = {
            "issued_at": datetime.datetime.now().isoformat(timespec="seconds"),
            "expires_after_batches": INJECTION_EXPIRY_BATCHES,
            "per_batch_min_operators": 2,
            "required_operators": unused_priority[:MAX_REQUIRED_OPERATORS],
            "skeleton_quota": skel_quota,
            "exempt": list(INJECTION_EXEMPT),
            "consumed_batches": [],
        }
    # ---- 注入落地率（B 方案④：对上一契约逐项对账） ----
    injection_landing = None
    if prev_injections:
        per_op = {op: {"used": ops.get(op, 0), "landed": ops.get(op, 0) > 0}
                  for op in prev_injections.get("required_operators", [])}
        landed_ops = [op for op, v in per_op.items() if v["landed"]]
        missed_ops = [op for op, v in per_op.items() if not v["landed"]]
        per_skel = {s: {"used": skel.get(s, 0), "landed": skel.get(s, 0) >= q}
                    for s, q in (prev_injections.get("skeleton_quota") or {}).items()}
        parts = []
        if per_op:
            parts.append(f"算子落地 {len(landed_ops)}/{len(per_op)}"
                         + (f"，未落地: {missed_ops}" if missed_ops else ""))
        if per_skel:
            parts.append(f"骨架落地 {sum(1 for v in per_skel.values() if v['landed'])}/{len(per_skel)}")
        injection_landing = {
            "checked_against": prev_injections.get("issued_at"),
            "consumed_batches": len(prev_injections.get("consumed_batches", [])),
            "per_operator": per_op,
            "per_skeleton": per_skel,
            "summary": "；".join(parts) if parts else "无强制项",
        }
    return {
        "audited_at": datetime.datetime.now().isoformat(timespec="seconds"),
        "region": ctx.region,
        "wave_files": len(files), "total_exprs": total, "unique_exprs": len(uniq),
        "duplicate_exprs": total - len(uniq),
        "operator_exploration_rate": round(len(used) / len(known_ops), 3),
        "operators_used": len(used), "operators_known": len(known_ops),
        "operators_unused": [op for op in known_ops if op not in used],
        "operator_freq_top": dict(ops.most_common(12)),
        "skeleton_distribution": dict(skel),
        "field_count": len(fields),
        "field_freq_top": dict(fields.most_common(12)),
        "scanned_files": [os.path.basename(f) for f in files],
        "source_distribution": dict(src_counts),
        "next_round_injections": next_injections,
        "injection_landing": injection_landing,
        # 内部字段：供 main() 签发规则契约 + 落地率对账（融合自学习规则引擎）
        "_ops": ops, "_skel": skel,
    }


def main():
    ap = argparse.ArgumentParser(description="多样性审计（latest+history 双写台账）")
    add_campaign_arg(ap)
    ap.add_argument("--no-ledger", action="store_true")
    ap.add_argument("--pattern", default=None,
                    help="可选：glob 覆盖扫描范围（默认 {prefix}_wave*_exprs.json + candidates/*.json）")
    a = ap.parse_args()
    ctx = CampaignContext(a.campaign_dir)
    known_ops = load_platform_constraints()["known_ops"]
    prev_injections = None
    # 只读台账取上一契约（--no-ledger 干跑也显示落地对账，仅不写回）
    state = make_ledger_store(ctx).load()
    if state:
        prev_injections = (state.get("diversity_audit_latest") or {}).get("next_round_injections")
    r = audit(ctx, known_ops, pattern=a.pattern, prev_injections=prev_injections)

    # ---- 融合自学习规则引擎：契约签发 + 落地率对账（区域规则库） ----
    # --no-ledger 干跑时不写规则库（与台账写一致，保持 dry-run 语义）
    ops_counter = r.pop("_ops", None)
    skel_counter = r.pop("_skel", None)
    contract_rid = None
    landing = r.get("injection_landing")  # 台账路径对账（兼容）
    if not a.no_ledger:
        try:
            # 落地率对账：对上一活跃/近期契约逐项对账 + 调置信度（L4）
            if ops_counter is not None:
                rule_landing = rules_mod.reconcile_contract_landing(
                    ctx, ctx.region, ops_counter, skel_counter)
                if rule_landing:
                    landing = rule_landing  # 规则引擎对账优先（含 confidence 调整）
                    r["injection_landing"] = rule_landing
            # 签发新契约（有强制项时）：写 explore_contract 规则（区域库）
            inj = r.get("next_round_injections")
            if inj and (inj.get("required_operators") or inj.get("skeleton_quota")):
                contract_rid = rules_mod.issue_contract(
                    ctx,
                    required_operators=inj.get("required_operators", []),
                    skeleton_quota=inj.get("skeleton_quota", {}),
                    region=ctx.region,
                    per_batch_min_operators=inj.get("per_batch_min_operators", 2),
                    expires_after_batches=inj.get("expires_after_batches", 10),
                    exempt=inj.get("exempt", ["repair"]),
                    evidence={"exploration_rate": r.get("operator_exploration_rate"),
                              "total_exprs": r.get("total_exprs")})
                r["explore_contract_rule_id"] = contract_rid
        except Exception as e:
            print(f"[rules] 契约签发/对账异常（不阻断，台账路径仍有效）: {e}", file=sys.stderr)

    print(json.dumps(r, ensure_ascii=False, indent=1))
    if not a.no_ledger:
        store = make_ledger_store(ctx)

        def mut(d):
            d["diversity_audit_latest"] = r
            hist = d.setdefault("diversity_history", [])
            hist.append({"at": r["audited_at"], "total": r["total_exprs"],
                         "unique": r["unique_exprs"],
                         "exploration_rate": r["operator_exploration_rate"],
                         "skeleton": r["skeleton_distribution"],
                         "injections": r.get("next_round_injections"),
                         "landing": r.get("injection_landing")})
        store.update(mut)
        print("ledger: diversity_audit_latest + diversity_history updated", file=sys.stderr)


if __name__ == "__main__":
    main()
