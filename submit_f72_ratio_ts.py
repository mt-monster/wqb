import os, requests, json, base64
from dotenv import load_dotenv
load_dotenv(r'D:\coding\traeCN_project\wqb\world-quant-brain-mcp\.env')

email = os.environ['CREDENTIALS_EMAIL']
pwd = os.environ['CREDENTIALS_PASSWORD']

s = requests.Session()
credentials = f'{email}:{pwd}'
encoded = base64.b64encode(credentials.encode()).decode()
headers = {'Authorization': f'Basic {encoded}'}
r = s.post('https://api.worldquantbrain.com/authentication', headers=headers, timeout=60)
print('Auth:', r.status_code)

settings = {
    'instrumentType': 'EQUITY',
    'region': 'MEA',
    'universe': 'TOP400',
    'delay': 1,
    'decay': 1,
    'neutralization': 'SECTOR',
    'truncation': 0.1,
    'pasteurization': 'ON',
    'language': 'FASTEXPR',
    'visualization': False,
    'testPeriod': 'P0Y0M',
    'maxTrade': 'OFF',
    'unitHandling': 'VERIFY',
    'nanHandling': 'ON'
}

# Batch 1: RATIO fields (profitability/efficiency ratios)
# Using fundamental72 ratio fields - constructed from available fields
ratio_exprs = [
    # ROE = earn_for_common / bs_tot_common_eq
    'rank(analyst_price_target_raised_count_four_weeks / analyst_price_target_count) + rank(-vec_avg(fnd72_pit_or_is_q_earn_for_common) / vec_avg(fnd72_pit_or_bs_q_bs_tot_common_eq))',
    # ROA = earn_for_common / bs_tot_asset
    'rank(analyst_price_target_raised_count_four_weeks / analyst_price_target_count) + rank(-vec_avg(fnd72_pit_or_is_q_earn_for_common) / vec_avg(fnd72_pit_or_bs_q_bs_tot_asset))',
    # Operating margin = oper_inc / rev
    'rank(analyst_price_target_raised_count_four_weeks / analyst_price_target_count) + rank(-vec_avg(fnd72_pit_or_is_q_is_oper_inc) / vec_avg(fnd72_pit_or_is_q_rev))',
    # Net margin = net_inc / rev
    'rank(analyst_price_target_raised_count_four_weeks / analyst_price_target_count) + rank(-vec_avg(fnd72_pit_or_is_q_net_inc) / vec_avg(fnd72_pit_or_is_q_rev))',
    # EBITDA margin = ebitda / rev
    'rank(analyst_price_target_raised_count_four_weeks / analyst_price_target_count) + rank(-vec_avg(fnd72_pit_or_is_q_ebitda) / vec_avg(fnd72_pit_or_is_q_rev))',
    # Cash flow margin = cash_from_oper / rev
    'rank(analyst_price_target_raised_count_four_weeks / analyst_price_target_count) + rank(-vec_avg(fnd72_pit_or_cf_q_cf_cash_from_oper) / vec_avg(fnd72_pit_or_is_q_rev))',
    # Asset turnover = rev / tot_asset
    'rank(analyst_price_target_raised_count_four_weeks / analyst_price_target_count) + rank(-vec_avg(fnd72_pit_or_is_q_rev) / vec_avg(fnd72_pit_or_bs_q_bs_tot_asset))',
    # Debt ratio = lt_borrow / tot_asset
    'rank(analyst_price_target_raised_count_four_weeks / analyst_price_target_count) + rank(-vec_avg(fnd72_pit_or_bs_q_bs_lt_borrow) / vec_avg(fnd72_pit_or_bs_q_bs_tot_asset))',
    # Retention ratio = retain_earn / tot_common_eq
    'rank(analyst_price_target_raised_count_four_weeks / analyst_price_target_count) + rank(-vec_avg(fnd72_pit_or_bs_q_bs_retain_earn) / vec_avg(fnd72_pit_or_bs_q_bs_tot_common_eq))',
    # Dividend payout = dividends_paid / net_inc
    'rank(analyst_price_target_raised_count_four_weeks / analyst_price_target_count) + rank(-vec_avg(dividends_paid_cash_flow_q) / vec_avg(fnd72_pit_or_is_q_net_inc))',
]

payload1 = []
for expr in ratio_exprs:
    payload1.append({
        'type': 'REGULAR',
        'settings': settings,
        'regular': expr
    })

r1 = s.post('https://api.worldquantbrain.com/simulations', json=payload1, timeout=60)
print('Batch 1 (RATIO):', r1.status_code)
if r1.status_code == 201:
    loc = r1.headers.get('Location', '')
    print('  Batch ID:', loc.split('/')[-1] if loc else 'N/A')
else:
    print('  Error:', r1.text[:300])

# Batch 2: TS_DELTA / TS_ZSCORE time-series changes
ts_exprs = [
    # ts_delta of total assets (growth)
    'rank(analyst_price_target_raised_count_four_weeks / analyst_price_target_count) + rank(-ts_delta(vec_avg(fnd72_pit_or_bs_q_bs_tot_asset), 63))',
    # ts_delta of operating income
    'rank(analyst_price_target_raised_count_four_weeks / analyst_price_target_count) + rank(-ts_delta(vec_avg(fnd72_pit_or_is_q_is_oper_inc), 63))',
    # ts_delta of net income
    'rank(analyst_price_target_raised_count_four_weeks / analyst_price_target_count) + rank(-ts_delta(vec_avg(fnd72_pit_or_is_q_net_inc), 63))',
    # ts_delta of cash from operations
    'rank(analyst_price_target_raised_count_four_weeks / analyst_price_target_count) + rank(-ts_delta(vec_avg(fnd72_pit_or_cf_q_cf_cash_from_oper), 63))',
    # ts_delta of EBITDA
    'rank(analyst_price_target_raised_count_four_weeks / analyst_price_target_count) + rank(-ts_delta(vec_avg(fnd72_pit_or_is_q_ebitda), 63))',
    # ts_zscore of total assets
    'rank(analyst_price_target_raised_count_four_weeks / analyst_price_target_count) + rank(-ts_zscore(vec_avg(fnd72_pit_or_bs_q_bs_tot_asset), 63))',
    # ts_zscore of operating income
    'rank(analyst_price_target_raised_count_four_weeks / analyst_price_target_count) + rank(-ts_zscore(vec_avg(fnd72_pit_or_is_q_is_oper_inc), 63))',
    # ts_zscore of net income
    'rank(analyst_price_target_raised_count_four_weeks / analyst_price_target_count) + rank(-ts_zscore(vec_avg(fnd72_pit_or_is_q_net_inc), 63))',
    # ts_zscore of revenue
    'rank(analyst_price_target_raised_count_four_weeks / analyst_price_target_count) + rank(-ts_zscore(vec_avg(fnd72_pit_or_is_q_rev), 63))',
    # ts_zscore of retained earnings
    'rank(analyst_price_target_raised_count_four_weeks / analyst_price_target_count) + rank(-ts_zscore(vec_avg(fnd72_pit_or_bs_q_bs_retain_earn), 63))',
]

payload2 = []
for expr in ts_exprs:
    payload2.append({
        'type': 'REGULAR',
        'settings': settings,
        'regular': expr
    })

r2 = s.post('https://api.worldquantbrain.com/simulations', json=payload2, timeout=60)
print('Batch 2 (TS_DELTA/TS_ZSCORE):', r2.status_code)
if r2.status_code == 201:
    loc = r2.headers.get('Location', '')
    print('  Batch ID:', loc.split('/')[-1] if loc else 'N/A')
else:
    print('  Error:', r2.text[:300])
