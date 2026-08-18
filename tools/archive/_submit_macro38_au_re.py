# -*- coding: utf-8 -*-
"""重提 AU-d2 主批 (#2-#8 共 7 条, winsorize 已修正), decay2/SUBIND。"""
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

async def main():
    await client.ensure_authenticated()
    exprs = load(r'd:\coding\traeCN_project\wqb\tracking\USA\runs\usa_macro38_batch_au.txt')
    # #2-#8 = index 1..7
    payload = []
    for expr in exprs[1:]:
        settings = dict(BASE, decay=2, neutralization='SUBINDUSTRY')
        payload.append({'type': 'REGULAR', 'settings': settings, 'regular': expr})
    resp = await client._request('POST', f'{client.base_url}/simulations', json=payload)
    loc = resp.headers.get('Location', '')
    print(f'[AU-d2-re] n={len(payload)} decay=2 neut=SUBINDUSTRY status={resp.status_code} -> {loc}')
    if resp.status_code != 201:
        print('  BODY:', resp.text[:500])
    time.sleep(3)
    print('ALL SUBMITTED')

asyncio.run(main())
