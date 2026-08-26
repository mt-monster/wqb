import sqlite3
import json

conn = sqlite3.connect('data/wqb.db')
cursor = conn.cursor()

# 查询 S0 白名单
cursor.execute("SELECT value FROM ledger_kv WHERE region='USA' AND key='s0_whitelist'")
result = cursor.fetchone()

if result:
    data = json.loads(result[0])
    datasets = data.get('datasets', [])
    print(f'S0 whitelist contains {len(datasets)} datasets:')
    for ds in datasets:
        print(f'  - {ds}')
    
    # 检查 multifactor_return_pred 是否在白名单中
    if 'multifactor_return_pred' in datasets:
        print('\n[YES] multifactor_return_pred is in whitelist')
    else:
        print('\n[NO] multifactor_return_pred is NOT in whitelist')
else:
    print('S0 whitelist not found')

conn.close()
