# -*- coding: utf-8 -*-
"""batch_simulate.py - GBR Wave 09 批量回测（8并发 create_multi_simulation）"""
import json
import os
import sys
import time

sys.path.insert(0, r'D:\coding\traeCN_project\wqb\.workbuddy\skills\wq-brain-campaign-toolkit\scripts')
from _lib.common import load_credentials
from _lib.api import Api, api_call

def load_exprs(path):
    with open(path, encoding='utf-8') as f:
        data = json.load(f)
    return data.get('expressions', [])

def main():
    # 加载凭证并登录
    email, password = load_credentials()
    api = Api()
    api.login(email, password)
    print("Logged in successfully")
    
    # GBR 设置（与 create_multi_simulation 格式对齐）
    settings = {
        'instrumentType': 'EQUITY',
        'region': 'GBR',
        'universe': 'TOP700',
        'delay': 1,
        'decay': 4,
        'neutralization': 'SUBINDUSTRY',
        'truncation': 0.08,
        'pasteurization': 'ON',
        'language': 'FASTEXPR',
        'visualization': False,
        'testPeriod': 'P0Y0M',
        'maxTrade': 'ON',
        'unitHandling': 'VERIFY',
        'nanHandling': 'OFF',
    }
    
    # 加载三个数据集的表达式
    base = r'D:\coding\traeCN_project\wqb\tracking\GBR\candidates'
    datasets = {
        'other455': load_exprs(os.path.join(base, 'wave09_other455_gate.json')),
        'model264': load_exprs(os.path.join(base, 'wave09_model264_gate.json')),
        'pattern_scores': load_exprs(os.path.join(base, 'wave09_pattern_scores_gate.json')),
    }
    
    # 准备批量提交（每个数据集4个，共12个，分2批，每批8个槽位）
    all_exprs = []
    for ds, exprs in datasets.items():
        for e in exprs:
            all_exprs.append({
                'dataset': ds,
                'expression': e,
                'settings': settings
            })
    
    print(f"Total expressions: {len(all_exprs)}")
    print(f"Datasets: {list(datasets.keys())}")
    
    # 第一批：8个表达式（other455 4个 + model264 4个）
    batch1 = all_exprs[:8]
    batch2 = all_exprs[8:]
    
    print(f"\n=== Batch 1: {len(batch1)} expressions ===")
    for i, item in enumerate(batch1, 1):
        print(f"  {i}. [{item['dataset']}] {item['expression'][:60]}...")
    
    # 提交第一批
    batch1_payload = [{
        'type': 'REGULAR',
        'settings': item['settings'],
        'regular': item['expression']
    } for item in batch1]
    
    print("\nSubmitting batch 1...")
    try:
        resp = api_call(api, 'post', '/simulations', batch1_payload)
        # 检查响应状态
        if resp.status == 201:
            location = resp.headers.get('Location', '')
            print(f"Batch 1 submitted successfully!")
            print(f"  Location: {location}")
            print(f"  Multisim ID: {location.split('/')[-1] if location else 'N/A'}")
        else:
            result = json.loads(resp.read())
            print(f"Batch 1 response: {result}")
    except Exception as e:
        print(f"Batch 1 failed: {e}")
        import traceback
        traceback.print_exc()
        return
    
    # 等待第一批完成
    print("\nWaiting for batch 1 to complete...")
    time.sleep(10)
    
    # 提交第二批
    if batch2:
        print(f"\n=== Batch 2: {len(batch2)} expressions ===")
        for i, item in enumerate(batch2, 1):
            print(f"  {i}. [{item['dataset']}] {item['expression'][:60]}...")
        
        batch2_payload = [{
            'type': 'REGULAR',
            'settings': item['settings'],
            'regular': item['expression']
        } for item in batch2]
        
        print("\nSubmitting batch 2...")
        try:
            resp = api_call(api, 'post', '/simulations', batch2_payload)
            if resp.status == 201:
                location = resp.headers.get('Location', '')
                print(f"Batch 2 submitted successfully!")
                print(f"  Location: {location}")
                print(f"  Multisim ID: {location.split('/')[-1] if location else 'N/A'}")
            else:
                result = json.loads(resp.read())
                print(f"Batch 2 response: {result}")
        except Exception as e:
            print(f"Batch 2 failed: {e}")

if __name__ == '__main__':
    main()
