# -*- coding: utf-8 -*-
"""backfill_alpha_metrics_from_platform.py — 从平台补 `alphas` 缺失的 2Y/sub/ladder。

★ 为什么需要它（2026-10-06 定案）
  平台**有** two_year_sharpe / sub_universe_sharpe（在 `get_alpha_details` 的
  `is.checks` 各 check 的 `value`，或 `metrics.*`），但部分本地入库路径没抽：
    - `tools/sync_platform_alphas.py` 曾**显式传 two_year_sharpe=None**（已修）；
    - 非 harvest 路径（无 `backtest_results` 行，如 `P0gv3AO7`）从不抽 2Y/sub。
  全库实测 **1798/11002 行 2Y 为 NULL**。本工具按需从平台回填，**不改 ingest 逻辑、不改回测**。

★ 口径
  - 目标 = `alphas` 中 `two_year_sharpe IS NULL OR sub_universe_sharpe IS NULL` 的行（可筛区/IDs/仅闸内）。
  - 只**补空**：已有值的列不覆盖（`--overwrite` 才覆盖）。
  - **每颗落盘可断点续跑**（checkpoint `results/backfill_alpha_metrics_checkpoint.json`）。
  - 默认 **dry-run**；`--apply` 才写库。纯 GET 只读平台，不占相关性队列。
用法:
  python tools/backfill_alpha_metrics_from_platform.py                     # dry-run（默认全库 NULL 行）
  python tools/backfill_alpha_metrics_from_platform.py --only-gate         # 只看「过 IS 闸」的 NULL 行
  python tools/backfill_alpha_metrics_from_platform.py --region GBR        # 限区
  python tools/backfill_alpha_metrics_from_platform.py --ids P0gv3AO7 xAb1 # 指定颗
  python tools/backfill_alpha_metrics_from_platform.py --only-gate --limit 200 --apply
退出码: 0=正常  3=DB/平台失败
"""
from __future__ import annotations

import argparse
import asyncio
import json
import os
import sqlite3
import sys
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple

_sys_pe = sys
_os_pe = os
_sys_pe.path.insert(0, _os_pe.path.dirname(_os_pe.path.abspath(__file__)))


REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MCP_DIR = os.path.join(REPO_ROOT, "world-quant-brain-mcp")
DB = os.path.join(REPO_ROOT, "data", "wqb.db")
CKPT = os.path.join(REPO_ROOT, "results", "backfill_alpha_metrics_checkpoint.json")


def _first_not_none(*vals: Any) -> Optional[float]:
    for v in vals:
        if v is not None:
            return v
    return None


def extract_is_metrics(d: Dict[str, Any]) -> Tuple[Optional[float], Optional[float], Optional[float]]:
    """从 `get_alpha_details` 的对象里抽 (two_year, sub_universe, is_ladder)。

    兼容平台多种形态：`is.checks[].value`（LOW_2Y_SHARPE / LOW_SUB_UNIVERSE_SHARPE /
    IS_LADDER_SHARPE）、`is.*` 扁平、`metrics.*`。
    """
    isd = d.get("is") or {}
    met = d.get("metrics") or {}
    ty = sub = ladder = None
    for c in (isd.get("checks") or []):
        if not isinstance(c, dict):
            continue
        n, v = c.get("name"), c.get("value")
        if v is None:
            continue
        if n == "LOW_2Y_SHARPE":
            ty = v
        elif n == "LOW_SUB_UNIVERSE_SHARPE":
            sub = v
        elif n == "IS_LADDER_SHARPE":
            ladder = v
    ty = _first_not_none(ty, isd.get("two_year_sharpe"), met.get("two_year_sharpe"),
                         (d.get("two_year_sharpe")))
    sub = _first_not_none(sub, isd.get("sub_universe_sharpe"), met.get("sub_universe_sharpe"),
                          (d.get("sub_universe_sharpe")))
    ladder = _first_not_none(ladder, isd.get("is_ladder_sharpe"), met.get("is_ladder_sharpe"))
    return ty, sub, ladder


def load_ckpt() -> Dict[str, Any]:
    if os.path.exists(CKPT):
        try:
            return json.load(open(CKPT, encoding="utf-8"))
        except Exception:
            pass
    return {"done": {}}


def save_ckpt(ck: Dict[str, Any]) -> None:
    os.makedirs(os.path.dirname(CKPT), exist_ok=True)
    tmp = CKPT + ".tmp"
    json.dump(ck, open(tmp, "w", encoding="utf-8"), ensure_ascii=False)
    os.replace(tmp, CKPT)


