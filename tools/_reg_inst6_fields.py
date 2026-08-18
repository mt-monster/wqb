# -*- coding: utf-8 -*-
"""登记 institutions6 (Institutions and Beneficial Stake Ownership) 字段到 fields_gate.json 白名单。"""
import json
import os

GATE_DIR = r'd:\coding\traeCN_project\wqb\data\fields_gate'
SCOPE = 'USA/TOP3000/D1'
fpath = os.path.join(GATE_DIR, SCOPE.replace('/', '_') + '.json')
with open(fpath, encoding='utf-8') as f:
    gate = json.load(f)

ds = gate.setdefault('institutions6', {'fields': {}})

# 全部 21 字段（coverage 均 1.0），来自 get_datafields 返回
fields = [
    'aggregate_equity_value_all_owners',
    'aggregate_equity_value_institutions',
    'aggregate_share_count_institutions',
    'count_institutional_buyers_security',
    'count_institutional_holders_security',
    'count_institutional_sellers_security',
    'inst6_num_of_institutional_buyers',
    'inst6_num_of_institutional_holders',
    'inst6_num_of_institutional_sellers',
    'inst6_num_of_institutional_shares_bought',
    'inst6_num_of_institutional_shares_sold',
    'inst6_total_share_held_by_owners',
    'inst6_total_shares_held_by_institutions',
    'inst6_value_held_by_institutions',
    'inst6_value_held_by_owners',
    'inst6_value_of_institutional_shares_bought',
    'inst6_value_of_institutional_shares_sold',
    'market_value_institutional_shares_acquired',
    'market_value_institutional_shares_disposed',
    'quantity_institutional_shares_acquired',
    'quantity_institutional_shares_disposed',
]

added = 0
for fid in fields:
    if fid not in ds['fields']:
        ds['fields'][fid] = {'type': 'MATRIX', 'coverage': 1.0}
        added += 1

with open(fpath, 'w', encoding='utf-8') as f:
    json.dump(gate, f, ensure_ascii=False, indent=2)

print(f'added {added} fields, total institutions6 = {len(ds["fields"])}')
