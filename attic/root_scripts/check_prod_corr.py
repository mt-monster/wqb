import sqlite3
import json

conn = sqlite3.connect('data/wqb.db')
cursor = conn.cursor()

# 查询 Wave 1 的 3 个候选表达式的 alpha_id
cursor.execute('''
    SELECT alpha_id, code, sharpe
    FROM backtest_results
    WHERE region='USA' AND wave='1' AND sharpe >= 1.0
    ORDER BY sharpe DESC
''')

candidates = cursor.fetchall()
print(f'Wave 1 候选表达式（共 {len(candidates)} 个）:')
print('=' * 100)

for i, (alpha_id, code, sharpe) in enumerate(candidates, 1):
    print(f'\n{i}. Alpha ID: {alpha_id}')
    print(f'   Sharpe: {sharpe:.3f}')
    print(f'   Expression: {code}')
    
    # 查询 payload_json 中的 prod_corr
    cursor.execute('''
        SELECT payload_json
        FROM backtest_results
        WHERE alpha_id = ?
    ''', (alpha_id,))
    
    payload_str = cursor.fetchone()[0]
    if payload_str:
        payload = json.loads(payload_str)
        prod_corr = payload.get('prod_corr', 'N/A')
        print(f'   Prod Corr: {prod_corr}')
        
        # 检查是否有其他关键指标
        if 'is' in payload:
            is_data = payload['is']
            print(f'   IS Sharpe: {is_data.get("sharpe", "N/A")}')
            print(f'   IS Fitness: {is_data.get("fitness", "N/A")}')
        
        if 'os' in payload:
            os_data = payload['os']
            print(f'   OS Sharpe: {os_data.get("sharpe", "N/A")}')
            print(f'   OS Fitness: {os_data.get("fitness", "N/A")}')
    else:
        print(f'   Prod Corr: N/A (no payload)')

conn.close()
