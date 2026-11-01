#!/usr/bin/env python3
"""Re-run Tier 2 EUR alphas (IS 1.8-1.99) with maxTrade=OFF."""
import json
import asyncio
import sys
import os
sys.path.insert(0, '/d/coding/traeCN_project/wqb/world-quant-brain-mcp')

from brain_api import brain_client

# Tier 2 EUR alphas - all EUR/TOP2500/delay=1/decay=40/FAST/truncation=0.08
# Format: (original_id, expression_code)
EXPRESSIONS = [
    ("GrW3PZ0P", "group_neutralize(group_scale(add(signed_power(group_zscore(divide(subtract(est_12m_ner_raisednum_4wks, est_12m_ner_lowerednum_4wks), est_12m_ner_num_4wks_ago), subindustry), 1.5), multiply(1.2, group_rank(imb5_score, subindustry))), industry), market)"),
    ("e75qk8YJ", "group_neutralize(group_scale(add(signed_power(group_zscore(divide(est_12m_dps_raisednum_4wks, est_12m_dps_num_4wks_ago), subindustry), 1.6), multiply(1.2, group_rank(imb5_score, subindustry))), industry), market)"),
    ("zq3PXlOO", "group_neutralize(group_scale(add(signed_power(group_zscore(divide(est_12m_dps_raisednum_4wks, est_12m_dps_num_4wks_ago), subindustry), 1.5), multiply(1.2, group_rank(ts_backfill(scl12_sentiment, 120), subindustry))), industry), market)"),
    ("GrWMEZn0", "group_neutralize(group_scale(signed_power(group_zscore(divide(est_12m_dps_raisednum_4wks, est_12m_dps_num_4wks_ago), subindustry), 1.5), industry), market)"),
    ("MPY5nW9M", "group_neutralize(group_scale(add(signed_power(group_zscore(divide(est_12m_dps_raisednum_4wks, est_12m_dps_num_4wks_ago), subindustry), 1.5), multiply(1.2, group_rank(vec_avg(snl27_skewness), subindustry))), industry), market)"),
    ("QPv5ZZdK", "add(group_zscore(divide(subtract(est_12m_ebt_raisednum_4wks, est_12m_ebt_lowerednum_4wks), est_12m_ebt_num_4wks_ago), subindustry), multiply(1.2, group_rank(divide(ts_mean(vec_sum(num_jobs_created), 66), ts_mean(vec_sum(num_jobs_active), 66)), subindustry)))"),
    ("1YNnkV3R", "group_neutralize(group_scale(add(signed_power(group_zscore(divide(est_12m_ebt_raisednum_4wks, est_12m_ebt_num_4wks_ago), subindustry), 1.5), multiply(1.2, group_rank(imb5_score, subindustry))), industry), market)"),
    ("bl6WGGpp", "trade_when(greater(mcr10_value, ts_quantile(mcr10_value, 504)), group_neutralize(group_scale(add(signed_power(group_zscore(divide(subtract(est_12m_ebt_raisednum_4wks, est_12m_ebt_lowerednum_4wks), est_12m_ebt_num_4wks_ago), subindustry), 2.1), multiply(1.2, group_rank(imb5_score, subindustry))), industry), market), 0)"),
    ("JjegKxPn", "group_neutralize(group_scale(add(signed_power(group_zscore(divide(subtract(est_12m_eps_raisednum_4wks, est_12m_eps_lowerednum_4wks), est_12m_eps_num_4wks_ago), subindustry), 1.125), multiply(1.2, group_rank(imb5_score, subindustry))), industry), market)"),
    ("RREko30o", "group_neutralize(group_scale(add(signed_power(group_zscore(divide(est_12m_dps_raisednum_4wks, est_12m_dps_num_4wks_ago), subindustry), 1.5), multiply(1.2, group_rank(vec_avg(snl27_top75pctrankingavg), subindustry))), industry), market)"),
    ("78LKlOw1", "group_neutralize(group_scale(add(signed_power(group_zscore(divide(est_12m_dps_raisednum_4wks, est_12m_dps_num_4wks_ago), subindustry), 1.5), multiply(1.2, group_rank(vec_avg(snl27_kurtosis), subindustry))), industry), market)"),
    ("LLMgJ9ZM", "group_neutralize(group_scale(add(signed_power(group_zscore(divide(subtract(est_12m_eps_raisednum_4wks, est_12m_eps_lowerednum_4wks), est_12m_eps_num_4wks_ago), subindustry), 1.5), multiply(1.5, group_rank(imb5_score, subindustry))), industry), market)"),
    ("A1VO5Wqe", "group_neutralize(group_scale(add(signed_power(group_zscore(divide(est_12m_dps_raisednum_4wks, est_12m_dps_num_4wks_ago), subindustry), 1.5), multiply(1.2, group_rank(vec_avg(snl27_top50pctrankingavg), subindustry))), industry), market)"),
    ("E56r2xvJ", "group_neutralize(group_scale(add(signed_power(group_zscore(divide(est_12m_dps_raisednum_4wks, est_12m_dps_num_4wks_ago), subindustry), 1.5), multiply(1.2, group_rank(vec_avg(snl27_totalcountrydomains), subindustry))), industry), market)"),
    ("vR1egk2b", "group_neutralize(group_scale(add(signed_power(group_zscore(divide(subtract(est_12m_eps_raisednum_4wks, est_12m_eps_lowerednum_4wks), est_12m_eps_num_4wks_ago), subindustry), 1.5), multiply(1.8, group_rank(imb5_score, subindustry))), industry), market)"),
    ("mLor9g65", "group_neutralize(group_scale(add(signed_power(group_zscore(divide(subtract(est_12m_eps_raisednum_4wks, est_12m_eps_lowerednum_4wks), est_12m_eps_num_4wks_ago), subindustry), 1.5), multiply(0.9, group_rank(imb5_score, subindustry))), industry), market)"),
    ("pwd1p3P3", "group_neutralize(group_scale(add(signed_power(group_zscore(divide(est_12m_dps_raisednum_4wks, est_12m_dps_num_4wks_ago), subindustry), 1.5), multiply(1.2, group_rank(vec_avg(mcr27_company_jobsactive), subindustry))), industry), market)"),
    ("kqN1lVgk", "group_neutralize(group_scale(add(signed_power(group_zscore(divide(subtract(est_12m_eps_raisednum_4wks, est_12m_eps_lowerednum_4wks), est_12m_eps_num_4wks_ago), subindustry), 1.5), multiply(0.6, group_rank(imb5_score, subindustry))), industry), market)"),
    ("WjOWJkGj", "add(group_zscore(divide(subtract(est_12m_ebt_raisednum_4wks, est_12m_ebt_lowerednum_4wks), est_12m_ebt_num_4wks_ago), subindustry), multiply(1.2, group_rank(divide(subtract(count_institutional_buyers_security, count_institutional_sellers_security), count_institutional_holders_security), subindustry)))"),
    ("gJeoONZM", "group_neutralize(group_scale(add(signed_power(group_zscore(divide(subtract(est_12m_ebt_raised_1wk, est_12m_ebt_lowered_1wk), est_12m_ebt_num), subindustry), 1.5), multiply(1.4, group_rank(imb5_score, subindustry))), industry), market)"),
    ("P0oXNE3E", "group_neutralize(group_scale(add(signed_power(group_zscore(divide(subtract(est_12m_ebt_raised_1wk, est_12m_ebt_lowered_1wk), est_12m_ebt_num), subindustry), 1.5), multiply(1.2, group_rank(imb5_score, subindustry))), industry), market)"),
    ("58EaNPLX", "group_neutralize(group_scale(add(signed_power(group_zscore(divide(est_12m_dps_raisednum_4wks, est_12m_dps_num_4wks_ago), subindustry), 1.5), multiply(1.2, group_rank(divide(subtract(count_institutional_buyers_security, count_institutional_sellers_security), add(count_institutional_buyers_security, count_institutional_sellers_security)), subindustry))), industry), market)"),
    ("bl6oER86", "group_neutralize(group_scale(add(signed_power(group_zscore(divide(subtract(est_12m_eps_raisednum_4wks, est_12m_eps_lowerednum_4wks), est_12m_eps_num_4wks_ago), subindustry), 1.875), multiply(1.2, group_rank(imb5_score, subindustry))), industry), market)"),
    ("9qxAv88o", "group_neutralize(group_scale(add(signed_power(group_zscore(divide(subtract(est_12m_ner_raisednum_4wks, est_12m_ner_lowerednum_4wks), est_12m_ner_num_4wks_ago), subindustry), 1.5), multiply(1.2, group_rank(ts_mean(vec_sum(stable_boundary_trade_count_21d), 22), subindustry))), industry), market)"),
    ("6XdY8lEJ", "group_neutralize(group_scale(add(signed_power(group_zscore(divide(subtract(est_12m_net_raisednum_4wks, est_12m_net_lowerednum_4wks), est_12m_net_num_4wks_ago), subindustry), 1.5), multiply(1.2, group_rank(divide(ts_mean(vec_sum(num_jobs_created), 66), ts_mean(vec_sum(num_jobs_active), 66)), subindustry))), industry), market)"),
    ("bl6WXeVN", "group_neutralize(group_scale(add(signed_power(group_zscore(divide(subtract(est_12m_roe_raisednum_4wks, est_12m_roe_lowerednum_4wks), est_12m_roe_num_4wks_ago), subindustry), 1.5), multiply(1.2, group_rank(imb5_score, subindustry))), industry), market)"),
    ("xArmAbkW", "group_neutralize(group_scale(add(signed_power(group_zscore(divide(subtract(est_12m_ebi_raisednum_4wks, est_12m_ebi_lowerednum_4wks), est_12m_ebi_num_4wks_ago), subindustry), 1.5), multiply(1.2, group_rank(imb5_score, subindustry))), industry), market)"),
    ("akKWYeR9", "group_neutralize(group_scale(add(signed_power(group_zscore(divide(subtract(est_12m_prr_raisednum_4wks, est_12m_prr_lowerednum_4wks), est_12m_prr_num_4wks_ago), subindustry), 1.5), multiply(1.2, group_rank(ts_mean(vec_sum(stable_boundary_trade_count_21d), 22), subindustry))), industry), market)"),
    ("ZYQWRNe3", "add(group_zscore(divide(subtract(est_12m_dps_raisednum_4wks, est_12m_dps_lowerednum_4wks), est_12m_dps_num_4wks_ago), subindustry), multiply(1.2, group_rank(imb5_score, subindustry)))"),
]

