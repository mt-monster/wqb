import json
items = json.load(open('D:/coding/traeCN_project/wqb/tracking/EUR/candidates/eur_wave19_aea_items.json', encoding='utf-8'))
exprs = [it['code'] for it in items]
out = 'D:/coding/traeCN_project/wqb/tracking/EUR/candidates/eur_wave19_aea_exprs.json'
json.dump(exprs, open(out, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(f'{len(exprs)} exprs -> {out}')
