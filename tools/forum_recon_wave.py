#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""forum_recon_wave.py — 波级默认取证：收批时对本波**共同卡住的那堵墙**（或全灭时的「有无解法」）问一次论坛，结果落 ledger。

定位：`tools/forum_recon.py` 是「有人提了问题 → 去查」；本工具是「没人记得提问题 → 代码替你问一次」。
问题由本波回测结果机械派生（`src/wqb/recon_wave.py`：墙问题 / 判死取证问题 / 不问），再交给 `forum_recon.recon()` 执行——
检索、有效文章判据、故障语义（故障 ≠ 无解）、7 天缓存全部复用，不另起一套。

落库（region 作用域的 ledger_kv）：
  - `forum_recon_<qkey>` / `forum_recon_negative_<qkey>` / `forum_recon_error_<qkey>`：问题本身的结局（`forum_recon.recon` 写）；
  - `forum_recon_wave_<wave>`：本波完成标记（本工具写）。**可靠结局**（有货 / 无解）占用本波额度，之后再调直接回放标记，不再查；
    **工具故障不占额度**（故障 ≠ 取证，修好后同一波应能重跑）；`--force` 忽略标记重跑。

用法：
  python tools/forum_recon_wave.py --region KOR --wave 97 [--dataset analyst4] [--force] [--dry-run]

退出码（与 `tools/forum_recon.py` 一致）：0 = 有货 / 本波没有需要问的问题 / 干跑；2 = 可靠的「论坛无解」；1 = 工具故障。
输出：最后一行是单行 JSON（`{"tool": "forum_recon_wave", ...}`），节点靠它取结构化结果。
干跑：`--dry-run` 只读库、派生问题并输出检索计划，零网络、零写库。

