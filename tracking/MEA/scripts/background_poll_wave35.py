#!/usr/bin/env python3
"""后台轮询 wave35 回测结果"""
import requests
import json
import time
from pathlib import Path
from datetime import datetime

# 读取 .env
env_path = Path('world-quant-brain-mcp/.env')
config = {}
with open(env_path) as f:
    for line in f:
        if '=' in line and not line.startswith('#'):
            k, v = line.strip().split('=', 1)
            config[k] = v.strip('"')

auth = (config['CREDENTIALS_EMAIL'], config['CREDENTIALS_PASSWORD'])
base_url = 'https://api.worldquantbrain.com'

# 所有子模拟 ID
all_children = [
    # Batch 1: fundamental72
    "1YEKC31GN4q7ceG1gt9FSb5K", "3D4lX2dx55iZbJJ1fjbacHhk", "2OWOq6aoO4jP98c5FqAn2rr", "44fCgodsA4xgavWGlOw5B6S",
    "3X9nCmgNC56ab2fkQIZnxuh", "44aQ1vb294oU8GH1aQi6woXU", "3EDSLyddO4i1bnMvGG4pHpr", "2JrWwCMX4Lfag6O5nG9OdK",
    # Batch 2: analyst7 + mixed
    "DCsXFgs54Ueb0UWE5oMubx", "13OaiBfPJ4RKc55OartkpUG", "3BUjQZ2Qt4lucutkvs1Yl7Q", "2wI2se8rn4zA9MR1gwA65LPX",
    "2zrwLB6H14AYaLhoCnTZqah", "hsryJPe4gqbQV8IzfqheE", "3p7jAj4MM4uW8FVMLKG3c5V", "3fKloz6ty4BtajFRcGC9Uwe"
]

def get_json(url):
    try:
        resp = requests.get(url, auth=auth, timeout=30)
        if resp.status_code == 200:
            return resp.json()
    except:
        pass
    return None

def poll_child(child_id):
    """轮询单个子模拟"""
    sim_resp = get_json(f"{base_url}/simulations/{child_id}")
    if not sim_resp:
        return None
    
    status = sim_resp.get('status')
    if status in ['DONE', 'COMPLETE']:
        alpha_id = sim_resp.get('alpha')
        if alpha_id:
            alpha_resp = get_json(f"{base_url}/alphas/{alpha_id}")
            if alpha_resp:
                is_data = alpha_resp.get('is', {})
                return {
                    'sim_id': child_id,
                    'alpha_id': alpha_id,
                    'expr': alpha_resp.get('regular', ''),
                    'sharpe': is_data.get('sharpe'),
                    'fitness': is_data.get('fitness'),
                    'turnover': is_data.get('turnover'),
                    'margin': is_data.get('margin'),
                    'returns': is_data.get('returns'),
                    'is': is_data,
                    'os': alpha_resp.get('os', {}),
                    'status': 'DONE'
                }
    elif status in ['ERROR', 'FAILED', 'CANCELLED']:
        return {'sim_id': child_id, 'status': status}
    
    return {'sim_id': child_id, 'status': 'RUNNING'}

def main():
    print(f"[{datetime.now()}] Starting background polling for wave35...")
    
    completed = []
    max_iterations = 60  # 最多轮询 60 次（30 分钟）
    
    for iteration in range(max_iterations):
        print(f"\n[Iteration {iteration+1}/{max_iterations}] {datetime.now()}")
        
        remaining = []
        for child_id in all_children:
            # 跳过已完成的
            if any(c['sim_id'] == child_id for c in completed):
                continue
            
            result = poll_child(child_id)
            if result:
                if result['status'] == 'DONE':
                    completed.append(result)
                    sharpe = result.get('sharpe', 'N/A')
                    fitness = result.get('fitness', 'N/A')
                    print(f"  ✓ {child_id}: sharpe={sharpe}, fitness={fitness}")
                elif result['status'] in ['ERROR', 'FAILED', 'CANCELLED']:
                    print(f"  ✗ {child_id}: {result['status']}")
                else:
                    remaining.append(child_id)
        
        print(f"  Progress: {len(completed)}/{len(all_children)} completed, {len(remaining)} running")
        
        if len(completed) + len([c for c in completed if c.get('status') in ['ERROR', 'FAILED', 'CANCELLED']]) >= len(all_children):
            print("\n✅ All simulations completed!")
            break
        
        # 保存中间结果
        output_file = 'tracking/MEA/results/wave35_results_partial.json'
        Path(output_file).parent.mkdir(parents=True, exist_ok=True)
        with open(output_file, 'w') as f:
            json.dump(completed, f, indent=2)
        
        time.sleep(30)  # 每 30 秒轮询一次
    
    # 保存最终结果
    output_file = 'tracking/MEA/results/wave35_results_final.json'
    with open(output_file, 'w') as f:
        json.dump(completed, f, indent=2)
    
    print(f"\n✅ Saved {len(completed)} results to {output_file}")
    
    # 筛选达标 alpha
    qualified = [c for c in completed if c.get('sharpe') and c['sharpe'] > 1.58 and c.get('fitness') and c['fitness'] > 1]
    print(f"\n📊 Qualified alphas (sharpe>1.58, fitness>1): {len(qualified)}")
    for q in qualified:
        print(f"  - {q['alpha_id']}: sharpe={q['sharpe']:.2f}, fitness={q['fitness']:.2f}, turnover={q.get('turnover', 'N/A')}")

if __name__ == '__main__':
    main()
