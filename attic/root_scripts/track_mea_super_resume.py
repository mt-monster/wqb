#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""MEA SuperAlpha 提交恢复/诊断：检查状态 + 必要时重试提交 + 轮询翻转。

容错：所有网络调用包 try/except，ReadTimeout 重试；轮询带退避。
用法：python track_mea_super_resume.py [alpha_id]
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


async def safe(fn, *a, retries=3, label="call", **kw):
    last = None
    for i in range(retries):
        try:
            return await fn(*a, **kw)
        except Exception as e:
            last = e
            wait = 15 * (i + 1)
            print(f"  [{label}] 尝试 {i+1} 失败: {str(e)[:160]}；{wait}s 后重试")
            await asyncio.sleep(wait)
    print(f"  [{label}] 重试 {retries} 次仍失败: {str(last)[:160]}")
    return None


async def main():
    brain = BrainApiClient()
    await brain.ensure_authenticated()

    print("=" * 60)
    print(f"[诊断] alpha {ALPHA_ID} 状态")
    det = await safe(brain.get_alpha_details, ALPHA_ID, label="get_alpha_details")
    if det is None:
        print("[致命] 无法获取 alpha 状态，退出")
        return
    status = det.get("status")
    stage = det.get("stage")
    print(f"  status={status} stage={stage} name={det.get('name')}")
    is_ = det.get("is") or {}
    print(f"  sharpe={is_.get('sharpe')} fitness={is_.get('fitness')} turnover={is_.get('turnover')}")
    # 列出 IS checks（若有）
    checks = (is_.get("checks") if isinstance(is_, dict) else None)
    if checks:
        for c in checks:
            print(f"    IS check: {c.get('name')} = {c.get('result')} (value={c.get('value')}, limit={c.get('limit')})")

    submitted_states = {"SUBMITTED", "PROCESSING", "TESTED", "ACTIVE", "PENDING"}
    if status in submitted_states or status in ("FAIL", "REJECTED", "DISABLED"):
        print(f"[结论] alpha 已处于终态/处理态：{status}，无需再提交。")
        # 仍轮询等待 ACTIVE（若还在处理）
        if status not in ("ACTIVE", "FAIL", "REJECTED", "DISABLED"):
            print("[轮询] 等待翻转 ACTIVE (最长 ~4 分钟)")
            for i in range(24):
                await asyncio.sleep(10)
                d = await safe(brain.get_alpha_details, ALPHA_ID, label=f"poll{i+1}")
                st = (d or {}).get("status")
                print(f"  [poll {i+1}] status={st}")
                if st in ("ACTIVE", "FAIL", "REJECTED", "DISABLED"):
                    status = st
                    break
        _report(brain, ALPHA_ID, status, det)
        return

    # status == UNSUBMITTED -> 执行提交
    print("=" * 60)
    print("[提交] status=UNSUBMITTED，发起 submit_alpha（带超时重试）")
    r = await safe(brain.submit_alpha, ALPHA_ID, label="submit_alpha", retries=4)
    print(f"  submit 返回: {json.dumps(r, ensure_ascii=False, default=str)[:600]}")
    sc = (r or {}).get("status_code")
    print(f"  status_code={sc} success={(r or {}).get('success')} reason={(r or {}).get('reason')}")

    print("-" * 60)
    print("[轮询] 等待翻转 ACTIVE (最长 ~5 分钟)")
    final_status = None
    for i in range(30):  # 30 * 10s = 300s
        await asyncio.sleep(10)
        d = await safe(brain.get_alpha_details, ALPHA_ID, label=f"poll{i+1}")
        if d is None:
            continue
        st = d.get("status")
        print(f"  [poll {i+1}] status={st} stage={d.get('stage')}")
        if st in ("ACTIVE", "FAIL", "REJECTED", "DISABLED"):
            final_status = st
            det = d
            break
    if final_status is None:
        d = await safe(brain.get_alpha_details, ALPHA_ID, label="final")
        final_status = (d or {}).get("status")
        det = d or det
    _report(brain, ALPHA_ID, final_status, det)


def _report(brain, aid, status, det):
    print("=" * 60)
    print(f"[结论] alpha {aid} 最终 status={status}")
    is_ = (det or {}).get("is") or {}
    print(f"  is.sharpe={is_.get('sharpe')} fitness={is_.get('fitness')} turnover={is_.get('turnover')}")
    OUT = ROOT / "research-data" / "superalpha_prep" / f"resume_{aid}.json"
    OUT.parent.mkdir(parents=True, exist_ok=True)
    try:
        OUT.write_text(json.dumps({"alpha_id": aid, "final_status": status, "detail": det},
                                  ensure_ascii=False, indent=2, default=str))
        print(f"[落盘] {OUT}")
    except Exception as e:
        print(f"[warn] 落盘失败: {str(e)[:120]}")


if __name__ == "__main__":
    asyncio.run(main())
