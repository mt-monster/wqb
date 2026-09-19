# -*- coding: utf-8 -*-
"""区域切换预筛门禁（P1-7：把 field-quality 的强制纪律机器化）。

纪律来源：brain-alpha-research-field-quality §3「区域切换预筛门禁」（2026-08-05 用户强制）——
每次切换区域回测前，必须先跑 `tools/webdata_quality.py --zip WebData_*.zip --region <R> ...`
读取区域级中性化排名/甜点区/退化标记。历史违规（USA/GBR subagent 未先跑）说明
"靠纪律与验证清单"不够，需要机器闸。

判定依据（满足其一即 PASS）：
  1. ledger_kv 存在键 `prescreen_<REGION>`（值含 webdata_quality 产出的摘要）；
  2. 战役目录存在 `reference/webdata_prescreen_<REGION>.json`（webdata_quality 落盘别名）。

用法：
  python tools/prescreen_gate.py --region KOR                 # 查门（exit 0=PASS / 1=BLOCK）
  python tools/prescreen_gate.py --region KOR --record \
      --source webdata_quality --summary '{"neutralization_top":"REVERSION_AND_MOMENTUM"}'
      # 预筛跑完后登记（写 ledger_kv prescreen_<REGION>）

退出码：0=PASS；1=BLOCK；2=参数/IO 错误。
"""
from __future__ import annotations

import argparse
import json
import os
import sqlite3
import sys
from datetime import datetime, timezone

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB = os.path.join(REPO, "data", "wqb.db")


def _ledger_has_prescreen(region: str) -> bool:
    if not os.path.exists(DB):
        return False
    conn = sqlite3.connect(DB)
    try:
        row = conn.execute(
            "SELECT value FROM ledger_kv WHERE region=? AND key=?",
            (region, f"prescreen_{region}")).fetchone()
        return row is not None
    finally:
        conn.close()


def _record(region: str, source: str, summary: dict) -> str:
    conn = sqlite3.connect(DB)
    try:
        conn.execute(
            "INSERT OR REPLACE INTO ledger_kv (region, key, value, updated_at) "
            "VALUES (?, ?, ?, ?)",
            (region, f"prescreen_{region}",
             json.dumps({"source": source, "summary": summary,
                         "recorded_at": datetime.now(timezone.utc).isoformat()},
                        ensure_ascii=False),
             datetime.now(timezone.utc).isoformat()))
        conn.commit()
    finally:
        conn.close()
    return f"ledger_kv[{region}].prescreen_{region}"


def main() -> int:
    ap = argparse.ArgumentParser(description="区域切换预筛门禁（查/登记）")
    ap.add_argument("--region", required=True)
    ap.add_argument("--record", action="store_true",
                    help="登记预筛已完成（写 ledger 键），而不是查门")
    ap.add_argument("--source", default="webdata_quality")
    ap.add_argument("--summary", default="{}", help="预筛摘要 JSON 字符串")
    a = ap.parse_args()
    region = a.region.strip().upper()

    if a.record:
        try:
            summary = json.loads(a.summary)
        except json.JSONDecodeError as e:
            print(f"[prescreen_gate] --summary 不是合法 JSON：{e}", file=sys.stderr)
            return 2
        where = _record(region, a.source, summary)
        print(f"[prescreen_gate] 已登记 {where}")
        return 0

    ref = os.path.join(REPO, "tracking", region,
                       "reference", f"webdata_prescreen_{region}.json")
    if _ledger_has_prescreen(region):
        print(f"[prescreen_gate] PASS：ledger 存在 prescreen_{region}")
        return 0
    if os.path.exists(ref):
        print(f"[prescreen_gate] PASS：存在 {ref}")
        return 0
    print(f"[prescreen_gate] BLOCK：区域 {region} 无预筛记录。"
          f"先跑 tools/webdata_quality.py --zip WebData_*.zip --region {region} --delay 1，"
          f"完成后用 --record 登记（纪律出处：brain-alpha-research-field-quality §3）。")
    return 1


if __name__ == "__main__":
    sys.exit(main())
