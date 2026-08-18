# -*- coding: utf-8 -*-
"""提交 inst6 T1/T2 批（最后配置点：T1=TOP3000/d1, T2=TOP1000/d2），直接 POST /simulations 数组。"""
import sys, os, time, asyncio

MCP_DIR = r'd:\coding\traeCN_project\wqb\world-quant-brain-mcp'
os.chdir(MCP_DIR)
sys.path.insert(0, MCP_DIR)

from brain_api import BrainApiClient  # noqa: E402

client = BrainApiClient()

BASE = {
    "instrumentType": "EQUITY", "region": "USA", "universe": "TOP3000",
    "delay": 1, "truncation": 0.0, "pasteurization": "ON",
    "unitHandling": "VERIFY", "nanHandling": "OFF", "maxTrade": "ON",
    "maxPosition": "OFF", "language": "FASTEXPR", "visualization": False,
    "startDate": "2014-01-01", "endDate": "2023-12-31",
}

def load(path):
    with open(path, encoding='utf-8') as f:
        return [l.strip() for l in f if l.strip()]

async def submit(tag, path, universe, decay):
    exprs = load(path)
    payload = []
    for expr in exprs:
        settings = dict(BASE, universe=universe, decay=decay, neutralization='SUBINDUSTRY')
        payload.append({'type': 'REGULAR', 'settings': settings, 'regular': expr})
    resp = await client._request('POST', f'{client.base_url}/simulations', json=payload)
    loc = resp.headers.get('Location', '')
    print(f'[{tag}] {os.path.basename(path)} univ={universe} decay={decay} status={resp.status_code} -> {loc}')
    if resp.status_code != 201:
        print('  BODY:', resp.text[:500])
    return loc

async def main():
    await client.ensure_authenticated()
    await submit('T1', r'd:\coding\traeCN_project\wqb\tracking\USA\runs\usa_inst6_batch_t1.txt', 'TOP3000', 1)
    time.sleep(5)
    await submit('T2', r'd:\coding\traeCN_project\wqb\tracking\USA\runs\usa_inst6_batch_t2.txt', 'TOP1000', 2)
    time.sleep(5)
    print('ALL SUBMITTED')

asyncio.run(main())
