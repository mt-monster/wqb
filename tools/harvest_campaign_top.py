"""收割全模板流水线的 top 候选数据集：取 alpha ID + 指标 + 表达式。
用法: python tools/harvest_campaign_top.py <ds1> <ds2> ...
"""
import asyncio
import json
import os
import sys

# MCP 目录走 _pyenv（$WQ_MCP_DIR 或 <repo>/world-quant-brain-mcp），wqb-scripts 走 $WQB_SCRIPTS 或 ~/wqb-scripts
import _pyenv  # noqa: E402  # tools/ 在 sys.path[0]
_pyenv.bootstrap_paths()
_wqb_scripts_dir = os.environ.get("WQB_SCRIPTS") or os.path.join(os.path.expanduser("~"), "wqb-scripts")
if _wqb_scripts_dir not in sys.path:
    sys.path.insert(0, _wqb_scripts_dir)

from brain_api import brain_client  # noqa: E402
from wqb_tools import _get_json  # noqa: E402

CK = 'results/full_template_campaign_checkpoint.json'
OUT = 'results/campaign_top_alphas.json'


def metrics(aj):
    m = aj.get('is') or {}
    ck = {x.get('name'): x for x in (m.get('checks') or []) if isinstance(x, dict)}
    y2 = m.get('twoYearSharpe')
    for nm in ('LOW_2Y_SHARPE', 'IS_LADDER_SHARPE'):
        v = (ck.get(nm) or {}).get('value')
        if v is not None:
            y2 = v
            break
    sub = m.get('subUniverseSharpe')
    sublim = None
    if (ck.get('LOW_SUB_UNIVERSE_SHARPE') or {}).get('value') is not None:
        sub = ck['LOW_SUB_UNIVERSE_SHARPE']['value']
        sublim = ck['LOW_SUB_UNIVERSE_SHARPE'].get('limit')
    return {
        's': m.get('sharpe'), 'f': m.get('fitness'), 'to': m.get('turnover'),
        'y2': y2, 'sub': sub, 'sublim': sublim,
        'ret': m.get('returns'),
    }


async def main():
    targets = sys.argv[1:]
    ck = json.load(open(CK, encoding='utf-8'))
    sims = ck.get('sims', {})
    out = {}
    await brain_client.ensure_authenticated()
    for ds in targets:
        lst = sims.get(ds, [])
        print(f'=== {ds}: {len(lst)} sims ===', flush=True)
        rows = []
        for sim, tpl, bi in lst:
            try:
                j = await _get_json(brain_client, f'/simulations/{sim}')
            except Exception as e:
                print(f'  {tpl}_{bi} sim-fail {str(e)[:50]}', flush=True)
                continue
            ch = j.get('children') or []
            got = 0
            for c in ch:
                try:
                    cj = await _get_json(brain_client, f'/simulations/{c}', tries=3, base_sleep=1.5)
                except Exception:
                    continue
                aid = cj.get('alpha')
                if not aid:
                    continue
                try:
                    aj = await _get_json(brain_client, f'/alphas/{aid}', tries=3, base_sleep=1.5)
                except Exception:
                    continue
                r = {'alpha': aid, 'tpl': tpl, 'sim': sim,
                     'code': (aj.get('regular') or {}).get('code') or ''}
                r.update(metrics(aj))
                rows.append(r)
                got += 1
            print(f'  {tpl}_{bi}: {got}/{len(ch)}', flush=True)
        out[ds] = rows
        ok = [r for r in rows if r['s'] is not None]
        ok.sort(key=lambda r: -(r['s'] or 0))
        print(f'  → {len(rows)} alphas, top3: ' +
              ', '.join(f"{r['alpha']}(S={r['s']},2Y={r['y2']})" for r in ok[:3]), flush=True)
    json.dump(out, open(OUT, 'w', encoding='utf-8'), indent=1)
    print('saved', OUT)


asyncio.run(main())
