import json
d = json.load(open('D:/coding/traeCN_project/wqb/tracking/EUR/reference/eur_global_seasonal_model_fields.json', encoding='utf-8'))
fields = d['fields']
top = sorted(fields, key=lambda f: -(f.get('userCount') or 0))[:20]
for f in top:
    print(f"{f['userCount']:>3} ac={f.get('alphaCount',0):>3} cov={f.get('coverage',0):.2f} {f['id']}")
