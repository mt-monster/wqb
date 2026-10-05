#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""区域 profile 漂移体检（profile green/red 精确层 ↔ DB 实证）。

机制见 region-profile-contract.md §5。本工具是「定期体检 / 审计」入口；
每次 win/dead_end 回写时的自动核对由 `upsert_registry_empirical` 的漂移钩子完成。

用法：
  python tools/profile_drift_check.py --region KOR           # 单区人读报告
  python tools/profile_drift_check.py --all                  # 全区汇总表
  python tools/profile_drift_check.py --all --json           # 机读
  python tools/profile_drift_check.py --region KOR --write-ledger   # 落 ledger profile_drift

退出码：0 = 无 high 级冲突；1 = 存在 high 级冲突（green_but_dead / red_but_won）；
2 = 用法 / 数据错误。
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "src"))

from wqb import db_conn  # noqa: E402
from wqb.config import REGIONS  # noqa: E402
from wqb.profile_drift import check_profile_drift  # noqa: E402

_SEV_MARK = {"high": "[HIGH]", "medium": "[med] ", "low": "[low] "}


def _print_report(rep: dict) -> None:
    s = rep.get("summary") or {}
    print(f"== {rep['region']}  needs_refresh={rep['needs_refresh']}  "
          f"last_verified={rep.get('last_verified') or '-'}  "
          f"high={s.get('high', 0)} med={s.get('medium', 0)} low={s.get('low', 0)}  "
          f"unbound_entries={s.get('unbound_entries', 0)}")
    for f in rep.get("findings") or []:
        mark = _SEV_MARK.get(f["severity"], f["severity"])
        ds = f["dataset"] or "-"
        print(f"  {mark} {f['kind']:22s} {ds:24s} {f['detail']}")
    print(f"  hint: {rep.get('hint')}")


def main() -> int:
    ap = argparse.ArgumentParser(description="区域 profile 漂移体检")
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--region", help="单区（如 KOR）")
    g.add_argument("--all", action="store_true", help="全部有 profile 的区域")
    ap.add_argument("--json", action="store_true", help="机读输出")
    ap.add_argument("--write-ledger", action="store_true",
                    help="把报告幂等写入 ledger_kv 的 profile_drift 键（缺省只读不写）")
    args = ap.parse_args()

    conn = db_conn.connect()
    regions = [args.region.upper()] if args.region else sorted(REGIONS)
    reports, n_high_total = [], 0
    try:
        for region in regions:
            rep = check_profile_drift(conn, region)
            if rep.get("profile") == "missing" and args.all:
                continue
            reports.append(rep)
            n_high_total += (rep.get("summary") or {}).get("high", 0)
            if args.write_ledger:
                conn.execute(
                    "INSERT OR REPLACE INTO ledger_kv (region, key, value, updated_at) "
                    "VALUES (?,?,?,datetime('now','localtime'))",
                    (region, "profile_drift", json.dumps(rep, ensure_ascii=False)),
                )
        if args.write_ledger:
            conn.commit()
    finally:
        conn.close()

    if args.json:
        print(json.dumps(reports if len(reports) > 1 else reports[0], ensure_ascii=False, indent=1))
    else:
        for rep in reports:
            _print_report(rep)
        if args.all:
            print(f"\n共 {len(reports)} 区，high 级冲突合计 {n_high_total}")
    return 1 if n_high_total else 0


if __name__ == "__main__":
    sys.exit(main())
