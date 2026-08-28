#!/usr/bin/env python3
"""轮询 wave35 回测结果"""
import sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
sys.path.insert(0, 'world-quant-brain-mcp')

from brain_api import brain_client
import json
import time

def poll_multisim(multisim_id, max_wait=300):
    """轮询 multisim 直到完成"""
    print(f"Polling {multisim_id}...")
    
    # 获取子模拟
    children_resp = brain_client.get(f"/simulations/{multisim_id}/children")
    if not children_resp or 'children' not in children_resp:
        print(f"No children found for {multisim_id}")
        return []
    
    children = children_resp['children']
    print(f"Found {len(children)} children")
    
    results = []
    for child in children:
        child_id = child.get('id') or child.get('location', '').split('/')[-1]
        if not child_id:
            continue
            
        # 轮询子模拟状态
        start = time.time()
        while time.time() - start < max_wait:
            sim_resp = brain_client.get(f"/simulations/{child_id}")
            if sim_resp and sim_resp.get('status') == 'DONE':
                alpha_id = sim_resp.get('alpha')
                if alpha_id:
                    # 获取 alpha 详情
                    alpha_resp = brain_client.get(f"/alphas/{alpha_id}")
                    if alpha_resp:
                        results.append({
                            'sim_id': child_id,
                            'alpha_id': alpha_id,
                            'expr': alpha_resp.get('regular', ''),
                            'is': alpha_resp.get('is', {}),
                            'os': alpha_resp.get('os', {})
                        })
                        print(f"  {child_id} -> {alpha_id}: sharpe={alpha_resp.get('is', {}).get('sharpe', 'N/A')}")
                        break
            time.sleep(5)
    
    return results

if __name__ == '__main__':
    # 两批 multisim
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
    with open(output_file, 'w') as f:
        json.dump(all_results, f, indent=2)
    
    print(f"\n✅ Saved {len(all_results)} results to {output_file}")
    
    # 筛选达标 alpha
    qualified = [r for r in all_results if r.get('is', {}).get('sharpe', 0) > 1.58 and r.get('is', {}).get('fitness', 0) > 1]
    print(f"📊 Qualified alphas (sharpe>1.58, fitness>1): {len(qualified)}")
    for q in qualified:
        print(f"  - {q['alpha_id']}: sharpe={q['is']['sharpe']:.2f}, fitness={q['is']['fitness']:.2f}")
