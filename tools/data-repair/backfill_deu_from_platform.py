#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""backfill_deu_from_platform.py — 把平台上「我自己的 DEU IS alpha」全部回填进本地 backtest_results。

**为什么要它（修复 #2 数据源缺口）**
    本会话 ~550 次测试的结果只存在于平台 + 终端输出里，**收割路径不落 backtest_results**
    ⇒ ① 画像的 UNTESTED 虚高、ALIVE 恒 0；② 会话记录一旦截断即永久丢失。

**做法**
    用 MCP 服务端的 BrainApiClient（同一鉴权）分页拉 `stage=IS` 的 alpha，
    把 code/metrics/ra 写进本地 `data/wqb.db::backtest_results`（幂等：按 alpha_id 去重）。

用法:
    python tools/backfill_deu_from_platform.py --region DEU --stage IS [--limit 100] [--dry-run]
"""
from __future__ import annotations

import argparse
import asyncio
import json
import os
import sqlite3
import sys
from typing import Any, Dict, List

from pathlib import Path as _Path

_REPO = str(next(_p for _p in _Path(__file__).resolve().parents if (_p / "pyproject.toml").exists() and (_p / "src" / "wqb").is_dir()))
DB = os.path.join(_REPO, "data", "wqb.db")
MCP = os.path.join(_REPO, "world-quant-brain-mcp")
sys.path.insert(0, MCP)


async def fetch_all(region: str, stage: str, page: int) -> List[Dict[str, Any]]:
    from brain_api import BrainApiClient  # noqa: E402

    c = BrainApiClient()
    await c.ensure_authenticated()
    out: List[Dict[str, Any]] = []
    offset = 0
    while True:
        url = f"{c.base_url}/users/self/alphas?stage={stage}&limit={page}&offset={offset}"
        r = await c._request("GET", url)
        if r.status_code != 200:
            print(f"[warn] offset={offset} HTTP {r.status_code}，停止分页")
            break
        j = r.json()
        res = j.get("results") or []
        if not res:
            break
        for a in res:
            st = (a.get("settings") or {}).get("region")
            if region and st and st.upper() != region.upper():
                continue
            out.append(a)
        print(f"[fetch] offset={offset} 本页 {len(res)} 条，累计匹配 {len(out)}")
        if not j.get("next") or len(res) < page:
            break
        offset += page
    return out


def to_row(a: Dict[str, Any], region: str, wave: str) -> Dict[str, Any]:
    """把平台列表接口的一条 alpha 映射成 backtest_results 行。

    ★ 关键结构（2026-10-08 实测确认）：
        a["regular"]["code"]           <- 表达式（**列表接口不返回顶层 code**）
        a["is"]                        <- IS 指标（sharpe/fitness/turnover/margin/...）
        a["is"]["checks"]["fail"]      <- 失败项列表 ⇒ 直接算 ra_failed_checks，无需额外调用
        a["classifications"]           <- 平台官方合规标记（如 DATA_USAGE:SINGLE_DATA_SET）
    """
    reg = a.get("regular") or {}
    m = a.get("is") or {}
    checks = m.get("checks")
    # ★ 列表接口里 is.checks 是 **list**（每项 {name,value,limit,result}）；详情接口里是 dict{fail,pass,...}
    if isinstance(checks, list):
        fails = [c.get("name") for c in checks
                 if isinstance(c, dict) and str(c.get("result", "")).upper() == "FAIL"]
        check_vals = {c.get("name"): c.get("value") for c in checks if isinstance(c, dict)}
    elif isinstance(checks, dict):
        fails = [c.get("name") for c in (checks.get("fail") or []) if isinstance(c, dict)]
        check_vals = {c.get("name"): c.get("value")
                      for c in (checks.get("fail") or []) if isinstance(c, dict)}
    else:
        fails, check_vals = [], {}

    # ★ 列表接口的 is 里没有 two_year_sharpe / sub_universe_sharpe，
    #   但 checks 里带了它们的 value ⇒ 从这里回填
    two_year = m.get("two_year_sharpe") or check_vals.get("LOW_2Y_SHARPE") or check_vals.get("IS_LADDER_SHARPE")
    sub_uni = m.get("sub_universe_sharpe") or check_vals.get("LOW_SUB_UNIVERSE_SHARPE")
    return {
        "expression_id": -1,  # 哨兵：回填行不关联 expressions 表
        "alpha_id": a.get("id"),
        "status": a.get("status"),
        "sharpe": m.get("sharpe"),
        "fitness": m.get("fitness"),
        "turnover": m.get("turnover"),
        "margin": m.get("margin"),
        "returns": m.get("returns"),
        "drawdown": m.get("drawdown"),
        "two_year_sharpe": two_year,
        "sub_universe_sharpe": sub_uni,
        "long_count": m.get("longCount"),
        "short_count": m.get("shortCount"),
        "pnl": m.get("pnl"),
        "book_size": m.get("bookSize"),
        "ra_failed_checks": json.dumps(fails),
        "region": region,
        "wave": wave,
        "dataset": None,
        "code": reg.get("code"),
        "payload_json": json.dumps(a, ensure_ascii=False),
        "risk_neutralized_sharpe": m.get("risk_neutralized_sharpe"),
    }


def upsert(con: sqlite3.Connection, rows: List[Dict[str, Any]]) -> int:
    cur = con.cursor()
    cols = list(rows[0].keys())
    n_new = 0
    for r in rows:
        got = cur.execute(
            "SELECT id FROM backtest_results WHERE alpha_id=?", (r["alpha_id"],)
        ).fetchone()
        if got:
            sets = ", ".join(f"{c}=?" for c in cols)
            cur.execute(
                f"UPDATE backtest_results SET {sets} WHERE alpha_id=?",
                [r[c] for c in cols] + [r["alpha_id"]],
            )
        else:
            cur.execute(
                f"INSERT INTO backtest_results ({','.join(cols)}, created_at) "
                f"VALUES ({','.join('?' * len(cols))}, datetime('now'))",
                [r[c] for c in cols],
            )
            n_new += 1
    con.commit()
    return n_new


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--region", default="DEU")
    ap.add_argument("--stage", default="IS")
    ap.add_argument("--limit", type=int, default=100)
    ap.add_argument("--wave", default="backfill_platform")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()

    alphas = asyncio.run(fetch_all(a.region, a.stage, a.limit))
    print(f"[fetch] 共取回 {a.region}/{a.stage} alpha {len(alphas)} 条")
    if not alphas:
        return 1
    rows = [to_row(x, a.region, a.wave) for x in alphas]
    if a.dry_run:
        print("[dry-run] 不落库。样例:", json.dumps(rows[0], ensure_ascii=False)[:300])
        return 0
    con = sqlite3.connect(DB)
    try:
        n = upsert(con, rows)
        print(f"[upsert] 新增 {n} 条 / 更新 {len(rows) - n} 条 → {DB}")
    finally:
        con.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
