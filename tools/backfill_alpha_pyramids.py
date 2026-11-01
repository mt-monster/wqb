# -*- coding: utf-8 -*-
"""把平台塔位指纹回填进 `alpha_pyramids`（复盘报告 A1）。

为什么需要
----------
`alphas` 表**没有** pyramid 列、没有 `decay` / `truncation` 列，`region_id` 还会混区
（同一 id 下 GBR 与 EUR 共存）。结果每轮审计都被迫逐条回平台 `get_alpha_details`。

★ 两个让这件事变简单的事实（2026-10-30 实测）：

1. **平台对 `UNSUBMITTED` alpha 也返回塔位，但位置在 `is.checks[]` 的
   `MATCHES_PYRAMID` 项里，不是顶层 `pyramids`**。
   实测 `rKRkL9QE`（`status=UNSUBMITTED`）：
   `j["pyramids"] is None`、`j["ra"]` 键不存在，而
   `j["is"]["checks"]` 里
   `{"name":"MATCHES_PYRAMID","effective":2,"multiplier":1.4,
     "pyramids":[{"name":"GBR/D1/PV","multiplier":1.4},
                 {"name":"GBR/D1/FUNDAMENTAL","multiplier":1.6}]}`
   ⇒ 不必等提交后才回填（解析逻辑在 `wqb/store/_pyramids.py`，本工具只负责取数）。
2. **`GET /alphas/{id}` 不占 prod 相关性单并发槽**（那是 `/correlations/prod` 专属）
   ⇒ 可以批量跑，只有 429 速率限制，没有队列锁。

★ 回填顺便**自纠混区**：库里存的是平台 `settings.region`，不是本地 `region_id`。

用法
----
    # 队列里所有 READY（最常用：提交前看这些会不会点塔）
    python tools/backfill_alpha_pyramids.py --region GBR --source ready

    # 队列全量（含 DEAD，用于历史归因）
    python tools/backfill_alpha_pyramids.py --region GBR --source queue

    # 本地 alphas 表里能捞到的（region 靠库内联表，可能混区，回填后自纠）
    python tools/backfill_alpha_pyramids.py --region GBR --source alphas --limit 300

    # 指定 alpha（最精确，零浪费）
    python tools/backfill_alpha_pyramids.py --ids rKRkL9QE 0mYoANkv WjOkLGWx --region GBR

    # 只读库出「如果全提交会点亮哪些塔」
    python tools/backfill_alpha_pyramids.py --region GBR --report
"""
from __future__ import annotations

import argparse
import asyncio
import os
import sqlite3
import sys

_REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _add_paths() -> None:
    for p in (os.path.join(_REPO, "src"),
              os.environ.get("WQ_MCP_DIR", os.path.join(_REPO, "world-quant-brain-mcp"))):
        if p and p not in sys.path:
            sys.path.insert(0, p)


def _db_path() -> str:
    return os.environ.get("WQB_DB_PATH") or os.path.join(_REPO, "data", "wqb.db")


def _ids_from_queue(region: str, status: str | None) -> list[str]:
    con = sqlite3.connect(_db_path())
    try:
        sql = "SELECT DISTINCT alpha_id FROM submit_ready WHERE region=?"
        args: list = [region]
        if status:
            sql += " AND status=?"
            args.append(status)
        sql += " AND alpha_id IS NOT NULL AND alpha_id != ''"
        return [r[0] for r in con.execute(sql, args)]
    finally:
        con.close()


def _ids_from_alphas(region: str, limit: int) -> list[str]:
    con = sqlite3.connect(_db_path())
    con.row_factory = sqlite3.Row
    try:
        rows = con.execute(
            """SELECT DISTINCT a.alpha_id FROM alphas a
               JOIN regions r ON r.id = a.region_id
               WHERE UPPER(r.name) = ? AND a.alpha_id IS NOT NULL
                 AND COALESCE(a.soft_deleted, 0) = 0
               ORDER BY a.sharpe DESC NULLS LAST
               LIMIT ?""",
            (region.upper(), int(limit)),
        )
        return [r["alpha_id"] for r in rows]
    finally:
        con.close()


async def _fetch(brain, alpha_id: str):
    """GET /alphas/{id}；失败返回 None（不抛，批量要跑完）。"""
    try:
        r = await brain._request("GET", f"{brain.base_url}/alphas/{alpha_id}")
    except Exception as exc:  # noqa: BLE001 - 单条失败不该中断整批
        print(f"  [ERR] {alpha_id}: {type(exc).__name__}: {exc}", flush=True)
        return None
    if getattr(r, "status_code", None) != 200:
        print(f"  [ERR] {alpha_id}: HTTP {getattr(r, 'status_code', '?')}", flush=True)
        return None
    try:
        return r.json()
    except Exception:  # noqa: BLE001
        return None


