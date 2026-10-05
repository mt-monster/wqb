#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""self_batch.py — 批量 self-corr 快筛（本地 PnL 池，免费，不占平台相关性槽）。

用法::
    python tools/self_batch.py A1:标签 A2:标签 ...
"""
from __future__ import annotations

import asyncio
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "world-quant-brain-mcp"))


async def main() -> int:
    from brain_api import brain_client as brain  # noqa: E402
    await brain.ensure_authenticated()
    print(f"{'alpha':12s} {'self':>8s}  flag  label")
    for arg in sys.argv[1:]:
        aid, _, lab = arg.partition(":")
        try:
            res = await brain.check_self_correlation(aid, threshold=0.7)
            mx = res.get("max_correlation")
            flag = "OK" if (mx is not None and mx < 0.7) else "FAIL"
            print(f"{aid:12s} {round(mx, 4) if mx is not None else None!s:>8s}  {flag}  {lab}")
        except Exception as e:
            print(f"{aid:12s} {'ERR':>8s}  --    {lab} {type(e).__name__}")
    return 0


if __name__ == "__main__":
    raise SystemExit(asyncio.run(main()))
