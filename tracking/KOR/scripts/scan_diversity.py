#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""scan_diversity.py —— 族驱动扫描器（防「模板单一」）

两个用途：
  1) --build <field> [--family F]  ：用 template_families.json 的骨架族，为某字段生成扫描网格
  2) --audit <batch_file>          ：审计手写批次的「族/算子多样性」，判是否过三闸

数据源（单一事实源）：
  - Claude/skills/wq-brain-campaign-toolkit/config/template_families.json          （9 族 + free_explore）
  - tracking/<REGION>/reference/<region>_generation_constraints.json               （used / unused / force_explore_ops）

用法（仓库根下执行；$WQ_PY = world-quant-brain-mcp/.venv 的解释器）：
  $WQ_PY tracking/KOR/scripts/scan_diversity.py --build pv47_for_statssimple_only_spret --family first_order_transform
  $WQ_PY tracking/KOR/scripts/scan_diversity.py --build close --all-families
  $WQ_PY tracking/KOR/scripts/scan_diversity.py --audit logs/_kor_d240.txt

背景（2026-10-14 会话实证）：手写表达式只用 1–2 个模板会系统性遗漏信号。
  insider_feats 用 SH 构型只到 S1.23；换「裸 multiply(rank(A),rank(B))」到 1.67（全闸过）。

⚠ 与 toolkit 的 `diversity_audit.py` **不是重复实现**（2026-10-15 核过，别再当重复清掉）：
  那个吃战役目录的 wave 产物、写台账并产出 `next_round_injections`（gate.py 闸 6 消费的契约）；
  本脚本吃**手写批次文本**、只往 stdout 打三闸判定，是发批前的自查，不落库。
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys

# 层数无关的仓库根（AGENTS.md §8.13）。
# 旧写法 os.path.join(dirname(__file__), "..", "..", "..", "..") 只在
# 「脚本恰好躺在 <repo>/Claude/skills/<skill>/scripts/」这一层数下成立；2026-10-15
# 迁到 tracking/KOR/scripts/ 后层数变了，硬编码会静默指到仓库外 —— 不报错，只是
# 后面 open(FAMILIES_JSON) 抛 FileNotFoundError，看不出是路径推导的锅。
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _repo_path import REPO as _REPO_PATH  # noqa: E402

REPO = str(_REPO_PATH)
FAMILIES_JSON = os.path.join(
    REPO, "Claude", "skills", "wq-brain-campaign-toolkit", "config", "template_families.json"
)

# 审计用的「族 → 特征算子（须全部命中才算）」映射；空列表 = 无法由算子判定
FAMILY_SIGNATURE = {
    "event_conviction_ratio": ["tail", "divide"],
    "event_gated_signal": ["trade_when"],
    "continuous_spread_pair": [],  # subtract(rank,rank) 太通用，无法由算子判定
    "ceiling_suppress": ["winsorize"],
    "discrete_score_bucket": ["bucket"],
    "low_freq_backfill": ["ts_backfill"],
    "analyst_revision_breadth": ["ts_delta", "vec_avg", "group_rank"],
    "target_price_premium": ["divide", "vec_avg", "group_rank"],
    "first_order_transform": ["ts_regression"],
    "free_explore": [],
}
# first_order_transform 的其它特征算子（命中任一即算）
FOT_ALT_OPS = ["ts_decay_linear", "signed_power", "reverse", "ts_step"]

FORCE_EXPLORE_FALLBACK = [
    "trade_when", "bucket", "winsorize", "ts_ir", "ts_corr", "ts_product", "if_else", "ts_arg_max",
]

OP_RE = re.compile(r"\b([a-z][a-z0-9_]*)\s*\(")


def _load_families() -> dict:
    with open(FAMILIES_JSON, encoding="utf-8") as f:
        return json.load(f)


def _constraints_path(region: str) -> str:
    return os.path.join(REPO, "tracking", region, "reference", f"{region.lower()}_generation_constraints.json")


def _load_constraints(region: str) -> dict:
    p = _constraints_path(region)
    if not os.path.isfile(p):
        return {}
    with open(p, encoding="utf-8") as f:
        return json.load(f)


def _ops_in(expr: str) -> set:
    return set(OP_RE.findall(expr))


def build(region: str, field: str, families: list, all_families: bool, grid: bool) -> None:
    fams = _load_families()
    wanted = None
    if all_families:
        wanted = [f["family_id"] for f in fams["families"]] + [fams["free_explore_family"]["family_id"]]
    elif families:
        wanted = families

    print(f"# 族驱动扫描网格 — region={region} field={field}")
    print(f"# 源: {os.path.relpath(FAMILIES_JSON, REPO)}\n")
    out = []
    for f in fams["families"]:
        fid = f["family_id"]
        if wanted and fid not in wanted:
            continue
        print(f"=== {fid} ===")
        print(f"  机制: {f.get('mechanism','')[:90]}")
        sk = f.get("skeleton")
        if sk:
            expr = sk.replace("{field}", field)
            # 通用占位符给出保守默认
            for ph in re.findall(r"\{([a-z_]+)\}", expr):
                expr = expr.replace("{%s}" % ph, _default_for(ph))
            print(f"  骨架: {sk}")
            print(f"  实例: {expr}")
            out.append(expr)
        for v in f.get("skeleton_variants", []) or []:
            e = v.get("expr", "").replace("{field}", field)
            for ph in re.findall(r"\{([a-z_]+)\}", e):
                e = e.replace("{%s}" % ph, _default_for(ph))
            print(f"  [{v.get('name'):<16}] {e}")
            out.append(e)
        print()
    if grid:
        print("--- 可直接发批（复制到 batch 文件）---")
        for e in out:
            print(e)


