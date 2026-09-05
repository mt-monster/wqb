# -*- coding: utf-8 -*-
"""metrics_cache.py - alpha IS 指标拉取 + 本地读穿缓存。

  - 单进程单登录（Api 实例复用）
  - cache/metrics/<alpha_id>.json 读穿缓存，命中即返；写盘原子（tmp+os.replace）
  - 输出 JSON lines（按 sharpe 降序）
  - CAMPAIGN_NO_CACHE=1 或 --refresh 强制回源

用法:
  python metrics_cache.py --campaign-dir <DIR> <alpha_id> [<alpha_id> ...] [--refresh] [--no-cache]
  python metrics_cache.py --campaign-dir <DIR> --multisim=<id> [--refresh]
作为模块:
  from metrics_cache import fetch_rows        # fetch_rows(ctx, [ids]) -> [row,...]
"""
import datetime
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _lib.common import (CampaignContext, add_campaign_arg, atomic_write, load_credentials,
                         load_json)
from _lib.api import Api


def row_from_alpha(aid, a):
    """从 GET /alphas/{id} 响应提取指标行（margin*10000、turnover*100 单位换算）。"""
    i = a.get("is") or {}
    rn = i.get("riskNeutralized") or {}
    checks = i.get("checks") or []
    two_y = next((c.get("value") for c in checks if c.get("name") == "LOW_2Y_SHARPE"), None)
    # BUG-1 修复（规则 metrics_cache_2y_fallback_bug）：跨 dataset 复合表达式的 checks
    # 不含 LOW_2Y_SHARPE 项（wave6/6b/6c 24 行全 None），fallback 到 is 顶层字段。
    if two_y is None:
        two_y = (i.get("two_year_sharpe") or i.get("twoYearSharpe")
                 or i.get("sharpe2y") or i.get("twoYear"))
    if isinstance(two_y, dict):  # 平台偶发返回 {value:..} 嵌套
        two_y = two_y.get("value")
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

    def __init__(self, ctx, use_cache=True):
        self.ctx = ctx
        self.api = None
        self.use_cache = use_cache and os.environ.get("CAMPAIGN_NO_CACHE") != "1"
        self.cache_dir = ctx.cache_path("metrics")
        os.makedirs(self.cache_dir, exist_ok=True)

    def _login(self):
        if self.api is None:
            e, pw = load_credentials()
            self.api = Api()
            self.api.login(e, pw)
        return self.api

    def fetch(self, aid, refresh=False):
        cp = os.path.join(self.cache_dir, f"{aid}.json")
        if self.use_cache and not refresh and os.path.exists(cp):
            try:
                return load_json(cp)
            except Exception:
                pass  # 缓存损坏则回源
        api = self._login()
        try:
            a = json.load(api.get("/alphas/" + aid))
        except Exception as e:
            code = getattr(e, "code", None)
            return {"id": aid, "error": f"HTTP {code}" if code else str(e)[:80]}
        row = row_from_alpha(aid, a)
        if self.use_cache:
            atomic_write(cp, row)
        return row

    def multisim_alpha_ids(self, msid):
        """解析 multisim 的 child alpha id 列表（全量 child 不截断；复用同一登录）。"""
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


def fetch_rows(ctx, ids, use_cache=True, refresh=False):
    f = MetricsFetcher(ctx, use_cache=use_cache)
    rows = [f.fetch(a, refresh=refresh) for a in ids]
    rows.sort(key=lambda r: -(r.get("sharpe") if r.get("sharpe") is not None else -99))
    return rows


def main():
    import argparse
    ap = argparse.ArgumentParser(description="alpha IS 指标拉取 + 读穿缓存")
    add_campaign_arg(ap)
    ap.add_argument("ids", nargs="*", help="alpha_id 列表")
    ap.add_argument("--multisim", default=None, help="解析 multisim 的 child alpha")
    ap.add_argument("--refresh", action="store_true", help="绕过缓存强制回源")
    ap.add_argument("--no-cache", action="store_true")
    a = ap.parse_args()
    ctx = CampaignContext(a.campaign_dir)
    f = MetricsFetcher(ctx, use_cache=not a.no_cache)
    if a.multisim:
        ids = f.multisim_alpha_ids(a.multisim)
        print(f"# multisim children resolved: {len(ids)}", file=sys.stderr)
    else:
        ids = a.ids
    if not ids:
        ap.error("need alpha_id 列表或 --multisim=<id>")
    rows = [f.fetch(x, refresh=a.refresh) for x in ids]
    rows.sort(key=lambda r: -(r.get("sharpe") if r.get("sharpe") is not None else -99))
    for r in rows:
        print(json.dumps(r, ensure_ascii=False))


if __name__ == "__main__":
    main()
