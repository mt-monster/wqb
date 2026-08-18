import json, os, base64, time, urllib.request, urllib.error

BASE = "https://api.worldquantbrain.com"
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "other455_fields.json")
c = json.load(open(os.path.expanduser("~/.brain_credentials"), encoding="utf-8"))
enc = base64.b64encode(("%s:%s" % (c[0], c[1])).encode()).decode()
op = urllib.request.build_opener()
op.open(urllib.request.Request(BASE + "/authentication", data=b"",
        headers={"Authorization": "Basic " + enc}), timeout=60)

url = BASE + "/data-fields?instrumentType=EQUITY&region=KOR&delay=1&universe=TOP600&dataset.id=other455&limit=100&offset=%d"
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
                wait = 10 * (attempt + 1)
                print("offset", offset, "429 sleep", wait, flush=True)
                time.sleep(wait)
            elif e.code == 400:
                print("offset", offset, "HTTP400 分页上限, 停止", flush=True)
                break
            else:
                print("offset", offset, "HTTP", e.code, flush=True)
                break
        except Exception as e:
            print("offset", offset, "attempt", attempt, e, flush=True)
            time.sleep(8)
    if d is None:
        break
    results = d.get("results", [])
    fields.extend(results)
    json.dump(fields, open(OUT, "w"), ensure_ascii=False)  # 增量落盘防中断丢失
    print("offset", offset, "got", len(results), "total", len(fields), flush=True)
    if len(results) < 100:
        break
    offset += 100
    time.sleep(3)

print("DONE total fields:", len(fields), flush=True)
types = {}
for f in fields:
    types[f.get("type")] = types.get(f.get("type"), 0) + 1
print("types:", types, flush=True)
