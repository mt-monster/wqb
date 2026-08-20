import json
d = json.load(open('tracking/EUR/reference/eur_news54_fields.json', encoding='utf-8'))
for f in d['fields']:
    print(f"{f['userCount']:>3} ac={f.get('alphaCount',0):>3} cov={f.get('coverage',0):.2f} {f['id']}")
