#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""波级 VECTOR 字段 vec_* 包裹修复器（幂等）。

背景（2026-10-02 GLB analyst69 实战）：
  混合数据集（type_distribution 同时含 VECTOR 与 MATRIX）由 GEM 生成时，
  若 data_type 取 catalog rollup = VECTOR，则候选会**裸用** VECTOR 字段，
  撞 gate 闸3 `[EVENT] 事件型字段必须经 vec_* 聚合` 整波全灭。

  修这个闸时有两个必须避开的坑（本工具就是为了固化它们）：

  ★ 坑1：字段知识源必须用 **typed catalog**（`_lib/wqb_store.load_catalog`），
    与 gate 闸3 判定同源。实测另两个源都是错的：
      - MCP `fix_vector_fields` 回包的 vector_fields：**只有 300 个**，
        缺 anl69_roes_* / anl69_cps_* / bps_market_status 等整族 → 修完仍 17 条红。
      - 本地 `fields` 表：**该集 0 行**，根本不是源。
    catalog 实测 779 字段 / VECTOR 515 → 一次修完 all_pass。

  ★ 坑2：**波成员口径必须与 gate 完全一致** = `status IN ('gem','selected')`。
    该波 DB 里共 1123 行，其余是 superseded/dropped；只修自己新生成的 42 条
    ⇒ 剩余 17 条 selected 旧式仍红，gate 永远 PASS 不了。

用法：
  # 预览（不改库）
  python tools/fix_wave_vectors.py --campaign-dir tracking/GLB --region GLB \\
      --dataset analyst69 --wave s2_analyst69_d1

  # 落库
  python tools/fix_wave_vectors.py ... --apply

退出码：0 = 成功（含"无需修复"）；1 = 参数/环境错误；2 = 修复后仍有残留。
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

# gate 校验的波成员状态口径（必须与之逐字一致，见模块 docstring 坑2）
GATE_STATUSES = ("gem", "selected")


def _resolve_catalog(campaign_dir: str, dataset: str) -> dict:
    """用 typed catalog（与 gate 闸3 同源）取字段类型。"""
    scripts = REPO / "Claude" / "skills" / "wq-brain-campaign-toolkit" / "scripts"
    sys.path.insert(0, str(scripts))
    from _lib.common import CampaignContext  # noqa: E402
    from _lib.wqb_store import load_catalog  # noqa: E402

    ctx = CampaignContext(campaign_dir)
    d = load_catalog(ctx, dataset)
    if not d or not d.get("fields"):
        raise SystemExit(f"[ERR] catalog 无字段：{campaign_dir} / {dataset}")
    return d


def _wrap_impl():
    """仓库权威包裹实现（禁从安装位 import，见 RULES 跨目录定位）。"""
    sys.path.insert(0, str(REPO / "tools"))
    from lib.vector_wrap import wrap_naked_vectors  # noqa: E402

    return wrap_naked_vectors


def _db_path() -> str:
    env = os.environ.get("WQB_DB_PATH")
    if env:
        return env
    return str(REPO / "data" / "wqb.db")


def main() -> int:
    ap = argparse.ArgumentParser(description="波级 VECTOR 字段 vec_* 包裹修复器")
    ap.add_argument("--campaign-dir", required=True)
    ap.add_argument("--region", required=True)
    ap.add_argument("--dataset", required=True)
    ap.add_argument("--wave", required=True)
    ap.add_argument("--apply", action="store_true", help="不传则只预览")
    ap.add_argument("--db", default=None, help="覆盖 DB 路径（默认 WQB_DB_PATH 或 data/wqb.db）")
    a = ap.parse_args()

    catalog = _resolve_catalog(a.campaign_dir, a.dataset)
    fts = {f["id"]: f.get("type") for f in catalog["fields"]}
    vec_all = sorted(f for f, t in fts.items() if str(t).upper() == "VECTOR")
    wrap = _wrap_impl()

    db = a.db or _db_path()
    con = sqlite3.connect(db)
    cur = con.cursor()
    ph = ",".join("?" * len(GATE_STATUSES))
    cur.execute(
        f"SELECT id, expression FROM expressions "
        f"WHERE wave=? AND region=? AND status IN ({ph}) ORDER BY id",
        (a.wave, a.region, *GATE_STATUSES),
    )
    rows = cur.fetchall()

    print(f"[catalog] fields={len(fts)} VECTOR={len(vec_all)} data_type={catalog.get('data_type')}")
    print(f"[db]      {a.region}/{a.wave} 成员(status={'/'.join(GATE_STATUSES)})={len(rows)}")
    if not rows:
        print("[WARN] 该波无成员，检查 region/wave 拼写")
        return 1

    fixed, changed, wrapped_fields = [], 0, set()
    for aid, expr in rows:
        new, wf = wrap(expr, vec_all)
        if wf:
            changed += 1
            wrapped_fields.update(wf)
        fixed.append((aid, expr, new))

    print(f"[wrap]    需修 {changed}/{len(rows)}；涉及字段 {len(wrapped_fields)} 个")
    for f in sorted(wrapped_fields):
        print(f"          - {f}")
    if changed == 0:
        print("[done] 无需修复（幂等通过）")
        return 0

    print("[样例]")
    for aid, old, new in fixed:
        if old != new:
            print(f"  #{aid}\n    old: {old[:110]}\n    new: {new[:110]}")
            break

    if not a.apply:
        print("[dry-run] 未落库；加 --apply 生效")
        return 0

    for aid, _old, new in fixed:
        cur.execute(
            "UPDATE expressions SET expression=?, updated_at=datetime('now') WHERE id=?",
            (new, aid),
        )
    con.commit()

    # 残留核验：再用同一 catalog 复查（幂等应 0）
    cur.execute(
        f"SELECT id, expression FROM expressions "
        f"WHERE wave=? AND region=? AND status IN ({ph}) ORDER BY id",
        (a.wave, a.region, *GATE_STATUSES),
    )
    resid = [(i, e) for i, e in cur.fetchall() if wrap(e, vec_all)[1]]
    con.close()
    print(f"[apply]   已落库 {len(fixed)} 条；残留仍需修 {len(resid)} 条")
    if resid:
        for i, e in resid[:5]:
            print(f"          ! #{i} {e[:100]}")
        return 2
    print("[done] 修复完成，可重跑 wave_gate 核验")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
