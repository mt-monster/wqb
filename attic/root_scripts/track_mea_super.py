#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""MEA SUPER 组合尝试（region 参数化，复用 KPGvRMg1 selection/combo 模板）。

用法：python track_mea_super.py [sel_limit] [self_gate]
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

REGION = "MEA"
UNIVERSE = "TOP400"
DELAY, DECAY = 1, 5
NEUTRALIZATION = "SUBINDUSTRY"
TRUNCATION = 0.08

SELECTION_LIMIT = int(sys.argv[1]) if len(sys.argv) > 1 else 10
SELF_GATE = float(sys.argv[2]) if len(sys.argv) > 2 else 0.55

SELECTION = (
    "(0.7 - prod_correlation) * "
    f"(self_correlation < {SELF_GATE}) * "
    "(turnover > 0.01) * (turnover < 0.5) * "
    "(1 + 0 * (prod_correlation > 0))"
)
COMBO = (
    "stats = generate_stats(alpha); "
    "innerCorr = self_corr(stats.returns, 500); "
    "ic = if_else(innerCorr == 1.0, nan, innerCorr); "
    "maxCorr = reduce_max(ic); "
    "1 - maxCorr"
)


async def main():
    await brain.ensure_authenticated()
    settings = SimulationSettings(
        instrumentType="EQUITY", region=REGION, universe=UNIVERSE,
        delay=DELAY, decay=DECAY, neutralization=NEUTRALIZATION,
        truncation=TRUNCATION, testPeriod="P0Y0M", language="FASTEXPR",
        visualization=False, pasteurization="ON", maxTrade="OFF",
        selectionHandling="POSITIVE", selectionLimit=SELECTION_LIMIT,
        componentActivation="IS", unitHandling="VERIFY", nanHandling="ON",
    )
    sim_data = SimulationData(
        type="SUPER", settings=settings, regular=None,
        combo=COMBO, selection=SELECTION,
    )
    tag = f"mea_sel{SELECTION_LIMIT}_self{SELF_GATE}"
    print(f"[创建] SUPER {REGION}/{UNIVERSE}/d{DELAY}/decay{DECAY}/{NEUTRALIZATION} "
          f"selectionLimit={SELECTION_LIMIT} self_gate={SELF_GATE}")
    result = await brain.create_simulation(sim_data)
    OUT = ROOT / "research-data" / "superalpha_prep" / f"{tag}.json"
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, ensure_ascii=False, indent=2, default=str))
    if "error" in result:
        print(f"[错误] {result.get('error')}")
        print(f"[message] {result.get('message')}")
    else:
        aid = result.get("id")
        is_ = result.get("is") or {}
        print(f"[结果] alpha id = {aid}")
        print(f"  sharpe={is_.get('sharpe')} fitness={is_.get('fitness')} "
              f"turnover={is_.get('turnover')}")
        # 双闸探针
        selfr = await brain.check_self_correlation(aid, correlation_type="self")
        print(f"  SELF max={selfr.get('max_correlation')} pass={selfr.get('passes_check')}")
        try:
            prodr = await brain.check_correlation(aid, correlation_type="production")
            for c in prodr.get("checks", {}).values():
                print(f"  PROD max={c.get('max_correlation')} "
                      f"pass={c.get('passes_check')}")
                break
        except Exception as e:
            print(f"  PROD error: {str(e)[:200]}")
    print(f"[落盘] {OUT}")


if __name__ == "__main__":
    asyncio.run(main())
