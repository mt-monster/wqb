import sys
sys.path.insert(0, 'd:/coding/traeCN_project/wqb/src')
from wqb.store import CampaignStore
import json

store = CampaignStore('d:/coding/traeCN_project/wqb/data/wqb.db')

# 从 checkpoint 中获取 alpha IDs
ckpt = store.get_ledger('USA', 'ckpt_w18')
if not ckpt:
    print("未找到 checkpoint")
    sys.exit(1)

alpha_ids = []
for batch in ckpt.get('batches', []):
    alpha_ids.extend(batch.get('alphas', []))

print(f"\n=== Wave 18 Alpha IDs ({len(alpha_ids)} 个) ===")
for i, alpha_id in enumerate(alpha_ids, 1):
    print(f"{i}. {alpha_id}")

# 查询每个 alpha 的详细信息
print(f"\n=== 查询 Alpha 详细信息 ===")
results = []
for alpha_id in alpha_ids:
    # 从数据库查询
    alpha = store.get_alpha_by_id(alpha_id)
    if alpha:
        results.append({
            'alpha_id': alpha_id,
            'fitness': alpha.get('fitness', 0) or 0,
            'sharpe': alpha.get('sharpe', 0) or 0,
            'turnover': alpha.get('turnover', 0) or 0,
            'status': alpha.get('status', 'N/A'),
            'expression': alpha.get('expression', 'N/A')
        })
    else:
        print(f"警告: 未找到 {alpha_id} 的详细信息")

# 按 fitness 排序
sorted_results = sorted(results, key=lambda x: x['fitness'], reverse=True)

print(f"\n=== Wave 18 回测结果（按 Fitness 排序）===")
for i, r in enumerate(sorted_results, 1):
    print(f"{i}. Alpha ID: {r['alpha_id']}")
    print(f"   Fitness: {r['fitness']:.2f}, Sharpe: {r['sharpe']:.2f}, Turnover: {r['turnover']:.4f}")
    print(f"   Status: {r['status']}")
    expr = r['expression'][:80] + '...' if len(r['expression']) > 80 else r['expression']
    print(f"   Expression: {expr}")
    print()

# 统计 Fitness >= 1.0 的候选
candidates = [r for r in results if r['fitness'] >= 1.0]
print(f"\n=== Fitness >= 1.0 的候选: {len(candidates)} 个 ===")
for i, r in enumerate(candidates, 1):
    print(f"{i}. {r['alpha_id']}: Fitness={r['fitness']:.2f}, Sharpe={r['sharpe']:.2f}")
