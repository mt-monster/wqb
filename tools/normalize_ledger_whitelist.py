# -*- coding: utf-8 -*-
"""normalize_ledger_whitelist.py — 把 `s0_whitelist` 归一为统一契约（2026-09-17 P0-4）。

## 为什么需要
实测 13 个区域该键有 **5 种形态**（candidates / whitelist / datasets / 推断 / 损坏），
导致 3 个消费者各自 fail-open。虽然 `wqb.ledger_whitelist.normalize()` 已让读取侧
容错，但**存量数据的形态漂移仍需收口**，否则第 6 种形态还会长出来。

## 目标契约（刻意对齐 s0_ranking 的稳定风格）
    {
      "datasets": ["ds_a", "ds_b", ...],     # 归一后的数据集 id
      "universe": "TOP1600",                  # 有则带上（顶层，不再藏 settings 里）
      "delay": 1,
      "entries": [ {...}, ... ],              # 原条目（保留 override 等审计字段）
      "_legacy": <原值>,                      # 原值备份，可回滚
      "_schema_from": "candidates"            # 来源形态，可追溯
    }

## 安全设计
- **默认 dry-run**：不加 `--apply` 只打印计划，绝不写库。
- **幂等**：已含 `_schema_from` 的记录直接跳过。
- **可回滚**：原值完整存进 `_legacy`；同时可选 `--db-backup` 先做文件级备份。
- **断点续跑**：状态写入 `logs/_state_normalize_whitelist.json`（原子写），
  重跑时跳过已完成区域（`--fresh` 可强制重来）。
- **未归一的区域不写**：解析失败（ok=False）时保留原值并计入报告，交由人工处理。

用法：
    python tools/normalize_ledger_whitelist.py                 # dry-run 全区域
    python tools/normalize_ledger_whitelist.py --region JPN    # 单区
    python tools/normalize_ledger_whitelist.py --apply         # 真正写库
    python tools/normalize_ledger_whitelist.py --apply --fresh  # 忽略续跑状态
"""
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

from wqb.ledger_whitelist import normalize, to_canonical  # noqa: E402

DEFAULT_DB = os.path.join(REPO_ROOT, "data", "wqb.db")
STATE_PATH = os.path.join(REPO_ROOT, "logs", "_state_normalize_whitelist.json")
KEY = "s0_whitelist"


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
    tmp = STATE_PATH + ".tmp"
    os.makedirs(os.path.dirname(STATE_PATH), exist_ok=True)
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)
    os.replace(tmp, STATE_PATH)


def is_already_canonical(rec):
    if not isinstance(rec, dict):
        return False
    return "datasets" in rec and "_schema_from" in rec


def main():
    ap = argparse.ArgumentParser(description="s0_whitelist 契约归一（默认 dry-run）")
    ap.add_argument("--db", default=DEFAULT_DB)
    ap.add_argument("--region", default=None, help="只处理指定区域（缺省全部）")
    ap.add_argument("--apply", action="store_true", help="真正写库（缺省只打印计划）")
    ap.add_argument("--fresh", action="store_true", help="忽略断点状态，全量重跑")
    ap.add_argument("--db-backup", action="store_true",
                    help="写库前先做 data/wqb.db 文件级备份（.bak_prewhitelist_<ts>）")
    a = ap.parse_args()

    if not os.path.isfile(a.db):
        raise SystemExit(f"[whitelist-norm] 库不存在: {a.db}")

    state = load_state(a.fresh)
    done = set(state["done"])
    conn = sqlite3.connect(a.db)
    conn.row_factory = sqlite3.Row

    sql = f"SELECT region, value FROM ledger_kv WHERE key='{KEY}'"
    params = ()
    if a.region:
        sql += " AND region=?"
        params = (a.region,)
    rows = conn.execute(sql, params).fetchall()

    print("=" * 78)
    print(f"s0_whitelist 契约归一 | 模式={'APPLY' if a.apply else 'DRY-RUN'} | "
          f"库={os.path.relpath(a.db, REPO_ROOT)} | 目标区域 {len(rows)} 个")
    print("=" * 78)

    planned, skipped_done, already, unparsable = [], [], [], []
    for r in rows:
        region, raw = r["region"], r["value"]
        if region in done and not a.apply:
            skipped_done.append(region)
            continue
        rec = normalize(raw)
        if not rec.get("ok"):
            unparsable.append((region, rec.get("reason")))
            continue
        # 已归一（幂等）
        try:
            existing = json.loads(raw) if isinstance(raw, (str, bytes)) else raw
        except Exception:
            existing = None
        if is_already_canonical(existing):
            already.append(region)
            continue
        canonical = to_canonical(rec, keep_legacy=raw)
        canonical["generated_at"] = datetime.now().strftime("%Y-%m-%dT%H:%M")
        planned.append((region, rec, canonical))

    for region, rec, canonical in planned:
        print(f"  {region:6s} schema={rec['schema']:11s} -> datasets={len(rec['datasets'])}"
              f" universe={rec.get('universe') or '-'} delay={rec.get('delay')}")
    if already:
        print(f"  [幂等] 已归一，跳过: {', '.join(already)}")
    if skipped_done:
        print(f"  [续跑] 已完成，跳过: {', '.join(skipped_done)}")
    for region, why in unparsable:
        print(f"  ★未归一（保留原值待人工处理）{region}: {why}")

    if not a.apply:
        print()
        print(f"[DRY-RUN] 计划改写 {len(planned)} 个区域；加 --apply 才会写库。")
        conn.close()
        return 0

    if a.db_backup:
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        bak = f"{a.db}.bak_prewhitelist_{ts}"
        shutil.copy2(a.db, bak)
        print(f"[backup] {os.path.relpath(bak, REPO_ROOT)}")

    written = 0
    for region, rec, canonical in planned:
        conn.execute("UPDATE ledger_kv SET value=? WHERE region=? AND key=?",
                     (json.dumps(canonical, ensure_ascii=False), region, KEY))
        conn.commit()
        written += 1
        done.add(region)
        state["done"] = sorted(done)
        save_state(state)          # 每区落一次状态 → 中断可续跑
        print(f"  [WRITE] {region} -> {len(canonical['datasets'])} datasets")
    conn.close()
    print(f"\n[APPLY] 已改写 {written} 个区域；状态文件 {os.path.relpath(STATE_PATH, REPO_ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
