#!/usr/bin/env python3
"""Retry failed Tier 2 EUR alphas (429 rate limit)."""
import json
import asyncio
import sys
import os
sys.path.insert(0, '/d/coding/traeCN_project/wqb/world-quant-brain-mcp')

from brain_api import brain_client

# Failed Tier 2 items from first attempt
FAILED = [
    ("bl6WGGpp", "trade_when(greater(mcr10_value, ts_quantile(mcr10_value, 504)), group_neutralize(group_scale(add(signed_power(group_zscore(divide(subtract(est_12m_ebt_raisednum_4wks, est_12m_ebt_lowerednum_4wks), est_12m_ebt_num_4wks_ago), subindustry), 2.1), multiply(1.2, group_rank(imb5_score, subindustry))), industry), market), 0)"),
    ("JjegKxPn", "group_neutralize(group_scale(add(signed_power(group_zscore(divide(subtract(est_12m_eps_raisednum_4wks, est_12m_eps_lowerednum_4wks), est_12m_eps_num_4wks_ago), subindustry), 1.125), multiply(1.2, group_rank(imb5_score, subindustry))), industry), market)"),
    ("RREko30o", "group_neutralize(group_scale(add(signed_power(group_zscore(divide(est_12m_dps_raisednum_4wks, est_12m_dps_num_4wks_ago), subindustry), 1.5), multiply(1.2, group_rank(vec_avg(snl27_top75pctrankingavg), subindustry))), industry), market)"),
    ("78LKlOw1", "group_neutralize(group_scale(add(signed_power(group_zscore(divide(est_12m_dps_raisednum_4wks, est_12m_dps_num_4wks_ago), subindustry), 1.5), multiply(1.2, group_rank(vec_avg(snl27_kurtosis), subindustry))), industry), market)"),
    ("LLMgJ9ZM", "group_neutralize(group_scale(add(signed_power(group_zscore(divide(subtract(est_12m_eps_raisednum_4wks, est_12m_eps_lowerednum_4wks), est_12m_eps_num_4wks_ago), subindustry), 1.5), multiply(1.5, group_rank(imb5_score, subindustry))), industry), market)"),
    ("A1VO5Wqe", "group_neutralize(group_scale(add(signed_power(group_zscore(divide(est_12m_dps_raisednum_4wks, est_12m_dps_num_4wks_ago), subindustry), 1.5), multiply(1.2, group_rank(vec_avg(snl27_top50pctrankingavg), subindustry))), industry), market)"),
    ("E56r2xvJ", "group_neutralize(group_scale(add(signed_power(group_zscore(divide(est_12m_dps_raisednum_4wks, est_12m_dps_num_4wks_ago), subindustry), 1.5), multiply(1.2, group_rank(vec_avg(snl27_totalcountrydomains), subindustry))), industry), market)"),
    ("vR1egk2b", "group_neutralize(group_scale(add(signed_power(group_zscore(divide(subtract(est_12m_eps_raisednum_4wks, est_12m_eps_lowerednum_4wks), est_12m_eps_num_4wks_ago), subindustry), 1.5), multiply(1.8, group_rank(imb5_score, subindustry))), industry), market)"),
    ("pwd1p3P3", "group_neutralize(group_scale(add(signed_power(group_zscore(divide(est_12m_dps_raisednum_4wks, est_12m_dps_num_4wks_ago), subindustry), 1.5), multiply(1.2, group_rank(vec_avg(mcr27_company_jobsactive), subindustry))), industry), market)"),
    ("gJeoONZM", "group_neutralize(group_scale(add(signed_power(group_zscore(divide(subtract(est_12m_ebt_raised_1wk, est_12m_ebt_lowered_1wk), est_12m_ebt_num), subindustry), 1.5), multiply(1.4, group_rank(imb5_score, subindustry))), industry), market)"),
    ("6XdY8lEJ", "group_neutralize(group_scale(add(signed_power(group_zscore(divide(subtract(est_12m_net_raisednum_4wks, est_12m_net_lowerednum_4wks), est_12m_net_num_4wks_ago), subindustry), 1.5), multiply(1.2, group_rank(divide(ts_mean(vec_sum(num_jobs_created), 66), ts_mean(vec_sum(num_jobs_active), 66)), subindustry))), industry), market)"),
    ("bl6WXeVN", "group_neutralize(group_scale(add(signed_power(group_zscore(divide(subtract(est_12m_roe_raisednum_4wks, est_12m_roe_lowerednum_4wks), est_12m_roe_num_4wks_ago), subindustry), 1.5), multiply(1.2, group_rank(imb5_score, subindustry))), industry), market)"),
    ("xArmAbkW", "group_neutralize(group_scale(add(signed_power(group_zscore(divide(subtract(est_12m_ebi_raisednum_4wks, est_12m_ebi_lowerednum_4wks), est_12m_ebi_num_4wks_ago), subindustry), 1.5), multiply(1.2, group_rank(imb5_score, subindustry))), industry), market)"),
    ("akKWYeR9", "group_neutralize(group_scale(add(signed_power(group_zscore(divide(subtract(est_12m_prr_raisednum_4wks, est_12m_prr_lowerednum_4wks), est_12m_prr_num_4wks_ago), subindustry), 1.5), multiply(1.2, group_rank(ts_mean(vec_sum(stable_boundary_trade_count_21d), 22), subindustry))), industry), market)"),
    ("ZYQWRNe3", "add(group_zscore(divide(subtract(est_12m_dps_raisednum_4wks, est_12m_dps_lowerednum_4wks), est_12m_dps_num_4wks_ago), subindustry), multiply(1.2, group_rank(imb5_score, subindustry)))"),
]

