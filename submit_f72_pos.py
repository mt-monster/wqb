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

# fundamental72 POSITIVE version (no negative sign)
fields = [
    'fnd72_pit_or_bs_q_bs_tot_asset',
    'fnd72_pit_or_bs_q_bs_retain_earn',
    'fnd72_pit_or_is_q_is_oper_inc',
    'fnd72_pit_or_is_q_earn_for_common',
    'fnd72_pit_or_cf_q_cf_cash_from_oper',
    'fnd72_pit_or_cf_q_cf_net_inc',
    'dividends_paid_cash_flow_q',
    'fnd72_pit_or_bs_q_bs_sh_out',
    'fnd72_pit_or_bs_q_bs_lt_borrow',
    'fnd72_pit_or_is_q_ebitda',
]

# POSITIVE: rank(+vec_avg(field))
base = 'rank(analyst_price_target_raised_count_four_weeks / analyst_price_target_count) + rank(vec_avg({}))'

payload = []
for f in fields:
    payload.append({
        'type': 'REGULAR',
        'settings': {
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
        },
        'regular': base.format(f)
    })

r2 = s.post('https://api.worldquantbrain.com/simulations', json=payload, timeout=60)
print('Sim status:', r2.status_code)
if r2.status_code == 201:
    loc = r2.headers.get('Location', '')
    print('Batch ID:', loc.split('/')[-1] if loc else 'N/A')
else:
    print(r2.text[:500])
