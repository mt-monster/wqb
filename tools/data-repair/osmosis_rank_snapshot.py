#!/usr/bin/env python
"""Daily Osmosis Rank 快照采集（写 data/wqb.db::osmosis_rank_history，每日幂等）。

背景（2026-11-08 定案）：`dailyOsmosisRank` 无历史端点，读了不存即永久丢失。
锁点有 7-8 天时滞，判断某期配置（如 USA 纳入 6-scope）是赚是亏，唯一依据是
rank 日序列在各自生效窗口内的对比——因此必须每日采样。

落库（2026-11-08 定案）：写 wqb.db 规范表 `osmosis_rank_history`——results/ 是
gitignore 运行期目录，曾发生 override 文件静默丢失事故，DB 才是规范库（retention
管辖）。数据只此一处，raw_json 字段保底整行原始快照。

数据源：GET /consultant/boards/leader?stage=osmosis&user=<id>（单行）。
注意：user 参数只认显式 id，`user=self` 返回空行（2026-11-08 实测）。

表结构（宽表，一行=一天）：
  sample_date TEXT PRIMARY KEY          -- 采样日（CST 日界；13:30 CST ≈ 00:30 EST
                                           leaderboard 按 EST 日更，永远采到当日新鲜值）
  daily_osmosis_rank REAL               -- 当日 rank 分（0-1）
  mean_prod_correlation REAL            -- REGULAR 池平均 prod 相关
  mean_self_correlation REAL            -- REGULAR 池平均 self 相关
  super_mean_prod_correlation REAL       -- SUPER 池同口径
  super_mean_self_correlation REAL       -- SUPER 池同口径（曾读 0.6083 偏高，盯）
  submissions_count INTEGER             -- 提交总数（REGULAR+SUPER）
  super_submissions_count INTEGER       -- SUPER 提交数
  data_fields_used INTEGER              -- 用过的字段数（多样性）
  weight_factor REAL                    -- 语义未确认，存着观察
  value_factor REAL                     -- 语义未确认，存着观察
  raw_json TEXT                         -- 整行原始快照（防未来加字段丢数据）
  sampled_at TEXT                       -- 采样时刻 ISO

用法：
  PYTHONPATH=world-quant-brain-mcp python tools/data-repair/osmosis_rank_snapshot.py
"""
from __future__ import annotations

import asyncio
import json
import os
import sys
from datetime import datetime, timezone, timedelta

_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, os.path.join(_ROOT, "world-quant-brain-mcp"))
sys.path.insert(0, _ROOT)

DB = os.path.join(_ROOT, "data", "wqb.db")

CST = timezone(timedelta(hours=8))

_COLS = [
    ("sample_date", "TEXT PRIMARY KEY"),
    ("daily_osmosis_rank", "REAL"),
    ("mean_prod_correlation", "REAL"),
    ("mean_self_correlation", "REAL"),
    ("super_mean_prod_correlation", "REAL"),
    ("super_mean_self_correlation", "REAL"),
    ("submissions_count", "INTEGER"),
    ("super_submissions_count", "INTEGER"),
    ("data_fields_used", "INTEGER"),
    ("weight_factor", "REAL"),
    ("value_factor", "REAL"),
    ("raw_json", "TEXT"),
    ("sampled_at", "TEXT NOT NULL"),
]


def ensure_table(con) -> None:
    cols_sql = ",\n  ".join(f"{n} {t}" for n, t in _COLS)
    con.execute(f"CREATE TABLE IF NOT EXISTS osmosis_rank_history (\n  {cols_sql}\n)")


def upsert(con, snap: dict, raw: str) -> None:
    snap = dict(snap)
    snap["raw_json"] = raw
    cols = [n for n, _ in _COLS]
    con.execute(
        f"""INSERT INTO osmosis_rank_history ({', '.join(cols)})
            VALUES ({', '.join('?' for _ in cols)})
            ON CONFLICT(sample_date) DO UPDATE SET
            {', '.join(f'{n}=excluded.{n}' for n in cols if n != 'sample_date')}""",
        tuple(snap.get(n) for n in cols),
    )


async def main() -> int:
    from brain_api import brain_client
    from wqb.db_conn import connect

    # 采样日 = 今天（CST）
    today = datetime.now(CST).strftime("%Y-%m-%d")

    # leaderboard 不认 user=self，只认显式 id（2026-11-08 实测 self 返回空行）
    await brain_client.ensure_authenticated()
    user_resp = await brain_client._request("GET", brain_client.base_url + "/users/self")
    user_resp.raise_for_status()
    user_id = user_resp.json().get("id")
    if not user_id:
        print("[error] 拿不到 user id", file=sys.stderr)
        return 1

    r = await brain_client._request(
        "GET", brain_client.base_url + "/consultant/boards/leader",
        params={"stage": "osmosis", "user": user_id},
    )
    r.raise_for_status()
    rows = (r.json() or {}).get("results") or []
    if not rows:
        print("[error] leaderboard 无返回行", file=sys.stderr)
        return 1
    row = rows[0]
    rank = row.get("dailyOsmosisRank")

    con = connect(readonly=False)
    try:
        ensure_table(con)
        # 幂等：当日已有样本且 rank 相同则跳过；rank 变化（平台日内刷新）则覆盖
        prev = con.execute(
            "SELECT daily_osmosis_rank FROM osmosis_rank_history WHERE sample_date=?",
            (today,),
        ).fetchone()
        if prev is not None and prev[0] == rank:
            print(f"[skip] {today} 已采样 rank={rank}")
            return 0

        snap = {
            "sample_date": today,
            "daily_osmosis_rank": rank,
            "mean_prod_correlation": row.get("meanProdCorrelation"),
            "mean_self_correlation": row.get("meanSelfCorrelation"),
            "super_mean_prod_correlation": row.get("superAlphaMeanProdCorrelation"),
            "super_mean_self_correlation": row.get("superAlphaMeanSelfCorrelation"),
            "submissions_count": row.get("submissionsCount"),
            "super_submissions_count": row.get("superAlphaSubmissionsCount"),
            "data_fields_used": row.get("dataFieldsUsed"),
            "weight_factor": row.get("weightFactor"),
            "value_factor": row.get("valueFactor"),
            "sampled_at": datetime.now(CST).isoformat(timespec="seconds"),
        }
        upsert(con, snap, json.dumps(row, ensure_ascii=False))
        con.commit()
    finally:
        con.close()

    print(f"[ok] {today} rank={rank} prod={row.get('meanProdCorrelation')} "
          f"self={row.get('meanSelfCorrelation')} -> wqb.db::osmosis_rank_history")
    return 0


if __name__ == "__main__":
    raise SystemExit(asyncio.run(main()))
