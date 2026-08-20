# -*- coding: utf-8 -*-
"""提交 AR 批: macro38 追批 - 换手控制主线 (AP 批 短期变化 1.09/2y1.35 但 tv 56.5%), decay4/SUBIND。"""
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
        return [l.strip() for l in f if l.strip() and not l.startswith('#')]

async def submit(tag, path, decay, neutralization):
    exprs = load(path)
    payload = []
    for expr in exprs:
        settings = dict(BASE, decay=decay, neutralization=neutralization)
        payload.append({'type': 'REGULAR', 'settings': settings, 'regular': expr})
    resp = await client._request('POST', f'{client.base_url}/simulations', json=payload)
    loc = resp.headers.get('Location', '')
    print(f'[{tag}] {os.path.basename(path)} decay={decay} neut={neutralization} status={resp.status_code} -> {loc}')
    if resp.status_code != 201:
        print('  BODY:', resp.text[:500])
    return loc

async def main():
    await client.ensure_authenticated()
    await submit('AR', r'd:\coding\traeCN_project\wqb\tracking\USA\runs\usa_macro38_batch_ar.txt', 4, 'SUBINDUSTRY')
    time.sleep(5)
    print('ALL SUBMITTED')

asyncio.run(main())
