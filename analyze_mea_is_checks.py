import json

with open(r'C:\Users\MENGTAO\.qoder-cn\cache\projects\wqb-a40170ec\agent-tools\task-d8b\6944196e.txt') as f:
    data = json.load(f)

print(f'Total MEA alphas: {data["count"]}')
print('\n筛选达标 alpha (平台 IS 全部指标通过):')
print('='*80)

qualified = []
for alpha in data['results']:
    # 检查 IS 指标是否全部通过
    is_checks = alpha.get('is', {})
    if not is_checks:
        continue
    
    # 平台 IS 硬闸：所有 check 都必须为 PASS
    all_pass = all(check.get('result') == 'PASS' for check in is_checks.values() if isinstance(check, dict))
    
    if all_pass:
        m = alpha['metrics']
        qualified.append(alpha)
        print(f"ID: {alpha['id']}")
        print(f"  Sharpe: {m['sharpe']:.2f}, Fitness: {m['fitness']:.2f}, Turnover: {m['turnover']:.2%}")
        print(f"  2Y Sharpe: {m.get('two_year_sharpe', 0):.2f}, Margin: {m.get('margin', 0)*10000:.2f}bp")
        print(f"  Code: {alpha['code'][:100]}...")
        print(f"  IS Checks: {list(is_checks.keys())}")
        print()

print(f'\n达标 alpha 数量: {len(qualified)}/{data["count"]}')

# 显示接近达标的 alpha（至少 sharpe>1.5）
print('\n接近达标 (sharpe>1.5, fitness>0.8):')
print('='*80)
near_qualified = []
for alpha in data['results']:
    m = alpha['metrics']
    if m['sharpe'] > 1.5 and m['fitness'] > 0.8:
        is_checks = alpha.get('is', {})
        failed_checks = [k for k, v in is_checks.items() if isinstance(v, dict) and v.get('result') != 'PASS']
        near_qualified.append(alpha)
        print(f"ID: {alpha['id']}")
        print(f"  Sharpe: {m['sharpe']:.2f}, Fitness: {m['fitness']:.2f}, Turnover: {m['turnover']:.2%}")
        print(f"  2Y Sharpe: {m.get('two_year_sharpe', 0):.2f}, Margin: {m.get('margin', 0)*10000:.2f}bp")
        print(f"  Failed IS checks: {failed_checks}")
        print(f"  Code: {alpha['code'][:100]}...")
        print()

print(f'\n接近达标 alpha 数量: {len(near_qualified)}/{data["count"]}')