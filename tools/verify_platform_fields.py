"""平台字段校验：对比本地库 vs 平台真实字段，找出「本地有、平台无」的幽灵字段。
用法: python tools/verify_platform_fields.py <ds1> <ds2> ...
"""
import asyncio
import json
import os
import sqlite3          # 仅用于 sqlite3.Row（连接本身一律走 db_connect）
import sys

import _pyenv  # noqa: E402  # tools/ 在 sys.path[0]
_pyenv.bootstrap_paths()

from brain_api import brain_client  # noqa: E402
from wqb.db_conn import connect as db_connect, default_db_path  # noqa: E402

# 2026-10-27：原先写 `'data/wqb.db'` / `'results/...'`（cwd 相对），换个目录跑就静默指向
# 不存在的库或把结果丢到仓库外。库位改由规范工厂解析（尊重 WQB_DB_PATH），产物锚定仓库根。
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB = default_db_path()
OUT = os.path.join(ROOT, 'results', 'platform_field_verification.json')


async def pull(ds):
    """拉取平台该数据集全部字段（方法内部分页），返回 {field_name: type}"""
    r = await brain_client.get_datafields(
        instrument_type='EQUITY', region='EUR', delay=1,
        universe='TOPCS1600', dataset_id=ds)
    j = r if isinstance(r, dict) else {}
    res = j.get('results') or []
    got = {}
    for it in res:
        got[it.get('id')] = it.get('type')
    if not got:
        print(f'   [warn] {ds}: platform returned 0 fields '
              f'(keys={list(j.keys())[:6]}, count={j.get("count")})', flush=True)
    return got


async def main():
    targets = sys.argv[1:]
    con = db_connect(DB, readonly=True)
    con.row_factory = sqlite3.Row
    await brain_client.ensure_authenticated()
    out = {}
    for ds in targets:
        try:
            plat = await pull(ds)
        except Exception as e:
            print(f'{ds}: platform pull FAILED {str(e)[:60]}', flush=True)
            out[ds] = {'error': str(e)[:120]}
            continue
        loc = {r['field_name']: r['field_type'] for r in con.execute(
            '''SELECT f.field_name, f.field_type FROM fields f
               JOIN datasets d ON f.dataset_id=d.id JOIN regions r ON d.region_id=r.id
               WHERE r.name='EUR' AND d.name=?''', (ds,))}
        ghost = sorted(set(loc) - set(plat))
        missing = sorted(set(plat) - set(loc))
        print(f'{ds}: platform={len(plat)} local={len(loc)} ghost(local-only)={len(ghost)} '
              f'platform-only={len(missing)}', flush=True)
        if ghost:
            print(f'   ghost e.g.: {ghost[:4]}', flush=True)
        out[ds] = {'platform': len(plat), 'local': len(loc),
                   'ghost': ghost, 'platform_only': missing,
                   'platform_types': plat}
    json.dump(out, open(OUT, 'w', encoding='utf-8'), indent=1)
    print('saved', OUT)


asyncio.run(main())
