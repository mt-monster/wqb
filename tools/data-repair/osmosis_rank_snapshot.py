#!/usr/bin/env python
"""Daily Osmosis 账户快照（写 data/wqb.db::osmosis_rank_history，每日幂等）。

背景（2026-11-08 定案）：`dailyOsmosisRank` 无历史端点，读了不存即永久丢失。
锁点有 7-8 天时滞，判断某期配置是赚是亏，唯一依据是 rank 日序列在各自
生效窗口内的对比——因此必须每日采样。

2026-11-10 升级（用户提问「只存这条记录够不够」后的整改）：
1. **去掉「rank 不变即跳过」的短路**。原逻辑只在 rank 变化时写库，而
   `submissionsCount` 几乎每天必涨、`dataFieldsUsed` / prod 也会变 ⇒ rank 不变
   的日子整天读数停在旧值（11-09 就因 15:29 已采、23:00 复采样被 skip，
   subs 之后的变化全部丢失）。现在一律 upsert，只在「全部读数与上一行相同」时
   标记 unchanged。
2. 新增 4 列（老库自动 ALTER 迁移，不重建表、不丢历史）：
   - `est_date`        采样时刻的纽约日期。平台按 EST 日更，CST 23:00 ≈ EST 10:00；
                       用 CST 日期当键会把跨日样本记错天。
   - `lock_sunday`     本次 rank 所用分配的锁定周日。官方：分配每周日 23:59 EST 锁，
                       **锁后第 8 天开始生效、持续一周**。
   - `effective_from`  = lock_sunday + 8 天（生效首日）。归因必须按这个键对齐，
                       不能按 sample_date。
   - `genius_level`    季度资格层。⚠ 2026-11-10 实测 `/users/self/consultant` 只回
                       `dateStarted` + `leaderboard`，**已不返回 geniusLevel** ⇒ 该列
                       当前恒为 NULL，保留待端点恢复。
3. `raw_json` 继续保留整行原始快照。

⚠ 机制边界（2026-11-10 核实官方 `osmosis-allocation-guide-consultants`）：
`dailyOsmosisRank` = 各**已分配** scope「当日 PnL 的横截面排名」的算术平均，
仅作 base payment 的 quality multiplier（1–2×）。本表是账户级标量，无法拆到
scope ⇒ per-scope 归因看 `osmosis_alloc_snapshot.py` 与 `osmosis_report.py`。
另：per-alpha OS 日 PnL **不可得**（`/alphas/{id}/recordsets/pnl` 只到 IS 期末
2023-12-29；加 startDate / os / is / version=2.0 参数均被忽略，2026-11-10 实测），
所以 combo 级 PnL 无法自建，per-scope 只能做代理指标。

数据源：GET /consultant/boards/leader?stage=osmosis&user=<id>（单行）。
注意：user 参数只认显式 id，`user=self` 返回空行（2026-11-08 实测）。

表结构（宽表，一行=一天）：
  sample_date TEXT PRIMARY KEY          -- 采样日（CST 日界，便于与本仓库其他日志对齐）
  daily_osmosis_rank REAL               -- 当日 rank 分（0-1，越大越好）
  mean_prod_correlation REAL            -- REGULAR 池平均 prod 相关
  mean_self_correlation REAL            -- REGULAR 池平均 self 相关
  super_mean_prod_correlation REAL      -- SUPER 池同口径
  super_mean_self_correlation REAL      -- SUPER 池同口径（曾读 0.6083 偏高，盯）
  submissions_count INTEGER             -- 提交总数（REGULAR+SUPER）
  super_submissions_count INTEGER       -- SUPER 提交数
  data_fields_used INTEGER              -- 用过的字段数（多样性）
  weight_factor REAL                    -- 季度奖乘数（季度奖 = WF × OS）
  value_factor REAL                     -- 每日 base 的核心乘数
  est_date TEXT                         -- 采样时刻纽约日期
  lock_sunday TEXT                      -- 该 rank 所用分配的锁定周日
  effective_from TEXT                   -- = lock_sunday + 8 天
  genius_level TEXT                     -- 季度资格层
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
from datetime import date, datetime, timedelta, timezone
from zoneinfo import ZoneInfo

_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, os.path.join(_ROOT, "world-quant-brain-mcp"))
sys.path.insert(0, _ROOT)
sys.path.insert(0, os.path.join(_ROOT, "src"))

DB = os.path.join(_ROOT, "data", "wqb.db")

CST = timezone(timedelta(hours=8))
NY = ZoneInfo("America/New_York")

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
    ("est_date", "TEXT"),
    ("lock_sunday", "TEXT"),
    ("effective_from", "TEXT"),
    ("genius_level", "TEXT"),
    ("raw_json", "TEXT"),
    ("sampled_at", "TEXT NOT NULL"),
]

#: 2026-11-10 新增列（老库用 ALTER 迁移）
_ADDED = ["est_date", "lock_sunday", "effective_from", "genius_level"]

#: 判「读数是否有变」的字段（sampled_at / raw_json 不参与）
_SIGNATURE = (
    "daily_osmosis_rank", "mean_prod_correlation", "mean_self_correlation",
    "super_mean_prod_correlation", "super_mean_self_correlation",
    "submissions_count", "super_submissions_count", "data_fields_used",
    "weight_factor", "value_factor",
)


def ensure_table(con) -> None:
    cols_sql = ",\n  ".join(f"{n} {t}" for n, t in _COLS)
    con.execute(f"CREATE TABLE IF NOT EXISTS osmosis_rank_history (\n  {cols_sql}\n)")
    have = {r[1] for r in con.execute("PRAGMA table_info(osmosis_rank_history)")}
    for name in _ADDED:
        if name not in have:
            con.execute(f"ALTER TABLE osmosis_rank_history ADD COLUMN {name} TEXT")


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


def lock_sunday_for(est_day: date) -> date:
    """给定采样日，返回其 rank 所用分配的锁定周日。

    官方：分配每周日 23:59 EST 锁定，锁后第 8 天开始生效、持续一周。
    例：2026-02-08（周日）锁 → 2026-02-16～02-22 使用。
    ⇒ lock = floor_sunday(est_day - 8)。
    """
    d = est_day - timedelta(days=8)
    return d - timedelta(days=(d.weekday() + 1) % 7)


async def main() -> int:
    from brain_api import brain_client
    from wqb.db_conn import connect

    now_cst = datetime.now(CST)
    now_ny = datetime.now(NY)
    today = now_cst.strftime("%Y-%m-%d")
    est_day = now_ny.date()
    lock = lock_sunday_for(est_day)
    effective_from = lock + timedelta(days=8)

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

    # geniusLevel：零成本顺带（失败留空，不阻断主采样）
    genius_level = None
    try:
        rc = await brain_client._request(
            "GET", brain_client.base_url + "/users/self/consultant")
        if rc.status_code == 200:
            body = rc.json() or {}
            g = body.get("geniusLevel")
            genius_level = g.get("level") if isinstance(g, dict) else g
    except Exception as exc:  # noqa: BLE001 - 辅助字段
        print(f"[warn] geniusLevel 读取失败：{type(exc).__name__}", file=sys.stderr)

    snap = {
        "sample_date": today,
        "daily_osmosis_rank": row.get("dailyOsmosisRank"),
        "mean_prod_correlation": row.get("meanProdCorrelation"),
        "mean_self_correlation": row.get("meanSelfCorrelation"),
        "super_mean_prod_correlation": row.get("superAlphaMeanProdCorrelation"),
        "super_mean_self_correlation": row.get("superAlphaMeanSelfCorrelation"),
        "submissions_count": row.get("submissionsCount"),
        "super_submissions_count": row.get("superAlphaSubmissionsCount"),
        "data_fields_used": row.get("dataFieldsUsed"),
        "weight_factor": row.get("weightFactor"),
        "value_factor": row.get("valueFactor"),
        "est_date": est_day.isoformat(),
        "lock_sunday": lock.isoformat(),
        "effective_from": effective_from.isoformat(),
        "genius_level": genius_level,
        "sampled_at": now_cst.isoformat(timespec="seconds"),
    }

    con = connect(DB, readonly=False)
    try:
        ensure_table(con)
        prev = con.execute(
            f"SELECT {', '.join(_SIGNATURE)} FROM osmosis_rank_history WHERE sample_date=?",
            (today,),
        ).fetchone()
        changed = prev is None or tuple(prev) != tuple(snap[k] for k in _SIGNATURE)
        upsert(con, snap, json.dumps(row, ensure_ascii=False))
        con.commit()
    finally:
        con.close()

    print(f"[ok] {today} rank={snap['daily_osmosis_rank']} "
          f"prod={snap['mean_prod_correlation']} self={snap['mean_self_correlation']} "
          f"vf={snap['value_factor']} wf={snap['weight_factor']} "
          f"lock={lock} ({'changed' if changed else 'unchanged'}) "
          f"-> wqb.db::osmosis_rank_history")
    return 0


if __name__ == "__main__":
    raise SystemExit(asyncio.run(main()))
