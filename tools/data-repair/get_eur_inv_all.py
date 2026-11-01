#!/usr/bin/env python3
"""Query investabilityConstrained data for ALL EUR alphas (Tier 1+2+3)."""
import json
import asyncio
import sys
import os
import time
sys.path.insert(0, '/d/coding/traeCN_project/wqb/world-quant-brain-mcp')

from brain_api import brain_client

# Collect alpha IDs from all poll results
ALPHA_IDS = {}
for tier in ['tier1', 'tier2', 'tier3']:
    path = f'results/eur_{tier}_poll.json'
    if os.path.exists(path):
        with open(path) as f:
            data = json.load(f)
        for tag, info in data.items():
            if info.get('status') == 'COMPLETE' and info.get('alpha'):
                ALPHA_IDS[info['alpha']] = info

# Add retry poll
retry_path = 'results/eur_tier3_retry_poll.json'
if os.path.exists(retry_path):
    with open(retry_path) as f:
        data = json.load(f)
    for tag, info in data.items():
        if info.get('status') == 'COMPLETE' and info.get('alpha'):
            ALPHA_IDS[info['alpha']] = info

print(f"Total unique alpha IDs to query: {len(ALPHA_IDS)}")

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
            'sharpe': is_data.get('sharpe'),
            'fitness': is_data.get('fitness'),
        }
    except Exception as e:
        return aid, {'error': str(e)}

async def main():
    results = {}
    todo = list(ALPHA_IDS.keys())
    t0 = time.time()

    while todo:
        batch = todo[:5]
        todo = todo[5:]
        tasks = [query_one(aid) for aid in batch]
        for coro in asyncio.as_completed(tasks):
            aid, data = await coro
            results[aid] = data
            pdata = ALPHA_IDS.get(aid, {})
            fails = pdata.get('checks_fail', [])
            status = '✅' if not fails else f'❌{len(fails)}'
            inv_s = data.get('inv_sharpe')
            print(f'  {aid}: inv_S={inv_s} inv_F={data.get("inv_fitness")} '
                  f'S={data.get("sharpe")} F={data.get("fitness")} {status}', flush=True)
        if todo:
            await asyncio.sleep(3)

    # Merge with poll data
    merged = {}
    for aid, idata in results.items():
        pdata = ALPHA_IDS.get(aid, {})
        merged[aid] = {
            'inv_sharpe': idata.get('inv_sharpe'),
            'inv_fitness': idata.get('inv_fitness'),
            'inv_turnover': idata.get('inv_turnover'),
            'inv_returns': idata.get('inv_returns'),
            'sharpe': idata.get('sharpe'),
            'fitness': idata.get('fitness'),
            'checks_fail': pdata.get('checks_fail', []),
            'ladder': pdata.get('ladder'),
        }

    with open('results/eur_inv_data_all.json', 'w') as f:
        json.dump(merged, f, indent=2, ensure_ascii=False)

    print(f'\n=== Done: {len(merged)} alphas in {time.time()-t0:.0f}s ===')

    # RA-failure-free
    ready = {k: v for k, v in merged.items() if not v['checks_fail']}
    print(f'\nRA-failure-free: {len(ready)}/{len(merged)}')
    for aid, v in sorted(ready.items(), key=lambda x: -(x[1].get('inv_sharpe') or 0)):
        print(f'  {aid}: inv_S={v["inv_sharpe"]} inv_F={v["inv_fitness"]} S={v["sharpe"]} F={v["fitness"]} 2Y={v["ladder"]}')

    # Stats
    inv_vals = [v['inv_sharpe'] for v in merged.values() if v.get('inv_sharpe')]
    if inv_vals:
        print(f'\nInv Sharpe range: {min(inv_vals):.2f} - {max(inv_vals):.2f}')
        print(f'Wavg inv Sharpe (all): {sum(inv_vals)/len(inv_vals):.2f}')
    ready_inv = [v['inv_sharpe'] for v in ready.values() if v.get('inv_sharpe')]
    if ready_inv:
        print(f'Wavg inv Sharpe (RA-ready): {sum(ready_inv)/len(ready_inv):.2f}')

asyncio.run(main())