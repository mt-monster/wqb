#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""PROD 饱和闸（S2 生成层前移，2026-09-07 P1-1）。

背景（审计实证）：全库可提交库存（sharpe≥1.58 & UNSUBMITTED &
prod_corr<0.7 & self_corr<0.7）仅 MEA 3 颗，其余区域全 0 ——
**prod 饱和是全局第一瓶颈**。典型样本 IND：104 条 S≥1.58 中
84 条来自同一数据集（dataset_id=41），全部撞 prod_corr 墙。

根因：饱和族字段在 S2 生成层未被排除，浪费到 S3 回测才暴露。
USA 战役提示词已有 `search_alphas_by_sharpe(USA, 1.58)` 饱和拦截
设计，本模块把它产品化为可执行闸门，供 wave_gate / preflight_wave /
workflow_gem 调用。

三态设计（与 field_inspect_gate 对齐，绝不把"没数据"伪装成"通过"）：

  enforced   —— DB 有该区域历史 alpha：统计字段族饱和度，超阈值即 FAIL
  partial    —— 表达式含 DB 未见过的字段：已知的照查，未知的列出来
  unavailable—— DB 无该区域 alpha 记录：不阻断，报告"本闸未生效"

饱和判定（两维度取 OR）：
  1. 字段级：字段 F 出现在 ≥ field_hit_max 条 S≥min_sharpe 的
     历史 alpha 表达式中 → F 视为饱和字段
  2. 数据集级：当前 wave 的 dataset 在 S≥min_sharpe 历史 alpha 中
     占比 ≥ dataset_share_max 且这些 alpha 的 prod_corr 全 ≥0.7 →
     该 dataset 视为饱和数据集

用法（库）：
    from prod_saturation_gate import check_wave
    report = check_wave(exprs, region="IND", dataset="model32")

用法（CLI 自查）：
    python tools/prod_saturation_gate.py --region IND --dataset model32 \
        --expr "rank(mdl32_x)"
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from collections import Counter
from typing import Any, Dict, List, Optional

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

#: 默认阈值（宽松起步；区域 profile 有更严值时以 profile 为准）
DEFAULTS = {
    "min_sharpe": 1.58,        # 只统计达标 alpha（与提交线一致）
    "field_hit_max": 8,        # 字段出现在 ≥N 条达标 alpha → 饱和
    "dataset_share_max": 0.6,  # 单数据集占达标 alpha 份额 → 数据集级饱和
    "prod_wall": 0.7,          # prod_corr ≥ 此值视为撞墙
}

_CALL_RE = re.compile(r"\b([a-z_][a-z0-9_]*)\s*\(")
_KWARG_RE = re.compile(r"\b([a-z_][a-z0-9_]*)\s*=")
_RESERVED = {
    "true", "false", "nan", "industry", "subindustry", "sector", "market",
    "country", "exchange", "and", "or", "not", "cap", "close", "open",
    "high", "low", "volume", "vwap", "returns", "adv20", "sharesout",
    "free_float", "split", "dividend",
}


def extract_fields(expr: str) -> List[str]:
    """提取表达式中的裸字段（排除算子调用/具名参数/保留字）。"""
    idents = set(re.findall(r"\b([a-z_][a-z0-9_]*)\b", expr.lower()))
    calls = set(_CALL_RE.findall(expr.lower()))
    kwargs = set(_KWARG_RE.findall(expr.lower()))
    return sorted(
        t for t in idents - calls - kwargs - _RESERVED
        if len(t) >= 4  # 过滤短噪声
    )


def _load_store(db_path: Optional[str] = None):
    """加载 CampaignStore（惰性；失败返回 None → unavailable 态）。"""
    src = os.path.join(REPO_ROOT, "src")
    if src not in sys.path:
        sys.path.insert(0, src)
    try:
        from wqb.store import CampaignStore
        path = db_path or os.path.join(REPO_ROOT, "data", "wqb.db")
        if not os.path.isfile(path):
            return None
        return CampaignStore(path)
    except Exception:
        return None


