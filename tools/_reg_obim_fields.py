# -*- coding: utf-8 -*-
"""登记 order_book_imbalance 字段到 fields_gate.json（USA/TOP3000/D1 scope，全 VECTOR）。"""
import sys, os, json, asyncio
from pathlib import Path

MCP_DIR = Path(r'd:\coding\traeCN_project\wqb\world-quant-brain-mcp')
sys.path.insert(0, str(MCP_DIR))
os.chdir(str(MCP_DIR))

from brain_api import BrainApiClient  # noqa: E402

GATE_DIR = r'd:\coding\traeCN_project\wqb\data\fields_gate'
SCOPE = 'USA/TOP3000/D1'
DS = 'order_book_imbalance'

async def main():
    client = BrainApiClient()
    await client.ensure_authenticated()
    data = await client.get_datafields(
        instrument_type='EQUITY', region='USA', delay=1, universe='TOP3000',
        theme='false', dataset_id=DS, data_type='', search=None, filter_sharpe=False,
    )
    fields = data.get('results', []) if isinstance(data, dict) else data
    print(f'fetched {len(fields)} fields')

    fpath = os.path.join(GATE_DIR, SCOPE.replace('/', '_') + '.json')
    with open(fpath, encoding='utf-8') as f:
        gate = json.load(f)
    ds = gate.setdefault(DS, {'fields': {}})

    added, skipped = 0, 0
    for fl in fields:
        fid = fl.get('id')
        if not fid:
            continue
        cov = fl.get('coverage', 1.0)
        ftype = fl.get('type', 'VECTOR')
        if fid not in ds['fields']:
            ds['fields'][fid] = {'type': ftype, 'coverage': cov}
            added += 1
        else:
            skipped += 1

    with open(fpath, 'w', encoding='utf-8') as f:
        json.dump(gate, f, ensure_ascii=False, indent=2)
    print(f'added={added} skipped={skipped} total={len(ds["fields"])}')

asyncio.run(main())
