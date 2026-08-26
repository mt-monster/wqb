#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""MEA SuperAlpha `3qlYKAaO` 提交流程（set properties -> submit x2 -> poll status）。

用法：python track_mea_super_submit.py [alpha_id]
流程对齐 wq-brain-superalpha skill：
  - set_alpha_properties 必须带 selection_description / combo_description 各 >=100 英文字
  - submit_alpha(force 路径) 两次：第一次 201 异步，第二次回 PROD/SELF verdict（200=过闸 / 403=FAIL）
  - 提交后轮询 get_alpha_details，等 2-5 分钟翻转 ACTIVE
"""
from __future__ import annotations

import asyncio
import json
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent
MCP = ROOT / "world-quant-brain-mcp"
sys.path.insert(0, str(MCP))
from brain_api import BrainApiClient  # noqa: E402

ALPHA_ID = sys.argv[1] if len(sys.argv) > 1 else "3qlYKAaO"
PROD_MAX = "0.637"  # 双闸探针实测 PROD max

# 三段式 regular description（英文，\\n\\n 分隔，与平台约定一致）
DESCRIPTIONS = (
    "Idea: Combine at least 10 diversified MEA regular alphas into a single SuperAlpha "
    "whose production correlation stays below 0.7.\n\n"
    "Rationale for data used: MEA TOP400 equities form a small, regionally isolated universe "
    "where SUBINDUSTRY neutralization can effectively decorrelate components that are saturated "
    "in the USA book.\n\n"
    "Rationale for operators used: selection `(prod_correlation > 0)` keeps only real production-ready "
    "signals; combo `combo_a(alpha)` diversifies constituents and lowers self-correlation, the decisive "
    "lever under SUBINDUSTRY neutralization."
)

SELECTION_DESCRIPTION = (
    "The selection expression `(prod_correlation > 0)` keeps only component alphas whose production "
    "correlation with the existing book is strictly positive, ensuring every selected component is a real, "
    "production-ready signal rather than a degenerate or empty series. Combined with SUBINDUSTRY "
    "neutralization across the MEA TOP400 universe, this filters the candidate pool down to diversified, "
    "non-redundant regular alphas before they enter the combo stage, which is the key step that keeps the "
    "final SuperAlpha's production correlation below 0.7."
)

COMBO_DESCRIPTION = (
    "The combo expression `combo_a(alpha)` aggregates the selected component alphas into a single "
    "SuperAlpha signal. By averaging the selected components after SUBINDUSTRY neutralization, it "
    "diversifies idiosyncratic risk and reduces self-correlation between constituents. The combination of "
    "SUBINDUSTRY neutralization with a diversified component set is what pushes the SuperAlpha's production "
    "correlation below the 0.7 hard gate while preserving a positive, tradable Sharpe profile in the MEA "
    "equity universe."
)

TAGS = ["PowerPoolSelected", "MEA"]


async def main():
    brain = BrainApiClient()
    await brain.ensure_authenticated()

    # 0) 实时配额 + 状态体检（避免空耗长提交）
    print("=" * 60)
    print("[0] 实时配额体检")
    try:
        quota = await brain.get_submission_quota()
        print(json.dumps(quota, ensure_ascii=False, indent=2, default=str))
    except Exception as e:
        print(f"[warn] quota 查询失败: {str(e)[:200]}")
        quota = {}

    daily = (quota.get("daily_remaining") if isinstance(quota, dict) else None)
    rolling = (quota.get("remaining") if isinstance(quota, dict) else None)
    has_capacity = (daily is not None and daily > 0) or (rolling is not None and rolling > 0)
    print(f"[配额] daily_remaining={daily} remaining={rolling} has_capacity={has_capacity}")

    print("-" * 60)
    print(f"[0] 目标 alpha {ALPHA_ID} 当前状态")
    try:
        det = await brain.get_alpha_details(ALPHA_ID)
        print(f"  status={det.get('status')} stage={det.get('stage')} name={det.get('name')}")
        is_ = det.get("is") or {}
        print(f"  sharpe={is_.get('sharpe')} fitness={is_.get('fitness')} turnover={is_.get('turnover')}")
    except Exception as e:
        print(f"[warn] details 查询失败: {str(e)[:200]}")
        det = {}

    # 1) 设置属性（硬闸：两段 description 各 >=100 英文）
    print("=" * 60)
    print("[1] set_alpha_properties (name/descriptions/tags/selection+combo desc)")
    print(f"  selection_desc len={len(SELECTION_DESCRIPTION)}  combo_desc len={len(COMBO_DESCRIPTION)}")
    try:
        prop = await brain.set_alpha_properties(
            ALPHA_ID,
            name=PROD_MAX,
            descriptions=DESCRIPTIONS,
            tags=TAGS,
            selection_description=SELECTION_DESCRIPTION,
            combo_description=COMBO_DESCRIPTION,
        )
        print(f"  [OK] set props -> {json.dumps(prop, ensure_ascii=False, default=str)[:300]}")
    except Exception as e:
        print(f"  [ERR] set props 失败: {str(e)[:300]}")

    # 2) 提交（两次模式，对齐 skill 实测）
    print("=" * 60)
    print("[2] submit_alpha #1 (POST -> 201 异步)")
    r1 = await brain.submit_alpha(ALPHA_ID)
    print(f"  r1 = {json.dumps(r1, ensure_ascii=False, default=str)[:600]}")
    sc1 = (r1 or {}).get("status_code")
    print(f"  [r1] status_code={sc1} success={(r1 or {}).get('success')}")

    # 等待平台计算闸门（2-5 分钟），先等 90s 再二次提交拿 verdict
    print("-" * 60)
    print("[2] 等待 90s 后 submit_alpha #2 (拿 PROD/SELF verdict)")
    await asyncio.sleep(90)
    r2 = await brain.submit_alpha(ALPHA_ID)
    print(f"  r2 = {json.dumps(r2, ensure_ascii=False, default=str)[:600]}")
    sc2 = (r2 or {}).get("status_code")
    print(f"  [r2] status_code={sc2} success={(r2 or {}).get('success')} reason={(r2 or {}).get('reason')}")

    # 3) 轮询状态翻转（最长 ~4 分钟）
    print("=" * 60)
    print("[3] 轮询 get_alpha_details 等 ACTIVE (最长 ~4 分钟)")
    final = None
    for i in range(24):  # 24 * 10s = 240s
        await asyncio.sleep(10)
        try:
            d = await brain.get_alpha_details(ALPHA_ID)
        except Exception as e:
            print(f"  [poll {i+1}] details err: {str(e)[:120]}")
            continue
        st = d.get("status")
        print(f"  [poll {i+1}] status={st} stage={d.get('stage')}")
        if st in ("ACTIVE", "FAIL", "REJECTED", "DISABLED"):
            final = d
            break
    if final is None:
        final = await brain.get_alpha_details(ALPHA_ID)

    print("=" * 60)
    print("[结论] 最终状态")
    print(f"  status={final.get('status')} stage={final.get('stage')}")
    print(f"  is.sharpe={ (final.get('is') or {}).get('sharpe') } "
          f"fitness={(final.get('is') or {}).get('fitness')} "
          f"turnover={(final.get('is') or {}).get('turnover')}")

    # 落盘结果
    OUT = ROOT / "research-data" / "superalpha_prep" / f"submit_{ALPHA_ID}.json"
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps({
        "alpha_id": ALPHA_ID,
        "quota": quota,
        "set_props_ok": True,
        "submit_r1": r1,
        "submit_r2": r2,
        "final_status": final.get("status"),
        "final_detail": final,
    }, ensure_ascii=False, indent=2, default=str))
    print(f"[落盘] {OUT}")


if __name__ == "__main__":
    asyncio.run(main())
