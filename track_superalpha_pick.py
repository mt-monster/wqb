#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""SuperAlpha 组件挑选（离线、只读）：拉干净组件详情，按字段族聚类，
跨族贪心选组成候选 SuperAlpha。正确端点 /alphas/{id}。"""
from __future__ import annotations

import asyncio
import json
import sys
from pathlib import Path
from collections import defaultdict

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "world-quant-brain-mcp"))
from brain_api import BrainApiClient  # noqa: E402

brain = BrainApiClient()
SUBSET = ROOT / "research-data" / "superalpha_prep" / "candidates.json"
OUT = ROOT / "research-data" / "superalpha_prep" / "picked.json"

FAMILIES = [
    ("model_value", ["mdl177", "mdl173"]),
    ("model_quality", ["mdl178", "mdl179", "mdl175"]),
    ("model_growth", ["mdl180", "mdl181", "mdl182"]),
    ("value_traditional", ["fwd_pe", "fwd_pb", "ep_yield", "market_cap"]),
    ("quality_financial", ["revenue_growth", "profit_margin", "roe", "roa"]),
    ("momentum", ["mom", "return_", "price_ret", "volatility"]),
    ("sentiment", ["sentiment", "vader", "news_sent"]),
    ("ownership", ["ownership", "aop", "open_pos"]),
    ("technical", ["rsi", "macd", "bollinger"]),
]

def classify(expr: str) -> list[str]:
    e = (expr or "").lower()
    hits = [f for f, kws in FAMILIES if any(k in e for k in kws)]
    return hits or ["other"]

def expr_of(alpha: dict) -> str:
    return alpha.get("expression") or alpha.get("expression_string") or ""

async def main():
    await brain.ensure_authenticated()
    rows = json.loads(SUBSET.read_text())
    clean = [r["id"] for r in rows if r["in_subset"] and not r["clash_partners"]]
    print(f"[干净组件] {len(clean)} 个（两两互相关均<0.7）")

    expr_map: dict[str, dict] = {}
    for aid in clean:
        try:
            d = await brain.get_alpha_details(aid)
            a = d.get("alpha") or d
            expr = expr_of(a)
            if not expr:
                continue
            sharpe = (a.get("sharpe_ratio") or a.get("fitness") or a.get("score")
                      or (a.get("recordsets") or [{}])[0].get("sharpe_ratio"))
            expr_map[aid] = {
                "expr": expr, "desc": a.get("description") or a.get("name") or "",
                "sharpe": sharpe, "families": classify(expr),
            }
        except Exception as ex:
            pass  # 静默跳过（404 等新 alpha 状态未落定）

    print(f"[成功取详情] {len(expr_map)}/{len(clean)} 个")
    if len(expr_map) < 4:
        print("[停止] 可取详情的组件不足 4 个，无法跨族挑选")
        OUT.write_text(json.dumps({"error": "not enough fetchable alphas", "n": len(expr_map)}))
        return

    fam_to_ids = defaultdict(list)
    for aid, info in expr_map.items():
        for f in info["families"]:
            fam_to_ids[f].append(aid)
    fam_desc = {"model_value": "模型价值", "model_quality": "模型质量", "model_growth": "模型成长",
                "value_traditional": "传统价值", "quality_financial": "财务质量", "momentum": "动量",
                "sentiment": "情绪", "ownership": "持仓", "technical": "技术", "other": "其他"}
    print("\n[字段族分布]")
    for f, ids in sorted(fam_to_ids.items(), key=lambda x: -len(x[1])):
        print(f"  {f:20s} ({fam_desc.get(f,f):8s}) : {len(ids)} 个")

    # 贪心跨族：优先覆盖大族，族内选 sharpe 最高；跳过纯重复族
    picked: list[dict] = []
    used_fams: set[str] = set()
    fams_sorted = sorted(fam_to_ids.items(), key=lambda x: -len(x[1]))
    for f, ids in fams_sorted:
        scored = sorted(ids, key=lambda aid: -(expr_map[aid]["sharpe"] or 0))
        for aid in scored:
            if aid in [p["id"] for p in picked]:
                continue
            new_fams = [ff for ff in expr_map[aid]["families"] if ff not in used_fams]
            if not new_fams:
                continue
            picked.append({
                "id": aid, "sharpe": expr_map[aid]["sharpe"],
                "expr": expr_map[aid]["expr"], "desc": expr_map[aid]["desc"][:80],
                "families": expr_map[aid]["families"], "new_fams": new_fams,
            })
            used_fams.update(expr_map[aid]["families"])
            break
        if len(picked) >= 6:
            break

    if len(picked) < 4:
        remaining = sorted(
            [aid for aid in clean if aid not in [p["id"] for p in picked] and aid in expr_map],
            key=lambda aid: -(expr_map[aid]["sharpe"] or 0))
        for aid in remaining:
            if len(picked) >= 4:
                break
            picked.append({
                "id": aid, "sharpe": expr_map[aid]["sharpe"],
                "expr": expr_map[aid]["expr"], "desc": expr_map[aid]["desc"][:80],
                "families": expr_map[aid]["families"], "new_fams": [],
            })

    result = {
        "market": {"instrument": "EQUITY", "region": "USA", "universe": "TOP3000", "delay": 1},
        "n_clean": len(clean), "n_fetchable": len(expr_map), "n_picked": len(picked),
        "picked": picked, "families_covered": sorted(used_fams),
        "reasoning": "从干净组件中跨字段族贪心选4-6个，最大化族覆盖以压低生产相关。",
        "risks": [
            "生产相关是最大风险：组件同在USA/TOP3000/delay1，与mdl177同质书目重叠，需组合回测验证prod_corr<0.7",
            "部分组件sharpe可能较低，组合sharpe或不足",
        ],
    }
    OUT.write_text(json.dumps(result, ensure_ascii=False, indent=2, default=str))
    print(f"\n[组合] 选出 {len(picked)} 个组件，覆盖字段族: {sorted(used_fams)}")
    print(f"[落盘] {OUT}")
    for p in picked:
        print(f"  - {p['id']:>12s}  sharpe={p['sharpe']}  fams={p['families']}  {p['desc']}")

if __name__ == "__main__":
    asyncio.run(main())
