import json,sys
raw=open(sys.argv[1],encoding="utf-8-sig").read(); d=json.loads(raw[raw.find("{"):])
ids={f.get("id") for f in (d.get("results") or [])}
for w in ["fnd23_ssfv","fnd23_dppv","fnd23_opts","fnd23_apts","fnd23_dapv","fnd23_ralv","total_assets_annual_atot","long_term_debt_total","quasi_equity_liabilities","other_off_balance_liabilities","retained_earnings_liabilities"]:
    print(("OK  " if w in ids else "MISS"), w)
