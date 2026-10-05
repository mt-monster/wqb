# -*- coding: utf-8 -*-
"""quota_status.py — 当日提交配额实况（ET 日历日口径；**提交配额的唯一实现**）。

**为什么需要它**（2026-09-21 事故）：提交前用 `GET /users/self/activities/submissions`
判断配额，该端点只返回 `{yesterday, current, previous, ytd}` 的快照 —— **没有 today 字段**，
且 `ytd.end` 停在昨天 → 极易误判为"今日 0 提交、配额全空"。实测当日被并行会话用掉 2 个后
仍显示"昨日 5"，导致本轮 3 颗里第 3 颗撞 `REGULAR_SUBMISSION(4/4)` 配额墙。

**可靠口径**：列 `stage=OS` 按 `dateSubmitted` 倒序，数**今天（ET）**提交的条目，并按类型分流。
配额上限：REGULAR 4 / ET 日；SUPER 1 / ET 日（**两条独立配额线**）；PPA 独立 1 / ET 日。
类型口径的唯一实现在 `wqb.quota`（判型首选记录自带的 `type` 字段）。

⚠ 2026-10-05 修正：此前本工具把今日提交**总数**当作 REGULAR 用量。因平台对
REGULAR（4/ET 日）与 SUPER（1/ET 日）是两条**独立**配额线，混合计数会**高估** REGULAR 用量
⇒ 在 REGULAR 仍有余额时误报满额、拦下合法提交。
实测当日 4 颗提交中 1 颗为 SUPER（`IND_S_10comp_...`），工具报 `4/4`，**实际 `3/4`**。
ET 日界由 `wqb.timeutil` 计算（America/New_York，含夏令时；2026-11-01 起 00:00 ET = 13:00 GMT+8）。
toolkit `pipeline.py` 的配额闸复用同一口径（`wqb.timeutil` + OS 池 dateSubmitted），
不再读 activities/submissions。

用法（自动 re-exec 到 MCP venv；`WQ_PY` 可覆盖解释器）：
  python tools/quota_status.py
"""
import argparse
import asyncio
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _pyenv  # noqa: E402  跨平台解释器/MCP 目录解析

try:  # 唯一实现见 wqb.quota（type 字段判型）；此处仅为向后兼容的模块级别名
    from wqb.quota import REGULAR_DAILY_LIMIT as REGULAR_LIMIT
    from wqb.quota import SUPER_DAILY_LIMIT as SUPER_LIMIT
except Exception:  # pragma: no cover — wqb 不在 sys.path 时退回字面量
    REGULAR_LIMIT, SUPER_LIMIT = 4, 1


def todays_submissions(results, now_utc=None):
    """OS 池结果里 dateSubmitted 落在**当前 ET 日历日**的条目 → [(region, alpha_id, dateSubmitted)]。

    时间解析与日界判定的唯一实现 = `wqb.quota.probe_today`；本函数只是它的元组视图
    （保持既有调用形态与测试口径），不再自己拆时间戳 —— 2026-10-05 消除双份实现。
    """
    from wqb.quota import probe_today
    q = probe_today(results, now_utc)
    return [(e["region"], e["alpha_id"], e["dateSubmitted"]) for e in q["entries"]]


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

    from wqb.quota import probe_today
    q = probe_today(res)

    print(f"ET 日 = {et_today()}（当前 ET {et_now():%H:%M}）")
    print(f"今日已提交 = {len(q['entries'])} 颗"
          f"（REGULAR {q['regular_explicit']} / SUPER {q['super_used']}"
          + (f" / 未判型 {q['unclassified_used']}" if q["unclassified_used"] else "") + "）")
    for e in q["entries"]:
        print(f"  {e['dateSubmitted']}  {e['kind']:<7} {(e['region'] or '?'):<5} {e['alpha_id']}")

    print(f"\nREGULAR 配额：{q['regular_used']}/{q['regular_limit']}"
          f" → 剩余 {q['regular_remaining']}"
          + (f"（含未判型 {q['unclassified_used']} 颗，按保守口径计入）"
             if q["unclassified_used"] else ""))
    if q["regular_remaining"] == 0:
        print("  ★ 今日 REGULAR 已用尽：任何新提交都会 403 `REGULAR_SUBMISSION(value=4, limit=4)`"
              f"（零成本，不扣配额）→ 等 ET 次日 00:00 重置（现为 {et_reset_hour_gmt8()}:00 GMT+8）")
    print(f"SUPER 配额：{q['super_used']}/{q['super_limit']} → 剩余 {q['super_remaining']}"
          "（与 REGULAR 是**两条独立配额线**）")
    if q["unclassified_used"]:
        print(f"  ⚠ 未判型 {q['unclassified_used']} 颗：已按保守口径计入 REGULAR；"
              "若持续非 0 说明上游记录缺 `type` 字段，请复核（判型依据见 wqb.quota.alpha_kind）")
    print("\n注意：`activities/submissions` 端点只有 yesterday/current/previous/ytd 快照，"
          "缺 today → 不得用于当日配额判断。")


if __name__ == "__main__":
    asyncio.run(main())
