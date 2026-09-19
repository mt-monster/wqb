# -*- coding: utf-8 -*-
"""migrate_priors_cache_key.py — 消除 priors 快照的大小写撞键（2026-09-17 P2-12）。

## 问题（实测）
`priors_snapshot_*` 键在 6 个区域**同时存在大小写两种**，且 payload 不同：

| 键 | 写入方 | 内容 | 典型长度 |
|---|---|---|---|
| `priors_snapshot_<REGION>`（大写）| `src/wqb/workflow/nodes/campaign.py` | **cache marker**（`assembled_at` + `stdout_tail`）| ~2033 |
| `priors_snapshot_<region>`（小写）| toolkit `assemble_priors.py --snapshot-ledger` | **真实 payload**（wins / dead_ends / sha）| 2471–7228 |

两者仅大小写之差 → **同名不同物**。查 `priors_snapshot_<REGION>` 想拿 priors，
拿到的却是不含 `wins`/`dead_ends` 的缓存标记。

消费侧（`brain-make-some-gem` 的 `run.py:359` / `economic_priors.py:75`）读的都是
**小写**，因此生成流程本身没拿错数据；本问题的真实危害是**键空间歧义**——
任何人（含 Agent）按大写查就会踩空，且 `_skill_roots` 式的"键名拼错即静默"隐患。

## 修法
把 campaign 节点的 cache marker 改为**独立命名** `assemble_priors_cache_<REGION>`
（与同族的 `s0_calibrate_<REGION>` 一致），并把存量大小写键改名（只改 key，payload 不动）。
改名后 `priors_snapshot_*` 只剩小写一种语义（真实 payload），歧义消除。

## 安全设计
- **默认 dry-run**；`--apply` 才写库；`--db-backup` 先做文件级备份。
- **幂等**：目标键已存在且源键不存在 → 跳过。
- **不覆盖新键**：若 `assemble_priors_cache_<REGION>` 已存在，保留较新者并报告。
- 状态落 `logs/_state_migrate_priors_cache.json`。

用法：
    python tools/migrate_priors_cache_key.py                      # dry-run
    python tools/migrate_priors_cache_key.py --db-backup --apply  # 备份后执行
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

PREFIX = "priors_snapshot_"
NEW_PREFIX = "assemble_priors_cache_"
STATE_PATH = os.path.join(REPO_ROOT, "logs", "_state_migrate_priors_cache.json")


def resolve_db_path() -> str:
    try:
        from wqb.workflow._common import resolve_db_path as _r
        return _r()
    except Exception:
        return os.path.join(REPO_ROOT, "data", "wqb.db")


def scan(conn) -> list:
    """找出「大写后缀」的 priors_snapshot 键（即 cache marker，应改名）。"""
    todo = []
    for region, key, updated in conn.execute(
        f"SELECT region, key, updated_at FROM ledger_kv WHERE key LIKE '{PREFIX}%'"
    ):
        suffix = key[len(PREFIX):]
        if suffix == suffix.lower():
            continue  # 已是小写 = 真实 payload，保持不动
        new_key = f"{NEW_PREFIX}{region}"
        exists = conn.execute(
            "SELECT COUNT(*) FROM ledger_kv WHERE region=? AND key=?", (region, new_key)
        ).fetchone()[0]
        todo.append((region, key, new_key, bool(exists), updated))
    return todo


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


def main() -> int:
    ap = argparse.ArgumentParser(description="消除 priors 快照大小写撞键（默认 dry-run）")
    ap.add_argument("--apply", action="store_true", help="真正写库")
    ap.add_argument("--db-backup", action="store_true", help="写库前做文件级备份")
    ap.add_argument("--fresh", action="store_true", help="忽略断点续跑状态")
    a = ap.parse_args()

    db = resolve_db_path()
    if not os.path.isfile(db):
        print(f"[priors-key] 找不到 DB：{db}", file=sys.stderr)
        return 2

    state = load_state(a.fresh)
    conn = sqlite3.connect(db)
    try:
        todo = scan(conn)
        print(f"[priors-key] DB   : {db}")
        print(f"[priors-key] 模式 : {'APPLY（写库）' if a.apply else 'DRY-RUN（不写库）'}")
        print(f"[priors-key] 待改名 {len(todo)} 个键：")
        for region, key, new_key, exists, updated in todo:
            flag = "（目标已存在，将保留较新者）" if exists else ""
            print(f"    {key:<28} -> {new_key:<28} region={region} {flag}  upd={updated}")

        if not todo:
            print("[priors-key] 无需处理（已是单一命名）")
            return 0
        if not a.apply:
            print("\n[priors-key] DRY-RUN 结束。确认后加 --apply --db-backup 执行。")
            return 0

        if a.db_backup:
            stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            bak = f"{db}.bak_priorskey_{stamp}"
            shutil.copy2(db, bak)
            print(f"[priors-key] 已备份 DB -> {bak}")

        renamed = skipped = 0
        for region, key, new_key, exists, updated in todo:
            if exists:
                # 目标已存在：保留两者中较新者（比较 updated_at 字符串，格式同源可比较）
                tgt = conn.execute(
                    "SELECT updated_at FROM ledger_kv WHERE region=? AND key=?",
                    (region, new_key),
                ).fetchone()
                tgt_upd = (tgt or [None])[0]
                if tgt_upd and updated and str(tgt_upd) >= str(updated):
                    conn.execute("DELETE FROM ledger_kv WHERE region=? AND key=?", (region, key))
                    skipped += 1
                    continue
                conn.execute("DELETE FROM ledger_kv WHERE region=? AND key=?", (region, new_key))
            conn.execute(
                "UPDATE ledger_kv SET key=?, updated_at=? WHERE region=? AND key=?",
                (new_key, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), region, key),
            )
            renamed += 1
        conn.commit()

        state["done"].extend([f"{r}:{k}" for r, k, _n, _e, _u in todo])
        state["done"] = sorted(set(state["done"]))
        save_state(state)

        print(f"[priors-key] 改名 {renamed} 个、合并丢弃 {skipped} 个")
        left = scan(conn)
        print(f"[priors-key] 复核：剩余大写键 {len(left)} 个"
              + ("（幂等 OK）" if not left else "（异常，请检查）"))
        # 额外报告：小写 payload 键分布
        n_low = conn.execute(
            f"SELECT COUNT(*) FROM ledger_kv WHERE key LIKE '{PREFIX}%'"
        ).fetchone()[0]
        print(f"[priors-key] 现存真实 payload 键（小写）: {n_low} 个")
        return 0 if not left else 1
    finally:
        conn.close()


if __name__ == "__main__":
    sys.exit(main())
