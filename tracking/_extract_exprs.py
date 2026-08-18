import json, sys
items = json.load(open(sys.argv[1], encoding='utf-8'))
codes = [it['code'] if isinstance(it, dict) else it for it in items]
json.dump(codes, open(sys.argv[2], 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(f"extracted {len(codes)} exprs -> {sys.argv[2]}")
