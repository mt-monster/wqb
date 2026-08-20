import json

with open(r'C:\Users\MENGTAO\.qoder-cn\cache\projects\wqb-a40170ec\agent-tools\task-d8b\8f05bf0a.txt') as f:
    data = json.load(f)

print(f'Total MEA alphas: {data["count"]}')

# 筛选达标 alpha
qualified = []
for alpha in data['results']:
    checks = alpha.get('checks', {})
    ra = alpha.get('ra', {})
    
    is_pass = len(checks.get('fail', [])) == 0
    ra_pass = ra.get('failed_ra_count', 1) == 0
    
    if is_pass and ra_pass:
        m = alpha['metrics']
        if (m['sharpe'] > 1.58 and m['fitness'] > 1 and 
            0.05 <= m['turnover'] <= 0.30 and
            m.get('two_year_sharpe', 0) > 1.6 and
            m.get('margin', 0) > 0.0005):
            qualified.append(alpha)

print(f'达标 alpha 数量: {len(qualified)}/{data["count"]}')

if qualified:
    print('\n达标 alpha 列表:')
    for alpha in qualified:
        m = alpha['metrics']
        print(f"ID: {alpha['id']}, Sharpe: {m['sharpe']:.2f}, Fitness: {m['fitness']:.2f}, Code: {alpha['code'][:60]}...")
else:
    print('\n无达标 alpha')
    
# 显示最新的 10 个 alpha
print('\n最新 10 个 alpha:')
for alpha in data['results'][:10]:
    m = alpha['metrics']
    ra = alpha.get('ra', {})
    print(f"ID: {alpha['id']}, Sharpe: {m['sharpe']:.2f}, RA Failed: {ra.get('failed_ra_count', 'N/A')}, Code: {alpha['code'][:60]}...")