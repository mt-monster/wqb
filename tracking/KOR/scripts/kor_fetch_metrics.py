# -*- coding: utf-8 -*-
"""KOR战役批量拉取alpha指标(标准库实现): 登录后逐个GET /alphas/{id}
用法: python kor_fetch_metrics.py <alpha_id> [<alpha_id> ...]
输出: stdout JSON表(id/sharpe/fitness/2y/margin_bp/turnover_pct/rn_sharpe/ra_failed)

2026-08-15 补丁(M12): 读穿本地缓存 cache/metrics/<alpha_id>.json(命中即返,写盘原子),
设 KOR_NO_CACHE=1 或传 --refresh 回源; multisim 分支复用同一登录(不再双登录)。"""
import json, sys, os, base64, urllib.request, urllib.error

BASE = "https://api.worldquantbrain.com"
CACHE_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "cache", "metrics")
os.makedirs(CACHE_DIR, exist_ok=True)

def load_creds():
    p = os.path.expanduser("~/.brain_credentials")
    d = json.load(open(p, encoding="utf-8"))
    if isinstance(d, list) and len(d) >= 2:
        return d[0], d[1]
    cfg = json.load(open(os.environ.get("MCP_CONFIG_FILE") or os.path.expanduser("~/.brain_mcp_config.json"), encoding="utf-8"))
    c = cfg.get("credentials", {})
    return c.get("email"), c.get("password")

class Api:
    def __init__(self):
        import http.cookiejar
        self.jar = http.cookiejar.CookieJar()
        self.op = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(self.jar))

    def post(self, path, payload=None, headers=None):
        data = json.dumps(payload).encode() if payload is not None else None
        h = {"Content-Type": "application/json"}
        if headers:
            h.update(headers)
        req = urllib.request.Request(BASE + path, data=data, headers=h)
        return self.op.open(req, timeout=60)

    def get(self, path):
        req = urllib.request.Request(BASE + path)
        return self.op.open(req, timeout=60)

    def login(self, email, password):
        enc = base64.b64encode(("%s:%s" % (email, password)).encode()).decode()
        req = urllib.request.Request(BASE + "/authentication", data=b"",
                                     headers={"Authorization": "Basic " + enc})
        self.op.open(req, timeout=60)

def main():
    ids = [a for a in sys.argv[1:] if a != "--refresh"]
    refresh = "--refresh" in sys.argv
    use_cache = os.environ.get("KOR_NO_CACHE") != "1"
    api = None  # 单进程单登录（multisim 分支与 per-alpha 循环复用）
    if ids and ids[0].startswith("--multisim="):
        msid = ids[0].split("=", 1)[1]
        api = Api()
        e, pw = load_creds()
        api.login(e, pw)
        ms = json.load(api.get("/simulations/" + msid))
        children = ms.get("children", [])
        ids = []
        for c in children:
            sim = json.load(api.get("/simulations/" + c))
            if sim.get("alpha"):
                ids.append(sim["alpha"])
            else:
                print("# child %s status=%s no alpha" % (c, sim.get("status")), file=sys.stderr)
        print("# multisim=%s children=%d alphas=%d" % (msid, len(children), len(ids)), file=sys.stderr)
    if not ids:
        print("usage: kor_fetch_metrics.py <alpha_id> ... [--refresh]")
        sys.exit(1)
    if api is None:
        email, password = load_creds()
        api = Api()
        api.login(email, password)
    rows = []
    for aid in ids:
        cp = os.path.join(CACHE_DIR, aid + ".json")
        if use_cache and not refresh and os.path.exists(cp):
            try:
                rows.append(json.load(open(cp, encoding="utf-8")))
                continue
            except Exception:
                pass  # 缓存损坏回源
        try:
            a = json.load(api.get("/alphas/" + aid))
        except urllib.error.HTTPError as e:
            rows.append({"id": aid, "error": "HTTP %d" % e.code})
            continue
        i = a.get("is") or {}
        rn = i.get("riskNeutralized") or {}
        checks = i.get("checks") or []
        two_y = None
        for c in checks:
            if c.get("name") == "LOW_2Y_SHARPE":
                two_y = c.get("value")
        failed = [c["name"] for c in checks if c.get("result") == "FAIL"]
        code = a.get("regular")
        if isinstance(code, dict):
            code = code.get("code", "")
        rows.append({
            "id": aid,
            "code": str(code or "")[:110],
            "neut": a.get("settings", {}).get("neutralization"),
            "sharpe": i.get("sharpe"),
            "fitness": i.get("fitness"),
            "two_year_sharpe": two_y,
            "margin_bp": round(i["margin"] * 10000, 2) if i.get("margin") is not None else None,
            "turnover_pct": round(i["turnover"] * 100, 2) if i.get("turnover") is not None else None,
            "rn_sharpe": rn.get("sharpe"),
            "rn_fitness": rn.get("fitness"),
            "failed_checks": failed,
        })
        if use_cache:  # M12: 原子写缓存
            tmp = cp + ".tmp"
            json.dump(rows[-1], open(tmp, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
            os.replace(tmp, cp)
    rows.sort(key=lambda r: -(r.get("sharpe") if r.get("sharpe") is not None else -99))
    for r in rows:
        print(json.dumps(r, ensure_ascii=False))

if __name__ == "__main__":
    main()
