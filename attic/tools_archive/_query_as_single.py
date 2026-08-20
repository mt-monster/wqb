# -*- coding: utf-8 -*-
"""查询 AS 批 d2/d8 单条 simulation 的 alpha 指标。"""
import sys, os, asyncio

MCP_DIR = r'd:\coding\traeCN_project\wqb\world-quant-brain-mcp'
os.chdir(MCP_DIR)
sys.path.insert(0, MCP_DIR)

from brain_api import BrainApiClient  # noqa: E402

client = BrainApiClient()

async def main():
    await client.ensure_authenticated()
    for sim_id in ['1vh3JaeuN5bSaGYbi95gEsd', '2gN0o5x14CW8UjzNoVyBSH']:
        resp = await client._request('GET', f'{client.base_url}/simulations/{sim_id}')
        data = resp.json()
        print(f'=== {sim_id} ===')
        print(f'status={data.get("status")}')
        alpha_id = data.get('alpha')
        print(f'alpha={alpha_id}')
        if alpha_id:
            resp2 = await client._request('GET', f'{client.base_url}/alphas/{alpha_id}')
            a = resp2.json()
            is_data = a.get('is', {})
            print(f'sharpe={is_data.get("sharpe")} fit={is_data.get("fitness")} tv={is_data.get("turnover")} margin={is_data.get("margin")}')
            checks = {c['name']: c.get('value') for c in a.get('is', {}).get('checks', [])}
            print(f'2y={checks.get("IS_LADDER_SHARPE", checks.get("LOW_2Y_SHARPE"))}')

asyncio.run(main())
