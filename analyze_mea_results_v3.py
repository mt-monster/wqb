import json

with open(r'C:\Users\MENGTAO\.qoder-cn\cache\projects\wqb-a40170ec\agent-tools\task-d8b\18721ff2.txt') as f:
    data = json.load(f)

print(f'Total MEA alphas: {data["count"]}')
print('\n筛选达标 alpha (sharpe>1.58, fitness>1, turnover 5%-30%, 2y_sharpe>1.6, margin>5bp):')
print('='*80)

qualified = []
for alpha in data['results']:
    m = alpha['metrics']
    if (m['sharpe'] > 1.58 and m['fitness'] > 1 and 
        0.05 <= m['turnover'] <= 0.30 and
        m.get('two_year_sharpe', 0) > 1.6 and
        m.get('margin', 0) > 0.0005):
        qualified.append(alpha)
        print(f"ID: {alpha['id']}")
        print(f"  Sharpe: {m['sharpe']:.2f}, Fitness: {m['fitness']:.2f}, Turnover: {m['turnover']:.2%}")
        print(f"  2Y Sharpe: {m.get('two_year_sharpe', 0):.2f}, Margin: {m.get('margin', 0)*10000:.2f}bp")
        print(f"  Code: {alpha['code'][:100]}...")
        print()

print(f'\n达标 alpha 数量: {len(qualified)}/{data["count"]}')

# 显示 sharpe>1.5 的 alpha（接近达标）
print('\n接近达标 (sharpe>1.5, fitness>0.8, turnover 5%-30%):')
print('='*80)
near_qualified = []
for alpha in data['results']:
    m = alpha['metrics']
    if (m['sharpe'] > 1.5 and m['fitness'] > 0.8 and 
        0.05 <= m['turnover'] <= 0.30):
        near_qualified.append(alpha)
        print(f"ID: {alpha['id']}")
        print(f"  Sharpe: {m['sharpe']:.2f}, Fitness: {m['fitness']:.2f}, Turnover: {m['turnover']:.2%}")
        print(f"  2Y Sharpe: {m.get('two_year_sharpe', 0):.2f}, Margin: {m.get('margin', 0)*10000:.2f}bp")
        print(f"  Code: {alpha['code'][:100]}...")
        print()

print(f'\n接近达标 alpha 数量: {len(near_qualified)}/{data["count"]}')
