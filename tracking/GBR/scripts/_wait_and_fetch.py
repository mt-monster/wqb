import json, sys, time
sys.path.insert(0, r"C:/Users/MENGTAO/.qoder-cn/skills/wq-brain-campaign-toolkit/scripts")
from _lib.common import CampaignContext, atomic_write, load_credentials
from _lib.api import Api, api_call
from _lib.poller import TERMINAL
import metrics_cache

msid = sys.argv[1]
tag = sys.argv[2]
ctx = CampaignContext("tracking/GBR")
api = Api(); api.login(*load_credentials())
fetcher = metrics_cache.MetricsFetcher(ctx)

for _ in range(60):
    d = json.load(api.get(f"/simulations/{msid}"))
    status = d.get("status")
    print(f"[poll] {msid} status={status} progress={d.get('progress')}")
    if status in TERMINAL:
        break
    time.sleep(20)

rows = []
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
    rows.append(fetcher.fetch(aid))

out = f"tracking/GBR/results/5slot_{tag}_probe_results.json"
atomic_write(out, {"msid": msid, "results": rows})
print(f"[save] {out} rows={len(rows)}")
for r in sorted(rows, key=lambda x: -(x.get("sharpe") or -99)):
    print(f"{r['id']} {r.get('code','')[:60]:<60} sh={r.get('sharpe') or 0:.2f} fit={r.get('fitness') or 0:.2f} 2y={r.get('two_year_sharpe') or 0:.2f} mg={r.get('margin_bp') or 0:.1f}bp tvr={r.get('turnover_pct') or 0:.1f}% rn={r.get('rn_sharpe') or 0:.2f} fail={r.get('failed_checks') or '-'}")
