# -*- coding: utf-8 -*-
"""dump alpha 顶层 prod/test/train 键内容, 查 2y null 根因 (数据覆盖假设验证)。"""
import sys, os, asyncio, json

MCP_DIR = r'd:\coding\traeCN_project\wqb\world-quant-brain-mcp'
os.chdir(MCP_DIR)
sys.path.insert(0, MCP_DIR)
from brain_api import BrainApiClient  # noqa: E402

c = BrainApiClient()


def dump(o, depth=0, max_depth=3):
    pad = '  ' * depth
    if isinstance(o, dict):
        for k, v in o.items():
            if isinstance(v, (dict, list)) and depth < max_depth:
                print(f'{pad}{k}:')
                dump(v, depth + 1, max_depth)
            else:
                print(f'{pad}{k} = {json.dumps(v, default=str, ensure_ascii=False)[:200]}')
    elif isinstance(o, list):
        for i, v in enumerate(o[:10]):
            if isinstance(v, (dict, list)) and depth < max_depth:
                print(f'{pad}[{i}]:')
                dump(v, depth + 1, max_depth)
            else:
                print(f'{pad}[{i}] = {json.dumps(v, default=str, ensure_ascii=False)[:200]}')


async def main():
    await c.ensure_authenticated()
    for aid in sys.argv[1:]:
        r = await c._request('GET', f'{c.base_url}/alphas/{aid}?include_properties=true')
        a = r.json()
        is_ = a.get('is') or {}
        print(f'===== {aid} sharpe={is_.get("sharpe")} =====')
        for key in ('prod', 'test', 'train'):
            if key in a:
                print(f'--- {key} ---')
                dump(a[key])
            else:
                print(f'--- {key}: 不存在 ---')
        # 对比: 纯 obim 的 vRN7eLab (有 2y)
        print(f'--- checks ---')
        for ch in is_.get('checks', []):
            print(f'   check: {ch.get("name")} = {ch.get("value")}')
        rn = is_.get('riskNeutralized') or {}
        print(f'RN sharpe={rn.get("sharpe")} fit={rn.get("fitness")}')

asyncio.run(main())
