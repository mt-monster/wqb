# -*- coding: utf-8 -*-
"""一次性大limit拉取analyst_consensus全字段(绕MCP翻页bug), 落盘本地过滤"""
import json, os, base64, http.cookiejar, urllib.request, io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
BASE = "https://api.worldquantbrain.com"
p = os.path.expanduser("~/.brain_credentials")
c = json.load(open(p, encoding="utf-8"))
jar = http.cookiejar.CookieJar()
op = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(jar))
enc = base64.b64encode(("%s:%s" % (c[0], c[1])).encode()).decode()
op.open(urllib.request.Request(BASE + "/authentication", data=b"",
        headers={"Authorization": "Basic " + enc}), timeout=60)
allr, off = [], 0
while True:
    url = (BASE + "/data-fields?instrumentType=EQUITY&region=KOR&delay=1&universe=TOP600"
           "&dataset.id=analyst_consensus&limit=50&offset=%d" % off)
    d = json.load(op.open(urllib.request.Request(url), timeout=120))
    rs = d.get('results', [])
    allr += rs
    if len(rs) < 50 or off > 3000:
        break
    off += 50
d['results'] = allr
out = r'd:\coding\traeCN_project\wqb\tracking\KOR\ac_fields.json'
json.dump(d, open(out, 'w', encoding='utf-8'), ensure_ascii=False)
rs = allr
print('total', len(rs), 'count', d.get('count'))
# 族统计
import re
from collections import Counter
fams = Counter('_'.join(r['id'].split('_')[:3]) for r in rs)
for f, n in fams.most_common(30):
    print(n, f)