需要论坛可达与凭据（`CREDENTIALS_EMAIL` / `CREDENTIALS_PASSWORD` 或 MCP `.env`）；缺了是工具故障，不是「论坛无解」。
"""
from __future__ import annotations

import argparse
import json
import os
import sqlite3
import sys
import time
from typing import Any, Dict, List, Optional

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
for _p in (os.path.join(REPO_ROOT, "src"), os.path.dirname(os.path.abspath(__file__))):
    if _p not in sys.path:
        sys.path.insert(0, _p)

from wqb import db_conn  # noqa: E402
from wqb import recon_evidence as RE  # noqa: E402
from wqb import recon_wave as RW  # noqa: E402

import forum_recon as fr  # noqa: E402  同目录：检索 / 缓存 / 故障语义的唯一实现


# ---------------------------------------------------------------- 只读取数
def _table_columns(conn: sqlite3.Connection, table: str) -> set:
    return {r[1] for r in conn.execute(f"PRAGMA table_info({table})")}


def load_rows(db_path: str, region: str, wave: str, dataset: Optional[str] = None) -> List[Dict[str, Any]]:
    """本波的回测行（只读；库不存在 / 表缺失 → []）。同一 alpha 只留最新一行；prod 相关性取自 alphas（有则带上）。"""
    if not os.path.isfile(db_path):
        return []
    try:
        conn = db_conn.connect(db_path, readonly=True, row_factory=sqlite3.Row)
    except sqlite3.Error:
        return []
    try:
        cols = _table_columns(conn, "backtest_results")
        if not {"region", "wave", "sharpe"} <= cols:
            return []
        prod = "a.prod_correlation" if "prod_correlation" in _table_columns(conn, "alphas") else "NULL"
        join = "LEFT JOIN alphas a ON a.alpha_id = b.alpha_id" if prod != "NULL" else ""
        ra = "b.ra_failed_checks" if "ra_failed_checks" in cols else "NULL"
        ds = "b.dataset" if "dataset" in cols else "NULL"
        sql = (f"SELECT b.id AS id, b.alpha_id AS alpha_id, {ds} AS dataset, b.sharpe AS sharpe, "
               f"{ra} AS ra_failed_checks, {prod} AS prod_correlation "
               f"FROM backtest_results b {join} WHERE b.region = ? AND b.wave = ?")
        args: List[Any] = [region, str(wave)]
        if dataset and "dataset" in cols:
            sql += " AND b.dataset = ?"
            args.append(dataset)
        rows = [dict(r) for r in conn.execute(sql + " ORDER BY b.id", args)]
    except sqlite3.Error:
        return []
    finally:
        conn.close()
    latest: Dict[Any, Dict[str, Any]] = {}
    for i, r in enumerate(rows):
        latest[r["alpha_id"] if r["alpha_id"] else ("_row", i)] = r     # 同 alpha 后写覆盖先写
    return list(latest.values())


def load_ledger(db_path: str, region: str, key: str) -> Optional[Dict[str, Any]]:
    """读一条 ledger_kv（只读；不存在 / 解析失败 → None）。"""
    if not os.path.isfile(db_path):
        return None
    try:
        conn = db_conn.connect(db_path, readonly=True)
    except sqlite3.Error:
        return None
    try:
        row = conn.execute("SELECT value FROM ledger_kv WHERE region = ? AND key = ?", (region, key)).fetchone()
    except sqlite3.Error:
        return None
    finally:
        conn.close()
    if not row or not row[0]:
        return None
    try:
        v = json.loads(row[0]) if isinstance(row[0], (str, bytes)) else row[0]
    except ValueError:
        return None
    return v if isinstance(v, dict) else None


# ---------------------------------------------------------------- 主流程
def _exit_code(found: Optional[bool]) -> int:
    return 0 if found is True else 2 if found is False else 1


def run_wave(region: str, wave: Any, dataset: Optional[str] = None, *, db_path: str, force: bool = False,
             dry_run: bool = False, limit: int = 3, max_rounds: int = 8, recon_fn=None) -> Dict[str, Any]:
    """派生本波的决策问题并（在需要时）执行一次 recon。返回可直接 JSON 化的结果字典，`exit_code` 是建议退出码。"""
    recon_fn = recon_fn or fr.recon
    region, wave = str(region).strip(), str(wave).strip()
    rows = load_rows(db_path, region, wave, dataset)
    decision = RW.derive_decision(region, wave, rows, dataset)
    result: Dict[str, Any] = {
        "tool": "forum_recon_wave", "region": region, "wave": wave, "dataset": decision["dataset"] or dataset,
        "kind": decision["kind"], "wall": decision["wall"], "question": decision["question"],
        "question_key": decision["question_key"], "basis": decision["basis"], "dry_run": bool(dry_run),
        "skipped": False, "reason": decision["reason"], "found": None, "status": None, "exit_code": 0,
    }
    if decision["kind"] is None:                                        # 本波没有需要问论坛的问题——不查（不在触发表内）
        result.update(skipped=True, note="本波没有共同瓶颈可问（不在触发表内，不查论坛）")
        return result

    marker = load_ledger(db_path, region, RE.key_wave(wave))
    if RW.marker_blocks_rerun(marker) and not force:                    # 每波 ≤ 1 次：回放上次的可靠结局
        found = marker.get("found")
        result.update(skipped=True, reason=RW.SKIP_DONE, found=found, status=RW.marker_status(marker),
                      question=marker.get("question") or result["question"],
                      question_key=marker.get("question_key") or result["question_key"],
                      sink=marker.get("sink"), previous_done_at=marker.get("done_at"),
                      exit_code=_exit_code(found),
                      note="本波已取证（可靠结局占用本波额度）；--force 可忽略标记重跑")
        return result

    if dry_run:
        plan = recon_fn(decision["question"], decision["context"], "ledger", max(1, limit), max(1, max_rounds),
                        None, True, db_path)
        result.update(plan=(plan or {}).get("plan", plan), previous_marker_status=RW.marker_status(marker),
                      note="干跑：只读库派生问题并给出检索计划（零网络、零写库）")
        return result

    try:
        outcome = recon_fn(decision["question"], decision["context"], "ledger", max(1, limit), max(1, max_rounds),
                           None, False, db_path)
    except Exception as e:                                              # recon 自己已把故障记成 error；这里兜住未预期异常
        outcome = {"found": None, "status": RE.STATUS_ERROR, "error": f"未预期异常：{e}"}
    found = outcome.get("found")
    result.update(found=found, status=RE.status_of(found), sink=outcome.get("sink"),
                  from_cache=bool(outcome.get("from_cache")), n_useful=outcome.get("n_useful"),
                  exit_code=_exit_code(found))
    if found is None:
        result["error"] = outcome.get("error") or "论坛检索工具故障"
    marker_value = RW.build_marker(region, wave, decision, outcome, time.strftime("%Y-%m-%dT%H:%M:%S"), forced=force)
    try:
        fr._ledger_upsert(db_path, region, RE.key_wave(wave), marker_value)
        result["marker"] = f"{region}/{RE.key_wave(wave)}"
    except Exception as e:                                              # 标记没落成：如实报，下次会重查（多花一次，不会误占额度）
        result["marker_error"] = str(e)
    return result


def main(argv: Optional[List[str]] = None) -> int:
    ap = argparse.ArgumentParser(
        description="波级默认取证：对本波共同卡住的墙（或全灭时的「有无解法」）问一次论坛，每波 ≤ 1 次，结果落 ledger")
    ap.add_argument("--region", required=True, help="区域（如 KOR）")
    ap.add_argument("--wave", required=True, help="波号（整数或字符串波号，如 97 / s2_<ds>_d1）")
    ap.add_argument("--dataset", default=None, help="数据集；缺省取本波回测行里最多的那个")
    ap.add_argument("--force", action="store_true", help="忽略本波已有的完成标记，重新取证")
    ap.add_argument("--limit", type=int, default=3, help="目标有效文章数（透传 forum_recon，默认 3）")
    ap.add_argument("--max-search-rounds", type=int, default=8, help="防失控安全上限（透传 forum_recon，默认 8）")
    ap.add_argument("--db", default=None, help="DB 路径（缺省 WQB_DB_PATH / <repo>/data/wqb.db）")
    ap.add_argument("--dry-run", action="store_true", help="只读库、派生问题并输出检索计划，零网络零写库")
    a = ap.parse_args(argv)
    try:
        result = run_wave(a.region, a.wave, a.dataset, db_path=fr._db_path(a.db), force=a.force, dry_run=a.dry_run,
                          limit=a.limit, max_rounds=a.max_search_rounds)
    except Exception as e:
        print(f"[forum_recon_wave] 工具异常：{e}", file=sys.stderr)
        print(json.dumps({"tool": "forum_recon_wave", "found": None, "status": RE.STATUS_ERROR,
                          "error": str(e), "exit_code": 1}, ensure_ascii=False))
        return 1
    print(json.dumps(result, ensure_ascii=False))
    return int(result.get("exit_code", 0))


if __name__ == "__main__":
    import _pyenv  # noqa: E402  文档里写的是 `python tools/forum_recon_wave.py`——系统解释器缺 requests / bs4 时自动切到 MCP venv
    _pyenv.reexec_under_venv()
    sys.exit(main())