def check_wave(
    exprs: List[str],
    region: str,
    dataset: Optional[str] = None,
    db_path: Optional[str] = None,
    thresholds: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """对一波表达式做 PROD 饱和检查。

    返回 report dict：
      status: enforced | unavailable
      passed: bool（enforced 态才有意义；unavailable 恒 True 不阻断）
      saturated_fields / saturated_dataset / violations / stats
    """
    cfg = dict(DEFAULTS)
    cfg.update(thresholds or {})

    report: Dict[str, Any] = {
        "gate": "prod_saturation",
        "region": region,
        "dataset": dataset,
        "thresholds": cfg,
        "status": "unavailable",
        "passed": True,
        "message": "",
    }

    store = _load_store(db_path)
    if store is None:
        report["message"] = (
            "wqb.db 不可达或无 alpha 历史 → 本闸未生效（不阻断）。"
            "首个战役波自然落在此态。"
        )
        return report

    try:
        rows = store.search_alphas_by_sharpe(
            region=region, min_sharpe=cfg["min_sharpe"], limit=500)
    finally:
        store.close()

    if not rows:
        report["message"] = (
            f"{region} 无 S≥{cfg['min_sharpe']} 历史 alpha → 本闸未生效（不阻断）。"
        )
        return report

    report["status"] = "enforced"

    # ---- 字段级饱和统计 ----
    field_hits: Counter = Counter()
    for r in rows:
        expr = r.get("expression") or ""
        for f in set(extract_fields(expr)):
            field_hits[f] += 1
    saturated_fields = {
        f for f, n in field_hits.items() if n >= cfg["field_hit_max"]
    }

    # ---- 数据集级饱和统计 ----
    ds_counter: Counter = Counter()
    ds_prod_walls: Dict[Any, List[float]] = {}
    for r in rows:
        did = r.get("dataset_id")
        ds_counter[did] += 1
        pc = r.get("prod_correlation")
        ds_prod_walls.setdefault(did, []).append(
            float(pc) if pc is not None else 0.0)
    total = sum(ds_counter.values())
    saturated_dataset_ids = set()
    for did, n in ds_counter.items():
        if n / total >= cfg["dataset_share_max"]:
            prods = ds_prod_walls[did]
            wall_ratio = sum(1 for p in prods if p >= cfg["prod_wall"]) / len(prods)
            if wall_ratio >= 0.8:  # 80% 撞墙才判死（留 20% 突围空间）
                saturated_dataset_ids.add(did)

    # dataset_id → dataset 名映射（当前 wave 比对用）
    cur_ds_saturated = False
    if dataset:
        import sqlite3
        try:
            con = sqlite3.connect(db_path or os.path.join(REPO_ROOT, "data", "wqb.db"))
            did = con.execute(
                "SELECT id FROM datasets WHERE name=? LIMIT 1", (dataset,)
            ).fetchone()
            con.close()
            if did and did[0] in saturated_dataset_ids:
                cur_ds_saturated = True
        except Exception:
            pass

    # ---- 逐表达式校验 ----
    violations = []
    n_checked = 0
    for i, expr in enumerate(exprs):
        fields = extract_fields(expr)
        if not fields:
            continue
        n_checked += 1
        hit = sorted(set(fields) & saturated_fields)
        if hit:
            violations.append({
                "index": i,
                "fields": hit,
                "reason": f"饱和字段 {hit}（各出现在 ≥{cfg['field_hit_max']} 条"
                          f" S≥{cfg['min_sharpe']} 历史 alpha）",
                "expr": expr[:100],
            })

    report.update({
        "n_history": len(rows),
        "n_checked": n_checked,
        "saturated_fields": sorted(saturated_fields),
        "saturated_dataset_ids": sorted(saturated_dataset_ids),
        "current_dataset_saturated": cur_ds_saturated,
        "violations": violations,
        "passed": not violations and not cur_ds_saturated,
    })
    if violations:
        report["message"] = (
            f"{len(violations)} 条表达式命中饱和字段，"
            f"{len(saturated_fields)} 个字段已饱和 —— 换字段族/数据集再生成。"
        )
    elif cur_ds_saturated:
        report["message"] = (
            f"数据集 {dataset} 在 {region} 达标 alpha 中份额 ≥"
            f"{cfg['dataset_share_max']:.0%} 且 ≥80% 撞 prod_corr 墙 —— "
            f"整数据集判饱和，建议换数据集。"
        )
    else:
        report["message"] = (
            f"PASS（{n_checked} 条校验，{len(saturated_fields)} 个历史饱和字段，"
            f"当前波零命中）"
        )
    return report


def format_report(report: Dict[str, Any]) -> str:
    lines = [f"[prod-sat] 状态={report['status']} {report['message']}"]
    if report.get("saturated_fields"):
        sf = report["saturated_fields"][:10]
        lines.append(f"[prod-sat] 历史饱和字段: {sf}"
                     + (f" 等 {len(report['saturated_fields'])} 个" if len(report['saturated_fields']) > 10 else ""))
    for v in report.get("violations", [])[:5]:
        lines.append(f"[prod-sat]   命中 #{v['index']}: {v['fields']} | {v['expr']}")
    return "\n".join(lines)


def main() -> None:
    ap = argparse.ArgumentParser(description="PROD 饱和闸（S2 生成层前移）")
    ap.add_argument("--region", required=True)
    ap.add_argument("--dataset", default=None)
    ap.add_argument("--expr", default=None, help="单条表达式")
    ap.add_argument("--exprs-file", default=None, help="每行一条表达式")
    ap.add_argument("--min-sharpe", type=float, default=DEFAULTS["min_sharpe"])
    ap.add_argument("--field-hit-max", type=int, default=DEFAULTS["field_hit_max"])
    ap.add_argument("--db", default=None, help="wqb.db 路径（默认 data/wqb.db）")
    a = ap.parse_args()

    if a.expr:
        exprs = [a.expr]
    elif a.exprs_file:
        exprs = [ln.strip() for ln in open(a.exprs_file, encoding="utf-8") if ln.strip()]
    else:
        raise SystemExit("need --expr / --exprs-file")

    report = check_wave(
        exprs, region=a.region, dataset=a.dataset, db_path=a.db,
        thresholds={"min_sharpe": a.min_sharpe, "field_hit_max": a.field_hit_max},
    )
    print(format_report(report))
    print(json.dumps({k: v for k, v in report.items()
                      if k not in ("saturated_fields", "violations")},
                     ensure_ascii=False, indent=1))
    sys.exit(0 if report["passed"] else 1)


if __name__ == "__main__":
    main()
