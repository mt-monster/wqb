#!/usr/bin/env python3
"""Re-run 8 Tier 1 EUR alphas with maxTrade=OFF to get investability data."""
import json
import asyncio
import sys
sys.path.insert(0, '/d/coding/traeCN_project/wqb/world-quant-brain-mcp')

from brain_api import brain_client

# 8 Tier 1 EUR alphas
EXPRESSIONS = [
    ("E56r190R", "group_neutralize(group_scale(add(signed_power(group_zscore(divide(subtract(est_12m_sal_raisednum_4wks, est_12m_sal_lowerednum_4wks), est_12m_sal_num_4wks_ago), subindustry), 1.5), multiply(1.2, group_rank(imb5_score, subindustry))), industry), market)"),
    ("P0oXWxxx", "group_neutralize(group_scale(add(signed_power(group_zscore(divide(subtract(est_12m_sal_raisednum_4wks, est_12m_sal_lowerednum_4wks), est_12m_sal_num_4wks_ago), subindustry), 1.5), multiply(1.2, group_rank(multiply(-1, ts_mean(scl12_buzz, 22)), subindustry))), industry), market)"),
    ("P0owqwKE", "group_neutralize(group_scale(signed_power(group_zscore(divide(subtract(est_12m_ebt_raisednum_4wks, est_12m_ebt_lowerednum_4wks), est_12m_ebt_num_4wks_ago), subindustry), 1.5), industry), market)"),
    ("MPY5Ox9M", "group_neutralize(group_scale(add(signed_power(group_zscore(divide(est_12m_pre_raisednum_4wks, est_12m_pre_num_4wks_ago), subindustry), 1.5), multiply(1.2, group_rank(imb5_score, subindustry))), industry), market)"),
    ("wpQJpbRx", "group_neutralize(group_scale(add(signed_power(group_zscore(divide(subtract(est_12m_ebt_raisednum_4wks, est_12m_ebt_lowerednum_4wks), est_12m_ebt_num_4wks_ago), subindustry), 2.1), multiply(1.2, group_rank(imb5_score, subindustry))), industry), market)"),
    ("P0oXNk6J", "group_neutralize(group_scale(add(signed_power(group_zscore(divide(subtract(est_12m_prr_raisednum_4wks, est_12m_prr_lowerednum_4wks), est_12m_prr_num_4wks_ago), subindustry), 1.5), multiply(1.2, group_rank(imb5_score, subindustry))), industry), market)"),
    ("N1N5wLKe", "group_neutralize(group_scale(add(signed_power(group_zscore(divide(subtract(est_12m_sal_raisednum_4wks, est_12m_sal_lowerednum_4wks), est_12m_sal_num_4wks_ago), subindustry), 1.5), multiply(1.2, group_rank(ts_mean(vec_sum(stable_boundary_trade_count_21d), 22), subindustry))), industry), market)"),
    ("QPv5Zrpp", "group_neutralize(group_scale(add(signed_power(group_zscore(divide(est_12m_dps_raisednum_4wks, est_12m_dps_num_4wks_ago), subindustry), 1.5), multiply(1.2, group_rank(imb5_score, subindustry))), industry), market)"),
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


async def main():
    payloads = build_payloads()
    results = {}

    # Split into 2 batches of 4
    batches = [payloads[:4], payloads[4:]]

    for bi, batch in enumerate(batches):
        print(f"=== Batch {bi+1} ({len(batch)} items) ===", flush=True)
        # Strip _original_id before sending to API
        api_payloads = [{k: v for k, v in p.items() if k != '_original_id'} for p in batch]
        try:
            result = await brain_client.batch_create_simulations(api_payloads)
            print(json.dumps(result, indent=2, ensure_ascii=False)[:3000], flush=True)
            for p, r in zip(batch, result.get("results", [])):
                oid = p['_original_id']
                sid = r.get('simulation_id', r.get('id', '?'))
                results[oid] = {"simulation_id": sid, "status": r.get('status', '?')}
        except Exception as e:
            print(f"ERROR batch {bi+1}: {e}", flush=True)
            import traceback
            traceback.print_exc()

    print("\n=== SUMMARY ===", flush=True)
    print(json.dumps(results, indent=2, ensure_ascii=False), flush=True)

    # Save mapping
    import os
    os.makedirs("/d/coding/traeCN_project/wqb/results", exist_ok=True)
    with open("/d/coding/traeCN_project/wqb/results/eur_tier1_rerun_map.json", "w") as f:
        json.dump({"items": [{"original_id": oid, "code": code[:60]} for oid, code in EXPRESSIONS],
                    "results": results}, f, indent=2, ensure_ascii=False)
    print("\nSaved to results/eur_tier1_rerun_map.json", flush=True)


asyncio.run(main())