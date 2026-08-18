# -*- coding: utf-8 -*-
"""等待 multisim 完成并输出指标表（simulation→children→alpha 两级拉取）。
用法: python _wait_sims.py <mid1> <mid2> ...
输出每行 JSON: alpha, GATE, fails, 及 is 指标 + settings。"""
import sys, os, time, asyncio, json

MCP_DIR = r'd:\coding\traeCN_project\wqb\world-quant-brain-mcp'
os.chdir(MCP_DIR)
sys.path.insert(0, MCP_DIR)

from brain_api import BrainApiClient  # noqa: E402

client = BrainApiClient()
BASE = f'{client.base_url}/simulations'

GATES = {'sharpe': 1.58, 'fitness': 1.0, 'sharpe2y': 1.6, 'margin': 5.0,
         'turnover_min': 5.0, 'turnover_max': 30.0, 'rn_sharpe': 1.0,
         'rn_fitness': 0.7, 'rn_margin': 5.0}


def fmt(v, nd=2):
    return f'{v:.{nd}f}' if isinstance(v, (int, float)) else str(v)


def gate_check(m):
    fails = []
    if m['sharpe'] is None or m['sharpe'] < GATES['sharpe']:
        fails.append(f"sharpe={fmt(m['sharpe'])}<1.58")
    if m['fitness'] is None or m['fitness'] < GATES['fitness']:
        fails.append(f"fit={fmt(m['fitness'])}<1.0")
    if m['sharpe2y'] is None or m['sharpe2y'] < GATES['sharpe2y']:
        fails.append(f"2y={fmt(m['sharpe2y'])}<1.6")
    if m['margin'] is None or m['margin'] * 100 < GATES['margin']:
        fails.append(f"margin={fmt(m['margin']*100 if m['margin'] is not None else None, 1)}bp<5")
    tv = m['turnover'] * 100 if m['turnover'] is not None else None
    if tv is None or tv < GATES['turnover_min']:
        fails.append(f"tv={fmt(tv,1)}<5%")
    if tv is not None and tv > GATES['turnover_max']:
        fails.append(f"tv={fmt(tv,1)}>30%")
    if m.get('ra_failed_count') not in (None, 0):
        fails.append(f"ra_fail={m['ra_failed_count']}")
    return (len(fails) == 0, fails)


async def fetch_alpha(aid):
    """拉 alpha 对象 is 指标。"""
    r = await client._request('GET', f'{client.base_url}/alphas/{aid}?include_properties=true')
    a = r.json()
    is_ = a.get('is') or {}
    rn = is_.get('riskNeutralized') or {}
    s = a.get('settings', {})
    checks = {c['name']: c.get('value') for c in is_.get('checks', [])}
    return {
        'alpha': aid,
        'sharpe': is_.get('sharpe'), 'fitness': is_.get('fitness'),
        'turnover': is_.get('turnover'), 'margin': is_.get('margin'),
        # 平台 2026-08 将 LOW_2Y_SHARPE 改名 IS_LADDER_SHARPE (同槽位新检查), 兼容两者
        'sharpe2y': checks.get('IS_LADDER_SHARPE', checks.get('LOW_2Y_SHARPE')),
        'returns': is_.get('returns'), 'drawdown': is_.get('drawdown'),
        'longCount': is_.get('longCount'), 'shortCount': is_.get('shortCount'),
        'subU': checks.get('LOW_SUB_UNIVERSE_SHARPE'),
        'cluster': checks.get('CLUSTER_TEST'),
        'rn_sharpe': rn.get('sharpe'), 'rn_fitness': rn.get('fitness'),
        'rn_margin': rn.get('margin'),
        'universe': s.get('universe'), 'delay': s.get('delay'),
        'decay': s.get('decay'), 'neutralization': s.get('neutralization'),
        'days': is_.get('days'), 'check_low_sharpe': checks.get('LOW_SHARPE'),
    }


async def fetch(mid):
    resp = await client._request('GET', f'{BASE}/{mid}')
    data = resp.json()
    children = data.get('children') or []
    out = {}
    for cid in children:
        r2 = await client._request('GET', f'{BASE}/{cid}')
        a = r2.json()
        aid = a.get('alpha')
        if aid:
            out[aid] = await fetch_alpha(aid)
    return data.get('status'), out


async def main():
    await client.ensure_authenticated()
    mids = sys.argv[1:]
    t0 = time.time()
    while time.time() - t0 < 600:
        all_done = True
        for mid in mids:
            status, out = await fetch(mid)
            done = status in ('COMPLETE', 'CANCELLED', 'ERROR')
            if not done:
                all_done = False
                print(f'[{mid}] {status} n={len(out)}')
        if all_done:
            break
        time.sleep(20)
    print('=== FINAL ===')
    for mid in mids:
        status, out = await fetch(mid)
        print(f'=== {mid} status={status} n={len(out)} ===')
        for alpha, m in out.items():
            try:
                ok, fails = gate_check(m)
                print(json.dumps({'alpha': alpha, 'GATE': 'PASS' if ok else 'FAIL',
                                  'fails': fails, **m}, ensure_ascii=False, default=str))
            except Exception as e:
                print(f'[PRINT_ERR {alpha}] {e}')
    print('DONE')

asyncio.run(main())
