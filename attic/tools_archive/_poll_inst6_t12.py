# -*- coding: utf-8 -*-
"""轮询 inst6 T1/T2 批 multisim 结果并输出指标表。"""
import sys, os, time, asyncio, json

MCP_DIR = r'd:\coding\traeCN_project\wqb\world-quant-brain-mcp'
os.chdir(MCP_DIR)
sys.path.insert(0, MCP_DIR)

from brain_api import BrainApiClient  # noqa: E402

client = BrainApiClient()
BASE = f'{client.base_url}/simulations'

KEYS = ['sharpe', 'fitness', 'turnover', 'margin', 'sharpe2y', 'returns',
        'longCount', 'shortCount', 'ra_failed_count', 'universe',
        'delay', 'decay', 'neutralization', 'days', 'subUniverse', 'prod']
RN = ['rn_sharpe', 'rn_fitness', 'rn_margin', 'rn_turnover', 'rn_ra_failed_count']


async def fetch_multisim(mid):
    """拉 multisim 并返回 {alpha_id: metrics}。"""
    out = {}
    resp = await client._request('GET', f'{BASE}/{mid}')
    data = resp.json()
    for a in data.get('simulations', []):
        m = a.get('settings', {})
        alpha = a.get('alpha', '')
        if not alpha:
            alpha = a.get('id', '?')
        out[alpha] = {
            'sharpe': a.get('sharpe'), 'fitness': a.get('fitness'),
            'turnover': a.get('turnover'), 'margin': a.get('margin'),
            'sharpe2y': a.get('sharpe2y'), 'returns': a.get('returns'),
            'longCount': a.get('longCount'), 'shortCount': a.get('shortCount'),
            'ra_failed_count': a.get('ra_failed_count'),
            'universe': m.get('universe'), 'delay': m.get('delay'),
            'decay': m.get('decay'), 'neutralization': m.get('neutralization'),
            'days': a.get('days'), 'subUniverse': m.get('subUniverse'),
            'prod': a.get('is_prod'),
        }
        for k in RN:
            out[alpha][k] = a.get(k)
    return data.get('status', '?'), out


async def main():
    await client.ensure_authenticated()
    mids = sys.argv[1:] or ['aInFTd2m54Zc2eEvZbZar0', '1RYSQiaC4ZkaVhWBp8euRD']
    for mid in mids:
        status, out = await fetch_multisim(mid)
        print(f'=== {mid} status={status} n={len(out)} ===')
        for alpha, m in out.items():
            print(json.dumps({'alpha': alpha, **m}, ensure_ascii=False))
        if status not in ('COMPLETE', 'CANCELLED'):
            print(f'  [NOT READY: {status}]')
        time.sleep(2)

asyncio.run(main())
