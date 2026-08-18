import json, sys

sys.stdout.reconfigure(encoding='utf-8', errors='replace')

d = json.load(open(r'D:\coding\traeCN_project\wqb\tracking\GBR\results\5slot_news17_probe_results.json', encoding='utf-8'))
rows = [r for r in d.get('results', []) if r.get('dataset') == 'news17']
out = r'D:\coding\traeCN_project\wqb\tracking\GBR\results\_news17_metrics.jsonl'
with open(out, 'w', encoding='utf-8') as f:
    for r in rows:
        f.write(json.dumps(r, ensure_ascii=False) + '\n')
print(f'rows={len(rows)} -> {out}')
best = max(rows, key=lambda r: abs(r.get('sharpe') or 0))
print('best:', best['id'], 'sh=', best.get('sharpe'), '2y=', best.get('two_year_sharpe'), 'mg=', best.get('margin_bp'), 'tvr=', best.get('turnover_pct'))
