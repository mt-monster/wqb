#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""2026-09-02 提交队列（12:00:20 GMT+8 开闸），复用 0901 队列引擎。

队列 = judge 终检排序（2026-09-01 13:2x，详见 mutual_corr_vs_newbook_20260901.json）：
  1. 1YzOz8ZM  GLB  (2.17/1.61, P 0.628/S≈0)  点亮 GLB 塔 + ATOM，与 book 正交(max 0.08)
  2. 0mwVnbkG  IND  (2.45/1.87, P 0.5895/S 0.5895)  与 RR7OWQKd 实测仅 0.379，安全
  3. Jj7ee6nO  MEA  (1.67/1.70, P 0.632/S 0.609)  孪生对胜者（弃 omqEE1pn 0.987）
  4. pwjpKGJ3  KOR  (1.65/1.38, P 0.5763/S 0.081)  与全部 ≤0.03 完全正交
弃：58kALa11（与 1YzOz8ZM 孪生 0.916）、omqEE1pn（与 Jj7ee6nO 孪生 0.987）。

用法：python _submit_queue_20260902.py   # 等到 RESET_AT 后执行；QUEUE_NOW=1 跳过等待
"""
import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

import _submit_queue_20260901 as q  # noqa: E402

q.RESET_AT = "2026-09-02T04:00:20+00:00"  # 09-02 12:00:20 GMT+8（ET 午夜重置）
q.OUT = q.WQ_ROOT / "research-data" / "submit_queue_20260902.json"

q.QUEUE = ["1YzOz8ZM", "0mwVnbkG", "Jj7ee6nO", "pwjpKGJ3"]

q.DESCS = {
    "1YzOz8ZM": q.DESCS["1YzOz8ZM"],
    "0mwVnbkG": q.DESCS["0mwVnbkG"],
    "Jj7ee6nO": (
        "Idea: Combine breadth of analyst net-income estimate revisions with "
        "balance-sheet deleveraging in the MEA TOP400 universe.\n\n"
        "Rationale for data used: one-week net-income estimate raises minus four-week "
        "downward revisions captures the direction and breadth of analyst earnings "
        "expectations; the half-year change in current liabilities captures improving "
        "short-term solvency.\n\n"
        "Rationale for operators used: vec_avg aggregates vector fields across "
        "analysts, subtract forms net revision breadth, ts_delta(...,126) measures the "
        "six-month liability trend with a negative sign rewarding deleveraging, and "
        "the two ranked legs are blended 0.5/0.5."
    ),
    "pwjpKGJ3": (
        "Idea: Track Korean market order-flow positioning: blend broad recent "
        "buy-sell transaction activity with the monthly shift in large-player "
        "buy-sell balance.\n\n"
        "Rationale for data used: buy_sell_tx_count_ratio_all_60d_filled measures "
        "market-wide buying versus selling transaction counts over 60 days, while "
        "buy_sell_ratio_top20_250d_filled captures the positioning of the top-20 "
        "largest participants over one year.\n\n"
        "Rationale for operators used: ts_backfill(...,60) fills sparse reporting "
        "gaps, rank equalizes scales, ts_delta(...,20) captures the monthly shift in "
        "large-player balance as the dominant 0.7 leg, blended with 0.3 of broad "
        "activity and scale-normalized."
    ),
}

if __name__ == "__main__":
    asyncio.run(q.main())
