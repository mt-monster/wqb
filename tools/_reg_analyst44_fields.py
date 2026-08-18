# -*- coding: utf-8 -*-
"""登记 analyst44 (Integrated Broker Estimates) 字段到 fields_gate.json 白名单。"""
import json
import os

GATE_DIR = r'd:\coding\traeCN_project\wqb\data\fields_gate'
SCOPE = 'USA/TOP3000/D1'
fpath = os.path.join(GATE_DIR, SCOPE.replace('/', '_') + '.json')
with open(fpath, encoding='utf-8') as f:
    gate = json.load(f)

ds = gate.setdefault('analyst44', {'fields': {}})

# (field_id, coverage) — 全部来自 get_datafields 返回
fields = [
    ('anl44_eps_best_eeps_cur_yr', 0.9847),
    ('anl44_eps_best_eeps_nxt_yr', 0.9848),
    ('anl44_ebitda_best_eeps_cur_yr', 0.9287),
    ('anl44_ebitda_best_eeps_nxt_yr', 0.9291),
    ('anl44_roe_best_eeps_cur_yr', 0.9287),
    ('anl44_roe_best_eeps_nxt_yr', 0.9291),
    ('anl44_roa_best_eeps_cur_yr', 0.9287),
    ('anl44_roa_best_eeps_nxt_yr', 0.9291),
    ('anl44_eps_ratio_best_eeps_cur_yr', 0.9287),
    ('anl44_eps_ratio_best_eeps_nxt_yr', 0.9291),
    ('anl44_epsr_best_eeps_cur_yr', 0.9287),
    ('anl44_epsr_best_eeps_nxt_yr', 0.9291),
    ('anl44_dps_best_eeps_cur_yr', 0.8742),
    ('anl44_dps_best_eeps_nxt_yr', 0.9848),
    ('anl44_cfps_best_eeps_cur_yr', 0.8742),
    ('anl44_cfps_best_eeps_nxt_yr', 0.8744),
    ('anl44_sales_best_eeps_cur_yr', 0.9287),
    ('anl44_sales_best_eeps_nxt_yr', 0.9291),
    ('anl44_ebit_best_eeps_cur_yr', 0.9287),
    ('anl44_ebit_best_eeps_nxt_yr', 0.9291),
    ('anl44_netprofit_gaap_best_eeps_cur_yr', 0.9287),
    ('anl44_netprofit_gaap_best_eeps_nxt_yr', 0.9291),
    ('anl44_netprofit_rep_best_eeps_cur_yr', 0.9287),
    ('anl44_netprofit_rep_best_eeps_nxt_yr', 0.9291),
    ('anl44_operatingprofit_best_eeps_cur_yr', 0.9287),
    ('anl44_operatingprofit_best_eeps_nxt_yr', 0.9291),
    ('anl44_pretaxprofit_best_eeps_cur_yr', 0.9287),
    ('anl44_pretaxprofit_best_eeps_nxt_yr', 0.9291),
    ('anl44_nav_best_eeps_cur_yr', 0.9287),
    ('anl44_nav_best_eeps_nxt_yr', 0.9291),
    ('anl44_netdebt_best_eeps_cur_yr', 0.9287),
    ('anl44_netdebt_best_eeps_nxt_yr', 0.9291),
    ('anl44_ffops_best_eeps_cur_yr', 0.9287),
    ('anl44_ffops_best_eeps_nxt_yr', 0.9291),
    ('anl44_eps_gaap_best_eeps_cur_yr', 0.9287),
    ('anl44_eps_gaap_best_eeps_nxt_yr', 0.9291),
    ('latest_quarter_eps_value', 0.9651),
]

added = 0
for fid, cov in fields:
    if fid not in ds['fields']:
        ds['fields'][fid] = {'type': 'MATRIX', 'coverage': cov}
        added += 1

with open(fpath, 'w', encoding='utf-8') as f:
    json.dump(gate, f, ensure_ascii=False, indent=2)

print(f'added {added} fields, total analyst44 = {len(ds["fields"])}')
