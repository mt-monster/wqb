# -*- coding: utf-8 -*-
"""临时工具：查看白名单数据集的字段级覆盖率"""
import json
import sys

for ds in sys.argv[1:]:
    p = f'tracking/mining/field_coverage_GBR_d1_TOP700_{ds}.json'
    try:
        d = json.load(open(p, encoding='utf-8'))
    except FileNotFoundError:
        print(f'=== {ds}: 文件不存在')
        continue
    print(f'=== {ds}  query: {d.get("query")}')
    print(f'field_count: {d.get("field_count")}')
    fields = d['fields']
    hi = [f for f in fields if f.get('coverage', 0) >= 0.85]
    print(f'cov>=0.85: {len(hi)}')
    for f in sorted(hi, key=lambda x: -x.get('coverage', 0)):
        print(f'  {f.get("id", "?"):48s} cov={f.get("coverage", 0):.3f} type={f.get("type", "?")} alphas={f.get("alphaCount", 0)}')
