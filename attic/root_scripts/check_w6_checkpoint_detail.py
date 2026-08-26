import sqlite3
import json

conn = sqlite3.connect('data/wqb.db')
cursor = conn.cursor()

# 查询 wave 6 的 checkpoint
cursor.execute("SELECT value FROM ledger_kv WHERE region='USA' AND key='ckpt_w6'")
result = cursor.fetchone()

if result:
    data = json.loads(result[0])
    print("Wave 6 Checkpoint 内容:")
    print(f"  wave: {data.get('wave')}")
    print(f"  stages: {list(data.get('stages', {}).keys())}")
    
    # 检查各个阶段
    stages = data.get('stages', {})
    for stage_name, stage_data in stages.items():
        print(f"\n  阶段: {stage_name}")
        if isinstance(stage_data, dict):
            print(f"    done: {stage_data.get('done')}")
            if 'total' in stage_data:
                print(f"    total: {stage_data.get('total')}")
            if 'passed' in stage_data:
                print(f"    passed: {len(stage_data.get('passed', []))}")
            if 'results' in stage_data:
                print(f"    results: {len(stage_data.get('results', []))}")
else:
    print("未找到 wave 6 的 checkpoint")

conn.close()
