#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run news20 repair4: settings-variant batches (startDate windowing, decay, neut)."""
import json, sys, time
from pathlib import Path

TOOLKIT = Path("C:/Users/MENGTAO/.qoder-cn/skills/wq-brain-campaign-toolkit/scripts")
sys.path.insert(0, str(TOOLKIT))

from _lib.common import CampaignContext, atomic_write, load_credentials
from _lib.api import Api, api_call
from _lib.poller import TERMINAL
import metrics_cache

EXPRS = json.load(open("tracking/GBR/candidates/probe_news20_repair4_exprs.json", encoding="utf-8"))

VARIANTS = [
    {"tag": "sd2018", "overrides": {"startDate": "2018-01-01"}},
    {"tag": "sd2019", "overrides": {"startDate": "2019-01-01"}},
    {"tag": "sd2018_d6", "overrides": {"startDate": "2018-01-01", "decay": 6}},
    {"tag": "sd2018_stat", "overrides": {"startDate": "2018-01-01", "neutralization": "STATISTICAL"}},
    {"tag": "sd2018_d2", "overrides": {"startDate": "2018-01-01", "decay": 2}},
    {"tag": "sd2020", "overrides": {"startDate": "2020-01-01"}},
]

ctx = CampaignContext("tracking/GBR")
api = Api(); api.login(*load_credentials())
fetcher = metrics_cache.MetricsFetcher(ctx)

out_dir = Path("tracking/GBR/results")
all_rows = []

for v in VARIANTS:
    settings = {k: val for k, val in ctx.settings.items() if not k.startswith("_")}
    settings.update(v["overrides"])
    payloads = [{"type": "REGULAR", "settings": settings, "regular": e} for e in EXPRS]
    r = api_call(api, "post", "/simulations", payloads)
    loc = r.headers.get("Location") or ""
    msid = loc.rstrip("/").split("/")[-1]
    print(f"[submit] {v['tag']} multisim={msid} n={len(payloads)}")
    for _ in range(60):
        d = json.load(api.get(f"/simulations/{msid}"))
        if d.get("status") in TERMINAL:
            break
        time.sleep(20)
    print(f"[poll] {msid} -> {d.get('status')}")
    ms = json.load(api.get(f"/simulations/{msid}"))
    ids = []
    for c in ms.get("children", []):
        try:
            sim = json.load(api.get(f"/simulations/{c}"))
            if sim.get("alpha"):
                ids.append(sim["alpha"])
        except Exception as e:
            print(f"[child] {c} err {e}", file=sys.stderr)
    if not ids and ms.get("alpha"):
        ids.append(ms["alpha"])
    for aid in ids:
        row = fetcher.fetch(aid)
        row["variant"] = v["tag"]
        row["code"] = EXPRS[len(all_rows) % len(EXPRS)] if isinstance(row, dict) else None
        all_rows.append(row)
    out = out_dir / f"5slot_news20_repair4_{v['tag']}.json"
    atomic_write(str(out), {"msid": msid, "results": all_rows})

print("\n=== ALL VARIANTS (top by sharpe) ===")
flat = [r for r in all_rows if isinstance(r, dict) and r.get("sharpe") is not None]
flat.sort(key=lambda x: -(x.get("sharpe") or -99))
for r in flat[:16]:
    print(f"{r.get('variant',''):<12} sh={r.get('sharpe') or 0:.2f} fit={r.get('fitness') or 0:.2f} 2y={r.get('two_year_sharpe') or 0:.2f} mg={r.get('margin_bp') or 0:.1f}bp tvr={r.get('turnover_pct') or 0:.1f}% rn={r.get('rn_sharpe') or 0:.2f} fail={r.get('failed_checks') or '-'}")
