# -*- coding: utf-8 -*-
"""metrics_cache.py - alpha IS 指标拉取 + 本地缓存（M12）。

解决：kor_fetch_metrics.py 每次 review 重复 GET /alphas/{id}、每进程多次登录。
设计：
  - 单进程单登录（Api 实例复用）
  - cache/metrics/<alpha_id>.json 读穿缓存，命中即返；写盘原子（tmp+os.replace）
  - 输出 JSON lines（按 sharpe 降序），行格式与 kor_fetch_metrics.py 兼容

用法:
  python metrics_cache.py <alpha_id> [<alpha_id> ...] [--refresh] [--no-cache]
  python metrics_cache.py --multisim=<id> [--refresh]
作为模块:
  from metrics_cache import fetch_rows        # fetch_rows([ids]) -> [row,...]
"""
import datetime
import json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
CACHE_DIR = os.path.join(ROOT, "cache", "metrics")
os.makedirs(CACHE_DIR, exist_ok=True)

sys.path.insert(0, HERE)
from kor_fetch_metrics import Api, load_creds  # 复用已固化的 Api/凭证


def _cache_path(aid):
    return os.path.join(CACHE_DIR, f"{aid}.json")


def _atomic_write(path, obj):
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=1)
    os.replace(tmp, path)


def row_from_alpha(aid, a):
    """从 GET /alphas/{id} 响应提取指标行（与 kor_fetch_metrics 行格式一致）。"""
    i = a.get("is") or {}
    rn = i.get("riskNeutralized") or {}
    checks = i.get("checks") or []
    two_y = next((c.get("value") for c in checks if c.get("name") == "LOW_2Y_SHARPE"), None)
    failed = [c["name"] for c in checks if c.get("result") == "FAIL"]
    code = a.get("regular")
    if isinstance(code, dict):
        code = code.get("code", "")
    return {
        "id": aid,
        "code": str(code or "")[:110],
        "neut": (a.get("settings") or {}).get("neutralization"),
        "sharpe": i.get("sharpe"),
        "fitness": i.get("fitness"),
        "two_year_sharpe": two_y,
        "margin_bp": round(i["margin"] * 10000, 2) if i.get("margin") is not None else None,
        "turnover_pct": round(i["turnover"] * 100, 2) if i.get("turnover") is not None else None,
        "rn_sharpe": rn.get("sharpe"),
        "rn_fitness": rn.get("fitness"),
        "failed_checks": failed,
        "cached_at": datetime.datetime.now().isoformat(timespec="seconds"),
    }


class MetricsFetcher:
    """单登录复用；读穿缓存。"""

    def __init__(self, use_cache=True):
        self.api = None
        self.use_cache = use_cache

    def _login(self):
        if self.api is None:
            e, pw = load_creds()
            self.api = Api()
            self.api.login(e, pw)
        return self.api

    def fetch(self, aid, refresh=False):
        cp = _cache_path(aid)
        if self.use_cache and not refresh and os.path.exists(cp):
            try:
                return json.load(open(cp, encoding="utf-8"))
            except Exception:
                pass  # 缓存损坏则回源
        api = self._login()
        try:
            a = json.load(api.get("/alphas/" + aid))
        except Exception as e:
            code = getattr(e, "code", None)
            return {"id": aid, "error": f"HTTP {code}" if code else str(e)[:80]}
        row = row_from_alpha(aid, a)
        _atomic_write(cp, row)
        return row

    def multisim_alpha_ids(self, msid):
        """解析 multisim 的 child alpha id 列表（复用同一登录，无双登录）。"""
        api = self._login()
        ms = json.load(api.get("/simulations/" + msid))
        ids = []
        for c in ms.get("children", []):
            try:
                sim = json.load(api.get("/simulations/" + c))
                if sim.get("alpha"):
                    ids.append(sim["alpha"])
                else:
                    print(f"# child {c} status={sim.get('status')} no alpha", file=sys.stderr)
            except Exception as e:
                print(f"# child {c} err {e}", file=sys.stderr)
        return ids


def fetch_rows(ids, use_cache=True, refresh=False):
    f = MetricsFetcher(use_cache=use_cache)
    rows = [f.fetch(a, refresh=refresh) for a in ids]
    rows.sort(key=lambda r: -(r.get("sharpe") if r.get("sharpe") is not None else -99))
    return rows


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--no-") and a != "--refresh"]
    use_cache = "--no-cache" not in sys.argv
    refresh = "--refresh" in sys.argv
    f = MetricsFetcher(use_cache=use_cache)
    ids = []
    if args and args[0].startswith("--multisim="):
        ids = f.multisim_alpha_ids(args[0].split("=", 1)[1])
        print(f"# multisim children resolved: {len(ids)}", file=sys.stderr)
    else:
        ids = args
    if not ids:
        print("usage: metrics_cache.py <alpha_id>... | --multisim=<id> [--refresh] [--no-cache]")
        sys.exit(1)
    rows = [f.fetch(a, refresh=refresh) for a in ids]
    rows.sort(key=lambda r: -(r.get("sharpe") if r.get("sharpe") is not None else -99))
    for r in rows:
        print(json.dumps(r, ensure_ascii=False))


if __name__ == "__main__":
    main()
