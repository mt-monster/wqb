#!/usr/bin/env python3
"""轮询 wave35 回测结果 - 简化版"""
import requests
import json
import time
from pathlib import Path

# 读取 .env
env_path = Path('world-quant-brain-mcp/.env')
config = {}
with open(env_path) as f:
    for line in f:
        if '=' in line and not line.startswith('#'):
            k, v = line.strip().split('=', 1)
            config[k] = v

auth = (config['CREDENTIALS_EMAIL'], config['CREDENTIALS_PASSWORD'])
base_url = 'https://api.worldquantbrain.com'

def get_json(url):
    resp = requests.get(url, auth=auth)
    if resp.status_code == 200:
        return resp.json()
    return None

def poll_multisim(multisim_id, max_wait=600):
    """轮询 multisim 直到完成"""
    print(f"Polling {multisim_id}...")
    
    # 等待子模拟生成
    time.sleep(10)
    
    # 获取子模拟
    children_resp = get_json(f"{base_url}/simulations/{multisim_id}/children")
    if not children_resp or 'children' not in children_resp:
        print(f"No children found for {multisim_id}")
        return []
    
    children = children_resp['children']
    print(f"Found {len(children)} children")
    
    results = []
    for child in children:
        child_url = child if isinstance(child, str) else child.get('url') or child.get('location')
        child_id = child_url.split('/')[-1] if '/' in child_url else child_url
        
        # 轮询子模拟状态
        start = time.time()
        while time.time() - start < max_wait:
            sim_resp = get_json(f"{base_url}/simulations/{child_id}")
            if sim_resp:
                status = sim_resp.get('status')
                if status == 'DONE' or status == 'COMPLETE':
                    alpha_id = sim_resp.get('alpha')
                    if alpha_id:
                        # 获取 alpha 详情
                        alpha_resp = get_json(f"{base_url}/alphas/{alpha_id}")
                        if alpha_resp:
                            is_data = alpha_resp.get('is', {})
                            results.append({
                                'sim_id': child_id,
                                'alpha_id': alpha_id,
                                'expr': alpha_resp.get('regular', ''),
                                'sharpe': is_data.get('sharpe'),
                                'fitness': is_data.get('fitness'),
                                'turnover': is_data.get('turnover'),
                                'margin': is_data.get('margin'),
                                'is': is_data,
                                'os': alpha_resp.get('os', {})
                            })
                            print(f"  ✓ {child_id} -> {alpha_id}: sharpe={is_data.get('sharpe', 'N/A')}")
                            break
                elif status in ['ERROR', 'FAILED']:
                    print(f"  ✗ {child_id}: {status}")
                    break
            time.sleep(10)
    
    return results

if __name__ == '__main__':
    batch1 = '1NvPlgd5o4vBbxqPEHkoaOx'  # fundamental72
    batch2 = 'Zuv59emn4j5cpE1aWFxGAlO'  # analyst7 + mixed
    
    all_results = []
    
    print("=== Batch 1: fundamental72 ===")
    results1 = poll_multisim(batch1)
    all_results.extend(results1)
    
    print("\n=== Batch 2: analyst7 + mixed ===")
    results2 = poll_multisim(batch2)
    all_results.extend(results2)
    
    # 保存结果
    output_file = 'tracking/MEA/results/wave35_results.json'
    Path(output_file).parent.mkdir(parents=True, exist_ok=True)
    with open(output_file, 'w') as f:
        json.dump(all_results, f, indent=2)
    
    print(f"\n✅ Saved {len(all_results)} results to {output_file}")
    
    # 筛选达标 alpha
    qualified = [r for r in all_results if r.get('sharpe') and r['sharpe'] > 1.58 and r.get('fitness') and r['fitness'] > 1]
    print(f"📊 Qualified alphas (sharpe>1.58, fitness>1): {len(qualified)}")
    for q in qualified:
        print(f"  - {q['alpha_id']}: sharpe={q['sharpe']:.2f}, fitness={q['fitness']:.2f}, turnover={q.get('turnover', 'N/A')}")
