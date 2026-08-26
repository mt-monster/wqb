import sys
sys.path.insert(0, 'd:/coding/traeCN_project/wqb/src')
from wqb.store import CampaignStore
import subprocess
import json

store = CampaignStore('d:/coding/traeCN_project/wqb/data/wqb.db')

# 从 checkpoint 中获取 alpha IDs
ckpt = store.get_ledger('USA', 'ckpt_w18')
alpha_ids = []
for batch in ckpt.get('batches', []):
    alpha_ids.extend(batch.get('alphas', []))

print(f"\n=== Wave 18 Alpha IDs ({len(alpha_ids)} 个) ===")

# 使用 MCP 工具查询每个 alpha 的详细信息
results = []
for alpha_id in alpha_ids:
    try:
        # 调用 MCP 工具
        result = subprocess.run(
            ['python', '-c', f'''
import json
import sys
sys.path.insert(0, "C:/Users/MENGTAO/AppData/Roaming/QoderCN/SharedClientCache/projects/d--coding-traeCN_project-wqb/mcps/wq-brain-http")
from wq_brain_http import get_alpha_details
result = get_alpha_details("{alpha_id}")
print(json.dumps(result))
'''],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode == 0:
            alpha = json.loads(result.stdout)
            metrics = alpha.get('metrics', {})
            checks = alpha.get('checks', {})
            
            results.append({
                'alpha_id': alpha_id,
                'fitness': metrics.get('fitness', 0) or 0,
                'sharpe': metrics.get('sharpe', 0) or 0,
                'turnover': metrics.get('turnover', 0) or 0,
                'status': alpha.get('status', 'N/A'),
                'expression': alpha.get('code', 'N/A'),
                'failed_checks': len(checks.get('fail', [])),
                'warning_checks': len(checks.get('warning', [])),
                'pending_checks': len(checks.get('pending', []))
            })
        else:
            print(f"警告: 查询 {alpha_id} 失败: {result.stderr}")
    except Exception as e:
        print(f"警告: 查询 {alpha_id} 异常: {e}")

# 按 fitness 排序
sorted_results = sorted(results, key=lambda x: x['fitness'], reverse=True)

print(f"\n=== Wave 18 回测结果（按 Fitness 排序）===")
for i, r in enumerate(sorted_results, 1):
    print(f"{i}. Alpha ID: {r['alpha_id']}")
    print(f"   Fitness: {r['fitness']:.2f}, Sharpe: {r['sharpe']:.2f}, Turnover: {r['turnover']:.4f}")
    print(f"   Status: {r['status']}")
    print(f"   Checks: fail={r['failed_checks']}, warning={r['warning_checks']}, pending={r['pending_checks']}")
    expr = r['expression'][:80] + '...' if len(r['expression']) > 80 else r['expression']
    print(f"   Expression: {expr}")
    print()

# 统计 Fitness >= 1.0 的候选
candidates = [r for r in results if r['fitness'] >= 1.0]
print(f"\n=== Fitness >= 1.0 的候选: {len(candidates)} 个 ===")
for i, r in enumerate(candidates, 1):
    print(f"{i}. {r['alpha_id']}: Fitness={r['fitness']:.2f}, Sharpe={r['sharpe']:.2f}, fail={r['failed_checks']}, warning={r['warning_checks']}, pending={r['pending_checks']}")