BASE_SETTINGS = {
    'instrumentType': 'EQUITY', 'region': 'EUR', 'universe': 'TOP2500',
    'delay': 1, 'decay': 40, 'neutralization': 'FAST', 'truncation': 0.08,
    'pasteurization': 'ON', 'language': 'FASTEXPR', 'visualization': False,
    'testPeriod': 'P0Y0M', 'maxTrade': 'OFF', 'unitHandling': 'VERIFY', 'nanHandling': 'OFF',
}


async def main():
    results = {}
    remaining = list(FAILED)

    for round_num in range(5):  # Max 5 retry rounds
        if not remaining:
            break
        print(f"\n--- Retry round {round_num+1}: {len(remaining)} items ---", flush=True)
        batch = remaining[:3]  # Only 3 per batch to avoid 429
        remaining = remaining[3:]

        payloads = []
        for oid, code in batch:
            payloads.append({'type': 'REGULAR', 'settings': dict(BASE_SETTINGS), 'regular': code})

        try:
            result = await brain_client.batch_create_simulations(payloads)
            for p, r in zip(batch, result.get("results", [])):
                oid = p[0]
                if r.get('ok'):
                    sid = r.get('simulation_id', r.get('id', '?'))
                    results[oid] = {"simulation_id": sid, "status": "SUBMITTED"}
                    print(f"  OK: {oid} -> {sid}", flush=True)
                else:
                    print(f"  FAIL: {oid} -> {r.get('error')}", flush=True)
        except Exception as e:
            print(f"  ERROR: {e}", flush=True)

        if remaining:
            await asyncio.sleep(60)  # Long delay between rounds

    print(f"\n=== RETRY SUMMARY: {len(results)} success ===", flush=True)
    for oid, r in results.items():
        print(f"  {oid}: {r['simulation_id']}", flush=True)

    # Merge with existing successful results
    map_path = "/d/coding/traeCN_project/wqb/results/eur_tier2_rerun_map.json"
    with open(map_path) as f:
        existing = json.load(f)
    existing["results"].update(results)
    existing["retry_results"] = results
    with open(map_path, "w") as f:
        json.dump(existing, f, indent=2, ensure_ascii=False)
    print(f"\nUpdated {map_path}", flush=True)


asyncio.run(main())