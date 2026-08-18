# -*- coding: utf-8 -*-
"""查 AU 批两个 simulation 的错误详情。"""
import sys, os, asyncio, json

MCP_DIR = r'd:\coding\traeCN_project\wqb\world-quant-brain-mcp'
os.chdir(MCP_DIR)
sys.path.insert(0, MCP_DIR)

from brain_api import BrainApiClient  # noqa: E402

client = BrainApiClient()

async def main():
    await client.ensure_authenticated()
    for sid in ['4dYgazfzy4ZHaKY4M9IUrE5', '2utckl7zA5hkc8hQGEMFDNs']:
        resp = await client._request('GET', f'{client.base_url}/simulations/{sid}')
        d = resp.json()
        print(f'=== {sid} ===')
        print(f'status={d.get("status")} alpha={d.get("alpha")}')
        err = d.get('error') or d.get('message') or d.get('statusMessage')
        print(f'error={err}')
        # children
        ch = d.get('children') or []
        print(f'children n={len(ch)}')
        for c in ch[:3]:
            cid = c if isinstance(c, str) else c.get('id')
            print(f'  child={cid}')
        print()

asyncio.run(main())
