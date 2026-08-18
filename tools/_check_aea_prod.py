import json, sys
sys.path.insert(0, 'C:/Users/MENGTAO/.qoder-cn/skills/wq-brain-campaign-toolkit/scripts')
from _lib.common import load_credentials
from _lib.api import Api, api_call
api = Api()
e, pw = load_credentials()
api.login(e, pw)
for aid in ['rKjpl3g3', 'omq8l2Xn']:
    r = api_call(api, 'GET', f'/alphas/{aid}')
    j = json.loads(r.read())
    # 打印所有 key 找 prod_corr 相关
    keys = [k for k in j.keys() if 'corr' in k.lower() or 'prod' in k.lower()]
    print(f'{aid}: corr_keys={keys}')
    for k in keys:
        print(f'  {k}={j[k]}')
    # 也查 is 下的字段
    is_data = j.get('is', {})
    if isinstance(is_data, dict):
        is_keys = [k for k in is_data.keys() if 'corr' in k.lower() or 'prod' in k.lower()]
        print(f'  is_corr_keys={is_keys}')
        for k in is_keys:
            print(f'  is.{k}={is_data[k]}')
