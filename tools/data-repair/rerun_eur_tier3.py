#!/usr/bin/env python3
"""Re-run Tier 3 EUR alphas (IS 1.5-1.79) with maxTrade=OFF."""
import json
import asyncio
import sys
import os
sys.path.insert(0, '/d/coding/traeCN_project/wqb/world-quant-brain-mcp')

from brain_api import brain_client

EXPRESSIONS = [
    ("RREkjZw1", "group_neutralize(group_scale(add(signed_power(group_zscore(divide(est_12m_ebt_raisednum_4wks, est_12m_ebt_num_4wks_ago), subindustry), 2.1), multiply(1.2, group_rank(imb5_score, subindustry))), industry), market)"),
    ("vR1JM723", "group_neutralize(group_scale(add(signed_power(group_zscore(divide(subtract(est_12m_ebt_raised_1wk, est_12m_ebt_lowered_1wk), est_12m_ebt_num), subindustry), 1.6), multiply(1.2, group_rank(imb5_score, subindustry))), industry), market)"),
    ("xArmAbnw", "group_neutralize(group_scale(add(signed_power(group_zscore(divide(subtract(est_12m_dps_raisednum_4wks, est_12m_dps_lowerednum_4wks), est_12m_dps_num_4wks_ago), subindustry), 1.5), multiply(1.2, group_rank(imb5_score, subindustry))), industry), market)"),
    ("zq3JKw78", "group_neutralize(group_scale(add(signed_power(group_zscore(divide(est_12m_ebi_raisednum_4wks, est_12m_ebi_num_4wks_ago), subindustry), 1.5), multiply(1.2, group_rank(imb5_score, subindustry))), industry), market)"),
    ("qMLmp1eP", "group_neutralize(group_scale(add(signed_power(group_zscore(divide(est_12m_ebt_raisednum_4wks, est_12m_ebt_num_4wks_ago), subindustry), 1.5), multiply(1.2, group_rank(vec_avg(snl27_kurtosis), subindustry))), industry), market)"),
    ("2rAn2eOY", "group_neutralize(group_scale(add(signed_power(group_zscore(divide(est_12m_ebt_raisednum_4wks, est_12m_ebt_num_4wks_ago), subindustry), 1.5), multiply(1.2, group_rank(vec_avg(mcr27_company_ajnet), subindustry))), industry), market)"),
    ("WjOWJVoQ", "add(group_zscore(divide(subtract(est_12m_eps_raisednum_4wks, est_12m_eps_lowerednum_4wks), est_12m_eps_num_4wks_ago), subindustry), multiply(1.2, group_rank(vec_avg(snl27_totaldomains), subindustry)))"),
    ("3qonqVA0", "group_neutralize(group_scale(add(signed_power(group_zscore(divide(subtract(est_12m_dps_raisednum_4wks, est_12m_dps_lowerednum_4wks), est_12m_dps_num_4wks_ago), subindustry), 1.5), multiply(1.8, group_rank(imb5_score, subindustry))), industry), market)"),
    ("omE3O6ok", "group_neutralize(group_scale(add(signed_power(group_zscore(divide(subtract(est_12m_eps_raisednum_4wks, est_12m_eps_lowerednum_4wks), est_12m_eps_num_4wks_ago), subindustry), 2.25), multiply(1.2, group_rank(imb5_score, subindustry))), industry), market)"),
    ("zq3J67rK", "group_neutralize(group_scale(add(signed_power(group_zscore(divide(subtract(est_12m_eps_raised_1wk, est_12m_eps_lowered_1wk), est_12m_eps_num), subindustry), 1.5), multiply(1.2, group_rank(imb5_score, subindustry))), industry), market)"),
    ("88RKbLAX", "group_neutralize(group_scale(add(signed_power(group_zscore(divide(est_12m_gps_raisednum_4wks, est_12m_gps_num_4wks_ago), subindustry), 1.5), multiply(1.2, group_rank(imb5_score, subindustry))), industry), market)"),
    ("O0A5O9eJ", "group_neutralize(group_scale(add(signed_power(group_zscore(divide(est_12m_ebt_raisednum_4wks, est_12m_ebt_num_4wks_ago), subindustry), 1.5), multiply(1.2, group_rank(divide(ts_mean(vec_sum(mcr27_company_ajnet), 66), ts_mean(vec_sum(num_jobs_active), 66)), subindustry))), industry), market)"),
    ("kqN1b19K", "group_neutralize(group_scale(signed_power(group_zscore(divide(subtract(est_12m_roe_raisednum_4wks, est_12m_roe_lowerednum_4wks), est_12m_roe_num_4wks_ago), subindustry), 1.5), industry), market)"),
    ("3qonJe1N", "add(group_zscore(divide(subtract(est_12m_dps_raisednum_4wks, est_12m_dps_lowerednum_4wks), est_12m_dps_num_4wks_ago), subindustry), multiply(1.2, group_rank(vec_avg(snl27_totalcountrydomains), subindustry)))"),
    ("LLMlj7R1", "group_neutralize(group_scale(add(signed_power(group_zscore(divide(subtract(ptg_raisednum_4wks, ptg_lowerednum_4wks), add(ptg_raisednum_4wks, ptg_lowerednum_4wks)), subindustry), 1.5), multiply(1.2, group_rank(divide(ts_mean(vec_sum(num_jobs_created), 66), ts_mean(vec_sum(num_jobs_active), 66)), subindustry))), industry), market)"),
    ("Jje5M0al", "group_neutralize(group_scale(add(signed_power(group_zscore(divide(est_12m_eps_raisednum_4wks, est_12m_eps_num_4wks_ago), subindustry), 1.5), multiply(1.2, group_rank(imb5_score, subindustry))), industry), market)"),
    ("zq3JeRg8", "add(group_zscore(divide(subtract(est_12m_dps_raisednum_4wks, est_12m_dps_lowerednum_4wks), est_12m_dps_num_4wks_ago), subindustry), multiply(1.2, group_rank(vec_avg(mcr27_company_jobsactive), subindustry)))"),
    ("qMLm8QdA", "group_neutralize(group_scale(add(signed_power(group_zscore(divide(subtract(est_12m_cps_raisednum_4wks, est_12m_cps_lowerednum_4wks), est_12m_cps_num_4wks_ago), subindustry), 1.5), multiply(1.2, group_rank(imb5_score, subindustry))), industry), market)"),
    ("vR1JP0Lr", "group_neutralize(group_scale(add(signed_power(group_zscore(divide(est_12m_ebt_raisednum_4wks, est_12m_ebt_num_4wks_ago), subindustry), 2.1), multiply(1.2, group_rank(vec_avg(mcr27_company_ajnet), subindustry))), industry), market)"),
    ("vR1JoPr3", "group_neutralize(group_scale(add(signed_power(group_zscore(divide(est_12m_ebt_raisednum_4wks, est_12m_ebt_num_4wks_ago), subindustry), 1.8), multiply(1.2, group_rank(count_institutional_holders_security, subindustry))), industry), market)"),
    ("mLoxpXOX", "group_neutralize(group_scale(add(signed_power(group_zscore(divide(est_12m_ebt_raisednum_4wks, est_12m_ebt_num_4wks_ago), subindustry), 2.1), multiply(1.2, group_rank(divide(ts_mean(vec_sum(num_jobs_created), 66), ts_mean(vec_sum(num_jobs_active), 66)), subindustry))), industry), market)"),
    ("d5WEeNdv", "group_neutralize(group_scale(add(signed_power(group_zscore(divide(subtract(est_12m_eps_raisednum_4wks, est_12m_eps_lowerednum_4wks), est_12m_eps_num_4wks_ago), subindustry), 1.5), multiply(1.2, group_rank(divide(subtract(count_institutional_buyers_security, count_institutional_sellers_security), add(count_institutional_buyers_security, count_institutional_sellers_security)), subindustry))), industry), market)"),
    ("9qxAkowd", "group_neutralize(group_scale(add(signed_power(group_zscore(divide(est_12m_ebt_raisednum_4wks, est_12m_ebt_num_4wks_ago), subindustry), 2.1), multiply(1.2, group_rank(count_institutional_holders_security, subindustry))), industry), market)"),
    ("RREk399d", "group_neutralize(group_scale(add(signed_power(group_zscore(divide(subtract(est_12m_roe_raisednum_4wks, est_12m_roe_lowerednum_4wks), est_12m_roe_num_4wks_ago), subindustry), 1.5), multiply(1.2, group_rank(ts_mean(vec_sum(stable_boundary_trade_count_21d), 22), subindustry))), industry), market)"),
    ("O0A5Ovpd", "group_neutralize(group_scale(add(signed_power(group_zscore(multiply(-1, divide(subtract(est_12m_ebt_high, est_12m_ebt_low), abs(est_12m_ebt_mean))), subindustry), 1.5), multiply(1.2, group_rank(imb5_score, subindustry))), industry), market)"),
    ("pwd13KxV", "add(group_zscore(divide(subtract(est_12m_dps_raisednum_4wks, est_12m_dps_lowerednum_4wks), est_12m_dps_num_4wks_ago), subindustry), multiply(1.2, group_rank(divide(vec_avg(snl27_topranking), vec_avg(snl27_avgranking)), subindustry)))"),
    ("xArmOOaw", "add(group_zscore(divide(subtract(est_12m_dps_raisednum_4wks, est_12m_dps_lowerednum_4wks), est_12m_dps_num_4wks_ago), subindustry), multiply(1.2, group_rank(divide(ts_mean(vec_sum(mcr27_company_ajnet), 66), ts_mean(vec_sum(num_jobs_active), 66)), subindustry)))"),
    ("omE9mWln", "group_neutralize(group_scale(add(signed_power(group_zscore(divide(subtract(est_12m_pre_mean, est_12m_pre_mean_4wks_ago), est_12m_pre_std), subindustry), 1.4), multiply(1.2, group_rank(imb5_score, subindustry))), industry), market)"),
]