def _default_for(ph: str) -> str:
    d = {
        "flow_field": "vec_sum(FIELD_A)", "stock_field": "vec_sum(FIELD_B)",
        "eps": "0.0001", "group": "industry", "event_window": "66", "win_std": "2", "q": "0.25",
        "low_freq_field": "FIELD", "backfill_window": "252", "window": "22", "window_fast": "22",
        "window_slow": "252", "cnt_field": "vec_sum(FIELD)", "target_field": "vec_avg(FIELD)",
        "event_cond": "ts_count_nans(FIELD, 22) < 5", "signal_expr": "FIELD", "neutral_val": "-1",
        "spread_a": "FIELD_A", "spread_b": "FIELD_B", "ceiling_field": "FIELD", "int_field": "FIELD",
        "transform": "ts_delta", "field": "FIELD",
    }
    return d.get(ph, "FIELD")


def audit(batch_file: str, region: str) -> int:
    with open(batch_file, encoding="utf-8") as f:
        exprs = [l.strip() for l in f if l.strip() and not l.strip().startswith("#")]

    used_ops: set = set()
    per_expr_ops = []
    for e in exprs:
        ops = _ops_in(e)
        used_ops |= ops
        per_expr_ops.append(ops)

    # 族判定（AND 语义：sig 须全部命中；first_order_transform 额外认 FOT_ALT_OPS）
    fam_hits = {}
    for fid, sigs in FAMILY_SIGNATURE.items():
        if not sigs:
            continue
        n = 0
        for e in exprs:
            ops = _ops_in(e)
            if all(s in ops for s in sigs):
                n += 1
            elif fid == "first_order_transform" and any(a in ops for a in FOT_ALT_OPS):
                n += 1
        if n:
            fam_hits[fid] = n

    cons = _load_constraints(region)
    known_used = set((cons.get("operator_stats", {}) or {}).get("used", {}).keys())
    declared_unused = set((cons.get("operator_stats", {}) or {}).get("unused", []) or [])
    force_ops = (cons.get("injection_rules", {}) or {}).get("force_explore_ops", FORCE_EXPLORE_FALLBACK)

    introduced = sorted(op for op in used_ops if known_used and op not in known_used)
    force_hit = sorted(op for op in used_ops if op in set(force_ops))

    print(f"# 批次多样性审计 — {batch_file}")
    print(f"表达式 {len(exprs)} 条 | 命中族 {len(fam_hits)} 个 | 算子 {len(used_ops)} 种\n")
    print("族命中：")
    for fid, n in sorted(fam_hits.items(), key=lambda x: -x[1]):
        print(f"  {fid:<28} {n} 条")
    if not fam_hits:
        print("  (无)")
    print("\n本批算子：", ", ".join(sorted(used_ops)))
    print("未用算子（本批引入）:", ", ".join(introduced) if introduced else "(无)")
    print("force_explore 命中:", ", ".join(force_hit) if force_hit else "(无)")

    c1 = len(fam_hits) >= 2
    c2 = len(force_hit) >= 1 or len(introduced) >= 2
    # 合规上限按「单条表达式算子调用数」计（不是批次去重算子数）
    max_per_expr = max((len(o) for o in per_expr_ops), default=0)
    c3 = max_per_expr < 10
    print("\n=== 三闸 ===")
    print(f"  [{'PASS' if c1 else 'FAIL'}] 族数 ≥2（当前 {len(fam_hits)}）")
    print(f"  [{'PASS' if c2 else 'FAIL'}] 未用/force 算子 ≥2（引入 {len(introduced)}，force 命中 {len(force_hit)}）")
    print(f"  [{'PASS' if c3 else 'FAIL'}] 单条表达式算子数 <10（本批最大 {max_per_expr}）")
    ok = c1 and c2 and c3
    print(f"\n结论: {'✅ 通过' if ok else '❌ 未过 —— 重写批次（增族/增未用算子）'}")
    return 0 if ok else 1


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--build", metavar="FIELD", help="为某字段生成族骨架网格")
    ap.add_argument("--family", action="append", default=[], help="只生成指定族（可重复）")
    ap.add_argument("--all-families", action="store_true")
    ap.add_argument("--grid", action="store_true", help="额外打印可复制粘贴的表达式列表")
    ap.add_argument("--audit", metavar="BATCH_FILE", help="审计批次文件的族/算子多样性")
    ap.add_argument("--region", default="KOR")
    a = ap.parse_args()
    if a.audit:
        return audit(a.audit, a.region)
    if a.build:
        build(a.region, a.build, a.family, a.all_families, a.grid)
        return 0
    ap.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())
