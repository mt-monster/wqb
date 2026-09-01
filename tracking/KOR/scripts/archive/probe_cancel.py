# -*- coding: utf-8 -*-
"""深挖CANCELLED子任务详情"""
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
        return r.status, r.read().decode()
    except Exception as e:
        return getattr(e, 'code', 'ERR'), str(getattr(e, 'read', lambda: b'')()[:400])

# P55子任务 + 多sim父
for p in ['/simulations/2Sy7AD5X35fxcEKB0qeecbi', '/simulations/3HV3sy9a94Ofbubj6tVz8mC']:
    st, body = get(p)
    print('==', p, st)
    print(body[:1500])
    print()
