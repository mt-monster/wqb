# -*- coding: utf-8 -*-
"""wave96: 生成 gate 输入文件 + 跑 gate 5 闸预检"""
import json, subprocess, sys, os

base = r'd:\coding\traeCN_project\wqb\tracking\KOR'
exprs = json.load(open(os.path.join(base, r'candidates\wave96_exprs.json'), encoding='utf-8'))
gate = r'C:\Users\MENGTAO\.qoder-cn\skills\wq-brain-campaign-toolkit\scripts\gate.py'
py = r'd:\coding\traeCN_project\wqb\world-quant-brain-mcp\.venv\Scripts\python.exe'
ds_map = {'P': 'price_signal_dl', 'A': 'ai_factor_transfer'}

for batch in exprs['batches']:
    ds = ds_map[batch['batch']]
    inp = os.path.join(base, 'candidates', f'wave96_gate_{ds}.json')
    json.dump({'expressions': [c['expr'] for c in batch['expressions']]},
              open(inp, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    cache = os.path.join(base, 'cache', f'gate_wave96_{ds}.json')
    r = subprocess.run([py, gate, '--campaign-dir', base, '--dataset', ds,
                        '--file', inp, '--cache-file', cache, '--skip-diversity-gate'],
                       capture_output=True, text=True, encoding='utf-8', errors='replace')
    out = f'=== {ds} (exit {r.returncode}) ===\n' + (r.stdout or '')[-2500:] + '\nSTDERR: ' + (r.stderr or '')[-800:]
    with open(os.path.join(base, 'cache', f'gate_wave96_{ds}.out.txt'), 'w', encoding='utf-8') as f:
        f.write(out)
    print(f'{ds} done, exit={r.returncode}, out -> cache/gate_wave96_{ds}.out.txt')
