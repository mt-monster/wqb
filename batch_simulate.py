# -*- coding: utf-8 -*-
"""batch_simulate.py - GBR Wave 09 批量回测（使用 MCP create_multi_simulation）"""
import json
import os
import sys
import time
from pathlib import Path

# 添加项目根目录到路径以便导入 tools
PROJECT_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(PROJECT_ROOT))

from tools.mcp_5slot_batch import McpClient, normalize_settings

def load_exprs(path):
    with open(path, encoding='utf-8') as f:
        data = json.load(f)
    return data.get('expressions', [])

def main():
    # 初始化 MCP 客户端
    print("[INFO] 初始化 MCP 客户端...")
    try:
        client = McpClient()
    except Exception as e:
        print(f"[ERROR] 无法连接到 MCP 服务，请确保 wq-brain-http 已在 http://127.0.0.1:8876/mcp 运行: {e}")
        return

    # GBR 设置（camelCase，将被 normalize_settings 转换）
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
    
    # 转换为 MCP 参数格式
    mcp_settings = normalize_settings(settings)
    mcp_settings['wait_for_completion'] = False
    mcp_settings['validate_fields'] = False

    # 加载三个数据集的表达式
    base = PROJECT_ROOT / 'tracking' / 'GBR' / 'candidates'
    datasets = {
        'other455': load_exprs(base / 'wave09_other455_gate.json'),
        'model264': load_exprs(base / 'wave09_model264_gate.json'),
        'pattern_scores': load_exprs(base / 'wave09_pattern_scores_gate.json'),
    }
    
    # 准备批量提交
    all_exprs = []
    for ds, exprs in datasets.items():
        for e in exprs:
            all_exprs.append({
                'dataset': ds,
                'expression': e,
            })
    
    print(f"Total expressions: {len(all_exprs)}")
    print(f"Datasets: {list(datasets.keys())}")
    
    # 分批（每批最多 10 个，MCP create_multi_simulation 限制）
    batch_size = 8
    batches = [all_exprs[i:i + batch_size] for i in range(0, len(all_exprs), batch_size)]
    
    for batch_idx, batch in enumerate(batches, 1):
        print(f"\n=== Batch {batch_idx}: {len(batch)} expressions ===")
        for i, item in enumerate(batch, 1):
            print(f"  {i}. [{item['dataset']}] {item['expression'][:60]}...")
        
        # 构建 MCP payload
        payload = dict(mcp_settings)
        payload['alpha_expressions'] = [item['expression'] for item in batch]
        
        print(f"\nSubmitting batch {batch_idx} via MCP create_multi_simulation...")
        try:
            result = client.call("create_multi_simulation", payload, timeout=120.0)
            print(f"Batch {batch_idx} submitted successfully!")
            print(f"  Result: {json.dumps(result, indent=2, ensure_ascii=False)}")
            
            # 提取 location 或 multisim_id
            if isinstance(result, dict):
                location = result.get('location') or result.get('multisimulation_id')
                if location:
                    print(f"  Multisim ID: {location}")
                    
        except Exception as e:
            print(f"Batch {batch_idx} failed: {e}")
            import traceback
            traceback.print_exc()
            
        # 批次间稍作等待，避免触发并发限制
        if batch_idx < len(batches):
            print("\nWaiting before next batch...")
            time.sleep(5)

if __name__ == '__main__':
    main()
