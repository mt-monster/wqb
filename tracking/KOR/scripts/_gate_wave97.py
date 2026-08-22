# -*- coding: utf-8 -*-
"""wave97: 批量语法校验 (verify_expr) + gate 5 闸预检 (model219)"""
import json, subprocess, os

base = r'd:\coding\traeCN_project\wqb\tracking\KOR'
exprs = json.load(open(os.path.join(base, r'candidates\wave97_exprs.json'), encoding='utf-8'))
verifier = r'C:\Users\MENGTAO\.qoder-cn\skills\alpha-expression-verifier\scripts\verify_expr.py'
gate = r'C:\Users\MENGTAO\.qoder-cn\skills\wq-brain-campaign-toolkit\scripts\gate.py'
py = r'd:\coding\traeCN_project\wqb\world-quant-brain-mcp\.venv\Scripts\python.exe'

# 1) 语法校验
print('=== 1) 语法校验 ===')
results = []
for c in exprs['expressions']:
    r = subprocess.run([py, verifier, c['expr']], capture_output=True, text=True, encoding='utf-8', errors='replace')
    out = json.loads(r.stdout)
    ok = out.get('valid', False)
    results.append({'id': c['id'], 'valid': ok, 'errors': out.get('errors', [])})
    print(f"  {c['id']}: {'PASS' if ok else 'FAIL ' + str(out.get('errors'))[:120]}")
all_ok = all(x['valid'] for x in results)

# 2) gate 预检
print('\n=== 2) gate 5 闸预检 (model219, --skip-diversity-gate) ===')
inp = os.path.join(base, 'candidates', 'wave97_gate_model219.json')
json.dump({'expressions': [c['expr'] for c in exprs['expressions']]},
          open(inp, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
cache = os.path.join(base, 'cache', 'gate_wave97_model219.json')
r = subprocess.run([py, gate, '--campaign-dir', base, '--dataset', 'model219',
                    '--file', inp, '--cache-file', cache, '--skip-diversity-gate'],
                   capture_output=True, text=True, encoding='utf-8', errors='replace')
out_txt = f'=== model219 (exit {r.returncode}) ===\n' + (r.stdout or '')[-2500:] + '\nSTDERR: ' + (r.stderr or '')[-800:]
with open(os.path.join(base, 'cache', 'gate_wave97_model219.out.txt'), 'w', encoding='utf-8') as f:
    f.write(out_txt)
try:
    g = json.loads(r.stdout[r.stdout.find('{'):r.stdout.rfind('}') + 1]) if '{' in r.stdout else None
    print(f"  all_pass={g.get('all_pass') if g else None}, total={g.get('total') if g else None}, passed={g.get('passed') if g else None}")
except Exception as e:
    print(f"  gate json parse: {e}")

print(f'\n=== 汇总: 语法 {sum(1 for x in results if x["valid"])}/{len(results)} PASS, gate out -> cache/gate_wave97_model219.out.txt ===')
