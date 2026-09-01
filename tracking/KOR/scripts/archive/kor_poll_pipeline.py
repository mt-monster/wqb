# -*- coding: utf-8 -*-
"""KOR战役轮询固化流水线: 状态查询 + 完成批自动拉指标, 一条命令闭环。

用法:
  python kor_poll_pipeline.py --multisim <id> [<id> ...] [--wait N] [--timeout M]
    --multisim : 一个或多个multisim ID(可多次传)
    --wait N   : 轮询初始间隔N秒(默认0=只查一次); >0 时循环轮询至 terminal
                 (指数退避至120s封顶), 复用同一登录
    --timeout M: 轮询总超时分钟(默认360); 挂起检测: progress 60min 无变化即放弃

行为:
  COMPLETE -> 复用 kor_fetch_metrics.py --multisim 拉全量指标(按sharpe降序)
  ERROR    -> 列出全部子模拟错误信息(逐个GET child取error; 不再截断前8个)
  其他     -> 打印 status/progress

凭证: ~/.brain_credentials (JSON list [email, password])
本脚本是战役唯一轮询入口, 禁止再写临时poll脚本(用户要求固化2026-08-15)。
2026-08-15 补丁(M13): --wait 改轮询循环+退避+挂起熔断; 单进程单登录; ERROR全量child。
"""
import json, sys, os, time, base64, http.cookiejar, urllib.request, urllib.error, subprocess

BASE = "https://api.worldquantbrain.com"
HERE = os.path.dirname(os.path.abspath(__file__))


def load_creds():
    p = os.path.expanduser("~/.brain_credentials")
    d = json.load(open(p, encoding="utf-8"))
    if isinstance(d, list) and len(d) >= 2:
        return d[0], d[1]
    raise RuntimeError("凭证缺失: ~/.brain_credentials 需为 [email, password] JSON list")


class Api:
    def __init__(self, email, password):
        self.jar = http.cookiejar.CookieJar()
        self.op = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(self.jar))
        enc = base64.b64encode(("%s:%s" % (email, password)).encode()).decode()
        req = urllib.request.Request(BASE + "/authentication", data=b"",
                                     headers={"Authorization": "Basic " + enc})
        self.op.open(req, timeout=60)

    def get(self, path):
        req = urllib.request.Request(BASE + path)
        return self.op.open(req, timeout=60)


def fetch_metrics(msid):
    """复用已固化的 kor_fetch_metrics.py, 返回其stdout文本"""
    py = sys.executable
    r = subprocess.run([py, "-X", "utf8", os.path.join(HERE, "kor_fetch_metrics.py"),
                        "--multisim=" + msid], capture_output=True, text=True,
                       encoding="utf-8", errors="replace")
    return r.stdout, r.stderr


def poll_once(api, msid):
    try:
        d = json.load(api.get("/simulations/" + msid))
    except urllib.error.HTTPError as e:
        return {"id": msid, "status": "HTTP_%d" % e.code}
    status = d.get("status")
    out = {"id": msid, "status": status, "progress": d.get("progress")}
    if status == "COMPLETE":
        stdout, _ = fetch_metrics(msid)
        out["metrics"] = [json.loads(l) for l in stdout.splitlines() if l.strip()]
    elif status == "ERROR":
        errs = []
        for c in (d.get("children") or []):  # M13: 全量 child（原 [:8] 截断会漏 >8 批次的错误）
            try:
                cs = json.load(api.get("/simulations/" + c))
                errs.append({"child": c, "error": cs.get("error", "")[:120]})
            except Exception as e:
                errs.append({"child": c, "error": str(e)[:80]})
        out["errors"] = errs
    return out


def main():
    args = sys.argv[1:]
    msids, wait, timeout_min = [], 0, 360
    i = 0
    while i < len(args):
        a = args[i]
        if a == "--multisim":
            i += 1
            msids.append(args[i])
        elif a.startswith("--multisim="):
            msids.append(a.split("=", 1)[1])
        elif a == "--wait":
            i += 1
            wait = int(args[i])
        elif a == "--timeout":
            i += 1
            timeout_min = int(args[i])
        i += 1
    if not msids:
        print("usage: kor_poll_pipeline.py --multisim <id> [...] [--wait N] [--timeout M]")
        sys.exit(1)
    api = Api(*load_creds())  # 单进程单登录（M13：原 --wait 复查会二次登录）
    results = {m: poll_once(api, m) for m in msids}
    if wait > 0:
        interval, waited = wait, 0
        last_change = {m: time.time() for m in msids}
        last_prog = {m: results[m].get("progress") for m in msids}
        while waited < timeout_min * 60:
            pending = [m for m in msids if results[m]["status"] not in ("COMPLETE", "ERROR", "STALLED")]
            if not pending:
                break
            time.sleep(interval)
            waited += interval
            interval = min(int(interval * 1.5), 120)  # 指数退避至 120s 封顶
            for m in pending:
                results[m] = poll_once(api, m)
                prog = results[m].get("progress")
                if prog != last_prog[m]:
                    last_prog[m], last_change[m] = prog, time.time()
                elif time.time() - last_change[m] > 3600:  # 挂起熔断（waveT 卡24h教训）
                    results[m]["status"] = "STALLED"
                    print(f"# {m} progress 60min 无变化，熔断放弃", file=sys.stderr)
    print(json.dumps([results[m] for m in msids], ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
