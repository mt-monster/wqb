# -*- coding: utf-8 -*-
"""dump alpha 的 checks 结构，查 2y null 原因。"""
import sys, os, asyncio

MCP_DIR = r'd:\coding\traeCN_project\wqb\world-quant-brain-mcp'
os.chdir(MCP_DIR)
sys.path.insert(0, MCP_DIR)
from brain_api import BrainApiClient  # noqa: E402

c = BrainApiClient()

async def main():
    await c.ensure_authenticated()
    for aid in sys.argv[1:]:
        r = await c._request('GET', f'{c.base_url}/alphas/{aid}?include_properties=true')
        a = r.json()
        is_ = a.get('is') or {}
        print(f'=== {aid} sharpe={is_.get("sharpe")}')
        for ch in is_.get('checks', []):
            print(f'   check: {ch.get("name")} = {ch.get("value")}')
        rn = is_.get('riskNeutralized') or {}
        print(f'   RN sharpe={rn.get("sharpe")} fit={rn.get("fitness")}')

asyncio.run(main())
