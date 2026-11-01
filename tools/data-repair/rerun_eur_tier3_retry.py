#!/usr/bin/env python3
"""Retry failed Tier 3 EUR alphas using batch_create_simulations (proper Location header parsing)."""
import json
import asyncio
import sys
import os
sys.path.insert(0, '/d/coding/traeCN_project/wqb/world-quant-brain-mcp')

from brain_api import brain_client

FAILED = [
    ("omE3O6ok", "group_neutralize(group_scale(add(signed_power(group_zscore(divide(subtract(est_12m_eps_raisednum_4wks, est_12m_eps_lowerednum_4wks), est_12m_eps_num_4wks_ago), subindustry), 2.25), multiply(1.2, group_rank(imb5_score, subindustry))), industry), market)"),
    ("zq3J67rK", "group_neutralize(group_scale(add(signed_power(group_zscore(divide(subtract(est_12m_eps_raised_1wk, est_12m_eps_lowered_1wk), est_12m_eps_num), subindustry), 1.5), multiply(1.2, group_rank(imb5_score, subindustry))), industry), market)"),
    ("88RKbLAX", "group_neutralize(group_scale(add(signed_power(group_zscore(divide(est_12m_gps_raisednum_4wks, est_12m_gps_num_4wks_ago), subindustry), 1.5), multiply(1.2, group_rank(imb5_score, subindustry))), industry), market)"),
    ("O0A5O9eJ", "group_neutralize(group_scale(add(signed_power(group_zscore(divide(est_12m_ebt_raisednum_4wks, est_12m_ebt_num_4wks_ago), subindustry), 1.5), multiply(1.2, group_rank(divide(ts_mean(vec_sum(mcr27_company_ajnet), 66), ts_mean(vec_sum(num_jobs_active), 66)), subindustry))), industry), market)"),
    ("mLoxpXOX", "group_neutralize(group_scale(add(signed_power(group_zscore(divide(est_12m_ebt_raisednum_4wks, est_12m_ebt_num_4wks_ago), subindustry), 2.1), multiply(1.2, group_rank(divide(ts_mean(vec_sum(num_jobs_created), 66), ts_mean(vec_sum(num_jobs_active), 66)), subindustry))), industry), market)"),
    ("d5WEeNdv", "group_neutralize(group_scale(add(signed_power(group_zscore(divide(subtract(est_12m_eps_raisednum_4wks, est_12m_eps_lowerednum_4wks), est_12m_eps_num_4wks_ago), subindustry), 1.5), multiply(1.2, group_rank(divide(subtract(count_institutional_buyers_security, count_institutional_sellers_security), add(count_institutional_buyers_security, count_institutional_sellers_security)), subindustry))), industry), market)"),
    ("9qxAkowd", "group_neutralize(group_scale(add(signed_power(group_zscore(divide(est_12m_ebt_raisednum_4wks, est_12m_ebt_num_4wks_ago), subindustry), 2.1), multiply(1.2, group_rank(count_institutional_holders_security, subindustry))), industry), market)"),
    ("RREk399d", "group_neutralize(group_scale(add(signed_power(group_zscore(divide(subtract(est_12m_roe_raisednum_4wks, est_12m_roe_lowerednum_4wks), est_12m_roe_num_4wks_ago), subindustry), 1.5), multiply(1.2, group_rank(ts_mean(vec_sum(stable_boundary_trade_count_21d), 22), subindustry))), industry), market)"),
    ("O0A5Ovpd", "group_neutralize(group_scale(add(signed_power(group_zscore(multiply(-1, divide(subtract(est_12m_ebt_high, est_12m_ebt_low), abs(est_12m_ebt_mean))), subindustry), 1.5), multiply(1.2, group_rank(imb5_score, subindustry))), industry), market)"),
    ("xArmOOaw", "add(group_zscore(divide(subtract(est_12m_dps_raisednum_4wks, est_12m_dps_lowerednum_4wks), est_12m_dps_num_4wks_ago), subindustry), multiply(1.2, group_rank(divide(ts_mean(vec_sum(mcr27_company_ajnet), 66), ts_mean(vec_sum(num_jobs_active), 66)), subindustry)))"),
]

BASE_SETTINGS = {
    'instrumentType': 'EQUITY', 'region': 'EUR', 'universe': 'TOP2500',
    'delay': 1, 'decay': 40, 'neutralization': 'FAST', 'truncation': 0.08,
    'pasteurization': 'ON', 'language': 'FASTEXPR', 'visualization': False,
    'testPeriod': 'P0Y0M', 'maxTrade': 'OFF', 'unitHandling': 'VERIFY', 'nanHandling': 'OFF',
}


async def main():
    # Load existing results
    existing = {}
    map_path = 'results/eur_tier3_map.json'
    if os.path.exists(map_path):
        with open(map_path) as f:
            existing = json.load(f).get('results', {})

    results = dict(existing)
    remaining = [(oid, code) for oid, code in FAILED if oid not in results]

    if not remaining:
        print("All Tier 3 items already submitted!")
        return

    print(f"Retrying {len(remaining)} failed Tier 3 items...")

    for i, (oid, code) in enumerate(remaining):
        payload = {'type': 'REGULAR', 'settings': dict(BASE_SETTINGS), 'regular': code}
        for attempt in range(5):
            try:
                await brain_client.ensure_authenticated()
                result = await brain_client.batch_create_simulations([payload])
                r = result.get('results', [{}])[0]
                if r.get('ok'):
                    sid = r.get('simulation_id')
                    results[oid] = sid
                    print(f'OK: {oid} -> {sid}', flush=True)
                    break
                else:
                    err_msg = r.get('error', '?')
                    print(f'  {oid}: batch fail attempt {attempt+1}/5: {err_msg}', flush=True)
                    await asyncio.sleep(20 * (attempt + 1))
            except Exception as e:
                print(f'  {oid}: ERR {e} attempt {attempt+1}/5', flush=True)
                await asyncio.sleep(20 * (attempt + 1))
        else:
            print(f'FAIL: {oid} after 5 attempts', flush=True)

        if i < len(remaining) - 1:
            await asyncio.sleep(20)

    # Save
    with open(map_path, 'w') as f:
        json.dump({"items": [{"original_id": oid, "code": code} for oid, code in FAILED],
                    "results": results}, f, indent=2, ensure_ascii=False)

    print(f'\n=== Tier 3 retry: {len(results)} total ===')
    for oid, sid in sorted(results.items()):
        print(f'  {oid}: {sid}')

asyncio.run(main())