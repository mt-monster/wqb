#!/usr/bin/env python
"""D9 存量回写（一次性动作，2026-09-28 用户批准）。

背景：`src/wqb/store/_backtest.py::upsert_backtest_rows` 原先只在「表达式不存在、自动补建」
分支写 status='backtested'；表达式已存在的分支只取 expr_id、不推进 status。
写入路径已在本次会话修复（+2 回归测试），但历史遗留不会自动补。

本脚本做一次性存量补偿：把已有回测结果、却仍停在回测前状态的表达式推进到 'backtested'。

安全约束：
  1. 只推进 ('gem','enhanced','pending','selected','gated') 五个回测前状态；
  2. 绝不触碰 backtested/submitted/completed/dropped/superseded/fail/coverage；
  3. 绝不覆盖已有 alpha_id；
  4. 执行前把 (id -> 原 status) 全量落盘为回滚清单；
  5. 幂等：重复执行只会命中「已被推进过」的行，天然空转。

判定口径：存在 backtest_results 行（按 expression_id 关联，或 expression 自身 alpha_id 非空）。

用法：
    python tools/backfill_expression_status_once.py            # 真实执行
    python tools/backfill_expression_status_once.py --dry-run  # 只报数不动库
"""
from __future__ import annotations

import argparse
import json
import sqlite3
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DB_PATH = ROOT / "data" / "wqb.db"
REPORTS = ROOT / "reports"
STAMP = datetime.now().strftime("%Y%m%d")

# 只推进回测前的状态（与 _backtest.py 修复保持一致）
ADVANCE_FROM = ("gem", "enhanced", "pending", "selected", "gated")
# 允许推进到的目标
TARGET = "backtested"


def _connect(readonly: bool = False):
    if readonly:
        return sqlite3.connect(f"file:{DB_PATH.as_posix()}?mode=ro", uri=True)
    return sqlite3.connect(str(DB_PATH))


def build_target_ids(con: sqlite3.Connection) -> list[int]:
    """按双触发口径算出待推进的表达式 id。

    触发 A：expression 自身 alpha_id 非空（已挂 alpha）
    触发 B：expression_id 能在 backtest_results 里找到
    """
    rows = con.execute(
        """
        SELECT e.id
        FROM expressions e
        WHERE e.status IN ({ph})
          AND (
                (e.alpha_id IS NOT NULL AND e.alpha_id <> '')
             OR EXISTS (SELECT 1 FROM backtest_results b WHERE b.expression_id = e.id)
          )
        ORDER BY e.id
        """.format(ph=",".join("?" * len(ADVANCE_FROM))),
        ADVANCE_FROM,
    ).fetchall()
    return [r[0] for r in rows]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true", help="只报数，不写库")
    ap.add_argument("--rollback-json", default=None, help="已有回滚清单路径（默认自动生成）")
    args = ap.parse_args()

    if not DB_PATH.exists():
        print(f"[FATAL] 数据库不存在: {DB_PATH}", file=sys.stderr)
        return 2

    con = _connect(readonly=True)
    ids = build_target_ids(con)
    before = dict(con.execute("SELECT status, COUNT(*) FROM expressions GROUP BY status").fetchall())
    by_region: list[tuple] = []
    if ids:
        # ids 为空时不得拼 SQL：IN () 会被解析成 0 个占位符，导致绑定数错配
        by_region = con.execute(
            """
            SELECT COALESCE(region,'?'), COUNT(*) FROM expressions
            WHERE id IN ({ph}) AND status IN ({sph})
            GROUP BY 1 ORDER BY 2 DESC
            """.format(ph=",".join("?" * len(ids)),
                       sph=",".join("?" * len(ADVANCE_FROM))),
            list(ids) + list(ADVANCE_FROM),
        ).fetchall()
    con.close()

    print(f"[INFO] 命中待推进行数: {len(ids)}")
    if by_region:
        print("[INFO] 区域分布: " + ", ".join(f"{r}={c}" for r, c in by_region))
    if not ids:
        print("[INFO] 无待推进行，退出（幂等空转）")
        return 0

    if args.dry_run:
        print("[DRY-RUN] 不写库，退出")
        return 0

    # ---------- 回滚清单 ----------
    rb_path = Path(args.rollback_json) if args.rollback_json else REPORTS / f"d9_status_backfill_rollback_{STAMP}.json"
    con = _connect(readonly=True)
    q = f"SELECT id, status FROM expressions WHERE id IN ({','.join('?' * len(ids))})"
    items = [[int(i), s] for i, s in con.execute(q, ids).fetchall()]
    con.close()
    REPORTS.mkdir(parents=True, exist_ok=True)
    rb_path.write_text(
        json.dumps(
            {
                "created_at": datetime.now().isoformat(timespec="seconds"),
                "purpose": "D9 status 存量回写回滚清单（id -> 原 status）",
                "target_status": TARGET,
                "n": len(items),
                "items": items,
            },
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )
    print(f"[OK] 回滚清单已写入: {rb_path}  (n={len(items)})")

    # ---------- 执行回写 ----------
    con = _connect()
    try:
        con.execute("PRAGMA journal_mode=WAL")
        changed = 0
        BATCH = 500
        for k in range(0, len(ids), BATCH):
            chunk = ids[k : k + BATCH]
            ph = ",".join("?" * len(chunk))
            cur = con.execute(
                f"""
                UPDATE expressions
                   SET status = ?, updated_at = datetime('now')
                 WHERE id IN ({ph})
                   AND status IN ({','.join('?' * len(ADVANCE_FROM))})
                """,
                [TARGET] + chunk + list(ADVANCE_FROM),
            )
            changed += cur.rowcount or 0
        con.commit()
    except Exception:
        con.rollback()
        raise
    finally:
        con.close()

    print(f"[OK] 实际推进行数: {changed}")

    # ---------- 校验 ----------
    con = _connect(readonly=True)
    after = dict(con.execute("SELECT status, COUNT(*) FROM expressions GROUP BY status").fetchall())
    protected = ("submitted", "completed", "dropped", "superseded", "fail", "coverage")
    leaked = []
    for st in protected:
        if after.get(st, 0) != before.get(st, 0):
            leaked.append((st, before.get(st, 0), after.get(st, 0)))
    con.close()

    print("[VERIFY] 受保护状态前后对比:")
    for st in protected:
        b, a = before.get(st, 0), after.get(st, 0)
        flag = "OK " if b == a else "!! "
        print(f"  {flag}{st:<12} {b} -> {a}")
    if leaked:
        print("[FATAL] 受保护状态被改动，请立即回滚！", file=sys.stderr)
        return 3

    print("[VERIFY] 全状态分布:")
    for st, c in sorted(after.items(), key=lambda x: -x[1]):
        print(f"  {st:<12} {before.get(st,0):>7} -> {c}")
    print("[DONE] 存量回写完成")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
