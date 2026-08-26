import sqlite3
import json
from datetime import datetime

# 基于成功案例 USA-MFP-4LEG-WIN 的骨架模式生成表达式
# 骨架: rank(add(multiply(w1, rank(ts_backfill(field1, 66))), multiply(w2, rank(ts_backfill(field2, 66))), ...))

# 成功案例使用的字段: long_term, short_hedge2, pv, event_5d
# 我们需要找到这些字段的完整名称

conn = sqlite3.connect('data/wqb.db')
cursor = conn.cursor()

# 查询字段
fields_to_find = ['long_term', 'short_hedge2', 'pv', 'event_5d']
found_fields = {}

for pattern in fields_to_find:
    cursor.execute("""
        SELECT name FROM datasets 
        WHERE region_id=(SELECT id FROM regions WHERE name='USA')
          AND name='multifactor_return_pred'
    """)
    # 从 catalog_json 中查找字段
    cursor.execute("""
        SELECT catalog_json FROM datasets 
        WHERE region_id=(SELECT id FROM regions WHERE name='USA')
          AND name='multifactor_return_pred'
    """)
    result = cursor.fetchone()
    if result:
        catalog = json.loads(result[0])
        fields = catalog.get('fields', [])
        for field in fields:
            field_id = field.get('id', '')
            if pattern in field_id:
                if pattern not in found_fields:
                    found_fields[pattern] = []
                found_fields[pattern].append(field_id)

print('找到的字段:')
for pattern, fields in found_fields.items():
    print(f'  {pattern}: {len(fields)} 个')
    for f in fields[:5]:
        print(f'    - {f}')

conn.close()
