# -*- coding: utf-8 -*-
"""normalize_wave_ids.py — 回填裸时间戳波号（2026-09-17 P2-6）。

## 为什么需要
实测 `expressions.wave` 有 **20 行裸 Unix 时间戳**（全部 DEU / `analyst93` /
`status='gated'`），成因是写入方在未给波号时用 `time.time()` 顶替。
写入侧护栏已加（`tools/mcp_batch_writer.py::_normalize_wave`），存量需一并收口。

**影响的准确表述**（推翻审计原文）：这**不影响**信号天花板闸 —— 该闸读的是
`backtest_results.wave`（DEU 该表无时间戳，实测 `batches=2 / max_sh=1.7 / ok`）。
真实影响是 5 个无名"波"混入波级统计，使 DEU 看起来存在从未命名过的波次。

## 归一契约
    <裸 epoch 秒>  ->  unlabeled_<dataset>_<ts>
刻意**不**猜真实波号（如 `s2_analyst93_d1`）——那属于编造历史。
保留原时间戳使映射可逆，`unlabeled_` 前缀让问题自曝而非被掩盖。

## 安全设计
- **默认 dry-run**：不加 `--apply` 只打印计划，绝不写库。
- **幂等**：已是 `unlabeled_` 前缀的行直接跳过。
- **可回滚**：`--db-backup` 先做文件级备份；映射表落盘 `logs/wave_id_migration_<ts>.json`。
- **断点续跑**：状态写 `logs/_state_normalize_wave_ids.json`（原子写）。
- 只改 `wave` 一列，**保留 `id` / `created_at`** 原始追溯链。

用法：
    python tools/normalize_wave_ids.py                      # dry-run
    python tools/normalize_wave_ids.py --db-backup --apply  # 备份后写库
"""
from __future__ import annotations

import argparse
import json
import os
import shutil
import sqlite3
import sys
from datetime import datetime

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC_DIR = os.path.join(REPO_ROOT, "src")
if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

from wqb.wave_id import normalize_wave_id, wave_kind  # noqa: E402

STATE_PATH = os.path.join(REPO_ROOT, "logs", "_state_normalize_wave_ids.json")
TABLES = ("expressions", "backtest_results")


def resolve_db_path() -> str:
    try:
        from wqb.workflow._common import resolve_db_path as _r
        return _r()
    except Exception:
        return os.path.join(REPO_ROOT, "data", "wqb.db")


def load_state(fresh=False):
    if fresh or not os.path.isfile(STATE_PATH):
        return {"done": [], "updated_at": None}
    try:
        with open(STATE_PATH, "r", encoding="utf-8") as f:
            st = json.load(f)
        st.setdefault("done", [])
        return st
    except Exception:
        return {"done": [], "updated_at": None}


def save_state(state):
    state["updated_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    os.makedirs(os.path.dirname(STATE_PATH), exist_ok=True)
    tmp = STATE_PATH + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)
    os.replace(tmp, STATE_PATH)


def scan(conn) -> list:
    """返回待归一行：[(table, id_col, row_id, region, dataset, old_wave, new_wave)]"""
    todo = []
    for tbl in TABLES:
        cols = {r[1] for r in conn.execute(f"pragma table_info({tbl})")}
        if "wave" not in cols:
            continue
        id_col = "alpha_id" if "alpha_id" in cols and tbl == "backtest_results" else "id"
        ds_expr = "dataset" if "dataset" in cols else "NULL"
        q = (f"SELECT {id_col}, region, {ds_expr}, wave FROM {tbl} "
             f"WHERE wave IS NOT NULL AND wave <> ''")
        for row_id, region, dataset, wave in conn.execute(q):
            if wave_kind(wave) != "timestamp":
                continue
            new = normalize_wave_id(wave, dataset=dataset, region=region)
            if new == str(wave):
                continue
            todo.append((tbl, id_col, row_id, region, dataset, str(wave), new))
    return todo


def main() -> int:
    ap = argparse.ArgumentParser(description="回填裸时间戳波号（默认 dry-run）")
    ap.add_argument("--apply", action="store_true", help="真正写库（缺省只打印计划）")
    ap.add_argument("--db-backup", action="store_true", help="写库前做文件级备份")
    ap.add_argument("--fresh", action="store_true", help="忽略断点续跑状态")
    ap.add_argument("--region", default=None, help="只处理指定区域")
    a = ap.parse_args()

    db = resolve_db_path()
    if not os.path.isfile(db):
        print(f"[wave-id] 找不到 DB：{db}", file=sys.stderr)
        return 2

    state = load_state(a.fresh)
    conn = sqlite3.connect(db)
    try:
        todo = scan(conn)
        if a.region:
            todo = [t for t in todo if (t[3] or "").upper() == a.region.upper()]

        print(f"[wave-id] DB       : {db}")
        print(f"[wave-id] 模式     : {'APPLY（写库）' if a.apply else 'DRY-RUN（不写库）'}")
        print(f"[wave-id] 待归一   : {len(todo)} 行")
        if not todo:
            print("[wave-id] 无裸时间戳波号，无需处理")
            return 0

        by_old = {}
        for tbl, _idc, _rid, region, dataset, old, new in todo:
            by_old.setdefault((tbl, region, dataset, old), [new, 0])[1] += 1
        print(f"[wave-id] 涉及 {(len(by_old))} 个 (表/区/数据集/旧波号) 组合：")
        for (tbl, region, dataset, old), (new, n) in sorted(by_old.items()):
            print(f"    {tbl:<17} {region}/{dataset or '-'}  {old} -> {new}   ({n} 行)")

        if not a.apply:
            print("\n[wave-id] DRY-RUN 结束。确认无误后加 --apply --db-backup 执行。")
            return 0

        if a.db_backup:
            stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            bak = f"{db}.bak_waveid_{stamp}"
            shutil.copy2(db, bak)
            print(f"[wave-id] 已备份 DB -> {bak}")

        mapping_path = os.path.join(
            REPO_ROOT, "logs",
            f"wave_id_migration_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
        )
        os.makedirs(os.path.dirname(mapping_path), exist_ok=True)

        n = 0
        for tbl, id_col, row_id, region, dataset, old, new in todo:
            conn.execute(f"UPDATE {tbl} SET wave=? WHERE {id_col}=?", (new, row_id))
            n += 1
        conn.commit()

        with open(mapping_path, "w", encoding="utf-8") as f:
            json.dump(
                [{"table": t, "id": i, "region": r, "dataset": d, "old": o, "new": nw}
                 for t, _c, i, r, d, o, nw in todo],
                f, ensure_ascii=False, indent=2,
            )
        state["done"].extend(sorted({f"{t}:{o}" for t, _c, _i, _r, _d, o, _nw in todo}))
        state["done"] = sorted(set(state["done"]))
        save_state(state)

        print(f"[wave-id] 已归一 {n} 行；映射表 -> {mapping_path}")
        left = scan(conn)
        print(f"[wave-id] 复核：剩余裸时间戳 {len(left)} 行"
              + ("（幂等 OK）" if not left else "（异常，请检查）"))
        return 0 if not left else 1
    finally:
        conn.close()


if __name__ == "__main__":
    sys.exit(main())
