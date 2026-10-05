#!/usr/bin/env python
"""收割 multisim 并按表达式反解参数，输出 F 缺口。

为什么不用 tools/harvest_multisim.py：
    它的 alpha_id 按 child 顺序打印，与 expressions 表行序不一致 ⇒ 结论性判断必须
    从 `/alphas/{id}` 的 `regular.code` 反解参数（见 MEMORY §1.10b）。

用法:
    python tools/harvest_by_expr.py <sim_id> [<sim_id> ...] [--persist WAVE] [--region GBR]

输出列: alpha_id | 表达式核心参数 | S | F | margin | TO | 2Y | failed_ra | F 缺口
"""
from __future__ import annotations

import argparse
import asyncio
import json
import re
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "world-quant-brain-mcp"))

# 表达式核心参数抽取（按需扩）
EXTRACTORS = [
    ("tvr", re.compile(r"target_tvr=([\d.]+)")),
    ("lmin", re.compile(r"lambda_min=([\d.]+)")),
    ("lmax", re.compile(r"lambda_max=([\d.]+)")),
    ("bf", re.compile(r"ts_backfill\([^,]+,\s*(\d+)\)")),
    ("win", re.compile(r"ts_delta\([^)]*?\),\s*(\d+)\)")),
    ("axis", re.compile(r"\),\s*(sector|industry|subindustry|country|market)\)")),
    ("field", re.compile(r"ts_backfill\(([a-z0-9_]+)")),
]


def core(code: str) -> str:
    parts = []
    for name, rx in EXTRACTORS:
        m = rx.search(code or "")
        if m:
            parts.append(f"{name}={m.group(1)}")
    return " ".join(parts)


def f_gap_bp(sharpe, margin) -> float:
    """F>=1.0 所需的 margin 与实际 margin 之差（bp）。S<=0 或 margin 缺失时返回 nan。"""
    if not sharpe or margin is None:
        return float("nan")
    return (1.0 / (504.0 * sharpe * sharpe) - margin) * 1e4


