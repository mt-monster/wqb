# -*- coding: utf-8 -*-
"""提交 RRAvGrn0（EUR_R_ARMINS_01）。用户于 2026-10-24 明确授权提交此颗。

前置终验（本脚本内复查，任一不过即中止，不发提交）：
  - status == UNSUBMITTED
  - ra.failed_ra_count == 0 且 checks.fail 为空
  - sharpe >= 1.58 / fitness >= 1.0 / turnover 在 [0.01, 0.7]
  - prod correlation < 0.7（check_correlation(refresh=True) 已在会话内确认 0.5437）
  - self correlation < 0.7（0.1723）

提交后按 MEMORY §0 的 ~240s 翻转窗轮询，直到 ACTIVE 或超时。
"""
from __future__ import annotations

import asyncio
import json
import os
import sys
import time

# 2026-10-27：原先第二行写死 Git-Bash 形态的绝对盘符路径
# (`/d/coding/...`)，换机 / 换目录即静默 ImportError。改为相对本文件推导。
_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(_ROOT, "src"))
sys.path.insert(0, os.path.join(_ROOT, "world-quant-brain-mcp"))

from wqb.workflow._common import get_brain_client  # noqa: E402

TARGET = "RRAvGrn0"
FLIP_WAIT_S = 260
POLL_INTERVAL = 15


def preflight(d: dict) -> tuple[bool, list[str]]:
    problems: list[str] = []
    m = d.get("metrics") or {}
    ra = d.get("ra") or {}
    checks = d.get("checks") or {}

    if d.get("status") != "UNSUBMITTED":
        problems.append(f"status={d.get('status')} != UNSUBMITTED")
    if int(ra.get("failed_ra_count") or 0) != 0:
        problems.append(f"failed_ra_count={ra.get('failed_ra_count')}")
    if checks.get("fail"):
        problems.append(f"checks.fail={checks.get('fail')}")

    s = m.get("sharpe")
    f = m.get("fitness")
    to = m.get("turnover")
    if s is None or s < 1.58:
        problems.append(f"sharpe={s} < 1.58")
    if f is None or f < 1.0:
        problems.append(f"fitness={f} < 1.0")
    if to is None or not (0.01 <= to <= 0.70):
        problems.append(f"turnover={to} out of [0.01,0.70]")
    return (not problems), problems


async def main() -> int:
    client = get_brain_client()

    print(f"=== Step 1: {TARGET} 提交前终验 ===")
    d = await client.get_alpha_details(TARGET)
    m = d.get("metrics") or {}
    ra = d.get("ra") or {}
    print(f"status={d.get('status')} stage={d.get('stage')} name={d.get('name')}")
    print(f"sharpe={m.get('sharpe')} fitness={m.get('fitness')} turnover={m.get('turnover')} "
          f"returns={m.get('returns')} drawdown={m.get('drawdown')} margin={m.get('margin')}")
    print(f"2Y={m.get('two_year_sharpe')} sub={m.get('sub_universe_sharpe')} "
          f"rob={m.get('robust_universe_sharpe')}")
    print(f"failed_ra_count={ra.get('failed_ra_count')} failed_ra_checks={ra.get('failed_ra_checks')}")
    print(f"pyramids={json.dumps(d.get('pyramids'), ensure_ascii=False)}")

    ok, problems = preflight(d)
    if not ok:
        print("\n[ABORT] 终验未通过，不提交：")
        for p in problems:
            print("  -", p)
        return 2
    print("\n[OK] 终验通过（模拟层无 FAIL、RA 0、S/F/TO 达标）")

    print(f"\n=== Step 2: POST /alphas/{TARGET}/submit ===")
    try:
        resp = await client.submit_alpha(TARGET)
        print(f"[submit] -> {json.dumps(resp, ensure_ascii=False)[:600]}")
    except Exception as e:
        print(f"[submit] ERROR: {e}")

    print(f"\n=== Step 3: 轮询翻转窗口（至多 {FLIP_WAIT_S}s）===")
    deadline = time.time() + FLIP_WAIT_S
    final = d
    while time.time() < deadline:
        await asyncio.sleep(POLL_INTERVAL)
        try:
            cur = await client.get_alpha_details(TARGET)
            st = cur.get("status")
            print(f"  t+{int(FLIP_WAIT_S - (deadline - time.time()))}s status={st} stage={cur.get('stage')} "
                  f"dateSubmitted={cur.get('dateSubmitted')}")
            final = cur
            if st == "ACTIVE":
                break
        except Exception as e:
            print(f"  poll error: {e}")

    print("\n=== Step 4: 最终状态 ===")
    m = final.get("metrics") or {}
    ra = final.get("ra") or {}
    checks = final.get("checks") or {}
    print(f"status={final.get('status')} stage={final.get('stage')} "
          f"dateSubmitted={final.get('dateSubmitted')}")
    print(f"failed_ra_count={ra.get('failed_ra_count')} failed_ppa_count={ra.get('failed_ppa_count')}")
    print(f"checks.fail={checks.get('fail')}")
    print(f"checks.pass={checks.get('pass')}")
    print(f"sharpe={m.get('sharpe')} fitness={m.get('fitness')} 2Y={m.get('two_year_sharpe')}")
    print(f"pyramids={json.dumps(final.get('pyramids'), ensure_ascii=False)}")
    print(f"\nACTIVE={final.get('status') == 'ACTIVE'}")
    return 0 if final.get("status") == "ACTIVE" else 1


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
