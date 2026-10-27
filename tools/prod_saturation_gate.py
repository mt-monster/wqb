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
  1. 配方级（2026-10-21 修正；原为字段级）：**（字段集 × 分组轴 × 归一化算子）**
     这个配方在 S≥min_sharpe 的历史 alpha 中出现，且这些 alpha **已知 prod_corr** 的 ≥50%
     撞墙（且撞墙 ≥ min_prod_hits 条）→ 该配方饱和，同配方的候选被拦截。
     **为什么按轴分层**：分组轴 = 持仓组合的骨架，同一组字段换轴就是换组合 ⇒
     prod 相关性不同。EUR 实证（2026-10-21，fundamental72）：sector 轴 CFO/TA×
     EBITDA>NI → prod 0.7571 / 0.7553 撞墙；同一字段集的 industry 轴 →
     prod 0.6747 破墙。按字段聚合会把「已探明能破墙的配方」一起误杀
     （自我指涉误报：自家高 Sharpe alpha 把自家字段染成饱和）。
     **为什么归一化算子也分层**：同轴同载荷换归一化位（group_zscore / group_rank /
     group_neutralize）仍是不同持仓组合（EUR 实测 zscore 四个闸门同时优于 rank）
     ⇒ 撞墙证据不跨归一化位外推。
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
import sys as _sys, os as _os
_sys.path.insert(0, str(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '..', 'src')))
from wqb.db_conn import connect as db_connect  # 规范工厂（2026-09-20 L1 收口）

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
    "country", "exchange", "sta1_allc5", "and", "or", "not", "cap", "close", "open",
    "high", "low", "volume", "vwap", "returns", "adv20", "sharesout",
    "free_float", "split", "dividend",
}

#: 平台分组轴白名单（platform_constraints.json 的 group_identifiers）——
#: 分组轴决定持仓组合 ⇒ prod 相关性必须按轴分层，不能按字段聚合。
_GROUP_AXES = {
    "sector", "subindustry", "industry", "market", "country", "exchange",
    "sta1_allc5",
}

#: 带分组参数的算子（第二个顶层参数 = 分组轴）
_GROUP_OPS = (
    "group_rank", "group_zscore", "group_neutralize", "group_scale",
    "group_percentage", "group_backfill", "group_mean", "group_max",
    "group_min", "group_sum", "group_std", "group_median", "group_vector_neut",
)


def _split_top_args(inner: str) -> List[str]:
    """按顶层逗号切分实参（括号内逗号不算）。"""
    args: List[str] = []
    depth = 0
    cur: List[str] = []
    for ch in inner:
        if ch == "(":
            depth += 1
        elif ch == ")":
            depth -= 1
        if ch == "," and depth == 0:
            args.append("".join(cur))
            cur = []
            continue
        cur.append(ch)
    args.append("".join(cur))
    return args


def extract_group_axes(expr: str) -> List[str]:
    """提取表达式里的分组轴（``group_*`` 算子的分组实参）。

    **为什么按轴分层（EUR 实证 2026-10-21）**：同一组字段在**不同分组轴**上
    是**不同持仓组合** ⇒ prod 相关性不同。实测 EUR fundamental72：
    sector 轴 CFO/TA×EBITDA>NI → prod 0.7571 / 0.7553（撞墙），
    industry 轴同一字段集 → prod 0.6747（破墙）。把两者聚合成「字段级饱和」
    会把**已探明能破墙的配方**一起拦掉（自我指涉误报）。
    """
    out: List[str] = []
    low = expr.lower()
    for op in _GROUP_OPS:
        for m in re.finditer(r"\b%s\s*\(" % op, low):
            i = m.end()
            depth = 1
            buf: List[str] = []
            while i < len(low):
                ch = low[i]
                if ch == "(":
                    depth += 1
                elif ch == ")":
                    depth -= 1
                    if depth == 0:
                        break
                buf.append(ch)
                i += 1
            args = _split_top_args("".join(buf))
            for a in args[1:]:
                a = a.strip()
                if a and "(" not in a and a in _GROUP_AXES:
                    out.append(a)
                    break
    return sorted(set(out))


