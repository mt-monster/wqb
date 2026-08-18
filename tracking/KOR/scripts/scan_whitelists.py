"""G1门补缺: 顺序扫描缺失白名单数据集(dl_riskfree_returns/other455/insider_feats)
长退避抗429; 每数据集增量落盘; 已存在的自动跳过"""
import json, os, base64, time, urllib.request, urllib.error

BASE = "https://api.worldquantbrain.com"
REF = r"d:\coding\traeCN_project\wqb\tracking\KOR\reference"
TARGETS = ["dl_riskfree_returns", "other455", "insider_feats"]
START_TS = time.time()
MAX_RUNTIME = 2400  # 总时长上限40分钟, 到点优雅退出防僵尸进程

c = json.load(open(os.path.expanduser("~/.brain_credentials"), encoding="utf-8"))
enc = base64.b64encode(("%s:%s" % (c[0], c[1])).encode()).decode()
op = urllib.request.build_opener()

def reauth():
    op.open(urllib.request.Request(BASE + "/authentication", data=b"",
            headers={"Authorization": "Basic " + enc}), timeout=60)
    print("  (重认证成功)", flush=True)

reauth()

def fetch_page(url):
    for attempt in range(10):
        if time.time() - START_TS > MAX_RUNTIME:
            return None, "总时长上限到"
        try:
            r = op.open(url, timeout=120)
            return json.loads(r.read().decode()), None
        except urllib.error.HTTPError as e:
            if e.code == 429:
                wait = min(60, 15 * (attempt + 1))
                print("  429 sleep", wait, flush=True)
                time.sleep(wait)
            elif e.code == 401:
                try:
                    reauth()
                except Exception as re_err:
                    print("  重认证失败:", re_err, flush=True)
                    time.sleep(10)
            elif e.code == 400:
                return None, "HTTP400"
            else:
                return None, "HTTP%d" % e.code
        except Exception as e:
            print("  err", e, "sleep 15", flush=True)
            time.sleep(15)
    return None, "429退避耗尽"

for ds in TARGETS:
    if time.time() - START_TS > MAX_RUNTIME:
        print("总时长上限到, 退出", flush=True)
        break
    dump_path = os.path.join(REF, "kor_%s_fields.json" % ds)
    wl_path = os.path.join(REF, "kor_%s_field_whitelist.json" % ds)
    if os.path.exists(wl_path) and os.path.getsize(wl_path) > 200:
        print(ds, "白名单已存在, 跳过", flush=True)
        continue
    # 断点续扫: 复用上次增量落盘的结果
    fields, offset = [], 0
    if os.path.exists(dump_path) and os.path.getsize(dump_path) > 10:
        try:
            fields = json.load(open(dump_path, encoding="utf-8"))
            offset = (len(fields) // 100) * 100
            print(ds, "续扫: 已有", len(fields), "offset=", offset, flush=True)
        except Exception:
            fields, offset = [], 0
    url = (BASE + "/data-fields?instrumentType=EQUITY&region=KOR&delay=1"
           "&universe=TOP600&dataset.id=%s&limit=100&offset=%%d" % ds)
    complete = False
    while True:
        d, err = fetch_page(url % offset)
        if d is None:
            print(ds, "offset", offset, "停止:", err, flush=True)
            break
        results = d.get("results", [])
        fields.extend(results)
        json.dump(fields, open(dump_path, "w"), ensure_ascii=False)
        print(ds, "offset", offset, "total", len(fields), flush=True)
        if len(results) < 100:
            complete = True
            break
        offset += 100
        time.sleep(10)
    # 防空白名单污染: 只有扫完(或已有非空结果)才写白名单
    if complete and fields:
        wl = {"dataset": ds, "region": "KOR", "delay": 1,
              "fields": sorted(f.get("id", "") for f in fields), "count": len(fields)}
        json.dump(wl, open(wl_path, "w"), ensure_ascii=False, indent=1)
        print(ds, "DONE count=", len(fields), flush=True)
    else:
        print(ds, "未完成(限流/错误), 保留增量 dump 待续扫, 不写白名单", flush=True)
    time.sleep(30)  # 数据集间冷却

print("ALL DONE", flush=True)
