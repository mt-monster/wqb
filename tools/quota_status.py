# -*- coding: utf-8 -*-
"""quota_status.py — 当日提交配额实况（ET 日口径）。

**为什么需要它**（2026-09-21 事故）：提交前用 `GET /users/self/activities/submissions`
判断配额，该端点只返回 `{yesterday, current, previous, ytd}` 的快照 —— **没有 today 字段**，
且 `ytd.end` 停在昨天 → 极易误判为"今日 0 提交、配额全空"。实测当日被并行会话用掉 2 个后
仍显示"昨日 5"，导致本轮 3 颗里第 3 颗撞 `REGULAR_SUBMISSION(4/4)` 配额墙。

**可靠口径**：列 `stage=OS` 按 `dateSubmitted` 倒序，数**今天（ET）**提交的颗数。
配额上限：REGULAR 4 / ET 日；SUPER 1 / ET 日（本工具数 REGULAR 用量）。

用法（需 MCP venv 的 Python）：
  world-quant-brain-mcp/.venv/Scripts/python.exe tools/quota_status.py
  ... --submission-type SUPER        # 改看 SUPER（其判定需从提交响应的 checks 取，见下）
"""
import argparse
import asyncio
import os
import sys
from datetime import datetime, timedelta, timezone

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "world-quant-brain-mcp"))
REGULAR_LIMIT = 4
SUPER_LIMIT = 1
ET = timezone(timedelta(hours=-4))  # EDT；EST 时改 -5


def et_today():
    return datetime.now(ET).strftime("%Y-%m-%d")


async def main():
    ap = argparse.ArgumentParser(description="当日提交配额实况（ET 日口径）")
    ap.add_argument("--limit-scan", type=int, default=100)
    a = ap.parse_args()

    from brain_api import brain_client
    await brain_client.ensure_authenticated()

    r = await brain_client.get_user_alphas(stage="OS", limit=a.limit_scan, offset=0,
                                          order="-dateSubmitted")
    res = (r or {}).get("results") or []
    today = et_today()
    todays = []
    for x in res:
        ds = x.get("dateSubmitted") or ""
        if not ds:
            continue
        try:
            d = datetime.fromisoformat(ds)
        except ValueError:
            continue
        if d.astimezone(ET).strftime("%Y-%m-%d") == today:
            todays.append(((x.get("settings") or {}).get("region"), x.get("id"), ds))

    print(f"ET 日 = {today}（当前 ET {datetime.now(ET):%H:%M}）")
    print(f"今日已提交 = {len(todays)} 颗")
    for reg, aid, ds in todays:
        print(f"  {ds}  {reg:<5} {aid}")

    used_r = len(todays)
    print(f"\nREGULAR 配额：{used_r}/{REGULAR_LIMIT} → 剩余 {max(0, REGULAR_LIMIT - used_r)}")
    if used_r >= REGULAR_LIMIT:
        print("  ★ 今日 REGULAR 已用尽：任何新提交都会 403 `REGULAR_SUBMISSION(value=4, limit=4)`"
              "（零成本，不扣配额）→ 等 ET 次日 12:00 GMT+8 重置")
    print(f"SUPER 配额上限 {SUPER_LIMIT}/ET 日（本工具不区分类型，SUPER 用量需从提交响应 checks 读）")
    print("\n注意：`activities/submissions` 端点只有 yesterday/current/previous/ytd 快照，"
          "缺 today → 不得用于当日配额判断。")


asyncio.run(main())
