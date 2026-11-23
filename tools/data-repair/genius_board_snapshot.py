"""Genius 榜快照（CAP / CSAP / COP 等季度账户级指标）。

## 背景

平台 Genius 榜 ``GET /consultant/boards/genius?user=<id>`` 返回账户级季度绩效：
  - ``combinedAlphaPerformance``            → CAP  (Combined Alpha Performance)
  - ``combinedSelectedAlphaPerformance``    → CSAP (Combined Selected Alpha Performance)
  - ``combinedOsmosisPerformance``          → COP  (Combined Osmosis Performance)
  - ``combinedPowerPoolAlphaPerformance``   → CPPA (Power Pool 分项，政策上不参与，仅存档)
  - rank / geniusLevel / alphaCount / pyramidCount / operator·field·community ...

这些是**账户级、季度刷新**（平台公告：CAP 每 4-6 周更新，统计截至上季末 OS 期），
**没有当日值**，也不在 osmosis leaderboard（``stage=osmosis``）里——
osmosis 接口只有 dailyOsmosisRank / valueFactor 那套日频字段。

## 为什么单独落库

面板要在「Genius 综合表现」卡展示 CAP/CSAP/COP，需要历史做趋势。
本脚本每次跑写一行 ``genius_board_history``（按 sample_date 主键 upsert），
面板 ``panel_genius_board.py`` 读最新行 + 趋势。

## 用法

  PYTHONPATH=world-quant-brain-mcp python tools/data-repair/genius_board_snapshot.py
"""
from __future__ import annotations

import asyncio
import json
import os
import sys
from datetime import date, datetime, timedelta, timezone
from zoneinfo import ZoneInfo

_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, os.path.join(_ROOT, "world-quant-brain-mcp"))
sys.path.insert(0, _ROOT)
sys.path.insert(0, os.path.join(_ROOT, "src"))

DB = os.path.join(_ROOT, "data", "wqb.db")

CST = timezone(timedelta(hours=8))

_COLS = [
    ("sample_date", "TEXT PRIMARY KEY"),
    ("rank", "INTEGER"),
    ("genius_level", "TEXT"),
    ("best_level", "TEXT"),
    ("cap", "REAL"),                      # combinedAlphaPerformance
    ("csap", "REAL"),                     # combinedSelectedAlphaPerformance
    ("cop", "REAL"),                      # combinedOsmosisPerformance
    ("cppa", "REAL"),                     # combinedPowerPoolAlphaPerformance
    ("alpha_count", "INTEGER"),
    ("pyramid_count", "INTEGER"),
    ("operator_count", "INTEGER"),
    ("field_count", "INTEGER"),
    ("community_activity", "REAL"),
    ("max_simulation_streak", "INTEGER"),
    ("country", "TEXT"),
    ("raw_json", "TEXT"),
    ("sampled_at", "TEXT NOT NULL"),
]

#: 判「读数是否有变」的字段（sampled_at / raw_json 不参与）
_SIGNATURE = (
    "rank", "genius_level", "cap", "csap", "cop", "cppa",
    "alpha_count", "pyramid_count", "operator_count", "field_count",
    "community_activity", "max_simulation_streak",
)

#: 平台字段 → 本地列名
_FIELD_MAP = {
    "combinedAlphaPerformance": "cap",
    "combinedSelectedAlphaPerformance": "csap",
    "combinedOsmosisPerformance": "cop",
    "combinedPowerPoolAlphaPerformance": "cppa",
    "geniusLevel": "genius_level",
    "bestLevel": "best_level",
    "alphaCount": "alpha_count",
    "pyramidCount": "pyramid_count",
    "operatorCount": "operator_count",
    "fieldCount": "field_count",
    "communityActivity": "community_activity",
    "maxSimulationStreak": "max_simulation_streak",
    "country": "country",
}


def ensure_table(con) -> None:
    cols_sql = ",\n  ".join(f"{n} {t}" for n, t in _COLS)
    con.execute(f"CREATE TABLE IF NOT EXISTS genius_board_history (\n  {cols_sql}\n)")


def upsert(con, snap: dict, raw: str) -> None:
    snap = dict(snap)
    snap["raw_json"] = raw
    cols = [n for n, _ in _COLS]
    con.execute(
        f"""INSERT INTO genius_board_history ({', '.join(cols)})
            VALUES ({', '.join('?' for _ in cols)})
            ON CONFLICT(sample_date) DO UPDATE SET
            {', '.join(f'{n}=excluded.{n}' for n in cols if n != 'sample_date')}""",
        tuple(snap.get(n) for n in cols),
    )


async def main() -> int:
    from brain_api import brain_client
    from wqb.db_conn import connect

    now_cst = datetime.now(CST)
    today = now_cst.strftime("%Y-%m-%d")

    await brain_client.ensure_authenticated()
    base = brain_client.base_url
    user_resp = await brain_client._request("GET", base + "/users/self")
    user_resp.raise_for_status()
    user_id = user_resp.json().get("id")
    if not user_id:
        print("[error] 拿不到 user id", file=sys.stderr)
        return 1

    r = await brain_client._request(
        "GET", base + "/consultant/boards/genius",
        params={"user": user_id},
    )
    r.raise_for_status()
    rows = (r.json() or {}).get("results") or []
    if not rows:
        print("[error] genius 榜无返回行", file=sys.stderr)
        return 1
    row = rows[0]

    snap = {"sample_date": today, "rank": row.get("rank"),
            "sampled_at": now_cst.isoformat(timespec="seconds")}
    for plat_key, col in _FIELD_MAP.items():
        snap[col] = row.get(plat_key)

    con = connect(DB, readonly=False)
    try:
        ensure_table(con)
        prev = con.execute(
            f"SELECT {', '.join(_SIGNATURE)} FROM genius_board_history WHERE sample_date=?",
            (today,),
        ).fetchone()
        changed = prev is None or tuple(prev) != tuple(snap.get(k) for k in _SIGNATURE)
        upsert(con, snap, json.dumps(row, ensure_ascii=False))
        con.commit()
    finally:
        con.close()

    print(f"[ok] {today} rank={snap['rank']} lvl={snap['genius_level']} "
          f"CAP={snap['cap']} CSAP={snap['csap']} COP={snap['cop']} "
          f"({ 'changed' if changed else 'unchanged'}) "
          f"-> wqb.db::genius_board_history")
    return 0


if __name__ == "__main__":
    raise SystemExit(asyncio.run(main()))
