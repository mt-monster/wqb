"""离线验证 carrier_expand 双路径（拦截 dispatch，不真派发）。"""
import json
import os
import sqlite3
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.environ["WQB_REPO_ROOT"] = ROOT
sys.path.insert(0, os.path.join(os.path.expanduser("~"), ".workbuddy", "skills", "wq-brain-ra-eur", "scripts"))
sys.path.insert(0, os.path.join(ROOT, "world-quant-brain-mcp"))

import wqb_campaign.fields as F            # noqa: E402
from wqb_campaign.fields import select_fields, carrier_expand, probe_field_scores  # noqa: E402
from wqb_campaign.generate import DS_FREQ  # noqa: E402

# ---- 拦截真派发 ----
SENT = []
F.dispatch = lambda exprs, ds, label, on_batch=None: (
    SENT.append((ds, label, list(exprs))), [(f"FAKE{i}", t, 0) for i, (t, _) in enumerate(exprs)]
)[1]
F.save_ckpt = lambda ck: None


class Ck(dict):
    pass


con = sqlite3.connect(os.path.join(ROOT, "data", "wqb.db")); con.execute("PRAGMA busy_timeout=30000")
con.row_factory = sqlite3.Row
cat = {d: c for d, c in con.execute("select dataset,category from dataset_profile where region='EUR'")}
res = json.load(open(os.path.join(ROOT, "results", "full_template_campaign_results.json"),
                     encoding="utf-8"))["results"]
OCATS = ("ANALYST", "FUNDAMENTAL", "INSIDERS", "INSTITUTIONS", "EARNINGS", "MACRO")

for ds in ("pv87", "other545", "techindi_model", "multi_source_model"):
    v = res.get(ds) or {}
    alphas = v.get("alphas") or []
    best = {}
    for a in alphas:
        if a.get("s") is None:
            continue
        t = a.get("tpl")
        cur = best.setdefault(t, {"max_s": None, "max_2y": None})
        cur["max_s"] = a["s"] if cur["max_s"] is None else max(cur["max_s"], a["s"])

    min_cov = 0.5 if ds in ("pv87", "other545") else 0.6
    sel = select_fields(con, ds, field_min_cov=min_cov)
    freq = DS_FREQ.get(ds, "quarterly" if (cat.get(ds) or "").upper() in OCATS else "daily")
    ds_max = max((b["max_s"] or -9) for b in best.values()) if best else -9

    sc = probe_field_scores(sel, alphas)
    print(f"\n=== {ds}  集级max={ds_max:.2f}  probe字段数="
          f"{sum(1 for r in sel if r.get('tier') == 'probe')} ===")
    top = sorted(sc.items(), key=lambda kv: -kv[1])[:5]
    print("  探针字段自身 lvl_rk（top5）:", ", ".join(f"{f}={s:.2f}" for f, s in top) or "（无）")

    before = len(SENT)
    sims = carrier_expand(ds, sel, best, freq, Ck({"sims": {}}), len(best), all_alphas=alphas)
    if len(SENT) > before:
        _ds, _label, exprs = SENT[-1]
        print(f"  → 派发 {len(exprs)} 条:")
        for t, e in exprs[:5]:
            print(f"     [{t}] {e[:104]}")
    else:
        print(f"  → 未派发（sims={sims}）")
