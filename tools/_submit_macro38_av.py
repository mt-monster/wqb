# -*- coding: utf-8 -*-
"""提交 AV 批: macro38 STATISTICAL 冠军精调, 全部 STAT 中性化, decay 分组 (#1 d3 / #2 d4 / #3-#8 d2)。"""
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

async def submit_multi(tag, exprs, decay):
    payload = []
    for expr in exprs:
        settings = dict(BASE, decay=decay, neutralization='STATISTICAL')
        payload.append({'type': 'REGULAR', 'settings': settings, 'regular': expr})
    resp = await client._request('POST', f'{client.base_url}/simulations', json=payload)
    loc = resp.headers.get('Location', '')
    print(f'[{tag}] n={len(payload)} decay={decay} neut=STATISTICAL status={resp.status_code} -> {loc}')
    if resp.status_code != 201:
        print('  BODY:', resp.text[:500])
    return loc

async def submit_single(tag, expr, decay):
    settings = dict(BASE, decay=decay, neutralization='STATISTICAL')
    payload = {'type': 'REGULAR', 'settings': settings, 'regular': expr}
    resp = await client._request('POST', f'{client.base_url}/simulations', json=payload)
    loc = resp.headers.get('Location', '')
    print(f'[{tag}] single decay={decay} neut=STATISTICAL status={resp.status_code} -> {loc}')
    if resp.status_code != 201:
        print('  BODY:', resp.text[:500])
    return loc

async def main():
    await client.ensure_authenticated()
    exprs = load(r'd:\coding\traeCN_project\wqb\tracking\USA\runs\usa_macro38_batch_av.txt')
    # #1 decay3 单条
    await submit_single('AV-d3', exprs[0], 3)
    time.sleep(2)
    # #2 decay4 单条
    await submit_single('AV-d4', exprs[1], 4)
    time.sleep(2)
    # #3-#8 decay2 主批 6 条
    await submit_multi('AV-d2', exprs[2:], 2)
    time.sleep(3)
    print('ALL SUBMITTED')

asyncio.run(main())
