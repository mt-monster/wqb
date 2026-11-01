#!/usr/bin/env python3
"""Query investabilityConstrained data for EUR alphas from Tier 1 & Tier 2."""
import json
import asyncio
import sys
import os
sys.path.insert(0, '/d/coding/traeCN_project/wqb/world-quant-brain-mcp')

from brain_api import brain_client

# Collect alpha IDs from poll results
ALPHA_IDS = set()
for tier in ['tier1', 'tier2']:
    path = f'results/eur_{tier}_poll.json'
    if os.path.exists(path):
        with open(path) as f:
            data = json.load(f)
        for tag, info in data.items():
            if info.get('status') == 'COMPLETE' and info.get('alpha'):
                ALPHA_IDS.add(info['alpha'])

print(f"Total unique alpha IDs to query: {len(ALPHA_IDS)}")
print(f"Alpha IDs: {sorted(ALPHA_IDS)}")

async def query_one(aid):
    try:
        await brain_client.ensure_authenticated()
        r = await brain_client._request('GET', f'{brain_client.base_url}/alphas/{aid}')
        if r.status_code != 200:
            return aid, {'error': f'HTTP {r.status_code}'}
        j = r.json()
        is_data = j.get('is') or {}
        inv = is_data.get('investabilityConstrained') or {}
        return aid, {
            'inv_sharpe': inv.get('sharpe'),
            'inv_fitness': inv.get('fitness'),
            'inv_turnover': inv.get('turnover'),
            'inv_returns': inv.get('returns'),
            'inv_pnl': inv.get('pnl'),
            'sharpe': is_data.get('sharpe'),
            'fitness': is_data.get('fitness'),
            'turnover': is_data.get('turnover'),
            'checks_fail': [c.get('name') for c in (is_data.get('checks') or []) if c.get('result') == 'FAIL'],
        }
    except Exception as e:
        return aid, {'error': str(e)}

async def main():
    results = {}
    todo = list(ALPHA_IDS)
    t0 = __import__('time').time()

    while todo:
        batch = todo[:5]
        todo = todo[5:]
        tasks = [query_one(aid) for aid in batch]
        for coro in asyncio.as_completed(tasks):
            aid, data = await coro
            results[aid] = data
            if 'error' in data:
                print(f'  {aid}: ERROR {data["error"]}', flush=True)
            else:
                print(f'  {aid}: inv_S={data["inv_sharpe"]} inv_F={data["inv_fitness"]} '
                      f'S={data["sharpe"]} F={data["fitness"]} fails={data["checks_fail"]}', flush=True)
        if todo:
            await asyncio.sleep(3)

    with open('results/eur_inv_data.json', 'w') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    print(f'\n=== Done: {len(results)} alphas queried in {__import__("time").time()-t0:.0f}s ===')
    # Summary
    ready = {k: v for k, v in results.items() if not v.get('checks_fail') and v.get('inv_sharpe')}
    print(f'RA-failure-free with inv data: {len(ready)}')
    for aid, v in sorted(ready.items(), key=lambda x: -(x[1].get('inv_sharpe') or 0)):
        print(f'  {aid}: inv_S={v["inv_sharpe"]:.2f} inv_F={v["inv_fitness"]:.2f} S={v["sharpe"]:.2f} F={v["fitness"]:.2f}')

asyncio.run(main())