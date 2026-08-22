#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""创建 SUPER 组合模拟（type=SUPER, selection+combo, SUBINDUSTRY）。

不消耗提交配额（创建模拟≠提交）。组件自动从 book 内同 region ACTIVE REGULAR 中
按 selection 评分筛选。创建完成后输出模拟结果（sharpe/fitness/checks），
PROD/SELF 探针由 check_* 端点零成本查询。

用法（world-quant-brain-mcp/.venv）：
    python track_superalpha_create.py
"""
from __future__ import annotations

import asyncio
import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
MCP = ROOT / "world-quant-brain-mcp"
sys.path.insert(0, str(MCP))

from brain_api import BrainApiClient  # noqa: E402
from brain_api_models import SimulationSettings, SimulationData  # noqa: E402

brain = BrainApiClient()

# ---------- SUPER 配置（对齐 KPGvRMg1：USA/TOP3000/delay1/decay5/SUBINDUSTRY）----------
REGION, UNIVERSE, DELAY, DECAY = "USA", "TOP3000", 1, 5
NEUTRALIZATION = "SUBINDUSTRY"
TRUNCATION = 0.08
# 变体参数（env 可覆盖）：selectionLimit / self 闸阈值 / combo 权重形状 / 评分幂
SELECTION_LIMIT = int(os.environ.get("SELECTION_LIMIT", "10"))
SELF_GATE = float(os.environ.get("SELF_GATE", "0.55"))
SCORE_POWER = float(os.environ.get("SCORE_POWER", "1"))  # (0.7-prod)^P
TAG = os.environ.get("TAG", f"sel{SELECTION_LIMIT}_self{SELF_GATE}_p{SCORE_POWER}")

# selection（KPGvRMg1 模板变体：self 闸阈值 / 评分幂可调）
_SEL_SCORE = f"((0.7 - prod_correlation))" if SCORE_POWER == 1 else \
    f"((0.7 - prod_correlation) * (0.7 - prod_correlation))"
SELECTION = (
    f"({_SEL_SCORE}) * "
    f"(self_correlation < {SELF_GATE}) * "
    "(turnover > 0.01) * (turnover < 0.5) * "
    "(1 + 0 * (prod_correlation > 0))"
)
# combo（KPGvRMg1 真实模板：多语句定义 maxCorr 后 1-maxCorr）
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
        instrumentType="EQUITY",
        region=REGION,
        universe=UNIVERSE,
        delay=DELAY,
        decay=DECAY,
        neutralization=NEUTRALIZATION,
        truncation=TRUNCATION,
        testPeriod="P0Y0M",
        language="FASTEXPR",
        visualization=False,
        pasteurization="ON",
        maxTrade="OFF",
        selectionHandling="POSITIVE",
        selectionLimit=SELECTION_LIMIT,
        componentActivation="IS",
        unitHandling="VERIFY",
        nanHandling="ON",
    )
    sim_data = SimulationData(
        type="SUPER",
        settings=settings,
        regular=None,
        combo=COMBO,
        selection=SELECTION,
    )

    print(f"[创建] SUPER {REGION}/{UNIVERSE}/d{DELAY}/decay{DECAY}/{NEUTRALIZATION} "
          f"selectionLimit={SELECTION_LIMIT} self_gate={SELF_GATE} score_pow={SCORE_POWER} [{TAG}]")
    print(f"  selection: {SELECTION}")
    print(f"  combo:     {COMBO}")
    print("  (模拟轮询可能需要 1-5 分钟...)")

    result = await brain.create_simulation(sim_data)
    OUT = ROOT / "research-data" / "superalpha_prep" / f"super_create_{TAG}.json"
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, ensure_ascii=False, indent=2, default=str))

    if "error" in result:
        print(f"[错误] {result['error']}")
        print(f"[落盘] {OUT}")
        return

    aid = result.get("id")
    print(f"[结果] alpha id = {aid}")
    is_ = result.get("is") or {}
    print(f"  sharpe={is_.get('sharpe')}  fitness={is_.get('fitness')}  "
          f"turnover={is_.get('turnover')}  returns={is_.get('returns')}")
    checks = result.get("checks") or []
    for c in checks:
        print(f"  check {c.get('name')}: {c.get('result')}")
    print(f"[落盘] {OUT}")


if __name__ == "__main__":
    asyncio.run(main())
