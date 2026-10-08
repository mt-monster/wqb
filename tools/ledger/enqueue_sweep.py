# -*- coding: utf-8 -*-
"""漏盘兜底扫描：本地可交付 alpha 一律补入 submit_ready（可交付必入）。

背景（2026-10-08 用户指令）：用户后续都从 submit_ready 取当日候选比较提交，
因此「挖掘出可交付的 alpha 后一定要入 submit_ready」。正常链路各有自动入队：
  - 收批：`tools/harvest_multisim.py --auto-upsert`（默认开）→ enqueue_from_alphas
  - 业绩极致优化：`tools/perf_max.py report`（默认开）/ `enqueue`
本工具是**事后兜底**（harvest_multisim 报错信息里承诺的 enqueue_sweep）：
扫本地 alphas/backtest_results，把「可交付但不在 submit_ready」的漏网补上。

可交付判定 = `wqb.store.submit_queue.is_pass`（阈值单源在 store/config，本工具零复写）：
IS 指标过线 + 最新 backtest 的 ra_failed_checks 为空 + 非 add 混腿。

⚠ 盘点盲区：本工具只扫**本地 SQLite**。「平台有、本地无」的 alpha（perf_max /
  MCP 直拉产出）扫不到，须用补录通道：
      python tools/submit_queue.py add --alpha-id <ID> [ID ...]
（补录后同样有列填充审计输出。）

用法
----
  python tools/enqueue_sweep.py                 # 全区域扫描并入队（commit）
  python tools/enqueue_sweep.py --region USA    # 限定区域
  python tools/enqueue_sweep.py --dry-run       # 演练不落盘
"""
from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path as _Path
from typing import Any, Dict, List, Optional


def _bootstrap_src():
    for _p in _Path(__file__).resolve().parents:
        if (_p / "pyproject.toml").exists() and (_p / "src" / "wqb").is_dir():
            _s = str(_p / "src")
            if _s not in sys.path:
                sys.path.insert(0, _s)
            return
    raise RuntimeError("repo root not found (pyproject.toml + src/wqb)")


_bootstrap_src()


def _latest_ra_fails(con, alpha_id: str) -> List[str]:
    row = con.execute(
        "SELECT ra_failed_checks FROM backtest_results WHERE alpha_id=? "
        "ORDER BY id DESC LIMIT 1", (alpha_id,)).fetchone()
    if not row or not row[0]:
        return []
    import ast as _ast
    import json as _json
    raw = row[0]
    if not isinstance(raw, str):
        return [str(x) for x in (raw or [])]
    for parser in (_json.loads, _ast.literal_eval):
        try:
            v = parser(raw.strip())
            return [str(x) for x in (v or [])]
        except Exception:
            continue
    # 非空但无法解析 → 保守视为有失败（宁可漏入队不可错入队，且不静默）
    return ["UNPARSED_RA_FAILS"]


def _latest_risk_neutralized(con, alpha_id: str) -> Optional[float]:
    row = con.execute(
        "SELECT risk_neutralized_sharpe FROM backtest_results WHERE alpha_id=? "
        "ORDER BY id DESC LIMIT 1", (alpha_id,)).fetchone()
    return row[0] if row else None


