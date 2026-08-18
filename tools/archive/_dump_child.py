# -*- coding: utf-8 -*-
"""打印单个 child simulation 完整 JSON。"""
import sys, os, asyncio, json

MCP_DIR = r'd:\coding\traeCN_project\wqb\world-quant-brain-mcp'
os.chdir(MCP_DIR)
sys.path.insert(0, MCP_DIR)
from brain_api import BrainApiClient  # noqa: E402

c = BrainApiClient()

async def main():
    await c.ensure_authenticated()
    cid = sys.argv[1] if len(sys.argv) > 1 else '3N9UX66gm5iFadS1a6HqpItD'
    r = await c._request('GET', f'{c.base_url}/simulations/{cid}')
    d = r.json()
    print(json.dumps(d, ensure_ascii=False, indent=1)[:4000])

asyncio.run(main())
