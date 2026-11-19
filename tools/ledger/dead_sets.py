#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""判死台账的查看与撤判回写计划（2026-11-19 新增）。

**为什么需要它**：2026-11-19 审计实测，判死台账与判死档案会**互相矛盾**且没人回写：

- `DEU` 的 `tracking/DEU/atom_orthogonal/DEATH_AUDIT_20261110.md` 已明确**撤判重开**
  `risk60` / `risk88` / `news50` / `other545` 等，但 ledger 里的死键原封未动
  ⇒ 硬闸照拦（"唯一真硬闸只读 ledger `<ds>_dead`" 的直接后果）。
- 反向：ledger 的判死记录有四种键形态，旧读取口径只认 `<ds>_dead`
  ⇒ 聚合键与带日期/后缀的记录读不到（见 `src/wqb/dead_datasets.py` 的 docstring）。

本工具做三件事，**都不写库**（写库一律走 `mcp__wqb-db__upsert_ledger_key`，幂等）：

1. `--region R`            打印该区三档判死（数据集级 / 条件死 / 族级）+ 口径说明；
2. `--reopen a,b`          生成**撤判回写计划**（`upsert_ledger_key` 的完整 payload），
                            由执行者照抄调用（AGENTS.md §5：台账写入走 MCP，且长 payload
                            不手转录 ⇒ 本工具直接打印可复制的 JSON）；
3. `--json`                机器读输出。

用法：
    python tools/dead_sets.py --region GBR
    python tools/dead_sets.py --region DEU --reopen risk60,risk88,news50
"""
from __future__ import annotations

import argparse
import json
import sqlite3
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "src"))

from wqb.dead_datasets import dead_levels, parse_dead_entries  # noqa: E402

DB = REPO / "data" / "wqb.db"

LEVEL_CN = {
    "dataset": "数据集级（**硬闸拦**）",
    "conditional": "条件死（**告警不拦**：只禁作主信号，允许作辅助腿）",
    "family": "族 / 路线级（不拦：判的是字段族或机制，不是整集）",
}


def _connect_readonly():
    """只读连接走规范工厂（`wqb.db_conn.connect(readonly=True)`）。

    ⚠ 不用裸 `sqlite3.connect`：`tests/unit/01_store_db/test_db_write_guards.py`
    的白名单闸只放行 `wqb.db_conn` / `_lib.db` 两条路；且 `readonly=True` 会跳过
    `PRAGMA journal_mode=WAL`（WAL 是持久化库级属性，设了即使不写行也会改库文件字节）。
    """
    from wqb.db_conn import connect
    return connect(readonly=True)


def _rows(conn: sqlite3.Connection, region: str) -> list[tuple[str, str]]:
    cur = conn.cursor()
    cur.execute(
        "SELECT key, value FROM ledger_kv WHERE region=? AND ("
        " key LIKE '%_dead' OR key LIKE 'dead_%' OR key LIKE '%_dead_%'"
        " OR key LIKE '%_dead_end' OR key LIKE 'dead_end_%')",
        (region,),
    )
    return cur.fetchall()


def _reopen_payload(region: str, dataset: str, reason: str) -> dict:
    """生成撤判回写 payload（**由执行者照抄调用 upsert_ledger_key**）。

    ⚠ **必须用 `mode="merge"`，不得 `replace`**（AGENTS.md §5 的覆写事故）：
    台账里该键的**原始判死证据**（dead_at / evidence / max_sharpe / probed …）必须原样保留，
    merge 只覆盖本次要改的标量字段 ⇒ 不会丢证据、也不会整值改坏。
    本函数**不重写原 value**，只给出增量字段。
    """
    return {
        "region": region,
        "key": f"{dataset}_dead",
        "mode": "merge",
        "value": {
            "status": "reopened",
            "reopened_at": "2026-11-19",
            "reopened_reason": reason,
            "reopen_note": ("2026-11-19 撤判回写：档案已判「撤判重开」，台账同步标记 reopened，"
                            "硬闸不再拦（判据本体 src/wqb/dead_datasets.py：status=reopened ⇒ 不入任何档）。"
                            "原始判死证据保留在本键的其余字段 / 对应档案里（merge 增量写，未整值覆盖）。"),
        },
    }


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="判死台账查看与撤判回写计划")
    ap.add_argument("--region", required=True, help="区域（如 DEU / GBR / EUR）")
    ap.add_argument("--reopen", default="", help="逗号分隔的数据集名，生成撤判回写计划")
    ap.add_argument("--reason", default="", help="撤判理由（配合 --reopen）")
    ap.add_argument("--json", action="store_true", help="机器读输出")
    args = ap.parse_args(argv)

    conn = _connect_readonly()
    try:
        rows = _rows(conn, args.region)
    finally:
        conn.close()

    levels = dead_levels(rows)
    parsed = parse_dead_entries(rows)

    if args.reopen:
        names = [x.strip() for x in args.reopen.split(",") if x.strip()]
        plans = [_reopen_payload(args.region, n, args.reason or "档案已判撤判重开") for n in names]
        if args.json:
            print(json.dumps({"region": args.region, "reopen_plan": plans},
                             ensure_ascii=False, indent=2))
        else:
            print(f"[dead_sets] 撤判回写计划（{args.region}）——**由执行者照抄调用**：")
            print("    mcp__wqb-db__upsert_ledger_key(")
            for p in plans:
                print(f"        region={p['region']!r}, key={p['key']!r}, value={json.dumps(p['value'], ensure_ascii=False)}")
            print("    )")
            print("⚠ 一次一键（merge 对 list 是整列覆盖 ⇒ 勿把多键塞进一次调用）")
        return 0

    if args.json:
        print(json.dumps({
            "region": args.region,
            "levels": levels,
            "entries": {k: {kk: vv for kk, vv in v.items() if kk != "detail"}
                        for k, v in parsed.items() if k != "__unclassified__"},
            "unclassified": parsed.get("__unclassified__", {}).get("key", ""),
        }, ensure_ascii=False, indent=2))
        return 0

    print(f"[dead_sets] 区域 {args.region} ｜ 判死记录 {len(rows)} 条")
    for lvl in ("dataset", "conditional", "family"):
        items = levels[lvl]
        print(f"\n  {LEVEL_CN[lvl]} —— {len(items)} 个")
        for ds in items:
            e = parsed.get(ds, {})
            reason = (e.get("reason") or "")[:100]
            key = e.get("key", "")
            extra = f"  [{key}]" if key else ""
            print(f"    - {ds}{extra}")
            if reason:
                print(f"        {reason}")
    unc = parsed.get("__unclassified__")
    if unc:
        print(f"\n  ○ 键形态未归类（不参与硬闸）：{unc.get('key')}")
    print("\n口径：数据集级 = 硬闸拦；条件死 / 族级 = 只告警不拦。"
          "判据本体 = src/wqb/dead_datasets.py（与 MCP get_dead_datasets、"
          "pipeline dead_dataset_guard 同源）。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
