# -*- coding: utf-8 -*-
"""续跑提交核验：检查 3 颗 alpha 当前状态，若 leM88RN5 仍为 UNSUBMITTED 则补发一次并轮询翻转。

用户已授权提交集合：pwvRK18v, rKd5lAo8, leM88RN5（去除 58jQknxX）。
此前 pwvRK18v / rKd5lAo8 已确认 ACTIVE；leM88RN5 POST 返 200 但 status 未翻转，本次补核+补发。
"""
from __future__ import annotations

import asyncio
import json
import os
import sys
import time

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "src"))
sys.path.insert(0, "/d/coding/traeCN_project/wqb/world-quant-brain-mcp")

from wqb.workflow._common import get_brain_client  # noqa: E402

ALPHAS = ["pwvRK18v", "rKd5lAo8", "leM88RN5"]
FLIP_WAIT_S = 240  # 平台翻转窗口（MEMORY §0）
POLL_INTERVAL = 15


async def details(client, alpha_id: str) -> dict:
    return await client.get_alpha_details(alpha_id)


def summarize(d: dict) -> str:
    return (f"status={d.get('status')} stage={d.get('stage')} "
            f"dateSubmitted={d.get('dateSubmitted')} "
            f"ra_failed={d.get('ra', {}).get('failed_ra_count') if isinstance(d.get('ra'), dict) else d.get('ra_failed_checks')}")


async def main() -> int:
    client = get_brain_client()

    # Step 1: 当前状态全量核对
    print("=== Step 1: 当前状态核对 ===")
    states = {}
    for aid in ALPHAS:
        try:
            d = await details(client, aid)
            states[aid] = d
            print(f"[{aid}] {summarize(d)}")
        except Exception as e:
            print(f"[{aid}] DETAILS ERROR: {e}")
            states[aid] = None

    # Step 2: 若 leM88RN5 未翻转，补发 + 轮询
    target = "leM88RN5"
    cur = states.get(target)
    need_resubmit = (cur is None) or cur.get("status") != "ACTIVE"
    print(f"\n=== Step 2: leM88RN5 是否需要补发 = {need_resubmit} ===")

    if need_resubmit:
        print(f"[resubmit] POST /alphas/{target}/submit ...")
        try:
            resp = await client.submit_alpha(target)
            print(f"[resubmit] submit_alpha -> {json.dumps(resp, ensure_ascii=False)[:500]}")
        except Exception as e:
            print(f"[resubmit] submit_alpha ERROR: {e}")

        # 轮询翻转
        print(f"[poll] 轮询 {target} 至多 {FLIP_WAIT_S}s ...")
        deadline = time.time() + FLIP_WAIT_S
        flipped = False
        while time.time() < deadline:
            await asyncio.sleep(POLL_INTERVAL)
            try:
                d = await details(client, target)
                st = d.get("status")
                print(f"  t+{int(FLIP_WAIT_S - (deadline - time.time()))}s status={st} stage={d.get('stage')}")
                if st == "ACTIVE":
                    flipped = True
                    states[target] = d
                    break
            except Exception as e:
                print(f"  poll error: {e}")
        print(f"[poll] flipped={flipped}")

    # Step 3: 最终汇总
    print("\n=== Step 3: 最终汇总 ===")
    all_active = True
    for aid in ALPHAS:
        try:
            d = await details(client, aid)
            ok = d.get("status") == "ACTIVE"
            all_active = all_active and ok
            print(f"[{aid}] {'ACTIVE ✓' if ok else 'NOT ACTIVE ✗'} | {summarize(d)}")
        except Exception as e:
            all_active = False
            print(f"[{aid}] FINAL ERROR: {e}")
    print(f"\nALL_ACTIVE={all_active}")
    return 0 if all_active else 1


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
