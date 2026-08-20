import json, sys
import os
sys.path.insert(0, os.environ.get("WQ_TOOLKIT", os.path.join(os.path.expanduser("~"), ".qoder-cn", "skills", "wq-brain-campaign-toolkit", "scripts")))
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

from _lib.ledger import LedgerStore

store = LedgerStore(r"D:\coding\traeCN_project\wqb\tracking\GBR\gbr_d1_campaign_state.json")

def mut(d):
    ws = d.setdefault("waves", {})
    if "18" not in ws:
        ws["18"] = {
            "dataset": "predictive_starmine",
            "note": ("16/16 backtested; top5 failed_checks=[] sh 1.04-1.19 <1.58 user gate; "
                     "fwdpe_mirror+ep_yield best (2y up to 2.05); starmine plateau, rotate next"),
            "at": "2026-08-18T01:00:00",
        }
    verdict = json.load(open(
        r"D:\coding\traeCN_project\wqb\tracking\GBR\reviews\wave18_verdict.json",
        encoding="utf-8"))
    verdict.setdefault("recorded_at", "2026-08-18")
    d["wave18_verdict"] = verdict

store.update(mut)
print("ledger OK; waves keys:", sorted(store.load().get("waves", {}).keys()))
