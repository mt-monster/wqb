"""拉取 dl_riskfree_returns KOR D1 全字段 -> 白名单 + 候选字段族分析"""
import json, os, base64, time, urllib.request, urllib.error

BASE = "https://api.worldquantbrain.com"
OUT = r"d:\coding\traeCN_project\wqb\tracking\KOR\reference\kor_dl_riskfree_returns_fields.json"
c = json.load(open(os.path.expanduser("~/.brain_credentials"), encoding="utf-8"))
enc = base64.b64encode(("%s:%s" % (c[0], c[1])).encode()).decode()
op = urllib.request.build_opener()
op.open(urllib.request.Request(BASE + "/authentication", data=b"",
        headers={"Authorization": "Basic " + enc}), timeout=60)

url = BASE + "/data-fields?instrumentType=EQUITY&region=KOR&delay=1&universe=TOP600&dataset.id=dl_riskfree_returns&limit=100&offset=%d"
fields = []
offset = 0
while True:
    d = None
    for attempt in range(5):
        try:
            r = op.open(url % offset, timeout=120)
            d = json.loads(r.read().decode())
            break
        except urllib.error.HTTPError as e:
            if e.code == 429:
                print("offset", offset, "429 sleep", 10 * (attempt + 1), flush=True)
                time.sleep(10 * (attempt + 1))
            else:
                print("offset", offset, "HTTP", e.code, flush=True)
                break
        except Exception as e:
            print("offset", offset, "err", e, flush=True)
            time.sleep(8)
    if d is None:
        break
    results = d.get("results", [])
    fields.extend(results)
    print("offset", offset, "total", len(fields), flush=True)
    if len(results) < 100:
        break
    offset += 100
    time.sleep(2)

json.dump(fields, open(OUT, "w"), ensure_ascii=False)
print("DONE total:", len(fields), flush=True)

# 字段族分析: 按 horizon/label 聚类
import re
fams = {}
for f in fields:
    fid = f.get("id", "")
    m = re.search(r"(\d+)day", fid)
    hz = m.group(1) + "d" if m else "?"
    fams.setdefault(hz, []).append(fid)
for hz, ids in sorted(fams.items()):
    print(hz, len(ids), "样例:", ids[:5], flush=True)
# 白名单(仅id)
wl = {"dataset": "dl_riskfree_returns", "region": "KOR", "delay": 1,
      "fields": sorted(f.get("id", "") for f in fields), "count": len(fields)}
json.dump(wl, open(r"d:\coding\traeCN_project\wqb\tracking\KOR\reference\kor_dl_riskfree_returns_field_whitelist.json", "w"), ensure_ascii=False, indent=1)
print("whitelist saved", flush=True)
