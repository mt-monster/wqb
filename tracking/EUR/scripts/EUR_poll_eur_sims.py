#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
"""Poll EUR multisimulation results until complete (max 15 min)."""
import sys, time, json, os
sys.path.insert(0, os.path.join(os.path.expanduser("~"), ".zcode", "skills", "shared_libs"))
import ace_lib
ace_lib.get_credentials = lambda: ('mthyzx@126.com', 'asdqwe123!')
from ace_lib import start_session

session = start_session()
base = ace_lib.brain_api_url
mids = ['eBVNK4Rj4qU9NgaA1SurLZ', 'rLpsDgAo4HQbze1fxziHW9V']
out_path = r'D:\coding\traeCN_project\wqb\tracking\EUR\results\EUR_sim_results.json'

deadline = time.time() + 900  # 15 min
results = {}
seen_ids = set()

while time.time() < deadline:
    for mid in mids:
        try:
            r = session.get(f'{base}/simulations/{mid}')
            if r.status_code != 200:
                continue
            data = r.json()
            children = data.get('children', [])
            for ch in children:
                if isinstance(ch, str) and '/simulations/' in ch:
                    sim_id = ch.split('/')[-1]
                elif isinstance(ch, dict):
                    sim_id = ch.get('id', '')
                else:
                    continue
                if not sim_id or sim_id in results:
                    continue
                seen_ids.add(sim_id)
                sr = session.get(f'{base}/simulations/{sim_id}')
                if sr.status_code != 200:
                    continue
                sd = sr.json()
                status = sd.get('status', '')
                entry = {'status': status, 'parent': mid, 'code': sd.get('code', '')}
                if status == 'COMPLETE':
                    isum = sd.get('is', {}) or {}
                    entry['sharpe'] = isum.get('sharpe')
                    entry['fitness'] = isum.get('fitness')
                    entry['turnover'] = isum.get('turnover')
                    entry['margin'] = isum.get('margin')
                    entry['returns'] = isum.get('returns')
                    entry['two_year_sharpe'] = isum.get('IS_LADDER_SHARPE', isum.get('two_year_sharpe'))
                    entry['long_count'] = isum.get('longCount')
                    entry['short_count'] = isum.get('shortCount')
                elif status in ('ERROR', 'CANCELLED'):
                    entry['error'] = sd.get('message', sd.get('error', ''))
                results[sim_id] = entry
                print(f"[{time.strftime('%H:%M:%S')}] {sim_id} -> {status}", flush=True)
        except Exception as e:
            print(f"[warn] {mid}: {e}", flush=True)

    if len(results) >= 11:
        break
    # print heartbeat
    print(f"[{time.strftime('%H:%M:%S')}] polled, {len(results)}/11 done", flush=True)
    time.sleep(20)

os.makedirs(os.path.dirname(out_path), exist_ok=True)
with open(out_path, 'w', encoding='utf-8') as f:
    json.dump(results, f, indent=2, ensure_ascii=False)

print('\n=== EUR 回测结果汇总 ===')
completed = sum(1 for v in results.values() if v.get('status') == 'COMPLETE')
for sim_id, info in results.items():
    if info.get('status') == 'COMPLETE':
        print(f"  ✅ {info.get('code','')[:65]}")
        print(f"     S={info.get('sharpe')} F={info.get('fitness')} T={info.get('turnover')} "
              f"M={info.get('margin')} R={info.get('returns')} 2Y={info.get('two_year_sharpe')} L/S={info.get('long_count')}/{info.get('short_count')}")
    else:
        print(f"  ❌ {info.get('code','')[:60]} -> {info.get('status')} {info.get('error','')}")
print(f'COMPLETE: {completed}/11')
print(f'Saved: {out_path}')
