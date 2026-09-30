# -*- coding: utf-8 -*-
"""step_event_log.py — 步级评估 T2 事件台账 CLI（2026-09-30 方案 B）。

只包 `src/wqb/step_events.py` 的读写原语（封闭词表 + source 必填 + 幂等键）。
事件 = 客观发生过的事实（cache_hit / ghost_blocked / retry_sent …），
**不接受**"accuracy=0.85" 式评估结论——那是旧 step_metrics 被下线的根因。

用法：
    # 记一条事件（幂等键可选；重复跑同 key 不重复计数）
    python tools/step_event_log.py record --region KOR --wave 54 --step S0 \
        --type cache_hit --source "campaign.py::run(cache)" --dedupe-key "KOR:54:S0:cache:s0_calibrate_KOR"

    # 查询
    python tools/step_event_log.py query --region KOR [--wave 54] [--step S0] [--type cache_hit]

    # 封闭词表
    python tools/step_event_log.py vocab

    # 聚合（step_eval 消费的同款视图）
    python tools/step_event_log.py aggregate --region KOR
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from wqb.step_events import (  # noqa: E402
    EVENT_VOCAB, STEP_NAMES, aggregate, query_events, record_event,
)


def main() -> int:
    ap = argparse.ArgumentParser(description="步级评估 T2 事件台账（客观事件，append-only）")
    sub = ap.add_subparsers(dest="cmd", required=True)

    p_rec = sub.add_parser("record", help="记录一条事件")
    p_rec.add_argument("--region", required=True)
    p_rec.add_argument("--wave", default=None)
    p_rec.add_argument("--step", required=True, choices=STEP_NAMES)
    p_rec.add_argument("--type", required=True, dest="event_type",
                       help=f"事件类型（封闭词表，见 vocab 子命令）")
    p_rec.add_argument("--value", type=float, default=1.0, help="计数/次数（默认 1）")
    p_rec.add_argument("--source", required=True, help="埋点位置（文件::函数），必填可审计")
    p_rec.add_argument("--dedupe-key", default=None, help="幂等键（同键重复写入不计数）")
    p_rec.add_argument("--note", default=None, help="备注（入 metadata.note）")

    p_q = sub.add_parser("query", help="查询事件")
    p_q.add_argument("--region", default=None)
    p_q.add_argument("--wave", default=None)
    p_q.add_argument("--step", default=None, choices=STEP_NAMES)
    p_q.add_argument("--type", default=None, dest="event_type")
    p_q.add_argument("--limit", type=int, default=200)

    sub.add_parser("vocab", help="打印封闭事件词表")

    p_agg = sub.add_parser("aggregate", help="按 (step, event_type) 聚合")
    p_agg.add_argument("--region", required=True)
    p_agg.add_argument("--wave", default=None)

    a = ap.parse_args()

    if a.cmd == "record":
        try:
            res = record_event(
                a.region, a.step, a.event_type,
                wave=a.wave, value=a.value, source=a.source,
                dedupe_key=a.dedupe_key,
                metadata={"note": a.note} if a.note else None,
            )
        except ValueError as e:
            print(json.dumps({"error": str(e)}, ensure_ascii=False))
            return 2
        print(json.dumps(res, ensure_ascii=False))
        return 0

    if a.cmd == "query":
        rows = query_events(region=a.region, wave=a.wave, step=a.step,
                            event_type=a.event_type, limit=a.limit)
        print(json.dumps(rows, ensure_ascii=False, indent=2))
        return 0

    if a.cmd == "vocab":
        print(json.dumps(EVENT_VOCAB, ensure_ascii=False, indent=2))
        return 0

    if a.cmd == "aggregate":
        print(json.dumps(aggregate(a.region, a.wave), ensure_ascii=False, indent=2))
        return 0

    return 1


if __name__ == "__main__":
    sys.exit(main())
