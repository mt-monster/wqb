# -*- coding: utf-8 -*-
"""检查 multisim children 的表达式内容。"""
import sys, os, asyncio

MCP_DIR = r'd:\coding\traeCN_project\wqb\world-quant-brain-mcp'
os.chdir(MCP_DIR)
sys.path.insert(0, MCP_DIR)
from brain_api import BrainApiClient  # noqa: E402

c = BrainApiClient()

async def main():
    await c.ensure_authenticated()
    for mid in sys.argv[1:]:
        r = await c._request('GET', f'{c.base_url}/simulations/{mid}')
        d = r.json()
        ch = d.get('children') or []
        print(f'=== {mid} status={d.get("status")} n={len(ch)}')
        for cid in ch:
            r2 = await c._request('GET', f'{c.base_url}/simulations/{cid}')
            a = r2.json()
            reg = (a.get('regular') or '')[:90]
            print(f'  {a.get("alpha")} decay={a.get("settings",{}).get("decay")} | {reg}')

asyncio.run(main())
