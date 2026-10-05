# -*- coding: utf-8 -*-
"""check_corr.py — 直连查 alpha 的 prod / self 相关性（不依赖 MCP 服务）。

背景（2026-10-05）：MCP `wq-brain-http` 进程可能中途挂掉（报 Connection closed），
但直连 `brain_api` 仍可用 ⇒ 需要一条不依赖 MCP 的相关性检查路径。

实现：轮询 `GET /alphas/{id}/correlations/{prod,self}`，直到返回非空 JSON 且含 `max`。
平台单并发、通常 1–5 分钟；本脚本串行轮询、每次 15s。

用法：
  python tracking/GBR/scripts/check_corr.py O089k78g [alpha_id ...] [--timeout 600]
"""
from __future__ import annotations

import argparse
import asyncio
import os
import sys
import time

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.insert(0, os.path.join(ROOT, "world-quant-brain-mcp"))

from brain_api import brain_client  # noqa: E402


async def one(alpha_id: str, timeout: int = 600, interval: int = 15):
    t0 = time.time()
    out = {}
    for kind in ("prod", "self"):
        while time.time() - t0 < timeout:
            r = await brain_client._request("GET", f"/alphas/{alpha_id}/correlations/{kind}")
            txt = (r.text or "").strip()
            if txt:
                try:
                    j = r.json()
                except Exception:
                    j = None
                if isinstance(j, dict) and j.get("max") is not None:
                    out[kind] = j
                    break
            await asyncio.sleep(interval)
        else:
            out[kind] = None
    return out


async def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("alpha_ids", nargs="+")
    ap.add_argument("--timeout", type=int, default=600)
    a = ap.parse_args()
    await brain_client.ensure_authenticated()
    for aid in a.alpha_ids:
        res = await one(aid, a.timeout)
        p, s = res.get("prod"), res.get("self")
        pm = p.get("max") if p else None
        sm = s.get("max") if s else None
        okp = "PASS" if (pm is not None and pm < 0.7) else "FAIL"
        oks = "PASS" if (sm is not None and sm < 0.7) else "FAIL"
        print(f"{aid}  prod={pm} [{okp}]  self={sm} [{oks}]")
        if s and s.get("top_correlated"):
            for t in s["top_correlated"][:3]:
                print(f"    self 最近邻: {t.get('id')} {t.get('correlation'):.4f}")


if __name__ == "__main__":
    asyncio.run(main())
