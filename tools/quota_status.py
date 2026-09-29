# -*- coding: utf-8 -*-
"""quota_status.py — 当日提交配额实况（ET 日历日口径；**提交配额的唯一实现**）。

**为什么需要它**（2026-09-21 事故）：提交前用 `GET /users/self/activities/submissions`
判断配额，该端点只返回 `{yesterday, current, previous, ytd}` 的快照 —— **没有 today 字段**，
且 `ytd.end` 停在昨天 → 极易误判为"今日 0 提交、配额全空"。实测当日被并行会话用掉 2 个后
仍显示"昨日 5"，导致本轮 3 颗里第 3 颗撞 `REGULAR_SUBMISSION(4/4)` 配额墙。

**可靠口径**：列 `stage=OS` 按 `dateSubmitted` 倒序，数**今天（ET）**提交的颗数。
配额上限：REGULAR 4 / ET 日；SUPER 1 / ET 日；PPA 独立 1 / ET 日（本工具数 OS 池里今日提交总数，
不区分类型——按类型的用量以提交响应 checks 的 value/limit 为准）。
ET 日界由 `wqb.timeutil` 计算（America/New_York，含夏令时；2026-11-01 起 00:00 ET = 13:00 GMT+8）。
toolkit `pipeline.py` 的配额闸复用同一口径（`wqb.timeutil` + OS 池 dateSubmitted），
不再读 activities/submissions。

用法（自动 re-exec 到 MCP venv；`WQ_PY` 可覆盖解释器）：
  python tools/quota_status.py
"""
import argparse
import asyncio
import datetime as _dt
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _pyenv  # noqa: E402  跨平台解释器/MCP 目录解析

REGULAR_LIMIT = 4
SUPER_LIMIT = 1


def todays_submissions(results, now_utc=None):
    """OS 池结果里 dateSubmitted 落在**当前 ET 日历日**的条目 → [(region, alpha_id, dateSubmitted)]。纯函数。"""
    from wqb.timeutil import et_date, et_today
    today = et_today(now_utc)
    out = []
    for x in results or []:
        ds = x.get("dateSubmitted") or ""
        if not ds:
            continue
        try:
            d = _dt.datetime.fromisoformat(ds.replace("Z", "+00:00"))
        except ValueError:
            continue
        if et_date(d) == today:
            out.append(((x.get("settings") or {}).get("region"), x.get("id"), ds))
    return out


async def main():
    ap = argparse.ArgumentParser(description="当日提交配额实况（ET 日历日口径）")
    ap.add_argument("--limit-scan", type=int, default=100)
    a = ap.parse_args()

    _pyenv.reexec_under_venv()
    _pyenv.bootstrap_paths()
    from wqb.timeutil import et_now, et_reset_hour_gmt8, et_today
    from brain_api import brain_client
    await brain_client.ensure_authenticated()

    r = await brain_client.get_user_alphas(stage="OS", limit=a.limit_scan, offset=0,
                                          order="-dateSubmitted")
    res = (r or {}).get("results") or []
    todays = todays_submissions(res)

    print(f"ET 日 = {et_today()}（当前 ET {et_now():%H:%M}）")
    print(f"今日已提交 = {len(todays)} 颗")
    for reg, aid, ds in todays:
        print(f"  {ds}  {reg or '?':<5} {aid}")

    used_r = len(todays)
    print(f"\nREGULAR 配额：{used_r}/{REGULAR_LIMIT} → 剩余 {max(0, REGULAR_LIMIT - used_r)}")
    if used_r >= REGULAR_LIMIT:
        print("  ★ 今日 REGULAR 已用尽：任何新提交都会 403 `REGULAR_SUBMISSION(value=4, limit=4)`"
              f"（零成本，不扣配额）→ 等 ET 次日 00:00 重置（现为 {et_reset_hour_gmt8()}:00 GMT+8）")
    print(f"SUPER 配额上限 {SUPER_LIMIT}/ET 日（本工具不区分类型，SUPER 用量需从提交响应 checks 读）")
    print("\n注意：`activities/submissions` 端点只有 yesterday/current/previous/ytd 快照，"
          "缺 today → 不得用于当日配额判断。")


if __name__ == "__main__":
    asyncio.run(main())
