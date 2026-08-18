# -*- coding: utf-8 -*-
"""检查 multisim 每个 child 的详细状态。"""
import sys, os, asyncio

MCP_DIR = r'd:\coding\traeCN_project\wqb\world-quant-brain-mcp'
os.chdir(MCP_DIR)
sys.path.insert(0, MCP_DIR)
from brain_api import BrainApiClient  # noqa: E402

c = BrainApiClient()

async def main():
    await c.ensure_authenticated()
    for mid in ['aInFTd2m54Zc2eEvZbZar0', '1RYSQiaC4ZkaVhWBp8euRD']:
        r = await c._request('GET', f'{c.base_url}/simulations/{mid}')
        d = r.json()
        ch = d.get('children') or []
        print(f'{mid} status={d.get("status")} children={len(ch)}')
        for cid in ch:
            r2 = await c._request('GET', f'{c.base_url}/simulations/{cid}')
            a = r2.json()
            err = str(a.get('error'))[:120] if a.get('error') else None
            print(f'  {cid} status={a.get("status")} alpha={a.get("alpha")} sharpe={a.get("sharpe")} err={err}')

asyncio.run(main())
