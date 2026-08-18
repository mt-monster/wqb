# -*- coding: utf-8 -*-
"""提交 AT 批: macro38 MAHILO decay2 精调, 混合 decay (1/2/3), SUBIND。"""
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

async def submit_multi(tag, exprs, decay, neutralization):
    payload = []
    for expr in exprs:
        settings = dict(BASE, decay=decay, neutralization=neutralization)
        payload.append({'type': 'REGULAR', 'settings': settings, 'regular': expr})
    resp = await client._request('POST', f'{client.base_url}/simulations', json=payload)
    loc = resp.headers.get('Location', '')
    print(f'[{tag}] n={len(exprs)} decay={decay} status={resp.status_code} -> {loc}')
    return loc

async def submit_single(tag, expr, decay, neutralization):
    settings = dict(BASE, decay=decay, neutralization=neutralization)
    payload = {'type': 'REGULAR', 'settings': settings, 'regular': expr}
    resp = await client._request('POST', f'{client.base_url}/simulations', json=payload)
    loc = resp.headers.get('Location', '')
    print(f'[{tag}] single decay={decay} status={resp.status_code} -> {loc}')
    return loc

async def main():
    await client.ensure_authenticated()
    exprs = load(r'd:\coding\traeCN_project\wqb\tracking\USA\runs\usa_macro38_batch_at.txt')
    # #1 decay3 单条
    await submit_single('AT-d3', exprs[0], 3, 'SUBINDUSTRY')
    time.sleep(3)
    # #8 decay1 单条
    await submit_single('AT-d1', exprs[7], 1, 'SUBINDUSTRY')
    time.sleep(3)
    # #2-#7 decay2 主批
    rest = [exprs[i] for i in [1, 2, 3, 4, 5, 6]]
    await submit_multi('AT-d2', rest, 2, 'SUBINDUSTRY')
    time.sleep(5)
    print('ALL SUBMITTED')

asyncio.run(main())
