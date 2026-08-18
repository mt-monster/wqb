import json, sys
import os
sys.path.insert(0, os.environ.get("WQ_TOOLKIT", os.path.join(os.path.expanduser("~"), ".qoder-cn", "skills", "wq-brain-campaign-toolkit", "scripts")))
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

from _lib.ledger import LedgerStore

store = LedgerStore(r"D:\coding\traeCN_project\wqb\tracking\GBR\gbr_d1_campaign_state.json")

def mut(d):
    ws = d.setdefault("waves", {})
    if "20" not in ws:
        ws["20"] = {
            "dataset": "sentiment27",
            "note": ("24/24 backtested; Tranco web-traffic popularity weak in GBR D1 "
                     "(best sh0.59 2y1.71 all LOW_SHARPE); one wave and rotate, dead-ish"),
            "at": "2026-08-18T02:20:00",
        }
    verdict = json.load(open(
        r"D:\coding\traeCN_project\wqb\tracking\GBR\reviews\wave20_verdict.json",
        encoding="utf-8"))
    verdict.setdefault("recorded_at", "2026-08-18")
    d["wave20_verdict"] = verdict

store.update(mut)
print("ledger OK; waves keys:", sorted(store.load().get("waves", {}).keys()))