async def _backfill(alpha_ids: list[str], delay_s: float) -> dict:
    _add_paths()
    from brain_api import BrainApiClient  # noqa: E402
    from wqb.store import CampaignStore  # noqa: E402

    brain = BrainApiClient()
    await brain.ensure_authenticated()
    store = CampaignStore(_db_path())
    got = 0
    miss: list[str] = []
    regions: dict[str, int] = {}
    for i, aid in enumerate(alpha_ids, 1):
        detail = await _fetch(brain, aid)
        if not detail:
            miss.append(aid)
            continue
        store.upsert_alpha_pyramids(detail)
        got += 1
        d = detail.get("result", detail) if isinstance(detail, dict) else {}
        rg = str((d.get("settings") or {}).get("region") or "?")
        regions[rg] = regions.get(rg, 0) + 1
        if i % 10 == 0 or i == len(alpha_ids):
            print(f"  [{i}/{len(alpha_ids)}] ok={got} miss={len(miss)}", flush=True)
        if delay_s:
            await asyncio.sleep(delay_s)
    return {"fetched": got, "missed": len(miss), "miss_ids": miss, "by_region": regions}


def _report(region: str) -> int:
    _add_paths()
    from wqb.store import CampaignStore  # noqa: E402

    store = CampaignStore(_db_path())
    for delay in (1, 0):
        tally = store.pyramid_tally(region=region, delay=delay, only_clean=True)
        if not tally["n_alphas"]:
            continue
        print(f"\n=== {region}/D{delay} · fRA=0 的 {tally['n_alphas']} 颗若全提交 ===",
              flush=True)
        for name, slot in sorted(tally["towers"].items(), key=lambda kv: -kv[1]["n"]):
            mult = slot.get("multiplier")
            ms = f" ×{mult:g}" if isinstance(mult, (int, float)) else ""
            print(f"  {name:26s} {slot['n']:3d} 颗{ms}", flush=True)
        print(f"  其中一鱼多塔：{tally['n_multi_tower']} 颗", flush=True)
    rows = store.list_alpha_pyramids(region=region, only_clean=True, limit=10000)
    if not rows:
        print(f"[report] {region} 在 alpha_pyramids 里没有 fRA=0 的记录 —— 先跑回填。",
              flush=True)
        return 1
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description="回填 alpha_pyramids（塔位指纹）")
    ap.add_argument("--region", default="GBR", help="区域（大写），用于选源与报告")
    ap.add_argument("--source", default="ready",
                    choices=["ready", "queue", "alphas", "none"],
                    help="ready=队列 READY；queue=队列全量；alphas=本地 alphas 表；none=只跑 --ids")
    ap.add_argument("--status", default=None, help="--source queue 时的额外状态过滤")
    ap.add_argument("--ids", nargs="*", default=None, help="显式指定 alpha id")
    ap.add_argument("--limit", type=int, default=300, help="--source alphas 的取数上限")
    ap.add_argument("--delay", type=float, default=0.15, help="每次 GET 后的间隔秒（防 429）")
    ap.add_argument("--report", action="store_true", help="只读库出点塔报告，不发网络请求")
    a = ap.parse_args()

    region = str(a.region).upper()
    if a.report:
        return _report(region)

    ids: list[str] = list(a.ids or [])
    if a.source == "ready":
        ids += _ids_from_queue(region, "READY")
    elif a.source == "queue":
        ids += _ids_from_queue(region, a.status)
    elif a.source == "alphas":
        ids += _ids_from_alphas(region, a.limit)
    seen: set[str] = set()
    ids = [x for x in ids if x and not (x in seen or seen.add(x))]
    if not ids:
        print("[backfill] 没有待回填的 alpha id", flush=True)
        return 1

    print(f"[backfill] region={region} source={a.source} 目标 {len(ids)} 条", flush=True)
    res = asyncio.run(_backfill(ids, a.delay))
    print(f"\n[backfill] 成功 {res['fetched']} / 失败 {res['missed']}", flush=True)
    if res["by_region"]:
        print(f"[backfill] 平台回报的区域分布：{res['by_region']}", flush=True)
        wrong = {k: v for k, v in res["by_region"].items() if k != region}
        if wrong:
            print(f"[backfill] ⚠ 混区自纠：有 {sum(wrong.values())} 条其实不属于 {region} "
                  f"（{wrong}）—— 本地 region_id 骗人，已按平台值落库。", flush=True)
    if res["miss_ids"]:
        print(f"[backfill] 失败 id：{res['miss_ids'][:20]}", flush=True)
    _report(region)
    return 0


if __name__ == "__main__":
    sys.exit(main())
