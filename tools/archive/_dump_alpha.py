# -*- coding: utf-8 -*-
"""打印 alpha 对象完整指标。用法: python _dump_alpha.py <alpha_id>"""
import sys, os, asyncio, json

MCP_DIR = r'd:\coding\traeCN_project\wqb\world-quant-brain-mcp'
os.chdir(MCP_DIR)
sys.path.insert(0, MCP_DIR)
from brain_api import BrainApiClient  # noqa: E402

c = BrainApiClient()

async def main():
    await c.ensure_authenticated()
    aid = sys.argv[1] if len(sys.argv) > 1 else 'E5Gn0YaR'
    r = await c._request('GET', f'{c.base_url}/alphas/{aid}?include_properties=true')
    print('status', r.status_code)
    print(r.text[:5000])

asyncio.run(main())
