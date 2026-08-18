#!/usr/bin/env python3
"""GBR 平台体检脚本 - 查询数据集和设置选项"""
import asyncio
import sys
sys.path.insert(0, 'world-quant-brain-mcp')

from brain_api import brain_client

async def check_gbr():
    await brain_client.ensure_authenticated()
    
    # 获取 GBR 数据集
    print('=== GBR Datasets (TOP700, D1) ===')
    datasets = await brain_client.get_datasets(None, 'GBR', 1, 'TOP700', 'false', None)
    for ds in datasets.get('results', [])[:30]:
        print(f"{ds.get('id')}: alphaCount={ds.get('alphaCount')}, fieldCount={ds.get('fieldCount')}, coverage={ds.get('coverage')}")
    
    # 获取平台设置选项
    print('\n=== GBR Platform Settings ===')
    try:
        settings = await brain_client.get_platform_setting_options('GBR', 1)
        print(settings)
    except Exception as e:
        print(f"Settings error: {e}")

if __name__ == '__main__':
    asyncio.run(check_gbr())
