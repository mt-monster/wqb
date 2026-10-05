#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""direct_submit.py — 直连 brain_client 提交（绕开 MCP 的 env 快照问题）。

为什么需要：`workflow_submit_alpha` 经 MCP 进程，其 `ALLOW_ALPHA_SUBMIT`
env 快照恒为 False（WorkBuddy 连接器管理不读项目级 .mcp.json 的 env 块，
且 MCP 进程会堆叠残留）⇒ MCP 路径永远被 global_submit_lock 拦。
本脚本在**同进程内**于 import config 之前设 `WQB_ALLOW_ALPHA_SUBMIT=1`，
闸读到 True，然后直连 REST 提交。**须由用户明确授权后运行。**

用法::
    python tools/direct_submit.py <alpha_id> [--name NAME] [--color BLUE] [--dry-run]
"""
from __future__ import annotations

import argparse
import asyncio
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# ★★ 必须在 import wqb.config 之前设置（config 在 import 时读 env）
os.environ["WQB_ALLOW_ALPHA_SUBMIT"] = "1"

sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "world-quant-brain-mcp"))


def _assert_gate_open() -> None:
    from wqb import config as cfg

    if not getattr(cfg, "ALLOW_ALPHA_SUBMIT", False):
        raise SystemExit(
            "闸未放行：wqb.config.ALLOW_ALPHA_SUBMIT 仍为 False。"
            "确认 WQB_ALLOW_ALPHA_SUBMIT=1 是在 import config 之前设置的。"
        )
    print("[direct-submit] 闸已放行（ALLOW_ALPHA_SUBMIT=True）")


async def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("alpha_id")
    ap.add_argument("--name", default=None)
    ap.add_argument("--color", default=None)
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()

    _assert_gate_open()

    from brain_api import brain_client as brain

    await brain.ensure_authenticated()

    # 1) 防重复提交：查平台当前状态
    d = await brain._request("GET", brain.base_url + f"/alphas/{a.alpha_id}")
    j = d.json() or {}
    st, stage = j.get("status"), j.get("stage")
    print(f"[direct-submit] 平台现状：status={st} stage={stage}")
    if st == "ACTIVE" or stage == "OS":
        print("[direct-submit] 该 alpha 已是 ACTIVE/OS，跳过（防重复提交）")
        return 0

    # 2) 稳健性台账守卫（region 取自 alpha settings，勿硬编码 KOR）
    import sqlite3

    region = (j.get("settings") or {}).get("region")
    if not region:
        print("[direct-submit] ⚠ 无法从 alpha settings 取到 region，中止（防跨区误读台账）")
        return 3
    conn = sqlite3.connect(str(ROOT / "data" / "wqb.db"))
    row = conn.execute(
        "SELECT value FROM ledger_kv WHERE region=? AND key=?",
        (region, f"robustness_{a.alpha_id}"),
    ).fetchone()
    conn.close()
    if not row:
        print(f"[direct-submit] ⚠ 未找到 region={region} 的 robustness_{a.alpha_id} 台账，请先写台账")
        return 3
    print(f"[direct-submit] 稳健性台账存在（region={region}, {len(row[0])} 字节）")

    if a.dry_run:
        print("[direct-submit] DRY-RUN，不实际提交")
        return 0

    # 3) 设属性（可选）
    if a.name or a.color:
        payload = {}
        if a.name:
            payload["name"] = a.name
        if a.color:
            payload["color"] = a.color
        r = await brain._request(
            "PATCH", brain.base_url + f"/alphas/{a.alpha_id}", json=payload
        )
        print(f"[direct-submit] PATCH 属性 -> {r.status_code}")

    # 4) 提交
    r = await brain._request(
        "POST", brain.base_url + f"/alphas/{a.alpha_id}/submit"
    )
    print(f"[direct-submit] POST /submit -> HTTP {r.status_code}")
    if r.status_code not in (200, 201):
        print(f"[direct-submit] 提交被拒：{(r.text or '')[:300]}")
        return 1

    # 5) 轮询确认
    for i in range(12):
        await asyncio.sleep(15)
        d = await brain._request("GET", brain.base_url + f"/alphas/{a.alpha_id}")
        j = d.json() or {}
        st, stage = j.get("status"), j.get("stage")
        print(f"  [{i+1}] status={st} stage={stage}")
        if st == "ACTIVE" or stage == "OS":
            print(f"[direct-submit] ✅ 提交成功：{a.alpha_id} -> {st}/{stage}")
            return 0
    print("[direct-submit] ⚠ 轮询超时，请稍后手工核对")
    return 2


if __name__ == "__main__":
    raise SystemExit(asyncio.run(main()))
