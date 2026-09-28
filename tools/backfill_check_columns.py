# -*- coding: utf-8 -*-
"""backfill_check_columns.py — 回填 checks 派生列（cluster_test / concentrated_weight 等）。

背景（2026-09-19 实测）：`tools/harvest_multisim.py::_pick_checks` 此前找的 4 条路径
（`data.checks` / `data.raw.checks` / `data.raw.is.checks`）**全部落空**，
而真实位置是**顶层 `is.checks`** → 该函数恒返回 `[]` → 所有 checks 派生列采集不到：

| 列 | 填充率（修复前）|
|---|---|
| `alphas.cluster_test` | **0 / 4,926** |
| `alphas.concentrated_weight` | **0 / 4,926** |
| `alphas.sub_universe_sharpe` | 8.3%（该列另有直读 `is.subUniverseSharpe` 路径）|

取值路径已修（见 `_pick_checks`）；本工具用平台详情把存量补齐。
证据：IND/QPGbAOn5 的 `is.checks` 含 `{name: CLUSTER_TEST, result: PASS, limit: 1, value: 2.59}`。

行为：**只填 NULL**（幂等，重跑零变化）；断点续跑（state 文件）；默认 dry-run。

用法（需 MCP venv 的 Python）：
  world-quant-brain-mcp/.venv/Scripts/python.exe tools/backfill_check_columns.py            # 预览
  world-quant-brain-mcp/.venv/Scripts/python.exe tools/backfill_check_columns.py --apply
  ... --scope active            # 只补 platform_status='ACTIVE'（默认）
  ... --scope all --limit 500   # 全量（按 fitness 降序），可断点续跑
"""
import argparse
import asyncio
import json
import os
import shutil
import sqlite3
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MCP_DIR = os.path.join(REPO, "world-quant-brain-mcp")
DB = os.path.join(REPO, "data", "wqb.db")
STATE = os.path.join(REPO, "logs", "_backfill_check_columns_state.json")
sys.path.insert(0, MCP_DIR)
sys.path.insert(0, os.path.join(REPO, "tools"))

#: 要回填的列 → 取值方式（checks 名 / is 直读键）
CHECK_COLS = {
    "cluster_test": ("checks", "CLUSTER_TEST"),
    "concentrated_weight": ("checks", "CONCENTRATED_WEIGHT"),
    "sub_universe_sharpe": ("checks", "LOW_SUB_UNIVERSE_SHARPE"),
}


def pick_targets(scope, limit):
    conn = sqlite3.connect(DB)
    where = "alpha_id IS NOT NULL"
    if scope == "active":
        where += " AND platform_status='ACTIVE'"
    sql = (f"SELECT alpha_id FROM alphas WHERE {where} "
           f"AND (cluster_test IS NULL OR concentrated_weight IS NULL "
           f"     OR sub_universe_sharpe IS NULL) "
           f"ORDER BY (fitness IS NULL), fitness DESC")
    if limit:
        sql += f" LIMIT {int(limit)}"
    rows = [r[0] for r in conn.execute(sql)]
    conn.close()
    return rows


def load_state():
    try:
        with open(STATE, encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {"done": [], "filled": 0}


def save_state(st):
    with open(STATE, "w", encoding="utf-8") as f:
        json.dump(st, f, ensure_ascii=False, indent=1)


def apply_rows(rows):
    conn = sqlite3.connect(DB)
    conn.execute("BEGIN")
    for aid, vals in rows:
        sets, params = [], []
        for col, v in vals.items():
            sets.append(f"{col}=COALESCE({col}, ?)")
            params.append(v)
        if sets:
            conn.execute(f"UPDATE alphas SET {', '.join(sets)} WHERE alpha_id=?", params + [aid])
    conn.commit()
    conn.close()


async def main():
    ap = argparse.ArgumentParser(description="回填 checks 派生列（只填 NULL，幂等）")
    ap.add_argument("--scope", default="active", choices=("active", "all"))
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--apply", action="store_true", help="实际写库（缺省只预览）")
    ap.add_argument("--db-backup", default=None, help="可选：写库前备份 DB 到该路径")
    ap.add_argument("--sleep", type=float, default=0.15, help="每次请求间隔秒")
    ap.add_argument("--fresh", action="store_true", help="忽略 state 从头跑")
    a = ap.parse_args()

    targets = pick_targets(a.scope, a.limit)
    state = {"done": [], "filled": 0} if a.fresh else load_state()
    done = set(state.get("done") or [])
    todo = [t for t in targets if t not in done]
    print(f"目标 {len(targets)} 条（scope={a.scope}）｜已完成 {len(done)}｜本次待补 {len(todo)}")
    if not todo:
        print("无待补（幂等：全部已有值或已处理）")
        return

    if a.apply and a.db_backup:
        if os.path.exists(a.db_backup):
            raise SystemExit(f"[拒绝] 备份目标已存在：{a.db_backup}")
        shutil.copy2(DB, a.db_backup)
        print(f"[备份] {DB} → {a.db_backup}")

    from brain_api import brain_client
    import harvest_multisim as H
    await brain_client.ensure_authenticated()

    pending_writes, hits = [], []
    for i, aid in enumerate(todo, 1):
        try:
            d = await brain_client.get_alpha_details(aid)
        except Exception as e:
            print(f"[{i}/{len(todo)}] {aid} 取详情失败 {type(e).__name__}")
            await asyncio.sleep(a.sleep)
            continue
        if not d:
            print(f"[{i}/{len(todo)}] {aid} 详情空")
            await asyncio.sleep(a.sleep)
            continue
        checks = H._pick_checks(d)
        isd = d.get("is") or {}
        vals = {}
        for col, (src, name) in CHECK_COLS.items():
            if src == "checks":
                v = H._extract_check_value(checks, name)
                if v is None and col == "sub_universe_sharpe":
                    v = isd.get("subUniverseSharpe")
            if v is not None:
                vals[col] = float(v)
        if vals:
            pending_writes.append((aid, vals))
            if "cluster_test" in vals:
                hits.append((aid, vals["cluster_test"],
                             (d.get("settings") or {}).get("region")))
        print(f"[{i}/{len(todo)}] {aid} → {vals}")
        done.add(aid)
        state["done"] = sorted(done)
        # 只在真正写库时持久化 checkpoint —— dry-run 不得把条目标记为"已处理"
        if a.apply and i % 10 == 0:
            save_state(state)
        await asyncio.sleep(a.sleep)

    save_state(state)
    print(f"\n可回填 {len(pending_writes)} 条｜其中带 CLUSTER_TEST {len(hits)} 条")
    for aid, v, reg in hits[:30]:
        print(f"   ★ {reg} {aid} cluster_test={v}")

    if not a.apply:
        print("\n[dry-run] 未写库。确认后加 --apply。")
        return
    apply_rows(pending_writes)
    conn = sqlite3.connect(DB)
    for col in CHECK_COLS:
        n = conn.execute(f"SELECT COUNT({col}) FROM alphas").fetchone()[0]
        tot = conn.execute("SELECT COUNT(*) FROM alphas").fetchone()[0]
        print(f"  {col:<22} {n}/{tot} ({n/tot*100:.1f}%)")
    conn.close()


asyncio.run(main())
