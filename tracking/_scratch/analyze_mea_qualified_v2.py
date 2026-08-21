import json

with open(r'C:\Users\MENGTAO\.qoder-cn\cache\projects\wqb-a40170ec\agent-tools\task-d8b\11b66668.txt') as f:
    data = json.load(f)

print(f'Total MEA alphas: {data["count"]}')
print('\n筛选达标 alpha (平台 IS 全部指标通过 + ra_failed_count=0):')
print('='*80)

qualified = []
for alpha in data['results']:
    # 检查 IS 指标是否全部通过
    checks = alpha.get('checks', {})
    ra = alpha.get('ra', {})
    
    # 平台 IS 硬闸：fail 必须为空，ra_failed_count 必须为 0
    is_pass = len(checks.get('fail', [])) == 0
    ra_pass = ra.get('failed_ra_count', 1) == 0
    
    if is_pass and ra_pass:
        m = alpha['metrics']
        # 额外筛选：sharpe>1.58, fitness>1, turnover 5%-30%, 2y_sharpe>1.6, margin>5bp
        if (m['sharpe'] > 1.58 and m['fitness'] > 1 and 
            0.05 <= m['turnover'] <= 0.30 and
            m.get('two_year_sharpe', 0) > 1.6 and
            m.get('margin', 0) > 0.0005):
            qualified.append(alpha)
            print(f"ID: {alpha['id']}")
            print(f"  Sharpe: {m['sharpe']:.2f}, Fitness: {m['fitness']:.2f}, Turnover: {m['turnover']:.2%}")
            print(f"  2Y Sharpe: {m.get('two_year_sharpe', 0):.2f}, Margin: {m.get('margin', 0)*10000:.2f}bp")
            print(f"  Code: {alpha['code'][:100]}...")
            print(f"  RA Failed Count: {ra.get('failed_ra_count', 0)}")
            print(f"  IS Fail: {checks.get('fail', [])}")
            print(f"  IS Warning: {[w['name'] for w in checks.get('warning', [])]}")
            print()

print(f'\n达标 alpha 数量: {len(qualified)}/{data["count"]}')

# 显示接近达标的 alpha（sharpe>1.5, fitness>0.8, ra_failed_count=0）
print('\n接近达标 (sharpe>1.5, fitness>0.8, ra_failed_count=0):')
print('='*80)
near_qualified = []
for alpha in data['results']:
    m = alpha['metrics']
    ra = alpha.get('ra', {})
    checks = alpha.get('checks', {})
    
    if (m['sharpe'] > 1.5 and m['fitness'] > 0.8 and 
        ra.get('failed_ra_count', 1) == 0 and
        len(checks.get('fail', [])) == 0):
        near_qualified.append(alpha)
        print(f"ID: {alpha['id']}")
        print(f"  Sharpe: {m['sharpe']:.2f}, Fitness: {m['fitness']:.2f}, Turnover: {m['turnover']:.2%}")
        print(f"  2Y Sharpe: {m.get('two_year_sharpe', 0):.2f}, Margin: {m.get('margin', 0)*10000:.2f}bp")
        print(f"  Code: {alpha['code'][:100]}...")
        print(f"  IS Warning: {[w['name'] for w in checks.get('warning', [])]}")
        print()

print(f'\n接近达标 alpha 数量: {len(near_qualified)}/{data["count"]}')