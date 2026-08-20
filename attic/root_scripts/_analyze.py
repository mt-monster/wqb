import json

# 读取数据质量报告 (尝试不同编码)
for enc in ['utf-8-sig', 'gbk', 'latin-1']:
    try:
        with open('tracking/ASI/asi_d1_data_quality.json', encoding=enc) as f:
            data = json.load(f)
        print(f'编码: {enc}')
        break
    except:
        continue

# 打印顶层 keys
print('顶层 keys:', list(data.keys()))

# 查找 analyst 数据集
if 'datasets' in data:
    analyst_datasets = [d for d in data['datasets'] if 'analyst' in d.get('dataset', '').lower()]
    print('\nAnalyst 数据集:')
    for d in analyst_datasets:
        print(f"  {d['dataset']}: count={d.get('count', 0)}, sharpe={d.get('sharpe', 0):.3f}")

if 'recommendations' in data:
    print('\n推荐数据集中的 Analyst:')
    for d in data['recommendations']:
        if 'analyst' in d.get('dataset', '').lower():
            print(f"  {d['dataset']}: score={d.get('score', 0):.3f}")