async def run(sim_ids: list[str], wave: str, region: str, dataset: str = "") -> list[dict]:
    from brain_api import brain_client

    await brain_client.ensure_authenticated()
    rows: list[dict] = []

    for sim in sim_ids:
        head = (await brain_client._request("GET", f"/simulations/{sim}")).json()
        children = head.get("children") or []
        print(f"\n[{sim}] status={head.get('status')} children={len(children)}")
        for c in children:
            cj = (await brain_client._request("GET", f"/simulations/{c}")).json()
            aid = cj.get("alpha")
            if not aid:
                print(f"  - {c[:10]} {cj.get('status')} {(cj.get('message') or '')[:80]}")
                continue
            a = (await brain_client._request("GET", f"/alphas/{aid}")).json()
            m = a.get("is") or {}
            reg = a.get("regular")
            code = reg.get("code") if isinstance(reg, dict) else (reg or "")
            ra = a.get("ra") or {}
            gap = f_gap_bp(m.get("sharpe"), m.get("margin"))
            row = {
                "alpha_id": aid, "sim": sim, "core": core(code), "code": code,
                "sharpe": m.get("sharpe"), "fitness": m.get("fitness"),
                "margin": m.get("margin"), "turnover": m.get("turnover"),
                "two_year": m.get("twoYearSharpe"), "sub": m.get("subUniverseSharpe"),
                "drawdown": m.get("drawdown"), "ra_failed": ra.get("failed_ra_count"),
                "f_gap_bp": gap,
            }
            rows.append(row)
            mark = "*** F>=1.0" if (m.get("fitness") or 0) >= 1.0 else ""
            print(f"  + {aid} [{row['core']}] S={m.get('sharpe')} F={m.get('fitness')} "
                  f"m={(m.get('margin') or 0)*1e4:.2f}bp TO={m.get('turnover')} "
                  f"2Y={m.get('twoYearSharpe')} raFail={ra.get('failed_ra_count')} "
                  f"gap={gap:+.2f}bp {mark}")
            time.sleep(1.0)  # 平台限流：连发 9 次 GET /alphas/{id} 即 rate limit

    if wave:
        import sqlite3
        db = sqlite3.connect(ROOT / "data" / "wqb.db")
        cur = db.cursor()
        # 2026-10-05 修正 2：dataset 名不再硬编码 "model53"。优先用 --dataset 传入；
        # 否则从表达式里的字段名反查 `datasets`（fields → datasets 唯一命中时采用）。
        ds_name = dataset
        if not ds_name:
            import re as _re
            cands = set()
            for r in rows:
                for f in _re.findall(r"[a-z][a-z0-9_]{4,}", r.get("code") or ""):
                    cur.execute("SELECT d.name FROM fields fl JOIN datasets d ON d.id=fl.dataset_id"
                                " WHERE d.region_id=(SELECT id FROM regions WHERE name=?)"
                                " AND fl.field_name=? LIMIT 1", (region, f))
                    _h = cur.fetchone()
                    if _h:
                        cands.add(_h[0])
            ds_name = (sorted(cands)[0] if len(cands) == 1
                       else ("+".join(sorted(cands)) if cands else "unknown"))
        # 2026-10-05 修正：原先硬编码 {"GBR": 7, "IND": 5, ...}，被
        # test_region_control_ratchets::test_no_new_region_literal_branches 判红
        # （§8.14「区域差异写数据，不写代码分支」）。改为查 regions 表——
        # 区域码 → region_id 是数据，不是代码。
        cur.execute("SELECT id FROM regions WHERE name=?", (region,))
        _row = cur.fetchone()
        if not _row:
            raise SystemExit(
                f"[harvest_by_expr] 区域 {region!r} 不在 regions 表，拒绝入库"
                f"（硬编码映射表在新增区域时会静默写错region_id）"
            )
        rid = _row[0]
        cur.execute("INSERT OR IGNORE INTO waves (region_id, wave_number, dataset_id,"
                    " expression_count, status, created_at, updated_at)"
                    " VALUES (?,?,?,?,'completed',datetime('now'),datetime('now'))",
                    (rid, wave, ds_name, len(rows)))
        cur.execute("SELECT id FROM waves WHERE region_id=? AND wave_number=?", (rid, wave))
        wid = cur.fetchone()[0]
        for r in rows:
            cur.execute("SELECT alpha_id FROM alphas WHERE alpha_id=?", (r["alpha_id"],))
            vals = (r["code"], r["sharpe"], r["fitness"], r["margin"], r["turnover"],
                    r["two_year"], r["sub"], r["drawdown"], r["alpha_id"])
            if cur.fetchone():
                cur.execute("UPDATE alphas SET expression=?,sharpe=?,fitness=?,margin=?,"
                            " turnover=?,two_year_sharpe=?,sub_universe_sharpe=?,drawdown=?,"
                            " updated_at=datetime('now') WHERE alpha_id=?", vals)
            else:
                cur.execute("INSERT INTO alphas (alpha_id,expression,region_id,dataset_id,"
                            " universe,delay,neutralization,sharpe,fitness,margin,turnover,"
                            " two_year_sharpe,sub_universe_sharpe,drawdown,status,created_at,updated_at)"
                            " VALUES (?,?,?,?,'TOP700',1,'STATISTICAL',?,?,?,?,?,?,?,"
                            " 'UNSUBMITTED',datetime('now'),datetime('now'))",
                            (r["alpha_id"], r["code"], rid, ds_name) + vals[1:-1])
            cur.execute("INSERT INTO expressions (wave_id,expression,status,alpha_id,sharpe,"
                        " fitness,margin,turnover,region,wave,dataset,created_at,updated_at)"
                        " VALUES (?,?,'backtested',?,?,?,?,?,?,?,?,datetime('now'),datetime('now'))",
                        (wid, r["code"], r["alpha_id"], r["sharpe"], r["fitness"],
                         r["margin"], r["turnover"], region, wave, ds_name))
        db.commit()
        db.close()
        print(f"\n[DB] persisted wave={wave} rows={len(rows)}")

    out = ROOT / "cache" / f"byexpr_{wave or 'latest'}.json"
    out.write_text(json.dumps(rows, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"[OUT] {out}")
    return rows


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("sim_ids", nargs="+")
    ap.add_argument("--persist", default="", help="写入 DB 的 wave 名")
    ap.add_argument("--region", default="GBR")
    ap.add_argument("--dataset", default="", help="数据集名（缺省则从表达式字段反查）")
    a = ap.parse_args()
    asyncio.run(run(a.sim_ids, a.persist, a.region, a.dataset))


if __name__ == "__main__":
    main()
