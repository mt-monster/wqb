# -*- coding: utf-8 -*-
"""查 AV 批 d3/d4 单条指标。"""
import sys, os, asyncio

MCP_DIR = r'd:\coding\traeCN_project\wqb\world-quant-brain-mcp'
os.chdir(MCP_DIR)
sys.path.insert(0, MCP_DIR)

from brain_api import BrainApiClient  # noqa: E402

client = BrainApiClient()

async def main():
    await client.ensure_authenticated()
    for tag, sid in [('AV-d3', '2fIItJ3yt4FOckf1h0kVEInS'), ('AV-d4', '4q5JDaLR4yz8CJzrwabuIZ')]:
        resp = await client._request('GET', f'{client.base_url}/simulations/{sid}')
        d = resp.json()
        aid = d.get('alpha')
        st = d.get('status')
        if aid:
            r = await client._request('GET', f'{client.base_url}/alphas/{aid}?include_properties=true')
            a = r.json()
            isd = a.get('is', {})
            checks = {c['name']: c.get('value') for c in isd.get('checks', [])}
            s2y = checks.get('IS_LADDER_SHARPE', checks.get('LOW_2Y_SHARPE'))
            print(f'[{tag}] {aid} status={st} sharpe={isd.get("sharpe")} fit={isd.get("fitness")} 2y={s2y} tv={isd.get("turnover")} margin={isd.get("margin")}')
        else:
            print(f'[{tag}] status={st} alpha=None')

asyncio.run(main())
