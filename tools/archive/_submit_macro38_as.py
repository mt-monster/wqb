# -*- coding: utf-8 -*-
"""提交 AS 批: macro38 冠军骨架精调 (MAHILO/ADX/CCI), 混合 decay (2/4/8), SUBIND。"""
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

async def submit_group(tag, exprs, decay, neutralization):
    payload = []
    for expr in exprs:
        settings = dict(BASE, decay=decay, neutralization=neutralization)
        payload.append({'type': 'REGULAR', 'settings': settings, 'regular': expr})
    resp = await client._request('POST', f'{client.base_url}/simulations', json=payload)
    loc = resp.headers.get('Location', '')
    print(f'[{tag}] n={len(exprs)} decay={decay} neut={neutralization} status={resp.status_code} -> {loc}')
    if resp.status_code != 201:
        print('  BODY:', resp.text[:500])
    return loc

async def main():
    await client.ensure_authenticated()
    exprs = load(r'd:\coding\traeCN_project\wqb\tracking\USA\runs\usa_macro38_batch_as.txt')
    # #1 decay2 (MAHILO margin 解锁测试)
    await submit_group('AS-d2', [exprs[0]], 2, 'SUBINDUSTRY')
    time.sleep(3)
    # #5 decay8 (CCI 压换手)
    await submit_group('AS-d8', [exprs[4]], 8, 'SUBINDUSTRY')
    time.sleep(3)
    # 其余 decay4
    rest = [exprs[i] for i in [1, 2, 3, 5, 6, 7]]
    await submit_group('AS-d4', rest, 4, 'SUBINDUSTRY')
    time.sleep(5)
    print('ALL SUBMITTED')

asyncio.run(main())
