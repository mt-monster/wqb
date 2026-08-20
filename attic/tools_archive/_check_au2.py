# -*- coding: utf-8 -*-
"""查 AU 批 children 指标 + AU-stat 单条指标。"""
import sys, os, asyncio

MCP_DIR = r'd:\coding\traeCN_project\wqb\world-quant-brain-mcp'
os.chdir(MCP_DIR)
sys.path.insert(0, MCP_DIR)

from brain_api import BrainApiClient  # noqa: E402

client = BrainApiClient()

def fmt(a):
    isd = a.get('is', {})
    checks = {c['name']: c.get('value') for c in isd.get('checks', [])}
    s2y = checks.get('IS_LADDER_SHARPE', checks.get('LOW_2Y_SHARPE'))
    return (f"{a.get('id')} sharpe={isd.get('sharpe')} fit={isd.get('fitness')} "
            f"2y={s2y} tv={isd.get('turnover')} margin={isd.get('margin')} "
            f"rn_sharpe={isd.get('rnSharpe')}")

async def main():
    await client.ensure_authenticated()
    # AU-stat 单条
    resp = await client._request('GET', f'{client.base_url}/alphas/1Yp3N7dX?include_properties=true')
    print('=== AU-stat (STATISTICAL) ===')
    print(fmt(resp.json()))
    print()
    # AU-d2 children
    resp = await client._request('GET', f'{client.base_url}/simulations/4dYgazfzy4ZHaKY4M9IUrE5')
    children = resp.json().get('children', [])
    print(f'=== AU-d2 children n={len(children)} ===')
    for c in children:
        cid = c if isinstance(c, str) else c.get('id')
        # child 是 simulation id, 取其 alpha
        r2 = await client._request('GET', f'{client.base_url}/simulations/{cid}')
        cd = r2.json()
        aid = cd.get('alpha')
        cst = cd.get('status')
        if aid:
            r3 = await client._request('GET', f'{client.base_url}/alphas/{aid}?include_properties=true')
            print(f'[{cst}] {fmt(r3.json())}')
        else:
            print(f'[{cst}] child={cid} alpha=None err={cd.get("error") or cd.get("message")}')

asyncio.run(main())
