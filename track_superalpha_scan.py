#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""SUPER 组合变体扫描：多个 selection 变体，每个创建后立即探针 SELF/PROD 双闸。

目的：找到与 book 内已有 SA/生产池相关性 <0.7 的可行组合（离线，不消耗提交配额）。
变体轴：selectionLimit / self 闸阈值。
输出：research-data/superalpha_prep/scan_results.json
"""
from __future__ import annotations

import asyncio
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
MCP = ROOT / "world-quant-brain-mcp"
sys.path.insert(0, str(MCP))

from brain_api import BrainApiClient  # noqa: E402
from brain_api_models import SimulationSettings, SimulationData  # noqa: E402

brain = BrainApiClient()

REGION, UNIVERSE, DELAY, DECAY = "USA", "TOP3000", 1, 5
NEUTRALIZATION = "SUBINDUSTRY"
TRUNCATION = 0.08

# 变体矩阵（selectionLimit, self_gate, score_pow）
VARIANTS = [
    {"sel": 6,  "self": 0.45, "pow": 1},
    {"sel": 10, "self": 0.45, "pow": 1},
    {"sel": 15, "self": 0.50, "pow": 1},
    {"sel": 10, "self": 0.55, "pow": 2},
]

COMBO = (
    "stats = generate_stats(alpha); "
    "innerCorr = self_corr(stats.returns, 500); "
    "ic = if_else(innerCorr == 1.0, nan, innerCorr); "
    "maxCorr = reduce_max(ic); "
    "1 - maxCorr"
)


def _selection(self_gate: float, pow_: float) -> str:
    score = "(0.7 - prod_correlation)" if pow_ == 1 else \
        "((0.7 - prod_correlation) * (0.7 - prod_correlation))"
    return (
        f"({score}) * (self_correlation < {self_gate}) * "
        "(turnover > 0.01) * (turnover < 0.5) * (1 + 0 * (prod_correlation > 0))"
    )


async def create_and_probe(v: dict) -> dict:
    tag = f"sel{v['sel']}_self{v['self']}_p{v['pow']}"
    settings = SimulationSettings(
        instrumentType="EQUITY", region=REGION, universe=UNIVERSE,
        delay=DELAY, decay=DECAY, neutralization=NEUTRALIZATION,
        truncation=TRUNCATION, testPeriod="P0Y0M", language="FASTEXPR",
        visualization=False, pasteurization="ON", maxTrade="OFF",
        selectionHandling="POSITIVE", selectionLimit=v["sel"],
        componentActivation="IS", unitHandling="VERIFY", nanHandling="ON",
    )
    sim_data = SimulationData(
        type="SUPER", settings=settings, regular=None,
        combo=COMBO, selection=_selection(v["self"], v["pow"]),
    )
    rec = {"variant": tag, "sel": v["sel"], "self_gate": v["self"], "score_pow": v["pow"]}
    try:
        result = await brain.create_simulation(sim_data)
        if "error" in result:
            rec.update({"error": result.get("error"), "message": result.get("message")})
            return rec
        aid = result.get("id")
        rec["alpha_id"] = aid
        is_ = result.get("is") or {}
        rec["sharpe"] = is_.get("sharpe")
        rec["fitness"] = is_.get("fitness")
        rec["turnover"] = is_.get("turnover")
        # 双闸探针
        selfr = await brain.check_self_correlation(aid, correlation_type="self")
        rec["self_max"] = selfr.get("max_correlation")
        rec["self_pass"] = selfr.get("passes_check")
        try:
            prodr = await brain.check_correlation(aid, correlation_type="production")
            prod_max = None
            for c in prodr.get("checks", {}).values():
                prod_max = c.get("max_correlation")
                break
            rec["prod_max"] = prod_max
            rec["prod_pass"] = (prod_max is not None and prod_max < 0.7)
        except Exception as e:
            rec["prod_error"] = str(e)[:200]
    except Exception as e:
        rec.update({"exception": str(e)[:300]})
    return rec


async def main():
    await brain.ensure_authenticated()
    results = []
    for v in VARIANTS:
        tag = f"sel{v['sel']}_self{v['self']}_p{v['pow']}"
        print(f"\n>>> 变体 {tag}")
        rec = await create_and_probe(v)
        print(f"    {json.dumps({k: rec.get(k) for k in ['alpha_id','sharpe','fitness','self_max','self_pass','prod_max','prod_pass','error']}, ensure_ascii=False, default=str)}")
        results.append(rec)
    OUT = ROOT / "research-data" / "superalpha_prep" / "scan_results.json"
    OUT.write_text(json.dumps(results, ensure_ascii=False, indent=2, default=str))
    print(f"\n[落盘] {OUT}")


if __name__ == "__main__":
    asyncio.run(main())
