# -*- coding: utf-8 -*-
"""快速查询 6 个参考 GLB 数据集的字段数"""
import sys
sys.path.insert(0, 'glb_alpha_machine')
from glb_machine_lib import login, get_datafields

REF_DATASETS = {
    'analyst15': 'TOP3000',
    'analyst47': 'TOP3000',
    'model106': 'TOP3000',
    'model109': 'TOP3000',
    'news87': 'TOP3000',
    'other432': 'MINVOL1M',
}

s = login()
for dd, uni in REF_DATASETS.items():
    try:
        df = get_datafields(s, dataset_id=dd, region='GLB', universe=uni, delay=1)
        n_matrix = len(df[df['type'] == 'MATRIX'])
        n_vector = len(df[df['type'] == 'VECTOR'])
        cov = df['coverage'].mean() if len(df) > 0 and 'coverage' in df.columns else 'N/A'
        print(f'{dd:12s} ({uni:8s}): total={len(df):4d}  MATRIX={n_matrix:4d}  VECTOR={n_vector:4d}  avg_cov={cov:.2f}')
        if len(df) > 0:
            print(f'  样例: {df.head(3)["id"].tolist()}')
    except Exception as e:
        print(f'{dd:12s}: ERROR {type(e).__name__}: {e}')