#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""2026-09-02 提交队列（12:00:20 GMT+8 开闸），复用 0901 队列引擎。

★ 2026-09-01 按用户新准则（优先点塔 → 绩效次之 → MEA 本季度排除）重排；
  点塔口径 = 该 catalog 下近 90 天提交 ACTIVE ≥3 颗。
  1. 0mwVnbkG  IND  (2.45/1.87, P 0.5895/S 0.5895)  oth696_*(OTHER, 现 2/3) → 补第 3 颗
       ★ 点亮 IND/D1/OTHER
  2. pwjpKGJ3  KOR  (1.65/1.38, P 0.5763/S 0.081)  buy_sell_* → insider_feats(OTHER，
       平台 /data-fields/{id} 已确认) → 补第 3 颗 ★ 点亮 KOR/D1/OTHER（现 2/3）
  3. 1YzOz8ZM  GLB  (2.17/1.61, P 0.628/S≈0)  intraday_pv_feats(PV)
       ⚠️ 不能点亮任何塔（GLB/D1/PV 现 0/3，提交后仅 1/3）——GLB 全域仅 1 颗 ACTIVE(OTHER)。
       价值 = GLB 区域第 2 个提交 + PV 塔打地基；绩效 1.61 排"不能点亮档"第一。
弃：58kALa11（与 1YzOz8ZM 孪生 0.916）、Jj7ee6nO/omqEE1pn（MEA 本季度排除 + 0.987 孪生）。
第 4 槽留空（已测候选池耗尽；MEA 本季度不放行）。

用法：python _submit_queue_20260902.py   # 等到 RESET_AT 后执行；QUEUE_NOW=1 跳过等待
"""
import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

import _submit_queue_20260901 as q  # noqa: E402

q.RESET_AT = "2026-09-02T04:00:20+00:00"  # 09-02 12:00:20 GMT+8（ET 午夜重置）
q.OUT = q.WQ_ROOT / "research-data" / "submit_queue_20260902.json"

q.QUEUE = ["0mwVnbkG", "pwjpKGJ3", "1YzOz8ZM"]

q.DESCS = {
    "1YzOz8ZM": q.DESCS["1YzOz8ZM"],
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
    "0mwVnbkG": q.DESCS["0mwVnbkG"],
}

if __name__ == "__main__":
    asyncio.run(q.main())