BASE_SETTINGS = {
    'instrumentType': 'EQUITY', 'region': 'EUR', 'universe': 'TOP2500',
    'delay': 1, 'decay': 40, 'neutralization': 'FAST', 'truncation': 0.08,
    'pasteurization': 'ON', 'language': 'FASTEXPR', 'visualization': False,
    'testPeriod': 'P0Y0M', 'maxTrade': 'OFF', 'unitHandling': 'VERIFY', 'nanHandling': 'OFF',
}


async def main():
    results = {}
    remaining = list(EXPRESSIONS)

    for round_num in range(10):
        if not remaining:
            break
        batch = remaining[:3]
        remaining = remaining[3:]

        payloads = []
        for oid, code in batch:
            payloads.append({'type': 'REGULAR', 'settings': dict(BASE_SETTINGS), 'regular': code})

        try:
            result = await brain_client.batch_create_simulations(payloads)
            for p, r in zip(batch, result.get("results", [])):
                oid = p[0]
                if r.get('ok'):
                    sid = r.get('simulation_id', '?')
                    results[oid] = sid
                    print(f'OK: {oid} -> {sid}', flush=True)
                else:
                    print(f'FAIL: {oid} (retrying)', flush=True)
        except Exception as e:
            print(f'ERR: {e}', flush=True)

        if remaining:
            await asyncio.sleep(45)

    print(f'\n=== Tier 3: {len(results)}/{len(EXPRESSIONS)} success ===', flush=True)
    for oid, sid in results.items():
        print(f'  {oid}: {sid}', flush=True)

    with open('/d/coding/traeCN_project/wqb/results/eur_tier3_map.json', 'w') as f:
        json.dump({"items": [{"original_id": oid, "code": code[:80]} for oid, code in EXPRESSIONS],
                    "results": results}, f, indent=2, ensure_ascii=False)

asyncio.run(main())