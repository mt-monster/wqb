import os, requests, json, base64
from dotenv import load_dotenv
load_dotenv(r'D:\coding\traeCN_project\wqb\world-quant-brain-mcp\.env')

email = os.environ['CREDENTIALS_EMAIL']
pwd = os.environ['CREDENTIALS_PASSWORD']

s = requests.Session()
credentials = f'{email}:{pwd}'
encoded = base64.b64encode(credentials.encode()).decode()
headers = {'Authorization': f'Basic {encoded}'}
r = s.post('https://api.worldquantbrain.com/authentication', headers=headers, timeout=120)
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

# Batch 1: RATIO fields with CORRECT field names
ratio_exprs = [
    # ROE = earn_for_common / shareholders_equity
    'rank(analyst_price_target_raised_count_four_weeks / analyst_price_target_count) + rank(-vec_avg(fnd72_pit_or_is_q_earn_for_common) / vec_avg(shareholders_equity_total_amt))',
    # ROA = earn_for_common / tot_asset
    'rank(analyst_price_target_raised_count_four_weeks / analyst_price_target_count) + rank(-vec_avg(fnd72_pit_or_is_q_earn_for_common) / vec_avg(fnd72_pit_or_bs_q_bs_tot_asset))',
    # Operating margin = oper_inc / sales_rev_turn
    'rank(analyst_price_target_raised_count_four_weeks / analyst_price_target_count) + rank(-vec_avg(fnd72_pit_or_is_q_is_oper_inc) / vec_avg(fnd72_pit_or_is_q_sales_rev_turn))',
    # Net margin = earn_for_common / sales_rev_turn
    'rank(analyst_price_target_raised_count_four_weeks / analyst_price_target_count) + rank(-vec_avg(fnd72_pit_or_is_q_earn_for_common) / vec_avg(fnd72_pit_or_is_q_sales_rev_turn))',
    # EBITDA margin = ebitda / sales_rev_turn
    'rank(analyst_price_target_raised_count_four_weeks / analyst_price_target_count) + rank(-vec_avg(fnd72_pit_or_is_q_ebitda) / vec_avg(fnd72_pit_or_is_q_sales_rev_turn))',
    # Asset turnover = sales_rev_turn / tot_asset
    'rank(analyst_price_target_raised_count_four_weeks / analyst_price_target_count) + rank(-vec_avg(fnd72_pit_or_is_q_sales_rev_turn) / vec_avg(fnd72_pit_or_bs_q_bs_tot_asset))',
    # Debt ratio = lt_borrow / tot_asset
    'rank(analyst_price_target_raised_count_four_weeks / analyst_price_target_count) + rank(-vec_avg(fnd72_pit_or_bs_q_bs_lt_borrow) / vec_avg(fnd72_pit_or_bs_q_bs_tot_asset))',
    # Retention ratio = retain_earn / shareholders_equity
    'rank(analyst_price_target_raised_count_four_weeks / analyst_price_target_count) + rank(-vec_avg(fnd72_pit_or_bs_q_bs_retain_earn) / vec_avg(shareholders_equity_total_amt))',
    # Dividend payout = dividends_paid / earn_for_common
    'rank(analyst_price_target_raised_count_four_weeks / analyst_price_target_count) + rank(-vec_avg(dividends_paid_cash_flow_q) / vec_avg(fnd72_pit_or_is_q_earn_for_common))',
    # Cash flow margin = cf_net_inc / sales_rev_turn
    'rank(analyst_price_target_raised_count_four_weeks / analyst_price_target_count) + rank(-vec_avg(fnd72_pit_or_cf_q_cf_net_inc) / vec_avg(fnd72_pit_or_is_q_sales_rev_turn))',
]

payload1 = []
for expr in ratio_exprs:
    payload1.append({
        'type': 'REGULAR',
        'settings': settings,
        'regular': expr
    })

r1 = s.post('https://api.worldquantbrain.com/simulations', json=payload1, timeout=120)
print('Batch 1 (RATIO):', r1.status_code)
if r1.status_code == 201:
    loc = r1.headers.get('Location', '')
    print('  Batch ID:', loc.split('/')[-1] if loc else 'N/A')
else:
    print('  Error:', r1.text[:300])

# Batch 2: TS_DELTA / TS_ZSCORE with CORRECT field names
ts_exprs = [
    # ts_delta of total assets
    'rank(analyst_price_target_raised_count_four_weeks / analyst_price_target_count) + rank(-ts_delta(vec_avg(fnd72_pit_or_bs_q_bs_tot_asset), 63))',
    # ts_delta of operating income
    'rank(analyst_price_target_raised_count_four_weeks / analyst_price_target_count) + rank(-ts_delta(vec_avg(fnd72_pit_or_is_q_is_oper_inc), 63))',
    # ts_delta of net income (earn_for_common)
    'rank(analyst_price_target_raised_count_four_weeks / analyst_price_target_count) + rank(-ts_delta(vec_avg(fnd72_pit_or_is_q_earn_for_common), 63))',
    # ts_delta of revenue
    'rank(analyst_price_target_raised_count_four_weeks / analyst_price_target_count) + rank(-ts_delta(vec_avg(fnd72_pit_or_is_q_sales_rev_turn), 63))',
    # ts_delta of EBITDA
    'rank(analyst_price_target_raised_count_four_weeks / analyst_price_target_count) + rank(-ts_delta(vec_avg(fnd72_pit_or_is_q_ebitda), 63))',
    # ts_zscore of total assets
    'rank(analyst_price_target_raised_count_four_weeks / analyst_price_target_count) + rank(-ts_zscore(vec_avg(fnd72_pit_or_bs_q_bs_tot_asset), 63))',
    # ts_zscore of operating income
    'rank(analyst_price_target_raised_count_four_weeks / analyst_price_target_count) + rank(-ts_zscore(vec_avg(fnd72_pit_or_is_q_is_oper_inc), 63))',
    # ts_zscore of net income
    'rank(analyst_price_target_raised_count_four_weeks / analyst_price_target_count) + rank(-ts_zscore(vec_avg(fnd72_pit_or_is_q_earn_for_common), 63))',
    # ts_zscore of revenue
    'rank(analyst_price_target_raised_count_four_weeks / analyst_price_target_count) + rank(-ts_zscore(vec_avg(fnd72_pit_or_is_q_sales_rev_turn), 63))',
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

r2 = s.post('https://api.worldquantbrain.com/simulations', json=payload2, timeout=120)
print('Batch 2 (TS_DELTA/TS_ZSCORE):', r2.status_code)
if r2.status_code == 201:
    loc = r2.headers.get('Location', '')
    print('  Batch ID:', loc.split('/')[-1] if loc else 'N/A')
else:
    print('  Error:', r2.text[:300])
