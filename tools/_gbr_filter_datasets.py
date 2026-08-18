#!/usr/bin/env python3
"""GBR 数据集筛选 - 硬门槛: coverage>=0.65, alphaCount<=100, fieldCount>=10"""
import asyncio
import sys
sys.path.insert(0, 'world-quant-brain-mcp')

from brain_api import brain_client

async def filter_gbr_datasets():
    await brain_client.ensure_authenticated()
    
    # 获取所有 GBR 数据集
    datasets = await brain_client.get_datasets(None, 'GBR', 1, 'TOP700', 'false', None)
    
    # 硬门槛筛选
    qualified = []
    for ds in datasets.get('results', []):
        cov = ds.get('coverage', 0) or 0
        ac = ds.get('alphaCount', 999) or 999
        fc = ds.get('fieldCount', 0) or 0
        
        if cov >= 0.65 and ac <= 100 and fc >= 10:
            qualified.append({
                'id': ds.get('id'),
                'alphaCount': ac,
                'fieldCount': fc,
                'coverage': cov,
                'pyramid': ds.get('pyramid', False)
            })
    
    # 按 coverage 排序
    qualified.sort(key=lambda x: x['coverage'], reverse=True)
    
    print('=== GBR 合格数据集 (coverage>=0.65, alphaCount<=100, fieldCount>=10) ===')
    print(f"{'Dataset':<30} {'AlphaCount':<12} {'FieldCount':<12} {'Coverage':<10} {'Pyramid'}")
    print('-' * 80)
    for q in qualified:
        print(f"{q['id']:<30} {q['alphaCount']:<12} {q['fieldCount']:<12} {q['coverage']:<10.4f} {q['pyramid']}")
    
    print(f"\n总计: {len(qualified)} 个合格数据集")
    
    # 标记金字塔数据集
    pyramid_ds = [q for q in qualified if q['pyramid']]
    print(f"金字塔数据集: {len(pyramid_ds)} 个")
    for p in pyramid_ds:
        print(f"  - {p['id']}")

if __name__ == '__main__':
    asyncio.run(filter_gbr_datasets())
