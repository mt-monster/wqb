# -*- coding: utf-8 -*-
"""wave96 表达式批量语法校验"""
import json, subprocess

exprs = json.load(open(r'd:\coding\traeCN_project\wqb\tracking\KOR\candidates\wave96_exprs.json', encoding='utf-8'))
verifier = r'C:\Users\MENGTAO\.qoder-cn\skills\alpha-expression-verifier\scripts\verify_expr.py'
py = r'd:\coding\traeCN_project\wqb\world-quant-brain-mcp\.venv\Scripts\python.exe'
allok = True
for batch in exprs['batches']:
    for c in batch['expressions']:
        r = subprocess.run([py, verifier, c['expr']], capture_output=True, text=True, encoding='utf-8')
        try:
            out = json.loads(r.stdout)  # 解析完整 stdout（多行 JSON）
            ok = out.get('valid', False)
        except Exception:
            ok = False
            out = {'errors': r.stdout[-300:] + r.stderr[-300:]}
        mark = 'PASS' if ok else 'FAIL'
        print(f"{c['id']:3s} {mark}  {c['expr'][:95]}")
        if not ok:
            allok = False
            print('     ', out.get('errors'))
print('ALL_OK' if allok else 'HAS_FAIL')