def pick_targets(con: sqlite3.Connection, region: Optional[str], only_gate: bool,
                 ids: Optional[List[str]], limit: Optional[int]) -> List[Tuple[str, Optional[str]]]:
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    if ids:
        q = ("SELECT a.alpha_id, r.name region FROM alphas a LEFT JOIN regions r ON a.region_id=r.id "
             "WHERE a.alpha_id IN (" + ",".join("?" * len(ids)) + ")")
        return [(r["alpha_id"], r["region"]) for r in cur.execute(q, ids).fetchall()]
    q = ("SELECT a.alpha_id, r.name region FROM alphas a LEFT JOIN regions r ON a.region_id=r.id "
         "WHERE (a.two_year_sharpe IS NULL OR a.sub_universe_sharpe IS NULL)")
    ps: List[Any] = []
    if region:
        q += " AND r.name = ?"
        ps.append(region)
    if only_gate:
        q += (" AND COALESCE(a.status,'') IN ('UNSUBMITTED','COMPLETE') "
              "AND COALESCE(a.soft_deleted,0)=0 AND COALESCE(a.disposition,'')<>'DEAD' "
              "AND COALESCE(a.platform_status,'') NOT IN ('ACTIVE','DECOMMISSIONED') "
              "AND a.date_submitted IS NULL "
              "AND a.sharpe>=1.58 AND a.fitness>=1.0 "
              "AND (a.prod_correlation IS NULL OR a.prod_correlation<0.7)")
    q += " ORDER BY a.sharpe DESC"
    if limit:
        q += f" LIMIT {int(limit)}"
    return [(r["alpha_id"], r["region"]) for r in cur.execute(q, ps).fetchall()]


async def fetch_metrics(alpha_id: str) -> Dict[str, Any]:
    from brain_api import brain_client
    d = await brain_client.get_alpha_details(alpha_id)
    if isinstance(d, dict) and isinstance(d.get("result"), dict):
        d = d["result"]
    ty, sub, ladder = extract_is_metrics(d or {})
    return {"two_year_sharpe": ty, "sub_universe_sharpe": sub, "is_ladder_sharpe": ladder}


def main() -> int:
    ap = argparse.ArgumentParser(description="从平台补 alphas 缺失的 2Y/sub/ladder（只补空）")
    ap.add_argument("--region", default=None, help="限区（如 GBR）")
    ap.add_argument("--only-gate", action="store_true", help="只处理过 IS 闸的 NULL 行")
    ap.add_argument("--ids", nargs="*", default=None, help="指定 alpha_id 列表")
    ap.add_argument("--limit", type=int, default=None, help="最多处理条数（按 sharpe 降序）")
    ap.add_argument("--apply", action="store_true", help="写库（默认 dry-run）")
    ap.add_argument("--overwrite", action="store_true", help="已有值的列也覆盖")
    a = ap.parse_args()

    try:
        con = sqlite3.connect(DB, timeout=15)
        targets = pick_targets(con, a.region, a.only_gate, a.ids, a.limit)
    except Exception as e:  # noqa: BLE001
        print(f"[ERROR] DB 打开/查询失败: {e}", file=sys.stderr)
        return 3
    con.row_factory = sqlite3.Row
    cur = con.cursor()

    ck = load_ckpt()
    done = ck.get("done", {})
    todo = [t for t in targets if t[0] not in done]
    print(f"目标 {len(targets)} 颗（已跳过已完成 {len(targets)-len(todo)}）; 待处理 {len(todo)}")
    if not a.apply:
        print("[dry-run] 未写库；加 --apply 生效。")
        for aid, reg in todo[:20]:
            print(f"  {aid} [{reg}]")
        if len(todo) > 20:
            print(f"  … 其余 {len(todo)-20} 条")
        return 0

    ts = datetime.now().isoformat(timespec="seconds")
    got = miss = err = 0
    for i, (aid, reg) in enumerate(todo):
        try:
            m = asyncio.run(fetch_metrics(aid))
        except Exception as e:  # noqa: BLE001
            err += 1
            done[aid] = {"error": str(e)[:120]}
            save_ckpt({"done": done})
            print(f"  [err] {aid}: {str(e)[:100]}")
            continue
        sets, vals = [], []
        for col, key in (("two_year_sharpe", "two_year_sharpe"),
                         ("sub_universe_sharpe", "sub_universe_sharpe"),
                         ("is_ladder_sharpe", "is_ladder_sharpe")):
            v = m.get(key)
            if v is None:
                continue
            if a.overwrite:
                sets.append(f"{col}=?"); vals.append(v)
            else:
                sets.append(f"{col}=COALESCE({col}, ?)"); vals.append(v)
        if sets:
            sets.append("updated_at=?"); vals.append(ts)
            cur.execute(f"UPDATE alphas SET {', '.join(sets)} WHERE alpha_id=?", vals + [aid])
            con.commit()
            got += 1
            done[aid] = {k: m.get(k) for k in ("two_year_sharpe", "sub_universe_sharpe", "is_ladder_sharpe")}
        else:
            miss += 1
            done[aid] = {"no_metrics": True}
        save_ckpt({"done": done})
        if (i + 1) % 25 == 0:
            print(f"  进度 {i+1}/{len(todo)} 补到={got} 无值={miss} 失败={err}")
    print(f"\n[apply] 完成：补到 {got} / 无值 {miss} / 失败 {err}（checkpoint={CKPT}）")
    r = cur.execute("""SELECT COUNT(*), SUM(CASE WHEN two_year_sharpe IS NOT NULL THEN 1 ELSE 0 END),
        SUM(CASE WHEN sub_universe_sharpe IS NOT NULL THEN 1 ELSE 0 END) FROM alphas""").fetchone()
    print(f"alphas 现状: 总量={r[0]} 2Y有值={r[1]} sub有值={r[2]}")
    con.close()
    return 0


if __name__ == "__main__":
    sys.path.insert(0, MCP_DIR)
    try:
        import _pyenv  # type: ignore  # noqa: E402
        _pyenv.reexec_under_venv()
    except Exception:
        pass
    sys.exit(main())