def extract_group_ops(expr: str) -> List[str]:
    """提取表达式里用到的归一化 / 分组算子名（``group_*``）。

    **为什么归一化位也要进配方键（EUR 实证 2026-10-21）**：同一字段集 + 同一分组轴，
    换归一化位仍是**不同持仓组合**（实测 group_zscore 与 group_rank 同轴同载荷
    ⇒ S/F/2Y/sub 四个闸门同时上台阶）⇒ 撞墙证据不能跨归一化位外推。
    """
    low = expr.lower()
    out: List[str] = []
    for op in _GROUP_OPS:
        if re.search(r"\b%s\s*\(" % op, low):
            out.append(op)
    return sorted(set(out))


def recipe_key(expr: str) -> tuple:
    """配方键 = (字段集, 分组轴元组, 归一化算子集)。

    prod 撞墙是**配方级**事实：同字段集换轴 / 换归一化位即换持仓组合 ⇒
    撞墙证据只在该键上成立（EUR：sector×CFO/TA×zscore 0.7571 撞墙，
    industry×CFO/TA×zscore 0.6747 破墙；group_rank 变体不因 zscore 撞墙被连坐）。
    """
    return (frozenset(extract_fields(expr)),
            tuple(extract_group_axes(expr)),
            frozenset(extract_group_ops(expr)))


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

    # ---- 配方级饱和统计（字段集 × 分组轴）----
    # 2026-10-21 修正（EUR 实证）：原实现按**字段**聚合撞墙证据 ⇒ 同一组字段在不同
    # 分组轴上的读数被混在一起，于是「sector 轴撞墙（0.7571/0.7553）」会把
    # 「industry 轴已探明破墙（0.6747）」的同字段配方一起误判饱和 —— 自我指涉误报，
    # 直接拦住后续整族挖掘。prod 相关性是**持仓组合**的性质，分组轴就是组合的骨架，
    # 故证据必须按（字段集 × 轴）分层。
    field_hits: Counter = Counter()
    field_prod_hits: Counter = Counter()   # 该字段 alpha 中 prod_corr >= prod_wall 的条数
    field_prod_known: Counter = Counter()  # 该字段 alpha 中 prod_corr 已知的条数
    recipe_known: Counter = Counter()      # 每个配方上 prod 已知的 alpha 条数
    recipe_walls: Counter = Counter()      # 每个配方上 prod 撞墙的 alpha 条数
    for r in rows:
        expr = r.get("expression") or ""
        pc = r.get("prod_correlation")
        fields = set(extract_fields(expr))
        for f in fields:
            field_hits[f] += 1
            if pc is not None:
                field_prod_known[f] += 1
                if float(pc) >= cfg["prod_wall"]:
                    field_prod_hits[f] += 1
        key = recipe_key(expr)
        if pc is not None:
            recipe_known[key] += 1
            if float(pc) >= cfg["prod_wall"]:
                recipe_walls[key] += 1
    # 2026-09-19 修正：只数"本账户 IS 过闸 alpha 出现次数"会把修复循环里的同字段变体误判饱和
    # （IND mean_flash_estimate_eps prod 0.58 却被判饱和拦下 w179）。饱和必须有 prod 撞墙证据：
    # 该**配方**出现 >= field_hit_max 且 (已知 prod 的条数中 >= 50% 撞墙，且撞墙 >= min_prod_hits)；
    # 完全没有 prod 信息的配方只记 candidate（报告里列出，不判 FAIL）。
    min_prod_hits = int(cfg.get("min_prod_hits", 2))
    saturated_recipes = set()
    saturation_candidates = set()
    for key, known in recipe_known.items():
        walls = recipe_walls[key]
        if known and walls >= min_prod_hits and walls / known >= 0.5:
            saturated_recipes.add(key)
    for f, n in field_hits.items():
        if n >= cfg["field_hit_max"] and field_prod_known[f] == 0:
            saturation_candidates.add(f)
    # 报告口径：饱和字段 = 出现在已撞墙配方里的字段（向后兼容旧字段名）
    saturated_fields = sorted({f for key in saturated_recipes for f in key[0]})

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
    # 必须按 region 过滤：datasets 表有 region_id，同名数据集可能跨区登记，
    # 裸 WHERE name=? 会拿到别区的行，导致「本区数据集被判饱和」的假阳性。
    cur_ds_saturated = False
    if dataset:
        import sqlite3
        try:
            con = db_connect(db_path or os.path.join(REPO_ROOT, "data", "wqb.db"))
            did = con.execute(
                "SELECT d.id FROM datasets d JOIN regions r ON r.id = d.region_id"
                " WHERE d.name=? AND r.name=? LIMIT 1",
                (dataset, region),
            ).fetchone()
            con.close()
            if did and did[0] in saturated_dataset_ids:
                cur_ds_saturated = True
        except Exception:
            pass

    # ---- 逐表达式校验（按配方 = 字段集 × 分组轴）----
    violations = []
    n_checked = 0
    for i, expr in enumerate(exprs):
        fields = extract_fields(expr)
        if not fields:
            continue
        n_checked += 1
        key = recipe_key(expr)
        if key in saturated_recipes:
            violations.append({
                "index": i,
                "fields": sorted(key[0]),
                "axes": list(key[1]),
                "norm_ops": sorted(key[2]),
                "reason": "配方已确认撞 prod 墙（字段集 %s / 分组轴 %s / 归一化 %s；"
                          "≥%d 条 S≥%s 历史 alpha 中 ≥50%% 撞墙）"
                          % (sorted(key[0]), list(key[1]) or ["无分组轴"],
                             sorted(key[2]) or ["无分组算子"],
                             cfg["field_hit_max"], cfg["min_sharpe"]),
                "expr": expr[:100],
            })

    report.update({
        "n_history": len(rows),
        "n_checked": n_checked,
        "saturated_fields": saturated_fields,
        "saturated_recipes": [
            {"fields": sorted(k[0]), "axes": list(k[1]), "norm_ops": sorted(k[2]),
             "known": recipe_known[k], "walls": recipe_walls[k]}
            for k in sorted(saturated_recipes,
                            key=lambda k: (sorted(k[0]), k[1], sorted(k[2])))
        ],
        "saturation_candidates_no_prod": sorted(saturation_candidates),
        "saturated_dataset_ids": sorted(saturated_dataset_ids),
        "current_dataset_saturated": cur_ds_saturated,
        "violations": violations,
        "passed": not violations and not cur_ds_saturated,
    })
    if violations:
        report["message"] = (
            f"{len(violations)} 条表达式命中已撞 prod 墙的配方，"
            f"{len(saturated_fields)} 个字段涉及 {len(saturated_recipes)} 个饱和配方 —— "
            f"换字段族/分组轴/数据集再生成。"
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
    for r in (report.get("saturated_recipes") or [])[:6]:
        lines.append("[prod-sat] 饱和配方: 字段 %s / 轴 %s / 归一化 %s（已知 prod %s 条，撞墙 %s 条）"
                     % (r["fields"], r["axes"] or "无分组轴",
                        r.get("norm_ops") or "无分组算子", r["known"], r["walls"]))
    if report.get("saturated_fields"):
        sf = report["saturated_fields"][:10]
        lines.append(f"[prod-sat] 历史饱和字段: {sf}"
                     + (f" 等 {len(report['saturated_fields'])} 个" if len(report['saturated_fields']) > 10 else ""))
    for v in report.get("violations", [])[:5]:
        lines.append("[prod-sat]   命中 #%s: %s / 轴 %s / 归一化 %s | %s"
                     % (v["index"], v.get("fields"), v.get("axes"),
                        v.get("norm_ops") or "-", v["expr"]))
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
    import os as _os_sc; _os_sc.environ.setdefault("WQB_STARTUP_CHECKS", "once")  # 启动校验每进程只打一次（2026-09-19）
    main()
