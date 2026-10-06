#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""波级低覆盖字段 ts_backfill 修复器（幂等）。

背景（2026-10-02 GLB/model31 实战）：
  体检硬门规则1（覆盖率 <0.4 的字段必须有 ts_backfill）在**降级包/完整包**下都会生效。
  GEM 不会自动加 backfill → 波被 `[done] 体检硬门拦截 N 条违规候选` 拦下。

  修复动作 = 把低覆盖字段包成 `ts_backfill(f, N)`（标准预处理，不改信号经济含义）。
  需 backfill 的字段清单**直接读体检包的 advices**（`'低覆盖(x<0.4) → 必须含 ts_backfill(x, N)'`），
  不自己推覆盖率阈值，避免与闸口径漂移。

用法：
  python tools/fix_wave_backfill.py --region GLB --dataset model31 --wave s2_model31_d1            # 预览
  python tools/fix_wave_backfill.py --region GLB --dataset model31 --wave s2_model31_d1 --apply    # 落库

退出码：0 = 成功；1 = 无体检包/无成员；2 = 落库后仍有残留
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sqlite3
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
GATE_STATUSES = ("gem", "selected")


def _pack_path(region: str, dataset: str) -> Path:
    return REPO / "tracking" / "mining" / f"field_inspect_{region.lower()}_{dataset}.json"


def _need_backfill(region: str, dataset: str) -> list[str]:
    p = _pack_path(region, dataset)
    if not p.exists():
        raise SystemExit(f"[ERR] 体检包不存在：{p}（先跑 tools/gen_inspect_from_db.py --region {region} --dataset {dataset}）")
    pack = json.loads(p.read_text(encoding="utf-8"))
    fmap = pack.get("fields", {}).get(dataset, {})
    need = [k for k, v in fmap.items() if any("ts_backfill" in a for a in (v.get("advices") or []))]
    return sorted(need, key=len, reverse=True)


def _wrap_backfill(expr: str, fields: list[str], window: int = 66) -> tuple[str, list[str]]:
    """把低覆盖字段包成 ts_backfill(f, window)。幂等（已包的不动）。"""
    if not fields:
        return expr, []
    new = expr
    wrapped = []
    for f in fields:  # 已按长度降序，防前缀互吞
        pat = re.compile(r"(?<![A-Za-z0-9_])" + re.escape(f) + r"(?![A-Za-z0-9_])")
        out, last, hit = [], 0, False
        for m in pat.finditer(new):
            # 已裹过（前面紧邻 ts_backfill( 或 group_backfill(）→ 跳过
            prefix = new[max(0, m.start() - 20):m.start()]
            if re.search(r"(?:ts|group)_backfill\($", prefix):
                continue
            out.append(new[last:m.start()])
            out.append(f"ts_backfill({f}, {window})")
            last = m.end()
            hit = True
        out.append(new[last:])
        if hit:
            new = "".join(out)
            wrapped.append(f)
    return new, wrapped


def _db_path(cli: str | None) -> str:
    return cli or os.environ.get("WQB_DB_PATH") or str(REPO / "data" / "wqb.db")


def main() -> int:
    ap = argparse.ArgumentParser(description="波级低覆盖字段 ts_backfill 修复器")
    ap.add_argument("--region", required=True)
    ap.add_argument("--dataset", required=True)
    ap.add_argument("--wave", required=True)
    ap.add_argument("--window", type=int, default=66)
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--db", default=None)
    a = ap.parse_args()

    fields = _need_backfill(a.region, a.dataset)
    print(f"[pack] 需 backfill 字段 {len(fields)} 个")
    if not fields:
        print("[done] 本集无低覆盖字段，无需修复")
        return 0

    con = sqlite3.connect(_db_path(a.db))
    cur = con.cursor()
    ph = ",".join("?" * len(GATE_STATUSES))
    cur.execute(
        f"SELECT id, expression FROM expressions WHERE wave=? AND region=? AND status IN ({ph}) ORDER BY id",
        (a.wave, a.region, *GATE_STATUSES),
    )
    rows = cur.fetchall()
    print(f"[db]   {a.region}/{a.wave} 成员={len(rows)}")
    if not rows:
        print("[WARN] 无成员，检查 region/wave")
        return 1

    fixed, changed, hits = [], 0, set()
    for aid, expr in rows:
        new, wf = _wrap_backfill(expr, fields, a.window)
        if wf:
            changed += 1
            hits.update(wf)
        fixed.append((aid, expr, new))

    print(f"[fix]  需修 {changed}/{len(rows)}；命中字段 {len(hits)} 个")
    for f in sorted(hits):
        print(f"        - {f}")
    if changed == 0:
        print("[done] 无需修复（幂等通过）")
        return 0
    for aid, old, new in fixed:
        if old != new:
            print(f"[样例] #{aid}\n  old: {old[:110]}\n  new: {new[:110]}")
            break

    if not a.apply:
        print("[dry-run] 未落库；加 --apply 生效")
        return 0

    for aid, _o, new in fixed:
        cur.execute("UPDATE expressions SET expression=?, updated_at=datetime('now') WHERE id=?", (new, aid))
    con.commit()

    cur.execute(
        f"SELECT id, expression FROM expressions WHERE wave=? AND region=? AND status IN ({ph}) ORDER BY id",
        (a.wave, a.region, *GATE_STATUSES),
    )
    resid = [i for i, e in cur.fetchall() if _wrap_backfill(e, fields, a.window)[1]]
    con.close()
    print(f"[apply] 已落库 {len(fixed)} 条；残留 {len(resid)} 条")
    return 2 if resid else 0


if __name__ == "__main__":
    raise SystemExit(main())
