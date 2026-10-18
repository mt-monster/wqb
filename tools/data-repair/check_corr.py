"""只读：检查 alpha 的 self / prod 相关性（提交前红线判定）。
用法: python tools/data-repair/check_corr.py <ALPHA_ID>"""
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


async def main(aid):
    await brain_client.ensure_authenticated()
    print("=== SELF correlation ===")
    try:
        sc = await brain_client.check_self_correlation(aid)
        print("  raw:", sc)
    except Exception as e:
        print("  ERR:", repr(e)[:300])
    print("\n=== PROD correlation (refresh=True) ===")
    try:
        pc = await brain_client.check_correlation(aid, refresh=True)
        print("  raw:", pc)
    except Exception as e:
        print("  ERR:", repr(e)[:300])


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("usage: check_corr.py <ALPHA_ID>")
        sys.exit(2)
    asyncio.run(main(sys.argv[1]))
