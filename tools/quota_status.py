# -*- coding: utf-8 -*-
"""quota_status.py — 当日提交配额实况（ET 日历日口径；**提交配额的唯一实现**）。

**为什么需要它**（2026-09-21 事故）：提交前用 `GET /users/self/activities/submissions`
判断配额，该端点只返回 `{yesterday, current, previous, ytd}` 的快照 —— **没有 today 字段**，
且 `ytd.end` 停在昨天 → 极易误判为"今日 0 提交、配额全空"。实测当日被并行会话用掉 2 个后
仍显示"昨日 5"，导致本轮 3 颗里第 3 颗撞 `REGULAR_SUBMISSION(4/4)` 配额墙。

**可靠口径**：列 `stage=OS` 按 `dateSubmitted` 倒序，数**今天（ET）**提交的颗数，
并**按类型分流**（REGULAR / SUPER 是两条独立配额线，混算会高估 REGULAR 用量）。
唯一实现 = :mod:`wqb.quota`（判型 + 计数 + 上限常量）；本文件只做 IO 与展示。
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

# ⚠ `src` 目录此刻通常还不在 sys.path（只有 pytest 的 conftest 会先加），
#   所以顶层 import wqb.* 会让 `python tools/quota_status.py` 直接 ModuleNotFoundError。
#   这里做惰性兜底：能import 就绑到模块级（供既有测试/调用方按 `mod.todays_submissions` 取），
#   不能 import 也不报错 —— main() 里 bootstrap_paths() 之后会再取一次。
try:
    from wqb.quota import probe_today, todays_submissions  # noqa: F401
except ImportError:  # pragma: no cover —— 取决于调用方是否已把 src 加入 sys.path
    probe_today = todays_submissions = None  # type: ignore[assignment]


async def main():
    ap = argparse.ArgumentParser(description="当日提交配额实况（ET 日历日口径）")
    ap.add_argument("--limit-scan", type=int, default=100)
    a = ap.parse_args()

    _pyenv.reexec_under_venv()
    _pyenv.bootstrap_paths()
    # 上限与判型逻辑一律来自 wqb.quota（唯一实现源，勿在此复制数值）
    global probe_today
    if probe_today is None:
        from wqb.quota import probe_today  # noqa: F811
    from wqb.timeutil import et_now, et_reset_hour_gmt8
    from brain_api import brain_client
    await brain_client.ensure_authenticated()

    r = await brain_client.get_user_alphas(stage="OS", limit=a.limit_scan, offset=0,
                                          order="-dateSubmitted")
    res = (r or {}).get("results") or []
    q = probe_today(res)

    print(f"ET 日 = {q['et_day']}（当前 ET {et_now():%H:%M}）")
    unc = q.get("unclassified_used", 0)
    print(f"今日已提交 = {len(q['entries'])} 颗（REGULAR {q['regular_used']}"
          + (f"（含未判型 {unc}）" if unc else "")
          + f" / SUPER {q['super_used']}）")
    for e in q["entries"]:
        print(f"  {e['dateSubmitted']}  {e['kind']:<9} {(e['region'] or '?'):<5} {e['alpha_id']}")

    print(f"\nREGULAR 配额：{q['regular_used']}/{q['regular_limit']}"
          f" → 剩余 {q['regular_remaining']}")
    if q["regular_remaining"] == 0:
        print("  ★ 今日 REGULAR 已用尽：任何新提交都会 403 `REGULAR_SUBMISSION(value=4, limit=4)`"
              f"（零成本，不扣配额）→ 等 ET 次日 00:00 重置（现为 {et_reset_hour_gmt8()}:00 GMT+8）")
    print(f"SUPER 配额：{q['super_used']}/{q['super_limit']} → 剩余 {q['super_remaining']}"
          "（与 REGULAR 是**两条独立配额线**，互不占用）")
    if unc:
        print(f"  ⚠ {unc} 颗未能判型，已保守计入 REGULAR；判型依据见 wqb.quota.alpha_kind")
    print("\n注意：`activities/submissions` 端点只有 yesterday/current/previous/ytd 快照，"
          "缺 today → 不得用于当日配额判断。")


if __name__ == "__main__":
    asyncio.run(main())
