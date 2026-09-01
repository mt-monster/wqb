# -*- coding: utf-8 -*-
"""探测回测配额: cookie登录 + 配额端点探测 + 今日sim计数"""
import json, os, base64, http.cookiejar, urllib.request, io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
BASE = "https://api.worldquantbrain.com"
c = json.load(open(os.path.expanduser("~/.brain_credentials"), encoding="utf-8"))
jar = http.cookiejar.CookieJar()
op = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(jar))
enc = base64.b64encode(("%s:%s" % (c[0], c[1])).encode()).decode()
op.open(urllib.request.Request(BASE + "/authentication", data=b"",
        headers={"Authorization": "Basic " + enc}), timeout=60)

def get(path):
    try:
        r = op.open(urllib.request.Request(BASE + path), timeout=60)
        return r.status, json.load(r)
    except Exception as e:
        return getattr(e, 'code', 'ERR'), str(getattr(e, 'read', lambda: b'')()[:200])

for p in ['/users/self/quota', '/simulations/limits', '/users/self/limits']:
    st, d = get(p)
    print('==', p, st)
    print(json.dumps(d, ensure_ascii=False)[:600] if isinstance(d, (dict, list)) else str(d)[:300])

st, d = get('/simulations?limit=5&offset=0')
print('== /simulations latest', st)
if isinstance(d, dict):
    print('total=', d.get('total'))
    for r in d.get('results', [])[:5]:
        print(' ', r.get('type'), r.get('status'), r.get('id'), str(r.get('createTime', r.get('lastUpdateTime', '')))[:19])