BASE_SETTINGS = {
    'instrumentType': 'EQUITY',
    'region': 'EUR',
    'universe': 'TOP2500',
    'delay': 1,
    'decay': 40,
    'neutralization': 'FAST',
    'truncation': 0.08,
    'pasteurization': 'ON',
    'language': 'FASTEXPR',
    'visualization': False,
    'testPeriod': 'P0Y0M',
    'maxTrade': 'OFF',
    'unitHandling': 'VERIFY',
    'nanHandling': 'OFF',
}


def build_payloads():
    payloads = []
    for orig_id, code in EXPRESSIONS:
        payloads.append({
            'type': 'REGULAR',
            'settings': dict(BASE_SETTINGS),
            'regular': code,
            '_original_id': orig_id,
        })
    return payloads


async def submit_batch(batch, batch_num, results):
    print(f"=== Batch {batch_num} ({len(batch)} items) ===", flush=True)
    api_payloads = [{k: v for k, v in p.items() if k != '_original_id'} for p in batch]
    try:
        result = await brain_client.batch_create_simulations(api_payloads)
        print(json.dumps(result, indent=2, ensure_ascii=False)[:2000], flush=True)
        for p, r in zip(batch, result.get("results", [])):
            oid = p['_original_id']
            if r.get('ok'):
                sid = r.get('simulation_id', r.get('id', '?'))
                results[oid] = {"simulation_id": sid, "status": "SUBMITTED"}
            else:
                results[oid] = {"simulation_id": None, "status": "FAILED", "error": r.get('error')}
    except Exception as e:
        print(f"ERROR batch {batch_num}: {e}", flush=True)
        for p in batch:
            oid = p['_original_id']
            results[oid] = {"simulation_id": None, "status": "ERROR", "error": str(e)}


async def main():
    payloads = build_payloads()
    results = {}

    # Submit in batches of 5 to avoid 429
    batches = [payloads[i:i+5] for i in range(0, len(payloads), 5)]

    for bi, batch in enumerate(batches):
        await submit_batch(batch, bi+1, results)
        if bi < len(batches) - 1:
            await asyncio.sleep(15)

    print("\n=== SUBMISSION SUMMARY ===", flush=True)
    success = {k: v for k, v in results.items() if v['status'] == 'SUBMITTED'}
    failed = {k: v for k, v in results.items() if v['status'] != 'SUBMITTED'}
    print(f"Success: {len(success)}/{len(results)}", flush=True)
    if failed:
        print(f"Failed: {json.dumps(failed, indent=2)}", flush=True)

    # Save mapping
    os.makedirs("/d/coding/traeCN_project/wqb/results", exist_ok=True)
    with open("/d/coding/traeCN_project/wqb/results/eur_tier2_rerun_map.json", "w") as f:
        json.dump({
            "items": [{"original_id": oid, "code": code[:80]} for oid, code in EXPRESSIONS],
            "results": results
        }, f, indent=2, ensure_ascii=False)
    print("\nSaved to results/eur_tier2_rerun_map.json", flush=True)


asyncio.run(main())