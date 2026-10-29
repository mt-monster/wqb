"""只读：检查 alpha 的 self / prod 相关性（提交前红线判定）。

用法:
    python tools/data-repair/check_corr.py <ALPHA_ID>             # 缓存/预读优先（默认）
    python tools/data-repair/check_corr.py <ALPHA_ID> --refresh   # 强制平台重测（终验用）

2026-10-28（P0-3）：默认改为缓存优先。旧版无条件 ``refresh=True``，每查一条都
强制平台重算——账号级单并发下代价是 195s 冷却 / 一次，而多数查询只是想看
「现在是多少」。要终验再显式 ``--refresh``。
"""
import os
import sys
import asyncio

HERE = os.path.dirname(os.path.abspath(__file__))
WQB = os.path.dirname(os.path.dirname(HERE))
MCP = os.path.join(WQB, "world-quant-brain-mcp")
for p in (HERE, MCP):
    if p not in sys.path:
        sys.path.insert(0, p)

from brain_api import brain_client


async def main(aid, refresh=False):
    await brain_client.ensure_authenticated()
    print("=== SELF correlation ===")
    try:
        sc = await brain_client.check_self_correlation(aid)
        print("  raw:", sc)
    except Exception as e:
        print("  ERR:", repr(e)[:300])
    print("\n=== PROD correlation (refresh=%s) ===" % refresh)
    try:
        pc = await brain_client.check_correlation(aid, refresh=refresh)
        print("  raw:", pc)
    except Exception as e:
        print("  ERR:", repr(e)[:300])


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("-")]
    flags = {a for a in sys.argv[1:] if a.startswith("-")}
    if not args or ("-h" in flags or "--help" in flags):
        print("usage: check_corr.py <ALPHA_ID> [--refresh]")
        sys.exit(0 if args or flags else 2)
    asyncio.run(main(args[0], refresh="--refresh" in flags))
