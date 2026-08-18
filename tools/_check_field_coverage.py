# -*- coding: utf-8 -*-
"""查 analyst44 与 order_book_imbalance 关键字段的数据覆盖 (dataset/startDate 等)。"""
import sys, os, asyncio

MCP_DIR = r'd:\coding\traeCN_project\wqb\world-quant-brain-mcp'
os.chdir(MCP_DIR)
sys.path.insert(0, MCP_DIR)
from brain_api import BrainApiClient  # noqa: E402

c = BrainApiClient()

TARGETS = [
    ('analyst44', 'anl44_eps_best_eeps_cur_yr'),
    ('analyst44', 'anl44_eps_best_eeps_nxt_yr'),
    ('order_book_imbalance', 'dark_trade_volume'),
    ('order_book_imbalance', 'trade_market_impact_coefficient'),
]

async def main():
    await c.ensure_authenticated()
    data = await c.get_datafields(instrument_type='EQUITY', region='USA', delay=1,
                                  universe='TOP3000', theme='false', dataset_id=None,
                                  data_type='', search=None, filter_sharpe=False)
    results = data.get('results', []) if isinstance(data, dict) else data
    by_name = {r.get('id'): r for r in results if isinstance(r, dict)}
    for ds, fname in TARGETS:
        r = by_name.get(fname)
        if not r:
            print(f'=== {ds}/{fname}: NOT FOUND')
            continue
        meta = r.get('meta', {}) or {}
        print(f'=== {ds}/{fname}')
        print(f'    coverage={r.get("coverage")} type={r.get("type")} users={r.get("userCount")}')
        print(f'    meta: {json_dumps(meta)[:300]}')

def json_dumps(o):
    import json
    return json.dumps(o, default=str, ensure_ascii=False)

asyncio.run(main())