def find_deliverables(con, region: Optional[str] = None) -> List[Dict[str, Any]]:
    """返回本地库里「可交付且不在 submit_ready」的候选记录列表（未写入）。"""
    from wqb.store import submit_queue as sq
    sq.ensure_table(con)
    q = """SELECT a.*, r.name AS region FROM alphas a LEFT JOIN regions r ON a.region_id = r.id
           WHERE a.alpha_id IS NOT NULL AND a.alpha_id <> ''
             AND COALESCE(a.soft_deleted,0)=0
             AND COALESCE(a.disposition,'') <> 'DEAD'
             AND a.status IN ('UNSUBMITTED','COMPLETE')
             AND COALESCE(a.platform_status,'') NOT IN ('ACTIVE','DECOMMISSIONED')
             AND a.date_submitted IS NULL"""
    ps: List[Any] = []
    if region:
        q += " AND r.name = ?"
        ps.append(region)
    out: List[Dict[str, Any]] = []
    for row in con.execute(q, ps).fetchall():
        if not row["region"]:
            continue
        aid = row["alpha_id"]
        exists = con.execute(
            "SELECT 1 FROM submit_ready WHERE alpha_id=? AND region=?",
            (aid, row["region"])).fetchone()
        if exists:
            continue
        ra_fails = _latest_ra_fails(con, aid)
        two_year = row["two_year_sharpe"]
        if two_year is None:
            two_year = row["is_ladder_sharpe"]   # 2Y 读数随区域换检查项（IND 用 ladder）
        ok, why = sq.is_pass(row["sharpe"], row["fitness"], two_year, row["turnover"],
                             row["prod_correlation"], row["self_correlation"],
                             ra_fails, row["expression"])
        if not ok:
            continue
        out.append({
            "alpha_id": aid, "region": row["region"],
            "universe": row["universe"], "delay": row["delay"], "decay": None,
            "neutralization": row["neutralization"],
            "expr": row["expression"], "alpha_type": row["alpha_type"],
            "sharpe": row["sharpe"], "fitness": row["fitness"],
            "turnover": row["turnover"], "two_year": two_year,
            "sub_universe": row["sub_universe_sharpe"],
            "cluster_test": row["cluster_test"],
            "margin": row["margin"], "returns": row["returns"],
            "drawdown": row["drawdown"],
            "long_count": row["long_count"], "short_count": row["short_count"],
            "investability_constrained_sharpe": None,   # alphas 表无此列
            "risk_neutralized_sharpe": _latest_risk_neutralized(con, aid),
            "prod": row["prod_correlation"], "self": row["self_correlation"],
            "towers": "[]",                              # 本地库无塔列（补录走 add）
            "family": sq.family_of_expr(row["expression"]),
        })
    return out


def run(region: Optional[str] = None, db_path: Optional[str] = None,
        dry_run: bool = False) -> int:
    from wqb.store import submit_queue as sq
    con = sq.connect(db_path)
    try:
        recs = find_deliverables(con, region)
        print(f"[sweep] is_pass 命中且未入队 = {len(recs)}"
              + (f"（region={region}）" if region else "（全区域）")
              + "（最终 gate 以入队判定为准：兄弟 prod 连坐 / PENDING 会转 DEAD 或 IS_ONLY）")
        for rec in recs:
            gate = sq.enqueue(con, rec, note="enqueue_sweep 漏盘补入")
            missing = sq.column_fill_audit(con, rec["alpha_id"], rec["region"]) or []
            print(f"  {rec['alpha_id']} [{rec['region']}] sh={rec['sharpe']} "
                  f"fit={rec['fitness']} → {gate}"
                  + (f" 未填列: {','.join(missing)}" if missing else " 列填充完整"))
        if dry_run:
            con.rollback()
            print("[sweep] dry-run，未写入")
        else:
            con.commit()
            print(f"[sweep] 已写入 {len(recs)} 条")
        print("[sweep] 提醒：平台有、本地无的 alpha 本扫描覆盖不到，"
              "用 `python tools/submit_queue.py add --alpha-id <ID>` 补录")
        return 0
    finally:
        con.close()


def main(argv: Optional[List[str]] = None) -> int:
    p = argparse.ArgumentParser(description="漏盘兜底：可交付 alpha 补入 submit_ready")
    p.add_argument("--region", help="限定区域")
    p.add_argument("--db-path", help="测试用库路径（默认正式库）")
    p.add_argument("--dry-run", action="store_true", help="演练不落盘")
    a = p.parse_args(argv)
    return run(region=a.region, db_path=a.db_path, dry_run=a.dry_run)


if __name__ == "__main__":
    sys.exit(main())
