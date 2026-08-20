import json, sys
import os
sys.path.insert(0, os.environ.get("WQ_TOOLKIT", os.path.join(os.path.expanduser("~"), ".qoder-cn", "skills", "wq-brain-campaign-toolkit", "scripts")))
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

from _lib.ledger import LedgerStore

store = LedgerStore(r"D:\coding\traeCN_project\wqb\tracking\GBR\gbr_d1_campaign_state.json")

def mut(d):
    ws = d.setdefault("waves", {})
    if "17" not in ws:
        ws["17"] = {
            "dataset": "predictive_starmine",
            "note": ("24/24 backtested; top: fy2_3 momentum mix sh1.16 failed_checks=[] "
                     "(Wj7EPb7Z), fwdpe_mirror+ebitda 2y2.11 margin20bp (rKj15Oj9); "
                     "bucket group-unit poison 2ERROR+6CANCELLED"),
            "at": "2026-08-18T00:40:00",
        }
    verdict = json.load(open(
        r"D:\coding\traeCN_project\wqb\tracking\GBR\reviews\wave17_verdict.json",
        encoding="utf-8"))
    verdict.setdefault("recorded_at", "2026-08-18")
    d["wave17_verdict"] = verdict

store.update(mut)
print("ledger OK; waves keys:", sorted(store.load().get("waves", {}).keys()))
print("wave17_verdict recorded:", "wave17_verdict" in store.load())
