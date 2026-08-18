# -*- coding: utf-8 -*-
"""提交 AU 批: macro38 MAHILO 终调, decay2 主批 + STATISTICAL 单条, SUBIND/STATISTICAL。"""
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
    print(f'[{tag}] n={len(exprs)} decay={decay} neut={neutralization} status={resp.status_code} -> {loc}')
    return loc

async def submit_single(tag, expr, decay, neutralization):
    settings = dict(BASE, decay=decay, neutralization=neutralization)
    payload = {'type': 'REGULAR', 'settings': settings, 'regular': expr}
    resp = await client._request('POST', f'{client.base_url}/simulations', json=payload)
    loc = resp.headers.get('Location', '')
    print(f'[{tag}] single decay={decay} neut={neutralization} status={resp.status_code} -> {loc}')
    return loc

async def main():
    await client.ensure_authenticated()
    exprs = load(r'd:\coding\traeCN_project\wqb\tracking\USA\runs\usa_macro38_batch_au.txt')
    # #1 STATISTICAL 单条
    await submit_single('AU-stat', exprs[0], 2, 'STATISTICAL')
    time.sleep(3)
    # #2-#8 SUBIND 主批
    rest = exprs[1:]
    await submit_multi('AU-d2', rest, 2, 'SUBINDUSTRY')
    time.sleep(5)
    print('ALL SUBMITTED')

asyncio.run(main())
